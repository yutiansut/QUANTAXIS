# coding=utf-8
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

import codecs
import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup
"""
打包的用的setup必须引入，
"""

if sys.version_info.major != 3 or sys.version_info.minor not in [4, 5, 6]:
    print('wrong version, should be 3.4/3.5/3.6 version')
    sys.exit()


def read(fname):

    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "quantaxis_trade"
"""
名字，一般放你包的名字即可
"""
PACKAGES = ["QA_tradex", "QA_status_center",
            "QA_shipane", "QA_Tdxtradeserver", 'util']
"""
包含的包，可以多个，这是一个列表
"""

DESCRIPTION = "QUANTAXIS:Quantitative Financial Strategy Framework"


LONG_DESCRIPTION = read("README.rst")
"""
参见read方法说明
"""

KEYWORDS = ["quantaxis", 'trade', "quant", "finance", "Backtest", 'Framework']
"""
关于当前包的一些关键字，方便PyPI进行分类。
"""

AUTHOR = 'yutiansut'
AUTHOR_EMAIL = "yutiansut@qq.com"

URL = "http://www.yutiansut.com"

VERSION = '0.1.0'


LICENSE = "MIT"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=['pytdx>=1.57', 'pandas>=0.20.3', 'numpy>=1.12.0', 'tushare==0.8.7', 'flask_socketio>=2.9.0 ', 'motor>=1.1',
                      'lxml>=4.0', ' beautifulsoup4', 'flask-socketio', 'flask', 'click>=6.7',  'matplotlib',
                      'pymongo>=3.4', 'celery>=4.0.0', 'six>=1.10.0', 'tabulate>=0.7.7', 'QUANTAXIS>=0.5.21',
                      'zenlog>=1.1', 'delegator.py>=0.0.12', 'flask>=0.12.2', 'pyecharts>=0.2.4', 'protobuf>=3.4.0'],
    entry_points={
    },
    # install_requires=requirements,
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
)

# 把上面的变量填入了一个setup()中即可。
