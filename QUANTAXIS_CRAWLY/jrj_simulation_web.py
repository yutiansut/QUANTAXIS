'''

'''
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import demjson
from QUANTAXIS_CRAWLY.run_selenium_alone import *
from QUANTAXIS.QAUtil import (QA_util_getBetweenQuarter,QA_util_add_months,
                              QA_util_today_str,QA_util_datetime_to_strdate)

def get_headers(report_date,headers):
    url = 'http://stock.jrj.com.cn/report/plsj.shtml?ob=2&od=d&_td=&_pid={}'.format(report_date)
    headers.update({"Referer":url})
    options = webdriver.ChromeOptions()
    # 设置中文
    for (key,value) in headers.items():
        options.add_argument('%s="%s"' % (key, value))
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    cookies=driver.get_cookies()
    driver.quit()
    headers.update({"Cookies":cookies})
    return(headers)

def read_financial_report_date(report_date, headers = None, psize= 2000,vname="plsj",page=1):
    if headers == None:
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Cache-Control': 'max-age=0',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                   'Connection': 'keep-alive'
                   }
    args=  {"report_date": report_date, "psize": psize, "vname": vname, 'page': page}

    strUrl1 = "http://app.jrj.com.cn/jds/data_ylj.php?cid=1002&_pd=&_pd2=&_pid={report_date}&ob=2&od=d&page={page}&psize={psize}&vname={vname}".format(**args)
    if page == 1:
        headers = get_headers(report_date,headers)
    options = webdriver.ChromeOptions()
    for (key,value) in headers.items():
        options.add_argument('%s="%s"' % (key, value))

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(strUrl1)
    soup = BeautifulSoup(driver.page_source, "html.parser").body.text
    driver.quit()
    start_str = 'var {vname} = '.format(**args)
    res = demjson.decode(soup.strip(start_str).strip(';'))
    pages = args['page']
    data = pd.DataFrame(res['data'])
    page_num = res['summary']['pages']


    while pages < page_num:
        pages = pages + 1
        res, page_num = read_financial_report_date(report_date,headers,page = pages)
        data = data.append(res)
    data=data.drop_duplicates(keep='first')
    return(data, page_num)

def get_financial_report_date(report_date, headers = None, psize= 2000,vname="plsj",page=1):
    data, page_num = read_financial_report_date(report_date, headers, psize,vname,page)
    data.columns= ['code','name','pre_date','first_date','second_date','third_date','real_date','codes']
    data['report_date']=report_date
    data['crawl_date']=QA_util_today_str()
    return(data[data["real_date"].apply(lambda x: len(x)!=0)])