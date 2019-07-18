

uri="http://mdfm.eastmoney.com/EM_UBG_MinuteApi/Js/Get\
?dtype=all&token=44c9d251add88e27b65ed86506f6e5da&rows=\
4000&cb=&page=1&id=6000121&gtvolume=&sort=asc&_=1534862271461"

# 日期       价格     手  1卖/2买            笔
# 09:30:04, 5.55,   10,  1,      -1, 9, 6, 2


# 字段	单位	备注
# 流入资金	万元	成交明细中方向识别为买入的成交
# 流出资金	万元	成交明细中方向识别为卖出的成交
# 净流入	万元	流入额-流出额
# 净流入率	%	净流入/成交额*100%
# 主力	　	单笔成交额>=100万元
# 散户	　	单笔成交额<=5万元
# 主力（散户）占比	%	主力（散户）净额/成交金额*100%
# 散单	　	单笔成交小于5万元
# 小单	　	单笔成交5万元-20万元
# 大单	　	单笔成交20万-100万元
# 特大单	　	单笔成交100万元以上
# 占成交额比	%	各分类净流入额与成交额总体的比值
# 占流通盘比	%	各分类净流入额与流通市值的比值

uri1="http://vip.stock.finance.sina.com.cn/quotes_service/api/\
json_v2.php/MoneyFlow.ssl_qsfx_lscjfb?page=1&num=20&sort=opendate&asc=0&daima=sh600012"

# 日期	         收盘价	涨跌幅	换手率	净流入率	             净流入/万
#                                                全部	    超大单	大单	    小单	     散单
# 2018-08-22	　5.59	-0.534%	0.1528%	-20.77%	 -206.90 	0.00  -197.93	-85.84	76.87
# {opendate:"2018-08-22",trade:"5.5900",changeratio:"-0.00533808",turnover:"15.2785",\
#  netamount:"-2069000.7800",ratioamount:"-0.207715",r0:"0.0000",r1:"1979283.4200",\
#  r2:"3464707.0000",r3:"4516841.2200",r0_net:"0.0000",r1_net:"-1979283.4200",\
#  r2_net:"-858401.0000",r3_net:"768683.6400"},


uri2="http://vip.stock.finance.sina.com.cn/quotes_service/api/\
json_v2.php/MoneyFlow.ssl_qsfx_zjlrqs?page=1&num=20&sort=opendate&asc=0&daima=sh600012"

# 日期	         收盘价	 涨跌幅	 换手率	净流入/万	 净流入率	主力净流入/万	主力净流入率	主力罗盘	行业净流入率
# 2018-08-22	　5.59	-0.534%	0.1528%	-206.90	-20.77%	   0.00	       0.00%   	180.00°	-12.80%

# {opendate:"2018-08-22",trade:"5.5900",changeratio:"-0.00533808",turnover:"15.2785",\
# netamount:"-2069000.7800",ratioamount:"-0.207715",r0_net:"0.0000",r0_ratio:"0.00000000",\
# r0x_ratio:"180",cnt_r0x_ratio:"2",cate_ra:"-0.128007",cate_na:"-433079636.9600"},
