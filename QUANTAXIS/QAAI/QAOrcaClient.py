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
"""OrcaRouter inference client (OpenAI-compatible transport).

This is the single place an OrcaRouter request is assembled and sent.  It is
credential-source agnostic: it is handed a
:class:`~QUANTAXIS.QAAI.QAOrcaCredential.QAOrcaCredentialResult` and never
asks where the key came from, so a pasted key and a PKCE-connected account
behave identically.

A ``401`` from the relay is terminal for the exact account generation that
made the rejected request: the generation is flagged ``needs_reauth`` and no
proactive or invented refresh is attempted.  ``429`` and transport failures
are transient and leave stored credentials untouched.
"""

import json
import urllib.error
import urllib.request

from QUANTAXIS.QAAI.QAOrcaCredential import (
    CREDENTIAL_NEEDS_REAUTH,
    classify_auth_failure,
)
from QUANTAXIS.QAAI.QAOrcaEndpoints import resolve_endpoints

__all__ = [
    'INFERENCE_TIMEOUT',
    'INFERENCE_MAX_BYTES',
    'QAOrcaInferenceError',
    'QAOrcaNeedsReauth',
    'QAOrcaRateLimited',
    'QAOrcaClient',
]

INFERENCE_TIMEOUT = 120.0
INFERENCE_MAX_BYTES = 16 * 1024 * 1024


class QAOrcaInferenceError(Exception):
    """A non-terminal inference failure.  Never carries the API key."""


class QAOrcaNeedsReauth(QAOrcaInferenceError):
    """The durable key was revoked; the user must re-run the connect flow."""


class QAOrcaRateLimited(QAOrcaInferenceError):
    """Transient rate limiting.  Stored credentials are left alone."""


class QAOrcaClient(object):
    """Bearer-authenticated client for ``{api_base}/v1``."""

    def __init__(
        self,
        credential,
        endpoints=None,
        opener=None,
        timeout=INFERENCE_TIMEOUT,
        store=None,
        account_id=None,
    ):
        self.credential = credential
        self.endpoints = endpoints or resolve_endpoints()
        self.opener = opener
        self.timeout = timeout
        self.store = store
        self.account_id = account_id
        self.last_generation = None

    def _current(self):
        """Resolve the credential and remember the exact generation used.

        Recording the generation here is what makes the ``401`` transition
        generation-safe: a late failure can only ever flag the credential
        that actually issued the rejected request.
        """
        result = self.credential.acquire()
        self.last_generation = self._generation_for(result)
        return result

    def _generation_for(self, result):
        if self.store is None:
            return None
        record = self.store.load(
            account_id=self.account_id or result.account_id,
            allow_needs_reauth=True,
        )
        if record is None:
            return None
        return record.get('generation')

    def models(self, capability=None):
        """Fetch model metadata through the catalog client."""
        from QUANTAXIS.QAAI.QAModelCatalog import discover_models

        result = self._current()
        return discover_models(
            self.endpoints,
            api_key=result.api_key,
            capability=capability
        )

    def chat(
        self,
        messages,
        model=None,
        stream=False,
        temperature=None,
        max_tokens=None,
        extra=None,
    ):
        """Send one chat completion in the OpenAI wire format."""
        if not messages:
            raise QAOrcaInferenceError('messages must not be empty')
        payload = {
            'model': model or self._default_model(),
            'messages': messages,
        }
        if stream:
            payload['stream'] = True
        if temperature is not None:
            payload['temperature'] = temperature
        if max_tokens is not None:
            payload['max_tokens'] = max_tokens
        if extra:
            payload.update(extra)
        return self._post(self.endpoints.chat_url, payload)

    def _default_model(self):
        return 'orcarouter/auto'

    def _post(self, url, payload):
        result = self._current()
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {0}'.format(result.api_key),
                'Accept': 'application/json',
            },
            method='POST',
        )
        opener = self.opener or urllib.request.urlopen
        try:
            with opener(request, timeout=self.timeout) as response:
                raw = response.read(INFERENCE_MAX_BYTES)
        except urllib.error.HTTPError as error:
            return self._handle_http_error(error, result)
        except (urllib.error.URLError, OSError) as error:
            # Transport failures are transient: the key is not at fault.
            raise QAOrcaInferenceError(
                'the OrcaRouter relay could not be reached: {0}'.format(
                    type(error).__name__
                )
            )
        return self._decode(raw)

    def _handle_http_error(self, error, result):
        decision = classify_auth_failure(error.code)
        if decision == CREDENTIAL_NEEDS_REAUTH:
            self._mark_needs_reauth(result)
            raise QAOrcaNeedsReauth(
                'the OrcaRouter credential for account {0!r} was rejected; '
                'run `orcarouter login` to reconnect it'.format(
                    result.account_id
                )
            )
        if error.code == 429:
            raise QAOrcaRateLimited(
                'OrcaRouter is rate limiting this account; retry shortly'
            )
        raise QAOrcaInferenceError(
            'the OrcaRouter relay answered HTTP {0}'.format(error.code)
        )

    def _mark_needs_reauth(self, result):
        """Flag the exact account generation, and nothing else."""
        if self.store is None:
            return
        self.store.mark_needs_reauth(
            self.account_id or result.account_id,
            self.last_generation
        )

    def _decode(self, raw):
        try:
            return json.loads(raw.decode('utf-8'))
        except ValueError:
            raise QAOrcaInferenceError(
                'the OrcaRouter relay returned a non-JSON response'
            )
