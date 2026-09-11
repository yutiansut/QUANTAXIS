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
"""OrcaRouter AI layer for QUANTAXIS.

QUANTAXIS ships no model provider of its own, so this package introduces the
provider seam once -- registry, credential seam, connect flows, model catalog
and OpenAI-compatible transport -- and every entry point (CLI, tornado
backend, GUI panel) binds to that seam rather than carrying its own copy of
the authentication or discovery logic.

Nothing here imports `QUANTAXIS/__init__.py`, so the AI layer stays usable
from tests and tools without the full quant stack (pandas, matplotlib,
MongoDB, ...) being importable.
"""

from QUANTAXIS.QAAI.QAOrcaEndpoints import (
    ORCA_APP_NAME,
    ORCA_AUTHORIZE_PATH,
    ORCA_CHAT_PATH,
    ORCA_EXCHANGE_PATH,
    ORCA_KEY_DASHBOARD_URL,
    ORCA_LOGO_URL,
    ORCA_MODELS_PATH,
    ORCA_PUBLIC_API_BASE,
    ORCA_PUBLIC_AUTH_BASE,
    QAOrcaEndpoints,
    resolve_endpoints,
)
from QUANTAXIS.QAAI.QAOrcaCredential import (
    CREDENTIAL_NEEDS_REAUTH,
    CREDENTIAL_OK,
    ORCA_KEY_PREFIX,
    ORCA_SOURCE_API_KEY,
    ORCA_SOURCE_OAUTH_PKCE,
    QAOrcaApiKeyAdapter,
    QAOrcaCredentialError,
    QAOrcaCredentialProvider,
    QAOrcaCredentialResult,
    QAOrcaCredentialStore,
    classify_auth_failure,
    default_credential_path,
    looks_like_orcarouter_key,
    mask_key,
)
from QUANTAXIS.QAAI.QAOrcaAuth import (
    FLOW_LOOPBACK,
    FLOW_OUT_OF_BAND,
    QAOrcaAuthDenied,
    QAOrcaAuthTimeout,
    QAOrcaLoginSession,
    QAOrcaLoopbackListener,
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
from QUANTAXIS.QAAI.QAModelCatalog import (
    CAPABILITY_CHAT,
    CAPABILITY_EMBEDDING,
    CAPABILITY_IMAGE,
    CAPABILITY_RERANK,
    CAPABILITY_VIDEO,
    QAOrcaCatalogError,
    QAOrcaModel,
    QAOrcaModelSelector,
    discover_models,
    filter_models,
    models_for_capability,
    parse_catalog,
    seed_catalog,
)
from QUANTAXIS.QAAI.QAOrcaClient import (
    QAOrcaClient,
    QAOrcaInferenceError,
    QAOrcaNeedsReauth,
    QAOrcaRateLimited,
)
from QUANTAXIS.QAAI.QAProvider import (
    ORCA_DEFAULT_MODEL,
    ORCA_OAUTH_PROVIDER_ID,
    ORCA_PROVIDER_ID,
    ORCA_PROVIDER_IDS,
    QA_PROVIDERS,
    QAProvider,
    describe_providers,
    get_provider,
    provider_ids,
    reload_providers,
)

__all__ = [
    'ORCA_APP_NAME',
    'ORCA_AUTHORIZE_PATH',
    'ORCA_CHAT_PATH',
    'ORCA_EXCHANGE_PATH',
    'ORCA_KEY_DASHBOARD_URL',
    'ORCA_LOGO_URL',
    'ORCA_MODELS_PATH',
    'ORCA_PUBLIC_API_BASE',
    'ORCA_PUBLIC_AUTH_BASE',
    'QAOrcaEndpoints',
    'resolve_endpoints',
    'CREDENTIAL_NEEDS_REAUTH',
    'CREDENTIAL_OK',
    'ORCA_KEY_PREFIX',
    'ORCA_SOURCE_API_KEY',
    'ORCA_SOURCE_OAUTH_PKCE',
    'QAOrcaApiKeyAdapter',
    'QAOrcaCredentialError',
    'QAOrcaCredentialProvider',
    'QAOrcaCredentialResult',
    'QAOrcaCredentialStore',
    'classify_auth_failure',
    'default_credential_path',
    'looks_like_orcarouter_key',
    'mask_key',
    'FLOW_LOOPBACK',
    'FLOW_OUT_OF_BAND',
    'QAOrcaAuthDenied',
    'QAOrcaAuthTimeout',
    'QAOrcaLoginSession',
    'QAOrcaLoopbackListener',
    'QAOrcaPkceAdapter',
    'QAOrcaPkceError',
    'QAOrcaScopeDowngrade',
    'build_authorize_url',
    'code_challenge_for',
    'exchange_code',
    'generate_state',
    'generate_verifier',
    'parse_callback_url',
    'CAPABILITY_CHAT',
    'CAPABILITY_EMBEDDING',
    'CAPABILITY_IMAGE',
    'CAPABILITY_RERANK',
    'CAPABILITY_VIDEO',
    'QAOrcaCatalogError',
    'QAOrcaModel',
    'QAOrcaModelSelector',
    'discover_models',
    'filter_models',
    'models_for_capability',
    'parse_catalog',
    'seed_catalog',
    'QAOrcaClient',
    'QAOrcaInferenceError',
    'QAOrcaNeedsReauth',
    'QAOrcaRateLimited',
    'ORCA_DEFAULT_MODEL',
    'ORCA_OAUTH_PROVIDER_ID',
    'ORCA_PROVIDER_ID',
    'ORCA_PROVIDER_IDS',
    'QA_PROVIDERS',
    'QAProvider',
    'describe_providers',
    'get_provider',
    'provider_ids',
    'reload_providers',
]
