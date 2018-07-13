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
        print("📊准备读取📝db🗃文件，目录位置📂%s" % (curdir + "/tdx_days"))
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
            print("📝⛓⚙️🔬📈📉📊️读取SQLLite文件{}比对数据".format(sqlLiteFile))

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
