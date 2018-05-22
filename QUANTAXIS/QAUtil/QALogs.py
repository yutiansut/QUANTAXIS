# Coding:utf-8
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

"""
QUANTAXIS Log Module
@yutiansut

QA_util_log_x is under [QAStandard#0.0.2@602-x] Protocol
QA_util_log_info()
QA_util_log_debug()
QA_util_log_expection()
"""

import configparser
import datetime
import os

from zenlog import logging

from QUANTAXIS.QAUtil.QALocalize import log_path, setting_path

CONFIGFILE_PATH = '{}{}{}'.format(setting_path, os.sep, 'config.ini')


def get_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIGFILE_PATH):
        config.read(CONFIGFILE_PATH)
        try:
            return config.get('LOG', 'path')
        except configparser.NoSectionError:
            config.add_section('LOG')
            config.set('LOG', 'path', log_path)
            return log_path
        except configparser.NoOptionError:
            config.set('LOG', 'path', log_path)
            return log_path
        finally:

            with open(CONFIGFILE_PATH, 'w') as f:
                config.write(f)

    else:
        f = open(CONFIGFILE_PATH, 'w')
        config.add_section('LOG')
        config.set('LOG', 'path', log_path)
        config.write(f)
        f.close()
        return log_path


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s QUANTAXIS>>> %(message)s',
                    datefmt='%H:%M:%S',
                    filename='{}{}quantaxis-{}-.log'.format(get_config(), os.sep, str(datetime.datetime.now().strftime(
                        '%Y-%m-%d-%H-%M-%S'))),
                    filemode='w',
                    )
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('QUANTAXIS>> %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


logging.info('start QUANTAXIS')


def QA_util_log_debug(logs):
    """
    QUANTAXIS Log Module
    @yutiansut

    QA_util_log_x is under [QAStandard#0.0.2@602-x] Protocol
    """
    logging.debug(logs)


def QA_util_log_info(logs):
    """
    QUANTAXIS Log Module
    @yutiansut

    QA_util_log_x is under [QAStandard#0.0.2@602-x] Protocol
    """
    logging.info(logs)


def QA_util_log_expection(logs):
    """
    QUANTAXIS Log Module
    @yutiansut

    QA_util_log_x is under [QAStandard#0.0.2@602-x] Protocol
    """
    logging.exception(logs)
