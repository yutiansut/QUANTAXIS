
Header	解释	示例
Accept-Ranges	表明服务器是否支持指定范围请求及哪种类型的分段请求	Accept-Ranges: bytes
Age	从原始服务器到代理缓存形成的估算时间（以秒计，非负）	Age: 12
Allow	对某网络资源的有效的请求行为，不允许则返回405	Allow: GET, HEAD
Cache-Control	告诉所有的缓存机制是否可以缓存及哪种类型	Cache-Control: no-cache
Content-Encoding	web服务器支持的返回内容压缩编码类型。	Content-Encoding: gzip
Content-Language	响应体的语言	Content-Language: en,zh
Content-Length	响应体的长度	Content-Length: 348
Content-Location	请求资源可替代的备用的另一地址	Content-Location: /index.htm
Content-MD5	返回资源的MD5校验值	Content-MD5: Q2hlY2sgSW50ZWdyaXR5IQ==
Content-Range	在整个返回体中本部分的字节位置	Content-Range: bytes 21010-47021/47022
Content-Type	返回内容的MIME类型	Content-Type: text/html; charset=utf-8
Date	原始服务器消息发出的时间	Date: Tue, 15 Nov 2010 08:12:31 GMT
ETag	请求变量的实体标签的当前值	ETag: “737060cd8c284d8af7ad3082f209582d”
Expires	响应过期的日期和时间	Expires: Thu, 01 Dec 2010 16:00:00 GMT
Last-Modified	请求资源的最后修改时间	Last-Modified: Tue, 15 Nov 2010 12:45:26 GMT
Location	用来重定向接收方到非请求URL的位置来完成请求或标识新的资源	Location: http://www.zcmhi.com/archives/94.html
Pragma	包括实现特定的指令，它可应用到响应链上的任何接收方	Pragma: no-cache
Proxy-Authenticate	它指出认证方案和可应用到代理的该URL上的参数	Proxy-Authenticate: Basic
refresh	应用于重定向或一个新的资源被创造，在5秒之后重定向（由网景提出，被大部分浏览器支持）	



Refresh: 5; url=
http://www.zcmhi.com/archives/94.html
Retry-After	如果实体暂时不可取，通知客户端在指定时间之后再次尝试	Retry-After: 120
Server	web服务器软件名称	Server: Apache/1.3.27 (Unix) (Red-Hat/Linux)
Set-Cookie	设置Http Cookie	Set-Cookie: UserID=JohnDoe; Max-Age=3600; Version=1
Trailer	指出头域在分块传输编码的尾部存在	Trailer: Max-Forwards
Transfer-Encoding	文件传输编码	Transfer-Encoding:chunked
Vary	告诉下游代理是使用缓存响应还是从原始服务器请求	Vary: *
Via	告知代理客户端响应是通过哪里发送的	Via: 1.0 fred, 1.1 nowhere.com (Apache/1.1)
Warning	警告实体可能存在的问题	Warning: 199 Miscellaneous warning
WWW-Authenticate	表明客户端请求实体应该使用的授权方案	WWW-Authenticate: Basic
HTTP Request的Header信息
1、HTTP请求方式
如下表：
方 法
描 述
GET
向Web服务器请求一个文件
POST
向Web服务器发送数据让Web服务器进行处理
PUT
向Web服务器发送数据并存储在Web服务器内部
HEAD
检查一个对象是否存在
DELETE
从Web服务器上删除一个文件
CONNECT
对通道提供支持
TRACE
跟踪到服务器的路径
OPTIONS
查询Web服务器的性能
说明：
主要使用到“GET”和“POST”。
实例：
POST /test/tupian/cm HTTP/1.1
分成三部分：
（1）POST：HTTP请求方式
（2）/test/tupian/cm：请求Web服务器的目录地址（或者指令）
（3）HTTP/1.1: URI（Uniform Resource Identifier，统一资源标识符）及其版本
备注：
         在Ajax中，对应method属性设置。
2、Host
说明：
请求的web服务器域名地址
实例：
例如web请求URL：http://zjm-forum-test10.zjm.baidu.com:8088/test/tupian/cm
Host就为zjm-forum-test10.zjm.baidu.com:8088
3、User-Agent
说明：
HTTP客户端运行的浏览器类型的详细信息。通过该头部信息，web服务器可以判断到当前HTTP请求的客户端浏览器类别。
实例：
    User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11
4、Accept
说明：
指定客户端能够接收的内容类型，内容类型中的先后次序表示客户端接收的先后次序。
实例：
         例如：
Accept:text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
备注：
在Prototyp（1.5）的Ajax代码封装中，将Accept默认设置为“text/javascript, text/html, application/xml, text/xml, */*”。这是因为Ajax默认获取服务器返回的Json数据模式。
在Ajax代码中，可以使用XMLHttpRequest 对象中setRequestHeader函数方法来动态设置这些Header信息。
5、Accept-Language
说明：
    指定HTTP客户端浏览器用来展示返回信息所优先选择的语言。
实例：
Accept-Language: zh-cn,zh;q=0.5
         这里默认为中文。
6、Accept-Encoding
说明：
         指定客户端浏览器可以支持的web服务器返回内容压缩编码类型。表示允许服务器在将输出内容发送到客户端以前进行压缩，以节约带宽。而这里设置的就是客户端浏览器所能够支持的返回压缩格式。
实例：
         Accept-Encoding: gzip,deflate
备注：
其实在百度很多产品线中，apache在给客户端返回页面数据之前，将数据以gzip格式进行压缩。
另外有关deflate压缩介绍：
http://man.chinaunix.net/newsoft/ApacheMenual_CN_2.2new/mod/mod_deflate.html
7、Accept-Charset
说明：
         浏览器可以接受的字符编码集。
实例：
         Accept-Charset: gb2312,utf-8;q=0.7,*;q=0.7
8、Content-Type
说明：
显示此HTTP请求提交的内容类型。一般只有post提交时才需要设置该属性。
实例：
         Content-type: application/x-www-form-urlencoded;charset:UTF-8
有关Content-Type属性值可以如下两种编码类型：
（1）“application/x-www-form-urlencoded”： 表单数据向服务器提交时所采用的编码类型，默认的缺省值就是“application/x-www-form-urlencoded”。 然而，在向服务器发送大量的文本、包含非ASCII字符的文本或二进制数据时这种编码方式效率很低。
（2）“multipart/form-data”： 在文件上载时，所使用的编码类型应当是“multipart/form-data”，它既可以发送文本数据，也支持二进制数据上载。
当提交为单单数据时，可以使用“application/x-www-form-urlencoded”；当提交的是文件时，就需要使用“multipart/form-data”编码类型。
在Content-Type属性当中还是指定提交内容的charset字符编码。一般不进行设置，它只是告诉web服务器post提交的数据采用的何种字符编码。
         一般在开发过程，是由前端工程与后端UI工程师商量好使用什么字符编码格式来post提交的，然后后端ui工程师按照固定的字符编码来解析提交的数据。所以这里设置的charset没有多大作用。
9、Connection
说明：
表示是否需要持久连接。如果web服务器端看到这里的值为“Keep-Alive”，或者看到请求使用的是HTTP 1.1（HTTP 1.1默认进行持久连接），它就可以利用持久连接的优点，当页面包含多个元素时（例如Applet，图片），显著地减少下载所需要的时间。要实现这一点， web服务器需要在返回给客户端HTTP头信息中发送一个Content-Length（返回信息正文的长度）头，最简单的实现方法是：先把内容写入ByteArrayOutputStream，然 后在正式写出内容之前计算它的大小。
实例：
Connection: keep-alive
10、Keep-Alive
说明：
         显示此HTTP连接的Keep-Alive时间。使客户端到服务器端的连接持续有效，当出现对服务器的后继请求时，Keep-Alive功能避免了建立或者重新建立连接。
         以前HTTP请求是一站式连接，从HTTP/1.1协议之后，就有了长连接，即在规定的Keep-Alive时间内，连接是不会断开的。
实例：
Keep-Alive: 300
11、cookie
说明：
         HTTP请求发送时，会把保存在该请求域名下的所有cookie值一起发送给web服务器。
12、Referer
说明：
包含一个URL，用户从该URL代表的页面出发访问当前请求的页面
·服务器端返回HTTP头部信息
1、Content-Length
说明：
         表示web服务器返回消息正文的长度
2、Content-Type:
说明：
         返回数据的类型（例如text/html文本类型）和字符编码格式。
实例：
Content-Type: text/html;charset=utf-8
3、Date
说明：
         显示当前的时间


本文根据RFC2616(HTTP/1.1规范),参考

http://www.w3.org/Protocols/rfc2068/rfc2068

http://www.w3.org/Protocols/rfc2616/rfc2616

http://www.ietf.org/rfc/rfc3229.txt

通常HTTP消息包括客户机向服务器的请求消息和服务器向客户机的响应消息。这两种类型的消息由一个起始行，一个或者多个头域，一个只是头域结束的空行和可 选的消息体组成。HTTP的头域包括通用头，请求头，响应头和实体头四个部分。每个头域由一个域名，冒号（:）和域值三部分组成。域名是大小写无关的，域 值前可以添加任何数量的空格符，头域可以被扩展为多行，在每行开始处，使用至少一个空格或制表符。 

　　通用头域 (通用首部)

通用头域包含请求和响应消息都支持的头域，提供了与报文相关的最基本的信息,通用头域包含 

Connection 允许客户端和服务器指定与请求/响应连接有关的选项

Date 提供日期和时间标志,说明报文是什么时间创建的

MIME-Version 给出发送端使用的MIME版本

Trailer 如果报文采用了分块传输编码(chunked transfer encoding) 方式,就可以用这个首部列出位于报文拖挂(trailer)部分的首部集合

Transfer-Encoding 告知接收端为了保证报文的可靠传输,对报文采用了什么编码方式

Upgrade 给出了发送端可能想要"升级"使用的新版本和协议

Via 显示了报文经过的中间节点(代理,网嘎un)

对通用头域的扩展要求通讯双方都支持此扩 展，如果存在不支持的通用头域，一般将会作为实体头域处理。下面简单介绍几个在UPnP消息中使用的通用头域。 


　　Cache-Control头域 

Cache -Control指定请求和响应遵循的缓存机制。在请求消息或响应消息中设置 Cache-Control并不会修改另一个消息处理过程中的缓存处理过程。请求时的缓存指令包括no-cache、no-store、max-age、 max-stale、min-fresh、only-if-cached，响应消息中的指令包括public、private、no-cache、no- store、no-transform、must-revalidate、proxy-revalidate、max-age。各个消息中的指令含义如 下： 

Public指示响应可被任何缓存区缓存。 

Private指示对于单个用户的整个或部分响应消息，不能被共享缓存处理。这允许服务器仅仅描述当用户的部分响应消息，此响应消息对于其他用户的请求无效。 

no-cache指示请求或响应消息不能缓存 

no-store用于防止重要的信息被无意的发布。在请求消息中发送将使得请求和响应消息都不使用缓存。 

max-age指示客户机可以接收生存期不大于指定时间（以秒为单位）的响应。 

min-fresh指示客户机可以接收响应时间小于当前时间加上指定时间的响应。 

max-stale指示客户机可以接收超出超时期间的响应消息。如果指定max-stale消息的值，那么客户机可以接收超出超时期指定值之内的响应消息。 


　　Date头域 

Date头域表示消息发送的时间，时间的描述格式由rfc822定义。例如，Date:Mon,31Dec200104:25:57GMT。Date描述的时间表示世界标准时，换算成本地时间，需要知道用户所在的时区。 

　　Pragma头域 

Pragma头域用来包含实现特定的指令，最常用的是Pragma:no-cache。在HTTP/1.1协议中，它的含义和Cache- Control:no-cache相同。 

　　请求消息 

请求消息的第一行为下面的格式： 

MethodSPRequest-URISPHTTP-VersionCRLFMethod 表示对于Request-URI完成的方法，这个字段是大小写敏感的，包括OPTIONS、GET、HEAD、POST、PUT、DELETE、 TRACE。方法GET和HEAD应该被所有的通用WEB服务器支持，其他所有方法的实现是可选的。GET方法取回由Request-URI标识的信息。 HEAD方法也是取回由Request-URI标识的信息，只是可以在响应时，不返回消息体。POST方法可以请求服务器接收包含在请求中的实体信息，可 以用于提交表单，向新闻组、BBS、邮件群组和数据库发送消息。 

SP表示空格。Request-URI遵循URI格式，在此字段为星 号（*）时，说明请求并不用于某个特定的资源地址，而是用于服务器本身。HTTP- Version表示支持的HTTP版本，例如为HTTP/1.1。CRLF表示换行回车符。请求头域允许客户端向服务器传递关于请求或者关于客户机的附加 信息。请求头域可能包含下列字段Accept、Accept-Charset、Accept- Encoding、Accept-Language、Authorization、From、Host、If-Modified-Since、If- Match、If-None-Match、If-Range、If-Range、If-Unmodified-Since、Max-Forwards、 Proxy-Authorization、Range、Referer、User-Agent。对请求头域的扩展要求通讯双方都支持，如果存在不支持的请 求头域，一般将会作为实体头域处理。 

　　典型的请求消息： 

GET http://download.google.com/somedata.exe 
Host: download.google.com
Accept:*/* 
Pragma: no-cache 
Cache-Control: no-cache 
Referer: http://download.google.com/ 
User-Agent:Mozilla/4.04[en](Win95;I;Nav) 
Range:bytes=554554- 

上例第一行表示HTTP客户端（可能是浏览器、下载程序）通过GET方法获得指定URL下的文件。棕色的部分表示请求头域的信息，绿色的部分表示通用头部分。 

　　Host头域 

Host头域指定请求资源的Intenet主机和端口号，必须表示请求url的原始服务器或网关的位置。HTTP/1.1请求必须包含主机头域，否则系统会以400状态码返回。 

　　Referer头域 

Referer 头域允许客户端指定请求uri的源资源地址，这可以允许服务器生成回退链表，可用来登陆、优化cache等。他也允许废除的或错误的连接由于维护的目的被 追踪。如果请求的uri没有自己的uri地址，Referer不能被发送。如果指定的是部分uri地址，则此地址应该是一个相对地址。 

　　Range头域 

Range头域可以请求实体的一个或者多个子范围。例如， 
表示头500个字节：bytes=0-499 
表示第二个500字节：bytes=500-999 
表示最后500个字节：bytes=-500 
表示500字节以后的范围：bytes=500- 
第一个和最后一个字节：bytes=0-0,-1 
同时指定几个范围：bytes=500-600,601-999 

但是服务器可以忽略此请求头，如果无条件GET包含Range请求头，响应会以状态码206（PartialContent）返回而不是以200 （OK）。 

　　User-Agent头域 

User-Agent头域的内容包含发出请求的用户信息。 

　　响应消息 

响应消息的第一行为下面的格式： 

HTTP-VersionSPStatus-CodeSPReason-PhraseCRLF 

HTTP -Version表示支持的HTTP版本，例如为HTTP/1.1。Status- Code是一个三个数字的结果代码。Reason-Phrase给Status-Code提供一个简单的文本描述。Status-Code主要用于机器自 动识别，Reason-Phrase主要用于帮助用户理解。Status-Code的第一个数字定义响应的类别，后两个数字没有分类的作用。第一个数字可 能取5个不同的值： 

1xx:信息响应类，表示接收到请求并且继续处理 

2xx:处理成功响应类，表示动作被成功接收、理解和接受 

3xx:重定向响应类，为了完成指定的动作，必须接受进一步处理 

4xx:客户端错误，客户请求包含语法错误或者是不能正确执行 

5xx:服务端错误，服务器不能正确执行一个正确的请求 

响应头域允许服务器传递不能放在状态行的附加信息，这些域主要描述服务器的信息和 Request-URI进一步的信息。响应头域包含Age、Location、Proxy-Authenticate、Public、Retry- After、Server、Vary、Warning、WWW-Authenticate。对响应头域的扩展要求通讯双方都支持，如果存在不支持的响应头 域，一般将会作为实体头域处理。 

典型的响应消息： 

HTTP/1.0200OK 
Date:Mon,31Dec200104:25:57GMT 
Server:Apache/1.3.14(Unix) 
Content-type:text/html 
Last-modified:Tue,17Apr200106:46:28GMT 
Etag:"a030f020ac7c01:1e9f" 
Content-length:39725426 
Content-range:bytes554554-40279979/40279980 

上例第一行表示HTTP服务端响应一个GET方法。棕色的部分表示响应头域的信息，绿色的部分表示通用头部分，红色的部分表示实体头域的信息。 

　　Location响应头 

Location响应头用于重定向接收者到一个新URI地址。 

　　Server响应头 

Server响应头包含处理请求的原始服务器的软件信息。此域能包含多个产品标识和注释，产品标识一般按照重要性排序。 

　　实体 

请求消息和响应消息都可以包含实体信息，实体信息一般由实体头域和实体组成。实体头域包含关于实体的原信息，实体头包括Allow、Content- Base、Content-Encoding、Content-Language、 Content-Length、Content-Location、Content-MD5、Content-Range、Content-Type、 Etag、Expires、Last-Modified、extension-header。extension-header允许客户端定义新的实体 头，但是这些域可能无法未接受方识别。实体可以是一个经过编码的字节流，它的编码方式由Content-Encoding或Content-Type定 义，它的长度由Content-Length或Content-Range定义。 

　　Content-Type实体头 

Content-Type实体头用于向接收方指示实体的介质类型，指定HEAD方法送到接收方的实体介质类型，或GET方法发送的请求介质类型 Content-Range实体头 

Content-Range实体头用于指定整个实体中的一部分的插入位置，他也指示了整个实体的长度。在服务器向客户返回一个部分响应，它必须描述响应覆盖的范围和整个实体长度。一般格式： 

Content-Range:bytes-unitSPfirst-byte-pos-last-byte-pos/entity-legth 

例如，传送头500个字节次字段的形式：Content-Range:bytes0- 499/1234如果一个http消息包含此节（例如，对范围请求的响应或对一系列范围的重叠请求），Content-Range表示传送的范围， Content-Length表示实际传送的字节数。 

　　Last-modified实体头 

应答头	说明
Allow	服务器支持哪些请求方法（如GET、POST等）。
Content-Encoding	文 档的编码（Encode）方法。只有在解码之后才可以得到Content-Type头指定的内容类型。利用gzip压缩文档能够显著地减少HTML文档的 下载时间。Java的GZIPOutputStream可以很方便地进行gzip压缩，但只有Unix上的Netscape和Windows上的IE 4、IE 5才支持它。因此，Servlet应该通过查看Accept-Encoding头（即request.getHeader("Accept- Encoding")）检查浏览器是否支持gzip，为支持gzip的浏览器返回经gzip压缩的HTML页面，为其他浏览器返回普通页面。
Content-Length	表 示内容长度。只有当浏览器使用持久HTTP连接时才需要这个数据。如果你想要利用持久连接的优势，可以把输出文档写入 ByteArrayOutputStram，完成后查看其大小，然后把该值放入Content-Length头，最后通过 byteArrayStream.writeTo(response.getOutputStream()发送内容。
Content-Type	表示后面的文档属于什么MIME类型。Servlet默认为text/plain，但通常需要显式地指定为text/html。由于经常要设置Content-Type，因此HttpServletResponse提供了一个专用的方法setContentTyep。 
Date	当前的GMT时间。你可以用setDateHeader来设置这个头以避免转换时间格式的麻烦。
Expires	应该在什么时候认为文档已经过期，从而不再缓存它？
Last-Modified	文 档的最后改动时间。客户可以通过If-Modified-Since请求头提供一个日期，该请求将被视为一个条件GET，只有改动时间迟于指定时间的文档 才会返回，否则返回一个304（Not Modified）状态。Last-Modified也可用setDateHeader方法来设置。
Location	表示客户应当到哪里去提取文档。Location通常不是直接设置的，而是通过HttpServletResponse的sendRedirect方法，该方法同时设置状态代码为302。
Refresh	表示浏览器应该在多少时间之后刷新文档，以秒计。除了刷新当前文档之外，你还可以通过setHeader("Refresh", "5; URL=http://host/path")让浏览器读取指定的页面。 
注 意这种功能通常是通过设置HTML页面HEAD区的＜META HTTP-EQUIV="Refresh" CONTENT="5;URL=http://host/path"＞实现，这是因为，自动刷新或重定向对于那些不能使用CGI或Servlet的 HTML编写者十分重要。但是，对于Servlet来说，直接设置Refresh头更加方便。 

注意Refresh的意义是“N秒之后 刷新本页面或访问指定页面”，而不是“每隔N秒刷新本页面或访问指定页面”。因此，连续刷新要求每次都发送一个Refresh头，而发送204状态代码则 可以阻止浏览器继续刷新，不管是使用Refresh头还是＜META HTTP-EQUIV="Refresh" ...＞。 

注意Refresh头不属于HTTP 1.1正式规范的一部分，而是一个扩展，但Netscape和IE都支持它。
Server	服务器名字。Servlet一般不设置这个值，而是由Web服务器自己设置。
Set-Cookie	设置和页面关联的Cookie。Servlet不应使用response.setHeader("Set-Cookie", ...)，而是应使用HttpServletResponse提供的专用方法addCookie。参见下文有关Cookie设置的讨论。
WWW-Authenticate	客 户应该在Authorization头中提供什么类型的授权信息？在包含401（Unauthorized）状态行的应答中这个头是必需的。例如， response.setHeader("WWW-Authenticate", "BASIC realm=＼"executives＼"")。 
注意Servlet一般不进行这方面的处理，而是让Web服务器的专门机制来控制受密码保护页面的访问（例如.htaccess）。

在php中header函数

　1. 页面没找到 Not Found
　　
　　header（‘HTTP/1.1 404 Not Found’）；
　　
　　2. 用这个header指令来解决URL重写产生的404 header
　　
　　header（‘HTTP/1.1 200 OK’）；
　　
　　3. 访问受限
　　
　　header（‘HTTP/1.1 403 Forbidden’）；
　　
　　// The page moved permanently should be used for
　　
　　// all redrictions, because search engines know
　　
　　// what's going on and can easily update their urls.
　　
　　4. 页面被永久删除，可以告诉搜索引擎更新它们的urls
　　
　　header（‘HTTP/1.1 301 Moved Permanently’）；
　　
　　5. 服务器错误
　　
　　header（‘HTTP/1.1 500 Internal Server Error’）；
　　
　　6. 重定向到一个新的位置
　　
　　header（‘Location: .example.org/’）；
　　
　　7. 延迟一段时间后重定向
　　
　　header（‘Refresh: 10; url=.example.org/’）；
　　
　　echo 'You will be redirected in 10 seconds';
　　
　　8. 加载要下载的文件：
　　
　　readfile（‘example.zip’）；
　　
　　9. 也可以使用HTML语法来实现延迟
　　
　　header（‘Content-Transfer-Encoding: binary’）；
　　
　　10. 禁止缓存当前文档：
　　
　　header（‘Cache-Control: no-cache, no-store, max-age=0, must-revalidate’）；
　　
　　header（‘Expires: Mon, 26 Jul 2010 05:00:00 GMT’）；
　　
　　header（‘Pragma: no-cache’）；
　　
　　11. 显示登录对话框，可以用来进行HTTP认证
　　
　　header（‘HTTP/1.1 401 Unauthorized’）；
　　
　　header（‘WWW-Authenticate: Basic realm=“Top Secret”’）；
　　
　　echo 'Text that will be displayed if the user hits cancel or ';
　　
　　echo 'enters wrong login data';
　　
　　12. 设置内容类型：
　　
　　header（‘Content-Type: text/html; charset=iso-8859-1’）；
　　
　　header（‘Content-Type: text/html; charset=utf-8’）；
　　
　　header（‘Content-Type: text/plain’）； // plain text file
　　
　　header（‘Content-Type: image/jpeg’）； // JPG picture
　　
　　header（‘Content-Type: application/zip’）； // ZIP file
　　
　　header（‘Content-Type: application/pdf’）； // PDF file
　　
　　header（‘Content-Type: audio/mpeg’）； // Audio MPEG （MP3,…） file
　　
　　header（‘Content-Type: application/x-shockwave-flash’）； // Flash animation
