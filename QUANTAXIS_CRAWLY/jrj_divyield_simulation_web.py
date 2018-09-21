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
    url = 'http://stock.jrj.com.cn/report/szph.shtml?p=1&ob=11&od=d&_ed={}'.format(report_date)
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

def read_stock_divyield(report_date, headers = None, page=1):
    if headers == None:
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Cache-Control': 'max-age=0',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                   'Connection': 'keep-alive'
                   }
    args=  {"report_date": report_date, "unixstamp": int(round(time.time() * 1000))}

    strUrl1 = "http://stock.jrj.com.cn/report/js/sz/{report_date}.js?ts={unixstamp}".format(**args)
    if page == 1:
        headers = get_headers(report_date,headers)
    options = webdriver.ChromeOptions()
    for (key,value) in headers.items():
        options.add_argument('%s="%s"' % (key, value))

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(strUrl1)
    soup = BeautifulSoup(driver.page_source, "html.parser").body.text
    driver.quit()
    start_str = 'var fhps = '.format(**args)
    res = demjson.decode(soup.strip(start_str).strip(';').replace(''',
,
,''',',0,0,').replace(''',
,''',',0,'))
    data = pd.DataFrame(res['data'])
    if data.shape[0] > 0:
        page_num = res['summary']['total']
        data=data.drop_duplicates(keep='first')
        data.columns= ['a_stockcode','a_stocksname','div_info','div_type_code','bonus_shr',
                       'cash_bt','cap_shr','epsp','ps_cr','ps_up','reg_date','dir_dcl_date',
                       'a_stockcode1','ex_divi_date','prg']
        data['report_date']=report_date
        data['crawl_date']=QA_util_today_str()
        return(data, page_num)
    else:
        print("No divyield data for today")
        return(None,None)


def get_stock_divyield(report_date, headers = None, page=1):
    data, page_num = read_stock_divyield(report_date, headers, page)
    if data is None:
        data = pd.DataFrame()
    return(data)