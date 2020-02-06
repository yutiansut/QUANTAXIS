#   Copyright 2017 Dan Krause
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#import SocketServer
import socket
import struct
import json


class IPCError(Exception):
    pass

class UnknownMessageClass(IPCError):
    pass

class InvalidSerialization(IPCError):
    pass

class ConnectionClosed(IPCError):
    pass


def _read_objects(sock):
    header = sock.recv(4)
    if len(header) == 0:
        raise ConnectionClosed()
    size = struct.unpack('!i', header)[0]
    data = sock.recv(size - 4)
    if len(data) == 0:
        raise ConnectionClosed()
    return Message.deserialize(json.loads(data))


def _write_objects(sock, objects):
    data = json.dumps([o.serialize() for o in objects])
    sock.sendall(struct.pack('!i', len(data) + 4))
    sock.sendall(data)

def _recursive_subclasses(cls):
    classmap = {}
    for subcls in cls.__subclasses__():
        classmap[subcls.__name__] = subcls
        classmap.update(_recursive_subclasses(subcls))
    return classmap


class Message(object):
    @classmethod
    def deserialize(cls, objects):
        classmap = _recursive_subclasses(cls)
        serialized = []
        for obj in objects:
            if isinstance(obj, Message):
                serialized.append(obj)
            else:
                try:
                    serialized.append(classmap[obj['class']](*obj['args'], **obj['kwargs']))
                except KeyError as e:
                    raise UnknownMessageClass(e)
                except TypeError as e:
                    raise InvalidSerialization(e)
        return serialized

    def serialize(self):
        args, kwargs = self._get_args()
        return {'class': type(self).__name__, 'args': args, 'kwargs': kwargs}

    def _get_args(self):
        return [], {}

    def __repr__(self):
        r = self.serialize()
        args = ', '.join([repr(arg) for arg in r['args']])
        kwargs = ''.join([', {}={}'.format(k, repr(v)) for k, v in r['kwargs'].items()])
        name = r['class']
        return '{}({}{})'.format(name, args, kwargs)


class Client(object):
    def __init__(self, server_address):
        self.addr = server_address
        if isinstance(self.addr, basestring):
            address_family = socket.AF_UNIX
        else:
            address_family = socket.AF_INET
        self.sock = socket.socket(address_family, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect(self.addr)

    def close(self):
        self.sock.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def send(self, objects):
        _write_objects(self.sock, objects)
        return _read_objects(self.sock)


class Server(SocketServer.ThreadingUnixStreamServer):
    def __init__(self, server_address, callback, bind_and_activate=True):
        if not callable(callback):
            callback = lambda x: []

        class IPCHandler(SocketServer.BaseRequestHandler):
            def handle(self):
                while True:
                    try:
                        results = _read_objects(self.request)
                    except ConnectionClosed as e:
                        return
                    _write_objects(self.request, callback(results))

        if isinstance(server_address, basestring):
            self.address_family = socket.AF_UNIX
        else:
            self.address_family = socket.AF_INET

        SocketServer.TCPServer.__init__(self, server_address, IPCHandler, bind_and_activate)