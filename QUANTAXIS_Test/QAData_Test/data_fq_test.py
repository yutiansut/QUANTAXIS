import unittest

import sys
import os
import struct
import sqlite3

import pprint;

import QUANTAXIS as QA
import QUANTAXIS.QAUtil.QADate as QAUtilDate
from QUANTAXIS.QASU.save_tushare import (QA_SU_save_stock_info_tushare ,QA_SU_save_stock_terminated)
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_stock_basic_info_tushare,QA_fetch_stock_terminated)


from QUANTAXIS.QAUtil.QAParameter import FREQUENCE, MARKET_TYPE, DATASOURCE, OUTPUT_FORMAT, DATABASE_TABLE

class QAData_fq_test(unittest.TestCase):

    '''
    wind 复权算法

    定点复权公司
    Pt’= P0* ( P1/ f1(P0))* ( P2/ f2(P1))*...*( Pt-1/ ft-1(Pt-2))*(Pt/ ft(Pt-1))

    Pt’:t 点复权价
    Pt:t 点交易价
    ft(Pt-1):昨收盘价  （除权函数），是一个递归函数，如何理解递归？ft 函数自己调用自己？


    🐷注意公式的大小写

    除权函数公式， 只考虑送股
    ft(Pt-1)=(Pt-1)/(1+送股比例)

    10送10 ，除权日前一天 1元 收盘价
    ft(Pt-1)函数计算后， 1/1+1  昨天收盘价要调整为 0.5 元


    除权函数递归前复权
    Pt’=f0(...(ft+2(ft+1(Pt)))...) , ft ,t = 。。。-2，-1 ，
    (t =......-2,-1 为交易日，t=0 为设定的基准日，P0’=P0)


for example：举个🌰栗子
    一个股票每天10送10 ，股价也不涨不跌， 现实是不会发生的  🐣

    d=0        d=1       d=2        d=3        d=4
    P0=1       P1=0.5    P2=0.25    P3=0.125   P4=0.0625 😜
    f0()       f1()      f2()       f3()       f4()

    除权函数递归前复权 Pt’=f0(...(ft+2(ft+1(Pt)))...)
    (t =......-2,-1 为交易日，t=0 为设定的基准日，P0’=P0)
    复权后
    P0=0.0625  P1=0.0625 P2=0.0625  P3=0.0625  P4=0.0625 🤪

    d = 1
    P0 = 1/(1+1) = 0.5

    d = 2
    P2 = 0.25
    P1 = 0.25 /(1+1) (递归）
    P0 = 1/(1+1)  /(1+1) = 0.025   (递归）

    d = 3
    P3 = 0.125
    P2 = 0.25 / (1+1) (递归）
    P1 = 0.5 / (1+1) / (1+1) (递归）
    P0 = 1/(1+1) /(1+1) /(1+1) = 0.025   (递归）


    如何理解
    Pt’=f0(...(ft+2(ft+1(Pt)))...) , ft ,t = 。。。-2，-1 ，
    当 t = -1
    Pt' = ft+1(Pt)
        = f0(P0)

    当 t = -2
    Pt' = ft+2(ft+1(Pt))
        = f0(f1(P1))

     当 t = -3
    Pt' = ft+3(ft+2(ft+1(Pt)))
        = f0(f2(f3(P3)))

    (t =......-2,-1 为交易日，t=0 为设定的基准日，P0’=P0)

    Pt , 取值， t=-1 表示 往前复权1天， t=-2 b 表示 往前复权2天 ...
    递归 的意思是

    往前复权n天，到 t=0
    要知道 d=0 ， 先 d+1 (对应ft+1）
    先 d=1 ， 先 d+2     (对应ft+2）
    。。。
    先 d=n ， 先 d+n     (对应ft）
    因为 公式 t  = -n ... -1,

    再来看这样一个🌰栗子
    一个股票每天10送10 ，股价也不涨不跌， 现实是不会发生的  🐣

    d=0        d=1       d=2        d=3        d=4
    P0=1       P1=0.5    P2=0.25    P3=0.125   P4=0.0625 😜

    f0(P0)     f1(P0)    f2(P1)     f3(P2)     f4(P3)

    写成递归的 代入：
    d = 0 , t = 0
    基准日  P0’=P0
    ---------------------------------------------------
    站在d = 1 那天，往前复权一天, t = -1
    P0' = ft+1(Pt) = f0(P-1) = f0(P0) =  1/(1+1)=0.5  🤪P-1 表示 d=1 那天往前挪动一天P0
    ---------------------------------------------------

    站在d= 2 那天, 往前复权一天，t = -1
    P1' = ft+1(Pt) = f1(P-1) = f1(P1) = 0.5/(1+1) = 0.25
    P0' = ft+2(ft+1(Pt)) = f1(f0(P0))) =

    站在d = 2 那天, 往前复权两天，t = -2
    P0' = f0(f1(P0)) = 1/(1+1)  /(1+1) = 0.25
    ---------------------------------------------------
    一次类推。。。。

    ft函数 还需要考虑 配股 和 分红 。

   前复权:复权后价格＝[(复权前价格-现金红利)＋配(新)股价格×流通股份变动比例]÷(1＋流通股份变动比例)
   后复权:复权后价格＝复权前价格×(1＋流通股份变动比例)-配(新)股价格×流通股份变动比例＋现金红利


for example：举个🌰栗子

    送股除权报价=股权登记日收盘价/（1+每股送股比例）

    t=1  1/(1+1) = 0.5
    t=3  0.8/(1+0.5) = 0.53333

    假设 一个股票 时间

         t=0    t=1     t=2   t=3     t=4

open      1     0.5    0.6    0.7     0.53
close     1     0.6    0.7    0.8     0.6
送股      无    10送10   无    10送5    无

    用递归 计算复权价
    '''
    def testFQ(self):
        print("测试复权")
        pass
    pass



    '''
    文件名称：sh601318.day(中国平安示例)
    路径：vipdoc\sh\lday  ---上海
         vipdoc\sz\lday   ---深圳
    内容格式：
    每32个字节为一天数据
    每4个字节为一个字段，每个字段内低字节在前
    00 ~ 03 字节：年月日, 整型
    04 ~ 07 字节：开盘价*100， 整型
    08 ~ 11 字节：最高价*100,  整型
    12 ~ 15 字节：最低价*100,  整型
    16 ~ 19 字节：收盘价*100,  整型
    20 ~ 23 字节：成交额（元），float型
    24 ~ 27 字节：成交量（手），整型
    28 ~ 31 字节：上日收盘*100, 整型股
    通达信常用文件说明一览(通达信文件结构)
    '''

    def parse_a_lday_file_to_df(self, lday_fullpath, lday_fileName):
        #
        #print("读取文件 "+ lday_fullpath)

        fsize = os.path.getsize(lday_fullpath)

        if fsize % 32 != 0:
            print("💔文件长度不是 32 字节的整数倍")

        nStockCount = fsize // 32;
        print("🦖准备读取{}文件共{}个日线数据🛸".format(lday_fullpath, nStockCount))

        with open(file=lday_fullpath, mode='rb') as f:

            curdir = os.getcwd()
            print("准备写入db🗃文件到目录%s" % (curdir + "/tdx_days"))
            path_for_save_data = curdir + "/tdx_days"
            path_for_save_data = path_for_save_data.rstrip("\\")
            isExists = os.path.exists(path_for_save_data)
            if isExists == False:
                os.mkdir(path_for_save_data)
                print("新建文件夹",path_for_save_data)

            db_file_save_file = path_for_save_data
            db_file_save_file = db_file_save_file + "/" + lday_fileName + '.db'

            conn = sqlite3.connect(db_file_save_file)
            c = conn.cursor()

            c.execute('''DROP TABLE IF EXISTS stock_days''')
            c.execute(
                '''CREATE TABLE stock_days (date int, open int, high int, low int, close int, amount real, vol int,lastclose int )''')

            for iCount in range( nStockCount ):

                #进度条显示
                iii = round((iCount / nStockCount) * 100.0)
                s1 = "\r%s %d%%[%s%s]" % (lday_fullpath, iii, "🐌" * iii, " " * (100 - iii))
                sys.stdout.write(s1)
                sys.stdout.flush()

                # todo 🛠 判断，通达信本地数据是否完整！



                read_data_section = f.read(32)
                values = struct.unpack("<LLLLLfLL", read_data_section)

                c.execute(
                    "INSERT INTO stock_days(date, open, high, low, close, amount, vol ,lastclose)  "
                    " VALUES (%d,%d,%d,%d,%d,%f,%d,%d)"
                    % (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7]))


            conn.commit()
            c.close()
            conn.close()
            f.closed


    def oktestLocalTdxDayFileData(self):
        '''
        读取通达信股票数据,到 sqllite 文件中去
        :return:
        '''

        self.tdxPath_SH_lday = ''
        self.tdxPath_SZ_lday = ''

        if sys.platform == 'darwin':
            home_dir = os.path.expandvars('$HOME');
            self.tdxPath_SH_lday = home_dir + '/.wine/drive_c/new_tdx/vipdoc/sh/lday'
            self.tdxPath_SZ_lday = home_dir + '/.wine/drive_c/new_tdx/vipdoc/sz/lday'

            bExist1 = os.path.exists(self.tdxPath_SH_lday)
            bExist2 = os.path.exists(self.tdxPath_SZ_lday)

            if bExist1 == True and bExist2 == True:
                print("读取通达信 日线数据 ")
        else:
            # todo 🛠 windows 环境下 读取注册获取通达信安装位置
            print("😞请指定通达信目录💔")
            self.tdxPath_SH_lday = ''
            self.tdxPath_SZ_lday = ''
            return

        lday_sh_filelist = os.listdir(self.tdxPath_SH_lday)
        sh_stock_count = len(lday_sh_filelist)
        lday_sh_filelist.sort()
        print("准备读取上海交易所证券日线数据 共{}个股票".format(sh_stock_count))
        for iIndex in range(sh_stock_count):
            print(' 进度 {}/{} '.format(iIndex, sh_stock_count))
            self.parse_a_lday_file_to_df(self.tdxPath_SH_lday + "/" + lday_sh_filelist[iIndex], lday_sh_filelist[iIndex])


        lday_sz_filelist = os.listdir(self.tdxPath_SZ_lday)
        sz_stock_count = len(lday_sz_filelist)
        lday_sz_filelist.sort()
        print("准备读取深圳交易所证券日线数据 共{}个股票".format(sz_stock_count))
        for iIndex in range(sz_stock_count):
            print(' 进度 {}/{} '.format(iIndex, sz_stock_count))
            self.parse_a_lday_file_to_df(self.tdxPath_SZ_lday + "/" + lday_sz_filelist[iIndex],lday_sz_filelist[iIndex])



    '''
        0。 通达信盘后数据下载 从 1990年开始到今天到全部日线数据。
        0。 通达信盘后数据下载 从 1990年开始到今天到全部日线数据。
        0。 允许qunataxis save all ， 保存所有至今到数据

        测试过程
        1。 从 tushare 获取最新的股票列表，上市日期
        2。 读取通达信日线数据，
        3。 循环比较两者之间到数据，并形成报告， 
    '''




    def checkFileNameStockType(self, fileName = ''):

        '''
            检查 shXXXXXX  szXXXXXX 文件名 的证券类型


            上市状态     基金类型        编码规则（国内的公募基金产品编码都是6位数字）

            上市基金     传统封闭式      深交所：18打头  上交所：50打头

                           LOF基金

                                        深交所：16打头(前两位均用“16”标识，
                                        中间两位为中国证监会信息中心统一规定的基金管理公司代码gg，
                                        后两位为该公司发行全部开放式基金的顺序号xx。具体表示为“16ggxx”)

                           ETF基金

                                        深交所：15打头(认购代码一级市场申赎代码二级市场交易代码均相同)
                                        上交所：51打头(认购代码最后一位是数字“3”一级市场申赎代码最后一位是数字“1”二级市场交易代码最后一位是数字“0”)

                           分级基金
                                        深交所：15打头（目前所有分级基金的子代码都在深交所上市交易）

                           其他

                                        深交所：16打头（合同生效后*年内封闭运作，并在深圳证券交易所上市交易，封闭期满后转为上市开放式基金（LOF））

            非上市基金

                一般开放式

                            基金编码为6位数字，前两位为基金管理公司的注册登记机构编码(TA编码)，后四位为产品流水号。

                上证通基金

                            519***标识基金挂牌代码和申购赎回代码
                            521***标识基金的认购代码
                            522***标识跨市场转托管代码
                            523***标识设置基金分红方式代码
        '''
        isSh = fileName.startswith('sh')
        isSz = fileName.startswith('sz')

        strCode = fileName[2:8]
        if isSz == True and strCode.startswith('000') == True:
            return '上证指数'

        if isSh == True and strCode.startswith('50') == True:
            return '上交所传统封闭式基金'

        if isSz == True and strCode.startswith('18') == True:
            return '深交所传统封闭式基金'

        if isSz == True and strCode.startswith('16') == True:
            return '深交所LOF基金 '

        if isSh == True and strCode.startswith('51') == True:
            return '上交所ETF基金'

        if isSz == True and strCode.startswith('15') == True:
            return '深交所ETF基金或分级基金'

        if isSz == True and strCode.startswith('16') == True:
            return '深交所其他基金'


        if isSh == True and strCode.startswith('60') == True:
            return '上交所A股'

        if isSh == True and strCode.startswith('800')== True:
            '''
            880001 总市值
            880011 A主总值
            880021 中小总值
            880031 创业总值
            880002 流通市值
            880012 A主流通
            880022 中小流通
            880032 创业流通
            880003 平均股价
            880013 A主平均
            880023 中小平均
            880033 创业平均
            880004 成交均价
            880014 A主均价
            880024 中小均价
            880034 创业均价
            880005 涨跌家数
            880015 A主涨跌
            880025 中小涨跌
            880035 创业涨跌
            880006 停板家数
            880016 A主停板
            880026 中小停板
            880036 创业停板
            '''
            return '统计指数'

        if isSh == True and strCode.startswith('900')== True:
            return '上交所B股'

        if isSz == True and strCode.startswith('000') == True:
            return '深交所主板'

        if isSz == True and strCode.startswith('002') == True:
            return '深交所中小板'

        if isSz == True and strCode.startswith('200') == True:
            return '深交所B股'

        if isSz == True and strCode.startswith('300') == True:
            return '深交所创业板'

        if isSz == True and strCode.startswith('399') == True:
            return '深交所指数'


    #测试mongodb 数据库， 不复权的日线数据
    def test_mongodb_day_data(self):

        #读取本地tdx日线数据 到 sqllite数据
        #self.oktestLocalTdxDayFileData()

        #更新股票列表
        QA_SU_save_stock_info_tushare() # 只有主版 创业板 中小板, 不包含已经退市的股票
        #QA_SU_save_stock_terminated() # 获取退市股票列表
        #
        stock_list = QA_fetch_stock_basic_info_tushare()
        stock_list.sort(key=lambda k: (k.get('code')))

        #stock_list_termined = QA_fetch_stock_terminated()

        #sorted(stock_list, key='code')

        curdir = os.getcwd()
        print("准备读取db🗃文件，目录位置%s" % (curdir + "/tdx_days"))
        path_for_saved_data = curdir + "/tdx_days"
        path_for_saved_data = path_for_saved_data.rstrip("\\")
        isExists = os.path.exists(path_for_saved_data)
        if isExists == False:
            print("数据库目录不存在， 请线运行 testLocalTdxDayFileData 测试 ，获取日线数据！💔")
        #读取通达信数据库文件

        saved_sqllite_files = os.listdir(path_for_saved_data);
        sqllite_file_count = len(saved_sqllite_files)

        saved_sqllite_files.sort()

        #检查 Tushare 获取的股票列表 和 通达信保存的股票列表是否一致。
        for aSavedFileName in saved_sqllite_files:
            bFound = False
            for iRow in stock_list:
                strCodeInDb = iRow.get('code')
                strCodeOnFileName = aSavedFileName[2:8]
                if strCodeInDb == strCodeOnFileName:
                    bFound = True
                    break

            if bFound == False:
                if (self.checkFileNameStockType(aSavedFileName) == '上交所A股') or \
                        (self.checkFileNameStockType(aSavedFileName) == '深交所中小板') or \
                        (self.checkFileNameStockType(aSavedFileName) == '深交所创业板'):

                    #从退市的股票列表中找
                    # bIsTerminatedStock = False
                    # for iTerminatedStock in stock_list_termined:
                    #     terminatedCode = iTerminatedStock.get('code')
                    #     strCode0 = aSavedFileName[2:8]
                    #     if terminatedCode == strCode0:
                    #         bIsTerminatedStock = True
                    #         continue
                    #if bIsTerminatedStock == True:
                    #    continue
                    # hard code 已经退市的股票
                    if aSavedFileName[2:8] == '600432' or \
                            aSavedFileName[2:8] == '600806':
                        continue

                    print("💔通达信数据下载不全， 没有找到 股票代码 ", aSavedFileName)
                    self.fail("💔通达信数据下载不全， 没有找到 股票代码 {}".format(aSavedFileName))
                    break
            else:
                    continue

        for iIndexSQLLiteFile in range(sqllite_file_count):
            strSavedFileName = saved_sqllite_files[iIndexSQLLiteFile];
            strCodeType = self.checkFileNameStockType(strSavedFileName)
            if strCodeType == '上交所A股' or \
                    strCodeType == '深交所中小板' or \
                    strCodeType == '深交所创业板':
                pass
            else:
                continue

            sqlLiteFile = path_for_saved_data + '/' + strSavedFileName
            print("⛓⚙️🔬📈📉️读取SQLLite文件{}比对数据".format(sqlLiteFile))

            conn = sqlite3.connect(sqlLiteFile)
            cur = conn.cursor()
            result = cur.execute('''select * from stock_days''')

            allrows = result.fetchall()

            for arow in allrows:

                strCode = strSavedFileName[2:8]
                intDate = arow[0]
                strDate = QAUtilDate.QA_util_date_int2str(intDate)

                if strCodeType == '上交所A股' or \
                    strCodeType == '深交所中小板' or \
                    strCodeType == '深交所创业板':                # if isSz == True and  isStartWith000 == True :
                        qaDataStructDay = QA.QA_quotation(code = strCode, start = strDate, end = strDate, frequence = FREQUENCE.DAY, market=MARKET_TYPE.STOCK_CN, source= DATASOURCE.MONGO,output=None  )
                else:
                    print("证券 类型不明确！")
                    break
                #对比其他 指数 基金 报价

                #print(type(qaDataStructDay))
                try:
                    vhigh = (qaDataStructDay.high).item()
                    vlow =  (qaDataStructDay.low).item()
                    vopen = (qaDataStructDay.open).item()
                    vclose = (qaDataStructDay.close).item()
                except :

                    print("error ")
                    print(arow)
                    print("数据库读取记录错误")

                #(qaDataStructDay.to_list())

                fopen  =  (arow[1] /100.0)
                fhigh  =  (arow[2] /100.0)
                flow   =  (arow[3] /100.0)
                fclose =  (arow[4] /100.0)

                bShowErro = True

                if fopen != vopen:
                    print(arow)
                    print(fopen, " 开盘价不匹配 ", vopen )

                    if abs(fopen-vopen)>10.0 :
                        self.fail('误差超过范围')

                if fhigh != vhigh:
                    print(arow)
                    print(fhigh, " 最高价不匹配 ",vhigh)

                    if abs(fopen - vopen) > 10.0:
                        self.fail('误差超过范围')

                if flow !=  vlow:
                    print(arow)
                    print(flow, " 最低价不匹配 ", vlow)

                    if abs(fopen - vopen) > 10.0:
                        self.fail('误差超过范围')

                if fclose != vclose:
                    print(arow)
                    print(fclose , " 收盘价不匹配 ", vclose)

                    if abs(fopen - vopen) > 10.0:
                        self.fail('误差超过范围')

                # self.assertEqual(fopen,  vopen)
                # self.assertEqual(fhigh,  vhigh)
                # self.assertEqual(flow,   vlow)
                # self.assertEqual(fclose, vclose)

                # todo 🛠 总是有小数点误差，不能简单的用 assertEqual 去比较， 要允许一定的误差。。。

            cur.close()
            conn.close()
        #获取改天的数据对比

        pass

''''
Testing started at 7:17 PM ...
/Users/jerryw/MyCode/QUANTAXIS/quantaxis_env/bin/python /Applications/PyCharm.app/Contents/helpers/pydev/pydevd.py --multiproc --qt-support=auto --client 127.0.0.1 --port 56088 --file /Applications/PyCharm.app/Contents/helpers/pycharm/_jb_unittest_runner.py --target data_fq_test.QAData_fq_test.test_mongodb_day_data
pydev debugger: process 18270 is connecting

Connected to pydev debugger (build 181.5087.37)
Launching unittests with arguments python -m unittest data_fq_test.QAData_fq_test.test_mongodb_day_data in /Users/jerryw/MyCode/QUANTAXIS/QUANTAXIS_Test/QAData_Test

QUANTAXIS>> start QUANTAXIS
QUANTAXIS>> Expand macros in /Users/jerryw/MyCode/QUANTAXIS/quantaxis_env/lib/python3.6/site-packages/macropy/core/hquotes.py
QUANTAXIS>> Finding macros in 'macropy.core.hquotes'
QUANTAXIS>> Importing macros from 'macropy.core.quotes' into 'macropy.core.hquotes'
QUANTAXIS>> Expand macros in /Users/jerryw/MyCode/QUANTAXIS/quantaxis_env/lib/python3.6/site-packages/macropy/core/quotes.py
QUANTAXIS>> Finding macros in 'macropy.core.quotes'
QUANTAXIS>> Expand macros in /Users/jerryw/MyCode/QUANTAXIS/quantaxis_env/lib/python3.6/site-packages/macropy/core/failure.py
QUANTAXIS>> Finding macros in 'macropy.core.failure'
QUANTAXIS>> Importing macros from 'macropy.core.hquotes' into 'macropy.core.failure'
QUANTAXIS>> Expand macros in /Users/jerryw/MyCode/QUANTAXIS/quantaxis_env/lib/python3.6/site-packages/cffi/api.py
QUANTAXIS>> Finding macros in 'cffi.api'
no display found. Using non-interactive Agg backend
if you use ssh, you can use ssh with -X parmas to avoid this issue
QUANTAXIS>> Expand macros in /Users/jerryw/MyCode/QUANTAXIS/quantaxis_env/lib/python3.6/site-packages/scipy/__config__.py
QUANTAXIS>> Finding macros in 'scipy.__config__'
QUANTAXIS>> Welcome to QUANTAXIS, the Version is 1.0.64
QUANTAXIS>>  
 ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
  ``########`````##````````##``````````##`````````####````````##```##########````````#``````##``````###```##`````######`` 
  `##``````## ```##````````##`````````####````````##`##```````##```````##```````````###``````##````##`````##```##`````##` 
  ##````````##```##````````##````````##`##````````##``##``````##```````##``````````####```````#```##``````##```##``````## 
  ##````````##```##````````##```````##```##```````##```##`````##```````##`````````##`##```````##`##```````##````##``````` 
  ##````````##```##````````##``````##`````##``````##````##````##```````##````````##``###```````###````````##`````##`````` 
  ##````````##```##````````##``````##``````##`````##`````##```##```````##```````##````##```````###````````##``````###```` 
  ##````````##```##````````##`````##````````##````##``````##``##```````##``````##``````##`````##`##```````##````````##``` 
  ##````````##```##````````##````#############````##```````##`##```````##`````###########`````##``##``````##`````````##`` 
  ###```````##```##````````##```##```````````##```##```````##`##```````##````##`````````##```##```##``````##```##`````##` 
  `##``````###````##``````###``##`````````````##``##````````####```````##```##``````````##``###````##`````##````##`````## 
  ``#########``````########```##``````````````###`##``````````##```````##``##````````````##`##``````##````##`````###``### 
  ````````#####`````````````````````````````````````````````````````````````````````````````````````````````````````##``  
  ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
  ``````````````````````````Copyright``yutiansut``2018``````QUANTITATIVE FINANCIAL FRAMEWORK````````````````````````````` 
  ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
 ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
 ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
 
 Get stock info from tushare,stock count is 3533
/Users/jerryw/MyCode/QUANTAXIS/QUANTAXIS/QASU/save_tushare.py:142: DeprecationWarning: insert is deprecated. Use insert_one or insert_many instead.
  coll.insert(json_data)
 Save data to stock_info_tushare collection， OK
准备读取db🗃文件，目录位置/Users/jerryw/MyCode/QUANTAXIS/QUANTAXIS_Test/QAData_Test/tdx_days
⛓⚙️🔬📈📉️读取SQLLite文件/Users/jerryw/MyCode/QUANTAXIS/QUANTAXIS_Test/QAData_Test/tdx_days/sh600000.day.db比对数据
/Users/jerryw/MyCode/QUANTAXIS/QUANTAXIS/QAFetch/QAQuery.py:68: DeprecationWarning: 
.ix is deprecated. Please use
.loc for label based indexing or
.iloc for positional indexing

See the documentation here:
http://pandas.pydata.org/pandas-docs/stable/indexing.html#ix-indexer-is-deprecated
  res = res.ix[:, ['code', 'open', 'high', 'low',
 Error QA_fetch_stock_day_adv parameter code=600000 , start=2001-06-25, end=2001-06-25 call QA_fetch_stock_day return None
error 
(20010625, 2025, 2030, 2005, 2021, 19141800.0, 949300, 2021)
数据库读取记录错误
(20010625, 2025, 2030, 2005, 2021, 19141800.0, 949300, 2021)
20.25  开盘价不匹配  20.17
(20010625, 2025, 2030, 2005, 2021, 19141800.0, 949300, 2021)
20.3  最高价不匹配  20.23
 Error QA_fetch_stock_day_adv parameter code=600000 , start=2001-08-16, end=2001-08-16 call QA_fetch_stock_day return None
error 
(20010816, 1588, 1595, 1560, 1564, 9489000.0, 600700, 1588)
数据库读取记录错误
(20010816, 1588, 1595, 1560, 1564, 9489000.0, 600700, 1588)
15.88  开盘价不匹配  15.92
(20010816, 1588, 1595, 1560, 1564, 9489000.0, 600700, 1588)
15.6  最低价不匹配  15.8
(20010816, 1588, 1595, 1560, 1564, 9489000.0, 600700, 1588)
15.64  收盘价不匹配  15.88
(20020131, 1451, 1451, 1380, 1414, 73053408.0, 5164800, 1319)
14.14  收盘价不匹配  14.11
(20020806, 1710, 1748, 1710, 1734, 23833430.0, 1375739, 1722)
17.34  收盘价不匹配  17.31
(20030827, 1050, 1050, 1027, 1032, 35389780.0, 3419950, 1035)
10.32  收盘价不匹配  10.33
 Error QA_fetch_stock_day_adv parameter code=600000 , start=2018-07-06, end=2018-07-06 call QA_fetch_stock_day return None
error 
(20180706, 931, 943, 917, 937, 210564112.0, 22594443, 65536)
数据库读取记录错误
(20180706, 931, 943, 917, 937, 210564112.0, 22594443, 65536)
9.31  开盘价不匹配  9.26
(20180706, 931, 943, 917, 937, 210564112.0, 22594443, 65536)
9.43  最高价不匹配  9.35
(20180706, 931, 943, 917, 937, 210564112.0, 22594443, 65536)
9.17  最低价不匹配  9.22
(20180706, 931, 943, 917, 937, 210564112.0, 22594443, 65536)
9.37  收盘价不匹配  9.26
 Error QA_fetch_stock_day_adv parameter code=600000 , start=2018-07-09, end=2018-07-09 call QA_fetch_stock_day return None
error 
(20180709, 937, 963, 937, 960, 212109328.0, 22172565, 65536)
数据库读取记录错误
(20180709, 937, 963, 937, 960, 212109328.0, 22172565, 65536)
9.37  开盘价不匹配  9.26
(20180709, 937, 963, 937, 960, 212109328.0, 22172565, 65536)
9.63  最高价不匹配  9.35
(20180709, 937, 963, 937, 960, 212109328.0, 22172565, 65536)
9.37  最低价不匹配  9.22
(20180709, 937, 963, 937, 960, 212109328.0, 22172565, 65536)
9.6  收盘价不匹配  9.26
 Error QA_fetch_stock_day_adv parameter code=600000 , start=2018-07-10, end=2018-07-10 call QA_fetch_stock_day return None
error 
(20180710, 961, 965, 950, 957, 118668136.0, 12402837, 65536)
数据库读取记录错误
(20180710, 961, 965, 950, 957, 118668136.0, 12402837, 65536)
9.61  开盘价不匹配  9.26
(20180710, 961, 965, 950, 957, 118668136.0, 12402837, 65536)
9.65  最高价不匹配  9.35
(20180710, 961, 965, 950, 957, 118668136.0, 12402837, 65536)
9.5  最低价不匹配  9.22
(20180710, 961, 965, 950, 957, 118668136.0, 12402837, 65536)
9.57  收盘价不匹配  9.26
⛓⚙️🔬📈📉️读取SQLLite文件/Users/jerryw/MyCode/QUANTAXIS/QUANTAXIS_Test/QAData_Test/tdx_days/sh600004.day.db比对数据
(20030715, 912, 925, 908, 916, 52158256.0, 5684894, 913)
9.16  收盘价不匹配  9.17
 Error QA_fetch_stock_day_adv parameter code=600004 , start=2018-07-06, end=2018-07-06 call QA_fetch_stock_day return None
error 
(20180706, 1295, 1344, 1282, 1327, 209779264.0, 15927074, 65536)
数据库读取记录错误
(20180706, 1295, 1344, 1282, 1327, 209779264.0, 15927074, 65536)
12.95  开盘价不匹配  13.2
(20180706, 1295, 1344, 1282, 1327, 209779264.0, 15927074, 65536)
13.44  最高价不匹配  13.33
(20180706, 1295, 1344, 1282, 1327, 209779264.0, 15927074, 65536)
12.82  最低价不匹配  12.86
(20180706, 1295, 1344, 1282, 1327, 209779264.0, 15927074, 65536)
13.27  收盘价不匹配  12.93
 Error QA_fetch_stock_day_adv parameter code=600004 , start=2018-07-09, end=2018-07-09 call QA_fetch_stock_day return None
error 
(20180709, 1330, 1410, 1321, 1395, 210136768.0, 15306820, 65536)
数据库读取记录错误
(20180709, 1330, 1410, 1321, 1395, 210136768.0, 15306820, 65536)
13.3  开盘价不匹配  13.2
(20180709, 1330, 1410, 1321, 1395, 210136768.0, 15306820, 65536)
14.1  最高价不匹配  13.33
(20180709, 1330, 1410, 1321, 1395, 210136768.0, 15306820, 65536)
13.21  最低价不匹配  12.86
(20180709, 1330, 1410, 1321, 1395, 210136768.0, 15306820, 65536)
13.95  收盘价不匹配  12.93
 Error QA_fetch_stock_day_adv parameter code=600004 , start=2018-07-10, end=2018-07-10 call QA_fetch_stock_day return None
error 
(20180710, 1399, 1465, 1399, 1428, 288483008.0, 20118802, 65536)
数据库读取记录错误
(20180710, 1399, 1465, 1399, 1428, 288483008.0, 20118802, 65536)
13.99  开盘价不匹配  13.2
(20180710, 1399, 1465, 1399, 1428, 288483008.0, 20118802, 65536)
14.65  最高价不匹配  13.33
(20180710, 1399, 1465, 1399, 1428, 288483008.0, 20118802, 65536)
13.99  最低价不匹配  12.86
(20180710, 1399, 1465, 1399, 1428, 288483008.0, 20118802, 65536)
14.28  收盘价不匹配  12.93
⛓⚙️🔬📈📉️读取SQLLite文件/Users/jerryw/MyCode/QUANTAXIS/QUANTAXIS_Test/QAData_Test/tdx_days/sh600006.day.db比对数据
 Error QA_fetch_stock_day_adv parameter code=600006 , start=2001-06-25, end=2001-06-25 call QA_fetch_stock_day return None
error 
(20010625, 983, 1005, 983, 1005, 39266808.0, 3935300, 988)
数据库读取记录错误
(20010625, 983, 1005, 983, 1005, 39266808.0, 3935300, 988)
9.83  开盘价不匹配  9.81
(20010625, 983, 1005, 983, 1005, 39266808.0, 3935300, 988)
10.05  最高价不匹配  9.88
(20010625, 983, 1005, 983, 1005, 39266808.0, 3935300, 988)
9.83  最低价不匹配  9.81
(20010625, 983, 1005, 983, 1005, 39266808.0, 3935300, 988)
10.05  收盘价不匹配  9.88
 Error QA_fetch_stock_day_adv parameter code=600006 , start=2001-08-16, end=2001-08-16 call QA_fetch_stock_day return None
error 
(20010816, 1006, 1006, 980, 980, 8620000.0, 870500, 1000)
数据库读取记录错误
(20010816, 1006, 1006, 980, 980, 8620000.0, 870500, 1000)
10.06  开盘价不匹配  10.2
(20010816, 1006, 1006, 980, 980, 8620000.0, 870500, 1000)
10.06  最高价不匹配  10.22
(20010816, 1006, 1006, 980, 980, 8620000.0, 870500, 1000)
9.8  最低价不匹配  9.95
(20010816, 1006, 1006, 980, 980, 8620000.0, 870500, 1000)
9.8  收盘价不匹配  10.0
(20020806, 1313, 1328, 1312, 1325, 5930199.0, 450201, 1317)
13.28  最高价不匹配  13.24
(20020806, 1313, 1328, 1312, 1325, 5930199.0, 450201, 1317)
13.25  收盘价不匹配  13.24
(20031009, 1096, 1098, 1090, 1093, 8070513.0, 738233, 1099)
10.93  收盘价不匹配  10.94
(20031013, 1081, 1110, 1070, 1084, 2748873.0, 252331, 1094)
10.84  收盘价不匹配  10.9
 Error QA_fetch_stock_day_adv parameter code=600006 , start=2018-07-06, end=2018-07-06 call QA_fetch_stock_day return None
error 
(20180706, 383, 390, 376, 387, 24013064.0, 6237196, 65536)
数据库读取记录错误
(20180706, 383, 390, 376, 387, 24013064.0, 6237196, 65536)
3.83  开盘价不匹配  3.94
(20180706, 383, 390, 376, 387, 24013064.0, 6237196, 65536)
3.9  最高价不匹配  3.96
(20180706, 383, 390, 376, 387, 24013064.0, 6237196, 65536)
3.76  最低价不匹配  3.81
(20180706, 383, 390, 376, 387, 24013064.0, 6237196, 65536)
3.87  收盘价不匹配  3.82
 Error QA_fetch_stock_day_adv parameter code=600006 , start=2018-07-09, end=2018-07-09 call QA_fetch_stock_day return None
error 
(20180709, 387, 395, 386, 395, 22124384.0, 5653076, 65536)
数据库读取记录错误
(20180709, 387, 395, 386, 395, 22124384.0, 5653076, 65536)
3.87  开盘价不匹配  3.94
(20180709, 387, 395, 386, 395, 22124384.0, 5653076, 65536)
3.95  最高价不匹配  3.96
(20180709, 387, 395, 386, 395, 22124384.0, 5653076, 65536)
3.86  最低价不匹配  3.81
(20180709, 387, 395, 386, 395, 22124384.0, 5653076, 65536)
3.95  收盘价不匹配  3.82
 Error QA_fetch_stock_day_adv parameter code=600006 , start=2018-07-10, end=2018-07-10 call QA_fetch_stock_day return None
error 
(20180710, 392, 397, 391, 395, 12712953.0, 3225950, 65536)
数据库读取记录错误
(20180710, 392, 397, 391, 395, 12712953.0, 3225950, 65536)
3.92  开盘价不匹配  3.94
(20180710, 392, 397, 391, 395, 12712953.0, 3225950, 65536)
3.97  最高价不匹配  3.96
(20180710, 392, 397, 391, 395, 12712953.0, 3225950, 65536)
3.91  最低价不匹配  3.81
(20180710, 392, 397, 391, 395, 12712953.0, 3225950, 65536)
3.95  收盘价不匹配  3.82
⛓⚙️🔬📈📉️读取SQLLite文件/Users/jerryw/MyCode/QUANTAXIS/QUANTAXIS_Test/QAData_Test/tdx_days/sh600007.day.db比对数据
 Error QA_fetch_stock_day_adv parameter code=600007 , start=2001-06-25, end=2001-06-25 call QA_fetch_stock_day return None
error 
(20010625, 1225, 1238, 1215, 1236, 11407816.0, 931000, 1223)
数据库读取记录错误
(20010625, 1225, 1238, 1215, 1236, 11407816.0, 931000, 1223)
12.25  开盘价不匹配  12.05
(20010625, 1225, 1238, 1215, 1236, 11407816.0, 931000, 1223)
12.38  最高价不匹配  12.25
(20010625, 1225, 1238, 1215, 1236, 11407816.0, 931000, 1223)
12.15  最低价不匹配  12.05
(20010625, 1225, 1238, 1215, 1236, 11407816.0, 931000, 1223)
12.36  收盘价不匹配  12.23
 Error QA_fetch_stock_day_adv parameter code=600007 , start=2001-08-16, end=2001-08-16 call QA_fetch_stock_day return None
error 
(20010816, 1110, 1110, 1086, 1087, 4842000.0, 442300, 1103)
数据库读取记录错误
(20010816, 1110, 1110, 1086, 1087, 4842000.0, 442300, 1103)
11.1  开盘价不匹配  10.97
(20010816, 1110, 1110, 1086, 1087, 4842000.0, 442300, 1103)
11.1  最高价不匹配  11.08
(20010816, 1110, 1110, 1086, 1087, 4842000.0, 442300, 1103)
10.86  最低价不匹配  10.96
(20010816, 1110, 1110, 1086, 1087, 4842000.0, 442300, 1103)
10.87  收盘价不匹配  11.03
(20030716, 679, 685, 672, 678, 1683282.0, 248910, 679)
6.78  收盘价不匹配  6.79
(20031009, 650, 652, 633, 634, 2022967.0, 314300, 648)
6.34  收盘价不匹配  6.35
 Error QA_fetch_stock_day_adv parameter code=600007 , start=2018-07-06, end=2018-07-06 call QA_fetch_stock_day return None
error 
(20180706, 1385, 1412, 1376, 1405, 5784274.0, 415398, 65536)
数据库读取记录错误
(20180706, 1385, 1412, 1376, 1405, 5784274.0, 415398, 65536)
13.85  开盘价不匹配  14.23
(20180706, 1385, 1412, 1376, 1405, 5784274.0, 415398, 65536)
14.12  最高价不匹配  14.27
(20180706, 1385, 1412, 1376, 1405, 5784274.0, 415398, 65536)
13.76  最低价不匹配  13.75
(20180706, 1385, 1412, 1376, 1405, 5784274.0, 415398, 65536)
14.05  收盘价不匹配  13.85
 Error QA_fetch_stock_day_adv parameter code=600007 , start=2018-07-09, end=2018-07-09 call QA_fetch_stock_day return None
error 
(20180709, 1409, 1440, 1394, 1435, 7855905.0, 550900, 65536)
数据库读取记录错误
(20180709, 1409, 1440, 1394, 1435, 7855905.0, 550900, 65536)
14.09  开盘价不匹配  14.23
(20180709, 1409, 1440, 1394, 1435, 7855905.0, 550900, 65536)
14.4  最高价不匹配  14.27
(20180709, 1409, 1440, 1394, 1435, 7855905.0, 550900, 65536)
13.94  最低价不匹配  13.75
(20180709, 1409, 1440, 1394, 1435, 7855905.0, 550900, 65536)
14.35  收盘价不匹配  13.85
 Error QA_fetch_stock_day_adv parameter code=600007 , start=2018-07-10, end=2018-07-10 call QA_fetch_stock_day return None
error 
(20180710, 1435, 1443, 1426, 1431, 4082487.0, 284800, 65536)
数据库读取记录错误
(20180710, 1435, 1443, 1426, 1431, 4082487.0, 284800, 65536)
14.35  开盘价不匹配  14.23
(20180710, 1435, 1443, 1426, 1431, 4082487.0, 284800, 65536)
14.43  最高价不匹配  14.27
(20180710, 1435, 1443, 1426, 1431, 4082487.0, 284800, 65536)
14.26  最低价不匹配  13.75
(20180710, 1435, 1443, 1426, 1431, 4082487.0, 284800, 65536)
14.31  收盘价不匹配  13.85
⛓⚙️🔬📈📉️读取SQLLite文件/Users/jerryw/MyCode/QUANTAXIS/QUANTAXIS_Test/QAData_Test/tdx_days/sh600008.day.db比对数据
 Error QA_fetch_stock_day_adv parameter code=600008 , start=2001-06-25, end=2001-06-25 call QA_fetch_stock_day return None
error 
(20010625, 2050, 2080, 2022, 2055, 36964504.0, 1802600, 2040)
数据库读取记录错误
(20010625, 2050, 2080, 2022, 2055, 36964504.0, 1802600, 2040)
20.5  开盘价不匹配  20.19
(20010625, 2050, 2080, 2022, 2055, 36964504.0, 1802600, 2040)
20.8  最高价不匹配  20.64
(20010625, 2050, 2080, 2022, 2055, 36964504.0, 1802600, 2040)
20.22  最低价不匹配  20.18
(20010625, 2050, 2080, 2022, 2055, 36964504.0, 1802600, 2040)
20.55  收盘价不匹配  20.4
 Error QA_fetch_stock_day_adv parameter code=600008 , start=2001-08-16, end=2001-08-16 call QA_fetch_stock_day return None
error 
(20010816, 1861, 1861, 1799, 1810, 17556000.0, 965700, 1850)
数据库读取记录错误
(20010816, 1861, 1861, 1799, 1810, 17556000.0, 965700, 1850)
18.61  开盘价不匹配  18.3
(20010816, 1861, 1861, 1799, 1810, 17556000.0, 965700, 1850)
18.61  最高价不匹配  18.62
(20010816, 1861, 1861, 1799, 1810, 17556000.0, 965700, 1850)
17.99  最低价不匹配  18.2
(20010816, 1861, 1861, 1799, 1810, 17556000.0, 965700, 1850)
18.1  收盘价不匹配  18.5
(20020806, 1366, 1386, 1349, 1374, 12038486.0, 880351, 1369)
13.74  收盘价不匹配  13.75
(20030715, 1098, 1098, 1080, 1094, 8865431.0, 814947, 1086)
10.94  收盘价不匹配  10.93
 Error QA_fetch_stock_day_adv parameter code=600008 , start=2018-07-06, end=2018-07-06 call QA_fetch_stock_day return None
error 
(20180706, 418, 420, 410, 418, 55594440.0, 13370113, 65536)
数据库读取记录错误
(20180706, 418, 420, 410, 418, 55594440.0, 13370113, 65536)
4.2  最高价不匹配  4.22
(20180706, 418, 420, 410, 418, 55594440.0, 13370113, 65536)
4.1  最低价不匹配  4.13
(20180706, 418, 420, 410, 418, 55594440.0, 13370113, 65536)
4.18  收盘价不匹配  4.19
 Error QA_fetch_stock_day_adv parameter code=600008 , start=2018-07-09, end=2018-07-09 call QA_fetch_stock_day return None
error 
(20180709, 420, 423, 418, 421, 52399204.0, 12461261, 65536)
数据库读取记录错误
(20180709, 420, 423, 418, 421, 52399204.0, 12461261, 65536)
4.2  开盘价不匹配  4.18
(20180709, 420, 423, 418, 421, 52399204.0, 12461261, 65536)
4.23  最高价不匹配  4.22
(20180709, 420, 423, 418, 421, 52399204.0, 12461261, 65536)
4.18  最低价不匹配  4.13
(20180709, 420, 423, 418, 421, 52399204.0, 12461261, 65536)
4.21  收盘价不匹配  4.19
 Error QA_fetch_stock_day_adv parameter code=600008 , start=2018-07-10, end=2018-07-10 call QA_fetch_stock_day return None
error 
(20180710, 422, 425, 418, 422, 49840248.0, 11830708, 65536)
数据库读取记录错误
(20180710, 422, 425, 418, 422, 49840248.0, 11830708, 65536)
4.22  开盘价不匹配  4.18
(20180710, 422, 425, 418, 422, 49840248.0, 11830708, 65536)
4.25  最高价不匹配  4.22
(20180710, 422, 425, 418, 422, 49840248.0, 11830708, 65536)
4.18  最低价不匹配  4.13
(20180710, 422, 425, 418, 422, 49840248.0, 11830708, 65536)
4.22  收盘价不匹配  4.19
⛓⚙️🔬📈📉️读取SQLLite文件/Users/jerryw/MyCode/QUANTAXIS/QUANTAXIS_Test/QAData_Test/tdx_days/sh600009.day.db比对数据
 Error QA_fetch_stock_day_adv parameter code=600009 , start=2001-06-25, end=2001-06-25 call QA_fetch_stock_day return None
error 
(20010625, 1040, 1048, 1035, 1048, 27798452.0, 2666400, 1037)
数据库读取记录错误
(20010625, 1040, 1048, 1035, 1048, 27798452.0, 2666400, 1037)
10.4  开盘价不匹配  10.2
(20010625, 1040, 1048, 1035, 1048, 27798452.0, 2666400, 1037)
10.48  最高价不匹配  10.4
(20010625, 1040, 1048, 1035, 1048, 27798452.0, 2666400, 1037)
10.35  最低价不匹配  10.19
(20010625, 1040, 1048, 1035, 1048, 27798452.0, 2666400, 1037)
10.48  收盘价不匹配  10.37
 Error QA_fetch_stock_day_adv parameter code=600009 , start=2001-08-16, end=2001-08-16 call QA_fetch_stock_day return None
error 
(20010816, 920, 922, 910, 911, 3601000.0, 394800, 919)
数据库读取记录错误
(20010816, 920, 922, 910, 911, 3601000.0, 394800, 919)
9.2  开盘价不匹配  9.14
(20010816, 920, 922, 910, 911, 3601000.0, 394800, 919)
9.22  最高价不匹配  9.24
(20010816, 920, 922, 910, 911, 3601000.0, 394800, 919)
9.1  最低价不匹配  9.13
(20010816, 920, 922, 910, 911, 3601000.0, 394800, 919)
9.11  收盘价不匹配  9.19
(20030715, 1130, 1154, 1129, 1143, 103606064.0, 9040788, 1130)
11.43  收盘价不匹配  11.44
 Error QA_fetch_stock_day_adv parameter code=600009 , start=2018-07-06, end=2018-07-06 call QA_fetch_stock_day return None
error 
(20180706, 5738, 5755, 5483, 5589, 264316880.0, 4734517, 65536)
数据库读取记录错误
(20180706, 5738, 5755, 5483, 5589, 264316880.0, 4734517, 65536)
57.38  开盘价不匹配  57.1
(20180706, 5738, 5755, 5483, 5589, 264316880.0, 4734517, 65536)
57.55  最高价不匹配  57.93
(20180706, 5738, 5755, 5483, 5589, 264316880.0, 4734517, 65536)
54.83  最低价不匹配  55.91
(20180706, 5738, 5755, 5483, 5589, 264316880.0, 4734517, 65536)
55.89  收盘价不匹配  57.38
 Error QA_fetch_stock_day_adv parameter code=600009 , start=2018-07-09, end=2018-07-09 call QA_fetch_stock_day return None
error 
(20180709, 5680, 5718, 5608, 5704, 238465936.0, 4201977, 65536)
数据库读取记录错误
(20180709, 5680, 5718, 5608, 5704, 238465936.0, 4201977, 65536)
56.8  开盘价不匹配  57.1
(20180709, 5680, 5718, 5608, 5704, 238465936.0, 4201977, 65536)
57.18  最高价不匹配  57.93
(20180709, 5680, 5718, 5608, 5704, 238465936.0, 4201977, 65536)
56.08  最低价不匹配  55.91
(20180709, 5680, 5718, 5608, 5704, 238465936.0, 4201977, 65536)
57.04  收盘价不匹配  57.38
 Error QA_fetch_stock_day_adv parameter code=600009 , start=2018-07-10, end=2018-07-10 call QA_fetch_stock_day return None
error 
(20180710, 5705, 6020, 5705, 6018, 471883008.0, 7931726, 65536)
数据库读取记录错误
(20180710, 5705, 6020, 5705, 6018, 471883008.0, 7931726, 65536)
57.05  开盘价不匹配  57.1
(20180710, 5705, 6020, 5705, 6018, 471883008.0, 7931726, 65536)
60.2  最高价不匹配  57.93
(20180710, 5705, 6020, 5705, 6018, 471883008.0, 7931726, 65536)
57.05  最低价不匹配  55.91
(20180710, 5705, 6020, 5705, 6018, 471883008.0, 7931726, 65536)
60.18  收盘价不匹配  57.38
⛓⚙️🔬📈📉️读取SQLLite文件/Users/jerryw/MyCode/QUANTAXIS/QUANTAXIS_Test/QAData_Test/tdx_days/sh600010.day.db比对数据
 Error QA_fetch_stock_day_adv parameter code=600010 , start=2001-06-25, end=2001-06-25 call QA_fetch_stock_day return None
error 
(20010625, 725, 740, 723, 728, 69837312.0, 9539700, 723)
数据库读取记录错误
(20010625, 725, 740, 723, 728, 69837312.0, 9539700, 723)
7.25  开盘价不匹配  7.15
(20010625, 725, 740, 723, 728, 69837312.0, 9539700, 723)
7.4  最高价不匹配  7.28
(20010625, 725, 740, 723, 728, 69837312.0, 9539700, 723)
7.23  最低价不匹配  7.1
(20010625, 725, 740, 723, 728, 69837312.0, 9539700, 723)
7.28  收盘价不匹配  7.23
 Error QA_fetch_stock_day_adv parameter code=600010 , start=2001-08-16, end=2001-08-16 call QA_fetch_stock_day return None
error 
(20010816, 656, 657, 645, 645, 6574000.0, 1015100, 656)
数据库读取记录错误
(20010816, 656, 657, 645, 645, 6574000.0, 1015100, 656)
6.56  开盘价不匹配  6.6
(20010816, 656, 657, 645, 645, 6574000.0, 1015100, 656)
6.57  最高价不匹配  6.6
(20010816, 656, 657, 645, 645, 6574000.0, 1015100, 656)
6.45  最低价不匹配  6.49
(20010816, 656, 657, 645, 645, 6574000.0, 1015100, 656)
6.45  收盘价不匹配  6.56
(20030715, 515, 527, 515, 519, 23051868.0, 4419021, 516)
5.19  收盘价不匹配  5.2
(20060216, 283, 284, 270, 270, 147228384.0, 53646967, 283)
2.7  收盘价不匹配  2.71

'''