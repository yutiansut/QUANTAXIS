# QUANTAXIS CRAWL



## SELENIUM WEBDRIVER

see https://gitee.com/yutiansut/QUANTAXIS_WEBDRIVER/

将python使用的webdriver都搜罗如下:

- chrome_webdriver(win32/mac/linux32/linux64)
- selenium(win32/mac/linux32/linux64)
- firefox_geckodriver(win32/win64/mac/linx32/linux64)
- operadriver(win32/win64/mac/linux64)


### clone repo/downlowd all files
```
git clone https://gitee.com/yutiansut/QUANTAXIS_WEBDRIVER/
```


### download file what you need

```python

sys in ['linux32','linux64','win32','win64','mac']

file in ['chromedriver','geckodriver','operadriver','phantomjs','chromedriver.exe','geckodriver.exe','operadriver.exe','phantomjs.exe']

'https://gitee.com/yutiansut/QUANTAXIS_WEBDRIVER/raw/master/{}/{}'.format(sys,file)

```