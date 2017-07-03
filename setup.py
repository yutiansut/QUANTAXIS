# coding:utf-8
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


def read(fname):

    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "quantaxis"
"""
名字，一般放你包的名字即可
"""
PACKAGES = ["QUANTAXIS", "QUANTAXIS.QAFetch", "QUANTAXIS.QACmd", "QUANTAXIS.QAMarket",
            "QUANTAXIS.QABacktest", "QUANTAXIS.QASQL", "QUANTAXIS.QATask",  "QUANTAXIS.QASpider",
            "QUANTAXIS.QASU", "QUANTAXIS.QAUtil", "QUANTAXIS.QAARP", "QUANTAXIS.QASignal", "QUANTAXIS.QAIndicator"]
"""
包含的包，可以多个，这是一个列表
"""

DESCRIPTION = "QUANTAXIS:Quantitative Financial Strategy Framework"


LONG_DESCRIPTION = read("README.rst")
"""
参见read方法说明
"""

KEYWORDS = ["quantaxis", "quant", "finance"]
"""
关于当前包的一些关键字，方便PyPI进行分类。
"""

AUTHOR = "yutiansut"

AUTHOR_EMAIL = "yutiansut@qq.com"

URL = "http://www.yutiansut.com"

VERSION = "0.3.9b2.dev26"


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
    install_requires=['pandas>=0.20', 'numpy>=1.12.0', 'tushare==0.7.5',
                      'pymongo>=3.4', 'celery>=4.0.0', 'six>=1.10.0', 'tabulate>=0.7.7',
                      'docopt>=0.6.2', 'zenlog>=1.1'],
    entry_points={
        'console_scripts': [
            'quantaxis=QUANTAXIS:main'
        ]
    },
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
