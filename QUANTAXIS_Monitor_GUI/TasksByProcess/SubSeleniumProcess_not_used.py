import socket
import re
from selenium import webdriver
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

import time

import os
from QUANTAXIS.QAUtil import (DATABASE)

'''
https://www.cnblogs.com/taurusfy/p/8464602.html
'''

#🛠todo fix 已到 QA_SU 目录下面
def open_chrome_driver():

    currentFile  = __file__
    print(currentFile);

    dirName = os.path.dirname(currentFile)
    dirName1 = os.path.dirname(dirName)
    dirName2 = os.path.dirname(dirName1)
    print(dirName2)


    if sys.platform == 'darwin':
        browser = webdriver.Chrome(dirName2 + '/QUANTAXIS_WEBDRIVER/macos/chromedriver')
    elif sys.platform == 'win32':
        browser = webdriver.Chrome(dirName2 + '/QUANTAXIS_WEBDRIVER/windows/chromedriver')
    elif sys.platform == 'linux':
        browser = webdriver.Chrome(dirName2 + './QUANTAXIS_WEBDRIVER/linux/chromedriver')
        # todo 🛠  linux 下没有测试， linux 下 非gui环境下，用chrome headless driver
        print("🎃")
        print("🎃./selenium_driver/linux/chromedrive   linux 平台上的的      🤖chromedriver 的路径")
        print("🎃./selenium_driver/windows/chromedrive windows 平台上的的    🤖chromedriver 的路径")
        print("🎃   https://npm.taobao.org/mirrors/chromedriver/            🤖chromedriver下载地址")
        print("🎃")
    return browser

def close_chrome_dirver(browser):
    browser.quit()


def crawly_code(code=None, conn = None, browser = None):

    #关闭先前的页面
    ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
    ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
    ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
    ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
    ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()


    urls = 'http://data.eastmoney.com/zjlx/{}.html'.format(code)
    pa = re.compile(r'\w+')

    # 启动chrome
    strMsg0 = "logging@开启代理游览器获取数据{}".format(code)
    bytes_content = strMsg0.encode()
    bytes_content = bytes_content.zfill(512)
    # 🛠todo fix 固定512 个byte 很傻
    assert(len(bytes_content) == 512)
    conn.sendall(bytes_content)



    browser.set_page_load_timeout(30)  # throw a TimeoutException when thepage load time is more than 15 seconds
    browser.minimize_window()

    bytes_content = b"progress@100"
    bytes_content =bytes_content.zfill(512)
    # 🛠todo fix 固定512 个byte 很傻
    assert(len(bytes_content) == 512)
    conn.sendall(bytes_content)

    browser.get(urls)

    strMsg0= "logging@页面成功打开{}OK, 解析网页中".format(code)
    bytes_content = strMsg0.encode()
    bytes_content = bytes_content.zfill(512)
    # 🛠todo fix 固定512 个byte 很傻
    assert (len(bytes_content) == 512)
    conn.sendall(bytes_content)

    try:
        # result = []
        zjlxtable = browser.find_element_by_id('content_zjlxtable')
        table_elements = zjlxtable.find_element_by_tag_name('table')

        table_header = table_elements.find_elements_by_tag_name('thead')
        # todo 🛠 不知道为何，tbody 标签那不到数据
        table_body = table_elements.find_elements_by_tag_name('tbody')

        # chrome debug copy xpath
        table_body2 = browser.find_elements_by_xpath('//*[@id="dt_1"]/tbody')

        head1_list = []
        head2_list = []

        if isinstance(table_header, list) == True:
            # print(table_header[0])
            # print(table_header[0].text)

            table_header_row = table_header[0].find_elements_by_tag_name('tr')

            assert (len(table_header_row) == 2)

            table_head_name1 = table_header_row[0].find_elements_by_tag_name('th')
            table_head_name2 = table_header_row[1].find_elements_by_tag_name('th')

            for i in range(len(table_head_name1)):
                head_name = table_head_name1[i].get_attribute("innerHTML")
                head1_list.append(head_name)
                # print(table_head_name1[i].get_attribute("value"))

            for i in range(len(table_head_name2)):
                head_name = table_head_name2[i].get_attribute("innerHTML")
                head2_list.append(head_name)
                # print(table_head_name1[i].get_attribute("value"))
        else:
            # raise NoSuchElementException
            print("error !!!!!!!!")

        row1_list = []
        if isinstance(table_body2, list) == True:

            table_body_row = table_body2[0].find_elements_by_tag_name('tr')
            print("🖼 成功获取 %d 天的资金流向数据️" % (len(table_body_row)))

            t0 = time.clock()

            row_length = len(table_body_row)
            for i in range(row_length):
                table_body_cell = table_body_row[i].find_elements_by_tag_name('td')
                assert (len(table_body_cell) == 13)

                dict_row = {}
                dict_row['stock_code'] = code

                dict_row['date'] = table_body_cell[0].text
                dict_row['zljll_je_wy'] = table_body_cell[1].text
                dict_row['zljll_jzb_bfb'] = table_body_cell[2].text
                dict_row['cddjll_je_wy'] = table_body_cell[3].text
                dict_row['cddjll_je_jzb'] = table_body_cell[4].text
                dict_row['ddjll_je_wy'] = table_body_cell[5].text
                dict_row['ddjll_je_jzb'] = table_body_cell[6].text
                dict_row['zdjll_je_wy'] = table_body_cell[7].text
                dict_row['zdjll_je_jzb'] = table_body_cell[8].text
                dict_row['xdjll_je_wy'] = table_body_cell[9].text
                dict_row['xdjll_je_jzb'] = table_body_cell[10].text
                dict_row['close_price'] = table_body_cell[11].text
                dict_row['change_price'] = table_body_cell[12].text

                row1_list.append(dict_row)

                # todo 🛠  循环获取网页速度非常慢， 进一步学习 selenium 的操作， 批量一次获取数据
                iPct = round((i / row_length) * 100.0)
                #s1 = "\r读取数据%d%%[%s%s]" % (iPct, "🐢" * iPct, " " * (100 - iPct))
                #sys.stdout.write(s1)
                #sys.stdout.flush()

                bytes_content = b"progress@%f"%iPct
                bytes_content = bytes_content.zfill(512)
                assert (len(bytes_content) == 512)
                # 🛠todo fix 固定512 个byte 很傻
                conn.sendall(bytes_content)


                # 不发送给主进程，
                # strData = json.dumps(dict_row)
                # strData = "data@%s" % strData
                # bytes_content = str.encode(strData, encoding='utf-8')
                # bytes_content = bytes_content.zfill(512)
                # assert (len(bytes_content) == 512)
                # # 🛠todo fix 固定512 个byte 很傻
                # conn.sendall(bytes_content)

                strMsg0 = "logging@股票资金流向{}, 日期数据 {} OK".format(code, dict_row['date'])
                bytes_content = strMsg0.encode()
                bytes_content = bytes_content.zfill(512)
                assert (len(bytes_content) == 512)
                # 🛠todo fix 固定512 个byte 很傻
                conn.sendall(bytes_content)

                # v = []
                # v.append() # 日期
                # v.append(table_body_cell[1].text) # 收盘价
                # v.append(table_body_cell[2].text) # 涨跌幅
                # v.append(table_body_cell[3].text) # 主力净流入_净额(万元)
                # v.append(table_body_cell[4].text) # 主力净流入_净占比(%)
                # v.append(table_body_cell[5].text) # 超大单净流入_净额(万元)
                # v.append(table_body_cell[6].text) # 超大单净流入_净占比(%)
                # v.append(table_body_cell[7].text) # 大单净流入_净额(万元)
                # v.append(table_body_cell[8].text) # 大单净流入_净占比(%)
                # v.append(table_body_cell[9].text) # 中单净流入_净额(万元)
                # v.append(table_body_cell[10].text)# 中单净流入_净占比(%)
                # v.append(table_body_cell[11].text)# 小单净流入_净额(万元)
                # v.append(table_body_cell[12].text)# 小单净流入_净占比(%)

            t = time.clock() - t0
            #print('总体耗时间： %f' % t)

        else:
            #raise NoSuchElementException
            #print("error !!!!!!!!")
            pass

        assert (len(row1_list) != 0)
        assert (len(head1_list) != 0)
        assert (len(head2_list) != 0)

        ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()

        #print("🖼 完成获取数据，关闭chromedrive ，")

        strMsg0 = "logging@准备写入数据库{}".format(code)
        bytes_content = strMsg0.encode()
        bytes_content = bytes_content.zfill(512)
        assert (len(bytes_content) == 512)
        # 🛠todo fix 固定512 个byte 很傻
        conn.sendall(bytes_content)

        client = DATABASE
        coll_stock_zjlx = client.eastmoney_stock_zjlx

        print("🥕准备写入mongodb 🎞保存数据库 ", 'eastmoney_stock_zjlx')

        new_rec = 0
        for i in range(len(row1_list)):
            aRec = row1_list[i]

            # 🛠todo 当天结束后，获取当天的资金流相，当天的资金流向是瞬时间点的
            ret = coll_stock_zjlx.find_one(aRec)
            if ret == None:
                coll_stock_zjlx.insert_one(aRec)
                new_rec = new_rec + 1
                print("🤑 插入新的记录 ", aRec)

                # strMsg0 = "logging@写入{}".format(aRec)
                # bytes_content = strMsg0.encode()
                # bytes_content = bytes_content.zfill(512)
                # assert (len(bytes_content) == 512)
                # # 🛠todo fix 固定512 个byte 很傻
                # conn.sendall(bytes_content)
            else:
                print("😵 记录已经存在 ", ret)

                # strMsg0 = "logging@记录已经存在{}".format(aRec)
                # bytes_content = strMsg0.encode()
                # bytes_content = bytes_content.zfill(512)
                # assert (len(bytes_content) == 512)
                # # 🛠todo fix 固定512 个byte 很傻
                # conn.sendall(bytes_content)
                pass

        print("🖼  🎞写入数据库  🐌 新纪录 ", new_rec, "条 💹 ")

        strMsg0 = "logging@{}写入数据库新纪录{}条".format(code,new_rec)
        bytes_content = strMsg0.encode()
        bytes_content = bytes_content.zfill(512)
        assert (len(bytes_content) == 512)
        # 🛠todo fix 固定512 个byte 很傻
        conn.sendall(bytes_content)


    except WebDriverException  as ee:
        print("❌ read_east_money_page_zjlx_to_sqllite 读取网页数据错误 🤮")

        errorMsg0  = "finished@code {} msg{}".format(code,ee.__str__())

        bytes_content = errorMsg0.encode()
        bytes_content = bytes_content.zfill(512)
        assert (len(bytes_content) == 512)
        # 🛠todo fix 固定512 个byte 很傻
        conn.sendall(bytes_content)

        ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
        ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
        ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()

        return

    okMsg0  = "finished@code {} 获取完成 OK".format(code)
    bytes_content = okMsg0.encode()
    bytes_content =bytes_content.zfill(512)
    assert(len(bytes_content) == 512)
    # 🛠todo fix 固定512 个byte 很傻
    conn.sendall(bytes_content)





if __name__ == '__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = sys.argv[1]

    # Bind the socket to the port
    server_address = ('localhost', int(port))
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    browser = open_chrome_driver();
    browser.minimize_window()


    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            strMsg0 = "logging@成功建立socket服务，开启Chrome驱动"
            bytes_content = strMsg0.encode()
            bytes_content = bytes_content.zfill(512)
            assert (len(bytes_content) == 512)
            # 🛠todo fix 固定512 个byte 很傻
            connection.sendall(bytes_content)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(11)
                print('received {!r}'.format(data))
                if data:
                    cmdString = data.decode('utf-8');
                    cmdArry = cmdString.split(':')
                    print(cmdArry)
                    #print('sending data back to the client')
                    #connection.sendall(data)

                    if cmdArry[0] == 'read':
                    # do the lone time get the data , report the status
                        crawly_code(code = cmdArry[1], conn= connection, browser= browser);
                        break
                    #等待获取结束
                    if cmdArry[0] == 'shutdown':
                        print(" shutdown 命令收到， 退出进程！")
                        ActionChains(browser).key_down(Keys.COMMAND).send_keys("Q").key_up(Keys.CONTROL).perform()
                        connection.close()
                        os._exit(88)
                else:
                    print('no data from', client_address)
                    break

        finally:
            # Clean up the connection
            connection.close()
