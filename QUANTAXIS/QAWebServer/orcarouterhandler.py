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
"""Tornado handlers and GUI panel for the OrcaRouter provider.

The browser holds **no** OrcaRouter API key.  Key entry is a POST of the
user's own paste, and every catalog/inference call is made server-side with
the stored credential; the panel only ever receives minimal model metadata.
The PKCE verifier never leaves the server process either -- the connect flow
is keyed by a server-side generation id.

Registered in ``QUANTAXIS/QAWebServer/server.py`` alongside the existing
handlers.
"""

import json
import os

from QUANTAXIS.QAAI.QAOrcaCredential import QAOrcaCredentialError
from QUANTAXIS.QAAI.QAOrcaI18n import (
    DEFAULT_LOCALE,
    TRANSLATIONS,
    available_locales,
    translate,
)
from QUANTAXIS.QAAI.QAOrcaService import get_orca_service
from QUANTAXIS.QAAI.QAModelCatalog import (
    CAPABILITY_CHAT,
    CAPABILITY_EMBEDDING,
    CAPABILITY_IMAGE,
    CAPABILITY_RERANK,
    CAPABILITY_VIDEO,
)
from QUANTAXIS.QAWebServer.basehandles import QABaseHandler

__all__ = [
    'ORCAROUTER_HANDLERS',
    'QAOrcaPanelHandler',
    'QAOrcaLogoHandler',
    'QAOrcaStatusHandler',
    'QAOrcaApiKeyHandler',
    'QAOrcaOAuthStartHandler',
    'QAOrcaOAuthCompleteHandler',
    'QAOrcaOAuthCancelHandler',
    'QAOrcaLogoutHandler',
    'QAOrcaModelsHandler',
    'QAOrcaChatHandler',
    'panel_path',
]

UI_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'orcarouter_ui'
)
PANEL_FILE = os.path.join(UI_DIR, 'panel.html')

CAPABILITIES = (
    CAPABILITY_CHAT,
    CAPABILITY_EMBEDDING,
    CAPABILITY_IMAGE,
    CAPABILITY_VIDEO,
    CAPABILITY_RERANK,
)


def panel_path():
    return PANEL_FILE


def _run_blocking(function, *args, **kwargs):
    """Run a blocking network call off the IOLoop."""
    import tornado.ioloop

    return tornado.ioloop.IOLoop.current().run_in_executor(
        None, lambda: function(*args, **kwargs)
    )


class QAOrcaBaseHandler(QABaseHandler):
    """Shared JSON plumbing."""

    def set_default_headers(self):
        super(QAOrcaBaseHandler, self).set_default_headers()
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def write_json(self, payload, status=200):
        self.set_status(status)
        self.write(json.dumps(payload, ensure_ascii=False))

    def body_json(self):
        raw = self.request.body or b'{}'
        try:
            return json.loads(raw.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            return {}

    @property
    def service(self):
        return get_orca_service()

    def requested_locale(self):
        # Named to avoid tornado's own RequestHandler.locale.
        return self.get_argument('locale', DEFAULT_LOCALE)

    def t(self, key, **kwargs):
        return translate(key, self.requested_locale(), **kwargs)


class QAOrcaPanelHandler(QAOrcaBaseHandler):
    """Serve the real OrcaRouter configuration panel."""

    def set_default_headers(self):
        super(QAOrcaPanelHandler, self).set_default_headers()
        self.set_header('Content-Type', 'text/html; charset=utf-8')

    def get(self):
        locale = self.requested_locale()
        service = self.service
        status = service.status()
        bootstrap = {
            'locale': locale,
            'available_locales': available_locales(),
            'i18n':
                {
                    key: translate(key,
                                   locale)
                    for key in sorted(TRANSLATIONS['en'])
                },
            'status': status,
            'capabilities': list(CAPABILITIES),
        }
        with open(panel_path(), 'r', encoding='utf-8') as handle:
            html = handle.read()
        html = html.replace(
            '/*__ORCA_BOOTSTRAP__*/',
            'window.QA_ORCAROUTER = {0};'.format(
                json.dumps(bootstrap,
                           ensure_ascii=False)
            ),
        )
        self.write(html)


class QAOrcaLogoHandler(QAOrcaBaseHandler):
    """Serve the official OrcaRouter mark from the local origin.

    The panel points its ``<img>`` at the canonical
    ``https://www.orcarouter.ai/orca-logo-classic.png`` first and falls back
    to this route, because a self-hosted QUANTAXIS install (a LAN box, an
    air-gapped deployment, a browser behind an authenticated proxy) often
    cannot reach the public origin directly.  The bytes are always the
    official asset, fetched server-side and size-bounded; nothing is drawn
    or substituted.
    """

    def set_default_headers(self):
        super(QAOrcaLogoHandler, self).set_default_headers()
        self.set_header('Content-Type', 'image/png')

    async def get(self):
        if self.application.settings.get('qa_orca_logo_cache') is None:
            try:
                data = await _run_blocking(_fetch_logo)
            except Exception:
                self.set_status(502)
                self.finish()
                return
            self.application.settings['qa_orca_logo_cache'] = data
        self.set_header('Cache-Control', 'public, max-age=86400')
        self.write(self.application.settings['qa_orca_logo_cache'])


def _fetch_logo():
    import urllib.request

    from QUANTAXIS.QAAI.QAOrcaEndpoints import ORCA_LOGO_URL

    with urllib.request.urlopen(ORCA_LOGO_URL, timeout=10) as response:
        data = response.read(512 * 1024)
    if not data.startswith(b'\x89PNG'):
        raise ValueError('the OrcaRouter logo was not a PNG')
    return data


class QAOrcaStatusHandler(QAOrcaBaseHandler):

    def get(self):
        self.write_json({'status': 200, 'result': self.service.status()})


class QAOrcaApiKeyHandler(QAOrcaBaseHandler):
    """Authentication choice 1: accept a pasted key.  Response is redacted."""

    async def post(self):
        payload = self.body_json()
        api_key = (payload.get('api_key') or '').strip()
        if not api_key:
            self.write_json(
                {
                    'status': 400,
                    'error': 'an API key is required'
                },
                status=400
            )
            return
        try:
            account_id = await _run_blocking(
                self.service.login_with_key,
                api_key
            )
        except QAOrcaCredentialError as error:
            self.write_json({'status': 400, 'error': str(error)}, status=400)
            return
        # The key is never echoed back, in any form other than its mask.
        self.write_json(
            {
                'status': 200,
                'result':
                    {
                        'account_id': account_id,
                        'credential': self.service.status()['credential'],
                    },
            }
        )


class QAOrcaOAuthStartHandler(QAOrcaBaseHandler):
    """Authentication choice 2, step 1.

    Returns the authorization URL only.  The verifier stays on the server,
    keyed by the generation returned here.
    """

    async def post(self):
        attempt = await _run_blocking(self.service.oauth_start)
        if attempt is None:
            self.write_json(
                {
                    'status': 409,
                    'error': 'a login attempt is already current'
                },
                status=409,
            )
            return
        self.write_json(
            {
                'status': 200,
                'result':
                    {
                        'generation': attempt['generation'],
                        'authorize_url': attempt['authorize_url'],
                        'auth_base': self.service.endpoints.auth_base,
                    },
            }
        )


class QAOrcaOAuthCompleteHandler(QAOrcaBaseHandler):
    """Authentication choice 2, step 2: exchange the shown code."""

    async def post(self):
        payload = self.body_json()
        generation = payload.get('generation')
        code = (payload.get('code') or '').strip()
        attempt = self.service.pending_attempt
        if not attempt or attempt['generation'] != generation:
            self.write_json(
                {
                    'status': 409,
                    'error': 'that login attempt is no longer '
                             'current'
                },
                status=409
            )
            return
        if not code:
            self.write_json(
                {
                    'status': 400,
                    'error': 'an authorization code is required'
                },
                status=400,
            )
            return
        try:
            done = await _run_blocking(
                self.service.oauth_complete,
                generation,
                code,
                attempt['verifier'],
                attempt['state'],
            )
        except QAOrcaCredentialError as error:
            self.write_json({'status': 400, 'error': str(error)}, status=400)
            return
        snapshot = self.service.oauth_snapshot()
        # The exchanged key is stored server-side and is not returned here.
        self.write_json(
            {
                'status': 200 if done else 400,
                'result':
                    {
                        'connected': bool(done),
                        'error': snapshot['error'],
                        'credential': self.service.status()['credential'],
                    },
            },
            status=200 if done else 400,
        )


class QAOrcaOAuthCancelHandler(QAOrcaBaseHandler):
    """Release the login lock: Cancel, provider switch, unmount, pagehide."""

    async def post(self):
        payload = self.body_json()
        await _run_blocking(
            self.service.oauth_cancel,
            payload.get('generation')
        )
        self.write_json({'status': 200, 'result': {'cancelled': True}})


class QAOrcaLogoutHandler(QAOrcaBaseHandler):

    async def post(self):
        removed = await _run_blocking(self.service.logout)
        self.write_json(
            {
                'status': 200,
                'result':
                    {
                        'removed': bool(removed),
                        'credential': self.service.status()['credential'],
                    },
            }
        )


class QAOrcaModelsHandler(QAOrcaBaseHandler):
    """Live catalog, capability-filtered server-side.

    The API key stays on the server; only model metadata crosses to the
    browser.
    """

    async def get(self):
        provider_id = self.service.normalize_provider_id(
            self.get_argument('provider_id',
                              None)
        )
        capability = self.get_argument('capability', CAPABILITY_CHAT)
        if capability not in CAPABILITIES:
            self.write_json(
                {
                    'status': 400,
                    'error': 'unknown capability'
                },
                status=400
            )
            return
        modalities = [item for item in self.get_arguments('modality') if item]
        selector = await _run_blocking(
            self.service.selector,
            provider_id,
            capability,
            modalities
        )
        snapshot = selector.snapshot()
        self.write_json(
            {
                'status': 200,
                'result':
                    {
                        'provider_id':
                            provider_id,
                        'capability':
                            capability,
                        'modalities':
                            modalities,
                        'source':
                            snapshot['source'],
                        'degraded':
                            snapshot['degraded'],
                        'error':
                            snapshot['error'],
                        'options':
                            snapshot['options'],
                        'selected':
                            snapshot['selected'],
                        'catalog_url':
                            '{0}/v1/models'.format(
                                self.service.endpoints.api_base
                            ),
                    },
            }
        )


class QAOrcaChatHandler(QAOrcaBaseHandler):

    async def post(self):
        payload = self.body_json()
        model = (payload.get('model') or '').strip()
        prompt = payload.get('prompt') or ''
        if not model or not prompt:
            self.write_json(
                {
                    'status': 400,
                    'error': 'model and prompt are required'
                },
                status=400,
            )
            return
        selector = await _run_blocking(self.service.selector)
        if model not in selector.option_ids():
            self.write_json(
                {
                    'status': 400,
                    'error':
                        '{0!r} is not in the current filtered model '
                        'list'.format(model),
                },
                status=400,
            )
            return
        try:
            response = await _run_blocking(
                self.service.chat,
                [{
                    'role': 'user',
                    'content': prompt
                }],
                model,
            )
        except QAOrcaCredentialError as error:
            self.write_json({'status': 502, 'error': str(error)}, status=502)
            return
        choices = response.get('choices') or []
        content = ''
        if choices:
            content = (choices[0].get('message') or {}).get('content') or ''
        self.write_json(
            {
                'status': 200,
                'result': {
                    'model': model,
                    'content': content
                },
            }
        )


ORCAROUTER_HANDLERS = [
    (r'/orcarouter/?',
     QAOrcaPanelHandler),
    (r'/orcarouter/asset/logo/?',
     QAOrcaLogoHandler),
    (r'/orcarouter/status/?',
     QAOrcaStatusHandler),
    (r'/orcarouter/login/key/?',
     QAOrcaApiKeyHandler),
    (r'/orcarouter/login/oauth/start/?',
     QAOrcaOAuthStartHandler),
    (r'/orcarouter/login/oauth/complete/?',
     QAOrcaOAuthCompleteHandler),
    (r'/orcarouter/login/oauth/cancel/?',
     QAOrcaOAuthCancelHandler),
    (r'/orcarouter/logout/?',
     QAOrcaLogoutHandler),
    (r'/orcarouter/models/?',
     QAOrcaModelsHandler),
    (r'/orcarouter/chat/?',
     QAOrcaChatHandler),
]
