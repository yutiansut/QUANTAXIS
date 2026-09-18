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
"""OrcaRouter locale catalogs.

The repository's user-facing strings are bilingual and there is no existing
i18n catalog to extend, so this module *is* the catalog: every locale ships
the same key set, canonical English values are always available as the
fallback, and ``available_locales``/``translate`` are the only accessors the
GUI uses.  A parity check (``tests/test_orcarouter_i18n.py``) asserts the
key sets are identical, so a label can never be hardcoded in one locale and
silently bypass its catalog in the others.
"""

__all__ = [
    'DEFAULT_LOCALE',
    'SUPPORTED_LOCALES',
    'TRANSLATIONS',
    'available_locales',
    'translate',
    'locale_keys',
]

DEFAULT_LOCALE = 'en'

#: Locales shipped with the OrcaRouter panel.  ``zh`` mirrors the
#: repository's primary documentation language so the new surface is not
#: English-only in a bilingual project.
SUPPORTED_LOCALES = ('en', 'zh')

TRANSLATIONS = {
    'en':
        {
            'provider.orcarouter.name':
                'OrcaRouter - API',
            'provider.orcarouter_oauth.name':
                'OrcaRouter - Auth',
            'provider.orcarouter.description':
                ('OrcaRouter is an OpenAI-compatible AI gateway.'),
            'panel.title':
                'OrcaRouter',
            'panel.subtitle':
                'Connect with an API key or with your account',
            'panel.auth.api_key.label':
                'API Key',
            'panel.auth.api_key.hint':
                'Paste an sk-orca-... key',
            'panel.auth.api_key.placeholder':
                'sk-orca-...',
            'panel.auth.api_key.submit':
                'Save key',
            'panel.auth.pkce.label':
                'Connect with OrcaRouter',
            'panel.auth.pkce.hint':
                'Opens a browser authorization (OAuth 2.0 + PKCE)',
            'panel.auth.pkce.start':
                'Start authorization',
            'panel.auth.pkce.code_label':
                'Authorization code',
            'panel.auth.pkce.code_placeholder':
                'Paste the code shown in the browser',
            'panel.auth.pkce.finish':
                'Finish connection',
            'panel.auth.pkce.cancel':
                'Cancel',
            'panel.auth.pkce.opening':
                'Waiting for authorization...',
            'panel.auth.method.legend':
                'Authentication method',
            'panel.status.connected':
                'Connected',
            'panel.status.disconnected':
                'Not connected',
            'panel.status.needs_reauth':
                'Reconnect required',
            'panel.status.source':
                'Credential source',
            'panel.status.scope':
                'Granted scope',
            'panel.status.env':
                'ORCAROUTER_API_KEY is set',
            'panel.action.logout':
                'Disconnect',
            'panel.action.refresh':
                'Refresh models',
            'panel.action.dashboard':
                'Manage keys',
            'panel.model.label':
                'Model',
            'panel.model.placeholder':
                'Select a model',
            'panel.model.loading':
                'Loading models...',
            'panel.model.empty':
                'No model matches this capability',
            'panel.model.degraded':
                'Showing the verified fallback catalog',
            'panel.model.error':
                'Could not load the model catalog',
            'panel.model.source.live':
                'Live catalog',
            'panel.model.source.seed':
                'Verified fallback',
            'panel.attachment.add_image':
                'Attach an image',
            'panel.attachment.image':
                'Image attached',
            'panel.attachment.remove':
                'Remove attachment',
            'panel.modality.requires_image':
                ('Only models that accept image input are listed'),
            'panel.chat.prompt':
                'Prompt',
            'panel.chat.send':
                'Send',
            'panel.error.state_mismatch':
                'The authorization response did not match',
            'panel.error.denied':
                'Authorization was denied',
            'panel.error.timeout':
                'Authorization timed out; start again',
            'panel.error.exchange':
                'The authorization code could not be exchanged',
        },
    'zh':
        {
            'provider.orcarouter.name': 'OrcaRouter - 密钥',
            'provider.orcarouter_oauth.name': 'OrcaRouter - 授权登录',
            'provider.orcarouter.description':
                ('OrcaRouter 是兼容 OpenAI 协议的人工智能网关。'),
            'panel.title': 'OrcaRouter',
            'panel.subtitle': '使用 API 密钥或账号授权接入',
            'panel.auth.api_key.label': 'API 密钥',
            'panel.auth.api_key.hint': '粘贴 sk-orca-... 密钥',
            'panel.auth.api_key.placeholder': 'sk-orca-...',
            'panel.auth.api_key.submit': '保存密钥',
            'panel.auth.pkce.label': '使用 OrcaRouter 账号登录',
            'panel.auth.pkce.hint': '打开浏览器授权 (OAuth 2.0 + PKCE)',
            'panel.auth.pkce.start': '开始授权',
            'panel.auth.pkce.code_label': '授权码',
            'panel.auth.pkce.code_placeholder': '粘贴浏览器中显示的授权码',
            'panel.auth.pkce.finish': '完成连接',
            'panel.auth.pkce.cancel': '取消',
            'panel.auth.pkce.opening': '等待授权中...',
            'panel.auth.method.legend': '认证方式',
            'panel.status.connected': '已连接',
            'panel.status.disconnected': '未连接',
            'panel.status.needs_reauth': '需要重新授权',
            'panel.status.source': '凭据来源',
            'panel.status.scope': '已授权范围',
            'panel.status.env': '环境变量 ORCAROUTER_API_KEY 已设置',
            'panel.action.logout': '断开连接',
            'panel.action.refresh': '刷新模型',
            'panel.action.dashboard': '管理密钥',
            'panel.model.label': '模型',
            'panel.model.placeholder': '请选择模型',
            'panel.model.loading': '正在加载模型...',
            'panel.model.empty': '该能力下没有匹配的模型',
            'panel.model.degraded': '当前显示已验证的备用目录',
            'panel.model.error': '无法加载模型目录',
            'panel.model.source.live': '实时目录',
            'panel.model.source.seed': '已验证备用目录',
            'panel.attachment.add_image': '添加图片附件',
            'panel.attachment.image': '已添加图片',
            'panel.attachment.remove': '移除附件',
            'panel.modality.requires_image': '仅列出支持图片输入的模型',
            'panel.chat.prompt': '提问',
            'panel.chat.send': '发送',
            'panel.error.state_mismatch': '授权响应校验失败',
            'panel.error.denied': '授权被拒绝',
            'panel.error.timeout': '授权超时，请重新开始',
            'panel.error.exchange': '授权码兑换失败',
        },
}


def available_locales():
    return list(TRANSLATIONS)


def locale_keys(locale):
    return sorted(TRANSLATIONS.get(locale, {}).keys())


def translate(key, locale=DEFAULT_LOCALE, **kwargs):
    """Resolve ``key`` through the requested catalog, then English."""
    catalog = TRANSLATIONS.get(locale) or {}
    value = catalog.get(key)
    if value is None:
        value = TRANSLATIONS[DEFAULT_LOCALE].get(key, key)
    if kwargs:
        try:
            return value.format(**kwargs)
        except (KeyError, IndexError):
            return value
    return value
