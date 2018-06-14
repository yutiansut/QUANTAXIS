import scrapy

import time
import re
from selenium import webdriver
import sys
from selenium.common.exceptions import NoSuchElementException
import sqlite3

def read_east_money_page_zjlx_to_sqllite(stockCode, save_sqlite_full_path_name):

    urls = 'http://data.eastmoney.com/zjlx/{}.html'.format(stockCode)
    pa=re.compile(r'\w+')

    if sys.platform == 'darwin':
        browser = webdriver.Chrome('./selenium_driver/macos/chromedriver')
    elif sys.platform == 'win32':
        browser = webdriver.Chrome('./selenium_driver/windows/chromedriver')
    elif sys.platform == 'linux':
        browser = webdriver.Chrome('./selenium_driver/linux/chromedriver')
        #todo 🛠  linux 下没有测试， linux 下 非gui环境下，用chrome headless driver
        print("🎃")
        print("🎃./selenium_driver/linux/chromedrive   linux 平台上的的      🤖chromedriver 的路径")
        print("🎃./selenium_driver/windows/chromedrive windows 平台上的的    🤖chromedriver 的路径")
        print("🎃   https://npm.taobao.org/mirrors/chromedriver/            🤖chromedriver下载地址")
        print("🎃")
        return

    # 启动chrome
    print("🖼 准备获取数据， 打开chromedrive ，")
    browser.set_page_load_timeout(30)  # throw a TimeoutException when thepage load time is more than 15 seconds
    browser.minimize_window()

    print("🖼 正在请求数据中，请耐心等待 🍺 ⌛ ⌛ ⌛ ⌛ ⌛ ️")
    browser.get(urls)
    time.sleep(1) # Let the page load

    try:
        #result = []
        zjlxtable = browser.find_element_by_id('content_zjlxtable')
        table_elements = zjlxtable.find_element_by_tag_name('table')

        table_header = table_elements.find_elements_by_tag_name('thead')
        # todo 🛠 不知道为何，tbody 标签那不到数据
        table_body   = table_elements.find_elements_by_tag_name('tbody')

        #chrome debug copy xpath
        table_body2  = browser.find_elements_by_xpath('//*[@id="dt_1"]/tbody')

        head1_list = []
        head2_list = []

        if isinstance(table_header,list) == True:
            #print(table_header[0])
            #print(table_header[0].text)

            table_header_row = table_header[0].find_elements_by_tag_name('tr')

            assert(len(table_header_row) == 2)

            table_head_name1 = table_header_row[0].find_elements_by_tag_name('th')
            table_head_name2 = table_header_row[1].find_elements_by_tag_name('th')

            for i in range(len(table_head_name1)):
                head_name = table_head_name1[i].get_attribute("innerHTML")
                head1_list.append(head_name)
                #print(table_head_name1[i].get_attribute("value"))

            for i in range(len(table_head_name2)):
                head_name = table_head_name2[i].get_attribute("innerHTML")
                head2_list.append(head_name)
                #print(table_head_name1[i].get_attribute("value"))
        else:
            raise NoSuchElementException

        row1_list = []
        if isinstance(table_body2,list) == True:

            table_body_row = table_body2[0].find_elements_by_tag_name('tr')
            print("🖼 成功获取 %d 天的资金流向数据️"%(len(table_body_row)))

            for i in range(len(table_body_row)):
                table_body_cell = table_body_row[i].find_elements_by_tag_name('td')
                assert( len(table_body_cell) == 13 )

                v = []
                v.append(table_body_cell[0].text) # 日期
                v.append(table_body_cell[1].text) # 收盘价
                v.append(table_body_cell[2].text) # 涨跌幅
                v.append(table_body_cell[3].text) # 主力净流入_净额(万元)
                v.append(table_body_cell[4].text) # 主力净流入_净占比(%)
                v.append(table_body_cell[5].text) # 超大单净流入_净额(万元)
                v.append(table_body_cell[6].text) # 超大单净流入_净占比(%)
                v.append(table_body_cell[7].text) # 大单净流入_净额(万元)
                v.append(table_body_cell[8].text) # 大单净流入_净占比(%)
                v.append(table_body_cell[9].text) # 中单净流入_净额(万元)
                v.append(table_body_cell[10].text)# 中单净流入_净占比(%)
                v.append(table_body_cell[11].text)# 小单净流入_净额(万元)
                v.append(table_body_cell[12].text)# 小单净流入_净占比(%)

                row1_list.append(v)
        else:
            raise NoSuchElementException

        assert (len(row1_list) != 0 )
        assert (len(head1_list) != 0)
        assert (len(head2_list) != 0)

        browser.close()
        print("🖼 完成获取数据，关闭chromedrive ，")
        #保存sqllite文件
        print("🥕准备写入数据库文件 🎞保存路径",save_sqlite_full_path_name)

        conn = sqlite3.connect(save_sqlite_full_path_name)
        # Create table
        conn.execute('''CREATE TABLE  IF NOT EXISTS  
                     zjlx(code text, date text,
                          close text, chg text, 
                          zljll_je text, zljll_jzb text,
                          cddjll_je text, cddjll_jzb text,
                          ddjll_je text, ddjll_jzb text,
                          zdjll_je text, zdjll_jzb text,
                          xdjll_je text, xdjll_jzb text,
                          primary key(code,date)) 
                     ''')

        for a_row in row1_list:
            # 如果记录重复，则替换
            strSQLExec = 'INSERT OR REPLACE INTO zjlx(code, date, close, chg, \
            zljll_je,  zljll_jzb, \
            cddjll_je, cddjll_jzb, \
            ddjll_je,  ddjll_jzb, \
            zdjll_je,  zdjll_jzb, \
            xdjll_je,  xdjll_jzb) \
            VALUES("%s","%s","%s","%s",\
                   "%s","%s",\
                   "%s","%s",\
                   "%s","%s",\
                   "%s","%s",\
                   "%s","%s")'%\
                        (stockCode,
                          a_row[0],
                          a_row[1],
                          a_row[2],
                          a_row[3],
                          a_row[4],
                          a_row[5],
                          a_row[6],
                          a_row[7],
                          a_row[8],
                          a_row[9],
                          a_row[10],
                          a_row[11],
                          a_row[12]
                          )

            conn.execute(strSQLExec)

            print("🖼  🎞写入数据库 🐌", a_row, " 💹 ")

            conn.commit()

        conn.close()


    except NoSuchElementException:
        print("❌ read_east_money_page_zjlx_to_sqllite 读取网页数据错误 🤮")

    #driver.close()

#todo 🛠  添加金融界
#todo 🛠  添加同花顺




if __name__ == '__main__':

    # code = '300439'
    # read_east_money_page_zjlx_to_sqllite(stockCode= code, save_sqlite_full_path_name="./300439_test.sqlite.db")
    #
    # code = '002344'
    # read_east_money_page_zjlx_to_sqllite(stockCode =code, save_sqlite_full_path_name="./002433_test.sqlite.db")
    pass