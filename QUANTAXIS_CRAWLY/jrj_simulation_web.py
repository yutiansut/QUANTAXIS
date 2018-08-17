'''

'''
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def get_financial_report_date(report_date,sleep_time):
    url = 'http://stock.jrj.com.cn/report/plsj.shtml?ob=2&od=d&_td=&_pid={}'.format(report_date)
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    data = pd.DataFrame()
    page = start = 1
    pages = int(soup.find('p', id='ntabFooter').get_text().split(' ')[-2])
    while page <= pages:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        data1 = pd.read_html(str(soup.find_all('table')[2]))[0]
        if page == start:
            data = data1
        else:
            data = data.append(data1, ignore_index=True)
        driver.find_element_by_xpath("//a[contains(text(),'下一页')]").click()
        page = page + 1
        time.sleep(sleep_time) # 睡2秒让网页加载完再去读它的html代码
    driver.quit()

    data.columns= ['No','code','name','pre_date','first_date','sec_date','third_date','final_date','stamp1','stamp2']
    data=data.drop_duplicates(keep='first')
    data['code'] =data['code'].apply(lambda x: str(x).zfill(6))
    data['report_date']=report_date
    return(data)