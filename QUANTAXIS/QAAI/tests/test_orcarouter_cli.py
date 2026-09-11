# coding:utf-8
"""CLI surface: two discoverable authentication choices on one command."""

import pytest

from QUANTAXIS.QAAI.QAOrcaCli import build_parser, QA_orca_command
from QUANTAXIS.QAAI.QAOrcaCredential import QAOrcaCredentialStore
from QUANTAXIS.QAAI.QAOrcaService import reset_orca_service

KEY_LIKE = 'sk-orca-clifakekey0123456789abcdef'


class Logger(object):

    def __init__(self):
        self.lines = []

    def __call__(self, message, *args):
        self.lines.append(str(message))

    @property
    def text(self):
        return '\n'.join(self.lines)


def run(arg, monkeypatch, tmp_path):
    store = QAOrcaCredentialStore(path=str(tmp_path / 'cli.json'))
    from QUANTAXIS.QAAI import QAOrcaService as module

    service = module.QAOrcaService(store=store)
    reset_orca_service(service)
    log = Logger()
    QA_orca_command(arg, log=log)
    return log, store, service


@pytest.fixture(autouse=True)
def _reset():
    yield
    reset_orca_service(None)


def test_the_command_exposes_both_authentication_flags():
    parser = build_parser()
    options = parser.parse_args(['login', '--key', KEY_LIKE])
    assert options.key == KEY_LIKE
    options = parser.parse_args(['login', '--oauth'])
    assert options.oauth is True


def test_login_with_a_key_stores_it_without_any_oauth(tmp_path, monkeypatch):
    log, store, service = run(
        'login --key {0}'.format(KEY_LIKE), monkeypatch, tmp_path
    )
    assert store.load()['api_key'] == KEY_LIKE
    assert 'stored the OrcaRouter API key' in log.text
    assert 'console/authorized-apps' in log.text
    # No authorization was attempted: no consent URL, no PKCE parameters.
    assert 'code_challenge' not in log.text
    assert '/auth?' not in log.text


def test_login_with_a_bad_key_is_refused(tmp_path, monkeypatch):
    log, store, _ = run('login --key sk-openai-nope', monkeypatch, tmp_path)
    assert store.load() is None
    assert 'sk-orca-' in log.text
    assert 'sk-openai-nope' not in log.text


def test_login_without_a_method_lists_both_choices(tmp_path, monkeypatch):
    log, _, _ = run('login', monkeypatch, tmp_path)
    assert '--key' in log.text
    assert '--oauth' in log.text


def test_login_oauth_prints_the_authorization_url_and_never_the_verifier(
    tmp_path,
    monkeypatch
):
    monkeypatch.setattr('builtins.input', lambda *args: '')
    log, store, service = run(
        'login --oauth --no-browser', monkeypatch, tmp_path
    )
    assert 'https://www.orcarouter.ai/auth?' in log.text
    assert 'code_challenge_method=S256' in log.text
    assert 'callback_url=oob' in log.text
    # The verifier never reaches the terminal.
    verifier = service.pending_attempt['verifier']
    assert verifier not in log.text
    assert store.load() is None


def test_login_oauth_can_be_cancelled_without_storing_anything(
    tmp_path,
    monkeypatch
):

    def boom(*args):
        raise KeyboardInterrupt()

    monkeypatch.setattr('builtins.input', boom)
    log, store, _ = run('login --oauth --no-browser', monkeypatch, tmp_path)
    assert 'cancelled' in log.text
    assert store.load() is None


def test_status_reports_both_methods_and_masks_the_key(tmp_path, monkeypatch):
    run('login --key {0}'.format(KEY_LIKE), monkeypatch, tmp_path)
    log, _, _ = run('status', monkeypatch, tmp_path)
    assert 'orcarouter' in log.text
    assert 'orcarouter-oauth' in log.text
    assert 'https://www.orcarouter.ai' in log.text
    assert 'https://api.orcarouter.ai' in log.text
    assert 'sk-orca-clifakekey0123456789abcdef' not in log.text


def test_logout_removes_the_credential(tmp_path, monkeypatch):
    run('login --key {0}'.format(KEY_LIKE), monkeypatch, tmp_path)
    log, store, _ = run('logout', monkeypatch, tmp_path)
    assert store.load() is None
    assert 'removed' in log.text


def test_logout_without_a_credential_is_not_an_error(tmp_path, monkeypatch):
    log, _, _ = run('logout', monkeypatch, tmp_path)
    assert 'no stored OrcaRouter credential' in log.text


def test_models_lists_live_catalog_entries(tmp_path, monkeypatch):
    from QUANTAXIS.QAAI import QAOrcaService as module

    store = QAOrcaCredentialStore(path=str(tmp_path / 'cli.json'))
    store.save(KEY_LIKE, 'api_key', 'acct')
    service = module.QAOrcaService(store=store)
    monkeypatch.setattr(
        service,
        'models',
        lambda *args, **kwargs: {
            'provider_id':
                'orcarouter',
            'source':
                'live',
            'degraded':
                False,
            'error':
                None,
            'models':
                [
                    {
                        'id': 'openai/gpt-5.5',
                        'name': 'GPT-5.5',
                        'endpoint_types': ['openai'],
                        'input_modalities': ['text', 'image'],
                        'output_modalities': ['text'],
                        'context_length': 400000,
                        'max_completion_tokens': 128000,
                        'reasoning': None,
                        'owned_by': 'OpenAI',
                        'verified': False,
                        'verified_note': None,}
                ],},
    )
    reset_orca_service(service)
    log = Logger()
    QA_orca_command('models --capability chat --modality image', log=log)
    assert 'openai/gpt-5.5' in log.text
    assert 'catalog source: live' in log.text


def test_models_flags_a_degraded_catalog(tmp_path, monkeypatch):
    from QUANTAXIS.QAAI import QAOrcaService as module

    store = QAOrcaCredentialStore(path=str(tmp_path / 'cli.json'))
    service = module.QAOrcaService(store=store)
    monkeypatch.setattr(
        service,
        'models',
        lambda *args, **kwargs: {
            'provider_id':
                'orcarouter',
            'source':
                'seed',
            'degraded':
                True,
            'error':
                'catalog unreachable',
            'models':
                [
                    {
                        'id': 'openai/gpt-5.5',
                        'name': 'GPT-5.5',
                        'endpoint_types': ['openai'],
                        'input_modalities': ['text'],
                        'output_modalities': ['text'],
                        'context_length': 400000,
                        'max_completion_tokens': 128000,
                        'reasoning':
                            {
                                'supported': True, 'efforts':
                                    ['low', 'medium', 'high', 'xhigh']
                            },
                        'owned_by': 'OpenAI',
                        'verified': True,
                        'verified_note': 'verified',}
                ],},
    )
    reset_orca_service(service)
    log = Logger()
    QA_orca_command('models', log=log)
    assert 'DEGRADED' in log.text
    assert 'catalog unreachable' in log.text


def test_chat_refuses_a_model_outside_the_filtered_list(tmp_path, monkeypatch):
    from QUANTAXIS.QAAI import QAOrcaService as module

    store = QAOrcaCredentialStore(path=str(tmp_path / 'cli.json'))
    service = module.QAOrcaService(store=store)
    reset_orca_service(service)
    log = Logger()
    QA_orca_command('chat not/a/real/model hi', log=log)
    assert 'not in the current OrcaRouter model list' in log.text


def test_an_empty_argument_prints_help(tmp_path, monkeypatch):
    log, _, _ = run('', monkeypatch, tmp_path)
    # argparse writes to stdout; the command must not raise.
    assert isinstance(log.text, str)
