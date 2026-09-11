# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2025 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""OrcaRouter credential seam.

Both user-facing authentication choices -- pasting an ``sk-orca-...`` key
and the OAuth 2.0 + PKCE connect flow -- end here, producing **one** ordinary
OrcaRouter API key.  Downstream code (inference adapter, model discovery)
consumes :class:`QAOrcaCredentialProvider` and never learns which choice
produced the key.

Storage reuses what QUANTAXIS already uses for local settings: a file under
``~/.quantaxis/setting`` written with ``0600`` permissions, created on demand
by :mod:`QUANTAXIS.QASetting.QALocalize`.  No new secret store is introduced.
An ``ORCAROUTER_API_KEY`` environment variable still takes precedence, matching
the repository's existing ``MONGOURI``-style environment override convention.
"""

import json
import os
import stat
import threading
import time

from QUANTAXIS.QAAI.QAOrcaEndpoints import ORCA_ENV_API_KEY

__all__ = [
    'ORCA_KEY_PREFIX',
    'ORCA_SOURCE_API_KEY',
    'ORCA_SOURCE_OAUTH_PKCE',
    'CREDENTIAL_NEEDS_REAUTH',
    'CREDENTIAL_OK',
    'QAOrcaCredentialError',
    'QAOrcaCredentialResult',
    'QAOrcaCredentialProvider',
    'QAOrcaApiKeyAdapter',
    'QAOrcaCredentialStore',
    'mask_key',
    'looks_like_orcarouter_key',
    'classify_auth_failure',
    'default_credential_path',
]

ORCA_KEY_PREFIX = 'sk-orca-'
ORCA_SOURCE_API_KEY = 'api_key'
ORCA_SOURCE_OAUTH_PKCE = 'oauth_pkce'

CREDENTIAL_OK = 'ok'
CREDENTIAL_NEEDS_REAUTH = 'needs_reauth'

#: Environment variable that overrides the on-disk credential location.  It
#: exists so tests and throwaway sandboxes never touch a real user profile.
CREDENTIAL_PATH_ENV = 'QA_ORCAROUTER_CREDENTIAL_FILE'


class QAOrcaCredentialError(Exception):
    """Raised for unusable credentials and credential-store failures."""


def default_credential_path():
    """Return the credential file path without importing the heavy package."""
    override = os.environ.get(CREDENTIAL_PATH_ENV)
    if override:
        return override
    return os.path.join(
        os.path.expanduser('~'),
        '.quantaxis',
        'setting',
        'orcarouter.json',
    )


def mask_key(key):
    """Return a redacted rendering of ``key`` safe for logs and UI.

    Only a fixed prefix and the last four characters survive; the middle is
    replaced by a constant number of asterisks so the mask reveals nothing
    about the key length either.
    """
    if not key:
        return ''
    if len(key) <= 12:
        return '****'
    return '{0}{1}{2}'.format(key[:8], '*' * 6, key[-4:])


def looks_like_orcarouter_key(key):
    """Lightweight format check.

    The ``sk-orca-`` prefix only catches obvious input mistakes; it is not
    proof that a credential is valid, and no paid request is issued to
    "validate" a key in a settings form.
    """
    return bool(key) and isinstance(
        key,
        str
    ) and key.startswith(ORCA_KEY_PREFIX) and len(
        key
    ) > len(ORCA_KEY_PREFIX) + 8 and ' ' not in key


def classify_auth_failure(status_code, body=None):
    """Map an OrcaRouter response to a credential lifecycle decision.

    ``401`` is terminal: the durable key was revoked or is wrong, and the
    only remedy is to re-run the connect flow.  ``429`` and transport
    failures are transient and must not touch stored credentials.
    """
    if status_code == 401:
        return CREDENTIAL_NEEDS_REAUTH
    if status_code == 403:
        # A granted scope that no longer covers this request; also terminal
        # for the stored credential until the user re-authorizes.
        return CREDENTIAL_NEEDS_REAUTH
    return 'transient'


class QAOrcaCredentialResult(object):
    """A credential handed to downstream consumers.

    The shape is identical for both authentication choices: an ordinary
    OrcaRouter API key plus the account it belongs to.
    """

    def __init__(self, api_key, source, account_id, scope='api'):
        self.api_key = api_key
        self.source = source
        self.account_id = account_id
        self.scope = scope

    def as_dict(self):
        return {
            'api_key': self.api_key,
            'source': self.source,
            'account_id': self.account_id,
            'scope': self.scope,
        }

    def redacted(self):
        return {
            'api_key': mask_key(self.api_key),
            'source': self.source,
            'account_id': self.account_id,
            'scope': self.scope,
        }

    def __repr__(self):
        # Never render the key itself.
        return 'QAOrcaCredentialResult(api_key={0!r}, source={1!r}, ' \
               'account_id={2!r}, scope={3!r})'.format(
                   mask_key(self.api_key),
                   self.source,
                   self.account_id,
                   self.scope,
               )


class QAOrcaCredentialProvider(object):
    """The seam.

    Downstream code (proxy, model catalog, CLI, web handlers) depends on this
    interface only, so it is structurally impossible for a consumer to behave
    differently depending on which authentication choice produced the key.
    """

    #: Identifier of the authentication choice, for status display only.
    source = None

    def acquire(self):
        """Return a :class:`QAOrcaCredentialResult` or raise.

        Implementations must never log, print or return the key inside an
        error message.
        """
        raise NotImplementedError

    def api_key(self):
        return self.acquire().api_key


class QAOrcaApiKeyAdapter(QAOrcaCredentialProvider):
    """Authentication choice 1: a user-supplied ``sk-orca-...`` key.

    Resolution order is explicit argument -> ``ORCAROUTER_API_KEY`` -> the
    project's stored credential.  The key is persisted through the same store
    the PKCE adapter uses.
    """

    source = ORCA_SOURCE_API_KEY

    def __init__(self, store=None, api_key=None, env=None, account_id=None):
        self.store = store or QAOrcaCredentialStore()
        self._explicit = api_key
        self._env = os.environ if env is None else env
        self.account_id = account_id

    def _from_env(self):
        return self._env.get(ORCA_ENV_API_KEY)

    def save(self, api_key, account_id=None):
        """Persist a pasted key after a light format check."""
        if not looks_like_orcarouter_key(api_key):
            raise QAOrcaCredentialError(
                'that does not look like an OrcaRouter key; expected the '
                'sk-orca- prefix'
            )
        return self.store.save(
            api_key=api_key,
            source=ORCA_SOURCE_API_KEY,
            account_id=account_id or self.account_id or 'orcarouter-api-key',
        )['account_id']

    def acquire(self):
        explicit = self._explicit or self._from_env()
        if explicit:
            return QAOrcaCredentialResult(
                api_key=explicit,
                source=ORCA_SOURCE_API_KEY,
                account_id=self.account_id or 'orcarouter-api-key',
            )
        credential = self.store.load(self.account_id)
        if credential is None:
            raise QAOrcaCredentialError(
                'no OrcaRouter API key configured; run `orcarouter login '
                '--key <sk-orca-...>` or set ORCAROUTER_API_KEY'
            )
        return QAOrcaCredentialResult(
            api_key=credential['api_key'],
            source=credential.get('source',
                                  ORCA_SOURCE_API_KEY),
            account_id=credential['account_id'],
            scope=credential.get('scope',
                                 'api'),
        )

    def clear(self):
        return self.store.clear(self.account_id)


class QAOrcaCredentialStore(object):
    """JSON credential store with generation-guarded ``401`` transitions."""

    VERSION = 1

    def __init__(self, path=None):
        self.path = path or default_credential_path()
        self._lock = threading.Lock()

    # -- low level ------------------------------------------------------
    def _read(self):
        try:
            with open(self.path, 'r') as handle:
                data = json.load(handle)
        except (IOError, OSError):
            return {'version': self.VERSION, 'accounts': {}}
        except ValueError:
            # A corrupt store must not take the process down; the user is
            # asked to re-authenticate instead.
            return {'version': self.VERSION, 'accounts': {}}
        if not isinstance(data, dict):
            return {'version': self.VERSION, 'accounts': {}}
        data.setdefault('accounts', {})
        return data

    def _write(self, data):
        directory = os.path.dirname(os.path.abspath(self.path))
        if directory and not os.path.isdir(directory):
            os.makedirs(directory, mode=0o700, exist_ok=True)
        tmp = '{0}.tmp'.format(self.path)
        with open(tmp, 'w') as handle:
            json.dump(data, handle, indent=2, sort_keys=True)
        os.chmod(tmp, stat.S_IRUSR | stat.S_IWUSR)
        os.replace(tmp, self.path)
        os.chmod(self.path, stat.S_IRUSR | stat.S_IWUSR)

    # -- public API -----------------------------------------------------
    def active_account_id(self):
        with self._lock:
            return self._read().get('active')

    def accounts(self):
        with self._lock:
            return self._read().get('accounts', {})

    def load(self, account_id=None, allow_needs_reauth=False):
        with self._lock:
            data = self._read()
            accounts = data.get('accounts', {})
            account_id = account_id or data.get('active')
            if account_id is None and len(accounts) == 1:
                account_id = list(accounts)[0]
            record = accounts.get(account_id)
            if record is None:
                return None
            if record.get('needs_reauth') and not allow_needs_reauth:
                return None
            record = dict(record)
            record['account_id'] = account_id
            return record

    def save(self, api_key, source, account_id, scope='api'):
        """Persist ``api_key`` and return the stored record.

        The previous record is only replaced once the new key is in hand, so
        a failed login can never destroy a working credential.
        """
        with self._lock:
            data = self._read()
            accounts = data.setdefault('accounts', {})
            previous = accounts.get(account_id) or {}
            generation = int(previous.get('generation', 0)) + 1
            record = {
                'api_key': api_key,
                'source': source,
                'scope': scope,
                'generation': generation,
                'needs_reauth': False,
                'created_at': previous.get('created_at',
                                           time.time()),
                'updated_at': time.time(),
            }
            accounts[account_id] = record
            data['active'] = account_id
            self._write(data)
            stored = dict(record)
            stored['account_id'] = account_id
            return stored

    def clear(self, account_id=None):
        """Remove a stored credential.  Returns True when something was removed."""
        with self._lock:
            data = self._read()
            accounts = data.setdefault('accounts', {})
            account_id = account_id or data.get('active')
            if account_id not in accounts:
                return False
            accounts.pop(account_id)
            if data.get('active') == account_id:
                data['active'] = next(iter(accounts), None)
            self._write(data)
            return True

    def mark_needs_reauth(self, account_id, generation=None):
        """Flag exactly one account generation as requiring reauthentication.

        A late ``401`` from a request issued against an older credential
        generation must never invalidate a credential the user has since
        replaced; passing the generation makes that check explicit.
        """
        with self._lock:
            data = self._read()
            accounts = data.setdefault('accounts', {})
            record = accounts.get(account_id)
            if record is None:
                return False
            if generation is not None and int(record.get('generation',
                                                         0)) != int(generation):
                # Stale failure: a newer credential already replaced this one.
                return False
            record['needs_reauth'] = True
            record['updated_at'] = time.time()
            self._write(data)
            return True

    def clear_needs_reauth(self, account_id=None):
        with self._lock:
            data = self._read()
            accounts = data.setdefault('accounts', {})
            account_id = account_id or data.get('active')
            record = accounts.get(account_id)
            if record is None:
                return False
            record['needs_reauth'] = False
            self._write(data)
            return True

    def status(self, account_id=None):
        """Redacted status for UI consumption.  Never returns the key."""
        with self._lock:
            data = self._read()
            accounts = data.get('accounts', {})
            active = data.get('active')
            account_id = account_id or active
            record = accounts.get(account_id)
            if record is None:
                return {
                    'configured': False,
                    'active_account': None,
                    'accounts': [],
                }
            entry = {
                'account_id': account_id,
                'source': record.get('source'),
                'scope': record.get('scope',
                                    'api'),
                'generation': record.get('generation',
                                         1),
                'needs_reauth': bool(record.get('needs_reauth')),
                'api_key_masked': mask_key(record.get('api_key')),
                'active': account_id == active,
            }
            return {
                'configured': True,
                'active_account': account_id,
                'accounts': [entry],
            }
