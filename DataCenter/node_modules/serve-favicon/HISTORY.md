2.3.0 / 2015-06-13
==================

  * Send non-chunked response for `OPTIONS`
  * deps: etag@~1.7.0
    - Always include entity length in ETags for hash length extensions
    - Generate non-Stats ETags using MD5 only (no longer CRC32)
    - Remove base64 padding in ETags to shorten
  * deps: fresh@0.3.0
    - Add weak `ETag` matching support
  * perf: enable strict mode
  * perf: remove argument reassignment
  * perf: remove bitwise operations

2.2.1 / 2015-05-14
==================

  * deps: etag@~1.6.0
   - Improve support for JXcore
   - Support "fake" stats objects in environments without `fs`
  * deps: ms@0.7.1
    - Prevent extraordinarily long inputs

2.2.0 / 2014-12-18
==================

  * Support query string in the URL
  * deps: etag@~1.5.1
    - deps: crc@3.2.1
  * deps: ms@0.7.0
    - Add `milliseconds`
    - Add `msecs`
    - Add `secs`
    - Add `mins`
    - Add `hrs`
    - Add `yrs`

2.1.7 / 2014-11-19
==================

  * Avoid errors from enumerables on `Object.prototype`

2.1.6 / 2014-10-16
==================

  * deps: etag@~1.5.0

2.1.5 / 2014-09-24
==================

  * deps: etag@~1.4.0

2.1.4 / 2014-09-15
==================

  * Fix content headers being sent in 304 response
  * deps: etag@~1.3.1
    - Improve ETag generation speed

2.1.3 / 2014-09-07
==================

  * deps: fresh@0.2.4

2.1.2 / 2014-09-05
==================

  * deps: etag@~1.3.0
    - Improve ETag generation speed

2.1.1 / 2014-08-25
==================

  * Fix `ms` to be listed as a dependency

2.1.0 / 2014-08-24
==================

  * Accept string for `maxAge` (converted by `ms`)
  * Use `etag` to generate `ETag` header

2.0.1 / 2014-06-05
==================

  * Reduce byte size of `ETag` header

2.0.0 / 2014-05-02
==================

  * `path` argument is required; there is no default icon.
  * Accept `Buffer` of icon as first argument.
  * Non-GET and HEAD requests are denied.
  * Send valid max-age value
  * Support conditional requests
  * Support max-age=0
  * Support OPTIONS method
  * Throw if `path` argument is directory.

1.0.2 / 2014-03-16
==================

  * Fixed content of default icon.

1.0.1 / 2014-03-11
==================

  * Fixed path to default icon.

1.0.0 / 2014-02-15
==================

  * Initial release
