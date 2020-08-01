# coding:utf-8
#
# The MIT License (MIT)
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
#
# Author: 604829050@qq.com
# Date: 2018-05-11
# Description: Unit test for the fetch data
import unittest

import fnmatch
import os
import struct
from QUANTAXIS import *
import sqlite3

import ctypes

'''
  
    mac or linux 可以使用wine 来运行 ， 需要指定字符集防止乱码
    安装
    env LC_ALL=zh_CN.UTF-8 wine instjd_1000.exe
    运行
    env LC_ALL=zh_CN.UTF-8 wine ~/.wine/drive_c/qianlong/jindian/JD/JD.exe

    设置 钱龙金典 数据下载目录 http://download2.ql18.com.cn/download/software/instjd_1000.exe
    
    new_tdx.exe 通达信也可安装上述方法
    env LC_ALL=zh_CN.UTF-8 wine ~/.wine/drive_c/new_tdx/TdxW.exe 

    同花顺 运行 wine 需要特殊配置。
    后期研究后发表。暂时用虚拟机共享目录的方式读取。
    
    --------------------------------------------------------------------------------------------
    读取 钱龙软件   本地数据文件进行比对 
    读取 同花顺软件  本地数据文件进行比对 ⭕️
    读取 通达信     本地数据文件进行比对  ⭕️


    📛钱龙数据文件格式
    上海日线存储路径为:\ml30\data\shase\day,文件扩展名为:.day
    上海周线存储路径为:\ml30\data\shase\week,文件扩展名为: .wek
    上海月线存储路径为:\ml30\data\shase\month,文件扩展名为: .mnt
    深圳日线存储路径为:\ml30\data\sznse\day
    深圳周线存储路径为:\ml30\data\sznse\week
    深圳月线存储路径为:\ml30\data\sznse\month
    以深发展日线为例:
    1A76:0100 D6 CD 2F 01 52 07 01 00-52 07 01 00 52 07 01 00
    1A76:0110 52 07 01 00 86 0F 00 00-4D 02 00 00 00 00 00 00
    1A76:0120 00 00 00 00 00 00 00 00-D7 CD 2F 01 60 03 01 00
    1A76:0130 60 03 01 00 60 03 01 00-60 03 01 00 82 05 00 00
    1A76:0140 D4 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00

    每一条记录的长度为40字节:
    1-4字节为日期,D6 CD 2F 01转换为十进制是:19910102
    5-8字节为开盘价*1000
    9-12字节为最高价*1000
    13-16字节为最低价*1000
    17-20字节为收盘价*1000
    21-24字节为成交量(手)
    25-28字节为成交金额
    其余12字节未使用
    
    
    钱龙数据结构及vb分析代码  

    钱龙数据结构及vb分析代码[存档]
    Public Type QLday '日线数据day的数据格式
        Rq As Long '十进制日期
        Op As Long '/1000=开盘价
        Hi As Long '/1000=最高价
        Lo As Long '/1000=最低价
        CL As Long '/1000=收盘价
        Am As Long '/10=成交金额(万元)
        Vo As Long '=成交量(手)
        t1 As Long '备用
        t2 As Long '备用
        t3 As Long '备用
    End Type

    Public Type QLQX '权息数据WGT的数据格式
        Rq As Long   '日期-是一个21位(bit)的数,占用4个字节(32位),前12位表示年,接着的4位表示月,接着的5位表示日,剩下的位未使用。
        Sgs As Long '送股数- /10000=每10股送股数
        Pgs As Long '配股数- /10000=每10股配股数
        Pgj As Long '配股价- /1000
        HL As Long '红利   - /1000
        Zzs As Long '转增数- /10000
        Zgb As Long '总股本- 单位是万股
        LTG As Long '流通股- 单位是万股
        Memo As Long '备注
    End Type

    Public Function RqQLQX(QXrq As Long) As Long '将权息数据的日期格式转换为long
    Dim QLDate0 As String, QLDate As String, QLYear As Long, QLMonth As Long, QLday As Long
    If QXrq = 0 Then
        RqQLQX = 0
    Else
        QLDate0 = DecimalToBinary(QXrq, 32)
        QLYear = BinaryToDecimal(Mid(QLDate0, 1, 12))
        QLMonth = BinaryToDecimal(Mid(QLDate0, 13, 4))
        QLday = BinaryToDecimal(Mid(QLDate0, 17, 5))
        QLDate = Format(QLYear, "0000") & Format(QLMonth, "00") & Format(QLday, "00")
        RqQLQX = Val(QLDate)
    End If
    End Function
    
    Public Function Date2Long(Date1 As Date) As Long
    Date2Long = Val(Format(Date1, "yyyymmdd"))
    End Function
    Public Function Long2Date(D1 As Long) As Date '"yyyymmdd"
    Dim S1 As String
    S1 = Trim(Str(D1))
    Long2Date = CDate(Left(S1, 4) & "-" & Mid(S1, 5, 2) & "-" & Right(S1, 2))
    End Function
    
    Public Function DCPrice(i As Integer, DateLong As Long, CodeName1 As String) As QLday
    '读取某日某股票:价格,i=1-上海 2-深圳
    Dim DayPath(2) As String '钱龙day数据目录  1-上海 2-深圳
    Dim QLday2 As QLday, Flag1 As Integer
    DayPath(1) = QLPathDaySH & CodeName1 & ".day"
    DayPath(2) = QLPathDaySZ & CodeName1 & ".day"
    Flag1 = 0
    Open DayPath(i) For Binary As #6
    Do While Not EOF(6)
        Get #6, , QLday2
        If QLday2.Rq < DateLong Then
        ElseIf QLday2.Rq = DateLong Then
            DCPrice = QLday2
            Flag1 = 1
            Exit Do
        Else
            Exit Do
        End If
    Loop
    Close #6
    If Flag1 <> 1 Then
        DCPrice.Rq = 0: DCPrice.Op = 0: DCPrice.Hi = 0: DCPrice.Lo = 0
        DCPrice.CL = 0: DCPrice.Am = 0: DCPrice.Vo = 0
    End If
    End Function
    
    Public Function DCLTG(i As Integer, DateLong As Long, CodeName1 As String) As Long
    '读取某日某股票:流通股,i=1-上海 2-深圳
    Dim WeightPath(2) As String '钱龙weight数据目录  1-上海 2-深圳
    Dim fso As New FileSystemObject
    Dim QLQX2 As QLQX, Flag1 As Integer, Tmp1 As Long
    Dim Rq1 As Long
    WeightPath(1) = QLPathWeightSH & CodeName1 & ".wgt"
    WeightPath(2) = QLPathWeightSZ & CodeName1 & ".wgt"
    DCLTG = 0
    If fso.FileExists(WeightPath(i)) = True Then
        Open WeightPath(i) For Binary As #7
        Do While Not EOF(7)
            Get #7, , QLQX2
            Rq1 = RqQLQX(QLQX2.Rq) '转换为长整形日期格式
            If Rq1 <= DateLong And Rq1 > 0 Then
                Tmp1 = QLQX2.LTG
            Else
                Exit Do
            End If
        Loop
        Close #7
        If Tmp1 > 0 Then
            DCLTG = Tmp1
        End If
    End If
    End Function
    
    Public Function DecimalToBinary(DecimalValue As Long, MinimumDigits As Integer) As String
    ' Returns a string containing the binary
    ' representation of a positive integer.
    Dim result As String
    Dim ExtraDigitsNeeded As Integer
    ' Make sure value is not negative.
    DecimalValue = Abs(DecimalValue)
    ' Construct the binary value.
    Do
        result = CStr(DecimalValue Mod 2) & result
        DecimalValue = DecimalValue \ 2
    Loop While DecimalValue > 0
    ' Add leading zeros if needed.
    ExtraDigitsNeeded = MinimumDigits - Len(result)
    If ExtraDigitsNeeded > 0 Then
        result = String(ExtraDigitsNeeded, "0") & result
    End If
    DecimalToBinary = result
    End Function
    
    Public Function BinaryToDecimal(BinaryValue As String) As Long
    ' Returns the decimal equivalent of a binary number.
    Dim idx As Integer
    Dim tmp As String
    Dim result As Long
    Dim digits As Integer
    digits = Len(BinaryValue)
    For idx = digits To 1 Step -1
        tmp = Mid(BinaryValue, idx, 1)
        If tmp = "1" Then result = result + 2 ^ (digits - idx)
    Next
    BinaryToDecimal = result
    End Function
    
    --------------------------------------------------------------------------------------------
    📛通达信数据文件格式

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

    通达信目录下T0002pad目录中，随你拷贝或复制
    数据下载Vipdoc
    自选股票T0002blocknewZXG.blk
    自编公式T0002PriGS.DAT
    自编模板T0002PriPack.DAT
    系统设置(常用指标)T0002user.配置设置
    通达信目录结构:
　　
　　 vipdoc:下载或缓存的历史数据目录
　　 diary:投资日志目录
　　 RemoteSH:缓存的上海F10
　　 RemoteSZ:缓存的深圳F10
　　 Ycinf缓存的公告消息
　 　安装目录下的SZ.*,SH.*是缓存的盘中数据文件
　
　　 T0002:个人信息目录,内有公式和自选股,个人设置等信息
　　 Advhq.dat 星空图相关个性化数据
　　 Block.cfg 板块设置文件
　　 cbset.dat 筹码分析个性化数据
　　 colwarn3.dat 行情栏目和预警个性化数据
　　 colwarnTj.dat 条件预警个性化数据
　　 CoolInfo.Txt 系统备忘录
　　 Line.dat 画线工具数据
　　 MyFavZX.dat 资讯收藏夹数据
　　 newmodem.ini 交易客户端个性化数据
　　 padinfo.dat 定制版面个性化数据
　　 PriCS.dat,PriGS.dat,PriText.dat 公式相关数据
　　 recentsearch.dat 最近资讯搜索数据
　　 Scheme.dat 配色方案
　　 tmptdx.css 临时网页CSS文件
　　 user.ini 全局个性化数据
　　 userfx.dat K线图个性化数据
　　
　　 [blocknew] 板块目录
　　 [cache] 系统数据高速缓存
　　 [zst_cache] 分时图数据高速缓存
　　 [coolinfo] 系统备忘录目录
　　 [Invest] 个人理财数据目录
      SUPERSTK下的文件:SYS.DTA 存放系统提供的公式;
      USERDATA下的文件：AUTOBLK.CFG:自动板块设定;SELF.DTA 存放用户自编的公式;
      BLOCK文件夹下的文件： *.IBK 板块指数定义;*.BLK 板块定义;*.EBK 条件选股结果;
      SELF 文件夹下的文件：   *.WSV 保存页面文件;ALERT.DAT 历史预警纪录;EXTDATA.INF 扩展数据定义;
    *.CEP 保存组合条件选股条件;TEMPCMPD.CEP测试附加条件;
    *.INV 用户个人投资纪录;*.TPT 保存指标模板;SELF年月日.DTA 每日自动公式备份文件;
          TEST 文件夹下的文件： *.TST 存放系统测试结果;*.OPT 存放参数优化的结果;
      PARAM参数指引文件夹: *.PRM 存放参数指引的结果;
      TABLE文件夹下的文件：*.ESS数据表文件;*.ESD数据表文件（带数据保存）;　　　
      SelfData文件夹下的文件：*.str　字符串数据;*.oth 与股票无关序列值数据;
      Pattern 文件夹下的文件:  *.PIN 模式匹配设计;*.PWT模式匹配方法;
      SpotAna文件夹下的文件:  *.SPT 定位分析结果;
      Relate文件夹下的文件:     *.RTL　相关分析结果;
      Posible文件夹下的文件:    *.PSB　预测分布设计;
      DATA件夹下的文件：       DAY.DAT 日线数据;EXTDAY.DAT 扩展数据;MIN.DAT 5分钟线数据;REPORT.DAT
                             当天的分笔成交数据;STKINFO.DAT 代码表/即时行情数据/财务数据/除权数据;
                             *.PRP历史回忆数据，一天一个文件;
       NEWS文件夹下的文件：*.TXT 财经报道、上交所公告、深交所公告



==========2014.10.18补充
5.85和5.86版本可能被服务器拒绝了，都考虑换5.87B版本吧，把T0002文件夹内容根据需要复制到新版本中。
如果单要恢复公式，可复制黏贴其下2个文件，PriCS.dat,PriGS.dat,PriText.dat 公式相关数据。
T0002:个别信息目录,内有公式和自选股,个别设备等信息
　　Advhq.dat 星空图相关性格化数据
　　Block.cfg 板块设备文件
　　cbset.dat 筹码分析性格化数据
　　colwarn3.dat 行情栏目和预警性格化数据
　　colwarnTj.dat 条件预警性格化数据
　　CoolInfo.Txt 体系备忘录
　　Line.dat 画线用具数据
　　MyFavZX.dat 资讯收藏夹数据
　　newmodem.ini 业务客户端性格化数据
　　padinfo.dat 定制版面性格化数据
　　PriCS.dat,PriGS.dat,PriText.dat 公式相关数据
　　recentsearch.dat 最近资讯包罗数据
　　Scheme.dat 配色方案
　　tmptdx.css 权且网页CSS文件
　　user.ini 全局性格化数据
　　userfx.dat K线图性格化数据
　　[blocknew] 板块目录
　　[cache] 体系数据高速缓存
　　[zst_cache] 分时图数据高速缓存
　　[coolinfo] 体系备忘录目录
　　[Invest] 个别理财数据目录
自选股放在通达信软件 \T0002\blocknew/zxg.blk


通达信股本变迁文件（gbbq）解密方法
数据哪里来呢？当然是拿来主义。。。问券商的交易软件要呗
到处查资料，得知通达信的权息文件数据齐全，不仅含有除权除息数据，还含有限售解禁、增发、可转债上市等股本变化数据
——这对于某些对成交量变化敏感的交易模型是非常重要的

然而，gbbq文件是加密的，网上找不到解密算法，说不得只好请出尘封已久的ollydebug大侠咯~

1、在fopen函数下个条件断点，esp寄存器指向的第一个参数是文件名指针地址，若文件名含有“gbbq”，断之
2、很容易找到后续代码里连续调用了2次fread，第一次只读4字节，很明显是文件包含的记录数
3、跟踪第二次fread，发现将数据存入内存后，开始与另一块内存中的数据进行反复相加、异或操作，最后完成解密
4、另一块内存中的数据经多次加载对比，发现内容固定，长度4176字节，应该是自带的密码表
5、没有必要搞明白密码表是哪来的，直接从内存dump出来存为文件就行了
6、每条记录29字节，前24字节是加密的，后5字节未加密，因为他用的加密算法是固定64位，一次加密8字节
7、解密过程汇编代码很长，但仔细分析后可以转换为16次循环，64位对称加密，16次循环，呵呵，DES嘛

 while (len)
 {
  for (i = 0; i < 3; i++)
  {
   eax = *((int*)(pCodeNow + 0x44));
   ebx=*((int*)(pDataNow));
   num = eax^ebx;
   numold = *((int*)(pDataNow + 0x4));

   for (j = 0x40; j > 0; j = j - 4)
   {
    ebx = (num & 0xff0000) >> 16;
    eax = *((int*)(pCodeNow + ebx * 4 + 0x448));
    ebx = num >> 24;
    eax += *((int*)(pCodeNow + ebx * 4 + 0x48));
    ebx = (num & 0xff00) >> 8;
    eax ^= *((int*)(pCodeNow + ebx * 4 + 0x848));
    ebx = num & 0xff;
    eax += *((int*)(pCodeNow + ebx * 4 + 0xC48));
    eax ^= *((int*)(pCodeNow + j));

    ebx = num;
    num = numold^eax;
    numold = ebx;
   }
   numold ^= *((int*)pCodeNow);
   pInt = (unsigned int*)pDataNow;
   *pInt = numold;
   pInt = (unsigned int*)(pDataNow+4);
   *pInt = num;
   pDataNow = pDataNow + 8;
  }
  pDataNow = pDataNow + 5;
  len--;
 }
搞定~ok
--------------------------------------------------------------------------------------------
Python读取通达信本地数据
通达信本地数据格式：
每32个字节为一个5分钟数据，每字段内低字节在前
00 ~ 01 字节：日期，整型，设其值为num，则日期计算方法为：
                        year=floor(num/2048)+2004;
                        month=floor(mod(num,2048)/100);
                        day=mod(mod(num,2048),100);
02 ~ 03 字节： 从0点开始至目前的分钟数，整型
04 ~ 07 字节：开盘价*100，整型
08 ~ 11 字节：最高价*100，整型
12 ~ 15 字节：最低价*100，整型
16 ~ 19 字节：收盘价*100，整型
20 ~ 23 字节：成交额*100，float型
24 ~ 27 字节：成交量（股），整型
28 ~ 31 字节：（保留）

每32个字节为一天数据
每4个字节为一个字段，每个字段内低字节在前
00 ~ 03 字节：年月日, 整型
04 ~ 07 字节：开盘价*100， 整型
08 ~ 11 字节：最高价*100,  整型
12 ~ 15 字节：最低价*100,  整型
16 ~ 19 字节：收盘价*100,  整型
20 ~ 23 字节：成交额（元），float型
24 ~ 27 字节：成交量（股），整型
28 ~ 31 字节：（保留）

读取需要加载struct模块，unpack之后得到一个元组。
日线读取：
fn="code.day";
fid=open(fn,"rb");
list=fid.read(32)
ulist=struct.unpack("iiiiifii", list)
5分钟线读取也是一样。

本地数据未除权。

struct模块的pack、unpack示例

除权数据 （加密，需要解密操作）

在通达信安装目录下的\T0002\hq_cache目录有个gbbq和gbbq.map的文件，是关于所有沪深市场上市证券的股本变动信息的文件。目前没有找到相关资料。
--------------------------------------------------------------------------------------------

📛同花顺数据文件格式， 参考 c# 的实现
    https://sourceforge.net/projects/ociathena/

'''


class Test_Query_Advance(unittest.TestCase):

    def check_qilong_dir_exist(self):
        # 替换 运行环境下本地路径
        self.strQianLong_QLDATA_ = '/Users/jerryw/.wine/drive_c/qianlong/jindian/QLDATA/'

        isExists = os.path.exists(self.strQianLong_QLDATA_)
        if not isExists:
            print("🔍查找路径不存在 %s ⛔️" % self.strQianLong_QLDATA_)
            return False
        else:

            # 初始化 钱龙 数据目录
            self.strQianLong_SHASE_day_dir = self.strQianLong_QLDATA_ + ('history/SHASE/day/')
            self.strQianLong_SHASE_weight_dir = self.strQianLong_QLDATA_ + ('history/SHASE/weight/')
            self.strQianLong_SHASE_nmn_dir = self.strQianLong_QLDATA_ + ('history/SHASE/nmn/')

            self.strQianLong_SZNSE_day_dir = self.strQianLong_QLDATA_ + ('history/SZNSE/day/')
            self.strQianLong_SZNSE_weight_dir = self.strQianLong_QLDATA_ + ('history/SZNSE/weight/')
            self.strQianLong_SZNSE_nmn_dir = self.strQianLong_QLDATA_ + ('history/SZNSE/nmn/')
            return True


    def parse_day_file_to_mysql_lite_db(self, day_file_path, db_file_save_dir, day_file):
        '''

        :param day_file_path:
        :param db_file_save_dir:
        :param day_file:
        :return:
        '''
        #time.sleep(1)
        file_size = os.path.getsize(day_file_path)
        assert((file_size % 40) == 0)
        #print(("%s 文件大小 %d Bytes"%(day_file_path, file_size)) +
        #("40Bytes/recrod, found %d records!"%(file_size / 40)))
        item_len = file_size // 40

        db_file_save_file = db_file_save_dir
        db_file_save_file = db_file_save_file + "/" + day_file[0:6] + '.sqlite_db'
        conn = sqlite3.connect(db_file_save_file)
        c = conn.cursor()
        # Create table
        c.execute('''DROP TABLE IF EXISTS stocks''')
        c.execute('''CREATE TABLE stocks (date int, open_price real, high_price real, low_price real, close_price real, volumn real, amount real)''')


        # 钱龙只下载 800 天到历史数据记录， 经一步研究如何下载完整到数据
        with open(file=day_file_path, mode='rb') as f:
            #读取每条记录， 然后写到 mysql lite 数据库中
            for i in range(item_len):
                read_data_section = f.read(40)
                values = struct.unpack("<LLLLLLL",read_data_section[0:28])
                c.execute("INSERT INTO stocks(date,open_price,high_price,low_price,close_price,volumn,amount)  VALUES (%d,%f,%f,%f,%f,%d,%d)" % (values[0], values[1] / 1000, values[2] / 1000, values[3] / 1000, values[4] / 1000,values[5],values[6]))
            f.closed
        conn.commit()
        c.close()
        conn.close()
        pass



    def read_all_day_file_directory_to_sql_lite(self):
        '''
        # 获取目录文件名，股票代码
        # 读取数据
        # 写到sqllite
        :return:
        '''
        if self.check_qilong_dir_exist() == False:
            return

        curdir = os.getcwd()
        print("准备写入db🗃文件到目录%s" % (curdir + "/qianglong_data_sh"))
        path_for_save_data = curdir + "/qianglong_data_sh"
        path_for_save_data = path_for_save_data.rstrip("\\")
        isExists = os.path.exists(path_for_save_data)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path_for_save_data)
            print(path_for_save_data + ' 创建成功😊')
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path_for_save_data + ' 目录已存在😅')

        stock_count = len(os.listdir(self.strQianLong_SHASE_day_dir))
        iCount = 0
        for day_file in os.listdir(self.strQianLong_SHASE_day_dir):

            iii = round((iCount / stock_count) * 100.0)
            s1 = "\r读取 上海证券交易所 股票数据%s %d%%[%s%s]" % (day_file, iii, "🐌" * iii, " " * (100 - iii))
            sys.stdout.write(s1)
            sys.stdout.flush()

            if fnmatch.fnmatch(day_file, '*.day'):
                fullPathFileName = self.strQianLong_SHASE_day_dir + day_file
                self.parse_day_file_to_mysql_lite_db(fullPathFileName, path_for_save_data, day_file)
                iCount = iCount + 1
        print("\n😇读取  上海证券交易所 日线数据完成")

        #todo 🛠读取深圳日线数据 到 sqllite保存

    # https://stackoverflow.com/questions/5832982/how-to-get-the-logical-right-binary-shift-in-python/5833119#5833119
    def rshift(val, n):
        return val >> n if val >= 0 else (val + 0x100000000) >> n

    # 解析 weight 文件
    def parse_weight_file_to_mysql_lite_db(self, weight_file_path, db_file_save_dir, weight_file):
        '''
        :param weight_file_path:  weight 文件全路径文件名
        :param db_file_save_dir: sqlite 数据库保存的目录
        :param weight_file: 读取的 *.wgt 文件的名字
        :return:
        '''

        if self.check_qilong_dir_exist() == False:
            return

        # time.sleep(1)
        file_size = os.path.getsize(weight_file_path)
        '''
        Rq As Long   '日期-是一个21位(bit)的数,占用4个字节(32位),前12位表示年,接着的4位表示月,接着的5位表示日,剩下的位未使用。
        Sgs As Long '送股数- /10000=每10股送股数
        Pgs As Long '配股数- /10000=每10股配股数
        Pgj As Long '配股价- /1000
        HL As Long '红利   - /1000
        Zzs As Long '转增数- /10000
        Zgb As Long '总股本- 单位是万股
        LTG As Long '流通股- 单位是万股
        Memo As Long '备注
        '''
        assert ((file_size % (9 * 4)) == 0)

        #print(("%s 文件大小 %d Bytes"%(weight_file_path, file_size)) +
        #("40Bytes/recrod, found %d records!"%(file_size / (9*4))))
        item_len = file_size // (9 * 4)


        db_file_save_file = db_file_save_dir
        db_file_save_file = db_file_save_file + "/" + weight_file[0:6] + '.wgt.sqlite_db'

        conn = sqlite3.connect(db_file_save_file)
        c = conn.cursor()

        c.execute('''DROP TABLE IF EXISTS stocks_weight''')
        c.execute('''CREATE TABLE stocks_weight (date int, shares_dividend real, shares_rationed real, shares_rationed_price real, cash_bonus real, transferOfstock real, totalStockIssue int,outstandingShares int, memo int )''')


        with open(file=weight_file_path, mode='rb') as f:
        #     # 读取每条记录， 然后写到 mysql lite 数据库中
            for i in range(item_len):
                read_data_section = f.read((9 * 4))
                values = struct.unpack('<LLLLLLLLL', read_data_section)

                date_raw = values[0]
                #print(type(date_raw))
                #print('%#x' % date_raw)

                year = date_raw >> (32 - 12) #前12位表示年
                #print('%#x' % (date_raw >> (32-12)) )
                                                            #print(year)
                                                                                                        #
                # #
                                                            # https://stackoverflow.com/questions/12163875/python-left-shift-sign-issue
                                                                                                        # #
                                                                                                                                                    # https://stackoverflow.com/questions/5832982/how-to-get-the-logical-right-binary-shift-in-python/5833119#5833119
                                                                                                                                                                                                # month
                                                                                                                                                                                                                                            # =
                                                                                                                                                                                                                                                                                        # (date_raw
                                                                                                                                                                                                                                                                                        # <<
                                                                                                                                                                                                                                                                                        # (12))
                                                                                                                                                                                                                                                                                        # >>
                                                                                                                                                                                                                                                                                        # (64
                                                                                                                                                                                                                                                                                        # -
                                                                                                                                                                                                                                                                                        # 4)
                                                                                                                                                                                                                                                                                        # #
                                                                                                                                                                                                                                                                                        # 前12位表示年
                #print('%#x' % (date_raw << (12)))
                                                            #print('%#x' %
                                                                                                        #(date_raw
                                                                                                                                                    #<<
                                                                                                                                                                                                #(12+4*100)))
                                                                                                                                                                                                                                            #😱奇怪的shift
                                                                                                                                                                                                                                                                                        #操作，0x7c8b80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
                # python 的数据类型 长度无限大 ？

                month = (date_raw & (0x000F0000)) >> (32 - (12 + 4))
                #print(month)

                day = (date_raw & (0x0000F800)) >> (32 - (12 + 4 + 5))
                #print(day)
                #print('%04d-%02d-%02d'%(year, month,day))

                #送股数
                shares_dividend = values[1] / 10000
                #print('送股%f'% shares_dividend)
                #配股数
                shares_rationed = values[2] / 10000
                #print('配股%f' % shares_rationed)
                #配股价
                shares_rationed_price = values[3] / 1000
                #print('配股价%f' % shares_rationed_price)
                #红利
                cash_bonus = values[4] / 1000
                #print('现金红利%f' % cash_bonus)
                #转增数
                transferOfstock = values[5] / 10000
                #print('转增数%f' % transferOfstock)

                #总股本
                totalStockIssue = values[6]
                #print('总股本%d' % totalStockIssue)

                outstandingShares = values[7]
                #print('流通股%d' % outstandingShares)

                memo = values[8]
                #print('备注%d' % memo)

                day_number = year * 10000 + month * 100 + day

                c.execute("INSERT INTO stocks_weight(date,shares_dividend,shares_rationed,shares_rationed_price,cash_bonus,transferOfstock,totalStockIssue,outstandingShares,memo)  "
                    " VALUES (%d,%f,%f,%f,%f,%f,%d,%d,%d)" % (day_number,shares_dividend,shares_rationed,shares_rationed_price,cash_bonus,transferOfstock,totalStockIssue,outstandingShares,memo))

                #流通股
                #备注
        #         read_data_section = f.read(40)
        #         values = struct.unpack("<LLLLLLL", read_data_section[0:28])
        #         c.execute(
        #             "INSERT INTO
        #             stocks(date,open_price,high_price,low_price,close_price,volumn,amount)
        #             VALUES (%d,%f,%f,%f,%f,%d,%d)"
        #             % (values[0], values[1] / 1000, values[2] / 1000,
        #             values[3] / 1000, values[4] / 1000, values[5],
        #                values[6]))
            f.closed
        conn.commit()
        c.close()
        conn.close()

        pass

    #读取 钱龙股本变动文件
    def read_all_weight_file_directory_to_sql_lite(self):

        if self.check_qilong_dir_exist() == False:
            return

        curdir = os.getcwd()
        print("准备写入day🗃文件到目录%s" % (curdir + "/qianglong_weight_data_sh"))
        path_for_save_data = curdir + "/qianglong_weight_data_sh"
        path_for_save_data = path_for_save_data.rstrip("\\")
        isExists = os.path.exists(path_for_save_data)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path_for_save_data)
            print(path_for_save_data + ' 创建成功😊')
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path_for_save_data + ' 目录已存在😅')

        weight_count = len(os.listdir(self.strQianLong_SHASE_weight_dir))

        iCount = 0
        for weight_file in os.listdir(self.strQianLong_SHASE_weight_dir):

            iii = round((iCount / weight_count) * 100.0)
            s1 = "\r读取 上海证券交易所 股份变动数据%s %d%%[%s%s]" % (weight_file, iii, "🐌" * iii, " " * (100 - iii))
            sys.stdout.write(s1)
            sys.stdout.flush()

            if fnmatch.fnmatch(weight_file, '*.wgt'):
                fullPathFileName = self.strQianLong_SHASE_weight_dir + weight_file
                self.parse_weight_file_to_mysql_lite_db(fullPathFileName, path_for_save_data, weight_file)

                #self.parse_weight_file_to_mysql_lite_db(self.strQianLong_SHASE_weight_dir+'600000.wgt',
                #path_for_save_data, '600000.wgt')

                iCount = iCount + 1
        print("\n😇读取  上海证券交易所 日线数据完成")

        #todo 🛠读取深圳 股份变动文件数据 到 sqllite保存
        pass



    # 对比 stock_day 数据库
    def test_MongoDB_DAY_collection_with_QiLong_DAY_File(self):
        self.read_all_day_file_directory_to_sql_lite()
        # todo 🛠 对比数据库去中数据

    # 对比 stock_xdxr 数据库
    def test_MongoDB_DAY_XDXR_data_with_QiLong_DAY(self):
        self.read_all_weight_file_directory_to_sql_lite()
        # todo 🛠 对比数据库去中数据



    def test_QA_fetch_stock_min_adv(self):
        # dataStruct = QA_fetch_stock_min_adv(start='2018-05-28 00:00:00',code
        # = '300439')
        # print("获取1分钟数据")
        # print(dataStruct)
        # #dataStruct.show()
        pass

    #def test_001(self):
        # print("-----------------------------------------------------------------------")
        # df = QATs.get_stock_basics()
        # print(df)
        # print("-----------------------------------------------------------------------")
        #data = QA_fetch_get_stock_list(package = "tdx")
        # print(data)
        # print("-----------------------------------------------------------------------")

        #engine = select_save_engine(engine="Tushare")
        #engine.QA_SU_save_stock_list(client=DATABASE)

        # date = str(datetime.date.today())
        # date_stamp = QA_util_date_stamp(date)
        # print(data)
        # print(date_stamp)
        # #
        # client = DATABASE
        # coll = client.stock_list
        # coll.insert({'date': date, 'date_stamp': date_stamp,
        #              'stock': {'code': data}})
        #return list(df.index)
        pass




    def setUp(self):
        #每次执行 test_XX 函数都会重复执行setUP
        pass

    def tearDown(self):
        #每次执行 test_XX tearDown
        pass


'''
'''
if __name__ == '__main__':
    # -*- coding: utf-8 -*-
    #import numpy as np
    #import pandas as pd
    #import matplotlib as mpl
    #import matplotlib.pyplot as plt
    #import seaborn as sns
    #import warnings; warnings.filterwarnings(action='once')
    #import tushare as ts
    #'''
    #36 带波峰波谷标记的时序图 （Time Series with Peaks and Troughs Annotated）
    #下面的时间序列绘制了所有峰值和低谷，并注释了所选特殊事件的发生。
    #'''
    #df = ts.get_hist_data('600006',start='2019-06-01')
    #df = df.sort_index(0)
    ##直接保存
    #df.to_csv('600006.csv')
    ## Import Data
    #df = pd.read_csv('600006.csv')
    ##('https://github.com/selva86/datasets/raw/master/AirPassengers.csv')
    ##df.to_csv('AirPassengers.csv')
    #print(df.info())
    ##df['value']=df['close']
    ## Get the Peaks and Troughs
    #data = df['close'].values
    #doublediff = np.diff(np.sign(np.diff(data)))
    #peak_locations = np.where(doublediff == -2)[0] + 1

    #doublediff2 = np.diff(np.sign(np.diff(-1*data)))
    #trough_locations = np.where(doublediff2 == -2)[0] + 1

    ## Draw Plot
    #plt.figure(figsize=(16,10), dpi= 80)
    #plt.plot('date', 'close', data=df, color='tab:blue', label='close')
    #plt.scatter(df.date[peak_locations], df.close[peak_locations],
    #marker=mpl.markers.CARETUPBASE, color='tab:green', s=100, label='Peaks')
    #plt.scatter(df.date[trough_locations], df.close[trough_locations],
    #marker=mpl.markers.CARETDOWNBASE, color='tab:red', s=100, label='Troughs')

    ## Annotate
    #for t, p in zip(trough_locations[1::5], peak_locations[::3]):
    #    plt.text(df.date[p], df.close[p], df.date[p],
    #    horizontalalignment='center', color='darkgreen')#df.close1[p]*(1+0.05)
    #    plt.text(df.date[t], df.close[t], df.date[t],
    #    horizontalalignment='center', color='darkred')#df.close1[t]*(1.0-0.05)

    ## Decoration
    ##plt.ylim(50,750)
    #xtick_location = df.index.tolist()[::6]
    #xtick_labels = df.date.tolist()[::6]
    #plt.xticks(ticks=xtick_location, labels=xtick_labels, rotation=45,
    #fontsize=12, alpha=.7)
    #plt.title("Peak and Troughs of 600006", fontsize=22)
    #plt.yticks(fontsize=12, alpha=.7)

    ## Lighten borders
    #plt.gca().spines["top"].set_alpha(.0)
    #plt.gca().spines["bottom"].set_alpha(.3)
    #plt.gca().spines["right"].set_alpha(.0)
    #plt.gca().spines["left"].set_alpha(.3)

    #plt.legend(loc='upper left')
    #plt.grid(axis='y', alpha=.3)
    #plt.show()

    #st = QA_fetch_stock_block_adv(None, ["北京", "计算机"])
    #QA_fetch_stock_realtime_adv(['000001', '000002'], num=10)
    import QUANTAXIS as QA
    from QUANTAXIS.QAFetch.QAhuobi import FIRST_PRIORITY
    codelist = ['BCHUSDT', 'BSVUSDT', 'BTCUSDT', 'EOSUSDT', 'ETHUSDT', 'ETCUSDT', 'DASHUSDT', 'LTCUSDT', 'XMRUSDT', 'XRPUSDT', 'ZECUSDT']
    data_1h = QA_fetch_crypto_asset_min_adv(['binance','huobi'],
            code=codelist + FIRST_PRIORITY,
            start='2020-02-01',
            end='2020-05-28 18:10:00',
            frequence='60min')
    data_day = QA_fetch_crypto_asset_day_adv(['binance','huobi'],
            symbol=codelist + FIRST_PRIORITY,
            start='2019-10-01',
            end='2020-05-28 18:10:00')
    data2 = QA_fetch_crypto_asset_min_adv(['huobi'],
            code=['btcusdt'],
            start='2020-02-01',
            end='2020-05-28 18:10:00',
            frequence='60min')
    
    #codelist = QA.QA_fetch_stock_block_adv().get_block('沪深300').code
    #print(codelist[0:30])

    # 获取全市场数据 QADataStruct格式
    #data1 = QA.QA_fetch_stock_day_adv(codelist, '2018-11-01','2020-05-29')

    #print(data1.data)
    #data1 = QA.QA_fetch_crypto_asset_min_adv(
    #    ['binance','huobi'],
    #    symbol=codelist+FIRST_PRIORITY,
    #    start='2019-08-21',
    #    end='2020-05-28 18:10:00',
    #    frequence='60min'
    #)
    #data_4h = QA.QA_DataStruct_Crypto_Asset_min(data2.resample('4h'))
    data_4h = QA.QA_DataStruct_Crypto_Asset_min(data2.resample('4h'))

    import numpy as np
    import talib
    import pandas as pd
    import scipy.signal as signal
    import matplotlib.pyplot as plt
    from QUANTAXIS.QAAnalysis.QAAnalysis_kline import QA_Timekline

    def ifup20_TA(data):
        # TA-lib计算
        return (talib.MA(data.close, 5) - talib.MA(data.close, 20)).dropna() > 0

    # 写个自定义指标 MAX_FACTOR TA-lib计算
    def ifmaxfactor_greater_TA(data):
        RSI = QA.TA_RSI(data.close, timeperiod=12)
        CCI = QA.TA_CCI(data.high, data.low, data.close)
        KDJ = QA.TA_KDJ(data.high, data.low, data.close)    
        MAX_FACTOR = CCI[:,0] + (RSI[:,0] - 50) * 4 + (KDJ[:,2] - 50) * 4
        MAX_FACTOR_delta = np.r_[np.nan, np.diff(MAX_FACTOR)]
        REGRESSION_BASELINE = (RSI[:,0] - 50) * 4
        return pd.DataFrame(((MAX_FACTOR + MAX_FACTOR_delta) - (REGRESSION_BASELINE - 133)), index=data.index).dropna() > 0

    def dual_cross(data):
        RSI = QA.TA_RSI(data.close, timeperiod=12)
        CCI = QA.TA_CCI(data.high, data.low, data.close)
        KDJ = QA.TA_KDJ(data.high, data.low, data.close)
    
        CCI_CROSS_JX = CROSS_STATUS(CCI[:,0], (RSI[:,0] - 50) * 4)
        KDJ_J_CROSS_JX = CROSS_STATUS(KDJ[:,2], RSI[:,0])
        KDJ_J_CROSS_JX_PLUS = CROSS_STATUS(KDJ[:,2] + KDJ[:,3], RSI[:,0])
        DUAL_CROSS_JX = CROSS_STATUS(CCI_CROSS_JX * (CCI_CROSS_JX + KDJ_J_CROSS_JX + KDJ_J_CROSS_JX_PLUS), 1)
    
        CCI_CROSS_SX = CROSS_STATUS((RSI[:,0] - 50) * 4, CCI[:,0])
        KDJ_J_CROSS_SX = CROSS_STATUS(RSI[:,0], KDJ[:,2])
        KDJ_J_CROSS_SX_PLUS = CROSS_STATUS(RSI[:,0], KDJ[:,2] + KDJ[:,3])
        DUAL_CROSS_SX = CROSS_STATUS(CCI_CROSS_SX * (CCI_CROSS_SX + KDJ_J_CROSS_SX + KDJ_J_CROSS_SX_PLUS), 1)
    
        DUAL_CROSS = pd.DataFrame(columns=['DUAL_CROSS', 'DUAL_CROSS_JX', 'DUAL_CROSS_SX'], index=data.index)
        DUAL_CROSS.loc[DUAL_CROSS_JX == 1, 'DUAL_CROSS'] = 1
        DUAL_CROSS.loc[DUAL_CROSS_SX == 1, 'DUAL_CROSS'] = -1
        DUAL_CROSS['DUAL_CROSS_JX'] = Timeline_Integral(DUAL_CROSS_JX)
        DUAL_CROSS['DUAL_CROSS_SX'] = Timeline_Integral(DUAL_CROSS_SX)
        return DUAL_CROSS

    def ma30_cross(data):
        MA5 = talib.MA(data.close, 5)
        MA30 = talib.MA(data.close, 30)
    
        MA30_CROSS_JX = CROSS(MA5, MA30)
        MA30_CROSS_JX_Integral = Timeline_Integral_with_cross_before(MA30_CROSS_JX)
        MA30_CROSS_SX = CROSS(MA30, MA5)
        MA30_CROSS_SX_Integral = Timeline_Integral_with_cross_before(MA30_CROSS_SX)
    
        MA30_CROSS = pd.DataFrame(columns=['MA30_CROSS', 'MA30_CROSS_JX', 'MA30_CROSS_SX', 'MA30_TP_CROSS_JX', 'MA30_TP_CROSS_SX'], index=data.index)
        MA30_CROSS.loc[MA30_CROSS_JX == 1, 'MA30_CROSS'] = 1
        MA30_CROSS.loc[MA30_CROSS_SX == 1, 'MA30_CROSS'] = -1
        MA30_CROSS['MA30_CROSS_JX'] = Timeline_Integral_with_cross_before(MA30_CROSS_JX)
        MA30_CROSS['MA30_CROSS_SX'] = Timeline_Integral_with_cross_before(MA30_CROSS_SX)
    
        # MA30 前29个是 NaN，处理会抛出 Warning，使用 [29:] 则不会计算 NaN，相应的 return_index+29
        MA30_tp_min, MA30_tp_max = signal.argrelextrema(MA30.values[29:], np.less)[0] + 29, signal.argrelextrema(MA30.values[29:], np.greater)[0] + 29
        MA30_TP_CROSS = pd.DataFrame(columns=['MA30_TP_CROSS_JX', 'MA30_TP_CROSS_SX'], index=data.index)
        MA30_TP_CROSS['MA30_TP_CROSS_SX'] = MA30_TP_CROSS['MA30_TP_CROSS_JX'] = 0
        MA30_TP_CROSS.iloc[MA30_tp_min, MA30_TP_CROSS.columns.get_loc('MA30_TP_CROSS_JX')] = 1
        MA30_TP_CROSS.iloc[MA30_tp_max, MA30_TP_CROSS.columns.get_loc('MA30_TP_CROSS_SX')] = 1
        MA30_CROSS['MA30_TP_CROSS_JX'] = Timeline_Integral_with_cross_before(MA30_TP_CROSS['MA30_TP_CROSS_JX'])
        MA30_CROSS['MA30_TP_CROSS_SX'] = Timeline_Integral_with_cross_before(MA30_TP_CROSS['MA30_TP_CROSS_SX'])
        return MA30_CROSS

    def boll_cross(data):
        BBANDS = QA.TA_BBANDS(data.close, timeperiod=20, nbdevup=2)

        BOLL_CROSS = pd.DataFrame(columns=['min_peak', 'max_peak', 'BOLL_CROSS', 'BOLL_CROSS_JX', 'BOLL_CROSS_SX'], index=data.index)
        
        # 防止插针行情突然搞乱
        data['smooth_low'] = talib.MA(data.low, 2)
        data['smooth_high'] = talib.MA(data.high, 2)

        BOLL_CROSS['min_peak'] = data.apply(lambda x: min(x['open'], x['close'], x['smooth_low']), axis=1)
        BOLL_CROSS['max_peak'] = data.apply(lambda x: max(x['open'], x['close'], x['smooth_high']), axis=1)

        BOLL_CROSS_JX = CROSS(BOLL_CROSS['min_peak'], BBANDS[:,2])
        BOLL_CROSS_SX = CROSS(BBANDS[:,0], BOLL_CROSS['max_peak'])

        BOLL_CROSS.loc[BOLL_CROSS_JX == 1, 'BOLL_CROSS'] = 1
        BOLL_CROSS.loc[BOLL_CROSS_SX == 1, 'BOLL_CROSS'] = -1
        BOLL_TP_CROSS = pd.DataFrame(columns=['BOLL_TP_CROSS_JX', 'BOLL_TP_CROSS_SX'], index=data.index)
        BOLL_TP_CROSS['BOLL_TP_CROSS_SX'] = BOLL_TP_CROSS['BOLL_TP_CROSS_JX'] = 0
        BOLL_TP_CROSS.loc[BOLL_CROSS_JX == 1, 'BOLL_TP_CROSS_JX'] = 1
        BOLL_TP_CROSS.loc[BOLL_CROSS_SX == 1, 'BOLL_TP_CROSS_SX'] = 1

        BOLL_CROSS = BOLL_CROSS.assign(BOLL_UB=BBANDS[:,0])
        BOLL_CROSS = BOLL_CROSS.assign(BOLL_MA=BBANDS[:,1])
        BOLL_CROSS = BOLL_CROSS.assign(BOLL_LB=BBANDS[:,2])
        BOLL_CROSS['BOLL_CROSS_JX'] = QA.Timeline_Integral_with_cross_before(BOLL_TP_CROSS['BOLL_TP_CROSS_JX'])
        BOLL_CROSS['BOLL_CROSS_SX'] = QA.Timeline_Integral_with_cross_before(BOLL_TP_CROSS['BOLL_TP_CROSS_SX'])
        return BOLL_CROSS

    def boll_cross_lf(data):
        BBANDS = QA.TA_BBANDS(data.close, timeperiod=20, nbdevup=2)

        BOLL_CROSS_JX1 = CROSS(data.open, BBANDS[:,2])
        BOLL_CROSS_JX2 = CROSS(data.close, BBANDS[:,2])
        BOLL_CROSS_JX3 = CROSS(talib.MA(data.low, 2), BBANDS[:,2])
        BOLL_CROSS_SX1 = CROSS(BBANDS[:,0], data.open)
        BOLL_CROSS_SX2 = CROSS(BBANDS[:,0], data.close)
        BOLL_CROSS_SX3 = CROSS(BBANDS[:,0], talib.MA(data.high, 2))

        BOLL_CROSS = pd.DataFrame(columns=['BOLL_CROSS', 'BOLL_CROSS_JX', 'BOLL_CROSS_SX'], index=data.index)
        BOLL_CROSS.loc[BOLL_CROSS_JX1 == 1, 'BOLL_CROSS'] = 1
        BOLL_CROSS.loc[BOLL_CROSS_JX2 == 1, 'BOLL_CROSS'] = 1
        BOLL_CROSS.loc[BOLL_CROSS_JX3 == 1, 'BOLL_CROSS'] = 1
        BOLL_CROSS.loc[BOLL_CROSS_SX1 == 1, 'BOLL_CROSS'] = -1
        BOLL_CROSS.loc[BOLL_CROSS_SX2 == 1, 'BOLL_CROSS'] = -1
        BOLL_CROSS.loc[BOLL_CROSS_SX3 == 1, 'BOLL_CROSS'] = -1
        BOLL_TP_CROSS = pd.DataFrame(columns=['BOLL_TP_CROSS_JX', 'BOLL_TP_CROSS_SX'], index=data.index)
        BOLL_TP_CROSS['BOLL_TP_CROSS_SX'] = BOLL_TP_CROSS['BOLL_TP_CROSS_JX'] = 0
        BOLL_TP_CROSS.loc[(BOLL_CROSS_JX1 | BOLL_CROSS_JX2 | BOLL_CROSS_JX3) == 1, 'BOLL_TP_CROSS_JX'] = 1
        BOLL_TP_CROSS.loc[(BOLL_CROSS_SX1 | BOLL_CROSS_SX2 | BOLL_CROSS_SX3) == 1, 'BOLL_TP_CROSS_SX'] = 1

        BOLL_CROSS = BOLL_CROSS.assign(BOLL_UB=BBANDS[:,0])
        BOLL_CROSS = BOLL_CROSS.assign(BOLL_MA=BBANDS[:,1])
        BOLL_CROSS = BOLL_CROSS.assign(BOLL_LB=BBANDS[:,2])
        BOLL_CROSS['BOLL_CROSS_JX'] = QA.Timeline_Integral_with_cross_before(BOLL_TP_CROSS['BOLL_TP_CROSS_JX'])
        BOLL_CROSS['BOLL_CROSS_SX'] = QA.Timeline_Integral_with_cross_before(BOLL_TP_CROSS['BOLL_TP_CROSS_SX'])
        return BOLL_CROSS

    def maxfactor_cross(data):
        RSI = QA.TA_RSI(data.close, timeperiod=12)
        CCI = QA.TA_CCI(data.high, data.low, data.close)
        KDJ = QA.TA_KDJ(data.high, data.low, data.close)    
        MAX_FACTOR = CCI[:,0] + (RSI[:,0] - 50) * 4 + (KDJ[:,2] - 50) * 4
        MAX_FACTOR_delta = np.r_[np.nan, np.diff(MAX_FACTOR)]
        REGRESSION_BASELINE = pd.Series((RSI[:,0] - 50) * 4, index=data.index)

        MAXFACTOR_CROSS = pd.DataFrame(columns=['MAXFACTOR_CROSS', 'MAXFACTOR_CROSS_JX', 'MAXFACTOR_CROSS_SX'], index=data.index)
        MAXFACTOR_CROSS = MAXFACTOR_CROSS.assign(MAXFACTOR=MAX_FACTOR)
        MAXFACTOR_CROSS = MAXFACTOR_CROSS.assign(MAXFACTOR_DELTA=MAX_FACTOR_delta)
        MAXFACTOR_CROSS = MAXFACTOR_CROSS.assign(REGRESSION_BASELINE=REGRESSION_BASELINE)

        MAXFACTOR_CROSS_JX1 = CROSS(MAX_FACTOR + MAX_FACTOR_delta, REGRESSION_BASELINE - 133)
        MAXFACTOR_CROSS_JX2 = CROSS(MAX_FACTOR + MAX_FACTOR_delta, REGRESSION_BASELINE)
        MAXFACTOR_CROSS_JX3 = CROSS(MAX_FACTOR + MAX_FACTOR_delta, REGRESSION_BASELINE + 133)
        MAXFACTOR_CROSS_JX = (MAXFACTOR_CROSS_JX1 | MAXFACTOR_CROSS_JX2 | MAXFACTOR_CROSS_JX3)
        MAXFACTOR_CROSS_SX1 = CROSS(REGRESSION_BASELINE + 133, MAX_FACTOR + MAX_FACTOR_delta)
        MAXFACTOR_CROSS_SX2 = CROSS(REGRESSION_BASELINE, MAX_FACTOR + MAX_FACTOR_delta)
        MAXFACTOR_CROSS_SX3 = CROSS(REGRESSION_BASELINE - 133, MAX_FACTOR + MAX_FACTOR_delta)
        MAXFACTOR_CROSS_SX = (MAXFACTOR_CROSS_SX1 | MAXFACTOR_CROSS_SX2 | MAXFACTOR_CROSS_SX3)
        MAXFACTOR_CROSS.loc[(MAXFACTOR_CROSS_JX1 | MAXFACTOR_CROSS_JX2 | MAXFACTOR_CROSS_JX3) == 1, 'MAXFACTOR_CROSS'] = 1
        MAXFACTOR_CROSS.loc[(MAXFACTOR_CROSS_SX1 | MAXFACTOR_CROSS_SX2 | MAXFACTOR_CROSS_SX3) == 1, 'MAXFACTOR_CROSS'] = -1
        MAXFACTOR_CROSS['MAXFACTOR_CROSS_JX'] = Timeline_Integral_with_cross_before(MAXFACTOR_CROSS_JX)
        MAXFACTOR_CROSS['MAXFACTOR_CROSS_SX'] = Timeline_Integral_with_cross_before(MAXFACTOR_CROSS_SX)
        return MAXFACTOR_CROSS

    # apply到 QADataStruct上

    ind1 = data_1h.add_func(ifup20_TA)
    ind2 = data_1h.add_func(ifmaxfactor_greater_TA)
    ind4 = data_1h.add_func(dual_cross)
    data_4h_maxfactor_cross = data_4h.add_func(maxfactor_cross)
    DUAL_CROSS_count = ind4['DUAL_CROSS'].dropna().groupby(level=0).sum() / len(codelist + QA.QAFetch.QAhuobi.FIRST_PRIORITY)
    #print(DUAL_CROSS_count)

    # 对于指标 groupby 日期 求和
    ma20_jx_count = ind1.dropna().groupby(level=0).sum() / ind1.get_code()
    MAX_FACTOR_jx_count = ind2.dropna().groupby(level=0).sum() / len(codelist + QA.QAFetch.QAhuobi.FIRST_PRIORITY)

    # 自定义指标极值点查找
    MA20_tp_min, MA20_tp_max = signal.argrelextrema(ma20_jx_count.values, np.less)[0], signal.argrelextrema(ma20_jx_count.values, np.greater)[0]
    MA20_tp_max = np.sort(np.r_[MA20_tp_max, signal.find_peaks(ma20_jx_count.values, width=8)[0]])
    MAX_FACTOR_tp_min, MAX_FACTOR_tp_max = signal.argrelextrema(MAX_FACTOR_jx_count.values, np.less)[0], signal.argrelextrema(MAX_FACTOR_jx_count.values, np.greater)[0]

    # 将极值点坐标标记写回 DataFrame 方便画图观察
    ma20_jx_count = pd.DataFrame(ma20_jx_count)
    ma20_jx_count = ma20_jx_count.assign(MA20_TP_CROSS_JX_MARK=None)
    ma20_jx_count.iloc[MA20_tp_min, ma20_jx_count.columns.get_loc('MA20_TP_CROSS_JX_MARK')] = ma20_jx_count.iloc[MA20_tp_min][0]
    ma20_jx_count = ma20_jx_count.assign(MA20_TP_CROSS_SX_MARK=None)
    ma20_jx_count.iloc[MA20_tp_max, ma20_jx_count.columns.get_loc('MA20_TP_CROSS_SX_MARK')] = ma20_jx_count.iloc[MA20_tp_max][0]

    MAX_FACTOR_jx_count = MAX_FACTOR_jx_count.assign(MAX_FACTOR_TP_CROSS_JX_MARK=None)
    MAX_FACTOR_jx_count.iloc[MAX_FACTOR_tp_min, MAX_FACTOR_jx_count.columns.get_loc('MAX_FACTOR_TP_CROSS_JX_MARK')] = MAX_FACTOR_jx_count.iloc[MAX_FACTOR_tp_min][0]
    MAX_FACTOR_jx_count = MAX_FACTOR_jx_count.assign(MAX_FACTOR_TP_CROSS_SX_MARK=None)
    MAX_FACTOR_jx_count.iloc[MAX_FACTOR_tp_max, MAX_FACTOR_jx_count.columns.get_loc('MAX_FACTOR_TP_CROSS_SX_MARK')] = MAX_FACTOR_jx_count.iloc[MAX_FACTOR_tp_max][0]

    # 利用极值点进行金叉死叉状态和趋势方向判断
    ma20_jx_count = ma20_jx_count.assign(MA20_TP_CROSS_JX=0)
    ma20_jx_count.iloc[MA20_tp_min, ma20_jx_count.columns.get_loc('MA20_TP_CROSS_JX')] = 1
    ma20_jx_count = ma20_jx_count.assign(MA20_TP_CROSS_SX=0)
    ma20_jx_count.iloc[MA20_tp_max, ma20_jx_count.columns.get_loc('MA20_TP_CROSS_SX')] = 1

    MAX_FACTOR_jx_count = MAX_FACTOR_jx_count.assign(MAX_FACTOR_TP_CROSS_JX=0)
    MAX_FACTOR_jx_count.iloc[MAX_FACTOR_tp_min, MAX_FACTOR_jx_count.columns.get_loc('MAX_FACTOR_TP_CROSS_JX')] = 1
    MAX_FACTOR_jx_count = MAX_FACTOR_jx_count.assign(MAX_FACTOR_TP_CROSS_SX=0)
    MAX_FACTOR_jx_count.iloc[MAX_FACTOR_tp_max, MAX_FACTOR_jx_count.columns.get_loc('MAX_FACTOR_TP_CROSS_SX')] = 1

    ma20_jx_count['MA20_TP_CROSS_JX'] = QA.Timeline_Integral_with_cross_before(ma20_jx_count['MA20_TP_CROSS_JX'])
    ma20_jx_count['MA20_TP_CROSS_SX'] = QA.Timeline_Integral_with_cross_before(ma20_jx_count['MA20_TP_CROSS_SX'])

    MAX_FACTOR_jx_count['MAX_FACTOR_TP_CROSS_JX'] = Timeline_Integral_with_cross_before(MAX_FACTOR_jx_count['MAX_FACTOR_TP_CROSS_JX'])
    MAX_FACTOR_jx_count['MAX_FACTOR_TP_CROSS_SX'] = Timeline_Integral_with_cross_before(MAX_FACTOR_jx_count['MAX_FACTOR_TP_CROSS_SX'])

    #照例，上面的自创指标出现 双金叉，就是买入点信号
    BUY_ACTION = (MAX_FACTOR_jx_count[0] < 0.382) & (MAX_FACTOR_jx_count['MAX_FACTOR_TP_CROSS_JX'] < MAX_FACTOR_jx_count['MAX_FACTOR_TP_CROSS_SX'])
    SELL_ACTION = (MAX_FACTOR_jx_count['MAX_FACTOR_TP_CROSS_SX'] < MAX_FACTOR_jx_count['MAX_FACTOR_TP_CROSS_JX'])
    BUY_ACTION2 = (ma20_jx_count['MA20_TP_CROSS_JX'] < ma20_jx_count['MA20_TP_CROSS_SX'])
    SELL_ACTION2 = (ma20_jx_count['MA20_TP_CROSS_SX'] < ma20_jx_count['MA20_TP_CROSS_JX'])
    BUY_ACTION = BUY_ACTION.tail(len(BUY_ACTION2))
    BUY_ACTION_DUAL = BUY_ACTION & BUY_ACTION2
    SELL_ACTION_DUAL = SELL_ACTION & SELL_ACTION2 | SELL_ACTION2 & ((MAX_FACTOR_jx_count[0] - ma20_jx_count[0]) < 0)
    #BUY_ACTION_DUAL = BUY_ACTION2
    BUY_ACTION_DUAL = BUY_ACTION_DUAL[BUY_ACTION_DUAL.apply(lambda x: x == True)]
    SELL_ACTION_DUAL = SELL_ACTION_DUAL[SELL_ACTION_DUAL.apply(lambda x: x == True)]

    # 画图看看
    data_4h_boll_cross = data_4h.add_func(boll_cross)

    hb10_1h = data_1h.select_code(['huobi'], ['btcusdt'])
    hb10_day = data_day.select_code(['huobi'], ['btcusdt'])

    hb10_ma30_cross = hb10_1h.add_func(ma30_cross)
    hb10_boll_cross = hb10_1h.add_func(boll_cross)
    #hb10_day_boll_cross = hb10_day.add_func(boll_cross_lf)
    hb10_day_boll_cross = hb10_day.add_func(boll_cross)

    # select_code 筛选过的单一代码数据，拆掉索引，免得计算过程中麻烦
    hb10_boll_cross = hb10_boll_cross.reset_index([1,2])
    hb10_day_boll_cross = hb10_day_boll_cross.reset_index([1,2])

    hb10_ma20_cross = hb10_1h.add_func(ifup20_TA).T
    hb10_ma20_cross.columns = [x[1] for x in hb10_ma20_cross.columns]
    hb10_ma20_cross = hb10_ma20_cross.reset_index([1,2])
    print(hb10_day_boll_cross.loc[pd.date_range('2020-02-01', periods=20, freq='D')])
    #print(hb10_ma20_cross)

    # 4H ——> 1H 跨周期策略比较，计算结果重采样到一致。
    data_4h_boll_cross.assign(ACTION=None)
    data_4h_boll_cross['ACTION'] = (data_4h_boll_cross['BOLL_CROSS_JX'] > 0)
    data_4h_boll_cross = data_4h_boll_cross.reset_index([1,2])
    hb10_day_boll_cross_to_1h = hb10_day_boll_cross.resample('1h').ffill()
    data_4h_boll_CROSS_to_1h = data_4h_boll_cross.resample('1h').ffill()
    print(data_4h_boll_cross.loc[[pd.Timestamp('2020-02-16 16:00:00'), pd.Timestamp('2020-02-16 20:00:00'), pd.Timestamp('2020-02-17 00:00:00')]])
    print(data_4h_boll_CROSS_to_1h.loc[[pd.Timestamp('2020-02-16 16:00:00'), pd.Timestamp('2020-02-16 17:00:00'), pd.Timestamp('2020-02-16 18:00:00'), pd.Timestamp('2020-02-16 19:00:00'), 
                                        pd.Timestamp('2020-02-16 20:00:00'), pd.Timestamp('2020-02-16 21:00:00'), pd.Timestamp('2020-02-16 22:00:00'), pd.Timestamp('2020-02-16 23:00:00'), 
                                        pd.Timestamp('2020-02-17 00:00:00'), pd.Timestamp('2020-02-17 01:00:00'), pd.Timestamp('2020-02-17 02:00:00'), pd.Timestamp('2020-02-17 03:00:00'), ]])
    
    data_4h_boll_CROSS_to_1h_action = data_4h_boll_CROSS_to_1h[data_4h_boll_CROSS_to_1h.apply(lambda x: x['ACTION'] == True, axis=1)]  # 去掉 False
    print(data_4h_boll_CROSS_to_1h_action)
    BOLL_CROSS_ACTION = ((hb10_boll_cross['BOLL_CROSS_JX'] > 0) & (data_4h_boll_CROSS_to_1h_action['ACTION'] == True) & (hb10_ma20_cross['btcusdt'] == True) & (hb10_boll_cross['BOLL_CROSS_JX'] < hb10_boll_cross['BOLL_CROSS_SX']))
    #DUAL_CROSS_ACTION = ((DUAL_CROSS_count > 0) &
    #(hb10_boll_cross['BOLL_CROSS_JX'] > 1))
    BOLL_CROSS_ACTION = BOLL_CROSS_ACTION[BOLL_CROSS_ACTION.apply(lambda x: x == True)]  # 去掉 False
    #DUAL_CROSS_SX = (DUAL_CROSS_count < 0) & (hb10_ma30_cross['MA30_CROSS_SX']
    #< hb10_ma30_cross['MA30_CROSS_JX']) & (hb10_ma20_cross['btcusdt'] ==
    #False)
    #DUAL_CROSS_SX = DUAL_CROSS_SX[DUAL_CROSS_SX.apply(lambda x: x == True)] #
    #去掉 False
    hb10_1h.data = hb10_1h.data.reset_index([1,2], drop=False)
    hb10_1h.data = hb10_1h.data.assign(BOLL_CROSS_JX_MARK=None)
    hb10_1h.data.loc[BOLL_CROSS_ACTION.index, 'DUAL_CROSS_JX_MARK'] = hb10_1h.data.loc[BOLL_CROSS_ACTION.index].close
    hb10_1h.data = hb10_1h.data.assign(BOLL_CROSS_SX_MARK=None)
    #hb10.data.loc[DUAL_CROSS_SX.index.get_level_values(level=0),
    #'DUAL_CROSS_SX_MARK'] =
    #hb10.data.loc[DUAL_CROSS_SX.index.get_level_values(level=0)].close
    
    # 打印出买入点信号日期
    #print(BUY_ACTION_DUAL.index)
    print('sell')
    print(SELL_ACTION_DUAL.index)

    # 画图看看
    fig = plt.figure()  
    ax1 = fig.add_subplot(111)  

    hb10_boll = TA_BBANDS(hb10_1h.data.close, timeperiod=20, nbdevup=2)
    #print(data2.data.close)
    #print(hb10.data.close)
    #hb10_kline = QA_Timekline(data2.data)
    #print(hb10_kline.indices['BOLL_UB'])
    #print(hb10_boll[:,0])
    ax1.plot(hb10_1h.data.index.get_level_values(level=0), hb10_1h.data.close.values,)
    ax1.plot(hb10_1h.data.index.get_level_values(level=0), hb10_boll[:,0], lw=1)
    ax1.plot(hb10_1h.data.index.get_level_values(level=0), hb10_boll[:,1], lw=1)
    ax1.plot(hb10_1h.data.index.get_level_values(level=0), hb10_boll[:,2], lw=1)
    #ax1.plot(MAX_FACTOR_jx_count[0])
    ax1.plot(hb10_1h.data['DUAL_CROSS_JX_MARK'],'ro')
    #ax1.plot(hb10.data['DUAL_CROSS_SX_MARK'],'bx')
    #hb10_kline.plot()
    plt.show()