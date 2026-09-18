# coding:utf-8
"""Shared pytest fixtures for the OrcaRouter integration tests.

Every test runs against a throwaway credential file and a throwaway
environment so no real user profile, and no real credential, is ever
touched.  Only fake ``sk-orca-...`` values appear in fixtures.
"""

import os
import sys

import pytest

REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from QUANTAXIS.QAAI.QAOrcaCredential import (  # noqa: E402
    QAOrcaCredentialStore,
)

#: Not a real credential.  Reserved-looking but entirely synthetic.
FAKE_KEY = 'sk-orca-testtesttesttesttesttesttesttest'
FAKE_KEY_TWO = 'sk-orca-secondsecondsecondsecondsecond'
FAKE_CODE = 'fake-auth-code-0000'

#: Environment variables the OrcaRouter layer reads.  Cleared between tests
#: so a developer's real configuration cannot leak into an assertion.
ORCA_ENV_VARS = (
    'ORCAROUTER_API_KEY',
    'ORCA_API_KEY',
    'ORCA_BASE_URL',
    'ORCA_AUTH_BASE_URL',
    'ORCA_API_BASE_URL',
)


@pytest.fixture(autouse=True)
def clean_orca_env(monkeypatch, tmp_path):
    for name in ORCA_ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv(
        'QA_ORCAROUTER_CREDENTIAL_FILE',
        str(tmp_path / 'orcarouter.json')
    )
    monkeypatch.setenv('HOME', str(tmp_path))
    yield


@pytest.fixture
def store(tmp_path):
    return QAOrcaCredentialStore(path=str(tmp_path / 'store.json'))
