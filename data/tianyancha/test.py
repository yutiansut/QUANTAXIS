#coding: utf-8
# -*- coding: utf-8 -*-  
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import urllib2

# Zip压缩包解压后exe文件所在的完整的位置

desired_capabilities= DesiredCapabilities.PHANTOMJS.copy()

headers = {'Accept': '*/*',

'Accept-Language': 'en-US,en;q=0.8',

'Cache-Control': 'max-age=0',

'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',#这种修改 UA 也有效

'Connection': 'keep-alive',
'Host':'www.tianyancha.com',
'Tyc-From':'normal',
'Referer':'http://www.tianyancha.com/'

}

for key, value in headers.iteritems():

    desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value

desired_capabilities['phantomjs.page.customHeaders.User-Agent'] ='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
driver = webdriver.PhantomJS(executable_path= "../phantomjs.exe",desired_capabilities=desired_capabilities)


def search(keyword):
    # 将手动输入的字符串进行转码
    keyword = keyword.encode("utf-8")
    url_keyword = urllib2.quote(keyword)
    url =  "http://www.tianyancha.com/search?key=%s&checkFrom=searchBox" % url_keyword
    #print url
    # print(url)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "lxml")
    # print(soup)
    soup = soup.find_all("span", {"class" : "ng-binding",  "ng-bind-html" : "node.name | trustHtml"})

    for s in soup:
        print s.get_text()

if __name__ == "__main__":
    while True:
        x = raw_input("str")
        x = unicode(x, 'gbk')  
        search(x)
