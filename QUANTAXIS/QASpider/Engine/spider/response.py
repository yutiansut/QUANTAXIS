

from urllib.parse import urljoin
from ..utils.url import base_url



class Response(object):
    def __init__(self, url, status, content, request, cookies=None, headers=None):
        self.request = request
        self.url = url
        self.base_url = base_url(url)
        self.cookies = cookies or {}
        self.headers = headers or {}
        self.status = status
        self.content = content or ''
        self.meta = getattr(request, 'meta', None)

    def urljoin(self, url):
        return urljoin(self.base_url, url)

    @property
    def content_as_unicode(self):
        return self.content.decode('utf-8')

    def __repr__(self):
        return '<Response status={} url="{}" content="{}">'.format(self.status, self.url,
                                                                   self.content[:60])
