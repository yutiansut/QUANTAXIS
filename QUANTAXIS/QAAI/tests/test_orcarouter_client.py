# coding:utf-8
"""OrcaRouter inference transport: origins, 401 lifecycle, no fake refresh."""

import json

import pytest

from QUANTAXIS.QAAI.QAOrcaClient import (
    QAOrcaClient,
    QAOrcaInferenceError,
    QAOrcaNeedsReauth,
    QAOrcaRateLimited,
)
from QUANTAXIS.QAAI.QAOrcaCredential import (
    ORCA_SOURCE_API_KEY,
    ORCA_SOURCE_OAUTH_PKCE,
    QAOrcaApiKeyAdapter,
)
from QUANTAXIS.QAAI.QAOrcaEndpoints import QAOrcaEndpoints

FAKE_KEY = 'sk-orca-inferencefakekey0123456789'
FAKE_KEY_TWO = 'sk-orca-replacementfakekey0987654321'


class RecordingOpener(object):
    """Stands in for ``urlopen``; records the request, returns canned data."""

    def __init__(self, payload=None, status=200, error=None):
        self.payload = payload if payload is not None else {
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': 'hi'
                }
            }]
        }
        self.status = status
        self.error = error
        self.requests = []

    def __call__(self, request, timeout=None):
        self.requests.append(
            {
                'url':
                    request.full_url,
                'method':
                    request.get_method(),
                'headers':
                    dict(request.headers),
                'body':
                    json.loads(request.data.decode()) if request.data else None,
                'timeout':
                    timeout,
            }
        )
        if self.error is not None:
            raise self.error

        class Response(object):

            status = self.status

            def __init__(self, payload):
                self._payload = json.dumps(payload).encode()

            def read(self, limit=None):
                return self._payload

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        return Response(self.payload)


def _http_error(code):
    import urllib.error

    return urllib.error.HTTPError(
        'https://api.orcarouter.ai/v1/chat/completions',
        code,
        'err',
        {},
        None
    )


def api_key_client(store, opener, key=FAKE_KEY, **kwargs):
    credential = QAOrcaApiKeyAdapter(store=store, api_key=key)
    return QAOrcaClient(
        credential=credential,
        opener=opener,
        store=store,
        **kwargs
    )


# -- transport ------------------------------------------------------------


def test_chat_posts_to_the_inference_origin_with_bearer_auth(store):
    opener = RecordingOpener()
    client = api_key_client(store, opener)
    result = client.chat(
        [{
            'role': 'user',
            'content': 'hello'
        }],
        model='openai/gpt-5.5'
    )
    assert result['choices'][0]['message']['content'] == 'hi'
    sent = opener.requests[0]
    assert sent['url'] == 'https://api.orcarouter.ai/v1/chat/completions'
    assert sent['method'] == 'POST'
    assert sent['headers']['Authorization'] == 'Bearer {0}'.format(FAKE_KEY)
    assert sent['body']['model'] == 'openai/gpt-5.5'


def test_inference_never_touches_the_auth_origin(store):
    opener = RecordingOpener()
    api_key_client(store,
                   opener).chat(
                       [{
                           'role': 'user',
                           'content': 'hi'
                       }],
                       model='orcarouter/auto'
                   )
    urls = [item['url'] for item in opener.requests]
    assert all('api.orcarouter.ai' in url for url in urls)
    assert not any('www.orcarouter.ai' in url for url in urls)


def test_explicit_api_override_wins_over_the_shared_base(store):
    opener = RecordingOpener()
    endpoints = QAOrcaEndpoints(
        auth_base='https://auth.internal',
        api_base='https://relay.internal',
    )
    client = QAOrcaClient(
        credential=QAOrcaApiKeyAdapter(store=store,
                                       api_key=FAKE_KEY),
        endpoints=endpoints,
        opener=opener,
    )
    client.chat([{'role': 'user', 'content': 'hi'}], model='orcarouter/auto')
    assert opener.requests[0]['url'] == (
        'https://relay.internal/v1/chat/completions'
    )


def test_shared_self_hosted_base_fills_both_origins(monkeypatch):
    from QUANTAXIS.QAAI.QAOrcaEndpoints import resolve_endpoints

    endpoints = resolve_endpoints(env={'ORCA_BASE_URL': 'https://orca.corp'})
    assert endpoints.auth_base == 'https://orca.corp'
    assert endpoints.api_base == 'https://orca.corp'
    assert endpoints.exchange_url == 'https://orca.corp/api/v1/auth/keys'
    assert endpoints.models_url == 'https://orca.corp/v1/models'


def test_explicit_override_beats_the_shared_base():
    from QUANTAXIS.QAAI.QAOrcaEndpoints import resolve_endpoints

    endpoints = resolve_endpoints(
        env={
            'ORCA_BASE_URL': 'https://orca.corp',
            'ORCA_AUTH_BASE_URL': 'https://login.corp',
        }
    )
    assert endpoints.auth_base == 'https://login.corp'
    assert endpoints.api_base == 'https://orca.corp'


@pytest.mark.parametrize(
    'origin',
    [
        'http://orca.example.com',
        'ftp://orca.example.com',
        'https://user:pass@orca.example.com',
        'https://orca.example.com?x=1',
        'not-a-url',
        '',
    ],
)
def test_non_https_remote_origins_are_refused(origin):
    from QUANTAXIS.QAAI.QAOrcaEndpoints import (
        QAOrcaEndpointError,
        validate_origin,
    )

    with pytest.raises(QAOrcaEndpointError):
        validate_origin(origin)


def test_http_is_allowed_only_for_loopback():
    from QUANTAXIS.QAAI.QAOrcaEndpoints import validate_origin

    assert validate_origin('http://127.0.0.1:8080') == 'http://127.0.0.1:8080'
    assert validate_origin('http://localhost:8080') == 'http://localhost:8080'


def test_empty_messages_are_refused_before_any_request(store):
    opener = RecordingOpener()
    with pytest.raises(QAOrcaInferenceError):
        api_key_client(store, opener).chat([], model='orcarouter/auto')
    assert opener.requests == []


# -- credential lifecycle -------------------------------------------------


def test_401_marks_the_exact_account_needs_reauth_and_does_not_refresh(store):
    store.save(FAKE_KEY, ORCA_SOURCE_API_KEY, 'acct')
    opener = RecordingOpener(error=_http_error(401))
    client = api_key_client(store, opener, key=FAKE_KEY, account_id='acct')
    with pytest.raises(QAOrcaNeedsReauth) as info:
        client.chat(
            [{
                'role': 'user',
                'content': 'hi'
            }],
            model='orcarouter/auto'
        )

    # Terminal: reauthentication is required, and the message says so.
    assert 'reconnect' in str(info.value) or 'rejected' in str(info.value)
    assert store.status()['accounts'][0]['needs_reauth'] is True
    # Exactly one request: no refresh attempt, no retry loop.
    assert len(opener.requests) == 1
    # The key survives, so a transient misclassification is recoverable.
    assert store.load('acct', allow_needs_reauth=True)['api_key'] == FAKE_KEY


def test_401_does_not_attempt_a_refresh_grant(store):
    store.save(FAKE_KEY, ORCA_SOURCE_API_KEY, 'acct')
    opener = RecordingOpener(error=_http_error(401))
    client = api_key_client(store, opener, key=FAKE_KEY, account_id='acct')
    with pytest.raises(QAOrcaNeedsReauth):
        client.chat(
            [{
                'role': 'user',
                'content': 'hi'
            }],
            model='orcarouter/auto'
        )
    bodies = [item['body'] for item in opener.requests]
    assert all('refresh_token' not in json.dumps(body) for body in bodies)
    assert all('grant_type' not in json.dumps(body) for body in bodies)


def test_a_stale_401_never_marks_a_newer_credential_broken(store):
    """The generation guard: only the rejected generation may be flagged."""
    store.save(FAKE_KEY, ORCA_SOURCE_API_KEY, 'acct')
    stale_client = api_key_client(
        store,
        RecordingOpener(error=_http_error(401)),
        key=FAKE_KEY,
        account_id='acct',
    )
    stale = stale_client._current()
    stale_generation = stale_client.last_generation

    # The user reconnects, replacing the credential.
    store.save(FAKE_KEY_TWO, ORCA_SOURCE_OAUTH_PKCE, 'acct')

    # The old request now fails.
    stale_client._mark_needs_reauth(stale)

    record = store.load('acct')
    assert record is not None
    assert record['api_key'] == FAKE_KEY_TWO
    assert record.get('needs_reauth') is False
    assert stale_generation is not None


def test_429_is_transient_and_leaves_credentials_alone(store):
    store.save(FAKE_KEY, ORCA_SOURCE_API_KEY, 'acct')
    opener = RecordingOpener(error=_http_error(429))
    client = api_key_client(store, opener, key=FAKE_KEY, account_id='acct')
    with pytest.raises(QAOrcaRateLimited):
        client.chat(
            [{
                'role': 'user',
                'content': 'hi'
            }],
            model='orcarouter/auto'
        )
    assert store.status()['accounts'][0]['needs_reauth'] is False
    assert store.load('acct') is not None


def test_transport_failure_is_transient(store):
    import urllib.error

    store.save(FAKE_KEY, ORCA_SOURCE_API_KEY, 'acct')
    opener = RecordingOpener(error=urllib.error.URLError('down'))
    client = api_key_client(store, opener, key=FAKE_KEY, account_id='acct')
    with pytest.raises(QAOrcaInferenceError) as info:
        client.chat(
            [{
                'role': 'user',
                'content': 'hi'
            }],
            model='orcarouter/auto'
        )
    assert not isinstance(info.value, QAOrcaNeedsReauth)
    assert store.load('acct') is not None


def test_server_error_carries_no_key(store):
    store.save(FAKE_KEY, ORCA_SOURCE_API_KEY, 'acct')
    opener = RecordingOpener(error=_http_error(500))
    client = api_key_client(store, opener, key=FAKE_KEY, account_id='acct')
    with pytest.raises(QAOrcaInferenceError) as info:
        client.chat(
            [{
                'role': 'user',
                'content': 'hi'
            }],
            model='orcarouter/auto'
        )
    assert FAKE_KEY not in str(info.value)


# -- seam agnosticism -----------------------------------------------------


def test_inference_cannot_tell_which_adapter_produced_the_key(store):
    """The client consumes the seam, so both sources behave identically."""
    from QUANTAXIS.QAAI.QAOrcaAuth import QAOrcaPkceAdapter

    store.save(FAKE_KEY, ORCA_SOURCE_API_KEY, 'orcarouter-api-key')
    store.save(FAKE_KEY_TWO, ORCA_SOURCE_OAUTH_PKCE, 'orcarouter-oauth-1')

    key_opener = RecordingOpener()
    pkce_opener = RecordingOpener()
    QAOrcaClient(
        credential=QAOrcaApiKeyAdapter(store=store),
        opener=key_opener,
        store=store,
    ).chat([{
        'role': 'user',
        'content': 'hi'
    }],
           model='orcarouter/auto')
    QAOrcaClient(
        credential=QAOrcaPkceAdapter(store=store),
        opener=pkce_opener,
        store=store,
    ).chat([{
        'role': 'user',
        'content': 'hi'
    }],
           model='orcarouter/auto')

    key_request = key_opener.requests[0]
    pkce_request = pkce_opener.requests[0]
    # Identical URL, identical method, identical header shape.
    assert key_request['url'] == pkce_request['url']
    assert key_request['method'] == pkce_request['method']
    assert key_request['body'] == pkce_request['body']
    # Only the bearer value differs, because the accounts differ.
    assert key_request['headers']['Authorization'].startswith('Bearer sk-orca-')
    assert pkce_request['headers']['Authorization'].startswith(
        'Bearer sk-orca-'
    )


def test_a_revoked_stored_key_is_not_silently_deleted(store):
    store.save(FAKE_KEY, ORCA_SOURCE_API_KEY, 'acct')
    store.mark_needs_reauth('acct')
    # Normal resolution refuses it...
    assert store.load('acct') is None
    # ...but the secret is still there for the user to replace.
    assert store.load('acct', allow_needs_reauth=True)['api_key'] == FAKE_KEY
    assert store.clear('acct') is True
