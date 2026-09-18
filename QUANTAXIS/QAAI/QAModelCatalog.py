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
"""OrcaRouter model catalog and capability filtering.

The single source of truth for the model list is ``GET {api_base}/models``
on the configured origin.  Nothing here invents model IDs: when live
discovery succeeds its result is authoritative, and when it fails a small,
independently verified cold-start seed is used and explicitly labelled
``degraded``.  A hand-written example list is never presented as the live
catalog.

Every downstream entry point asks for the capability it actually needs, so
the model selector can only ever offer models the gateway advertises as
compatible with that entry point.  A model whose metadata does not prove
compatibility fails closed rather than being guessed at from its name.
"""

import json
import urllib.error
import urllib.parse
import urllib.request

__all__ = [
    'CAPABILITY_CHAT',
    'CAPABILITY_EMBEDDING',
    'CAPABILITY_IMAGE',
    'CAPABILITY_VIDEO',
    'CAPABILITY_RERANK',
    'MODALITY_IMAGE',
    'MODALITY_AUDIO',
    'MODALITY_VIDEO',
    'TEXT_ENDPOINT_TYPES',
    'NON_TEXT_ENDPOINT_TYPES',
    'CATALOG_TIMEOUT',
    'CATALOG_MAX_BYTES',
    'CATALOG_MAX_ITEMS',
    'VERIFIED_SEED',
    'QAOrcaCatalogError',
    'QAOrcaModel',
    'filter_models',
    'models_for_capability',
    'parse_catalog',
    'seed_catalog',
    'discover_models',
    'QAOrcaModelSelector',
]

CAPABILITY_CHAT = 'chat'
CAPABILITY_EMBEDDING = 'embedding'
CAPABILITY_IMAGE = 'image'
CAPABILITY_VIDEO = 'video'
CAPABILITY_RERANK = 'rerank'

MODALITY_TEXT = 'text'
MODALITY_IMAGE = 'image'
MODALITY_AUDIO = 'audio'
MODALITY_VIDEO = 'video'

#: Endpoint types a text chat/agent entry point can actually speak.  A model
#: advertising only ``image-generation``, ``openai-video`` or ``jina-rerank``
#: is not a text model no matter what its name suggests.
TEXT_ENDPOINT_TYPES = frozenset(
    ('openai',
     'anthropic',
     'gemini',
     'openai-response')
)

#: Endpoint types that are specialised for a non-text task.  They are
#: subtracted from the chat capability so a mixed record cannot leak a
#: non-text model into a text picker.
NON_TEXT_ENDPOINT_TYPES = frozenset(
    ('image-generation',
     'openai-video',
     'jina-rerank',
     'embeddings')
)

#: Every route this client can actually speak.  A catalog record naming
#: anything else is dropped rather than displayed.
SUPPORTED_ENDPOINT_TYPES = TEXT_ENDPOINT_TYPES | NON_TEXT_ENDPOINT_TYPES

#: Bounds.  A catalog response must not be able to consume unbounded memory
#: or advertise routes this client cannot speak.
CATALOG_TIMEOUT = 15.0
CATALOG_MAX_BYTES = 4 * 1024 * 1024
CATALOG_MAX_ITEMS = 500

#: Cold-start seed used only when live discovery fails.  Each entry carries
#: its own verification note and its metadata, so an outage does not silently
#: downgrade reasoning, context, or input-modality information.  The
#: reasoning-effort ladder on ``openai/gpt-5.5`` is preserved deliberately.
VERIFIED_SEED = (
    {
        'id':
            'openai/gpt-5.5',
        'name':
            'OpenAI: GPT-5.5',
        'owned_by':
            'OpenAI',
        'context_length':
            400000,
        'max_completion_tokens':
            128000,
        'supported_endpoint_types': ['openai',
                                     'openai-response'],
        'architecture':
            {
                'input_modalities': ['text',
                                     'image',
                                     'file'],
                'output_modalities': ['text'],
            },
        'reasoning':
            {
                'supported': True,
                'efforts': ['low',
                            'medium',
                            'high',
                            'xhigh'],
            },
        'verified':
            True,
        'verified_note':
            (
                'reasoning effort ladder low/medium/high/xhigh verified against '
                'the OrcaRouter catalog'
            ),
    },
    {
        'id': 'anthropic/claude-opus-4.8',
        'name': 'Anthropic: Claude Opus 4.8',
        'owned_by': 'Anthropic',
        'context_length': 1000000,
        'max_completion_tokens': 128000,
        'supported_endpoint_types': ['openai',
                                     'anthropic',
                                     'openai-response'],
        'architecture':
            {
                'input_modalities': ['text',
                                     'image',
                                     'file'],
                'output_modalities': ['text'],
            },
        'verified': True,
    },
    {
        'id': 'google/gemini-3.5-flash',
        'name': 'Gemini 3.5 Flash',
        'owned_by': 'Google',
        'context_length': 1048576,
        'max_completion_tokens': 65536,
        'supported_endpoint_types': ['openai',
                                     'gemini'],
        'architecture':
            {
                'input_modalities': ['text',
                                     'image',
                                     'video',
                                     'file',
                                     'audio'],
                'output_modalities': ['text'],
            },
        'verified': True,
    },
    {
        'id': 'deepseek/deepseek-v4-pro',
        'name': 'DeepSeek: DeepSeek V4 Pro',
        'owned_by': 'custom',
        'context_length': 1048576,
        'max_completion_tokens': 384000,
        'supported_endpoint_types': ['openai',
                                     'openai-response'],
        'architecture':
            {
                'input_modalities': ['text'],
                'output_modalities': ['text'],
            },
        'verified': True,
    },
    {
        'id': 'orcarouter/auto',
        'name': 'OrcaRouter Auto',
        'owned_by': 'orcarouter',
        'supported_endpoint_types':
            ['openai',
             'openai-response',
             'anthropic',
             'gemini'],
        'architecture':
            {
                'input_modalities': ['text'],
                'output_modalities': ['text'],
            },
        'verified': True,
    },
)


class QAOrcaCatalogError(Exception):
    """Raised when the model catalog cannot be read."""


class QAOrcaModel(object):
    """One catalog entry, normalized but never renamed.

    ``id`` keeps the vendor/model namespace exactly as advertised, because
    that string is what the relay expects on the wire.
    """

    def __init__(
        self,
        model_id,
        name=None,
        endpoint_types=None,
        input_modalities=None,
        output_modalities=None,
        context_length=None,
        max_completion_tokens=None,
        reasoning=None,
        owned_by=None,
        verified=False,
        verified_note=None,
    ):
        self.id = model_id
        self.name = name or model_id
        self.endpoint_types = tuple(endpoint_types or ())
        self.input_modalities = tuple(input_modalities or ())
        self.output_modalities = tuple(output_modalities or ())
        self.context_length = context_length
        self.max_completion_tokens = max_completion_tokens
        self.reasoning = reasoning
        self.owned_by = owned_by
        self.verified = verified
        self.verified_note = verified_note

    @property
    def reasoning_efforts(self):
        if not isinstance(self.reasoning, dict):
            return ()
        return tuple(self.reasoning.get('efforts') or ())

    def supports_text_endpoint(self):
        return bool(TEXT_ENDPOINT_TYPES.intersection(self.endpoint_types))

    def supports_modality(self, modality):
        """Fail closed: an unstated modality is not supported."""
        return modality in self.input_modalities

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'owned_by': self.owned_by,
            'endpoint_types': list(self.endpoint_types),
            'input_modalities': list(self.input_modalities),
            'output_modalities': list(self.output_modalities),
            'context_length': self.context_length,
            'max_completion_tokens': self.max_completion_tokens,
            'reasoning': self.reasoning,
            'verified': self.verified,
            'verified_note': self.verified_note,
        }

    def __repr__(self):
        return 'QAOrcaModel({0!r})'.format(self.id)


def _coerce_model(record, verified=False):
    """Normalize one raw catalog record, rejecting unusable shapes."""
    if not isinstance(record, dict):
        return None
    model_id = record.get('id')
    if not isinstance(model_id, str) or not model_id.strip():
        return None
    if len(model_id) > 256:
        return None
    architecture = record.get('architecture')
    if not isinstance(architecture, dict):
        architecture = {}
    endpoint_types = record.get('supported_endpoint_types')
    if not isinstance(endpoint_types, (list, tuple)):
        endpoint_types = ()
    endpoint_types = tuple(
        item for item in endpoint_types if isinstance(item, str)
    )
    reasoning = record.get('reasoning')
    if not isinstance(reasoning, dict):
        reasoning = None

    def _int(value):
        return value if isinstance(value, int) and value > 0 else None

    return QAOrcaModel(
        model_id=model_id,
        name=record.get('name') if isinstance(record.get('name'),
                                              str) else None,
        owned_by=(
            record.get('owned_by') if isinstance(record.get('owned_by'),
                                                 str) else None
        ),
        endpoint_types=endpoint_types,
        input_modalities=architecture.get('input_modalities') or (),
        output_modalities=architecture.get('output_modalities') or (),
        context_length=_int(
            record.get('context_length')
            or (record.get('top_provider') or {}).get('context_length')
        ),
        max_completion_tokens=_int(
            record.get('max_completion_tokens')
            or (record.get('top_provider') or {}).get('max_completion_tokens')
        ),
        reasoning=reasoning,
        verified=verified or bool(record.get('verified')),
        verified_note=record.get('verified_note'),
    )


def parse_catalog(payload, max_items=CATALOG_MAX_ITEMS):
    """Turn a ``/v1/models`` payload into normalized models.

    Unusable records are dropped rather than raising, so one malformed entry
    cannot empty a working catalog.  The item count is bounded.
    """
    if isinstance(payload, (bytes, str)):
        try:
            payload = json.loads(payload)
        except ValueError:
            raise QAOrcaCatalogError('the model catalog was not valid JSON')
    if not isinstance(payload, dict):
        raise QAOrcaCatalogError('the model catalog had an unexpected shape')
    raw_items = payload.get('data')
    if raw_items is None:
        raw_items = payload.get('models')
    if not isinstance(raw_items, (list, tuple)):
        raise QAOrcaCatalogError('the model catalog carried no model list')

    models = []
    seen = set()
    for record in raw_items[:max_items]:
        model = _coerce_model(record)
        if model is None or model.id in seen:
            continue
        seen.add(model.id)
        models.append(model)
    return models


def seed_catalog():
    """The verified cold-start catalog, used when discovery fails."""
    return [
        model for model in
        (_coerce_model(dict(entry), verified=True) for entry in VERIFIED_SEED)
        if model is not None
    ]


def filter_models(models, capability, modalities=None, endpoint_types=None):
    """Filter ``models`` down to the entries compatible with one entry point.

    ``capability`` selects the family (chat / embedding / image / video /
    rerank).  ``modalities`` names the non-text modalities this entry point
    actually uploads; a model that does not explicitly declare every one of
    them is excluded -- unstated capability fails closed.
    """
    modalities = tuple(modalities or ())
    if capability == CAPABILITY_CHAT:
        required = TEXT_ENDPOINT_TYPES
        if endpoint_types:
            required = required.intersection(endpoint_types)
        allowed = []
        for model in models:
            types = set(model.endpoint_types)
            if types and not types.intersection(required):
                continue
            if types and types.issubset(NON_TEXT_ENDPOINT_TYPES):
                continue
            allowed.append(model)
    elif capability == CAPABILITY_EMBEDDING:
        allowed = [
            model for model in models if 'embeddings' in model.endpoint_types
        ]
    elif capability == CAPABILITY_IMAGE:
        allowed = [
            model for model in models
            if 'image-generation' in model.endpoint_types
        ]
    elif capability == CAPABILITY_VIDEO:
        allowed = [
            model for model in models if 'openai-video' in model.endpoint_types
        ]
    elif capability == CAPABILITY_RERANK:
        allowed = [
            model for model in models if 'jina-rerank' in model.endpoint_types
        ]
    else:
        raise QAOrcaCatalogError('unknown capability {0!r}'.format(capability))

    if modalities:
        allowed = [
            model for model in allowed
            if all(model.supports_modality(item) for item in modalities)
        ]
    return allowed


def models_for_capability(
    models,
    capability,
    modalities=None,
    endpoint_types=None,
    limit=None
):
    filtered = filter_models(
        models,
        capability,
        modalities=modalities,
        endpoint_types=endpoint_types,
    )
    if limit is not None and limit >= 0:
        filtered = filtered[:limit]
    return filtered


def _http_models(endpoints, api_key, capability, timeout, max_bytes):
    url = endpoints.models_url
    if capability:
        url = '{0}?{1}'.format(
            url,
            urllib.parse.urlencode({'capability': capability})
        )
    headers = {'Accept': 'application/json'}
    if api_key:
        headers['Authorization'] = 'Bearer {0}'.format(api_key)
    request = urllib.request.Request(url, headers=headers, method='GET')
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise QAOrcaCatalogError('the model catalog response was too large')
    return raw


def discover_models(
    endpoints,
    credential=None,
    capability=None,
    api_key=None,
    timeout=CATALOG_TIMEOUT,
    max_bytes=CATALOG_MAX_BYTES,
    fetcher=None,
):
    """Fetch the authoritative catalog from the configured API origin.

    The request is bounded in time, bytes and item count, and filters out
    records advertising endpoint types this client cannot speak.  The
    caller's own OrcaRouter API key is used so the result is the set this
    workspace can actually call.
    """
    if api_key is None and credential is not None:
        # Seam-agnostic: whichever adapter produced the credential, this is
        # the only thing read from it.
        api_key = credential.api_key()
    fetcher = fetcher or _http_models
    try:
        raw = fetcher(endpoints, api_key, capability, timeout, max_bytes)
    except urllib.error.HTTPError as error:
        raise QAOrcaCatalogError(
            'the model catalog request was rejected with HTTP {0}'.format(
                error.code
            )
        )
    except (urllib.error.URLError, OSError) as error:
        raise QAOrcaCatalogError(
            'could not reach the model catalog: {0}'.format(
                type(error).__name__
            )
        )
    models = parse_catalog(raw)
    # A record advertising an endpoint type this client has no route for is
    # dropped rather than surfaced: the selector must never offer a model
    # the transport cannot speak.
    models = [
        model for model in models
        if set(model.endpoint_types).issubset(SUPPORTED_ENDPOINT_TYPES)
    ]
    if capability:
        # The server-side `capability` query is a convenience, not a
        # contract: the filter that actually binds the control is applied
        # here, on the returned records.
        models = filter_models(models, capability)
    return models


class QAOrcaModelSelector(object):
    """Model options bound to (provider, capability, modalities).

    Options are always a filtered list, never free text.  When the inputs
    change the options are recomputed, and a previously selected model that
    is no longer compatible is cleared instead of being silently kept.
    """

    def __init__(self):
        self.provider_id = None
        self.capability = CAPABILITY_CHAT
        self.modalities = ()
        self.models = []
        self.selected = None
        self.source = 'none'
        self.degraded = False
        self.error = None
        self.loading = False

    def options(self):
        return models_for_capability(
            self.models,
            self.capability,
            modalities=self.modalities,
        )

    def option_ids(self):
        return [model.id for model in self.options()]

    def set_provider(self, provider_id):
        """Switching provider recomputes the options and drops the selection."""
        if provider_id == self.provider_id:
            return False
        self.provider_id = provider_id
        self.selected = None
        self.models = []
        self.source = 'none'
        self.degraded = False
        self.error = None
        return True

    def set_capability(self, capability, modalities=None):
        """Changing capability/attachments recomputes the options."""
        modalities = tuple(modalities or ())
        changed = (
            capability != self.capability or modalities != self.modalities
        )
        self.capability = capability
        self.modalities = modalities
        if changed:
            self._drop_incompatible_selection()
        return changed

    def load(self, models, source='live', degraded=False, error=None):
        """Install a catalog result and re-validate the current selection."""
        self.models = list(models)
        self.source = source
        self.degraded = degraded
        self.error = error
        self.loading = False
        self._drop_incompatible_selection()
        return self.options()

    def load_seed(self, error=None):
        """Degraded fallback: the verified seed, clearly labelled as such."""
        return self.load(
            seed_catalog(),
            source='seed',
            degraded=True,
            error=error
        )

    def select(self, model_id):
        if model_id not in self.option_ids():
            raise QAOrcaCatalogError(
                '{0!r} is not in the current filtered model list'
                .format(model_id)
            )
        self.selected = model_id
        return model_id

    def _drop_incompatible_selection(self):
        """Clear a stale selection.  Never silently keep a wrong value."""
        if self.selected is not None and self.selected not in self.option_ids():
            self.selected = None
            return True
        return False

    def snapshot(self):
        return {
            'provider_id': self.provider_id,
            'capability': self.capability,
            'modalities': list(self.modalities),
            'options': [model.as_dict() for model in self.options()],
            'selected': self.selected,
            'source': self.source,
            'degraded': self.degraded,
            'loading': self.loading,
            'error': self.error,
        }
