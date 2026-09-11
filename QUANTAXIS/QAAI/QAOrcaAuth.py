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
"""OrcaRouter OAuth 2.0 + PKCE connect flows.

Flow B (out-of-band code) is the primary flow, and Flow A (loopback
redirect) is implemented as well because a developer running the CLI on
their own workstation can use the automatic callback.  Flow C (device
grant) is *not* implemented; the integration guidance explicitly allows
choosing one flow, and QUANTAXIS is self-hosted software whose panel address
differs on every deployment -- the situation Flow B exists for.

Security invariants enforced here, and covered by tests:

* a fresh ``verifier`` and ``state`` are drawn from a cryptographic RNG for
  every attempt;
* the challenge is ``base64url(sha256(verifier))`` with padding stripped, and
  ``S256`` is always sent -- including on Flow A, because the user may choose
  "show me a code" on the consent screen;
* the verifier never leaves this process until the exchange, and is never
  placed in a URL, a log line, or an exception message;
* Flow A compares ``state`` in constant time before touching the code;
* the ``scope`` returned by the exchange is what was *granted*; a downgrade
  is reported rather than ignored;
* the exchanged key is a durable API key, not a refresh token, so nothing
  here ever attempts a refresh grant.
"""

import base64
import hashlib
import hmac
import http.server
import json
import secrets
import socket
import threading
import urllib.error
import urllib.parse
import urllib.request

from QUANTAXIS.QAAI.QAOrcaCredential import (
    ORCA_SOURCE_OAUTH_PKCE,
    QAOrcaCredentialError,
    QAOrcaCredentialResult,
    QAOrcaCredentialProvider,
    QAOrcaCredentialStore,
    looks_like_orcarouter_key,
)
from QUANTAXIS.QAAI.QAOrcaEndpoints import (
    ORCA_APP_NAME,
    resolve_endpoints,
)

__all__ = [
    'FLOW_LOOPBACK',
    'FLOW_OUT_OF_BAND',
    'ORCA_REQUIRED_SCOPE',
    'QAOrcaPkceError',
    'QAOrcaAuthDenied',
    'QAOrcaAuthTimeout',
    'QAOrcaScopeDowngrade',
    'generate_verifier',
    'generate_state',
    'code_challenge_for',
    'build_authorize_url',
    'parse_callback_url',
    'exchange_code',
    'QAOrcaPkceAdapter',
    'QAOrcaLoopbackListener',
    'QAOrcaLoginSession',
]

FLOW_LOOPBACK = 'loopback'
FLOW_OUT_OF_BAND = 'oob'

#: The scope this integration asks for, and the only scope it accepts as
#: sufficient for its own use.
ORCA_REQUIRED_SCOPE = 'api'

CALLBACK_PATH = '/cb'

DEFAULT_TIMEOUT = 300.0
DEFAULT_EXCHANGE_TIMEOUT = 30.0
_MAX_RESPONSE_BYTES = 64 * 1024


class QAOrcaPkceError(QAOrcaCredentialError):
    """Base class for connect-flow failures.  Never carries the verifier."""


class QAOrcaAuthDenied(QAOrcaPkceError):
    """The user declined, or the consent server returned an error."""


class QAOrcaAuthTimeout(QAOrcaPkceError):
    """The authorization window closed before a code arrived."""


class QAOrcaScopeDowngrade(QAOrcaPkceError):
    """The exchange succeeded but granted less than the requested scope."""


def _b64url(raw):
    return base64.urlsafe_b64encode(raw).decode('ascii').rstrip('=')


def generate_verifier(nbytes=32):
    """A fresh, high-entropy PKCE verifier from the OS cryptographic RNG."""
    return _b64url(secrets.token_bytes(nbytes))


def generate_state(nbytes=16):
    """A fresh CSRF state value from the OS cryptographic RNG."""
    return _b64url(secrets.token_bytes(nbytes))


def code_challenge_for(verifier):
    """``base64url(sha256(verifier))`` with no padding."""
    return _b64url(hashlib.sha256(verifier.encode('ascii')).digest())


def build_authorize_url(
    endpoints,
    challenge,
    state,
    flow,
    app_name=ORCA_APP_NAME,
    callback_port=None,
    scope=ORCA_REQUIRED_SCOPE,
    login_hint=None,
    extra=None,
):
    """Compose the consent-screen URL.

    ``callback_url`` is either the literal ``oob`` or a loopback address the
    listener already holds open.  ``code_challenge_method`` is always
    ``S256``.
    """
    params = {
        'callback_url':
            (
                'oob' if flow == FLOW_OUT_OF_BAND else
                'http://127.0.0.1:{0}{1}'.format(callback_port,
                                                 CALLBACK_PATH)
            ),
        'code_challenge': challenge,
        'code_challenge_method': 'S256',
        'state': state,
        'app_name': app_name,
        'scope': scope,
    }
    if login_hint:
        params['login_hint'] = login_hint
    if extra:
        for key, value in extra.items():
            if value is not None:
                params[key] = value
    return '{0}?{1}'.format(
        endpoints.authorize_url,
        urllib.parse.urlencode(params)
    )


def parse_callback_url(url):
    """Parse a pasted redirect URL or a bare code into its components.

    Accepts the full ``http://127.0.0.1:port/cb?code=...&state=...`` URL when
    the browser could not reach the local listener, and also a bare code as
    displayed on the consent screen, optionally as ``code#state``.  Returns
    ``(code, state, error)``.
    """
    if not url:
        raise QAOrcaPkceError('no authorization code was provided')
    text = url.strip()
    if not text:
        raise QAOrcaPkceError('no authorization code was provided')
    if text.startswith('http://') or text.startswith('https://'):
        parsed = urllib.parse.urlparse(text)
        query = urllib.parse.parse_qs(parsed.query)
        code = (query.get('code') or [None])[0]
        state = (query.get('state') or [None])[0]
        error = (query.get('error') or [None])[0]
        return code, state, error
    if '#' in text:
        code, _, state = text.partition('#')
        return code or None, state or None, None
    return text, None, None


def _read_limited(response, limit=_MAX_RESPONSE_BYTES):
    return response.read(limit)


def exchange_code(
    endpoints,
    code,
    verifier,
    timeout=DEFAULT_EXCHANGE_TIMEOUT,
    transport=None,
):
    """POST the auth code plus verifier to the auth origin's exchange path.

    The request always goes to ``{auth_base}/api/v1/auth/keys``.  It never
    goes to the inference origin, and the endpoint is never derived by
    rewriting a hostname or appending ``/v1``.
    """
    payload = json.dumps(
        {
            'code': code,
            'code_verifier': verifier,
            'code_challenge_method': 'S256',
        }
    ).encode('utf-8')
    request = urllib.request.Request(
        endpoints.exchange_url,
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    opener = urllib.request.urlopen if transport is None else transport
    try:
        with opener(request, timeout=timeout) as response:
            raw = _read_limited(response)
            status = getattr(response, 'status', 200)
    except urllib.error.HTTPError as error:
        body = ''
        try:
            body = _read_limited(error).decode('utf-8', 'replace')
        except Exception:                                             # pragma: no cover - defensive
            body = ''
        raise QAOrcaPkceError(
            'code exchange was rejected with HTTP {0}{1}'.format(
                error.code,
                _safe_error_detail(body)
            )
        )
    except (urllib.error.URLError, socket.timeout, OSError) as error:
        raise QAOrcaPkceError(
            'could not reach the OrcaRouter authentication service: '
            '{0}'.format(type(error).__name__)
        )

    if status >= 400:
        raise QAOrcaPkceError(
            'code exchange was rejected with HTTP {0}'.format(status)
        )

    try:
        data = json.loads(raw.decode('utf-8'))
    except ValueError:
        raise QAOrcaPkceError('the exchange response was not valid JSON')

    key = data.get('key')
    if not looks_like_orcarouter_key(key):
        # Never echo the body: it could contain a partially-valid credential.
        raise QAOrcaPkceError(
            'the exchange response did not contain an OrcaRouter API key'
        )
    return data


def _safe_error_detail(body):
    """Extract an OAuth ``error``/``error_description`` without credentials.

    Error bodies are ``{"error": ..., "error_description": ...}`` rather than
    the API's usual envelope, deliberately, so standard OAuth clients parse
    them.  Only those two fields are surfaced; the rest is dropped.
    """
    if not body:
        return ''
    try:
        parsed = json.loads(body)
    except ValueError:
        return ''
    if not isinstance(parsed, dict):
        return ''
    error = parsed.get('error')
    description = parsed.get('error_description')
    if not error and not description:
        return ''
    return ' ({0})'.format(
        ': '.join(str(part) for part in (error, description) if part)
    )


class QAOrcaLoopbackListener(object):
    """Flow A helper: a loopback listener bound *before* the browser opens.

    The port is taken from the OS, so nothing races between opening the
    browser and knowing where the callback lands.
    """

    def __init__(self, host='127.0.0.1'):
        self.host = host
        self.httpd = None
        self.port = None
        self._result = {}
        self._event = threading.Event()
        self._thread = None

    def start(self):
        outer = self

        class Handler(http.server.BaseHTTPRequestHandler):

            def log_message(self, *args, **kwargs):
                # Silence the default stderr access log: the request line
                # carries the one-time code and the state.
                return

            def do_GET(self):                                                # noqa: N802 - stdlib naming
                parsed = urllib.parse.urlparse(self.path)
                if parsed.path != CALLBACK_PATH:
                    self.send_response(404)
                    self.end_headers()
                    return
                query = urllib.parse.parse_qs(parsed.query)
                outer._result['code'] = (query.get('code') or [None])[0]
                outer._result['state'] = (query.get('state') or [None])[0]
                outer._result['error'] = (query.get('error') or [None])[0]
                body = (
                    b'<html><body><p>Connected. You can close this tab.</p>'
                    b'</body></html>'
                )
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(body)
                outer._event.set()

        self.httpd = http.server.HTTPServer((self.host, 0), Handler)
        self.port = self.httpd.server_address[1]
        self._thread = threading.Thread(target=self.httpd.serve_forever)
        self._thread.daemon = True
        self._thread.start()
        return self.port

    def wait(self, state, timeout=DEFAULT_TIMEOUT):
        """Block until the callback arrives, then compare ``state``.

        ``state`` is compared with a constant-time comparison *before* the
        code is looked at, so a code somebody else's page dropped on this
        listener cannot be redeemed.
        """
        if not self._event.wait(timeout):
            raise QAOrcaAuthTimeout(
                'the browser never returned to the local callback listener'
            )
        returned = self._result.get('state')
        if not hmac.compare_digest(str(returned or ''), str(state or '')):
            raise QAOrcaPkceError('state mismatch; the callback was rejected')
        error = self._result.get('error')
        if error:
            raise QAOrcaAuthDenied(
                'authorization was denied ({0})'.format(error)
            )
        code = self._result.get('code')
        if not code:
            raise QAOrcaPkceError('the callback carried no authorization code')
        return code

    def stop(self):
        self._event.set()
        if self.httpd is not None:
            try:
                self.httpd.shutdown()
            except Exception: # pragma: no cover - defensive
                pass
            try:
                self.httpd.server_close()
            except Exception: # pragma: no cover - defensive
                pass
            self.httpd = None


class QAOrcaPkceAdapter(QAOrcaCredentialProvider):
    """Authentication choice 2: browser authorization yielding a normal key.

    Produces the *same* :class:`QAOrcaCredentialResult` as the API-key
    adapter, so nothing downstream can tell the two apart.
    """

    source = ORCA_SOURCE_OAUTH_PKCE

    def __init__(
        self,
        store=None,
        endpoints=None,
        opener=None,
        app_name=ORCA_APP_NAME,
        login_hint=None,
        scope=ORCA_REQUIRED_SCOPE,
    ):
        self.store = store or QAOrcaCredentialStore()
        self.endpoints = endpoints or resolve_endpoints()
        self.opener = opener
        self.app_name = app_name
        self.login_hint = login_hint
        self.scope = scope

    # -- flow B ---------------------------------------------------------
    def start_out_of_band(self):
        """Return ``(url, verifier, state)`` for a paste-the-code login."""
        verifier = generate_verifier()
        state = generate_state()
        url = build_authorize_url(
            self.endpoints,
            code_challenge_for(verifier),
            state,
            FLOW_OUT_OF_BAND,
            app_name=self.app_name,
            scope=self.scope,
            login_hint=self.login_hint,
        )
        return url, verifier, state

    def finish_out_of_band(self, url_or_code, verifier, expected_state=None):
        """Exchange a pasted code/redirect URL, then persist the key.

        Two shapes are accepted, and they are checked differently:

        * a full redirect URL, which carries ``state`` -- it must match the
          state this process generated, compared in constant time;
        * the bare code the consent screen displays, which carries no state
          by construction.  There is nothing to compare, which is exactly
          why Flow B mandates ``S256``: the code is redeemable only by the
          process holding the verifier.
        """
        code, returned_state, error = parse_callback_url(url_or_code)
        if error:
            raise QAOrcaAuthDenied(
                'authorization was denied ({0})'.format(error)
            )
        if not code:
            raise QAOrcaPkceError('no authorization code was provided')
        if returned_state is not None:
            if expected_state is None or not hmac.compare_digest(
                    str(returned_state),
                    str(expected_state)):
                raise QAOrcaPkceError(
                    'state mismatch; the pasted code was rejected'
                )
        return self._exchange_and_store(code, verifier)

    # -- flow A ---------------------------------------------------------
    def connect_loopback(
        self,
        browser_open=None,
        timeout=DEFAULT_TIMEOUT,
        listener=None
    ):
        """Run the loopback redirect flow to completion."""
        listener = listener or QAOrcaLoopbackListener()
        port = listener.start()
        verifier = generate_verifier()
        state = generate_state()
        url = build_authorize_url(
            self.endpoints,
            code_challenge_for(verifier),
            state,
            FLOW_LOOPBACK,
            app_name=self.app_name,
            callback_port=port,
            scope=self.scope,
            login_hint=self.login_hint,
        )
        try:
            if browser_open is not None:
                browser_open(url)
            code = listener.wait(state, timeout=timeout)
            return self._exchange_and_store(code, verifier)
        finally:
            listener.stop()

    # -- shared ---------------------------------------------------------
    def _exchange_and_store(self, code, verifier, exchange=None):
        exchange = exchange or exchange_code
        data = exchange(self.endpoints, code, verifier)
        scope = data.get('scope') or ORCA_REQUIRED_SCOPE
        granted_ok = _scope_satisfies(scope, self.scope)
        account_id = 'orcarouter-oauth-{0}'.format(
            data.get('user_id') or 'unknown'
        )
        stored = self.store.save(
            api_key=data['key'],
            source=ORCA_SOURCE_OAUTH_PKCE,
            account_id=account_id,
            scope=scope,
        )
        if not granted_ok:
            # The key is valid and stored, but it does not cover what this
            # integration needs; say so instead of assuming the request.
            raise QAOrcaScopeDowngrade(
                'the granted scope is {0!r}, which does not cover {1!r}'.format(
                    scope,
                    self.scope
                )
            )
        return QAOrcaCredentialResult(
            api_key=stored['api_key'],
            source=ORCA_SOURCE_OAUTH_PKCE,
            account_id=account_id,
            scope=scope,
        )

    def acquire(self):
        """Reuse the stored key; never re-authorize on every launch.

        There is a cap of 10 PKCE-issued keys per user per 24 hours, so a
        client that started a login on every launch would lock its own users
        out.  A stored, non-revoked key is therefore reused until OrcaRouter
        revokes it.
        """
        credential = self.store.load(allow_needs_reauth=True)
        if credential is not None and not credential.get('needs_reauth'):
            return QAOrcaCredentialResult(
                api_key=credential['api_key'],
                source=credential.get('source',
                                      ORCA_SOURCE_OAUTH_PKCE),
                account_id=credential['account_id'],
                scope=credential.get('scope',
                                     ORCA_REQUIRED_SCOPE),
            )
        raise QAOrcaCredentialError(
            'no stored OrcaRouter authorization; run `orcarouter login '
            '--oauth` to connect an account'
        )


def _scope_satisfies(granted, requested):
    """Check that ``granted`` covers ``requested``.

    The exchange response reports what was *granted*, not what was asked
    for, so the two are compared rather than assumed equal.
    """
    if granted == requested:
        return True
    granted_parts = set(str(granted or '').split())
    requested_parts = set(str(requested or '').split())
    return requested_parts.issubset(granted_parts)


class QAOrcaLoginSession(object):
    """Server-side "login already in progress" state for one client.

    Every terminal path releases the lock: success, denial, exchange error,
    timeout, explicit cancel, switching provider or method, closing the
    modal, and ``pagehide``.  A monotonically increasing generation makes
    every asynchronous response prove it still belongs to the current
    attempt, so a late success from provider A can never appear under
    provider B.
    """

    def __init__(self, adapter=None, timeout=DEFAULT_TIMEOUT):
        self.adapter = adapter or QAOrcaPkceAdapter()
        self.timeout = timeout
        self.generation = 0
        self.busy = False
        self.hint = None
        self.error = None
        self.result = None
        self._lock = threading.Lock()

    def begin(self):
        """Start a new attempt, invalidating anything still in flight."""
        with self._lock:
            self.generation += 1
            self.busy = True
            self.hint = None
            self.error = None
            self.result = None
            generation = self.generation
        url, verifier, state = self.adapter.start_out_of_band()
        with self._lock:
            if self.generation != generation:
                return None
            self.hint = url
        return {
            'generation': generation,
            'authorize_url': url,
            'verifier': verifier,
            'state': state,
        }

    def complete(self, generation, pasted, verifier, state):
        """Finish an attempt; a stale generation is refused, not applied."""
        with self._lock:
            if not self._is_current(generation):
                return False
        try:
            result = self.adapter.finish_out_of_band(pasted, verifier, state)
        except Exception as error:
            with self._lock:
                if self._is_current(generation):
                    self.busy = False
                    self.error = str(error)
            return False
        with self._lock:
            if not self._is_current(generation):
                # A newer attempt already took over; do not touch its state.
                return False
            self.busy = False
            self.result = result
            self.hint = None
            return True

    def cancel(self, generation=None):
        """Release the lock.  Used by the Cancel button and on unmount."""
        with self._lock:
            if generation is not None and not self._is_current(generation):
                return False
            self.generation += 1
            self.busy = False
            self.hint = None
            self.error = None
            return True

    def pagehide(self, generation=None):
        """Back-forward-cache safe cancellation.

        The busy flag and the authorization hint are cleared *synchronously*,
        because the browser may restore this page from the back-forward cache
        where a mounted component's guarded cleanup would refuse to mutate
        state and leave the page permanently busy.
        """
        return self.cancel(generation)

    def snapshot(self):
        with self._lock:
            return {
                'generation':
                    self.generation,
                'busy':
                    self.busy,
                'hint':
                    self.hint,
                'error':
                    self.error,
                'connected':
                    self.result is not None,
                'account_id':
                    (
                        self.result.account_id
                        if self.result is not None else None
                    ),
            }

    def _is_current(self, generation):
        """Caller holds ``self._lock``."""
        return generation is not None and generation == self.generation
