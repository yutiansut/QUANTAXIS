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
"""Facade binding the OrcaRouter pieces together.

One object is shared by the CLI, the tornado handlers and the GUI panel, so
provider selection, credential resolution, model discovery and inference all
run through the same code path no matter which entry point the user came
from.  It deliberately exposes the two authentication choices as separate,
independently testable methods.
"""

import threading

from QUANTAXIS.QAAI.QAModelCatalog import (
    CAPABILITY_CHAT,
    QAOrcaCatalogError,
    QAOrcaModelSelector,
    discover_models,
    seed_catalog,
)
from QUANTAXIS.QAAI.QAOrcaClient import QAOrcaClient
from QUANTAXIS.QAAI.QAOrcaCredential import (
    ORCA_SOURCE_OAUTH_PKCE,
    QAOrcaApiKeyAdapter,
    QAOrcaCredentialError,
    QAOrcaCredentialStore,
)
from QUANTAXIS.QAAI.QAOrcaAuth import QAOrcaLoginSession, QAOrcaPkceAdapter
from QUANTAXIS.QAAI.QAOrcaEndpoints import ORCA_KEY_DASHBOARD_URL, resolve_endpoints
from QUANTAXIS.QAAI.QAProvider import (
    ORCA_DEFAULT_MODEL,
    ORCA_OAUTH_PROVIDER_ID,
    ORCA_PROVIDER_ID,
    ORCA_PROVIDER_IDS,
    describe_providers,
    get_provider,
)

__all__ = ['QAOrcaService', 'get_orca_service', 'reset_orca_service']

_SERVICE = None
_SERVICE_LOCK = threading.Lock()


class QAOrcaService(object):
    """Shared, credential-source-agnostic OrcaRouter facade."""

    def __init__(self, store=None, endpoints=None):
        self.store = store or QAOrcaCredentialStore()
        self.endpoints = endpoints or resolve_endpoints()
        self.session = QAOrcaLoginSession(
            adapter=QAOrcaPkceAdapter(
                store=self.store,
                endpoints=self.endpoints
            )
        )
        self.pending_attempt = None
        self.last_catalog_error = None

    # -- registry -------------------------------------------------------
    def providers(self):
        """The provider registry, for the selection control."""
        registered = describe_providers()
        for entry in registered:
            entry['base_url'] = self.endpoints.api_base + '/v1'
        return registered

    def provider_for(self, provider_id):
        if provider_id not in ORCA_PROVIDER_IDS:
            raise QAOrcaCredentialError(
                'unknown OrcaRouter provider {0!r}'.format(provider_id)
            )
        return get_provider(provider_id)

    def normalize_provider_id(self, provider_id):
        """Map any registry id (or a bare 'OrcaRouter') onto a real id."""
        if not provider_id:
            return ORCA_PROVIDER_ID
        if provider_id in ORCA_PROVIDER_IDS:
            return provider_id
        if provider_id.lower() in ('orcarouter', 'orca'):
            return ORCA_PROVIDER_ID
        raise QAOrcaCredentialError(
            'unknown OrcaRouter provider {0!r}'.format(provider_id)
        )

    # -- credential seam ------------------------------------------------
    def credential_provider(self, provider_id=ORCA_PROVIDER_ID):
        """Return the credential adapter for one authentication choice."""
        provider_id = self.normalize_provider_id(provider_id)
        if provider_id == ORCA_OAUTH_PROVIDER_ID:
            adapter = QAOrcaPkceAdapter(
                store=self.store,
                endpoints=self.endpoints
            )
            adapter.source = ORCA_SOURCE_OAUTH_PKCE
            return adapter
        return QAOrcaApiKeyAdapter(store=self.store)

    def status(self):
        """Redacted credential status.  Never returns a key."""
        stored = self.store.status()
        api_key_env_present = bool(
            QAOrcaApiKeyAdapter(store=self.store)._from_env()
        )
        return {
            'providers':
                self.providers(),
            'default_provider':
                ORCA_PROVIDER_ID,
            'default_model':
                ORCA_DEFAULT_MODEL,
            'api_key_env_present':
                api_key_env_present,
            'key_dashboard_url':
                ORCA_KEY_DASHBOARD_URL,
            'endpoints':
                self.endpoints.as_dict(),
            'credential':
                stored,
            'auth_methods':
                [
                    {
                        'id': ORCA_PROVIDER_ID,
                        'label': 'OrcaRouter - API',
                        'kind': 'api_key',
                    },
                    {
                        'id': ORCA_OAUTH_PROVIDER_ID,
                        'label': 'OrcaRouter - Auth',
                        'kind': 'oauth_pkce',
                    },
                ],
        }

    def login_with_key(self, api_key):
        """Authentication choice 1: persist a pasted key."""
        adapter = QAOrcaApiKeyAdapter(store=self.store)
        return adapter.save(api_key)

    def oauth_start(self):
        """Authentication choice 2, step 1: produce the consent URL."""
        attempt = self.session.begin()
        # Remembered so a second invocation (a paste-back after the terminal
        # closed, for instance) can finish the same attempt.  The verifier
        # never leaves this process.
        self.pending_attempt = attempt
        return attempt

    def oauth_complete(self, generation, pasted, verifier, state):
        return self.session.complete(generation, pasted, verifier, state)

    def oauth_snapshot(self):
        return self.session.snapshot()

    def oauth_cancel(self, generation=None):
        return self.session.cancel(generation)

    def oauth_pagehide(self, generation=None):
        return self.session.pagehide(generation)

    def logout(self, account_id=None):
        self.session.cancel()
        return self.store.clear(account_id)

    # -- model catalog --------------------------------------------------
    def client(self, provider_id=ORCA_PROVIDER_ID):
        return QAOrcaClient(
            credential=self.credential_provider(provider_id),
            endpoints=self.endpoints,
            store=self.store,
        )

    def models(
        self,
        provider_id=ORCA_PROVIDER_ID,
        capability=None,
        refresh=False
    ):
        """Authoritative catalog, with a labelled degraded fallback.

        A live result is used exactly as returned.  On failure the verified
        seed is served together with ``degraded=True`` and the error, so a
        catalog outage never turns the selector into free text and never
        passes a seed off as the live list.
        """
        provider_id = self.normalize_provider_id(provider_id)
        try:
            credential = self.credential_provider(provider_id)
            models = discover_models(
                self.endpoints,
                credential=credential,
                capability=capability,
            )
        except (QAOrcaCatalogError, QAOrcaCredentialError) as error:
            self.last_catalog_error = str(error)
            return {
                'provider_id': provider_id,
                'source': 'seed',
                'degraded': True,
                'error': str(error),
                'models': [model.as_dict() for model in seed_catalog()],
            }
        if not models:
            self.last_catalog_error = 'the catalog returned no usable models'
            return {
                'provider_id': provider_id,
                'source': 'seed',
                'degraded': True,
                'error': self.last_catalog_error,
                'models': [model.as_dict() for model in seed_catalog()],
            }
        self.last_catalog_error = None
        return {
            'provider_id': provider_id,
            'source': 'live',
            'degraded': False,
            'error': None,
            'models': [model.as_dict() for model in models],
        }

    def selector(
        self,
        provider_id=ORCA_PROVIDER_ID,
        capability=CAPABILITY_CHAT,
        modalities=None
    ):
        """A model selector bound to one capability, already filtered."""
        from QUANTAXIS.QAAI.QAModelCatalog import QAOrcaModel

        selector = QAOrcaModelSelector()
        selector.set_provider(self.normalize_provider_id(provider_id))
        selector.set_capability(capability, modalities)
        catalog = self.models(provider_id, capability=capability)
        selector.load(
            [
                QAOrcaModel(
                    model_id=item['id'],
                    name=item.get('name'),
                    endpoint_types=item.get('endpoint_types'),
                    input_modalities=item.get('input_modalities'),
                    output_modalities=item.get('output_modalities'),
                    context_length=item.get('context_length'),
                    max_completion_tokens=item.get('max_completion_tokens'),
                    reasoning=item.get('reasoning'),
                    owned_by=item.get('owned_by'),
                    verified=item.get('verified'),
                    verified_note=item.get('verified_note'),
                ) for item in catalog['models']
            ],
            source=catalog['source'],
            degraded=catalog['degraded'],
            error=catalog['error'],
        )
        return selector

    # -- inference ------------------------------------------------------
    def chat(
        self,
        messages,
        model=None,
        provider_id=ORCA_PROVIDER_ID,
        **kwargs
    ):
        if model is None:
            raise QAOrcaCredentialError(
                'select a model from the OrcaRouter catalog first'
            )
        return self.client(provider_id).chat(messages, model=model, **kwargs)


def get_orca_service():
    """Process-wide service, used by the CLI and the tornado handlers."""
    global _SERVICE
    if _SERVICE is None:
        with _SERVICE_LOCK:
            if _SERVICE is None:
                _SERVICE = QAOrcaService()
    return _SERVICE


def reset_orca_service(service=None):
    global _SERVICE
    with _SERVICE_LOCK:
        _SERVICE = service
    return _SERVICE
