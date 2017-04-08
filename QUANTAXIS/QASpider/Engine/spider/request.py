
from ..utils.url import safe_url




class Request(object):
    def __init__(self, url, method='GET', data=None, cookies=None, headers=None, meta=None, proxy=None, callback=None,
                 dont_filter=False):
        self.url = safe_url(url)

        # Available methods: GET, POST
        self.method = method
        self.data = data
        self.cookies = cookies or {}
        self.headers = headers or {}
        self.meta = meta
        self.proxy = proxy
        self.callback = callback
        self.dont_filter = dont_filter

    def __repr__(self):
        return '<Request url="{url}">'.format(**self.__dict__)


if __name__ == '__main__':
    print(safe_url('http://www.baidu.com/爱情'))