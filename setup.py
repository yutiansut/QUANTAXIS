#coding:utf-8
import codecs
import os
import sys
 
try:
    from setuptools  import setup
except:
    from  distutils.core import setup
"""
打包的用的setup必须引入，
"""
 
def read(fname):

    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
 
 
 
NAME = "quantaxis"
"""
名字，一般放你包的名字即可
"""
PACKAGES = ["QUANTAXIS", "QUANTAXIS.QAFetch", "QUANTAXIS.QAMarket", "QUANTAXIS.QAStrategy", "QUANTAXIS.QATasks",  "QUANTAXIS.QASpider","QUANTAXIS.QASU","QUANTAXIS.QAUtil"]
"""
包含的包，可以多个，这是一个列表
"""
 
DESCRIPTION = "QUANTAXIS:Quantitative Financial Strategy Framework"

 
LONG_DESCRIPTION = read("README.rst")
"""
参见read方法说明
"""
 
KEYWORDS = ["quantaxis","quant","finance"]
"""
关于当前包的一些关键字，方便PyPI进行分类。
"""
 
AUTHOR = "yutiansut"

AUTHOR_EMAIL = "yutiansut@qq.com"
 
URL = "http://www.yutiansut.com"

VERSION = "0.3.8b0"

 
LICENSE = "MIT"

 
setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires = ['pymongo==3.5.0.dev0','celery==4.0.2','tushare==0.7.4','scrapy==1.3.3','selenium==3.3.1','easyquotation==0.5.1','lxml==3.7.3','pandas==0.19.2','matplotlib==2.0.0'],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)
 
## 把上面的变量填入了一个setup()中即可。