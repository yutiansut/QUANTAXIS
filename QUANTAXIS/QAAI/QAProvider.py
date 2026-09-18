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
"""OrcaRouter provider registry.

OrcaRouter is registered here as a *first-class named provider* -- it is not
a custom base URL bolted onto somebody else's entry.  Two authentication
choices share one inference adapter, one base URL and one model namespace,
exactly as the OrcaRouter integration guidance requires:

===============  ==================  ===================================
provider id      label               credential source
===============  ==================  ===================================
``orcarouter``   ``OrcaRouter - API``   user pastes an ``sk-orca-...`` key
``orcarouter-oauth``  ``OrcaRouter - Auth``  browser authorization (PKCE)
===============  ==================  ===================================

A generic "OrcaRouter" button that sometimes asks for a key and sometimes
opens a browser makes support, logout and reauthentication harder, so the two
choices stay explicitly separable while sharing everything downstream.
"""

from QUANTAXIS.QAAI.QAOrcaEndpoints import (
    ORCA_KEY_DASHBOARD_URL,
    resolve_endpoints,
)

__all__ = [
    'ORCA_PROVIDER_ID',
    'ORCA_OAUTH_PROVIDER_ID',
    'ORCA_PROVIDER_IDS',
    'ORCA_DEFAULT_MODEL',
    'ORCA_DEFAULT_AUTH_METHOD',
    'QAProvider',
    'QA_PROVIDERS',
    'get_provider',
    'provider_ids',
    'describe_providers',
    'reload_providers',
    'resolve_provider_endpoints',
]

ORCA_PROVIDER_ID = 'orcarouter'
ORCA_OAUTH_PROVIDER_ID = 'orcarouter-oauth'
ORCA_PROVIDER_IDS = (ORCA_PROVIDER_ID, ORCA_OAUTH_PROVIDER_ID)

ORCA_DEFAULT_MODEL = 'orcarouter/auto'
ORCA_DEFAULT_AUTH_METHOD = ORCA_PROVIDER_ID

#: Localization keys resolved through the project's locale catalogs.  The
#: English canonical value is kept as the fallback everywhere.
I18N_ORCA_PROVIDER_NAME = 'provider.orcarouter.name'
I18N_ORCA_OAUTH_PROVIDER_NAME = 'provider.orcarouter_oauth.name'
I18N_ORCA_PROVIDER_DESC = 'provider.orcarouter.description'


class QAProvider(object):
    """One selectable model provider.

    The OpenAI-compatible wire format is used for every provider here, so
    adding OrcaRouter does not require a bespoke transport.
    """

    def __init__(
        self,
        provider_id,
        label,
        label_key,
        description_key,
        base_url,
        auth_method,
        env_key,
        description='',
        default_model=ORCA_DEFAULT_MODEL,
        wire_api='openai',
        oauth=False,
    ):
        self.id = provider_id
        self.label = label
        self.label_key = label_key
        self.description = description
        self.description_key = description_key
        self.base_url = base_url
        self.auth_method = auth_method
        self.env_key = env_key
        self.default_model = default_model
        self.wire_api = wire_api
        self.oauth = oauth

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.label,
            'name_key': self.label_key,
            'description': self.description,
            'description_key': self.description_key,
            'base_url': self.base_url,
            'auth_method': self.auth_method,
            'env_key': self.env_key,
            'default_model': self.default_model,
            'wire_api': self.wire_api,
            'oauth': self.oauth,
            'key_dashboard_url': ORCA_KEY_DASHBOARD_URL,
        }

    def __repr__(self):
        return 'QAProvider({0!r}, base_url={1!r})'.format(
            self.id,
            self.base_url
        )


def _build_providers(endpoints=None):
    endpoints = endpoints or resolve_endpoints()
    return {
        ORCA_PROVIDER_ID:
            QAProvider(
                provider_id=ORCA_PROVIDER_ID,
                label='OrcaRouter - API',
                label_key=I18N_ORCA_PROVIDER_NAME,
                description='OrcaRouter (API key)',
                description_key=I18N_ORCA_PROVIDER_DESC,
                base_url=endpoints.api_base + '/v1',
                auth_method='api_key',
                env_key='ORCAROUTER_API_KEY',
            ),
        ORCA_OAUTH_PROVIDER_ID:
            QAProvider(
                provider_id=ORCA_OAUTH_PROVIDER_ID,
                label='OrcaRouter - Auth',
                label_key=I18N_ORCA_OAUTH_PROVIDER_NAME,
                description=
                'OrcaRouter (browser authorization, OAuth 2.0 + PKCE)',
                description_key=I18N_ORCA_PROVIDER_DESC,
                base_url=endpoints.api_base + '/v1',
                auth_method='oauth_pkce',
                env_key='ORCAROUTER_API_KEY',
                oauth=True,
            ),
    }


#: The registry.  It intentionally contains only OrcaRouter: QUANTAXIS ships
#: no other model provider, so this is the canonical place a future provider
#: is added rather than a per-page special case.
QA_PROVIDERS = _build_providers()


def reload_providers(endpoints=None):
    """Rebuild the registry after an origin override changed."""
    global QA_PROVIDERS
    QA_PROVIDERS = _build_providers(endpoints)
    return QA_PROVIDERS


def provider_ids():
    return list(QA_PROVIDERS)


def get_provider(provider_id):
    return QA_PROVIDERS.get(provider_id)


def describe_providers():
    """Registry contents for the GUI.  Contain no credentials."""
    return [provider.as_dict() for provider in QA_PROVIDERS.values()]


def resolve_provider_endpoints(**kwargs):
    """Expose origin resolution next to the registry for GUI/CLI use."""
    return resolve_endpoints(**kwargs)
