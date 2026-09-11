# coding:utf-8
"""OrcaRouter credential seam: API-key adapter, store, lifecycle.

The invariant under test is that **both** authentication choices produce the
same credential result shape, so nothing downstream can behave differently
depending on how the key was obtained.
"""

import json
import os
import stat

import pytest

from QUANTAXIS.QAAI.QAOrcaCredential import (
    CREDENTIAL_NEEDS_REAUTH,
    ORCA_SOURCE_API_KEY,
    ORCA_SOURCE_OAUTH_PKCE,
    QAOrcaApiKeyAdapter,
    QAOrcaCredentialError,
    QAOrcaCredentialProvider,
    QAOrcaCredentialResult,
    QAOrcaCredentialStore,
    classify_auth_failure,
    looks_like_orcarouter_key,
    mask_key,
)
from QUANTAXIS.QAAI.tests.conftest import FAKE_KEY

KEY_LIKE = 'sk-orca-abcdefghijklmnopqrstuvwxyz012345'
KEY_LIKE_TWO = 'sk-orca-zyxwvutsrqponmlkjihgfedcba543210'


def test_api_key_adapter_is_a_credential_provider(store):
    adapter = QAOrcaApiKeyAdapter(store=store)
    assert isinstance(adapter, QAOrcaCredentialProvider)
    assert adapter.source == ORCA_SOURCE_API_KEY


def test_save_then_acquire_returns_the_key(store):
    adapter = QAOrcaApiKeyAdapter(store=store)
    account_id = adapter.save(KEY_LIKE)
    assert account_id == 'orcarouter-api-key'
    result = adapter.acquire()
    assert isinstance(result, QAOrcaCredentialResult)
    assert result.api_key == KEY_LIKE
    assert result.source == ORCA_SOURCE_API_KEY


def test_save_rejects_a_key_without_the_orcarouter_prefix(store):
    adapter = QAOrcaApiKeyAdapter(store=store)
    with pytest.raises(QAOrcaCredentialError) as info:
        adapter.save('sk-openai-not-an-orcarouter-key')
    # The message must be actionable and must not echo the rejected value.
    assert 'sk-orca-' in str(info.value)
    assert 'sk-openai-not-an-orcarouter-key' not in str(info.value)


def test_environment_key_takes_precedence_over_the_store(store, monkeypatch):
    adapter = QAOrcaApiKeyAdapter(store=store)
    adapter.save(KEY_LIKE)
    monkeypatch.setenv('ORCAROUTER_API_KEY', FAKE_KEY)
    adapter_env = QAOrcaApiKeyAdapter(store=store)
    assert adapter_env.acquire().api_key == FAKE_KEY


def test_clear_removes_the_stored_key(store):
    adapter = QAOrcaApiKeyAdapter(store=store)
    adapter.save(KEY_LIKE)
    assert adapter.clear() is True
    assert adapter.clear() is False
    assert store.load() is None
    with pytest.raises(QAOrcaCredentialError):
        adapter.acquire()


def test_acquire_without_any_credential_explains_both_choices(store):
    adapter = QAOrcaApiKeyAdapter(store=store)
    with pytest.raises(QAOrcaCredentialError) as info:
        adapter.acquire()
    message = str(info.value)
    assert '--key' in message
    assert 'ORCAROUTER_API_KEY' in message


def test_stored_secret_is_not_world_readable(store, tmp_path):
    adapter = QAOrcaApiKeyAdapter(store=store)
    adapter.save(KEY_LIKE)
    mode = stat.S_IMODE(os.stat(store.path).st_mode)
    assert mode == stat.S_IRUSR | stat.S_IWUSR


def test_corrupt_store_is_treated_as_no_credential_rather_than_crashing(
    tmp_path
):
    path = tmp_path / 'broken.json'
    path.write_text('{ this is not json')
    store = QAOrcaCredentialStore(path=str(path))
    assert store.load() is None
    assert store.status()['configured'] is False
    # And the store still works afterwards.
    store.save(KEY_LIKE, ORCA_SOURCE_API_KEY, 'acct')
    assert store.load()['api_key'] == KEY_LIKE


def test_status_returns_a_mask_and_never_the_key(store):
    adapter = QAOrcaApiKeyAdapter(store=store)
    adapter.save(KEY_LIKE)
    status = store.status()
    assert status['configured'] is True
    rendered = json.dumps(status)
    assert KEY_LIKE not in rendered
    assert status['accounts'][0]['api_key_masked'] == mask_key(KEY_LIKE)


def test_result_repr_never_contains_the_key(store):
    result = QAOrcaCredentialResult(
        api_key=KEY_LIKE,
        source=ORCA_SOURCE_API_KEY,
        account_id='acct',
        scope='api',
    )
    assert KEY_LIKE not in repr(result)
    assert KEY_LIKE not in json.dumps(result.redacted())


def test_mask_reveals_neither_the_middle_nor_the_length():
    long_key = 'sk-orca-' + 'x' * 60
    masked = mask_key(long_key)
    assert long_key not in masked
    assert masked.startswith('sk-orca-')
    assert masked.endswith('xxxx')


@pytest.mark.parametrize(
    'value,expected',
    [
        ('sk-orca-abcdefghijklmnop',
         True),
        ('sk-orca-',
         False),
        ('',
         False),
        (None,
         False),
        ('sk-orca-has a space',
         False),
        ('sk-openai-abcdefghijklmnop',
         False),
    ],
)
def test_format_check_catches_obvious_mistakes_only(value, expected):
    assert looks_like_orcarouter_key(value) is expected


def test_mask_of_none_is_empty():
    assert mask_key(None) == ''


# -- credential lifecycle -------------------------------------------------


def test_401_is_terminal_and_429_is_transient():
    assert classify_auth_failure(401) == CREDENTIAL_NEEDS_REAUTH
    assert classify_auth_failure(429) != CREDENTIAL_NEEDS_REAUTH
    assert classify_auth_failure(500) != CREDENTIAL_NEEDS_REAUTH


def test_save_bumps_the_generation(store):
    first = store.save(KEY_LIKE, ORCA_SOURCE_API_KEY, 'acct')
    second = store.save(KEY_LIKE_TWO, ORCA_SOURCE_OAUTH_PKCE, 'acct')
    assert second['generation'] == first['generation'] + 1


def test_needs_reauth_hides_the_credential_from_normal_resolution(store):
    store.save(KEY_LIKE, ORCA_SOURCE_API_KEY, 'acct')
    assert store.mark_needs_reauth('acct') is True
    assert store.load('acct') is None
    # But the record survives, so nothing is silently destroyed.
    record = store.load('acct', allow_needs_reauth=True)
    assert record['api_key'] == KEY_LIKE
    assert record['needs_reauth'] is True
    assert store.status()['accounts'][0]['needs_reauth'] is True


def test_reauthentication_clears_needs_reauth(store):
    store.save(KEY_LIKE, ORCA_SOURCE_API_KEY, 'acct')
    store.mark_needs_reauth('acct')
    store.save(KEY_LIKE_TWO, ORCA_SOURCE_OAUTH_PKCE, 'acct')
    record = store.load('acct')
    assert record['api_key'] == KEY_LIKE_TWO
    assert record.get('needs_reauth') is False


def test_stale_401_does_not_break_a_reauthorized_credential(store):
    """A late failure from generation N must not flag generation N+1."""
    store.save(KEY_LIKE, ORCA_SOURCE_API_KEY, 'acct')
    stale_generation = store.load('acct')['generation']
    store.save(KEY_LIKE_TWO, ORCA_SOURCE_OAUTH_PKCE, 'acct')
    # The replaced request finally fails with a 401.
    assert store.mark_needs_reauth('acct', generation=stale_generation) is False
    record = store.load('acct')
    assert record is not None
    assert record['api_key'] == KEY_LIKE_TWO
    assert record.get('needs_reauth') is False


def test_stale_401_for_another_account_is_ignored(store):
    store.save(KEY_LIKE, ORCA_SOURCE_API_KEY, 'acct-a')
    store.save(KEY_LIKE_TWO, ORCA_SOURCE_OAUTH_PKCE, 'acct-b')
    assert store.mark_needs_reauth('acct-a', generation=99) is False
    assert store.load('acct-b') is not None


def test_mark_needs_reauth_on_an_unknown_account_is_a_no_op(store):
    store.save(KEY_LIKE, ORCA_SOURCE_API_KEY, 'acct')
    assert store.mark_needs_reauth('nobody') is False


# -- both adapters are interchangeable ------------------------------------


def test_both_adapters_produce_the_same_credential_shape(store):
    """The seam's whole point: downstream cannot tell the sources apart."""
    from QUANTAXIS.QAAI.QAOrcaAuth import QAOrcaPkceAdapter

    key_adapter = QAOrcaApiKeyAdapter(store=store, api_key=KEY_LIKE)
    pkce_adapter = QAOrcaPkceAdapter(store=store)
    pkce_adapter._exchange_and_store = lambda code, verifier, **kw: (
        QAOrcaCredentialResult(
            api_key=KEY_LIKE_TWO,
            source=ORCA_SOURCE_OAUTH_PKCE,
            account_id='orcarouter-oauth-42',
            scope='api',)
    )
    store.save(KEY_LIKE_TWO, ORCA_SOURCE_OAUTH_PKCE, 'orcarouter-oauth-42')

    from_api = key_adapter.acquire()
    from_pkce = pkce_adapter.acquire()

    assert set(from_api.as_dict()) == set(from_pkce.as_dict())
    assert isinstance(from_api, QAOrcaCredentialResult)
    assert isinstance(from_pkce, QAOrcaCredentialResult)
    assert from_api.source != from_pkce.source
    # Only the source label differs; everything a consumer reads is equal
    # in kind, and both yield a plain OrcaRouter key.
    assert from_api.api_key.startswith('sk-orca-')
    assert from_pkce.api_key.startswith('sk-orca-')
