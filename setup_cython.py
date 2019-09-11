# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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
import io
import os
import re
import sys
import webbrowser
import platform
import configparser
try:
    from setuptools import setup, Extension
except:
    from distutils.core import setup
"""
"""

if sys.version_info.major != 3 or sys.version_info.minor not in [4, 5, 6, 7, 8]:
    print('wrong version, should be 3.4/3.5/3.6/3.7/3.8 version')
    sys.exit()

with io.open('QUANTAXIS/__init__.py', 'rt', encoding='utf8') as f:
    context = f.read()
    VERSION = re.search(r'__version__ = \'(.*?)\'', context).group(1)
    AUTHOR = re.search(r'__author__ = \'(.*?)\'', context).group(1)


try:
    if sys.platform in ['win32', 'darwin']:
        print(webbrowser.open(
            'https://github.com/QUANTAXIS/QUANTAXIS/releases'))
        print('finish install')
except:
    pass


def read(fname):

    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "quantaxis"
"""

"""
PACKAGES = ["QUANTAXIS", "QUANTAXIS.QAFetch", "QUANTAXIS.QACmd", "QUANTAXIS.QAMarket", 'QUANTAXIS.QASetting', "QUANTAXIS.QACmd",
            "QUANTAXIS.QAApplication", "QUANTAXIS.QAEngine", "QUANTAXIS.QAData", 'QUANTAXIS.QAData.proto', "QUANTAXIS.QAAnalysis", 'QUANTAXIS.QASelector',
            "QUANTAXIS.QASU", "QUANTAXIS.QAUtil", "QUANTAXIS.QAARP", "QUANTAXIS.QAIndicator"]
"""

"""

DESCRIPTION = "QUANTAXIS:Quantitative Financial Strategy Framework"

with open("README_ENG.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

"""

"""

KEYWORDS = ["quantaxis", "quant", "finance", "Backtest", 'Framework']
"""

"""

AUTHOR_EMAIL = "yutiansut@qq.com"

URL = "https://github.com/quantaxis/quantaxis"


LICENSE = "MIT"


ext_modules = [
    Extension('QUANTAXIS.QAARP.QAAccount', ['QUANTAXIS/QAARP/QAAccount.pyx']),
    Extension('QUANTAXIS.QAMARKET.QAOrder', ['QUANTAXIS/QAMARKET/QAOrder.pyx'])]

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
    install_requires=['pandas>=0.23.4', 'numpy>=1.12.0', 'tushare', 'flask_socketio>=2.9.0 ', 'motor>=1.1', 'seaborn>=0.8.1', 'pyconvert>=0.6.3',
                      'lxml>=4.0', ' beautifulsoup4', 'matplotlib', 'requests', 'tornado', 'janus',
                      'demjson>=2.2.4', 'pymongo>=3.7', 'six>=1.10.0', 'tabulate>=0.7.7', 'pytdx>=1.67', 'retrying>=1.3.3',
                      'zenlog>=1.1', 'delegator.py>=0.0.12', 'flask>=0.12.2', 'pyecharts', 'protobuf>=3.4.0'],
    entry_points={
        'console_scripts': [
            'quantaxis=QUANTAXIS.QACmd:QA_cmd',
            'quantaxisq=QUANTAXIS.QAFetch.QATdx_adv:bat',
            'qarun=QUANTAXIS.QACmd.runner:run'
        ]
    },
    ext_modules=ext_modules,
    # install_requires=requirements,
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True
)
