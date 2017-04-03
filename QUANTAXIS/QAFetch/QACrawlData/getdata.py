#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
import json
import datetime
import time
import pandas as pd
from bs4 import *
import lxml
from multiprocessing.dummy import Pool
import socket


def _get_data(url):
    time.sleep(0.1)
    headers = {'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
               }
    data = None
 
    req = urllib.request.Request(url, data, headers)
    ret = urllib.request.urlopen(req)
    return ret

def _soup(url,element):
    ret = _get_data(url).read()
    try:
        html = ret.decode('utf-8')
    except:
        try:
            html = ret.decode('gbk')
        except:
            html = ret.decode('gb2312')
    soup = BeautifulSoup(html, 'lxml')
    var = soup.find_all(element)
    return var


def _thread(hs, cs, n):
    pool = Pool(n)
    ret = pool.map(hs, cs)
    pool.close()
    pool.join()
    return ret
###财务报表
def _financial(x):
    index = x[0]['title'][0]
    ret = []
    for i in range(len(x)):
        ret.append([])
    for i in range(len(x)):
        report = x[i]['report']
        title = x[i]['title']
        z = len(title)
        y = len(report[0])
        for j in range(y):
            var = {}
            var[str(title[0])] = datetime.datetime.strptime(str(report[0][j]),'%Y-%m-%d')
            for k in range(1,z):
                if  report[k][j] != '':
                    var[str(title[k])] = float(report[k][j])
                else:
                    var[str(title[k])] = float(0)
            ret[i].append(var)
    for i in range(len(x)):
        ret[i] = pd.DataFrame(ret[i])
        ret[i] = ret[i].set_index(index)
    return ret
def _get_financial(hy):
    url = []
    ret = []
    url.append('http://stockpage.10jqka.com.cn/basic/' + hy + '/debt.txt')
    url.append('http://stockpage.10jqka.com.cn/basic/' + hy + '/benefit.txt')
    url.append('http://stockpage.10jqka.com.cn/basic/' + hy + '/cash.txt')
    for i in url:
        var = _get_data(i)
        ret.append(json.loads(var.read().decode()))
    ret = _financial(ret)
    return ret
def get_financial(hy):
    return _get_financial(hy)
###F10基本信息
def _cninfosymbol(hy):#转换合约代码
    if hy[0] =='6':
        ret = 'shmb' +hy
    elif hy[0] =='3':
        ret ='szcn' + hy
    else:
        if hy[0:3] == '000':
            ret = 'szmb' + hy
        else :
            ret = 'szsme' + hy
    return ret

def _cninfo(cs):
    url = 'http://www.cninfo.com.cn/information/' + cs[0] +'/' +  _cninfosymbol(cs[1])  +'.html'
    var =_soup(url,'td')
    ret =[]
    for i in var:
        x =i.text.replace('\r\n' ,'').rstrip()
        ret.append(x)
    for i in range(3):
        del ret[0]
    return ret
def ths_ipo():
    url = 'http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/1/order/desc/ajax/1/'
    try :
        var = _soup(url,'td')
        title =_soup(url,'a')
    except UnicodeDecodeError:
         var = _soup(url,'td')
         title =_soup(url,'a')
    id =[]
    for i  in range (len(title)):
        if title[i].text == '股票代码':
            id .append(i)
    title =title[id[0]:id[1]]
    id =[]
    for i in title:
        id.append(i.text)
    z =len(var)
    y = z // 18
    ret = []
    for i in range (y):
        tmp ={}
        for j in range(len(id)):
            tmp[id[j]] = var[i*18 +j].text
        tmp['中签缴款日期']=tmp['中签缴款日期'].split('\n')[0]
        tmp['股票代码'] = tmp['股票代码'].split('\n')[1]
        ret.append(tmp)
    ret = pd.DataFrame(ret)
    ret = ret.set_index('股票代码')
    return ret


def _tfp(dt):#dt = 2016-09-30
    if len(dt) == 8:
        dt = dt[:4]  + '-' + dt[4:6] + '-' + dt[6:8]
    url ='http://www.cninfo.com.cn/cninfo-new/memo-2?queryDate=' +  dt  + '&queryType=queryType1'
    var = _soup(url,'li')
    id = []
    for i in range(len(var)):
        if var[i].text =='代码':
            id.append(i)
    tp =[]
    for i in range(id[0],id[1]):
        tp.append(var[i])
    fp =[]
    for i in range(id[1],id[2]):
        fp.append(var[i])
    tp = pd.DataFrame(_ftptmp(tp))
    fp = pd.DataFrame(_ftptmp(fp))
    tp = tp.set_index('代码')
    fp = fp.set_index('代码')
    return [tp,fp]
def _ftptmp(tfp):
    var =[]
    title = []
    z =len(tfp)
    for i in range(0, 6):
        title.append(tfp[i].text)
    for i in range(1, z // 6):
        tmp = {}
        for j in range(6):
            tmp[title[j]] = tfp[i * 6 + j].text
        var.append(tmp)
    return var

def get_tfp(dt):
    return _tfp(dt)

def _get_brief(hy):#公司概况
    cs = ['brief',hy]
    var = _cninfo(cs)
    z = len(var)
    ret =[]
    for i in range(0,z):
        if i % 2 ==0:
            ret.append([var[i],var[i+1]])
    z = len(ret)
    var = {'code': hy}
    for i in range(z):
        t = ret[i][0]
        t = t[:len(t) - 1]
        var[t] = ret[i][1]
    return var

def get_brief(symbol_list):#公司概况
    n = 1
    if len(symbol_list) >4 :
        n = 4
    var = _thread(_get_brief,symbol_list,n)
    var =  pd.DataFrame(var)
    var = var.set_index('code')
    return var

def _get_lastest(hy):#最新资料
    cs = ['lastest',hy]
    var = _cninfo(cs)
    z = len(var)
    ret =[]
    for i in range(0,z):
        if i % 2 ==0:
            ret.append([var[i],var[i+1]])
    z = len(ret)
    var = {'code': hy}
    for i in range(z):
        t = ret[i][0]
        t = t[:len(t) - 1]
        var[t] = ret[i][1]
    return var
def get_lastest(symbol_list):
    n = 1
    if len(symbol_list) >4 :
        n = 4
    var = _thread(_get_lastest,symbol_list,n)
    var =  pd.DataFrame(var)
    var = var.set_index('code')
    return var
def get_dividend(hy):#分红
    cs =['dividend',hy]
    var = _cninfo(cs)
    for i in range(0,5):
        del var[0]
    ret =[]
    z = len(var)
    k = z // 5
    for i in range(1,k):
        y={}
        for j in range(0,5):
            y[var[j]] = var[i * 5 + j].lstrip()
        ret.append(y)
    ret = pd.DataFrame(ret)
    return ret

def get_allotment(hy):#配股
    cs =['allotment',hy]
    var = _cninfo(cs)
    for i in range(0,5):
        del var[0]
    ret =[]
    z = len(var)
    k = z // 7
    for i in range(1,k):
        y={}
        for j in range(0,7):
            y[var[j]] = var[i * 7 + j].lstrip()
        ret.append(y)
    ret = pd.DataFrame(ret)
    return ret

def _fhdate():
    t =datetime.datetime.now()
    year = t.year
    month = 11
    ret =[]
    if month <=3 :
        dt1 = str(year - int(1)) +'-'+'06-30'
        dt2 = str(year - int(2)) +'-'+'12-31'
        ret =[dt1,dt2]
    elif month <=6 :
        dt1 = str(year - int(1)) + '-' + '06-30'
        dt2 = str(year - int(1)) + '-' + '12-31'
        ret = [dt2, dt1]
    else:
        dt1 = str(year ) + '-' + '06-30'
        dt2 = str(year - int(1)) + '-' + '12-31'
        ret = [dt1, dt2]
    return ret
def _get_fhpage(dt):
    pg = '1'
    url = 'http://data.10jqka.com.cn/financial/sgpx/date/' + dt + '/board/ALL/field/yaggr/order/desc/page/' + pg + '/ajax/1/'
    page = _soup(url,'span')
    pages = int(page[0].text.split('/')[1])
    return pages
def _get_lastfh(cs):
    dt =cs[0]
    pg =str(cs[1])
    url = 'http://data.10jqka.com.cn/financial/sgpx/date/' + dt + '/board/ALL/field/yaggr/order/desc/page/'+ pg +'/ajax/1/'
    var = _soup(url,'td')
    title = ['序号', '股票代码', '股票简称', '最新价', '预计除权除息价', '是否已分配', '送股(每十股)', '转增股(每十股)', '送转总数(每十股)', '派息 / 元(每十股)',
             '预案公布日', '股权登记日', '除权除息日']
    z = len(var)
    y = len(title)
    fh = []
    for i in range(0, z // y):
        v = {}
        for j in range(y):
            v[title[j]] = var[i * y + j].text.replace('\n','')
        fh.append(v)
    return fh
def get_fh_all():
    dt = _fhdate()
    cs = []
    for i in range(2):
        p = _get_fhpage(dt[i])
        for j in range(p):
            cs.append([dt[i], j + 1])
    z = len(cs)
    n = max (z // 5 ,1)
    var = _thread(_get_lastfh, cs, n)
    ret = []
    for i in range(z):
        for j in var[i]:
            ret.append(j)
    ret = pd.DataFrame(ret)
    ret = ret.set_index('股票代码')
    return ret

#######
##########截面数据
def _get_pages(url):
    var = _get_data(url)
    var = var.read().decode('gbk').split('=')[1].split('},')
    var[0] = var[0].split(',')[1].split(':')[1]
    for i in ['[', ']', '"']:
        var[2] = var[2].replace(i, '')
    var[2] = var[2].split('\n')
    del var[2][0]
    del var[2][0]
    del var[2][len(var[2]) - 1]
    del var[2][len(var[2]) - 1]
    z = len(var[2])
    if z > 0:
        for i in range(0, z):
            var[2][i] = var[2][i].split(',')
            if var[2][i][len(var[2][i]) - 1] == '':
                del var[2][i][len(var[2][i]) - 1]
    del var[1]
    return var
def get_stocklist():#取A股列表
    url = 'http://q.jrjimg.cn/?q=cn|s|sa&c=m&n=hqa&o=code,a&p=1100'
    sj = _get_pages(url)
    z = int(sj[0])
    var = []
    for i in range(1, z + 1):
        k = str(i) + '100'
        var.append('http://q.jrjimg.cn/?q=cn|s|sa&c=m&n=hqa&o=code,a&p=' + k)
    sj = _thread(_get_pages, var, 4)
    ret = []
    x = ['id', 'code', 'name', 'lcp', 'stp', 'open', 'high', 'low', 'close', 'vol', 'amount', '涨跌', '涨幅', 'sl', '量比',
         '换手', '内盘', '外盘', '现手', '现额', 'bsa', '市盈率']
    z = len(x)
    for i in sj:
        for k in i[1]:
            var = {}
            for j in range(0, z):
                strlist = ['id', 'code', 'name']
                intlist = ['vol', '内盘', '外盘', '现手']
                if x[j] in strlist:
                    var[x[j]] = k[j]
                elif x[j] in intlist:
                    var[x[j]] = int(k[j])
                else:
                    var[x[j]] = float(k[j])
            ret.append(var)
    ret = pd.DataFrame(ret)
    ret = ret.set_index('code')
    return ret


def _get_last_daily(hy):
    url = 'http://q.jrjimg.cn/?q=cn|s&i=' +hy+'&c=l'
    var = _get_data(url)
    var = var.read().decode('gbk').split('=')[1].split('},')
    for i in ['[', ']', '"']:
        var[2] = var[2].replace(i, '')
    var[2] = var[2].split('\n')
    del var[2][0]
    del var[2][0]
    del var[2][len(var[2]) - 1]
    del var[2][len(var[2]) - 1]
    if len(var[2]) == 1:
        var = var[2][0].split(',')
    x = ['id', 'code', 'name', '涨停', '跌停', 'lcp', 'stp', '均价', 'open', 'high', 'low', 'close', 'vol', 'amount',
         '流通股（亿）', '总股本（亿）', '流通市值', '总市值', '涨跌', '涨幅', 'sl', 'pens', '量比', 'cot', '换手', '内盘', '外盘', 'time', 'hqtime',
         '现手', '现额', 'bsa',
         '买1价', '买2价', '买3价', '买4价', '买5价', '买1量', '买2量', '买3量', '买4量', '买5量', '卖1价', '卖2价', '卖3价', '卖4价', '卖5价', '卖1量',
         '卖2量', '卖3量', '卖4量', '卖5量', '市盈率', '市净率', 'min5pl', 'apesh']
    ret = {}
    for i in range(0, len(var)):
        timelist =['time','hqtime']
        strlist =['id', 'code', 'name']
        intlist = ['vol', '内盘', '外盘',  '买1量', '买2量', '买3量', '买4量', '买5量', '卖1量','卖2量', '卖3量', '卖4量', '卖5量','现手']
        if x[i] in strlist:
            ret[x[i]] = var[i]
        elif x[i] in timelist:
            ret[x[i]] = datetime.datetime.strptime(  var[i],'%Y%m%d%H%M%S')
        elif x[i] in intlist:
            ret[x[i]] = int(var[i])
        else:
            ret[x[i]] = float(var[i])
    return ret

def get_last_dailybar(symbol_list):#取当日截面数据
    x =[1]
    ret =[]
    if type(x) == type(symbol_list) :
        z = len(symbol_list)
        if z>10:
            n=4
        else:
            n=1
        ret = _thread(_get_last_daily, symbol_list, n)
    if len(ret) > 0:
        ret =  pd.DataFrame(ret)
        ret = ret.set_index('code')
    return ret

#######h获取TICK
def _get_tick(cs):
    symbol = cs[0]
    page =str(cs[1])
    num = str(cs[2])
    url = 'http://qmx.jrjimg.cn/mx.do?code=' + symbol +'&page=' + page +'&size=' + num
    VAR = _get_data(url).read().decode('gbk').split('\r\n')
    var = []
    var.append(VAR[2])
    var.append(VAR[4])
    for i in range(7,len(VAR)-1):
        var.append(VAR[i])
    var[0] = var[0][6:len(var[0]) - 2].split(',')
    for i in range(len(var[0])):
        var[0][i] = int(var[0][i].split(':')[1])
    var[1] = var[1].split('"')
    del var[1][6]
    del var[1][4]
    del var[1][2]
    del var[1][0]
    z = len(var)
    ret = [var[0] + var[1]]
    for i in range(2, z):
        VAR = {}
        k = ['{', '},', '"', ' ','}']
        for j in k:
            var[i] = var[i].replace(j, '')
        var[i] = var[i].split(',')
        VAR['成交价'] = float(var[i][0][3:len(var[i][0]) ])
        VAR['成交量'] = int(var[i][1][3:len(var[i][1]) ])
        amount = var[i][2][3:len(var[i][2]) ]
        if 'E' in list(amount):
            amount = amount.split('E')
            AM = round(float(amount[0]) * float(100000000.00),2)
        else:
            AM = float(amount)
        VAR['成交额'] = AM
        VAR['成交笔'] = int(var[i][3][3:len(var[i][3]) ])
        VAR['成交时间'] = var[i][4][3:len(var[i][4]) ]
        VAR['成交方向'] = var[i][5][3:len(var[i][5]) ]
        ret.append(VAR)
    return ret
def get_last_tick(symbol_list):#取当日最后1个TICK
    x = [1]
    if type(x) == type(symbol_list):
        z = len(symbol_list)
        if z > 10:
            n = 4
        else:
            n = 1
        var =[]
        for i in symbol_list:
            var.append([i,1,1])
        ret = _thread(_get_tick, var, n)
        var =[]
        for i in range(z):
            tmp = ret[i][1]
            tmp['code'] = ret[i][0][4]
            tmp['name'] = ret[i][0][5]
            var.append(tmp)
    if len(var) > 0:
        ret = pd.DataFrame(var)
        ret = ret.set_index('code')
    return ret


def _get_last100_ticks(symbol_list):#取当日最近100个TICK
    x = [1]
    if type(x) == type(symbol_list):
        z = len(symbol_list)
        if z > 10:
            n = 4
        else:
            n = 1
        var = []
        for i in symbol_list:
            var.append([i,1, 100])
        ret = _thread(_get_tick, var, n)
        for i in range(z):
            for j in range(1,len(ret[i])):
                code= ret[i][0][4]
                name = ret[i][0][5]
                ret[i][j]['code'] =code
                ret[i][j]['name'] =name
            del ret[i][0]
    return ret
def get_last100_ticks(symbol_list):
    var =_get_last100_ticks(symbol_list)
    z = len(var)
    ret = []
    for i in range(z):
        t = var[i]
        t = pd.DataFrame (t)
        t = t.set_index('成交时间')
        ret.append(t)
    return ret



def _get_all_ticks(symbol):
    n = 1
    cs =[symbol,1,1]
    var =_get_tick(cs)
    ret = [var[0]]
    page = var[0][2] // 100
    ys = var[0][2] // 100
    if ys != 0 :
        page = page + 2
    else:
        page = page +1
    if page >10 :
        n  = 4
    VAR =[]
    for i in range (1,page):
        VAR.append([symbol,i,100])
    var = _thread(_get_tick, VAR, n)
    for i in var:
        for j in range (1,len(i)):
            ret.append(i[j])
    return ret
def _all_ticks(symbol_list):#取当日全部TICK
    x = [1]
    if type(x) == type(symbol_list):
        z = len(symbol_list)
        if z > 10:
            n = 4
        else:
            n = 1
        ret = _thread(_get_all_ticks, symbol_list, n)
        for i in range(z):
            for j in range(1, len(ret[i])):
                code = ret[i][0][4]
                name = ret[i][0][5]
                ret[i][j]['code'] = code
                ret[i][j]['name'] = name
            del ret[i][0]
    return ret
def get_all_ticks(symbol_list):
    var = _all_ticks(symbol_list)
    z = len(var)
    ret = []
    for i in range(z):
        t = var[i]
        t = pd.DataFrame(t)
        t = t.set_index('成交时间')
        ret.append(t)
    return ret
def _moneyflow(hy):
    url ='http://hqcdn.quote.eastmoney.com/allXML/xml/' + hy + '.xml'
    var =_soup(url,'slice')
    ret = {'code':hy}
    for i in range ( len(var)):
        ret[var[i].attrs['title']] = float(var[i].text)
    return ret
def _get_moneyflow(symbol_list):
    ret = []
    if type(ret) == type(symbol_list):
        z = len(symbol_list)
        if z > 10:
            n = 4
        else:
            n = 1
        ret = _thread(_moneyflow, symbol_list, n)
    return ret
def get_moneyflow(symbol_list):
    var = _get_moneyflow(symbol_list)
    var = pd.DataFrame(var)
    var =var.set_index('code')
    return var
############
def _money_on_minute(hy):
    url ='http://hqcdn.quote.eastmoney.com/allXML/' + hy +'.xml'
    var =_get_data(url).read().decode().split('\r\n')
    del var[len(var)-1]
    del var[0]
    del var[0]
    ret = []
    for i in range(len(var)):
        tmp={}
        var[i] = var[i].split(';')
        tmp['time'] =var[i][0]
        tmp['主力净流入'] = var[i][1]
        tmp['超大单净流入'] = var[i][1]
        tmp['大单净流入'] = var[i][2]
        tmp['中单净流入'] = var[i][3]
        tmp['小单净流入'] = var[i][4]
        ret.append(tmp)
    return ret

def get_money_on_minute(hy):
    var = _money_on_minute(hy)
    var = pd.DataFrame(var)
    var = var.set_index('time')
    return var



####获取日K线
def _get_datalist(var,hy):
    for i in range(0, len(var)):
        var[i] = var[i].split(',')
        for j in range(1, 7):
            try:
                if var[i][j] != '':
                    var[i][j] = float(var[i][j])
                else:
                    var[i][j] = float(0)
            except ValueError:
                continue
        var[i][7] = int(hy)
        tim =datetime.datetime.strptime(str(var[i][0]),'%Y%m%d')
        var[i][0] = tim
    return var
def _get_day_year(cs):
    hy = cs[0]
    year = str(cs[1])
    style = cs[2]
    url = 'http://d.10jqka.com.cn/v2/line/hs_'  +hy +'/' + style + '/' + year +'.js'
    var = _get_data(url).read().decode()
    var = var.split('":"')[1]
    var = var[0:len(var) - 4].split(';')
    ret = _get_datalist(var,hy)
    return ret
def _get_day_lastyear(cs):
    hy = cs[0]
    style = cs[1]
    url = 'http://d.10jqka.com.cn/v2/line/hs_'  +hy +'/' + style + '/'  +'last.js'
    var = _get_data(url).read().decode()
    var = var.replace('"','').split('{')
    num =[]
    var[2]=var[2].split('}')
    var[2][1] = var[2][1].split('data')
    var[2][0] = var[2][0].split(',')
    for i in var[2][0]:
        num.append(i)
    VAR = var[2][1][1]
    VAR = VAR [1:len(VAR)].split(';')
    var = _get_datalist(VAR,hy)
    return [num,var]
def _fq(var):#复权参数
    if var =='qfq':
        ret = '01'
    elif var =='hfq':
        ret = '02'
    else:
        ret = '00'
    return ret
def get_dailybars_year(cs):
    cs[2] =_fq(cs[2])
    ret = _get_day_year(cs)
    ret = _klinetodict(ret)
    ret = pd.DataFrame(ret)
    ret = ret.set_index('date')
    return ret
def get_yearlist(cs):
    cs[1] =_fq(cs[1])
    var =_get_day_lastyear(cs)[0]
    return var

def get_last_n_dailybars(cs):#[hy,n,'qfq']
    hy = cs[0]
    n  = cs[1]
    style = _fq(cs[2])
    cs =[hy,style]
    var = _get_day_lastyear(cs)
    z = len(var[1])
    ret =[]
    if n > z :
        t = []
        for i in var[0]:
            t.append(i.split(':'))
        sj = 0  # K线数量的变量
        m = []  # 定位年份
        num = 0  # 全部数据个数
        for i in range(0, len(t)):  # 计算上市以来全部K线数量
            num = num + int(t[i][1])
        if num >= n :
            for i in range(0, len(t)):
                k = len(t) - 1 - i
                if sj < n:
                    sj = sj + int(t[k][1])
                    m.append(t[k][0])
        else:
            for i in range(0, len(t)):
                k = len(t) - 1 - i
                m.append(t[k][0])
        cs =[]
        for i in range(0,len(m)):
            k = len(m) -1-i
            cs.append([hy,m[k],style])
        for i in cs:
            VAR = _get_day_year(i)
            for i in VAR:
                ret.append(i)
    else:
        ret = var[1]
    x = len(ret)
    if x >n :
            y = x - n
            for k in range(0,y):
                del ret[0]
    ret = _klinetodict(ret)
    ret = pd.DataFrame(ret)
    ret = ret.set_index('date')
    return ret

def get_all_dailybars(cs):#[hy,'hfq']
    hy = cs[0]
    style = _fq(cs[1])
    cs =[hy,style]
    var = _get_day_lastyear(cs)
    z = len(var[1])
    if  z > 0 :
        t = []
        for i in var[0]:
            t.append(i.split(':'))
        cs =[]
        ret =[]
        for i in range(0,len(t)):
            cs.append([hy,t[i][0],style])
        for i in cs:
            VAR = _get_day_year(i)
            for i in VAR:
                ret.append(i)
    ret =_klinetodict(ret)
    ret = pd.DataFrame(ret)
    ret = ret.set_index('date')
    return ret

####获取分钟K
def _hexun_symbol(hy):
    if len(hy) == 6:
        if hy[0] =='6' :
            ret = 'sse' + hy
        else:
            ret = 'szse' + hy
    else:
        if hy[0:2] == 'sh':
            ret = 'sse' + hy[2:8]
        else:
            ret = 'szse' + hy[2:8]
    return ret
def _hexun_time():
    now =datetime.datetime.now()
    ret = now.strftime('%Y%m%d') + '150000'
    return ret
def get_bars(cs):
    hy =_hexun_symbol(cs[0])
    TYPE =str(cs[1])
    now =_hexun_time()
    url = 'http://webstock.quote.hermes.hexun.com/a/kline?code=' + hy +'&start='+ now + '&number=-1000&type=' + TYPE
    var = _get_data(url).read().decode()
    var = var[1:len(var) - 2]
    VAR = json.loads(var)
    var = VAR['Data']
    for i in var[0]:
        i[0] = datetime.datetime.strptime(str(i[0]),'%Y%m%d%H%M%S')
        i[1] = i[2] / var[4]
        i[2] = i[4]/ var[4]
        i[4] = i[3]/ var[4]
        i[3] = i[5]/ var[4]
        i[5] = i[6]/ var[4]
        i[6] = i[7]/ var[4]
        hy =hy[len(hy)-6:len(hy)]
        i[7] = str(hy)
    ret = _klinetodict(var[0])
    ret = pd.DataFrame(ret)
    ret = ret.set_index('date')
    return ret
def _klinetodict(var):
    ret =[]
    DICT =['date','open','high','low','close','vol','amount','code']
    for i in var:
        VAR ={}
        for j in range(0, len(DICT)):
            VAR[DICT[j] ]= i[j]
        ret.append(VAR)
    return ret
def get_money_30days(hy):
    url ='http://data.eastmoney.com/zjlx/graph/his_' +hy +'.html'
    var = _get_data(url).read().decode().split('\r\n')
    del var[len(var)-1]
    del var[len(var) - 1]
    del var[0]
    del var[0]
    z=len(var)
    ret=[]
    for i in range(z):
            var[i] = var[i].split(';')
            tmp = {}
            tmp['date'] = var[i][0]
            tmp['主力净流入'] =var[i][1]
            tmp['超大单净流入'] = var[i][2]
            tmp['大单净流入'] = var[i][3]
            tmp['中单净流入'] =var[i][4]
            tmp['小单净流入'] =var[i][5]
            ret.append(tmp)
    ret = pd.DataFrame(ret)
    day = list(get_last_n_dailybars([hy,40,'bfq']).index)
    for i in range (len(ret)):
        for j in range (len(day)):
            tr = day[j].strftime('%m-%d')
            if tr == ret.iloc[i]['date']:
                ret.iloc[i]['date'] = day[j]
    return ret


####历史tick接口1
def _hy_xl(hy):
    if hy[0]  != 's':
        if hy[0] == '6':
            hy = 'sh' +hy
        else:
            hy = 'sz' +hy
    return hy
def _tick_page(cs):
    url = 'http://market.finance.sina.com.cn/transHis.php?symbol=' + cs[0] + '&date=' + cs[1] + '&page=' +str(cs[2])
    var = _soup(url, ['th', 'td'])
    z =len(var)
    n = z //6
    ret =[]
    for i in range(1,n):
        tmp = {}
        t = cs[1] + var[i * 6 + 0].text
        t = datetime.datetime.strptime(t,'%Y-%m-%d%H:%M:%S')
        tmp['date'] = t
        tmp['close'] = float(var[i * 6 + 1].text.replace(',',''))
        tmp['vol'] = int(var[i * 6 + 3].text.replace(',',''))
        tmp['amount'] = float(var[i * 6 + 4].text.replace(',',''))
        tmp['type'] = var[i * 6 + 5].text
        tmp['code'] = cs[0]
        ret.append(tmp)
    return ret
def _tick_pages(cs):
    hy = cs[0]
    dt = cs[1]
    url = 'http://market.finance.sina.com.cn/transHis.php?symbol=' + hy +'&date=' + dt +'&page=1'
    var = _get_data(url).read().decode('gb2312').split('var')[5].replace(';','').replace(']','').split(',[')
    ret = []
    for i in range (len(var)):
        ret.append([hy,dt,i+1])
    return ret
def _tick_day(cs):
    hy =cs[0]
    dt = str(cs[1])
    cs = _tick_pages([hy,dt])
    n = 4
    ret = _thread(_tick_page,cs,n)
    var = []
    for i in ret:
        for j in i:
            var.append(j)
    return var
####历史tick接口2
def _tick_history_data(cs):
    hy =cs[0]
    dt = str(cs[1])
    url = 'http://market.finance.sina.com.cn/downxls.php?date='+ dt + '&symbol=' + hy
    var = _get_data(url).read().decode('gb2312').split('\n')
    return [hy,dt,var]
def _tick_his(VAR):
    hy = VAR[0]
    dt = VAR[1]
    var =VAR[2]
    del var[len(var)-1]
    del var[0]
    z = len(var)
    for i in range(z):
        var[i] =var[i].split('\t')
    ret =[]
    for i in var:
        tmp = {}
        Time = dt  + i[0]
        Time = datetime.datetime.strptime(Time,'%Y-%m-%d%H:%M:%S')
        tmp['date'] =Time
        tmp['close'] = float(i[1])
        tmp['vol'] = int(i[3])
        tmp['amount'] = float(i[4])
        tmp['type'] = str(i[5])
        tmp['code'] = hy
        ret.append(tmp)
    return ret
def _tick_onday(cs):
    var = _tick_history_data(cs)
    var =_tick_his(var)
    return var
def _get_tick1(cs):
    try :
        var= _tick_onday(cs)
        if len(var) <5 :
            var = _tick_day(cs)
    except :
        var = _tick_day(cs)
    return var
def _get_tick2(cs):
    try:
        var = _tick_day(cs)
    except :
        var = _tick_onday(cs)
    return var
def get_tick_history(hy,dt):
    if len(dt) == 8:
        dt = dt[:4] + '-' + dt[4:6] + '-' + dt[6:8]
    hy = _hy_xl(hy)
    cs = [hy, dt]
    try:
        var = _get_tick1(cs)
    except:
        try:
            var = _get_tick2(cs)
        except ValueError :
            pass
    try:
        var =pd.DataFrame(var)
        var = var.set_index('date')
        return var
    except :
        pass

def _tick_to_min(data):
    tmp = {}
    tmp['close'] = data['close'][0]
    tmp['open'] = data['close'][len(data)-1]
    tmp['high'] = data['close'].max()
    tmp['low'] = data['close'].min()
    tmp['vol'] = data['vol'].sum()
    tmp['amount'] = data['amount'].sum()
    tmp['code'] = data['code'][0][2:8]
    return tmp
def tick_to_min(var,n):
    #处理时间序列
    d1 = var.index[0].strftime('%Y-%m-%d') + ' 15:00:00'
    d2 = var.index[0].strftime('%Y-%m-%d') + ' 11:30:00'
    sw= pd.date_range(d2, periods=180 // n +1, freq='-'+ str(60*n)+'S')
    xw= pd.date_range(d1, periods=120 // n +1, freq= '-'+str(60*n)+'S')
    ret = []#BAR临时存放
    x = 120 // n 
    for i in range (0,x):#处理下午的数据
        t_end = xw[i] 
        t_begin =xw[i+1]+ datetime.timedelta(seconds=1)
        data = var[t_end:t_begin]
        if data.size !=0 :
            tmp = _tick_to_min(data)
            tmp['date']  =xw[i+1]
            ret.append(tmp)
    for i in range (0,x-1):#处理上午的数据
        t_end = sw[i] 
        t_begin =sw[i+1]+ datetime.timedelta(seconds=1)
        data = var[t_end:t_begin]
        if data.size !=0 :
            tmp = _tick_to_min(data)
            tmp['date']  =sw[i+1]
            ret.append(tmp)
    #处理上午第一根BAR
    t_end = sw[x-1] 
    t_begin = sw[len(sw)-1]
    data = var[t_end:t_begin]
    print (data)
    tmp = _tick_to_min(data)
    tmp['date']  =sw[x]
    ret.append(tmp)
    kline = []
    z=len(ret)
    for i in range(z):#把BAR时间反转
        kline.append(ret[z-1-i])
    kline = pd.DataFrame(kline)
    kline = kline.set_index('date')
    return kline

#############################期货
def _list(blocknum):
    dce = { 'c':444, 'cs':727, 'i':473, 'j':452, 'jd':478,'jm':453, 'l':450, 'm':447, 'p':449, 'pp':539, 'v':451, 'y':448}
    czce ={'cf':456, 'sr':457,'oi':459,'rm':463,'ta':458,'ma':460,'fg':461,'zc':465}
    shfe = {'cu':433,'al':434,'zn':435,'ru':442,'au':437,'rb':439,'pb':436,'ag':438,'bu':443,'ni':772,'sn':773,'hc':538}
    cffex={'if':771,'ic':775,'ih':774,'tf':765,'t':766}
    dcenum =list(dce.values())
    czcenum =list(czce.values())
    shfenum =list(shfe.values())
    cfnum =list(cffex.values())
    if blocknum in cfnum:
        id = 'CFFEX'
        url = 'http://webcffex.hermes.hexun.com/cffex/sortlist?block=' +str(blocknum) +'&number=100&title=5&commodityid=0&direction=0&start=0&column=code,name,price,updown,buyPrice,buyVolume,sellPrice,sellVolume,volume,lastClose,open,high,low,openInterest,addPosition,amount,vibrationRatio,priceWeight,dateTime&callback=hx'
    else:
        if blocknum in dcenum:
            id ='DCE'
        elif blocknum in czcenum:
            id = 'CZCE'
        elif blocknum in shfenum:
            id = 'SHFE'
        else:
            pass
        url ='http://webftcn.hermes.hexun.com/shf/sortlist?block=' +str(blocknum) +'&number=100&title=5&commodityid=0&direction=0&start=0&column=code,name,price,updown,buyPrice,buyVolume,sellPrice,sellVolume,volume,lastClose,open,high,low,openInterest,addPosition,amount,vibrationRatio,priceWeight,dateTime&callback=hx'
    var = _get_data(url).read().decode()
    var = var[3:len(var) - 2]
    VAR = json.loads(var)
    ret = []
    for   i in VAR['Data'][0]:
        if i[0][len(i[0])-2] !='L' :
            tmp ={}
            price = i[17]
            tmp['code'] = id + '.'+i[0]
            tmp['name'] = i[1]
            tmp['close'] =i[2] /price
            tmp['涨跌'] =i[3] /price
            tmp['卖一价'] = i[4][0] /price
            tmp['卖一量'] = i[5][0]
            tmp['买一价'] = i[6][0] /price
            tmp['买一量'] = i[7][0]
            tmp['vol'] = i[8]
            tmp['昨结'] =i[9]
            tmp['open'] =i[10]
            tmp['high'] = i[11] /price
            tmp['low'] = i[12] /price
            tmp['opi'] = i[13]
            tmp['增仓'] =i[14]
            tmp['date'] = i[18]
            ret.append(tmp)
    ret = pd.DataFrame(ret)
    ret = ret.set_index('code')
    return ret
def futrue_list(ls):
    ret = []
    for i in ls :
        var = _list(i)
        ret.append(var)
    return ret
def futrue_id(id):
    dce = { 'c':444, 'cs':727, 'i':473, 'j':452, 'jd':478,'jm':453, 'l':450, 'm':447, 'p':449, 'pp':539, 'v':451, 'y':448}
    czce ={'cf':456, 'sr':457,'oi':459,'rm':463,'ta':458,'ma':460,'fg':461,'zc':465}
    shfe = {'cu':433,'al':434,'zn':435,'ru':442,'au':437,'rb':439,'pb':436,'ag':438,'bu':443,'ni':772,'sn':773,'hc':538}
    cffex={'if':771,'ic':775,'ih':774,'tf':765,'t':766}
    id = id.split('.')
    var =[]
    if id[0].lower() == 'dce':
        if len(id) ==1 :
            var = list(dce.values())
        else:
            var =[dce[id[1].lower()]]
    elif id[0].lower() == 'czce':
        if len(id) ==1 :
            var = list(czce.values())
        else:
            var =[czce[id[1].lower()]]
    elif id[0].lower() == 'shfe':
        if len(id) ==1 :
            var = list(shfe.values())
        else:
            var =[shfe[id[1].lower()]]
    elif id[0].lower() == 'cffex':
        if len(id) ==1 :
            var = list(cffex.values())
        else:
            var =[cffex[id[1].lower()]]
    else:
        pass
    return var
def get_future_list(id):#分类合约
    ls =futrue_id(id)
    return futrue_list(ls)


def get_zhuli():#得到主力合约
    mkid=['dce','czce','shfe','cffex']
    ret = []
    for i in mkid:
        var = get_future_list(i)
        for j in var:
            ret.append(j.head(1))
    z = len(ret)
    for i in range(1,z):
        ret[0] = ret[0].append(ret[i])
    return ret[0]


def _hx_time():
    now =datetime.datetime.now()
    hour = now.hour
    if hour < 16:
        ret = now.strftime('%Y%m%d') + '210000'
    else:
        now = now + datetime.timedelta(days =1)
        ret = now.strftime('%Y%m%d') + '150000'
    return ret

def get_future_bars(cs):
    ID =cs[0].split('.')
    hy = cs[0].replace('.','')
    TYPE = str(cs[1])
    now = _hx_time()
    if ID[0].lower() == 'cffex':
        url = 'http://webcffex.hermes.hexun.com/cffex/kline?code=' + hy + '&start=' + now + '&number=-1440&type=' + TYPE
    else:
        if ID[0].lower() == 'shfe':
            if ID[1][:2].lower()  == 'ru':
                hy = ID[0]  + ID[1]
            elif ID[1][:2].lower()  in ['ag','au']:
                hy = ID[0] + '2' + ID[1]
            else:
                hy = ID[0] + '3' + ID[1]
        url = 'http://webftcn.hermes.hexun.com/shf/kline?code=' + hy + '&start=' + now + '&number=-1440&type=' + TYPE
    var = _get_data(url).read().decode()
    var = var[1:len(var) - 2]
    VAR = json.loads(var)
    var = VAR['Data']
    for i in var[0]:
        i[0] = datetime.datetime.strptime(str(i[0]),'%Y%m%d%H%M%S')
        i[1] = i[2] / var[4]
        i[2] = i[4]/ var[4]
        i[4] = i[3]/ var[4]
        i[3] = i[5]/ var[4]
        i[5] = i[6]/ var[4]
        i[6] = i[7]/ var[4]

        i[7] = cs[0]
    ret = _klinetodict(var[0])
    ret = pd.DataFrame(ret)
    ret = ret.set_index('date')
    return ret

def _find_number(jydw):
    num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    id1 = []
    for k in num:
        x = jydw.find(k)
        id1.append(x)
    y = max(id1)
    jydw = int(jydw[:y + 1])
    return jydw
def future_info(symbol):
    hy = symbol.split('.')[1]
    url = 'http://quote.futures.hexun.com/info/'+ hy +'.shtml'
    var = _soup(url,'td')
    start = 0
    end = 0
    for i in range(len(var)):
        if var[i].text == '品种':
            start = i
        if var[i].text =='交割地点':
            end = i
    z = (end - start) //2
    tmp ={}
    for i in range (z):
        k = 2 * i + start
        tmp[var[k].text.lstrip().rstrip()] = var[k+1].text.lstrip().rstrip()
    
    return tmp
def get_calendar(starttime,endtime):
    url ='http://img1.money.126.net/data/hs/kline/day/times/0000001.json?callback=n'
    var = _get_data(url).read().decode('gb2312')
    var = var[2:len(var) - 2]
    VAR = json.loads(var)
    ret = []
    for i in range (len(VAR['times'])):
        c = VAR['closes'][i]
        dt = datetime.datetime.strptime(VAR['times'][i],'%Y%m%d')
        ret.append({'date':dt,'close':c})
    ret = pd.DataFrame (ret)
    ret = ret.set_index('date')
    var = ret[starttime:endtime ]
    var = list(var.index)
    return var
def get_future_tick(symbol):
    hy = symbol.split('.')
    now = _hx_time()
    if hy[0].lower() == 'cffex':
        url = 'http://webftcn.hermes.hexun.com/shf/deal?code=' + symbol.replace('.','')+ '&start=' + now + '&number=-1000'
    else:
        id = hy[0] + hy[1]
        if hy[0].lower() == 'shfe':
            if hy[1][:2].lower() == 'ru':
                id = hy[0] + hy[1]
            elif hy[1][:2].lower() in ['ag', 'au']:
                id = hy[0] + '2' + hy[1]
            else:
                id = hy[0] + '3' + hy[1]
        url = 'http://webftcn.hermes.hexun.com/shf/deal?code=' + id + '&start=' + now + '&number=-1000'
    var = _get_data(url).read().decode()
    var = var[1:len(var) - 2]
    VAR = json.loads(var)
    PriceWeight = VAR['Data'][5]
    ret = []
    for i in VAR['Data'][0]:
        tmp = {}
        for j  in range (len(VAR['DEAL'])):
            index  = list(VAR['DEAL'][j].keys())[0].lower()
            tmp[index] = i[j]
        ret.append(tmp)
    type2 = VAR['DEAL'][5]['Type2'].split(':')[1].split(',')
    for i in range(len(type2)):
        type2[i] = type2[i].split('－')
    TICK=[]
    for i in range(len(ret)):
        TMP ={}
        TMP['code'] = symbol
        tmp = ret[i]['type2']
        TMP['type'] = type2[tmp-1][0]
        tmp = ret[i]['time']
        tmp =datetime.datetime.strptime(str(tmp),'%Y%m%d%H%M%S')
        TMP['date'] = tmp
        tmp = ret[i]['price'] / PriceWeight
        TMP['close'] = tmp
        tmp = ret[i]['volume']
        TMP['vol'] = tmp
        tmp = ret[i]['amount']
        TMP['amount'] = tmp
        tmp = ret[i]['positiondiff']
        TMP['仓差'] =tmp
        tmp = ret[i]['openposition']
        TMP['开仓量'] = tmp
        tmp = ret[i]['closeposition']
        TMP['平仓量'] = tmp
        TICK.append(TMP)
    z = len(TICK)
    for i in range (1,z):
        k = z-1-i
        if TICK[k]['date'] == TICK[k-1]['date']:
                TICK[k]['date'] =TICK[k]['date'] +datetime.timedelta( microseconds=80000 )
                TICK[k-1]['date']=TICK[k-1]['date'] +datetime.timedelta( microseconds=50000 )
    TICK = pd.DataFrame(TICK)
    TICK = TICK.set_index('date')
    return TICK

