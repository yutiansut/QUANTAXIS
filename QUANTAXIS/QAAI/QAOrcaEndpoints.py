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
"""OrcaRouter origin resolution.

OrcaRouter serves authentication and inference from two different public
origins:

* authentication (consent screen and code exchange) lives on
  ``https://www.orcarouter.ai``;
* inference and model discovery live on ``https://api.orcarouter.ai/v1``.

The two are never derived from one another.  Replacing a hostname or
appending ``/v1`` to the auth origin yields
``https://api.orcarouter.ai/v1/auth/keys``, which is a 404 -- the single most
common integration mistake.  Authentication paths are therefore pinned as
constants here and are only ever combined with an explicit auth base.

Self-hosted deployments may run both services behind one origin, so a shared
``ORCA_BASE_URL`` fallback is supported next to the explicit
``ORCA_AUTH_BASE_URL`` / ``ORCA_API_BASE_URL`` overrides.  Explicit overrides
always win over the shared value.
"""

import os

from urllib.parse import urlparse

__all__ = [
    'ORCA_PUBLIC_AUTH_BASE',
    'ORCA_PUBLIC_API_BASE',
    'ORCA_AUTHORIZE_PATH',
    'ORCA_EXCHANGE_PATH',
    'ORCA_DEVICE_CODE_PATH',
    'ORCA_DEVICE_TOKEN_PATH',
    'ORCA_MODELS_PATH',
    'ORCA_CHAT_PATH',
    'ORCA_KEY_DASHBOARD_URL',
    'ORCA_LOGO_URL',
    'ORCA_APP_NAME',
    'ORCA_ENV_API_KEY',
    'ORCA_ENV_AUTH_BASE',
    'ORCA_ENV_API_BASE',
    'ORCA_ENV_SHARED_BASE',
    'QAOrcaEndpointError',
    'QAOrcaEndpoints',
    'resolve_endpoints',
]

ORCA_PUBLIC_AUTH_BASE = 'https://www.orcarouter.ai'
ORCA_PUBLIC_API_BASE = 'https://api.orcarouter.ai'

# Fixed paths.  The auth service answers under /api/v1/auth on the auth
# origin; the relay answers under /v1 on the inference origin.
ORCA_AUTHORIZE_PATH = '/auth'
ORCA_EXCHANGE_PATH = '/api/v1/auth/keys'
ORCA_DEVICE_CODE_PATH = '/api/v1/auth/device/code'
ORCA_DEVICE_TOKEN_PATH = '/api/v1/auth/device/token'

ORCA_MODELS_PATH = '/v1/models'
ORCA_CHAT_PATH = '/v1/chat/completions'

ORCA_KEY_DASHBOARD_URL = 'https://www.orcarouter.ai/console/authorized-apps'
ORCA_LOGO_URL = 'https://www.orcarouter.ai/orca-logo-classic.png'

ORCA_APP_NAME = 'QUANTAXIS'

ORCA_ENV_API_KEY = 'ORCAROUTER_API_KEY'
ORCA_ENV_AUTH_BASE = 'ORCA_AUTH_BASE_URL'
ORCA_ENV_API_BASE = 'ORCA_API_BASE_URL'
ORCA_ENV_SHARED_BASE = 'ORCA_BASE_URL'

_LOOPBACK_HOSTS = ('localhost', '127.0.0.1', '::1', '[::1]')


class QAOrcaEndpointError(ValueError):
    """Raised when a configured OrcaRouter origin is not usable."""


def _is_loopback(host):
    return (host or '').lower() in _LOOPBACK_HOSTS


def validate_origin(origin, name='origin'):
    """Validate one OrcaRouter base URL.

    Remote origins must be HTTPS.  Plain HTTP is accepted only for loopback
    development hosts, matching the callback rules of the authorization
    service itself.
    """
    if not origin or not isinstance(origin, str):
        raise QAOrcaEndpointError('{0} is empty'.format(name))

    parsed = urlparse(origin)
    if not parsed.scheme or not parsed.netloc:
        raise QAOrcaEndpointError(
            '{0} must be an absolute URL, got {1!r}'.format(name,
                                                            origin)
        )
    if parsed.username or parsed.password:
        raise QAOrcaEndpointError('{0} must not carry userinfo'.format(name))
    if parsed.query or parsed.fragment:
        raise QAOrcaEndpointError(
            '{0} must not carry a query or fragment'.format(name)
        )
    if parsed.scheme == 'https':
        return origin.rstrip('/')
    if parsed.scheme == 'http':
        if _is_loopback(parsed.hostname):
            return origin.rstrip('/')
        raise QAOrcaEndpointError(
            '{0} uses plain http for non-loopback host {1!r}; '
            'HTTPS is required'.format(name,
                                       parsed.hostname)
        )
    raise QAOrcaEndpointError(
        '{0} uses unsupported scheme {1!r}'.format(name,
                                                   parsed.scheme)
    )


class QAOrcaEndpoints(object):
    """The pair of OrcaRouter origins a client talks to.

    ``auth_base`` is used for the consent screen and for the code exchange;
    ``api_base`` is used for inference and model discovery.
    """

    def __init__(self, auth_base=None, api_base=None):
        self.auth_base = validate_origin(
            auth_base or ORCA_PUBLIC_AUTH_BASE,
            'auth base'
        ).rstrip('/')
        self.api_base = validate_origin(
            api_base or ORCA_PUBLIC_API_BASE,
            'api base'
        ).rstrip('/')

    @property
    def authorize_url(self):
        return '{0}{1}'.format(self.auth_base, ORCA_AUTHORIZE_PATH)

    @property
    def exchange_url(self):
        return '{0}{1}'.format(self.auth_base, ORCA_EXCHANGE_PATH)

    @property
    def device_code_url(self):
        return '{0}{1}'.format(self.auth_base, ORCA_DEVICE_CODE_PATH)

    @property
    def device_token_url(self):
        return '{0}{1}'.format(self.auth_base, ORCA_DEVICE_TOKEN_PATH)

    @property
    def models_url(self):
        return '{0}{1}'.format(self.api_base, ORCA_MODELS_PATH)

    @property
    def chat_url(self):
        return '{0}{1}'.format(self.api_base, ORCA_CHAT_PATH)

    def as_dict(self):
        return {
            'auth_base': self.auth_base,
            'api_base': self.api_base,
            'authorize_url': self.authorize_url,
            'exchange_url': self.exchange_url,
            'models_url': self.models_url,
        }

    def __repr__(self):
        return 'QAOrcaEndpoints(auth_base={0!r}, api_base={1!r})'.format(
            self.auth_base,
            self.api_base
        )


def resolve_endpoints(
    auth_base=None,
    api_base=None,
    shared_base=None,
    env=None
):
    """Resolve the OrcaRouter origin pair from explicit values and environment.

    Precedence, highest first:

    1. ``auth_base`` / ``api_base`` arguments (already-resolved caller values);
    2. ``ORCA_AUTH_BASE_URL`` / ``ORCA_API_BASE_URL``;
    3. ``ORCA_BASE_URL`` -- one origin for both services (self-hosted);
    4. the public defaults.
    """
    env = os.environ if env is None else env
    shared = shared_base or env.get(ORCA_ENV_SHARED_BASE)
    resolved_auth = (
        auth_base or env.get(ORCA_ENV_AUTH_BASE) or shared
        or ORCA_PUBLIC_AUTH_BASE
    )
    resolved_api = (
        api_base or env.get(ORCA_ENV_API_BASE) or shared or ORCA_PUBLIC_API_BASE
    )
    return QAOrcaEndpoints(auth_base=resolved_auth, api_base=resolved_api)
