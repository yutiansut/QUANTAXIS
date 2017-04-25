# -*- coding: utf-8 -*-

import scrapy
import re
import json
from .mongodbQuery import querylist
from wallstreetCN.items import WallstreetcnItem,articlePool
from wallstreetCN.phantomjs import selenium_request
from scrapy.spiders import Spider  
from scrapy.selector import Selector  
import pymongo

class WscSpider(scrapy.Spider):
    name = "wsc"
    def start_requests(self):
     #   models = imput("models:")
     #   if models ==1:
     #       link = 'http://wallstreetcn.com/news'
     #       yield scrapy.Request(link,self.parse_url_list)
     #   elif models ==2:
        for i in range(1,15):
            api ='https://api.wallstreetcn.com/v2/pcarticles?page=%s&limit=100' %i
            yield scrapy.Request(api,self.parse_json_list)
     #   elif models == 3:
    
        #yield scrapy.Request(link, cookies=self.cookies,headers=self.headers,callback=self.parse_url_list) 
       # yield scrapy.Request(link,self.parse_url_list)

    def parse_url_list(self, response):
        sel = scrapy.Selector(response)
        print(sel)
        # first_url_list = sel.xpath('//title[1]//text()').extract()
        # print(first_url_list)
        
        article_xpath = ".//*[@id='news']/ul/li/div/a[1]/@href"
        article_url_list = sel.xpath(article_xpath).extract()

        for article_url in article_url_list:
            print(article_url)
            yield scrapy.Request(article_url,self.parse_article)
            

            #yield self.parse_article(url)

        #content = selenium_request(article_url_list)
        #print(content)
    def parse_article(self, response):
        print ('start crawling articles')
        storageItem=WallstreetcnItem()
        sel = scrapy.Selector(response)
        #title
        article_title_xpath=".//*[@id='main']/div[1]/div[1]/div[1]/text()"
        article_title = sel.xpath(article_title_xpath).extract()[0]
        print(article_title)
        #url
        article_url_xpath=".//*[@id='user-modal']/@data-currenturl"
        article_url = sel.xpath(article_url_xpath).extract()[0]
        print(article_url)
        #content
        article_content_xpath=".//*[@id='main']/div[1]/div[2]//text()"
        article_content_raw = sel.xpath(article_content_xpath).extract()
        article_content_clean = ""
        for i in range(len(article_content_raw)):
            if  article_content_raw[i] == "": continue
            article_content_clean+=article_content_raw[i]
        article_content =article_content_clean.replace(u"\u2022","").replace(u"\xa0","").replace("\n","").replace("\r","")
        print(article_content)

        #tag
        article_tag_xpath = ".//*[@id='article-leftbar']/ul/li[1]/div[2]/div//text()"
        article_tag = sel.xpath(article_tag_xpath).extract()
        print(article_tag)
        #poster
        article_poster_xpath = ".//*[@id='article-rightbar']/div[1]/div[1]/div[1]/a[2]/text()"
        article_poster = sel.xpath(article_poster_xpath).extract()[0]
        print(article_poster)
        article_time_xpath = ".//*[@id='main']/div[1]/div[1]/div[2]/div[1]/text()"
        article_time = sel.xpath(article_time_xpath).extract()[1]
        print(article_time)
        article_viewNum_xpath = ".//*[@id='js-article-viewCount']/text()"
        article_viewNum = sel.xpath(article_viewNum_xpath).extract()[0]
        print(article_viewNum)
        #comments
        article_comments_xpath = ".//*[@id='comments']/div/div/div[6]/div/div[2]/p/text()"
        article_comments = sel.xpath(article_comments_xpath).extract()
        print(article_comments)
        storageItem["title"]=article_title
        storageItem["url"]=article_url
        storageItem["content"]=article_content
        storageItem["tag"]=article_tag
        storageItem["poster"]=article_poster
        storageItem["time"]=article_time
        storageItem["viewNum"]=article_viewNum
        storageItem["comments"]=article_comments
        
        
        return storageItem
        return WallstreetcnItem
            
       # first_url = first_url_list[0]
       # list_content = selenium_request(first_url)
       # soup = BeautifulSoup(list_content,'lxml')
       # h4_list = soup.find_all('h4')
       # if h4_list:
       #     for href in h4_list:
       #         url = 'http://mp.weixin.qq.com%s' % href.get('hrefs')
       #         #print(url)
       #         yield self.parse_item(url)
       # else:
       #     print('yanzheng')
                            #yield scrapy.Request(first_url, callback=self.parse)

    def parse_json_list(self,response):
        
        sel = scrapy.Selector(response)

        data = json.loads(response.body)
        # print data
        news_list = data['posts']
        articleCursor = data['articleCursor']
        for news in news_list:
            item = articlePool()
            news_data = news.get("resource",None)
            news_url = news_data.get("url", None)
            query = querylist()
            count =query.queryMongodbSame('title','news_url',news_url)
            print (count)
            if count == 0:
                item["title"]=news_data.get("title", None)
                item["comment_num"]=news_data.get("commentCount", None)
                item["pic"]=news_data.get("imageUrl", None)
                item["news_no"]=news_data.get("id", None)
                item["title"]=news_data.get("title", None)
                item["news_url"] = news_url
                item["abstract"] = news_data.get("summary", None)
                item["author"] = news_data.get("user", None).get("screenName", None) if news_data.get("user", None) else None
                yield item
                yield articlePool
                countx = query.queryMongodbSame('articles','url',news_url)
                print ('articles url')
                print (news_url)
                print (countx)
                if countx == 0:
                    yield scrapy.Request(news_url,self.parse_article)
                else:
                    print ('articles are already in database')
                    continue
            else:
                countx = query.queryMongodbSame('articles','url',news_url)
                print (countx)
                if countx == 0:
                    print ('artiles will be insert to database')
                    print (news_url)
                    yield scrapy.Request(news_url,self.parse_article)
                else:
                    print ('articles are already in database')
                    continue
                continue
