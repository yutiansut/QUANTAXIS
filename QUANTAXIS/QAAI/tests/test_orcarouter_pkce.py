# coding:utf-8
"""OrcaRouter OAuth 2.0 + PKCE connect flows, end to end.

The authorization server here is a real local HTTP server: the tests drive
the same adapter the GUI and CLI use, through a full
authorize -> callback/code -> exchange -> persist round trip.  No test
fabricates a credential by calling a helper directly.
"""

import json
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from QUANTAXIS.QAAI.QAOrcaAuth import (
    FLOW_LOOPBACK,
    QAOrcaAuthDenied,
    QAOrcaAuthTimeout,
    QAOrcaLoopbackListener,
    QAOrcaLoginSession,
    QAOrcaPkceAdapter,
    QAOrcaPkceError,
    QAOrcaScopeDowngrade,
    build_authorize_url,
    code_challenge_for,
    exchange_code,
    generate_state,
    generate_verifier,
    parse_callback_url,
)
from QUANTAXIS.QAAI.QAOrcaCredential import (
    ORCA_SOURCE_OAUTH_PKCE,
    QAOrcaCredentialStore,
)
from QUANTAXIS.QAAI.QAOrcaEndpoints import QAOrcaEndpoints, resolve_endpoints

VERIFIER_KEY = 'sk-orca-oauthissuedkey0123456789abcdef'
PLAINTEXT_VERIFIER = 'fixed-verifier-must-never-be-used'


class FakeAuthServer(object):
    """A local stand-in for the OrcaRouter consent + exchange endpoints."""

    def __init__(self, response=None, status=200, delay=0.0):
        self.exchanges = []
        self.requests = []
        self.response = response if response is not None else {
            'key': VERIFIER_KEY,
            'user_id': '12345',
            'scope': 'api'
        }
        self.status = status
        self.delay = delay
        self.httpd = None
        self.thread = None
        self.port = None

    def start(self):
        outer = self

        class Handler(BaseHTTPRequestHandler):

            def log_message(self, *args, **kwargs):
                return

            def _record(self):
                length = int(self.headers.get('Content-Length') or 0)
                body = self.rfile.read(length).decode('utf-8') if length else ''
                outer.requests.append(
                    {
                        'path': self.path,
                        'method': self.command,
                        'body': body,
                        'headers': dict(self.headers),
                    }
                )
                return body

            def do_GET(self):                                                   # noqa: N802
                self._record()
                payload = json.dumps(
                    {
                        'authorization_endpoint':
                            'http://127.0.0.1:{0}/auth'.format(outer.port),
                        'token_endpoint':
                            (
                                'http://127.0.0.1:{0}/api/v1/auth/keys'.format(
                                    outer.port
                                )
                            ),
                    }
                ).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def do_POST(self): # noqa: N802
                body = self._record()
                if outer.delay:
                    time.sleep(outer.delay)
                try:
                    outer.exchanges.append(json.loads(body))
                except ValueError:
                    outer.exchanges.append({'raw': body})
                payload = json.dumps(outer.response).encode('utf-8')
                self.send_response(outer.status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

        self.httpd = HTTPServer(('127.0.0.1', 0), Handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        return self.port

    def stop(self):
        if self.httpd is not None:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None

    @property
    def endpoints(self):
        base = 'http://127.0.0.1:{0}'.format(self.port)
        return QAOrcaEndpoints(auth_base=base, api_base=base)


@pytest.fixture
def auth_server():
    server = FakeAuthServer()
    server.start()
    yield server
    server.stop()


# -- PKCE primitives ------------------------------------------------------


def test_verifier_and_state_are_fresh_every_time():
    verifiers = {generate_verifier() for _ in range(50)}
    states = {generate_state() for _ in range(50)}
    assert len(verifiers) == 50
    assert len(states) == 50
    assert all(len(item) >= 40 for item in verifiers)


def test_challenge_is_unpadded_base64url_sha256_of_the_verifier():
    import base64
    import hashlib

    verifier = generate_verifier()
    challenge = code_challenge_for(verifier)
    expected = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).decode().rstrip('=')
    assert challenge == expected
    assert '=' not in challenge
    assert '+' not in challenge and '/' not in challenge
    # The challenge is a one-way function of the verifier: it must not be
    # possible to read the verifier back out of it.
    assert verifier not in challenge
    assert challenge != verifier


def test_a_fixed_verifier_is_never_used(auth_server):
    """Two attempts must never share a verifier or a challenge."""
    adapter = QAOrcaPkceAdapter(
        store=QAOrcaCredentialStore(path='/tmp/never-written.json'),
        endpoints=auth_server.endpoints,
    )
    first = adapter.start_out_of_band()
    second = adapter.start_out_of_band()
    assert first[1] != second[1] # verifier
    assert first[2] != second[2] # state
    assert PLAINTEXT_VERIFIER not in first[0]
    assert PLAINTEXT_VERIFIER not in second[0]


# -- authorize URL --------------------------------------------------------


def test_authorize_url_only_uses_the_auth_origin(auth_server):
    adapter = QAOrcaPkceAdapter(endpoints=auth_server.endpoints)
    url, verifier, state = adapter.start_out_of_band()
    parsed = urllib.parse.urlparse(url)
    assert parsed.scheme == 'http'
    assert parsed.port == auth_server.port
    assert parsed.path == '/auth'

    query = urllib.parse.parse_qs(parsed.query)
    assert query['callback_url'] == ['oob']
    assert query['code_challenge_method'] == ['S256']
    assert query['code_challenge'] == [code_challenge_for(verifier)]
    assert query['state'] == [state]
    assert query['scope'] == ['api']
    assert query['app_name'] == ['QUANTAXIS']
    # The verifier must never ride on the authorize URL.
    assert verifier not in url


def test_loopback_authorize_url_names_the_listener_port(auth_server):
    url = build_authorize_url(
        auth_server.endpoints,
        code_challenge_for(generate_verifier()),
        generate_state(),
        FLOW_LOOPBACK,
        callback_port=51733,
    )
    query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    assert query['callback_url'] == ['http://127.0.0.1:51733/cb']
    assert query['code_challenge_method'] == ['S256']


def test_public_defaults_are_two_distinct_origins():
    endpoints = resolve_endpoints(env={})
    assert endpoints.auth_base == 'https://www.orcarouter.ai'
    assert endpoints.api_base == 'https://api.orcarouter.ai'
    assert endpoints.authorize_url == 'https://www.orcarouter.ai/auth'
    assert endpoints.exchange_url == (
        'https://www.orcarouter.ai/api/v1/auth/keys'
    )
    assert endpoints.models_url == 'https://api.orcarouter.ai/v1/models'
    # The mistake this guards against: the exchange must never live on the
    # inference origin, and must never be derived by appending '/v1' to it.
    assert endpoints.exchange_url == (endpoints.auth_base + '/api/v1/auth/keys')
    assert not endpoints.exchange_url.startswith(endpoints.api_base)


# -- exchange -------------------------------------------------------------


def test_exchange_posts_to_the_auth_origin_exchange_path(auth_server):
    verifier = generate_verifier()
    data = exchange_code(auth_server.endpoints, 'the-code', verifier)
    assert data['key'] == VERIFIER_KEY

    assert len(auth_server.exchanges) == 1
    sent = auth_server.exchanges[0]
    assert sent['code'] == 'the-code'
    assert sent['code_verifier'] == verifier
    assert sent['code_challenge_method'] == 'S256'
    request = auth_server.requests[0]
    assert request['path'] == '/api/v1/auth/keys'
    assert request['method'] == 'POST'


def test_exchange_never_targets_the_inference_path(auth_server):
    exchange_code(auth_server.endpoints, 'the-code', generate_verifier())
    paths = [item['path'] for item in auth_server.requests]
    assert paths == ['/api/v1/auth/keys']
    # The 404-shaped mistake is the *relay* path, which has no /api prefix
    # and lives on the inference origin.  Neither is ever requested here.
    assert not any(
        path == '/v1/auth/keys' or path.startswith('/v1/auth') for path in paths
    )


def test_exchange_rejection_is_reported_without_the_verifier(auth_server):
    auth_server.response = {'error': 'invalid_grant'}
    auth_server.status = 403
    verifier = generate_verifier()
    with pytest.raises(QAOrcaPkceError) as info:
        exchange_code(auth_server.endpoints, 'reused-code', verifier)
    message = str(info.value)
    assert '403' in message
    assert verifier not in message
    assert 'reused-code' not in message


def test_reused_or_expired_code_is_terminal(auth_server):
    """A second redemption of the same code is refused, not retried."""
    auth_server.status = 403
    auth_server.response = {'error': 'invalid_grant'}
    with pytest.raises(QAOrcaPkceError):
        exchange_code(
            auth_server.endpoints,
            'already-used',
            generate_verifier()
        )


def test_rate_limit_is_a_clean_failure(auth_server):
    auth_server.status = 429
    auth_server.response = {'error': 'slow_down'}
    with pytest.raises(QAOrcaPkceError) as info:
        exchange_code(auth_server.endpoints, 'code', generate_verifier())
    assert '429' in str(info.value)


def test_a_malformed_exchange_body_is_rejected(auth_server):
    auth_server.response = {'not_a_key': 'nope'}
    with pytest.raises(QAOrcaPkceError) as info:
        exchange_code(auth_server.endpoints, 'code', generate_verifier())
    assert 'did not contain an OrcaRouter API key' in str(info.value)


def test_network_failure_is_a_clean_error():
    endpoints = QAOrcaEndpoints(
        auth_base='http://127.0.0.1:1',
        api_base='http://127.0.0.1:1'
    )
    with pytest.raises(QAOrcaPkceError):
        exchange_code(endpoints, 'code', generate_verifier(), timeout=2)


# -- full connect flow (Flow B) -------------------------------------------


def test_out_of_band_connect_persists_a_usable_credential(
    auth_server,
    tmp_path
):
    store = QAOrcaCredentialStore(path=str(tmp_path / 'cred.json'))
    adapter = QAOrcaPkceAdapter(store=store, endpoints=auth_server.endpoints)
    url, verifier, state = adapter.start_out_of_band()

    result = adapter.finish_out_of_band('the-shown-code', verifier, state)

    assert result.api_key == VERIFIER_KEY
    assert result.source == ORCA_SOURCE_OAUTH_PKCE
    assert result.scope == 'api'
    assert verifier not in url
    # It is a durable key: stored, and reused instead of re-authorizing.
    assert store.load()['api_key'] == VERIFIER_KEY
    assert adapter.acquire().api_key == VERIFIER_KEY


def test_second_connect_reuses_the_stored_key(auth_server, tmp_path):
    store = QAOrcaCredentialStore(path=str(tmp_path / 'cred.json'))
    adapter = QAOrcaPkceAdapter(store=store, endpoints=auth_server.endpoints)
    url, verifier, state = adapter.start_out_of_band()
    adapter.finish_out_of_band('code', verifier, state)
    exchanges_before = len(auth_server.exchanges)

    # acquire() must not start another authorization: there is a cap of 10
    # PKCE-issued keys per user per 24 hours.
    assert adapter.acquire().api_key == VERIFIER_KEY
    assert len(auth_server.exchanges) == exchanges_before


def test_denied_authorization_is_reported_and_stores_nothing(
    auth_server,
    tmp_path
):
    store = QAOrcaCredentialStore(path=str(tmp_path / 'cred.json'))
    adapter = QAOrcaPkceAdapter(store=store, endpoints=auth_server.endpoints)
    url, verifier, state = adapter.start_out_of_band()
    with pytest.raises(QAOrcaAuthDenied):
        adapter.finish_out_of_band(
            'http://127.0.0.1:1/cb?error=access_denied&state=' + state,
            verifier,
            state,
        )
    assert store.load() is None
    assert auth_server.exchanges == []


def test_state_mismatch_on_a_pasted_redirect_is_refused(auth_server, tmp_path):
    store = QAOrcaCredentialStore(path=str(tmp_path / 'cred.json'))
    adapter = QAOrcaPkceAdapter(store=store, endpoints=auth_server.endpoints)
    url, verifier, state = adapter.start_out_of_band()
    attacker_state = generate_state()
    with pytest.raises(QAOrcaPkceError) as info:
        adapter.finish_out_of_band(
            'http://127.0.0.1:1/cb?code=stolen&state=' + attacker_state,
            verifier,
            state,
        )
    assert 'state mismatch' in str(info.value)
    # The code was never redeemed and nothing was stored.
    assert auth_server.exchanges == []
    assert store.load() is None


def test_the_shown_code_is_accepted_and_a_stray_redirect_is_not(
    auth_server,
    tmp_path
):
    """Flow B accepts the displayed code, which carries no state.

    That is exactly why Flow B mandates S256: the code is redeemable only by
    the process holding the verifier.  A *redirect-shaped* value, by
    contrast, claims a state and must match it.
    """
    adapter = QAOrcaPkceAdapter(
        store=QAOrcaCredentialStore(path=str(tmp_path / 'cred.json')),
        endpoints=auth_server.endpoints,
    )
    url, verifier, state = adapter.start_out_of_band()
    # A redirect URL carrying somebody else's state is refused.
    with pytest.raises(QAOrcaPkceError):
        adapter.finish_out_of_band(
            'http://127.0.0.1:1/cb?code=injected&state=not-our-state',
            verifier,
            state,
        )
    assert auth_server.exchanges == []

    # The bare code shown on the consent screen is the supported shape.
    result = adapter.finish_out_of_band('the-displayed-code', verifier, state)
    assert result.api_key == VERIFIER_KEY
    assert auth_server.exchanges[0]['code'] == 'the-displayed-code'


def test_scope_downgrade_is_reported_but_the_key_is_kept(auth_server, tmp_path):
    auth_server.response = {
        'key': VERIFIER_KEY,
        'user_id': '7',
        'scope': 'connector'
    }
    store = QAOrcaCredentialStore(path=str(tmp_path / 'cred.json'))
    adapter = QAOrcaPkceAdapter(store=store, endpoints=auth_server.endpoints)
    url, verifier, state = adapter.start_out_of_band()
    with pytest.raises(QAOrcaScopeDowngrade) as info:
        adapter.finish_out_of_band('code', verifier, state)
    assert 'connector' in str(info.value)
    # The granted scope is recorded as granted, not as requested.
    assert store.load()['scope'] == 'connector'


@pytest.mark.parametrize(
    'pasted,expected',
    [
        ('http://127.0.0.1/cb?code=abc&state=xyz',
         ('abc',
          'xyz',
          None)),
        ('abc#xyz',
         ('abc',
          'xyz',
          None)),
        ('abc',
         ('abc',
          None,
          None)),
    ],
)
def test_pasted_values_are_parsed(pasted, expected):
    assert parse_callback_url(pasted) == expected


def test_empty_pasted_value_is_rejected():
    with pytest.raises(QAOrcaPkceError):
        parse_callback_url('   ')


# -- full connect flow (Flow A) -------------------------------------------


def test_loopback_connect_completes_and_persists(auth_server, tmp_path):
    store = QAOrcaCredentialStore(path=str(tmp_path / 'cred.json'))
    adapter = QAOrcaPkceAdapter(store=store, endpoints=auth_server.endpoints)
    captured = {}

    def browser_open(url):
        captured['url'] = url
        # Simulate the browser following the redirect back to the listener.
        query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        callback = query['callback_url'][0]
        state = query['state'][0]
        threading.Thread(
            target=_hit_callback,
            args=(callback,
                  state,
                  'flow-a-code'),
            daemon=True,
        ).start()

    result = adapter.connect_loopback(browser_open=browser_open, timeout=20)
    assert result.api_key == VERIFIER_KEY
    assert 'code_challenge_method=S256' in captured['url']
    assert result.api_key not in captured['url']


def test_loopback_rejects_a_callback_with_the_wrong_state(
    auth_server,
    tmp_path
):
    store = QAOrcaCredentialStore(path=str(tmp_path / 'cred.json'))
    adapter = QAOrcaPkceAdapter(store=store, endpoints=auth_server.endpoints)
    captured = {}

    def browser_open(url):
        captured['url'] = url
        query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        callback = query['callback_url'][0]
        threading.Thread(
            target=_hit_callback,
            args=(callback,
                  generate_state(),
                  'attacker-code'),
            daemon=True,
        ).start()

    with pytest.raises(QAOrcaPkceError) as info:
        adapter.connect_loopback(browser_open=browser_open, timeout=20)
    assert 'state mismatch' in str(info.value)
    assert auth_server.exchanges == []
    assert store.load() is None


def test_loopback_releases_the_listener_even_on_failure(auth_server, tmp_path):
    adapter = QAOrcaPkceAdapter(
        store=QAOrcaCredentialStore(path=str(tmp_path / 'cred.json')),
        endpoints=auth_server.endpoints,
    )
    listener = QAOrcaLoopbackListener()
    with pytest.raises(QAOrcaAuthTimeout):
        adapter.connect_loopback(
            browser_open=lambda url: None,
            timeout=0.3,
            listener=listener
        )
    assert listener.httpd is None


def test_loopback_listener_rejects_other_paths():
    listener = QAOrcaLoopbackListener()
    port = listener.start()
    try:
        import urllib.request

        try:
            urllib.request.urlopen(
                'http://127.0.0.1:{0}/nope'.format(port),
                timeout=5
            )
            raise AssertionError('expected a 404')
        except Exception as error:
            assert '404' in str(error)
    finally:
        listener.stop()


def _hit_callback(callback_url, state, code):
    import urllib.request

    time.sleep(0.05)
    try:
        urllib.request.urlopen(
            '{0}?code={1}&state={2}'.format(callback_url,
                                            code,
                                            state),
            timeout=10,
        ).read()
    except Exception: # pragma: no cover - best effort in a thread
        pass


# -- login session lifecycle ----------------------------------------------


def test_session_pagehide_clears_busy_without_remounting(auth_server, tmp_path):
    store = QAOrcaCredentialStore(path=str(tmp_path / 'cred.json'))
    adapter = QAOrcaPkceAdapter(store=store, endpoints=auth_server.endpoints)
    session = QAOrcaLoginSession(adapter=adapter)
    session.begin()
    assert session.snapshot()['busy'] is True
    assert session.snapshot()['hint']

    # Back-forward cache: the page is frozen and restored, never remounted.
    session.pagehide()
    snapshot = session.snapshot()
    assert snapshot['busy'] is False
    assert snapshot['hint'] is None

    # A second login must be able to start on the same instance.
    second = session.begin()
    assert second is not None
    assert session.snapshot()['busy'] is True


def test_session_cancel_releases_the_lock(auth_server, tmp_path):
    adapter = QAOrcaPkceAdapter(
        store=QAOrcaCredentialStore(path=str(tmp_path / 'cred.json')),
        endpoints=auth_server.endpoints,
    )
    session = QAOrcaLoginSession(adapter=adapter)
    session.begin()
    assert session.cancel() is True
    snapshot = session.snapshot()
    assert snapshot['busy'] is False
    assert snapshot['hint'] is None
    assert session.begin() is not None


def test_a_stale_response_cannot_overwrite_a_newer_login(auth_server, tmp_path):
    adapter = QAOrcaPkceAdapter(
        store=QAOrcaCredentialStore(path=str(tmp_path / 'cred.json')),
        endpoints=auth_server.endpoints,
    )
    session = QAOrcaLoginSession(adapter=adapter)
    first = session.begin()
    # The user cancels and starts over; the first attempt is now stale.
    session.cancel(first['generation'])
    second = session.begin()

    assert session.complete(
        first['generation'],
        'code',
        first['verifier'],
        first['state']
    ) is False
    assert session.snapshot()['connected'] is False
    # The newer attempt is untouched and still current.
    assert session.snapshot()['generation'] == second['generation']
    assert session.snapshot()['busy'] is True


def test_completing_a_failed_exchange_releases_busy(auth_server, tmp_path):
    auth_server.status = 403
    auth_server.response = {'error': 'invalid_grant'}
    adapter = QAOrcaPkceAdapter(
        store=QAOrcaCredentialStore(path=str(tmp_path / 'cred.json')),
        endpoints=auth_server.endpoints,
    )
    session = QAOrcaLoginSession(adapter=adapter)
    attempt = session.begin()
    assert session.complete(
        attempt['generation'],
        'code',
        attempt['verifier'],
        attempt['state']
    ) is False
    snapshot = session.snapshot()
    assert snapshot['busy'] is False
    assert snapshot['error']


def test_successful_completion_releases_busy(auth_server, tmp_path):
    adapter = QAOrcaPkceAdapter(
        store=QAOrcaCredentialStore(path=str(tmp_path / 'cred.json')),
        endpoints=auth_server.endpoints,
    )
    session = QAOrcaLoginSession(adapter=adapter)
    attempt = session.begin()
    assert session.complete(
        attempt['generation'],
        'code',
        attempt['verifier'],
        attempt['state']
    ) is True
    snapshot = session.snapshot()
    assert snapshot['busy'] is False
    assert snapshot['hint'] is None


# -- secret hygiene -------------------------------------------------------


def test_verifier_and_key_never_appear_in_errors_or_snapshots(
    auth_server,
    tmp_path,
    capsys
):
    store = QAOrcaCredentialStore(path=str(tmp_path / 'cred.json'))
    adapter = QAOrcaPkceAdapter(store=store, endpoints=auth_server.endpoints)
    attempt = adapter.start_out_of_band()
    verifier = attempt[1]
    adapter.finish_out_of_band('code', verifier, attempt[2])

    status = store.status()
    rendered = json.dumps(status) + repr(status)
    assert verifier not in rendered
    assert VERIFIER_KEY not in rendered
    # Nothing was printed to stdout/stderr along the way.
    captured = capsys.readouterr()
    assert verifier not in captured.out + captured.err
    assert VERIFIER_KEY not in captured.out + captured.err
