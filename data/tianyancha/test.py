#coding: utf-8
# -*- coding: utf-8 -*-  
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib2

# Zip压缩包解压后exe文件所在的完整的位置
driver = webdriver.PhantomJS(executable_path= "../phantomjs.exe")

def search(keyword):
    # 将手动输入的字符串进行转码
    keyword = keyword.encode("utf-8")
    url_keyword = urllib2.quote(keyword)
    url =  "http://www.tianyancha.com/search?key=%s&checkFrom=searchBox" % url_keyword
    print url
    # print(url)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "lxml")
    # print(soup)
    soup = soup.find_all("span", {"class" : "ng-binding",  "ng-bind-html" : "node.name | trustHtml"})

    for s in soup:
        # 输出文本的内容
        print s.get_text()

if __name__ == "__main__":
    while True:
        x = raw_input("str")
        x = unicode(x, 'gbk')  
        search(x)
