#coding:utf-8
"""
QAWind

QAWind is a data fetch module just for WIND Institution Version

QAWind is under the [QAStandard#0.0.2 @101-1],[QAStandard#0.0.2 @501-0] protocol

@author: yutiansut

@last modified:2017/4/5
"""
import time
import datetime,re
import pymongo
from . import data_list as data_list
#from WindPy import w
#w.start()

#w.start()

#Stock
def QA_fetch_get_stock_info(name, startDate, endDate):
    from WindPy import w
    #w.start()
    w.start()
    w.isconnected()
    #get the all stock list on the endDate
    # judge the vaild date
    if(is_valid_date(endDate)==False):
        print ("wrong date")
    else :
        #tempStr='date='+endDate+";sectorid=a001010100000000"
        #data=w.wset("sectorconstituent",tempStr)
        data=w.wsd(name, "sec_name,sec_englishname,ipo_date,exch_city,mkt,sec_status,delist_date,issuecurrencycode,curr,RO,parvalue,lotsize,tunit,exch_eng,country,concept,marginornot,SHSC,parallelcode,sec_type,backdoor,backdoordate,windtype", startDate, endDate)
        #print(data)
        if (data.ErrorCode!=0):
            print ("Connent to Wind successfully")
            return data.Data
def QA_fetch_get_stock_day(name, startDate, endDate):
    from WindPy import w
    #w.start
    w.start()
    w.isconnected()
    if(is_valid_date(endDate)==False):
        print ("wrong date")
    else :
        print (w.isconnected())
        w.close()
        print (w.isconnected())
        w.start()
        print (w.isconnected())
        data=w.wsd(name,"sec_name,pre_close,open,high,low,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,adjfactor,turn,free_turn,lastradeday_s,last_trade_day,rel_ipo_chg,rel_ipo_pct_chg,trade_status,susp_days,susp_reason,maxupordown,open3,high3,low3,close3",startDate,endDate, "Fill=Previous;PriceAdj=F")
        #data=w.wsd("000002.SZ", "open,high,low,close,volume", "2017-03-03", "2017-04-01", "PriceAdj=B")
        print(data.ErrorCode)
        if (data.ErrorCode==0):
            print ("Connent to Wind successfully")
            return data.Data

def QA_fetch_get_stock_day_simple(name, startDate, endDate):
    from WindPy import w
    #w.start
    w.start()
    w.isconnected()
    if(is_valid_date(endDate)==False):
        print ("wrong date")
    else :
        data=w.wsd(name,"sec_name,preclose,open,high,low,close,volume",startDate,endDate, "Fill=Previous;PriceAdj=F")
        #data=w.wsd("000002.SZ", "open,high,low,close,volume", "2017-03-03", "2017-04-01", "PriceAdj=B")
        print(data.ErrorCode)
        if (data.ErrorCode==0):
            print ("Connent to Wind successfully")
            return data.Data
def QA_fetch_get_stock_indicator(name, startDate, endDate):
    from WindPy import w
    #w.start()
    w.start()
    w.isconnected()
    if(is_valid_date(endDate)==False):
        print ("wrong date")
    else :
        #ADTM动态买卖气指标,ATR真实波幅,BBI多空指数,BBIBOLL多空布林线,BIAS乖离率,BOLL布林带,CCI顺势指标,CDP逆势操作,DMA平均线差,DMI趋向标准,DPO区间震荡线,ENV,EXPMA指数平滑移动平均,KDJ随机指标,slowKD慢速kd,MA简单移动平均,MACD指数平滑移动平均,MIKE麦克指数,MTM动力指标,PRICEOSC价格震荡指标,PVT量价趋势指标,RC变化率指数,ROC变动速率,RSI相对强弱指标,SAR抛物转向,SI摆动指标,SOBV能量潮,SRMI MI修正指标,STD 标准差,TAPI 加权指数成交值,TRIX 三重指数平滑平均,VHF纵横指标,VMA量简单移动平均,VMACD量指数平滑移动平均,VOSC成交量震荡,WVAD威廉变异离散量,vol_ratio量比
        data=w.wsd(name, "ADTM,ATR,BBI,BBIBOLL,BIAS,BOLL,CCI,CDP,DMA,DMI,DPO,ENV,EXPMA,KDJ,slowKD,MA,MACD,MIKE,MTM,PRICEOSC,PVT,RC,ROC,RSI,SAR,SI,SOBV,SRMI,STD,TAPI,TRIX,VHF,VMA,VMACD,VOSC,WVAD,vol_ratio", startDate,endDate, "ADTM_N1=23;ADTM_N2=8;ADTM_IO=1;ATR_N=14;ATR_IO=1;BBI_N1=3;BBI_N2=6;BBI_N3=12;BBI_N4=24;BBIBOLL_N=10;BBIBOLL_Width=3;BBIBOLL_IO=1;BIAS_N=12;BOLL_N=26;BOLL_Width=2;BOLL_IO=1;CCI_N=14;CDP_IO=1;DMA_S=10;DMA_L=50;DMA_N=10;DMA_IO=1;DMI_N=14;DMI_N1=6;DMI_IO=1;DPO_N=20;DPO_M=6;DPO_IO=1;ENV_N=14;ENV_IO=1;EXPMA_N=12;KDJ_N=9;KDJ_M1=3;KDJ_M2=3;KDJ_IO=1;SlowKD_N1=9;SlowKD_N2=3;SlowKD_N3=3;SlowKD_N4=5;SlowKD_IO=1;MA_N=5;MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=1;MIKE_N=12;MIKE_IO=1;MTM_interDay=6;MTM_N=6;MTM_IO=1;PRICEOSC_L=26;PRICEOSC_S=12;RC_N=50;ROC_interDay=12;ROC_N=6;ROC_IO=1;RSI_N=6;SAR_N=4;SAR_SP=2;SAR_MP=20;SR    MI_N=9;STD_N=26;TAPI_N=6;TAPI_IO=1;TRIX_N1=12;TRIX_N2=20;TRIX_IO=1;VHF_N=28;VMA_N=5;VMACD_S=12;VMACD_L=26;VMACD_N=9;VMACD_IO=1;VOSC_S=12;VOSC_L=26;WVAD_N1=24;WVAD_N2=6;WVAD_IO=1;VolumeRatio_N=5")
        if (data.ErrorCode==0):
            print ("Connent to Wind successfully")
    return data.Data
def QA_fetch_get_stock_shape(name, startDate, endDate):
    from WindPy import w
    #w.start()
    w.start()
    w.isconnected()
    if(is_valid_date(endDate)==False):
        print ("wrong date")
    else :
        #history_low近期创历史新低,stage_high近期创阶段新高,history_high近期创历史新高,stage_low近期创阶段新高,up_days连涨天数,down_days连跌天数,breakout_ma向上有效突破均线,breakdown_ma向下有效突破均线,bull_bear_ma均线多空排列看涨看跌
        data=w.wsd(name, "history_low,stage_high,history_high,stage_low,up_days,down_days,breakout_ma,breakdown_ma,bull_bear_ma", startDate, endDate, "n=3;m=60;meanLine=60;N1=5;N2=10;N3=20;N4=30;upOrLow=1")
        if (data.ErrorCode==0):
            print ("Connent to Wind successfully")
    return data.Data
def QA_fetch_get_stock_risk(name, startDate, endDate):
    from WindPy import w
    w.start()
    w.isconnected()
    if(is_valid_date(endDate)==False):
        print ("wrong date")
    else :
        data=w.wsd(name, "annualyeild_100w,annualyeild_24m,annualyeild_60m,annualstdevr_100w,annualstdevr_24m,annualstdevr_60m,beta_100w,beta_24m,beta_60m,avgreturn,avgreturny,stdevry,stdcof,risk_nonsysrisk1,r2,alpha2,beta,sharpe,treynor,jensen,jenseny,betadf", startDate, endDate, "period=2;returnType=1;index=000001.SH;yield=1")
        if (data.ErrorCode==0):
            print ("Connent to Wind successfully")
    return data.Data
def QA_fetch_get_stock_xueqiu(name, startDate, endDate):
    from WindPy import w
    #w.start()
    w.start()
    w.isconnected()
    if(is_valid_date(endDate)==False):
        print ("wrong date")
    else :
        data=w.wsd(name, "xq_accmfocus,xq_accmcomments,xq_accmshares,xq_focusadded,xq_commentsadded,xq_sharesadded,xq_WOW_focus,xq_WOW_comments,xq_WOW_shares", startDate, endDate, "")
        if (data.ErrorCode==0):
            print ("Connent to Wind successfully")
    return data.Data
def QA_fetch_get_stock_financial(name, startDate, endDate):
    from WindPy import w
    #w.start()
    w.start()
    w.isconnected()
    pass
def is_valid_date(str):
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False
        
def QA_fetch_get_trade_date(endDate, exchange):
    from WindPy import w
    #w.start()
    w.start()
    w.isconnected()
    supportExchanges=["SSE","SZSE","CFFEX","SHFE","DCE","CZCE"]
    if (exchange in supportExchanges):
    #"SSE","SZSE","CFFEX","SHFE","DCE","CZCE"
    #上海股票交易所,深圳股票交易所,中国金融期货交易所,上海期货交易所,大连商品交易所,郑州期货交易所
        exchanges="TradingCalendar="+exchange
        data=w.tdays("1990-01-01", endDate, exchanges)
        #print(data.Data)
        dates=data.Data
    else: 
        print("exchange name problem")
    return dates


def QA_fetch_get_stock_list(date):
    
    #w.start()
    w.start()
    w.isconnected()
    if(is_valid_date(date)==False):
        print ("wrong date")
    else :
        awgs='date='+date+';sectorid=a001010100000000'
        data=w.wset("sectorconstituent",awgs)
        return data.Data

def QA_fetch_get_stock_list_special(date,id):
    from WindPy import w
        #w.start()
    w.start()
    w.isconnected()
    if(is_valid_date(date)==False):
        print ("wrong date")
    else :
        # 
        #
        if id in ['big','small','cixin','yujing','rzrq','rq','yj','st','sst']:
            awgs='date='+date+';sectorid='+data_list.wind_stock_list_special_id[id]
            data=w.wset("sectorconstituent",awgs)
            return data.Data


        