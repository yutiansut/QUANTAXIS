# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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

import inspect
import json
import re
import sys
import xml.dom.minidom

import tornado
import tornado.ioloop
import tornado.web
import tornado.wsgi
from pyconvert.pyconv import (convert2JSON, convert2XML, convertJSON2OBJ,
                              convertXML2OBJ)
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

from QUANTAXIS.QAWeb.util import (APPLICATION_JSON, APPLICATION_XML, TEXT_XML,
                                  convert)

"""
基础类
"""


class QABaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名
        #self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS, DELETE, PUT, PATCH')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header(
            'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        self.set_header('Server', 'QUANTAXISBACKEND')
        #headers.set('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        # self.Content-Type: text/html; charset=utf-8

    def post(self):
        self.write('some post')

    def get(self):
        self.write('some get')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def wirte_error(self, status_code, **kwargs):
        pass

    def initialize(self):
        pass

    def on_finish(self):
        pass


class QAWebSocketHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS, DELETE, PUT, PATCH')
        self.set_header('Access-Control-Max-Age',
                        999999999999999999999999999999999)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Server', 'QUANTAXISBACKEND')

    def open(self):
        self.write_message('x')


class PyRestfulException(Exception):
    """ Class for PyRestful exceptions """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


def config(func, method, **kwparams):
    """ Decorator config function """
    path = None
    produces = None
    consumes = None
    types = None
    manual_response = None
    catch_fire = False

    if len(kwparams):
        path = kwparams['_path']
        if '_produces' in kwparams:
            produces = kwparams['_produces']
        if '_consumes' in kwparams:
            consumes = kwparams['_consumes']
        if '_types' in kwparams:
            types = kwparams['_types']
        if '_manual_response' in kwparams:
            manual_response = kwparams['_manual_response']
        if '_catch_fire' in kwparams:
            catch_fire = kwparams['_catch_fire']

    def operation(*args, **kwargs):
        return func(*args, **kwargs)

    operation.func_name = func.__name__
    operation._func_params = inspect.getargspec(func).args[1:]
    operation._types = types or [str]*len(operation._func_params)
    operation._service_name = re.findall(r'(?<=/)\w+', path)
    operation._service_params = re.findall(r'(?<={)\w+', path)
    operation._method = method
    operation._produces = produces
    operation._consumes = consumes
    operation._query_params = re.findall(r'(?<=<)\w+', path)
    operation._path = path
    operation._manual_response = manual_response
    operation._catch_fire = catch_fire

    if not operation._produces in [APPLICATION_JSON, APPLICATION_XML, TEXT_XML, None]:
        raise PyRestfulException(
            'The media type used do not exist : '+operation.func_name)

    return operation


def get(*params, **kwparams):
    """ Decorator for config a python function like a Rest GET verb	"""
    def method(f):
        return config(f, 'GET', **kwparams)
    return method


def post(*params, **kwparams):
    """ Decorator for config a python function like a Rest POST verb """
    def method(f):
        return config(f, 'POST', **kwparams)
    return method


def put(*params, **kwparams):
    """ Decorator for config a python function like a Rest PUT verb	"""
    def method(f):
        return config(f, 'PUT', **kwparams)
    return method


def patch(*params, **kwparams):
    """ Decorator for config a python function like a Rest PATCH verb """
    def method(f):
        return config(f, 'PATCH', **kwparams)
    return method


def delete(*params, **kwparams):
    """ Decorator for config a python function like a Rest PUT verb	"""
    def method(f):
        return config(f, 'DELETE', **kwparams)
    return method


class QARestHandler(RequestHandler):
    def get(self):
        """ Executes get method """
        self._exe('GET')

    def post(self):
        """ Executes post method """
        self._exe('POST')

    def put(self):
        """ Executes put method """
        self._exe('PUT')

    def patch(self):
        """ Executes patch method """
        self._exe('PATCH')

    def delete(self):
        """ Executes put method """
        self._exe('DELETE')

    def _exe(self, method):
        """ Executes the python function for the Rest Service """
        request_path = self.request.path
        path = request_path.split('/')
        services_and_params = list(filter(lambda x: x != '', path))
        content_type = None
        if 'Content-Type' in self.request.headers.keys():
            content_type = self.request.headers['Content-Type']

        # Get all funcion names configured in the class RestHandler
        functions = list(filter(lambda op: hasattr(getattr(self, op), '_service_name')
                                == True and inspect.ismethod(getattr(self, op)) == True, dir(self)))
        # Get all http methods configured in the class RestHandler
        http_methods = list(map(lambda op: getattr(
            getattr(self, op), '_method'), functions))

        if method not in http_methods:
            raise tornado.web.HTTPError(
                405, 'The service not have %s verb' % method)
        for operation in list(map(lambda op: getattr(self, op), functions)):
            service_name = getattr(operation, '_service_name')
            service_params = getattr(operation, '_service_params')
            # If the _types is not specified, assumes str types for the params
            params_types = getattr(operation, "_types") or [
                str]*len(service_params)
            params_types = params_types + [str] * \
                (len(service_params)-len(params_types))
            produces = getattr(operation, '_produces')
            consumes = getattr(operation, '_consumes')
            services_from_request = list(
                filter(lambda x: x in path, service_name))
            query_params = getattr(operation, '_query_params')
            manual_response = getattr(operation, '_manual_response')
            catch_fire = getattr(operation, '_catch_fire')

            if operation._method == self.request.method and service_name == services_from_request and len(service_params) + len(service_name) == len(services_and_params):
                try:
                    params_values = self._find_params_value_of_url(
                        service_name, request_path) + self._find_params_value_of_arguments(operation)
                    p_values = self._convert_params_values(
                        params_values, params_types)
                    if consumes == None and produces == None:
                        consumes = content_type
                        produces = content_type
                    if consumes == APPLICATION_XML:
                        if params_types[0] in [str]:
                            param_obj = xml.dom.minidom.parseString(
                                self.request.body)
                        else:
                            param_obj = convertXML2OBJ(params_types[0], xml.dom.minidom.parseString(
                                self.request.body).documentElement)
                        p_values.append(param_obj)
                    elif consumes == APPLICATION_JSON:
                        body = self.request.body
                        if sys.version_info > (3,):
                            body = str(self.request.body, 'utf-8')
                        if params_types[0] in [dict, str]:
                            param_obj = json.loads(body)
                        else:
                            param_obj = convertJSON2OBJ(
                                params_types[0], json.loads(body))
                        p_values.append(param_obj)
                    response = operation(*p_values)

                    if response == None:
                        return

                    if produces:
                        self.set_header('Content-Type', produces)

                    if manual_response:
                        return

                    if produces == APPLICATION_JSON and hasattr(response, '__module__'):
                        response = convert2JSON(response)
                    elif produces == APPLICATION_XML and hasattr(response, '__module__') and not isinstance(response, xml.dom.minidom.Document):
                        response = convert2XML(response)

                    if produces == APPLICATION_JSON and isinstance(response, dict):
                        self.write(response)
                        self.finish()
                    elif produces == APPLICATION_JSON and isinstance(response, list):
                        self.write(json.dumps(response))
                        self.finish()
                    elif produces in [APPLICATION_XML, TEXT_XML] and isinstance(response, xml.dom.minidom.Document):
                        self.write(response.toxml())
                        self.finish()
                    else:
                        self.gen_http_error(
                            500, 'Internal Server Error : response is not %s document' % produces)
                        if catch_fire == True:
                            raise PyRestfulException(
                                'Internal Server Error : response is not %s document' % produces)
                except Exception as detail:
                    self.gen_http_error(
                        500, 'Internal Server Error : %s' % detail)
                    if catch_fire == True:
                        raise PyRestfulException(detail)

    def _find_params_value_of_url(self, services, url):
        """ Find the values of path params """
        values_of_query = list()
        i = 0
        url_split = url.split('/')
        values = [item for item in url_split if item not in services and item != '']
        for v in values:
            if v != None:
                values_of_query.append(v)
                i += 1
        return values_of_query

    def _find_params_value_of_arguments(self, operation):
        values = []
        if len(self.request.arguments) > 0:
            a = operation._service_params
            b = operation._func_params
            params = [item for item in b if item not in a]
            for p in params:
                if p in self.request.arguments.keys():
                    v = self.request.arguments[p]
                    values.append(v[0])
                else:
                    values.append(None)
        elif len(self.request.arguments) == 0 and len(operation._query_params) > 0:
            values = [None]*(len(operation._func_params) -
                             len(operation._service_params))
        return values

    def _convert_params_values(self, values_list, params_types):
        """ Converts the values to the specifics types """
        values = list()
        i = 0
        for v in values_list:
            if v != None:
                values.append(convert(v, params_types[i]))
            else:
                values.append(v)
            i += 1
        return values

    def gen_http_error(self, status, msg):
        """ Generates the custom HTTP error """
        self.clear()
        self.set_status(status)
        self.write('<html><body>'+str(msg)+'</body></html>')
        self.finish()

    @classmethod
    def get_services(self):
        """ Generates the resources (uri) to deploy the Rest Services """
        services = []
        for f in dir(self):
            o = getattr(self, f)
            if callable(o) and hasattr(o, '_service_name'):
                services.append(getattr(o, '_service_name'))
        return services

    @classmethod
    def get_paths(self):
        """ Generates the resources from path (uri) to deploy the Rest Services """
        paths = []
        for f in dir(self):
            o = getattr(self, f)
            if callable(o) and hasattr(o, '_path'):
                paths.append(getattr(o, '_path'))
        return paths

    @classmethod
    def get_handlers(self):
        """ Gets a list with (path, handler) """
        svs = []
        paths = self.get_paths()
        for p in paths:
            s = re.sub(r'(?<={)\w+}', '.*', p).replace('{', '')
            o = re.sub(r'(?<=<)\w+', '', s).replace('<',
                                                    '').replace('>', '').replace('&', '').replace('?', '')
            svs.append((o, self))

        return svs


class QARestService(tornado.web.Application):
    """ Class to create Rest services in tornado web server """
    resource = None

    def __init__(self, rest_handlers, resource=None, handlers=None, default_host='', transforms=None, **settings):
        restservices = []
        self.resource = resource
        for r in rest_handlers:
            svs = self._generateRestServices(r)
            restservices += svs
        if handlers != None:
            restservices += handlers
        tornado.web.Application.__init__(
            self, restservices, default_host, transforms, **settings)

    def _generateRestServices(self, rest):
        svs = []
        paths = rest.get_paths()
        for p in paths:
            s = re.sub(r'(?<={)\w+}', '.*', p).replace('{', '')
            o = re.sub(r'(?<=<)\w+', '', s).replace('<',
                                                    '').replace('>', '').replace('&', '').replace('?', '')
            svs.append((o, rest, self.resource))

        return svs


class QAWSGIRestService(tornado.wsgi.WSGIApplication):
    """ Class to create WSGI Rest services in tornado web server """
    resource = None

    def __init__(self, rest_handlers, resource=None, handlers=None, default_host='', **settings):
        restservices = []
        self.resource = resource
        for r in rest_handlers:
            svs = self._generateRestServices(r)
            restservices += svs
        if handlers != None:
            restservices += handlers
        tornado.wsgi.WSGIApplication.__init__(
            self, restservices, default_host, **settings)

    def _generateRestServices(self, rest):
        svs = []
        paths = rest.get_paths()
        for p in paths:
            s = re.sub(r'(?<={)\w+}', '.*', p).replace('{', '')
            o = re.sub(r'(?<=<)\w+', '', s).replace('<',
                                                    '').replace('>', '').replace('&', '').replace('?', '')
            svs.append((o, rest, self.resource))

        return svs
