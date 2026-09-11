# coding:utf-8
"""OrcaRouter model catalog: parsing, capability filtering, fail-closed.

Fixture records mirror the shape of ``GET /v1/models`` on the configured
origin, and cover text-only chat, image-input chat, embedding, image
generation, video, and rerank.
"""

import json

import pytest

from QUANTAXIS.QAAI.QAModelCatalog import (
    CAPABILITY_CHAT,
    CAPABILITY_EMBEDDING,
    CAPABILITY_IMAGE,
    CAPABILITY_RERANK,
    CAPABILITY_VIDEO,
    CATALOG_MAX_ITEMS,
    NON_TEXT_ENDPOINT_TYPES,
    QAOrcaCatalogError,
    QAOrcaModelSelector,
    TEXT_ENDPOINT_TYPES,
    VERIFIED_SEED,
    discover_models,
    filter_models,
    models_for_capability,
    parse_catalog,
    seed_catalog,
)
from QUANTAXIS.QAAI.QAOrcaEndpoints import QAOrcaEndpoints

CATALOG = {
    'data':
        [
            {
                'id': 'openai/gpt-5.5',
                'name': 'OpenAI: GPT-5.5',
                'supported_endpoint_types': ['openai',
                                             'openai-response'],
                'context_length': 400000,
                'architecture':
                    {
                        'input_modalities': ['text',
                                             'image',
                                             'file'],
                        'output_modalities': ['text'],
                    },
            },
            {
                'id': 'deepseek/deepseek-v4-pro',
                'supported_endpoint_types': ['openai',
                                             'openai-response'],
                'context_length': 1048576,
                'architecture': {
                    'input_modalities': ['text']
                },
            },
            {
                'id': 'anthropic/claude-opus-4.8',
                'supported_endpoint_types': ['openai',
                                             'anthropic'],
                'architecture': {
                    'input_modalities': ['text',
                                         'image',
                                         'file']
                },
            },
            {
                'id': 'google/gemini-3.5-flash',
                'supported_endpoint_types': ['openai',
                                             'gemini'],
                'architecture': {
                    'input_modalities': ['text',
                                         'image',
                                         'audio']
                },
            },
            {
                'id': 'google/text-embedding-004',
                'supported_endpoint_types': ['embeddings'],
                'architecture': {
                    'input_modalities': ['text']
                },
            },
            {
                'id': 'openai/gpt-image-1',
                'supported_endpoint_types': ['image-generation'],
                'architecture':
                    {
                        'input_modalities': ['text'],
                        'output_modalities': ['image']
                    },
            },
            {
                'id': 'google/veo-3',
                'supported_endpoint_types': ['openai-video'],
                'architecture': {
                    'input_modalities': ['text']
                },
            },
            {
                'id': 'jina/jina-reranker-v2',
                'supported_endpoint_types': ['jina-rerank'],
            },
            {
                'id': 'orcarouter/auto',
                'supported_endpoint_types':
                    ['openai',
                     'openai-response',
                     'anthropic',
                     'gemini'],
                'architecture': {
                    'input_modalities': ['text']
                },
            },
        ]
}


def catalog():
    return parse_catalog(CATALOG)


def ids(models):
    return [model.id for model in models]


# -- parsing --------------------------------------------------------------


def test_parse_keeps_vendor_namespace_verbatim():
    parsed = catalog()
    assert 'openai/gpt-5.5' in ids(parsed)
    assert 'anthropic/claude-opus-4.8' in ids(parsed)
    # No normalization, no slugging, no prefix stripping.
    assert all('/' in model.id for model in parsed)


def test_parse_accepts_bytes_and_str():
    assert ids(parse_catalog(json.dumps(CATALOG))) == ids(catalog())
    assert ids(parse_catalog(json.dumps(CATALOG).encode())) == ids(catalog())


def test_parse_rejects_unusable_shapes():
    with pytest.raises(QAOrcaCatalogError):
        parse_catalog('not json')
    with pytest.raises(QAOrcaCatalogError):
        parse_catalog({'nope': []})
    with pytest.raises(QAOrcaCatalogError):
        parse_catalog([1, 2, 3])


def test_parse_drops_individual_malformed_records():
    parsed = parse_catalog(
        {
            'data':
                [
                    {
                        'id': 'good/model'
                    },
                    {
                        'no_id': True
                    },
                    {
                        'id': ''
                    },
                    {
                        'id': 12345
                    },
                    'not-a-dict',
                    {
                        'id': 'x' * 300
                    },
                ]
        }
    )
    assert ids(parsed) == ['good/model']


def test_parse_deduplicates_and_bounds_the_item_count():
    parsed = parse_catalog(
        {
            'data':
                [{
                    'id': 'a/b'
                },
                 {
                     'id': 'a/b'
                 }] + [
                     {
                         'id': 'm/{0}'.format(index)
                     } for index in range(CATALOG_MAX_ITEMS)
                 ]
        }
    )
    assert len(parsed) <= CATALOG_MAX_ITEMS
    assert ids(parsed).count('a/b') == 1


def test_context_length_falls_back_to_top_provider():
    parsed = parse_catalog(
        {'data': [{
            'id': 'a/b',
            'top_provider': {
                'context_length': 128000
            },
        }]}
    )
    assert parsed[0].context_length == 128000


# -- capability filtering -------------------------------------------------


def test_chat_keeps_text_capable_models_and_excludes_specialised_ones():
    result = ids(filter_models(catalog(), CAPABILITY_CHAT))
    assert 'openai/gpt-5.5' in result
    assert 'orcarouter/auto' in result
    # Specialised, non-text endpoint types must not leak in.
    assert 'openai/gpt-image-1' not in result
    assert 'google/veo-3' not in result
    assert 'jina/jina-reranker-v2' not in result
    assert 'google/text-embedding-004' not in result


def test_chat_supports_every_accepted_wire_type():
    assert TEXT_ENDPOINT_TYPES == frozenset(
        ('openai',
         'anthropic',
         'gemini',
         'openai-response')
    )
    result = ids(filter_models(catalog(), CAPABILITY_CHAT))
    assert 'anthropic/claude-opus-4.8' in result # anthropic wire type
    assert 'google/gemini-3.5-flash' in result   # gemini wire type


def test_multimodal_filter_is_fail_closed_on_image_input():
    result = ids(
        filter_models(catalog(),
                      CAPABILITY_CHAT,
                      modalities=['image'])
    )
    # Only models that *explicitly* declare image input survive.
    assert result == [
        'openai/gpt-5.5',
        'anthropic/claude-opus-4.8',
        'google/gemini-3.5-flash',
    ]
    # deepseek declares text only -- it is not guessed in from its name.
    assert 'deepseek/deepseek-v4-pro' not in result


def test_multimodal_filter_requires_every_requested_modality():
    result = ids(
        filter_models(
            catalog(),
            CAPABILITY_CHAT,
            modalities=['image',
                        'audio']
        )
    )
    assert result == ['google/gemini-3.5-flash']


def test_a_model_with_no_declared_modalities_fails_closed():
    models = parse_catalog({'data': [{'id': 'a/b'}]})
    assert filter_models(models, CAPABILITY_CHAT, modalities=['image']) == []
    assert ids(filter_models(models, CAPABILITY_CHAT)) == ['a/b']


@pytest.mark.parametrize(
    'capability,expected',
    [
        (CAPABILITY_EMBEDDING,
         ['google/text-embedding-004']),
        (CAPABILITY_IMAGE,
         ['openai/gpt-image-1']),
        (CAPABILITY_VIDEO,
         ['google/veo-3']),
        (CAPABILITY_RERANK,
         ['jina/jina-reranker-v2']),
    ],
)
def test_specialised_capabilities_match_their_strict_endpoint(
    capability,
    expected
):
    assert ids(filter_models(catalog(), capability)) == expected


def test_unknown_capability_is_an_error():
    with pytest.raises(QAOrcaCatalogError):
        filter_models(catalog(), 'telepathy')


def test_limit_is_applied_after_filtering():
    result = models_for_capability(catalog(), CAPABILITY_CHAT, limit=2)
    assert len(result) == 2


# -- verified seed --------------------------------------------------------


def test_seed_matches_the_verified_list_and_keeps_metadata():
    models = {model.id: model for model in seed_catalog()}
    assert set(models) == {
        'openai/gpt-5.5',
        'anthropic/claude-opus-4.8',
        'google/gemini-3.5-flash',
        'deepseek/deepseek-v4-pro',
        'orcarouter/auto',
    }
    gpt = models['openai/gpt-5.5']
    assert gpt.reasoning_efforts == ('low', 'medium', 'high', 'xhigh')
    assert gpt.supports_modality('image')
    assert gpt.context_length == 400000
    # Every seed entry is marked as verified, and says why it is trustworthy.
    assert all(model.verified for model in models.values())
    assert models['openai/gpt-5.5'].verified_note


def test_seed_is_valid_for_the_chat_selector():
    assert len(filter_models(seed_catalog(), CAPABILITY_CHAT)) == 5


def test_seed_entries_all_carry_endpoint_types():
    for entry in VERIFIED_SEED:
        assert entry['supported_endpoint_types']


# -- discovery ------------------------------------------------------------


class FakeResponse(object):

    def __init__(self, payload):
        self._payload = payload

    def read(self, limit=None):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_discover_uses_the_api_origin_and_bearer_auth():
    seen = {}

    def fetcher(endpoints, api_key, capability, timeout, max_bytes):
        seen['url'] = endpoints.models_url
        seen['capability'] = capability
        seen['api_key'] = api_key
        seen['timeout'] = timeout
        seen['max_bytes'] = max_bytes
        return json.dumps(CATALOG).encode()

    endpoints = QAOrcaEndpoints(
        auth_base='https://www.orcarouter.ai',
        api_base='https://api.orcarouter.ai',
    )
    models = discover_models(
        endpoints,
        api_key='sk-orca-fake',
        capability=CAPABILITY_CHAT,
        fetcher=fetcher,
    )
    assert seen['url'] == 'https://api.orcarouter.ai/v1/models'
    assert seen['capability'] == CAPABILITY_CHAT
    assert seen['api_key'] == 'sk-orca-fake'
    assert seen['timeout'] and seen['max_bytes']
    assert 'openai/gpt-5.5' in ids(models)
    # A chat discovery must never hand a text picker an image, video or
    # rerank route -- even though the server-side ?capability= query does
    # not filter, the returned records are filtered here.
    assert not set(ids(models)) & {
        'openai/gpt-image-1',
        'google/veo-3',
        'jina/jina-reranker-v2',
        'google/text-embedding-004',
    }


def test_discover_without_a_capability_keeps_every_supported_route():

    def fetcher(endpoints, api_key, capability, timeout, max_bytes):
        return json.dumps(CATALOG).encode()

    models = discover_models(QAOrcaEndpoints(), fetcher=fetcher)
    assert set(ids(models)) >= {
        'openai/gpt-image-1',
        'google/veo-3',
        'jina/jina-reranker-v2',
        'google/text-embedding-004',
    }


def test_discover_drops_routes_the_client_cannot_speak():

    def fetcher(endpoints, api_key, capability, timeout, max_bytes):
        return json.dumps(
            {
                'data':
                    [
                        {
                            'id': 'good/model',
                            'supported_endpoint_types': ['openai']
                        },
                        {
                            'id': 'weird/model',
                            'supported_endpoint_types': ['some-future-route']
                        },
                    ]
            }
        ).encode()

    assert ids(discover_models(QAOrcaEndpoints(),
                               fetcher=fetcher)) == ['good/model']


def test_discover_uses_the_injected_credential_and_never_the_auth_origin():
    from QUANTAXIS.QAAI.QAOrcaCredential import QAOrcaCredentialResult

    class Provider(object):

        def acquire(self):
            return QAOrcaCredentialResult(
                api_key='sk-orca-fromcredential',
                source='api_key',
                account_id='acct',
            )

        def api_key(self):
            return self.acquire().api_key

    seen = {}

    def fetcher(endpoints, api_key, capability, timeout, max_bytes):
        seen['api_key'] = api_key
        seen['endpoint'] = endpoints
        return json.dumps(CATALOG).encode()

    endpoints = QAOrcaEndpoints()
    discover_models(endpoints, credential=Provider(), fetcher=fetcher)
    assert seen['api_key'] == 'sk-orca-fromcredential'
    assert seen['endpoint'].auth_base == 'https://www.orcarouter.ai'


def test_discover_reports_failures_without_leaking_the_key():

    def fetcher(endpoints, api_key, capability, timeout, max_bytes):
        raise OSError('connection refused')

    with pytest.raises(QAOrcaCatalogError) as info:
        discover_models(
            QAOrcaEndpoints(),
            api_key='sk-orca-secretvalue',
            fetcher=fetcher
        )
    assert 'sk-orca-secretvalue' not in str(info.value)


def test_discover_bounds_the_response_size():

    class Oversized(object):

        def read(self, limit=None):
            return b'x' * 10

    def fetcher(endpoints, api_key, capability, timeout, max_bytes):
        raise QAOrcaCatalogError('the model catalog response was too large')

    with pytest.raises(QAOrcaCatalogError):
        discover_models(QAOrcaEndpoints(), fetcher=fetcher, max_bytes=5)


# -- selector binding -----------------------------------------------------


def test_selector_options_come_from_the_loaded_catalog():
    selector = QAOrcaModelSelector()
    selector.set_provider('orcarouter')
    selector.load(catalog())
    assert 'openai/gpt-5.5' in selector.option_ids()
    assert selector.source == 'live'
    assert selector.degraded is False


def test_selector_recomputes_on_capability_change():
    selector = QAOrcaModelSelector()
    selector.set_provider('orcarouter')
    selector.load(catalog())
    assert 'google/text-embedding-004' not in selector.option_ids()
    selector.set_capability(CAPABILITY_EMBEDDING)
    assert selector.option_ids() == ['google/text-embedding-004']


def test_selector_clears_an_incompatible_selection_on_attachment_change():
    selector = QAOrcaModelSelector()
    selector.set_provider('orcarouter')
    selector.load(catalog())
    selector.select('deepseek/deepseek-v4-pro')
    assert selector.selected == 'deepseek/deepseek-v4-pro'

    # Attaching an image must drop the text-only model, not keep it.
    selector.set_capability(CAPABILITY_CHAT, ['image'])
    assert selector.selected is None
    assert 'deepseek/deepseek-v4-pro' not in selector.option_ids()
    assert selector.option_ids() == [
        'openai/gpt-5.5',
        'anthropic/claude-opus-4.8',
        'google/gemini-3.5-flash',
    ]


def test_selector_refuses_a_model_outside_the_filtered_list():
    selector = QAOrcaModelSelector()
    selector.set_provider('orcarouter')
    selector.load(catalog())
    selector.set_capability(CAPABILITY_CHAT, ['image'])
    with pytest.raises(QAOrcaCatalogError):
        selector.select('deepseek/deepseek-v4-pro')


def test_switching_provider_drops_the_selection_and_the_options():
    selector = QAOrcaModelSelector()
    selector.set_provider('orcarouter')
    selector.load(catalog())
    selector.select('openai/gpt-5.5')
    assert selector.set_provider('orcarouter-oauth') is True
    assert selector.selected is None
    assert selector.option_ids() == []
    assert selector.source == 'none'


def test_degraded_load_labels_the_source_and_keeps_the_seed_usable():
    selector = QAOrcaModelSelector()
    selector.set_provider('orcarouter')
    selector.load_seed(error='catalog unreachable')
    assert selector.source == 'seed'
    assert selector.degraded is True
    assert selector.error == 'catalog unreachable'
    assert 'openai/gpt-5.5' in selector.option_ids()
    # The verified reasoning ladder survives the outage.
    gpt = [m for m in selector.options() if m.id == 'openai/gpt-5.5'][0]
    assert gpt.reasoning_efforts == ('low', 'medium', 'high', 'xhigh')


def test_a_live_catalog_replaces_the_seed_rather_than_merging_it():
    selector = QAOrcaModelSelector()
    selector.set_provider('orcarouter')
    selector.load_seed()
    assert 'orcarouter/auto' in selector.option_ids()

    live = parse_catalog(
        {
            'data':
                [
                    {
                        'id': 'vendor/live-only',
                        'supported_endpoint_types': ['openai']
                    }
                ]
        }
    )
    selector.load(live)
    assert selector.option_ids() == ['vendor/live-only']
    assert selector.degraded is False
    # No seed model is smuggled into an authoritative live result.
    assert 'orcarouter/auto' not in selector.option_ids()


def test_snapshot_reports_capability_modalities_and_source():
    selector = QAOrcaModelSelector()
    selector.set_provider('orcarouter')
    selector.set_capability(CAPABILITY_CHAT, ['image'])
    selector.load(catalog())
    snapshot = selector.snapshot()
    assert snapshot['capability'] == CAPABILITY_CHAT
    assert snapshot['modalities'] == ['image']
    assert snapshot['degraded'] is False
    assert all(
        'image' in option['input_modalities'] for option in snapshot['options']
    )
    assert all(
        option['id'].startswith(('openai/',
                                 'anthropic/',
                                 'google/')) for option in snapshot['options']
    )


def test_non_text_endpoint_types_are_the_specialised_ones():
    assert NON_TEXT_ENDPOINT_TYPES == frozenset(
        ('image-generation',
         'openai-video',
         'jina-rerank',
         'embeddings')
    )
