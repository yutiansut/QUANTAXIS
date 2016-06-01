0.1.5 / 2015-09-17
==================

  * Fix regression when setting empty cookie value
    - Ease the new restriction, which is just basic header-level validation
  * Fix typo in invalid value errors

0.1.4 / 2015-09-17
==================

  * Throw better error for invalid argument to parse
  * Throw on invalid values provided to `serialize`
    - Ensures the resulting string is a valid HTTP header value

0.1.3 / 2015-05-19
==================

  * Reduce the scope of try-catch deopt
  * Remove argument reassignments

0.1.2 / 2014-04-16
==================

  * Remove unnecessary files from npm package

0.1.1 / 2014-02-23
==================

  * Fix bad parse when cookie value contained a comma
  * Fix support for `maxAge` of `0`

0.1.0 / 2013-05-01
==================

  * Add `decode` option
  * Add `encode` option

0.0.6 / 2013-04-08
==================

  * Ignore cookie parts missing `=`

0.0.5 / 2012-10-29
==================

  * Return raw cookie value if value unescape errors

0.0.4 / 2012-06-21
==================

  * Use encode/decodeURIComponent for cookie encoding/decoding
    - Improve server/client interoperability

0.0.3 / 2012-06-06
==================

  * Only escape special characters per the cookie RFC

0.0.2 / 2012-06-01
==================

  * Fix `maxAge` option to not throw error

0.0.1 / 2012-05-28
==================

  * Add more tests

0.0.0 / 2012-05-28
==================

  * Initial release
