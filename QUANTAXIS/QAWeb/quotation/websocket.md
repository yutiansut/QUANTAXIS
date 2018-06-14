# WEBSOCKET

<!-- vscode-markdown-toc -->
* 1. [WebSocketHandler.open(*args, **kwargs)[source]](#WebSocketHandler.openargskwargssource)
* 2. [WebSocketHandler.on_message(message)[source]](#WebSocketHandler.on_messagemessagesource)
* 3. [WebSocketHandler.on_close()[source]](#WebSocketHandler.on_closesource)
* 4. [WebSocketHandler.select_subprotocol(subprotocols)[source]](#WebSocketHandler.select_subprotocolsubprotocolssource)
* 5. [WebSocketHandler.on_ping(data)[source]](#WebSocketHandler.on_pingdatasource)
* 6. [WebSocketHandler.write_message(message, binary=False)[source]](#WebSocketHandler.write_messagemessagebinaryFalsesource)
* 7. [WebSocketHandler.close(code=None, reason=None)[source]](#WebSocketHandler.closecodeNonereasonNonesource)
* 8. [WebSocketHandler.check_origin(origin)[source]](#WebSocketHandler.check_originoriginsource)
* 9. [WebSocketHandler.get_compression_options()[source]](#WebSocketHandler.get_compression_optionssource)
* 10. [WebSocketHandler.set_nodelay(value)[source]](#WebSocketHandler.set_nodelayvaluesource)
* 11. [WebSocketHandler.ping(data)[source]](#WebSocketHandler.pingdatasource)
* 12. [WebSocketHandler.on_pong(data)[source]](#WebSocketHandler.on_pongdatasource)
* 13. [tornado.websocket.websocket_connect(url, io_loop=None, callback=None, connect_timeout=None, on_message_callback=None, compression_options=None, ping_interval=None, ping_timeout=None, max_message_size=None)[source]](#tornado.websocket.websocket_connecturlio_loopNonecallbackNoneconnect_timeoutNoneon_message_callbackNonecompression_optionsNoneping_intervalNoneping_timeoutNonemax_message_sizeNonesource)
* 14. [class tornado.websocket.WebSocketClientConnection(io_loop, request, on_message_callback=None, compression_options=None, ping_interval=None, ping_timeout=None, max_message_size=None)[source]](#classtornado.websocket.WebSocketClientConnectionio_looprequeston_message_callbackNonecompression_optionsNoneping_intervalNoneping_timeoutNonemax_message_sizeNonesource)
* 15. [write_message(message, binary=False)[source]](#write_messagemessagebinaryFalsesource)
* 16. [read_message(callback=None)[source]](#read_messagecallbackNonesource)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

Event handlers
##  1. <a name='WebSocketHandler.openargskwargssource'></a>WebSocketHandler.open(*args, **kwargs)[source]
Invoked when a new WebSocket is opened.

The arguments to open are extracted from the tornado.web.URLSpec regular expression, just like the arguments to tornado.web.RequestHandler.get.

##  2. <a name='WebSocketHandler.on_messagemessagesource'></a>WebSocketHandler.on_message(message)[source]
Handle incoming messages on the WebSocket

This method must be overridden.

Changed in version 4.5: on_message can be a coroutine.

##  3. <a name='WebSocketHandler.on_closesource'></a>WebSocketHandler.on_close()[source]
Invoked when the WebSocket is closed.

If the connection was closed cleanly and a status code or reason phrase was supplied, these values will be available as the attributes self.close_code and self.close_reason.

Changed in version 4.0: Added close_code and close_reason attributes.

##  4. <a name='WebSocketHandler.select_subprotocolsubprotocolssource'></a>WebSocketHandler.select_subprotocol(subprotocols)[source]
Invoked when a new WebSocket requests specific subprotocols.

subprotocols is a list of strings identifying the subprotocols proposed by the client. This method may be overridden to return one of those strings to select it, or None to not select a subprotocol. Failure to select a subprotocol does not automatically abort the connection, although clients may close the connection if none of their proposed subprotocols was selected.

##  5. <a name='WebSocketHandler.on_pingdatasource'></a>WebSocketHandler.on_ping(data)[source]
Invoked when the a ping frame is received.


Output
##  6. <a name='WebSocketHandler.write_messagemessagebinaryFalsesource'></a>WebSocketHandler.write_message(message, binary=False)[source]
Sends the given message to the client of this Web Socket.

The message may be either a string or a dict (which will be encoded as json). If the binary argument is false, the message will be sent as utf8; in binary mode any byte string is allowed.

If the connection is already closed, raises WebSocketClosedError.

Changed in version 3.2: WebSocketClosedError was added (previously a closed connection would raise an AttributeError)

Changed in version 4.3: Returns a Future which can be used for flow control.

##  7. <a name='WebSocketHandler.closecodeNonereasonNonesource'></a>WebSocketHandler.close(code=None, reason=None)[source]
Closes this Web Socket.

Once the close handshake is successful the socket will be closed.

code may be a numeric status code, taken from the values defined in RFC 6455 section 7.4.1. reason may be a textual message about why the connection is closing. These values are made available to the client, but are not otherwise interpreted by the websocket protocol.

Changed in version 4.0: Added the code and reason arguments.

Configuration
##  8. <a name='WebSocketHandler.check_originoriginsource'></a>WebSocketHandler.check_origin(origin)[source]
Override to enable support for allowing alternate origins.

The origin argument is the value of the Origin HTTP header, the url responsible for initiating this request. This method is not called for clients that do not send this header; such requests are always allowed (because all browsers that implement WebSockets support this header, and non-browser clients do not have the same cross-site security concerns).

Should return True to accept the request or False to reject it. By default, rejects all requests with an origin on a host other than this one.

This is a security protection against cross site scripting attacks on browsers, since WebSockets are allowed to bypass the usual same-origin policies and don’t use CORS headers.

Warning

This is an important security measure; don’t disable it without understanding the security implications. In particular, if your authentication is cookie-based, you must either restrict the origins allowed by check_origin() or implement your own XSRF-like protection for websocket connections. See these articles for more.

To accept all cross-origin traffic (which was the default prior to Tornado 4.0), simply override this method to always return true:

def check_origin(self, origin):
    return True
To allow connections from any subdomain of your site, you might do something like:

def check_origin(self, origin):
    parsed_origin = urllib.parse.urlparse(origin)
    return parsed_origin.netloc.endswith(".mydomain.com")
New in version 4.0.

##  9. <a name='WebSocketHandler.get_compression_optionssource'></a>WebSocketHandler.get_compression_options()[source]
Override to return compression options for the connection.

If this method returns None (the default), compression will be disabled. If it returns a dict (even an empty one), it will be enabled. The contents of the dict may be used to control the following compression options:

compression_level specifies the compression level.

mem_level specifies the amount of memory used for the internal compression state.

These parameters are documented in details here: https://docs.python.org/3.6/library/zlib.html#zlib.compressobj
New in version 4.1.

Changed in version 4.5: Added compression_level and mem_level.

##  10. <a name='WebSocketHandler.set_nodelayvaluesource'></a>WebSocketHandler.set_nodelay(value)[source]
Set the no-delay flag for this stream.

By default, small messages may be delayed and/or combined to minimize the number of packets sent. This can sometimes cause 200-500ms delays due to the interaction between Nagle’s algorithm and TCP delayed ACKs. To reduce this delay (at the expense of possibly increasing bandwidth usage), call self.set_nodelay(True) once the websocket connection is established.

See BaseIOStream.set_nodelay for additional details.

New in version 3.1.

Other
##  11. <a name='WebSocketHandler.pingdatasource'></a>WebSocketHandler.ping(data)[source]
Send ping frame to the remote end.

##  12. <a name='WebSocketHandler.on_pongdatasource'></a>WebSocketHandler.on_pong(data)[source]
Invoked when the response to a ping frame is received.

exception tornado.websocket.WebSocketClosedError[source]
Raised by operations on a closed connection.

New in version 3.2.

Client-side support
##  13. <a name='tornado.websocket.websocket_connecturlio_loopNonecallbackNoneconnect_timeoutNoneon_message_callbackNonecompression_optionsNoneping_intervalNoneping_timeoutNonemax_message_sizeNonesource'></a>tornado.websocket.websocket_connect(url, io_loop=None, callback=None, connect_timeout=None, on_message_callback=None, compression_options=None, ping_interval=None, ping_timeout=None, max_message_size=None)[source]
Client-side websocket support.

Takes a url and returns a Future whose result is a WebSocketClientConnection.

compression_options is interpreted in the same way as the return value of WebSocketHandler.get_compression_options.

The connection supports two styles of operation. In the coroutine style, the application typically calls read_message in a loop:

conn = yield websocket_connect(url)
while True:
    msg = yield conn.read_message()
    if msg is None: break
    # Do something with msg
In the callback style, pass an on_message_callback to websocket_connect. In both styles, a message of None indicates that the connection has been closed.

Changed in version 3.2: Also accepts HTTPRequest objects in place of urls.

Changed in version 4.1: Added compression_options and on_message_callback. The io_loop argument is deprecated.

Changed in version 4.5: Added the ping_interval, ping_timeout, and max_message_size arguments, which have the same meaning as in WebSocketHandler.

##  14. <a name='classtornado.websocket.WebSocketClientConnectionio_looprequeston_message_callbackNonecompression_optionsNoneping_intervalNoneping_timeoutNonemax_message_sizeNonesource'></a>class tornado.websocket.WebSocketClientConnection(io_loop, request, on_message_callback=None, compression_options=None, ping_interval=None, ping_timeout=None, max_message_size=None)[source]
WebSocket client connection.

This class should not be instantiated directly; use the websocket_connect function instead.

close(code=None, reason=None)[source]
Closes the websocket connection.

code and reason are documented under WebSocketHandler.close.

New in version 3.2.

Changed in version 4.0: Added the code and reason arguments.

##  15. <a name='write_messagemessagebinaryFalsesource'></a>write_message(message, binary=False)[source]
Sends a message to the WebSocket server.

##  16. <a name='read_messagecallbackNonesource'></a>read_message(callback=None)[source]
Reads a message from the WebSocket server.

If on_message_callback was specified at WebSocket initialization, this function will never return messages

Returns a future whose result is the message, or None if the connection is closed. If a callback argument is given it will be called with the future when it is ready.
