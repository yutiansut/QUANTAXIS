'''

Author 604829050@qq.com
https://blog.csdn.net/elecjack/article/details/51532482
'''

import scrapy

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
#from buluo.items import BuluoItem



class MySpiderForEastMoney(scrapy.Spider):
    name = 'zjlx'
    #start_urls = ['http://data.eastmoney.com/zjlx/detail.html']

    def __init__(self):
        super(MySpiderForEastMoney, self).__init__()

        #设定chromedriver 使用相对路径
        self.driver = webdriver.Chrome('./thirdpart/chromedriver')

        #启动chrome
        self.driver.set_page_load_timeout(15)  # throw a TimeoutException when thepage load time is more than 15 seconds
        self.driver.minimize_window()

    def start_requests(self):
        urls = ['http://data.eastmoney.com/zjlx/002433.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'zjlx.html'


    def closed(self):
        #结束chrome
        self.driver.close()
