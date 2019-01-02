import time

import pandas as pd
from selenium import webdriver

"""这里我给了一个同花顺的页面爬虫 用于gecko_driver  也就是 火狐浏览器内核爬虫的教学

推荐使用火狐浏览器的内核 配置方便
"""

opener = webdriver.Firefox()  # should make sure the gekkodriver.exe in path
data = []


for item in ['gn', 'dy', 'thshy', 'zjhhy']:
    opener.get('http://q.10jqka.com.cn/{}/'.format(item))

    hpage = opener.page_source

    # opener.save_screenshot('page_gn.png')
    try:
        if opener.find_element_by_class_name('cate_toggle.boxShadow').text == '收起':
            pass
        else:
            opener.find_element_by_class_name('cate_toggle.boxShadow').click()
    except:
        pass

    res = opener.find_elements_by_xpath('/html/body/div/div/div/div/div/a')

    data.extend([[res.text, res.get_attribute('href'), item] for res in res])

    time.sleep(1)


res = pd.DataFrame(data)
print(res)
opener.close()
res.to_csv('ths.csv')
