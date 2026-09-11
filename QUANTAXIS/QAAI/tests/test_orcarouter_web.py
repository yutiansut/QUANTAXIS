# coding:utf-8
"""The tornado-facing OrcaRouter surface: handler wiring and browser safety.

These tests run the real tornado application with the real handler list, so
the routes the GUI and the Playwright evidence use are the routes this
repository actually serves.  They assert that no API key is ever placed in a
response the browser receives.
"""

import json

import pytest

tornado = pytest.importorskip('tornado')

from tornado.testing import AsyncHTTPTestCase # noqa: E402

from QUANTAXIS.QAAI.QAProvider import describe_providers # noqa: E402
from QUANTAXIS.QAWebServer.orcarouterhandler import (    # noqa: E402
    ORCAROUTER_HANDLERS,
    QAOrcaPanelHandler,
    panel_path,
)

FAKE_KEY = 'sk-orca-panelfakekey0123456789abcdef'


class PanelTestCase(AsyncHTTPTestCase):

    def get_app(self):
        from tornado.web import Application

        return Application(ORCAROUTER_HANDLERS, debug=False)

    def json(self, path, method='GET', body=None):
        response = self.fetch(
            path,
            method=method,
            body=json.dumps(body) if body is not None else None,
            headers={'Content-Type': 'application/json'} if body else None,
        )
        return response, json.loads(response.body.decode('utf-8'))


class TestPanel(PanelTestCase):

    def test_panel_is_served_with_the_bootstrap(self):
        response = self.fetch('/orcarouter')
        assert response.code == 200
        html = response.body.decode('utf-8')
        assert 'window.QA_ORCAROUTER' in html
        assert '/*__ORCA_BOOTSTRAP__*/' not in html

    def test_panel_shows_both_authentication_choices(self):
        html = self.fetch('/orcarouter').body.decode('utf-8')
        # API Key entry
        assert 'orca-api-key-input' in html
        assert 'type="password"' in html
        assert 'orca-api-key-form' in html
        # Connect with OrcaRouter (PKCE)
        assert 'orca-oauth-start' in html
        assert 'orca-oauth-finish' in html
        # The legend that labels the two as a choice.
        assert 'orca-auth-legend' in html

    def test_panel_renders_a_heading_for_each_authentication_choice(self):
        """A registry key mismatch must not leave a choice unlabelled."""
        html = self.fetch('/orcarouter').body.decode('utf-8')
        assert 'orca-api-key-label' in html
        assert 'orca-oauth-label' in html
        # The registry entries the panel reads expose `name`, which is what
        # the heading falls back to.
        for entry in describe_providers():
            assert entry['name']
            assert entry['id']

    def test_panel_uses_the_official_orcarouter_mark(self):
        html = self.fetch('/orcarouter').body.decode('utf-8')
        assert 'https://www.orcarouter.ai/orca-logo-classic.png' in html

    def test_panel_model_control_is_a_listbox_not_a_free_text_field(self):
        html = self.fetch('/orcarouter').body.decode('utf-8')
        assert 'role="listbox"' in html
        assert 'aria-expanded="false"' in html
        assert 'orca-model-trigger' in html

    def test_panel_localization_resolves_through_the_catalog(self):
        english = self.fetch('/orcarouter?locale=en').body.decode('utf-8')
        chinese = self.fetch('/orcarouter?locale=zh').body.decode('utf-8')
        assert 'OrcaRouter - API' in english
        assert 'OrcaRouter - 密钥' in chinese
        assert 'OrcaRouter - Auth' in english
        assert 'OrcaRouter - 授权登录' in chinese
        # Same keys, different values: no hardcoded label escaped the catalog.
        assert english.count('"panel.') == chinese.count('"panel.')

    def test_panel_serves_the_real_template_file(self):
        import os

        assert os.path.isfile(panel_path())
        assert QAOrcaPanelHandler is not None


class TestStatus(PanelTestCase):

    def test_status_reports_both_providers_and_no_secret(self):
        response, body = self.json('/orcarouter/status')
        assert response.code == 200
        result = body['result']
        ids = [item['id'] for item in result['providers']]
        assert ids == ['orcarouter', 'orcarouter-oauth']
        kinds = sorted(item['kind'] for item in result['auth_methods'])
        assert kinds == ['api_key', 'oauth_pkce']
        assert result['endpoints']['auth_base'] == 'https://www.orcarouter.ai'
        assert result['endpoints']['api_base'] == 'https://api.orcarouter.ai'
        assert result['key_dashboard_url'] == (
            'https://www.orcarouter.ai/console/authorized-apps'
        )
        assert FAKE_KEY not in json.dumps(body)


class TestApiKey(PanelTestCase):

    def test_storing_a_key_returns_only_a_mask(self):
        response, body = self.json(
            '/orcarouter/login/key', 'POST', {'api_key': FAKE_KEY}
        )
        assert response.code == 200
        rendered = json.dumps(body)
        assert FAKE_KEY not in rendered
        assert body['result']['credential']['accounts'][0]['api_key_masked']

    def test_a_key_without_the_prefix_is_refused(self):
        response, body = self.json(
            '/orcarouter/login/key', 'POST', {'api_key': 'sk-openai-nope'}
        )
        assert response.code == 400
        assert 'sk-orca-' in body['error']
        assert 'sk-openai-nope' not in json.dumps(body)

    def test_an_empty_key_is_refused(self):
        response, body = self.json('/orcarouter/login/key', 'POST', {})
        assert response.code == 400


class TestModelRouting(PanelTestCase):

    def test_models_endpoint_requires_a_known_capability(self):
        response, body = self.json('/orcarouter/models?capability=telepathy')
        assert response.code == 400

    def test_models_endpoint_returns_a_bounded_option_list(self):
        response, body = self.json('/orcarouter/models?capability=chat')
        assert response.code == 200
        result = body['result']
        assert result['capability'] == 'chat'
        assert result['provider_id'] == 'orcarouter'
        assert isinstance(result['options'], list)
        assert result['catalog_url'].endswith('/v1/models')
        # Every option carries the metadata the selector filters on.
        for option in result['options']:
            assert option['id']
            assert 'endpoint_types' in option
            assert 'input_modalities' in option

    def test_models_endpoint_never_returns_a_key(self):
        response = self.fetch('/orcarouter/models?capability=chat')
        assert FAKE_KEY not in response.body.decode('utf-8')

    def test_chat_refuses_a_model_outside_the_filtered_list(self):
        response, body = self.json(
            '/orcarouter/chat', 'POST',
            {'model': 'not/a/real/model', 'prompt': 'hello'},
        )
        assert response.code == 400
        assert 'filtered model list' in body['error']

    def test_chat_requires_both_fields(self):
        response, body = self.json('/orcarouter/chat', 'POST', {})
        assert response.code == 400


class TestOAuthLock(PanelTestCase):

    def test_cancel_releases_the_login_lock(self):
        response, body = self.json('/orcarouter/login/oauth/cancel', 'POST', {})
        assert response.code == 200
        assert body['result']['cancelled'] is True

    def test_start_returns_only_the_authorization_url(self):
        response, body = self.json('/orcarouter/login/oauth/start', 'POST', {})
        assert response.code == 200
        result = body['result']
        assert result['authorize_url'].startswith(
            'https://www.orcarouter.ai/auth?'
        )
        assert not result['authorize_url'
                         ].startswith('https://api.orcarouter.ai')
        assert result['auth_base'] == 'https://www.orcarouter.ai'
        # The verifier stays server side; it is not in the response.
        rendered = json.dumps(body)
        assert 'code_verifier' not in rendered
        assert 'verifier' not in rendered
        # The state travels only inside the authorize URL, which is where the
        # consent server expects it; it is not returned as a bare field.
        assert 'state' not in result

    def test_completing_an_unknown_generation_is_refused(self):
        response, body = self.json(
            '/orcarouter/login/oauth/complete', 'POST',
            {'generation': 99999, 'code': 'whatever'},
        )
        assert response.code == 409


class TestLogout(PanelTestCase):

    def test_logout_is_idempotent(self):
        response, body = self.json('/orcarouter/logout', 'POST', {})
        assert response.code == 200
        assert 'removed' in body['result']
