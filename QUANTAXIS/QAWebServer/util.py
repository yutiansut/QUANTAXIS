import datetime
import json
import sys
from datetime import date

APPLICATION_JSON = 'application/json'
APPLICATION_XML = 'application/xml'
TEXT_XML = 'text/xml'


boolean = str

if sys.version_info > (3,):
    long = int
    unicode = str
    str = bytes


def convert(value, type):
    """ Convert / Cast function """
    if issubclass(type, str) and not (value.upper() in ['FALSE', 'TRUE']):
        return value.decode('utf-8')
    elif issubclass(type, unicode):
        return unicode(value)
    elif issubclass(type, int):
        return int(value)
    elif issubclass(type, long):
        return long(value)
    elif issubclass(type, float):
        return float(value)
    elif issubclass(type, boolean) and (value.upper() in ['FALSE', 'TRUE']):
        if str(value).upper() == 'TRUE':
            return True
        elif str(value).upper() == 'FALSE':
            return False
    else:
        return value


class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
