# QUANTAXIS_SPIDER  (Nodejs version)



## Using superagent for http requests

### SuperAgent
[**superagent**](https://github.com/visionmedia/superagent)
>SuperAgent is a small progressive client-side HTTP request library, and Node.js module with the same API, sporting many high-level HTTP client features
```Nodejs
request
  .post('/api/pet')
  .send({ name: 'Manny', species: 'cat' })
  .set('X-API-Key', 'foobar')
  .set('Accept', 'application/json')
  .end(function(err, res){
    // Calling the end function will send the request
  });
```

### SuperAgent with plugin
```Nodejs
var nocache = require('superagent-no-cache');
var request = require('superagent');
var prefix = require('superagent-prefix')('/static');

request
  .get('/some-url')
  .query({ action: 'edit', city: 'London' }) // query string
  .use(prefix) // Prefixes *only* this request
  .use(nocache) // Prevents caching of *only* this request
  .end(function(err, res){
    // Do something
  });
```

### SuperAgent with asynchronous callback

[**superagent-promise**](https://github.com/lightsofapollo/superagent-promise)
```Nodejs
var Promise = this.Promise || require('promise');
var agent = require('superagent-promise')(require('superagent'), Promise);

// method, url form with `end`
agent('GET', 'http://google.com')
  .end()
  .then(function onResult(res) {
    // do stuff
  }, function onError(err) {
    //err.response has the response from the server
  });

// method, url form with `then`
agent('GET', 'http://google.com')
  .then(function onResult(res) {
    // do stuff
  });


// helper functions: options, head, get, post, put, patch, del
agent.put('http://myxfoo', 'data')
  .end()
  .then(function(res) {
    // do stuff`
  });

// helper functions: options, head, get, post, put, patch, del
agent.put('http://myxfoo', 'data').
  .then(function(res) {
    // do stuff
  });
```
### SuperAgent retry
[**superagent-retry**](https://github.com/segmentio/superagent-retry)
```Nodejs
var superagent = require('superagent');
require('superagent-retry')(superagent);

superagent
  .get('https://segment.io')
  .retry(2) // retry twice before responding
  .end(onresponse);


function onresponse (err, res) {
  console.log(res.status, res.headers);
  console.log(res.body);
}
```
[**axios**]()
[**cheerio**]()
```Nodejs
this is a serverside jquery module

```
[xpath]
[xmldom]