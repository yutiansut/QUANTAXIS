# Coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
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
import sys
from zenlog import logging
from QUANTAXIS.QASetting.QALocalize import log_path, setting_path

from QUANTAXIS.QAUtil.QASetting import QA_Setting


"""2019-01-03  升级到warning级别 不然大量别的代码的log会批量输出出来
2020-02-19 默认使用本地log 不再和数据库同步
"""

try:
    _name = '{}{}quantaxis_{}-{}-.log'.format(
        log_path,
        os.sep,
        os.path.basename(sys.argv[0]).split('.py')[0],
        str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    )
except:
    _name = '{}{}quantaxis-{}-.log'.format(
        log_path,
        os.sep,
        str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    )

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s QUANTAXIS>>> %(message)s',
    datefmt='%H:%M:%S',
    filename=_name,
    filemode='w',
)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('QUANTAXIS>> %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

#logging.info('start QUANTAXIS')


def QA_util_log_debug(logs, ui_log=None, ui_progress=None):
    
    """
    explanation:
        QUANTAXIS DEBUG级别日志接口	

    params:
        * logs ->:
            meaning: log信息
            type: null
            optional: [null]
        * ui_log ->:
            meaning:
            type: null
            optional: [null]
        * ui_progress ->:
            meaning:
            type: null
            optional: [null]

    return:
        None
	
    demonstrate:
        Not described
	
    output:
        Not described
    """
    logging.debug(logs)


def QA_util_log_info(logs, ui_log=None, ui_progress=None, ui_progress_int_value=None):

    """
    explanation:
        QUANTAXIS INFO级别日志接口	

    params:
        * logs ->:
            meaning: 日志信息
            type: null
            optional: [null]
        * ui_log ->:
            meaning: 
            type: null
            optional: [null]
        * ui_progress ->:
            meaning: 
            type: null
            optional: [null]
        * ui_progress_int_value ->:
            meaning:
            type: null
            optional: [null]

    return:
        None
	
    demonstrate:
        Not described
	
    output:
        Not described
    """

    """
    QUANTAXIS Log Module
    @yutiansut

    QA_util_log_x is under [QAStandard#0.0.2@602-x] Protocol
    """
    logging.warning(logs)

    # 给GUI使用，更新当前任务到日志和进度
    if ui_log is not None:
        if isinstance(logs, str):
            ui_log.emit(logs)
        if isinstance(logs, list):
            for iStr in logs:
                ui_log.emit(iStr)

    if ui_progress is not None and ui_progress_int_value is not None:
        ui_progress.emit(ui_progress_int_value)


def QA_util_log_expection(logs, ui_log=None, ui_progress=None):
    
    """
    explanation:
        QUANTAXIS ERROR级别日志接口		

    params:
        * logs ->:
            meaning: 日志信息
            type: null
            optional: [null]
        * ui_log ->:
            meaning:
            type: null
            optional: [null]
        * ui_progress ->:
            meaning:
            type: null
            optional: [null]

    return:
        None
	
    demonstrate:
        Not described
	
    output:
        Not described
    """

    logging.exception(logs)
