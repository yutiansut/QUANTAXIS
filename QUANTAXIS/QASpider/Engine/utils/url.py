

from hashlib import sha1
from urllib.parse import urlparse, urlencode, urlsplit, urlunsplit, quote


def url_fingerprint(url):
    h = sha1()
    h.update(url.encode('utf-8'))
    return h.hexdigest()


def safe_url(url, remove_empty_query=True):
    scheme, netloc, path, query, fragment = urlsplit(url)

    if not query:
        return url.rstrip('/')

    # Sort all the queries
    queries = []
    for q in query.split('&'):
        if '=' not in q:
            return url

        key, value = q.split('=')
        if remove_empty_query and not value:
            continue

        queries.append((key, value))

    queries.sort(key=lambda x: x[0])
    query = urlencode(queries)

    return urlunsplit((scheme, netloc, path, query, fragment)).rstrip('/')


def base_url(url):
    parser = urlparse(url)
    return '://'.join((parser.scheme or 'http', parser.netloc))


def main():
    url = (safe_url('http://fanyi.baidu.com/translate?jlfal=测试&aldtype=16047&ell='))
    print(url)
    print(safe_url('https://movie.douban.com/subject/2353023'))


if __name__ == '__main__':
    main()
