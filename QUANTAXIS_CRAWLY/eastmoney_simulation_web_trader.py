'''

'''
import time
import re
from selenium import webdriver
import sys
from selenium.common.exceptions import NoSuchElementException
import sqlite3

class SingletonMeta(type):
    def __init__(cls, name, bases, namespaces):
        super().__init__(cls, name, bases, namespaces)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)
        else:
            print("instance already existed!")
        return cls.instance



class EastMoneySimulationWebTrader():


    def startTrade(self):

        urls = 'http://www.eastmoney.com/' #登陆到我的东方财富
        pa = re.compile(r'\w+')

        self.webdriver_parent_path = './QUANTAXIS_WEBDRIVER/macos/'

        if sys.platform == 'darwin':
            browser = webdriver.Chrome(self.webdriver_parent_path+'chromedriver')
        elif sys.platform == 'win32':
            browser = webdriver.Chrome(self.webdriver_parent_path+'chromedriver')
        elif sys.platform == 'linux':
            browser = webdriver.Chrome(self.webdriver_parent_path+'chromedriver')
            # todo 🛠  linux 下没有测试， linux 下 非gui环境下，用chrome headless driver
            print("🎃")
            print("🎃./selenium_driver/linux/chromedrive   linux 平台上的的      🤖chromedriver 的路径")
            print("🎃./selenium_driver/windows/chromedrive windows 平台上的的    🤖chromedriver 的路径")
            print("🎃   https://npm.taobao.org/mirrors/chromedriver/            🤖chromedriver下载地址")
            print("🎃")
            return

        # 启动chrome
        print("🖼 准备获取数据， 打开chromedrive ，")
        browser.set_page_load_timeout(30)  # throw a TimeoutException when thepage load time is more than 15 seconds
        #browser.minimize_window()

        print("🖼 正在请求数据中，请耐心等待 🍺 ⌛ ⌛ ⌛ ⌛ ⌛ ️")
        #.get(urls)
        #browser.
        browser.get(urls)

        num = browser.window_handles

        print(type(num[0]))


        browser.find_element_by_id('loginMenu').click()

        num = browser.window_handles
        # browser.switch_to(num[1])
        time.sleep(1)  # Let the page load
        time.sleep(1)  # Let the page load

        #spanTag = browser.find_elements_by_name('body')

        #browser.find_elements_by_id()

        #currHandle = browser.current_window_handler
        browser.switch_to.window(num[1])

        txt = browser.find_element_by_xpath('/html/body/div[1]/div/div/h1')
        print(txt.text)

        frameLogIn = browser.find_element_by_id('frame_login')
        browser.switch_to.frame(frameLogIn)


        #account = browser.find_element_by_id('txt_account')
        account = browser.find_elements_by_xpath('//*[@id="txt_account"]')

        #输入用户名
        account[0].send_keys('*********')
        #输入密码
        password = browser.find_element_by_id('txt_pwd')
        password.send_keys('*********')

        browser.find_element_by_id('btn_login').click()
        # id; txt_account
        # account; txt_pwd


        time.sleep(1)  # Let the page load
        time.sleep(1)  # Let the page load
        time.sleep(1)  # Let the page load
        time.sleep(1)  # Let the page load
        time.sleep(1)  # Let the page load


        # 成功登陆东方财富

        browser.quit()

pass
