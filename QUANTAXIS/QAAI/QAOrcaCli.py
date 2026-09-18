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
"""CLI surface for the OrcaRouter provider.

The two authentication choices are two discoverable flags of one command,
so a headless/SSH user can paste a key and a user without a key can start a
browser authorization without leaving the terminal.  Both end at the same
credential seam.
"""

import argparse
import shlex
import sys
import webbrowser

from QUANTAXIS.QAAI.QAOrcaAuth import QAOrcaAuthDenied, QAOrcaAuthTimeout
from QUANTAXIS.QAAI.QAOrcaCredential import QAOrcaCredentialError
from QUANTAXIS.QAAI.QAOrcaEndpoints import ORCA_KEY_DASHBOARD_URL
from QUANTAXIS.QAAI.QAOrcaService import get_orca_service
from QUANTAXIS.QAAI.QAModelCatalog import (
    CAPABILITY_CHAT,
    CAPABILITY_EMBEDDING,
    CAPABILITY_IMAGE,
    CAPABILITY_RERANK,
    CAPABILITY_VIDEO,
)

__all__ = ['QA_orca_command', 'build_parser']

CAPABILITY_CHOICES = [
    CAPABILITY_CHAT,
    CAPABILITY_EMBEDDING,
    CAPABILITY_IMAGE,
    CAPABILITY_VIDEO,
    CAPABILITY_RERANK,
]
MODALITY_CHOICES = ['image', 'audio', 'video']


def build_parser():
    parser = argparse.ArgumentParser(
        prog='orcarouter',
        description='OrcaRouter provider for QUANTAXIS',
    )
    sub = parser.add_subparsers(dest='action')

    sub.add_parser('status', help='show provider and credential status')

    login = sub.add_parser('login', help='connect an OrcaRouter account')
    login.add_argument(
        '--key',
        help='paste an existing sk-orca-... API key (API Key choice)',
    )
    login.add_argument(
        '--oauth',
        action='store_true',
        help='sign in with a browser (OAuth 2.0 + PKCE choice)',
    )
    login.add_argument(
        '--no-browser',
        action='store_true',
        help='print the authorization URL instead of opening a browser',
    )
    login.add_argument(
        '--code',
        help='complete a previous --oauth login with the shown code',
    )

    sub.add_parser('logout', help='remove the stored OrcaRouter credential')

    models = sub.add_parser('models', help='list models from the live catalog')
    models.add_argument(
        '--capability',
        default=CAPABILITY_CHAT,
        choices=CAPABILITY_CHOICES
    )
    models.add_argument(
        '--modality',
        action='append',
        choices=MODALITY_CHOICES,
        default=None
    )
    models.add_argument('--limit', type=int, default=25)

    chat = sub.add_parser('chat', help='run one chat completion')
    chat.add_argument('model')
    chat.add_argument('prompt')
    return parser


def QA_orca_command(arg, log=print):
    """Entry point used by ``QUANTAXIS.QACmd.CLI.do_orcarouter``."""
    argv = shlex.split(arg or '')
    parser = build_parser()
    try:
        options = parser.parse_args(argv)
    except SystemExit:
        return None
    if not options.action:
        parser.print_help()
        return None
    handler = {
        'status': _cmd_status,
        'login': _cmd_login,
        'logout': _cmd_logout,
        'models': _cmd_models,
        'chat': _cmd_chat,
    }[options.action]
    try:
        return handler(options, log)
    except QAOrcaCredentialError as error:
        # A rejected key is an expected user mistake, not a crash.
        log('{0}'.format(error))
        return None


def _cmd_status(options, log):
    service = get_orca_service()
    status = service.status()
    log('OrcaRouter providers:')
    for provider in status['providers']:
        log(
            '  {0:<20} {1}  ({2})'.format(
                provider['id'],
                provider['name'],
                provider['base_url']
            )
        )
    log('auth origin : {0}'.format(status['endpoints']['auth_base']))
    log('inference   : {0}'.format(status['endpoints']['api_base']))
    log('key dashboard: {0}'.format(status['key_dashboard_url']))
    credential = status['credential']
    if credential['configured']:
        for account in credential['accounts']:
            log(
                'credential  : {0} via {1} [{2}]{3}'.format(
                    account['api_key_masked'],
                    account['source'],
                    account['scope'],
                    ' NEEDS REAUTH' if account['needs_reauth'] else '',
                )
            )
    else:
        log('credential  : none stored')
    if status['api_key_env_present']:
        log('credential  : ORCAROUTER_API_KEY is set in the environment')
    if not credential['configured'] and not status['api_key_env_present']:
        log('')
        log(
            'Use `orcarouter login --key <sk-orca-...>` for the API Key '
            'choice, or `orcarouter login --oauth` to sign in with a browser.'
        )
    return status


def _cmd_login(options, log):
    service = get_orca_service()
    if options.key:
        account_id = service.login_with_key(options.key)
        log('stored the OrcaRouter API key for account {0}'.format(account_id))
        log('manage or revoke keys at {0}'.format(ORCA_KEY_DASHBOARD_URL))
        return account_id
    if options.oauth:
        return _cmd_login_oauth(service, options, log)
    log('choose an authentication method:')
    log('  orcarouter login --key sk-orca-...   (API Key)')
    log('  orcarouter login --oauth             (OAuth 2.0 + PKCE)')
    return None


def _cmd_login_oauth(service, options, log):
    if options.code:
        attempt = service.pending_attempt
        if not attempt:
            log(
                'no login is in progress; run `orcarouter login --oauth` '
                'first'
            )
            return None
        try:
            result = service.oauth_complete(
                attempt['generation'],
                options.code,
                attempt['verifier'],
                attempt['state'],
            )
        except QAOrcaCredentialError as error:
            log('connect failed: {0}'.format(error))
            return None
        log(
            'connected' if result else 'connect failed: {0}'
            .format(service.oauth_snapshot()['error'])
        )
        return result

    attempt = service.oauth_start()
    if attempt is None:
        log('another login attempt is already current; retry')
        return None
    # The verifier stays in this process until the exchange; only the
    # challenge and the state ever reach the browser.
    log('Open this URL to authorize QUANTAXIS:')
    log('')
    log('  {0}'.format(attempt['authorize_url']))
    log('')
    if not options.no_browser:
        try:
            webbrowser.open(attempt['authorize_url'])
        except Exception:
            pass
    try:
        code = input('Authorization code: ').strip()
    except (EOFError, KeyboardInterrupt):
        service.oauth_cancel(attempt['generation'])
        log('login cancelled')
        return None
    try:
        result = service.oauth_complete(
            attempt['generation'],
            code,
            attempt['verifier'],
            attempt['state'],
        )
    except (QAOrcaAuthDenied,
            QAOrcaAuthTimeout,
            QAOrcaCredentialError) as error:
        log('connect failed: {0}'.format(error))
        return None
    if result:
        log('connected; the key is stored in the QUANTAXIS setting folder')
    else:
        log('connect failed: {0}'.format(service.oauth_snapshot()['error']))
    return result


def _cmd_logout(options, log):
    service = get_orca_service()
    removed = service.logout()
    log(
        'removed the stored OrcaRouter credential'
        if removed else 'no stored OrcaRouter credential to remove'
    )
    return removed


def _cmd_models(options, log):
    service = get_orca_service()
    catalog = service.models(capability=options.capability)
    selector = service.selector(
        capability=options.capability,
        modalities=options.modality
    )
    options_list = selector.options()[:options.limit or None]
    log(
        'catalog source: {0}{1}'.format(
            catalog['source'],
            ' (DEGRADED)' if catalog['degraded'] else ''
        )
    )
    if catalog['error']:
        log('catalog error : {0}'.format(catalog['error']))
    log(
        'capability {0}, modalities {1}: {2} model(s)'.format(
            options.capability,
            options.modality or ['text'],
            len(options_list)
        )
    )
    for model in options_list:
        log('  {0}'.format(model.id))
    if not options_list:
        log(
            '  (no model in the catalog matches this capability; the '
            'selector stays empty rather than offering free text)'
        )
    return options_list


def _cmd_chat(options, log):
    service = get_orca_service()
    selector = service.selector()
    ids = selector.option_ids()
    if options.model not in ids:
        log(
            '{0!r} is not in the current OrcaRouter model list for chat'.format(
                options.model
            )
        )
        log('run `orcarouter models` to list compatible models')
        return None
    try:
        response = service.chat(
            [{
                'role': 'user',
                'content': options.prompt
            }],
            model=options.model,
        )
    except QAOrcaCredentialError as error:
        log('request failed: {0}'.format(error))
        return None
    choices = response.get('choices') or []
    if choices:
        message = choices[0].get('message') or {}
        log(message.get('content') or '')
    else:
        log(str(response)[:2000])
    return response


if __name__ == '__main__': # pragma: no cover - manual use
    sys.exit(0 if QA_orca_command(' '.join(sys.argv[1:])) else 0)
