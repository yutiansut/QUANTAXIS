# coding:utf-8
"""Locale-catalog parity and the provider registry.

Every shipped locale must carry the same key set, so an OrcaRouter label can
never be hardcoded in one locale and silently bypass its catalog in another.
"""

from QUANTAXIS.QAAI.QAOrcaI18n import (
    DEFAULT_LOCALE,
    SUPPORTED_LOCALES,
    TRANSLATIONS,
    available_locales,
    locale_keys,
    translate,
)
from QUANTAXIS.QAAI.QAProvider import (
    ORCA_DEFAULT_MODEL,
    ORCA_OAUTH_PROVIDER_ID,
    ORCA_PROVIDER_ID,
    QAProvider,
    describe_providers,
    get_provider,
    provider_ids,
    reload_providers,
    resolve_provider_endpoints,
)

# -- i18n -----------------------------------------------------------------


def test_every_shipped_locale_is_in_the_catalog():
    assert available_locales() == list(SUPPORTED_LOCALES)
    # The canonical locale is always present as the fallback.
    assert DEFAULT_LOCALE in TRANSLATIONS


def test_locale_key_parity_holds_across_every_catalog():
    reference = set(locale_keys(DEFAULT_LOCALE))
    assert reference
    for locale in SUPPORTED_LOCALES:
        assert set(locale_keys(locale)) == reference, locale


def test_no_locale_ships_a_blank_value():
    for locale, catalog in TRANSLATIONS.items():
        for key, value in catalog.items():
            assert isinstance(value, str) and value.strip(), (locale, key)


def test_english_values_are_the_canonical_fallbacks():
    for key in locale_keys(DEFAULT_LOCALE):
        assert translate(key, DEFAULT_LOCALE) == TRANSLATIONS['en'][key]
        # A locale that forgot a key still resolves to English, never to the
        # raw key.
        assert translate(key, 'xx-not-a-locale') == TRANSLATIONS['en'][key]


def test_an_unknown_key_resolves_to_itself_rather_than_crashing():
    assert translate('panel.does.not.exist') == 'panel.does.not.exist'


def test_both_authentication_labels_are_in_every_locale():
    from QUANTAXIS.QAAI.QAProvider import (
        I18N_ORCA_OAUTH_PROVIDER_NAME,
        I18N_ORCA_PROVIDER_NAME,
    )

    for locale in SUPPORTED_LOCALES:
        assert translate(I18N_ORCA_PROVIDER_NAME, locale)
        assert translate(I18N_ORCA_OAUTH_PROVIDER_NAME, locale)
    # The two labels must be distinguishable in each locale, not the same
    # string twice.
    for locale in SUPPORTED_LOCALES:
        assert translate(I18N_ORCA_PROVIDER_NAME,
                         locale
                        ) != translate(I18N_ORCA_OAUTH_PROVIDER_NAME,
                                       locale)


def test_translation_formatting_never_raises_on_a_missing_placeholder():
    assert translate(
        'panel.title',
        'en',
        nope=1
    ) == TRANSLATIONS['en']['panel.title']


# -- provider registry ----------------------------------------------------


def test_orcarouter_is_a_first_class_named_provider():
    ids = provider_ids()
    assert ids == [ORCA_PROVIDER_ID, ORCA_OAUTH_PROVIDER_ID]
    provider = get_provider(ORCA_PROVIDER_ID)
    assert isinstance(provider, QAProvider)
    assert provider.label == 'OrcaRouter - API'


def test_the_two_choices_share_a_base_url_and_a_namespace():
    api = get_provider(ORCA_PROVIDER_ID)
    oauth = get_provider(ORCA_OAUTH_PROVIDER_ID)
    # One inference adapter, one base URL, one model namespace.
    assert api.base_url == oauth.base_url == 'https://api.orcarouter.ai/v1'
    assert api.default_model == oauth.default_model == ORCA_DEFAULT_MODEL
    assert api.wire_api == oauth.wire_api == 'openai'
    # But their credential acquisition stays explicitly distinct.
    assert api.auth_method == 'api_key'
    assert oauth.auth_method == 'oauth_pkce'
    assert api.oauth is False
    assert oauth.oauth is True
    assert api.label != oauth.label


def test_the_default_model_is_orcarouter_namespaced():
    assert ORCA_DEFAULT_MODEL.startswith('orcarouter/')


def test_registry_exposes_no_secret_material():
    import json

    rendered = json.dumps(describe_providers())
    assert 'sk-orca-' not in rendered
    # Only the *name* of the environment variable appears, never a value.
    assert 'ORCAROUTER_API_KEY' in rendered
    for entry in describe_providers():
        assert not any(
            key in entry
            for key in ('api_key', 'secret', 'token', 'credential')
        )


def test_registry_uses_the_configured_api_origin():
    providers = describe_providers()
    assert all(
        item['base_url'] == 'https://api.orcarouter.ai/v1' for item in providers
    )


def test_registry_rebuilds_against_a_self_hosted_origin():
    endpoints = resolve_provider_endpoints(
        env={'ORCA_BASE_URL': 'https://orca.internal'}
    )
    rebuilt = reload_providers(endpoints)
    try:
        assert all(
            item.base_url == 'https://orca.internal/v1'
            for item in rebuilt.values()
        )
    finally:
        reload_providers()


def test_provider_lookup_by_unknown_id_returns_nothing():
    assert get_provider('some-other-provider') is None


def test_registry_entries_carry_i18n_keys():
    for item in describe_providers():
        assert item['name_key'].startswith('provider.orcarouter')
        assert item['description_key'].startswith('provider.orcarouter')
        assert translate(item['name_key'], 'zh')
