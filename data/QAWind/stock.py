#coding:utf-8

import time
import datetime,re
import pymongo
from WindPy import w
w.start()


#Stock
def getStockInfo(startDate,endDate,name):
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
def getStockData_day(startDate,endDate,name):
    if(is_valid_date(endDate)==False):
        print ("wrong date")
    else :
        data=w.wsd(name,"sec_name,pre_close,open,high,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,adjfactor,turn,free_turn,lastradeday_s,last_trade_day,rel_ipo_chg,rel_ipo_pct_chg,trade_status,susp_days,susp_reason,maxupordown,open3,high3,low3,close3",startDate,endDate, "Fill=Previous;PriceAdj=F")
        print(data)
        if (data.ErrorCode==0):
            print ("Connent to Wind successfully")
    return data.Data
def getStockindex(startDate,endDate,name):
    if(is_valid_date(endDate)==False):
        print ("wrong date")
    else :
        w.wsd(name, "ADTM,ATR,BBI,BBIBOLL,BIAS,BOLL,CCI,CDP,DMA,DMI,DPO,ENV,EXPMA,KDJ,slowKD,MA,MACD,MIKE,MTM,PRICEOSC,PVT,RC,ROC,RSI,SAR,SI,SOBV,SRMI,STD,TAPI,TRIX,VHF,VMA,VMACD,VOSC,WVAD,vol_ratio", startDate,endDate, "ADTM_N1=23;ADTM_N2=8;ADTM_IO=1;ATR_N=14;ATR_IO=1;BBI_N1=3;BBI_N2=6;BBI_N3=12;BBI_N4=24;BBIBOLL_N=10;BBIBOLL_Width=3;BBIBOLL_IO=1;BIAS_N=12;BOLL_N=26;BOLL_Width=2;BOLL_IO=1;CCI_N=14;CDP_IO=1;DMA_S=10;DMA_L=50;DMA_N=10;DMA_IO=1;DMI_N=14;DMI_N1=6;DMI_IO=1;DPO_N=20;DPO_M=6;DPO_IO=1;ENV_N=14;ENV_IO=1;EXPMA_N=12;KDJ_N=9;KDJ_M1=3;KDJ_M2=3;KDJ_IO=1;SlowKD_N1=9;SlowKD_N2=3;SlowKD_N3=3;SlowKD_N4=5;SlowKD_IO=1;MA_N=5;MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=1;MIKE_N=12;MIKE_IO=1;MTM_interDay=6;MTM_N=6;MTM_IO=1;PRICEOSC_L=26;PRICEOSC_S=12;RC_N=50;ROC_interDay=12;ROC_N=6;ROC_IO=1;RSI_N=6;SAR_N=4;SAR_SP=2;SAR_MP=20;SRMI_N=9;STD_N=26;TAPI_N=6;TAPI_IO=1;TRIX_N1=12;TRIX_N2=20;TRIX_IO=1;VHF_N=28;VMA_N=5;VMACD_S=12;VMACD_L=26;VMACD_N=9;VMACD_IO=1;VOSC_S=12;VOSC_L=26;WVAD_N1=24;WVAD_N2=6;WVAD_IO=1;VolumeRatio_N=5")
        if (data.ErrorCode==0):
            print ("Connent to Wind successfully")
    return data.Data

def is_valid_date(str):
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False
        
def test():
    #a=getStockInfo("2000-01-01","2017-03-29","000001.SZ")
    a=getStockData_day("2000-01-01","2015-03-29","000001.SZ")
    print (a)
test()
