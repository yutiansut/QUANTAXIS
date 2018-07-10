import unittest

import sys
import os
import struct
import sqlite3
import QUANTAXIS as QA
import QUANTAXIS.QAUtil.QADate as QAUtilDate
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

    t=1  1/1+1 = 0.5
    t=3  0.8/1+0.5 = 0.53333

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
            print("📊准备写入📝db🗃文件到目录📂%s" % (curdir + "/tdx_days"))
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
                s1 = "\r🚀%s %d%%[%s%s]" % (lday_fullpath, iii, "🐌" * iii, " " * (100 - iii))
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


    def testLocalTdxDayFileData(self):
        '''
        读取通达信股票数据,到 sqllite 文件中去
        :return:
        '''

        codelist = self.qa_data = QA.QA_fetch_stock_list_adv().code.tolist();

        QA.QA_fetch_stock_block_adv()
        codelist = QA.QA_fetch_stock_block_adv().get_block('云计算').code
        bockList = QA.QA_fetch_stock_block_adv()
        #data = QA.QA_fetch_stock_day_adv(codelist, '2017-09-01', '2018-05-20')

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

        lday_sh_filelist = os.listdir(self.tdxPath_SH_lday);
        sh_stock_count = len(lday_sh_filelist)
        lday_sh_filelist.sort()
        print("准备读取上海交易所证券日线数据 共{}个股票".format(sh_stock_count))
        for iIndex in range(sh_stock_count):
            print(' 进度 {}/{} '.format(iIndex, sh_stock_count));
            self.parse_a_lday_file_to_df(self.tdxPath_SH_lday + "/" + lday_sh_filelist[iIndex], lday_sh_filelist[iIndex])


        lday_sz_filelist = os.listdir(self.tdxPath_SZ_lday);
        sz_stock_count = len(lday_sz_filelist)
        lday_sz_filelist.sort()
        print("准备读取深圳交易所证券日线数据 共{}个股票".format(sz_stock_count))
        for iIndex in range(sz_stock_count):
            print(' 进度 {}/{} '.format(iIndex, sz_stock_count));
            self.parse_a_lday_file_to_df(self.tdxPath_SZ_lday + "/" + lday_sz_filelist[iIndex],lday_sz_filelist[iIndex])

    #测试mongodb 数据库， 不复权的日线数据
    def test_mongodb_day_data(self):

        #读取本地 sqllite 数据

        curdir = os.getcwd()
        print("📊准备读取📝db🗃文件，目录位置📂%s" % (curdir + "/tdx_days"))
        path_for_saved_data = curdir + "/tdx_days"
        path_for_saved_data = path_for_saved_data.rstrip("\\")
        isExists = os.path.exists(path_for_saved_data)
        if isExists == False:
            print("数据库目录不存在， 请线运行 testLocalTdxDayFileData 测试 ，获取日线数据！💔")
        #读取通达信数据库文件

        saved_sqllite_file = os.listdir(path_for_saved_data);
        sqllite_file_count = len(saved_sqllite_file)

        saved_sqllite_file.sort()

        for iIndexSQLLiteFile in range(sqllite_file_count):
            sqlLiteFile = path_for_saved_data + '/' + saved_sqllite_file[iIndexSQLLiteFile]
            print("📝⛓⚙️🔬📈📉📊️读取SQLLite文件{}比对数据".format(sqlLiteFile))

            conn = sqlite3.connect(sqlLiteFile)
            cur = conn.cursor()
            result = cur.execute('''select * from stock_days''');

            allrows = result.fetchall()

            for arow in allrows:
                print(arow)

                strCode = saved_sqllite_file[iIndexSQLLiteFile]
                isSz =  strCode.startswith('sh');
                strCode = strCode[2:8]
                isStartWith000 = strCode.startswith('000');
                intDate = arow[0];
                strDate = QAUtilDate.QA_util_date_int2str(intDate)

                if isSz == True and  isStartWith000 == True :
                    qaDataStructDay = QA.QA_quotation(code = strCode, start = strDate, end = strDate, frequence = FREQUENCE.DAY, market=MARKET_TYPE.INDEX_CN, source= DATASOURCE.MONGO,output=None  )
                else:
                    qaDataStructDay = QA.QA_quotation(code = strCode, start = strDate, end = strDate, frequence = FREQUENCE.DAY, market=MARKET_TYPE.STOCK_CN, source= DATASOURCE.MONGO,output=None  )

                #print(type(qaDataStructDay))
                vhigh = (qaDataStructDay.high).item()
                vlow =  (qaDataStructDay.low).item()
                vopen =(qaDataStructDay.open).item()
                vclose = (qaDataStructDay.close).item()
                #(qaDataStructDay.to_list())

                fopen  =  (arow[1] /100.0)
                fhigh  =  (arow[2] /100.0)
                flow   =  (arow[3] /100.0)
                fclose =  (arow[4] /100.0)

                self.assertEqual(fopen,  vopen)
                self.assertEqual(fhigh,  vhigh)
                self.assertEqual(flow,   vlow)
                self.assertEqual(fclose, vclose)

                # todo 🛠 总是有小数点误差，不能简单的用 assertEqual 去比较， 要允许一定的误差。。。

            cur.close()
            conn.close()
        #获取改天的数据对比

        pass
