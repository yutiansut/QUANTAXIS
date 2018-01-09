

```python
import QUANTAXIS as QA
import random
market = QA.QA_Market()
user = QA.QA_Portfolio()
# 创建两个account
# 这里是创建一个资产组合,然后在组合里面创建两个account  你可以想象成股票里面的两个策略账户
# 然后返回的是这个账户的id
a_1 = user.new_account()

market.start()
market.connect(QA.RUNNING_ENVIRONMENT.BACKETEST)

# 打印market
print(market)


"""
登陆到这个交易前置上 把你刚才的两个账户
"""
# 登陆交易
market.login(QA.BROKER_TYPE.BACKETEST, a_1, user.get_account(a_1))
for date in QA.QA_util_get_trade_range('2017-01-01','2017-01-31'):
    for code in ['000001', '000002', '000004', '000007']:
        if random.random()<0.5:
            market.insert_order(account_id=a_1, amount=1000, price=None, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT, time=date, code=code,
                                order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.BUY, market_type=QA.MARKET_TYPE.STOCK_DAY,
                                data_type=QA.MARKETDATA_TYPE.DAY, broker_name=QA.BROKER_TYPE.BACKETEST)
        else:
            try:
                market.insert_order(account_id=a_1, amount=1000, price=None, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT, time=date, code=code,
                                    order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.SELL, market_type=QA.MARKET_TYPE.STOCK_DAY,
                                    data_type=QA.MARKETDATA_TYPE.DAY, broker_name=QA.BROKER_TYPE.BACKETEST)
            except:
                pass
    market._settle(QA.BROKER_TYPE.BACKETEST)
        
while True:
    if market.clear():
        break
print(user.get_account(a_1).history)
print(user.get_account(a_1).cash)
print(user.get_account(a_1).cash_available)
print(user.get_account(a_1).history_table)
print(user.get_account(a_1).hold)

```

    QUANTAXIS>> start QUANTAXIS
    QUANTAXIS>> Selecting the Best Server IP of TDX
    QUANTAXIS>> === The BEST SERVER ===
     stock_ip 218.75.126.9 future_ip 61.152.107.141
    QUANTAXIS>> Welcome to QUANTAXIS, the Version is remake-version
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
      ``#########``````########```##``````````````###`##``````````##```````##``##````````````##`##``````##````##`````##````## 
      ````````#####`````````````````````````````````````````````````````````````````````````````````````````````````````####` 
      ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
      ``````````````````````````Copyright``yutiansut``2017``````QUANTITATIVE FINANCIAL FRAMEWORK````````````````````````````` 
      ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
     ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
     ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` 
     
    

    < QA_MARKET with ['backtest'] Broker >
    < QA_Order datetime:2017-01-03 09:31:00 code:000002 price:20.73 towards:1 btype:0x01 order_id:Order_qD7NezRt account:Acc_5dFLiKEG status:300 >
    ===== SETTLED None =====
    ===== SETTLED None =====< QA_Order datetime:2017-01-03 09:31:00 code:000004 price:44.45 towards:1 btype:0x01 order_id:Order_wCmTcb96 account:Acc_5dFLiKEG status:300 >
    
    ===== SETTLED None =====
    < QA_Order datetime:2017-01-03 09:31:00 code:000007 price:26.1 towards:1 btype:0x01 order_id:Order_u8stOwGg account:Acc_5dFLiKEG status:300 >
    ===== SETTLED None =====< QA_Order datetime:2017-01-04 09:31:00 code:000001 price:9.16 towards:1 btype:0x01 order_id:Order_7IXP5NFn account:Acc_5dFLiKEG status:300 >
    
    < QA_Order datetime:2017-01-04 09:31:00 code:000004 price:44.7 towards:1 btype:0x01 order_id:Order_MShxXan2 account:Acc_5dFLiKEG status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-04 09:31:00 code:000007 price:26.47 towards:1 btype:0x01 order_id:Order_rKC2vRnq account:Acc_5dFLiKEG status:300 >
    ===== SETTLED None =====< QA_Order datetime:2017-01-05 09:31:00 code:000002 price:20.93 towards:1 btype:0x01 order_id:Order_jkxOGbhE account:Acc_5dFLiKEG status:300 >
    
    < QA_Order datetime:2017-01-06 09:31:00 code:000002 price:20.64 towards:1 btype:0x01 order_id:Order_Q0oPdXkZ account:Acc_5dFLiKEG status:300 >===== SETTLED None =====
    
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    < QA_Order datetime:2017-01-06 09:31:00 code:000007 price:25.45 towards:1 btype:0x01 order_id:Order_sF7J31mO account:Acc_5dFLiKEG status:300 >

    
    

    
    

    QUANTAXIS>> code 000002 date 2017-01-12 price None order_model close amount_model by_amount

    < QA_Order datetime:2017-01-09 09:31:00 code:000002 price:20.66 towards:1 btype:0x01 order_id:Order_tqROyjWx account:Acc_5dFLiKEG status:300 >

    
    

    
    < QA_Order datetime:2017-01-09 09:31:00 code:000004 price:43.01 towards:1 btype:0x01 order_id:Order_qWytne8G account:Acc_5dFLiKEG status:300 >
    ===== SETTLED None =====
    < QA_Order datetime:2017-01-09 09:31:00 code:000007 price:25.09 towards:1 btype:0x01 order_id:Order_ziThVZ79 account:Acc_5dFLiKEG status:300 >
    ===== SETTLED None =====
    < QA_Order datetime:2017-01-10 09:31:00 code:000001 price:9.15 towards:1 btype:0x01 order_id:Order_KdHhs9fz account:Acc_5dFLiKEG status:300 >
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    

    < QA_Order datetime:2017-01-10 09:31:00 code:000002 price:20.58 towards:-1 btype:0x01 order_id:Order_svGIw9g8 account:Acc_5dFLiKEG status:300 >

    QUANTAXIS>> code 000007 date 2017-01-16 price None order_model close amount_model by_amount

    
    

    
    

    < QA_Order datetime:2017-01-10 09:31:00 code:000004 price:43.25 towards:-1 btype:0x01 order_id:Order_zst497J2 account:Acc_5dFLiKEG status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-10 09:31:00 code:000007 price:24.79 towards:-1 btype:0x01 order_id:Order_fPorXvb5 account:Acc_5dFLiKEG status:300 >
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    

    < QA_Order datetime:2017-01-11 09:31:00 code:000001 price:9.14 towards:1 btype:0x01 order_id:Order_Hy4EuL5s account:Acc_5dFLiKEG status:300 >
    

    QUANTAXIS>> code 000007 date 2017-01-17 price None order_model close amount_model by_amount

    < QA_Order datetime:2017-01-11 09:31:00 code:000002 price:20.4 towards:-1 btype:0x01 order_id:Order_ft0UpN6C account:Acc_5dFLiKEG status:300 >

    
    

    
    ===== SETTLED None =====< QA_Order datetime:2017-01-11 09:31:00 code:000004 price:42.45 towards:1 btype:0x01 order_id:Order_Pg5eGyI2 account:Acc_5dFLiKEG status:300 >
    
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    

    < QA_Order datetime:2017-01-11 09:31:00 code:000007 price:24.85 towards:1 btype:0x01 order_id:Order_cvMGAFy8 account:Acc_5dFLiKEG status:300 >

    QUANTAXIS>> code 000007 date 2017-01-18 price None order_model close amount_model by_amount

    
    

    
    

    ===== SETTLED None =====< QA_Order datetime:2017-01-12 09:31:00 code:000001 price:9.15 towards:-1 btype:0x01 order_id:Order_RtlPAFei account:Acc_5dFLiKEG status:300 >
    
    < QA_Order datetime:2017-01-12 09:31:00 code:000004 price:42.05 towards:-1 btype:0x01 order_id:Order_0Dn6tYr7 account:Acc_5dFLiKEG status:300 >
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    QUANTAXIS>> code 000007 date 2017-01-19 price None order_model close amount_model by_amount

    < QA_Order datetime:2017-01-12 09:31:00 code:000007 price:24.61 towards:-1 btype:0x01 order_id:Order_72ayebkG account:Acc_5dFLiKEG status:300 >

    
    

    
    ===== SETTLED None =====
    < QA_Order datetime:2017-01-13 09:31:00 code:000001 price:9.16 towards:-1 btype:0x01 order_id:Order_iy43nmaH account:Acc_5dFLiKEG status:300 >
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    < QA_Order datetime:2017-01-13 09:31:00 code:000002 price:21.81 towards:-1 btype:0x01 order_id:Order_GePWHtca account:Acc_5dFLiKEG status:300 >

    
    

    
    

    QUANTAXIS>> code 000007 date 2017-01-20 price None order_model close amount_model by_amount

    < QA_Order datetime:2017-01-13 09:31:00 code:000004 price:41.0 towards:1 btype:0x01 order_id:Order_hCmPEodp account:Acc_5dFLiKEG status:300 >

    
    

    
    ===== SETTLED None =====< QA_Order datetime:2017-01-13 09:31:00 code:000007 price:23.81 towards:-1 btype:0x01 order_id:Order_bjLSasGl account:Acc_5dFLiKEG status:300 >
    
    < QA_Order datetime:2017-01-16 09:31:00 code:000002 price:21.0 towards:-1 btype:0x01 order_id:Order_NifFeo6d account:Acc_5dFLiKEG status:300 >

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    
    

    
    QUANTAXIS>> code 000007 date 2017-01-23 price None order_model close amount_model by_amount

    < QA_Order datetime:2017-01-16 09:31:00 code:000004 price:38.26 towards:-1 btype:0x01 order_id:Order_TLWHRXh8 account:Acc_5dFLiKEG status:300 >

    
    

    
    ===== SETTLED None =====< QA_Order datetime:2017-01-17 09:31:00 code:000001 price:9.15 towards:-1 btype:0x01 order_id:Order_GfYcXjlW account:Acc_5dFLiKEG status:300 >
    
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    < QA_Order datetime:2017-01-17 09:31:00 code:000002 price:20.8 towards:-1 btype:0x01 order_id:Order_lxnGy6kO account:Acc_5dFLiKEG status:300 >

    
    

    
    

    QUANTAXIS>> code 000007 date 2017-01-24 price None order_model close amount_model by_amount
    

    < QA_Order datetime:2017-01-17 09:31:00 code:000004 price:37.37 towards:1 btype:0x01 order_id:Order_wLXiE3sT account:Acc_5dFLiKEG status:300 >
    < QA_Order datetime:2017-01-18 09:31:00 code:000001 price:9.17 towards:1 btype:0x01 order_id:Order_Zjwk6oEQ account:Acc_5dFLiKEG status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-18 09:31:00 code:000002 price:20.92 towards:-1 btype:0x01 order_id:Order_BsdtqSRD account:Acc_5dFLiKEG status:300 >
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    

    < QA_Order datetime:2017-01-18 09:31:00 code:000004 price:37.15 towards:-1 btype:0x01 order_id:Order_L2tBAEDw account:Acc_5dFLiKEG status:300 >

    QUANTAXIS>> code 000007 date 2017-01-25 price None order_model close amount_model by_amount

    
    

    
    

    < QA_Order datetime:2017-01-19 09:31:00 code:000001 price:9.18 towards:-1 btype:0x01 order_id:Order_jLKnzptg account:Acc_5dFLiKEG status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-19 09:31:00 code:000002 price:20.6 towards:-1 btype:0x01 order_id:Order_pboORh93 account:Acc_5dFLiKEG status:300 >

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    
    

    
    

    < QA_Order datetime:2017-01-19 09:31:00 code:000004 price:35.69 towards:-1 btype:0x01 order_id:Order_uYnJAc9x account:Acc_5dFLiKEG status:300 >

    QUANTAXIS>> code 000007 date 2017-01-26 price None order_model close amount_model by_amount
    

    
    < QA_Order datetime:2017-01-20 09:31:00 code:000001 price:9.22 towards:1 btype:0x01 order_id:Order_jT1mtsLc account:Acc_5dFLiKEG status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-20 09:31:00 code:000002 price:20.68 towards:-1 btype:0x01 order_id:Order_DdlSYfz9 account:Acc_5dFLiKEG status:300 >
    < QA_Order datetime:2017-01-20 09:31:00 code:000004 price:36.48 towards:1 btype:0x01 order_id:Order_kT3C91Js account:Acc_5dFLiKEG status:300 >
    < QA_Order datetime:2017-01-23 09:31:00 code:000001 price:9.22 towards:-1 btype:0x01 order_id:Order_BWQzvSZV account:Acc_5dFLiKEG status:300 >
    < QA_Order datetime:2017-01-23 09:31:00 code:000002 price:20.74 towards:1 btype:0x01 order_id:Order_Ns1I8zyi account:Acc_5dFLiKEG status:300 >
    < QA_Order datetime:2017-01-23 09:31:00 code:000004 price:37.56 towards:1 btype:0x01 order_id:Order_sW5NpLrZ account:Acc_5dFLiKEG status:300 >
    < QA_Order datetime:2017-01-24 09:31:00 code:000001 price:9.27 towards:1 btype:0x01 order_id:Order_Ed5pn8hW account:Acc_5dFLiKEG status:300 >
    < QA_Order datetime:2017-01-24 09:31:00 code:000002 price:20.69 towards:1 btype:0x01 order_id:Order_IBodSh0G account:Acc_5dFLiKEG status:300 >
    < QA_Order datetime:2017-01-24 09:31:00 code:000004 price:38.63 towards:-1 btype:0x01 order_id:Order_E6Nfvkp1 account:Acc_5dFLiKEG status:300 >
    < QA_Order datetime:2017-01-25 09:31:00 code:000002 price:20.61 towards:1 btype:0x01 order_id:Order_gBxjODyY account:Acc_5dFLiKEG status:300 >
    < QA_Order datetime:2017-01-25 09:31:00 code:000004 price:38.25 towards:-1 btype:0x01 order_id:Order_AdWkxYQr account:Acc_5dFLiKEG status:300 >
    < QA_Order datetime:2017-01-26 09:31:00 code:000001 price:9.33 towards:-1 btype:0x01 order_id:Order_AEdwvGom account:Acc_5dFLiKEG status:300 >
    < QA_Order datetime:2017-01-26 09:31:00 code:000004 price:38.29 towards:1 btype:0x01 order_id:Order_9eiqlU7n account:Acc_5dFLiKEG status:300 >
    [['2017-01-03 09:31:00', '000002', 20.73, 1000.0, 'Order_qD7NezRt', 'Trade_jvVQfoGn', 31.095000000000002], ['2017-01-03 09:31:00', '000004', 44.45, 1000.0, 'Order_wCmTcb96', 'Trade_RNmWeFZn', 66.67500000000001], ['2017-01-03 09:31:00', '000007', 26.1, 1000.0, 'Order_u8stOwGg', 'Trade_8NPLDMXV', 39.150000000000006], ['2017-01-04 09:31:00', '000001', 9.16, 1000.0, 'Order_7IXP5NFn', 'Trade_3vNUoPfb', 13.74], ['2017-01-04 09:31:00', '000004', 44.7, 1000.0, 'Order_MShxXan2', 'Trade_VgazesrI', 67.05000000000001], ['2017-01-04 09:31:00', '000007', 26.47, 1000.0, 'Order_rKC2vRnq', 'Trade_n6FmXLCE', 39.705], ['2017-01-05 09:31:00', '000002', 20.93, 1000.0, 'Order_jkxOGbhE', 'Trade_8mHaBhfn', 31.395], ['2017-01-06 09:31:00', '000002', 20.64, 1000.0, 'Order_Q0oPdXkZ', 'Trade_s1ykwzmd', 30.96], ['2017-01-06 09:31:00', '000007', 25.45, 1000.0, 'Order_sF7J31mO', 'Trade_ECcve0xs', 38.175], ['2017-01-09 09:31:00', '000002', 20.66, 1000.0, 'Order_tqROyjWx', 'Trade_JWhDNaKZ', 30.99], ['2017-01-09 09:31:00', '000004', 43.01, 1000.0, 'Order_qWytne8G', 'Trade_xbia8Z40', 64.515], ['2017-01-09 09:31:00', '000007', 25.09, 1000.0, 'Order_ziThVZ79', 'Trade_PdlqSB6y', 37.635000000000005], ['2017-01-10 09:31:00', '000001', 9.15, 1000.0, 'Order_KdHhs9fz', 'Trade_Qm16wOg5', 13.725000000000001], ['2017-01-10 09:31:00', '000002', 20.58, -1000.0, 'Order_svGIw9g8', 'Trade_gyKlO4Ni', 30.869999999999997], ['2017-01-10 09:31:00', '000004', 43.25, -1000.0, 'Order_zst497J2', 'Trade_adfjV8ZA', 64.875], ['2017-01-10 09:31:00', '000007', 24.79, -1000.0, 'Order_fPorXvb5', 'Trade_YiK9qIE2', 37.185], ['2017-01-11 09:31:00', '000001', 9.14, 1000.0, 'Order_Hy4EuL5s', 'Trade_BZLgsvct', 13.71], ['2017-01-11 09:31:00', '000002', 20.4, -1000.0, 'Order_ft0UpN6C', 'Trade_jyS4ULQ9', 30.599999999999998], ['2017-01-11 09:31:00', '000004', 42.45, 1000.0, 'Order_Pg5eGyI2', 'Trade_7QHRwdOW', 63.67500000000001], ['2017-01-11 09:31:00', '000007', 24.85, 1000.0, 'Order_cvMGAFy8', 'Trade_5yBD2rml', 37.275000000000006], ['2017-01-12 09:31:00', '000001', 9.15, -1000.0, 'Order_RtlPAFei', 'Trade_q80zHrE7', 13.725000000000001], ['2017-01-12 09:31:00', '000004', 42.05, -1000.0, 'Order_0Dn6tYr7', 'Trade_dfM1gYA5', 63.07499999999999], ['2017-01-12 09:31:00', '000007', 24.61, -1000.0, 'Order_72ayebkG', 'Trade_Xz2aBb4f', 36.915000000000006], ['2017-01-13 09:31:00', '000001', 9.16, -1000.0, 'Order_iy43nmaH', 'Trade_Ix7B34cT', 13.74], ['2017-01-13 09:31:00', '000002', 21.81, -1000.0, 'Order_GePWHtca', 'Trade_MUdBTinP', 32.715], ['2017-01-13 09:31:00', '000004', 41.0, 1000.0, 'Order_hCmPEodp', 'Trade_4tAxRTdB', 61.5], ['2017-01-13 09:31:00', '000007', 23.81, -1000.0, 'Order_bjLSasGl', 'Trade_DFw14fYj', 35.714999999999996], ['2017-01-16 09:31:00', '000002', 21.0, -1000.0, 'Order_NifFeo6d', 'Trade_QDfBxAO6', 31.5], ['2017-01-16 09:31:00', '000004', 38.26, -1000.0, 'Order_TLWHRXh8', 'Trade_UaLQt10y', 57.38999999999999], ['2017-01-17 09:31:00', '000001', 9.15, -1000.0, 'Order_GfYcXjlW', 'Trade_vHqF8hBr', 13.725000000000001], ['2017-01-17 09:31:00', '000002', 20.8, -1000.0, 'Order_lxnGy6kO', 'Trade_U5EgWJQX', 31.200000000000003], ['2017-01-17 09:31:00', '000004', 37.37, 1000.0, 'Order_wLXiE3sT', 'Trade_d3hwFqy9', 56.055], ['2017-01-18 09:31:00', '000001', 9.17, 1000.0, 'Order_Zjwk6oEQ', 'Trade_MFzfnsZG', 13.754999999999999], ['2017-01-18 09:31:00', '000002', 20.92, -1000.0, 'Order_BsdtqSRD', 'Trade_Xm2RcPEu', 31.380000000000006], ['2017-01-18 09:31:00', '000004', 37.15, -1000.0, 'Order_L2tBAEDw', 'Trade_0jvMGLDs', 55.724999999999994], ['2017-01-19 09:31:00', '000001', 9.18, -1000.0, 'Order_jLKnzptg', 'Trade_mz0U7a6p', 13.77], ['2017-01-19 09:31:00', '000002', 20.6, -1000.0, 'Order_pboORh93', 'Trade_cqnR4Y0s', 30.900000000000002], ['2017-01-19 09:31:00', '000004', 35.69, -1000.0, 'Order_uYnJAc9x', 'Trade_w5cuNIea', 53.535], ['2017-01-20 09:31:00', '000001', 9.22, 1000.0, 'Order_jT1mtsLc', 'Trade_qQFhkBrV', 13.830000000000002], ['2017-01-20 09:31:00', '000002', 20.68, -1000.0, 'Order_DdlSYfz9', 'Trade_vnemBp8r', 31.02], ['2017-01-20 09:31:00', '000004', 36.48, 1000.0, 'Order_kT3C91Js', 'Trade_1ul5aIWf', 54.72], ['2017-01-23 09:31:00', '000001', 9.22, -1000.0, 'Order_BWQzvSZV', 'Trade_Z5iLcCFP', 13.830000000000002], ['2017-01-23 09:31:00', '000002', 20.74, 1000.0, 'Order_Ns1I8zyi', 'Trade_kbl7xa4O', 31.11], ['2017-01-23 09:31:00', '000004', 37.56, 1000.0, 'Order_sW5NpLrZ', 'Trade_ri0QXxYP', 56.34], ['2017-01-24 09:31:00', '000001', 9.27, 1000.0, 'Order_Ed5pn8hW', 'Trade_x60OmP5z', 13.905], ['2017-01-24 09:31:00', '000002', 20.69, 1000.0, 'Order_IBodSh0G', 'Trade_tBw2JocE', 31.035000000000004], ['2017-01-24 09:31:00', '000004', 38.63, -1000.0, 'Order_E6Nfvkp1', 'Trade_uGN5jM4a', 57.945], ['2017-01-25 09:31:00', '000002', 20.61, 1000.0, 'Order_gBxjODyY', 'Trade_v2brxVKi', 30.915000000000003], ['2017-01-25 09:31:00', '000004', 38.25, -1000.0, 'Order_AdWkxYQr', 'Trade_qOLzc8UC', 57.375], ['2017-01-26 09:31:00', '000001', 9.33, -1000.0, 'Order_AEdwvGom', 'Trade_SlaG5L1W', 13.995000000000001], ['2017-01-26 09:31:00', '000004', 38.29, 1000.0, 'Order_9eiqlU7n', 'Trade_A36OPsc1', 57.435]]
    [1000000, 979238.905, 934722.23, 908583.08, 899409.34, 854642.2899999999, 828132.585, 807171.19, 786500.23, 761012.0549999999, 740321.065, 697246.5499999999, 672118.9149999999, 662955.19, 683504.32, 726689.445, 751442.2599999999, 742288.5499999999, 762657.95, 720144.2749999999, 695256.9999999999, 704393.2749999999, 746380.2, 770953.2849999999, 780099.5449999999, 801876.83, 760815.33, 784589.615, 805558.115, 843760.725, 852897.0, 873665.8, 836239.745, 827055.99, 847944.61, 885038.885, 894205.115, 914774.215, 950410.6799999999, 941176.85, 961825.83, 925291.11, 934497.28, 913726.17, 876109.8300000001, 866825.925, 846104.89, 884676.9450000001, 864036.03, 902228.655, 911544.66, 873197.225]
    873197.225
                   datetime    code  price  amount        order_id  \
    0   2017-01-03 09:31:00  000002  20.73  1000.0  Order_qD7NezRt   
    1   2017-01-03 09:31:00  000004  44.45  1000.0  Order_wCmTcb96   
    2   2017-01-03 09:31:00  000007  26.10  1000.0  Order_u8stOwGg   
    3   2017-01-04 09:31:00  000001   9.16  1000.0  Order_7IXP5NFn   
    4   2017-01-04 09:31:00  000004  44.70  1000.0  Order_MShxXan2   
    5   2017-01-04 09:31:00  000007  26.47  1000.0  Order_rKC2vRnq   
    6   2017-01-05 09:31:00  000002  20.93  1000.0  Order_jkxOGbhE   
    7   2017-01-06 09:31:00  000002  20.64  1000.0  Order_Q0oPdXkZ   
    8   2017-01-06 09:31:00  000007  25.45  1000.0  Order_sF7J31mO   
    9   2017-01-09 09:31:00  000002  20.66  1000.0  Order_tqROyjWx   
    10  2017-01-09 09:31:00  000004  43.01  1000.0  Order_qWytne8G   
    11  2017-01-09 09:31:00  000007  25.09  1000.0  Order_ziThVZ79   
    12  2017-01-10 09:31:00  000001   9.15  1000.0  Order_KdHhs9fz   
    13  2017-01-10 09:31:00  000002  20.58 -1000.0  Order_svGIw9g8   
    14  2017-01-10 09:31:00  000004  43.25 -1000.0  Order_zst497J2   
    15  2017-01-10 09:31:00  000007  24.79 -1000.0  Order_fPorXvb5   
    16  2017-01-11 09:31:00  000001   9.14  1000.0  Order_Hy4EuL5s   
    17  2017-01-11 09:31:00  000002  20.40 -1000.0  Order_ft0UpN6C   
    18  2017-01-11 09:31:00  000004  42.45  1000.0  Order_Pg5eGyI2   
    19  2017-01-11 09:31:00  000007  24.85  1000.0  Order_cvMGAFy8   
    20  2017-01-12 09:31:00  000001   9.15 -1000.0  Order_RtlPAFei   
    21  2017-01-12 09:31:00  000004  42.05 -1000.0  Order_0Dn6tYr7   
    22  2017-01-12 09:31:00  000007  24.61 -1000.0  Order_72ayebkG   
    23  2017-01-13 09:31:00  000001   9.16 -1000.0  Order_iy43nmaH   
    24  2017-01-13 09:31:00  000002  21.81 -1000.0  Order_GePWHtca   
    25  2017-01-13 09:31:00  000004  41.00  1000.0  Order_hCmPEodp   
    26  2017-01-13 09:31:00  000007  23.81 -1000.0  Order_bjLSasGl   
    27  2017-01-16 09:31:00  000002  21.00 -1000.0  Order_NifFeo6d   
    28  2017-01-16 09:31:00  000004  38.26 -1000.0  Order_TLWHRXh8   
    29  2017-01-17 09:31:00  000001   9.15 -1000.0  Order_GfYcXjlW   
    30  2017-01-17 09:31:00  000002  20.80 -1000.0  Order_lxnGy6kO   
    31  2017-01-17 09:31:00  000004  37.37  1000.0  Order_wLXiE3sT   
    32  2017-01-18 09:31:00  000001   9.17  1000.0  Order_Zjwk6oEQ   
    33  2017-01-18 09:31:00  000002  20.92 -1000.0  Order_BsdtqSRD   
    34  2017-01-18 09:31:00  000004  37.15 -1000.0  Order_L2tBAEDw   
    35  2017-01-19 09:31:00  000001   9.18 -1000.0  Order_jLKnzptg   
    36  2017-01-19 09:31:00  000002  20.60 -1000.0  Order_pboORh93   
    37  2017-01-19 09:31:00  000004  35.69 -1000.0  Order_uYnJAc9x   
    38  2017-01-20 09:31:00  000001   9.22  1000.0  Order_jT1mtsLc   
    39  2017-01-20 09:31:00  000002  20.68 -1000.0  Order_DdlSYfz9   
    40  2017-01-20 09:31:00  000004  36.48  1000.0  Order_kT3C91Js   
    41  2017-01-23 09:31:00  000001   9.22 -1000.0  Order_BWQzvSZV   
    42  2017-01-23 09:31:00  000002  20.74  1000.0  Order_Ns1I8zyi   
    43  2017-01-23 09:31:00  000004  37.56  1000.0  Order_sW5NpLrZ   
    44  2017-01-24 09:31:00  000001   9.27  1000.0  Order_Ed5pn8hW   
    45  2017-01-24 09:31:00  000002  20.69  1000.0  Order_IBodSh0G   
    46  2017-01-24 09:31:00  000004  38.63 -1000.0  Order_E6Nfvkp1   
    47  2017-01-25 09:31:00  000002  20.61  1000.0  Order_gBxjODyY   
    48  2017-01-25 09:31:00  000004  38.25 -1000.0  Order_AdWkxYQr   
    49  2017-01-26 09:31:00  000001   9.33 -1000.0  Order_AEdwvGom   
    50  2017-01-26 09:31:00  000004  38.29  1000.0  Order_9eiqlU7n   
    
              trade_id  commission_fee  
    0   Trade_jvVQfoGn          31.095  
    1   Trade_RNmWeFZn          66.675  
    2   Trade_8NPLDMXV          39.150  
    3   Trade_3vNUoPfb          13.740  
    4   Trade_VgazesrI          67.050  
    5   Trade_n6FmXLCE          39.705  
    6   Trade_8mHaBhfn          31.395  
    7   Trade_s1ykwzmd          30.960  
    8   Trade_ECcve0xs          38.175  
    9   Trade_JWhDNaKZ          30.990  
    10  Trade_xbia8Z40          64.515  
    11  Trade_PdlqSB6y          37.635  
    12  Trade_Qm16wOg5          13.725  
    13  Trade_gyKlO4Ni          30.870  
    14  Trade_adfjV8ZA          64.875  
    15  Trade_YiK9qIE2          37.185  
    16  Trade_BZLgsvct          13.710  
    17  Trade_jyS4ULQ9          30.600  
    18  Trade_7QHRwdOW          63.675  
    19  Trade_5yBD2rml          37.275  
    20  Trade_q80zHrE7          13.725  
    21  Trade_dfM1gYA5          63.075  
    22  Trade_Xz2aBb4f          36.915  
    23  Trade_Ix7B34cT          13.740  
    24  Trade_MUdBTinP          32.715  
    25  Trade_4tAxRTdB          61.500  
    26  Trade_DFw14fYj          35.715  
    27  Trade_QDfBxAO6          31.500  
    28  Trade_UaLQt10y          57.390  
    29  Trade_vHqF8hBr          13.725  
    30  Trade_U5EgWJQX          31.200  
    31  Trade_d3hwFqy9          56.055  
    32  Trade_MFzfnsZG          13.755  
    33  Trade_Xm2RcPEu          31.380  
    34  Trade_0jvMGLDs          55.725  
    35  Trade_mz0U7a6p          13.770  
    36  Trade_cqnR4Y0s          30.900  
    37  Trade_w5cuNIea          53.535  
    38  Trade_qQFhkBrV          13.830  
    39  Trade_vnemBp8r          31.020  
    40  Trade_1ul5aIWf          54.720  
    41  Trade_Z5iLcCFP          13.830  
    42  Trade_kbl7xa4O          31.110  
    43  Trade_ri0QXxYP          56.340  
    44  Trade_x60OmP5z          13.905  
    45  Trade_tBw2JocE          31.035  
    46  Trade_uGN5jM4a          57.945  
    47  Trade_v2brxVKi          30.915  
    48  Trade_qOLzc8UC          57.375  
    49  Trade_SlaG5L1W          13.995  
    50  Trade_A36OPsc1          57.435  
    code
    000001       0.0
    000002   -1000.0
    000004    2000.0
    000007    2000.0
    Name: amount, dtype: float64
    


```python
user.get_account(a_1).history_table
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>datetime</th>
      <th>code</th>
      <th>price</th>
      <th>amount</th>
      <th>order_id</th>
      <th>trade_id</th>
      <th>commission_fee</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2017-01-03 09:31:00</td>
      <td>000002</td>
      <td>20.73</td>
      <td>1000.0</td>
      <td>Order_qD7NezRt</td>
      <td>Trade_jvVQfoGn</td>
      <td>31.095</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017-01-03 09:31:00</td>
      <td>000004</td>
      <td>44.45</td>
      <td>1000.0</td>
      <td>Order_wCmTcb96</td>
      <td>Trade_RNmWeFZn</td>
      <td>66.675</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-01-03 09:31:00</td>
      <td>000007</td>
      <td>26.10</td>
      <td>1000.0</td>
      <td>Order_u8stOwGg</td>
      <td>Trade_8NPLDMXV</td>
      <td>39.150</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017-01-04 09:31:00</td>
      <td>000001</td>
      <td>9.16</td>
      <td>1000.0</td>
      <td>Order_7IXP5NFn</td>
      <td>Trade_3vNUoPfb</td>
      <td>13.740</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017-01-04 09:31:00</td>
      <td>000004</td>
      <td>44.70</td>
      <td>1000.0</td>
      <td>Order_MShxXan2</td>
      <td>Trade_VgazesrI</td>
      <td>67.050</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2017-01-04 09:31:00</td>
      <td>000007</td>
      <td>26.47</td>
      <td>1000.0</td>
      <td>Order_rKC2vRnq</td>
      <td>Trade_n6FmXLCE</td>
      <td>39.705</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2017-01-05 09:31:00</td>
      <td>000002</td>
      <td>20.93</td>
      <td>1000.0</td>
      <td>Order_jkxOGbhE</td>
      <td>Trade_8mHaBhfn</td>
      <td>31.395</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2017-01-06 09:31:00</td>
      <td>000002</td>
      <td>20.64</td>
      <td>1000.0</td>
      <td>Order_Q0oPdXkZ</td>
      <td>Trade_s1ykwzmd</td>
      <td>30.960</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2017-01-06 09:31:00</td>
      <td>000007</td>
      <td>25.45</td>
      <td>1000.0</td>
      <td>Order_sF7J31mO</td>
      <td>Trade_ECcve0xs</td>
      <td>38.175</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2017-01-09 09:31:00</td>
      <td>000002</td>
      <td>20.66</td>
      <td>1000.0</td>
      <td>Order_tqROyjWx</td>
      <td>Trade_JWhDNaKZ</td>
      <td>30.990</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2017-01-09 09:31:00</td>
      <td>000004</td>
      <td>43.01</td>
      <td>1000.0</td>
      <td>Order_qWytne8G</td>
      <td>Trade_xbia8Z40</td>
      <td>64.515</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2017-01-09 09:31:00</td>
      <td>000007</td>
      <td>25.09</td>
      <td>1000.0</td>
      <td>Order_ziThVZ79</td>
      <td>Trade_PdlqSB6y</td>
      <td>37.635</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2017-01-10 09:31:00</td>
      <td>000001</td>
      <td>9.15</td>
      <td>1000.0</td>
      <td>Order_KdHhs9fz</td>
      <td>Trade_Qm16wOg5</td>
      <td>13.725</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2017-01-10 09:31:00</td>
      <td>000002</td>
      <td>20.58</td>
      <td>-1000.0</td>
      <td>Order_svGIw9g8</td>
      <td>Trade_gyKlO4Ni</td>
      <td>30.870</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2017-01-10 09:31:00</td>
      <td>000004</td>
      <td>43.25</td>
      <td>-1000.0</td>
      <td>Order_zst497J2</td>
      <td>Trade_adfjV8ZA</td>
      <td>64.875</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2017-01-10 09:31:00</td>
      <td>000007</td>
      <td>24.79</td>
      <td>-1000.0</td>
      <td>Order_fPorXvb5</td>
      <td>Trade_YiK9qIE2</td>
      <td>37.185</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2017-01-11 09:31:00</td>
      <td>000001</td>
      <td>9.14</td>
      <td>1000.0</td>
      <td>Order_Hy4EuL5s</td>
      <td>Trade_BZLgsvct</td>
      <td>13.710</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2017-01-11 09:31:00</td>
      <td>000002</td>
      <td>20.40</td>
      <td>-1000.0</td>
      <td>Order_ft0UpN6C</td>
      <td>Trade_jyS4ULQ9</td>
      <td>30.600</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2017-01-11 09:31:00</td>
      <td>000004</td>
      <td>42.45</td>
      <td>1000.0</td>
      <td>Order_Pg5eGyI2</td>
      <td>Trade_7QHRwdOW</td>
      <td>63.675</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2017-01-11 09:31:00</td>
      <td>000007</td>
      <td>24.85</td>
      <td>1000.0</td>
      <td>Order_cvMGAFy8</td>
      <td>Trade_5yBD2rml</td>
      <td>37.275</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2017-01-12 09:31:00</td>
      <td>000001</td>
      <td>9.15</td>
      <td>-1000.0</td>
      <td>Order_RtlPAFei</td>
      <td>Trade_q80zHrE7</td>
      <td>13.725</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2017-01-12 09:31:00</td>
      <td>000004</td>
      <td>42.05</td>
      <td>-1000.0</td>
      <td>Order_0Dn6tYr7</td>
      <td>Trade_dfM1gYA5</td>
      <td>63.075</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2017-01-12 09:31:00</td>
      <td>000007</td>
      <td>24.61</td>
      <td>-1000.0</td>
      <td>Order_72ayebkG</td>
      <td>Trade_Xz2aBb4f</td>
      <td>36.915</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2017-01-13 09:31:00</td>
      <td>000001</td>
      <td>9.16</td>
      <td>-1000.0</td>
      <td>Order_iy43nmaH</td>
      <td>Trade_Ix7B34cT</td>
      <td>13.740</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2017-01-13 09:31:00</td>
      <td>000002</td>
      <td>21.81</td>
      <td>-1000.0</td>
      <td>Order_GePWHtca</td>
      <td>Trade_MUdBTinP</td>
      <td>32.715</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2017-01-13 09:31:00</td>
      <td>000004</td>
      <td>41.00</td>
      <td>1000.0</td>
      <td>Order_hCmPEodp</td>
      <td>Trade_4tAxRTdB</td>
      <td>61.500</td>
    </tr>
    <tr>
      <th>26</th>
      <td>2017-01-13 09:31:00</td>
      <td>000007</td>
      <td>23.81</td>
      <td>-1000.0</td>
      <td>Order_bjLSasGl</td>
      <td>Trade_DFw14fYj</td>
      <td>35.715</td>
    </tr>
    <tr>
      <th>27</th>
      <td>2017-01-16 09:31:00</td>
      <td>000002</td>
      <td>21.00</td>
      <td>-1000.0</td>
      <td>Order_NifFeo6d</td>
      <td>Trade_QDfBxAO6</td>
      <td>31.500</td>
    </tr>
    <tr>
      <th>28</th>
      <td>2017-01-16 09:31:00</td>
      <td>000004</td>
      <td>38.26</td>
      <td>-1000.0</td>
      <td>Order_TLWHRXh8</td>
      <td>Trade_UaLQt10y</td>
      <td>57.390</td>
    </tr>
    <tr>
      <th>29</th>
      <td>2017-01-17 09:31:00</td>
      <td>000001</td>
      <td>9.15</td>
      <td>-1000.0</td>
      <td>Order_GfYcXjlW</td>
      <td>Trade_vHqF8hBr</td>
      <td>13.725</td>
    </tr>
    <tr>
      <th>30</th>
      <td>2017-01-17 09:31:00</td>
      <td>000002</td>
      <td>20.80</td>
      <td>-1000.0</td>
      <td>Order_lxnGy6kO</td>
      <td>Trade_U5EgWJQX</td>
      <td>31.200</td>
    </tr>
    <tr>
      <th>31</th>
      <td>2017-01-17 09:31:00</td>
      <td>000004</td>
      <td>37.37</td>
      <td>1000.0</td>
      <td>Order_wLXiE3sT</td>
      <td>Trade_d3hwFqy9</td>
      <td>56.055</td>
    </tr>
    <tr>
      <th>32</th>
      <td>2017-01-18 09:31:00</td>
      <td>000001</td>
      <td>9.17</td>
      <td>1000.0</td>
      <td>Order_Zjwk6oEQ</td>
      <td>Trade_MFzfnsZG</td>
      <td>13.755</td>
    </tr>
    <tr>
      <th>33</th>
      <td>2017-01-18 09:31:00</td>
      <td>000002</td>
      <td>20.92</td>
      <td>-1000.0</td>
      <td>Order_BsdtqSRD</td>
      <td>Trade_Xm2RcPEu</td>
      <td>31.380</td>
    </tr>
    <tr>
      <th>34</th>
      <td>2017-01-18 09:31:00</td>
      <td>000004</td>
      <td>37.15</td>
      <td>-1000.0</td>
      <td>Order_L2tBAEDw</td>
      <td>Trade_0jvMGLDs</td>
      <td>55.725</td>
    </tr>
    <tr>
      <th>35</th>
      <td>2017-01-19 09:31:00</td>
      <td>000001</td>
      <td>9.18</td>
      <td>-1000.0</td>
      <td>Order_jLKnzptg</td>
      <td>Trade_mz0U7a6p</td>
      <td>13.770</td>
    </tr>
    <tr>
      <th>36</th>
      <td>2017-01-19 09:31:00</td>
      <td>000002</td>
      <td>20.60</td>
      <td>-1000.0</td>
      <td>Order_pboORh93</td>
      <td>Trade_cqnR4Y0s</td>
      <td>30.900</td>
    </tr>
    <tr>
      <th>37</th>
      <td>2017-01-19 09:31:00</td>
      <td>000004</td>
      <td>35.69</td>
      <td>-1000.0</td>
      <td>Order_uYnJAc9x</td>
      <td>Trade_w5cuNIea</td>
      <td>53.535</td>
    </tr>
    <tr>
      <th>38</th>
      <td>2017-01-20 09:31:00</td>
      <td>000001</td>
      <td>9.22</td>
      <td>1000.0</td>
      <td>Order_jT1mtsLc</td>
      <td>Trade_qQFhkBrV</td>
      <td>13.830</td>
    </tr>
    <tr>
      <th>39</th>
      <td>2017-01-20 09:31:00</td>
      <td>000002</td>
      <td>20.68</td>
      <td>-1000.0</td>
      <td>Order_DdlSYfz9</td>
      <td>Trade_vnemBp8r</td>
      <td>31.020</td>
    </tr>
    <tr>
      <th>40</th>
      <td>2017-01-20 09:31:00</td>
      <td>000004</td>
      <td>36.48</td>
      <td>1000.0</td>
      <td>Order_kT3C91Js</td>
      <td>Trade_1ul5aIWf</td>
      <td>54.720</td>
    </tr>
    <tr>
      <th>41</th>
      <td>2017-01-23 09:31:00</td>
      <td>000001</td>
      <td>9.22</td>
      <td>-1000.0</td>
      <td>Order_BWQzvSZV</td>
      <td>Trade_Z5iLcCFP</td>
      <td>13.830</td>
    </tr>
    <tr>
      <th>42</th>
      <td>2017-01-23 09:31:00</td>
      <td>000002</td>
      <td>20.74</td>
      <td>1000.0</td>
      <td>Order_Ns1I8zyi</td>
      <td>Trade_kbl7xa4O</td>
      <td>31.110</td>
    </tr>
    <tr>
      <th>43</th>
      <td>2017-01-23 09:31:00</td>
      <td>000004</td>
      <td>37.56</td>
      <td>1000.0</td>
      <td>Order_sW5NpLrZ</td>
      <td>Trade_ri0QXxYP</td>
      <td>56.340</td>
    </tr>
    <tr>
      <th>44</th>
      <td>2017-01-24 09:31:00</td>
      <td>000001</td>
      <td>9.27</td>
      <td>1000.0</td>
      <td>Order_Ed5pn8hW</td>
      <td>Trade_x60OmP5z</td>
      <td>13.905</td>
    </tr>
    <tr>
      <th>45</th>
      <td>2017-01-24 09:31:00</td>
      <td>000002</td>
      <td>20.69</td>
      <td>1000.0</td>
      <td>Order_IBodSh0G</td>
      <td>Trade_tBw2JocE</td>
      <td>31.035</td>
    </tr>
    <tr>
      <th>46</th>
      <td>2017-01-24 09:31:00</td>
      <td>000004</td>
      <td>38.63</td>
      <td>-1000.0</td>
      <td>Order_E6Nfvkp1</td>
      <td>Trade_uGN5jM4a</td>
      <td>57.945</td>
    </tr>
    <tr>
      <th>47</th>
      <td>2017-01-25 09:31:00</td>
      <td>000002</td>
      <td>20.61</td>
      <td>1000.0</td>
      <td>Order_gBxjODyY</td>
      <td>Trade_v2brxVKi</td>
      <td>30.915</td>
    </tr>
    <tr>
      <th>48</th>
      <td>2017-01-25 09:31:00</td>
      <td>000004</td>
      <td>38.25</td>
      <td>-1000.0</td>
      <td>Order_AdWkxYQr</td>
      <td>Trade_qOLzc8UC</td>
      <td>57.375</td>
    </tr>
    <tr>
      <th>49</th>
      <td>2017-01-26 09:31:00</td>
      <td>000001</td>
      <td>9.33</td>
      <td>-1000.0</td>
      <td>Order_AEdwvGom</td>
      <td>Trade_SlaG5L1W</td>
      <td>13.995</td>
    </tr>
    <tr>
      <th>50</th>
      <td>2017-01-26 09:31:00</td>
      <td>000004</td>
      <td>38.29</td>
      <td>1000.0</td>
      <td>Order_9eiqlU7n</td>
      <td>Trade_A36OPsc1</td>
      <td>57.435</td>
    </tr>
  </tbody>
</table>
</div>




```python
r=QA.QA_Risk(user.get_account(a_1))
```


```python
user.get_account(a_1).hold
```




    code
    000001       0.0
    000002   -1000.0
    000004    2000.0
    000007    2000.0
    Name: amount, dtype: float64




```python
user.get_account(a_1).trade
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>code</th>
      <th>000001</th>
      <th>000002</th>
      <th>000004</th>
      <th>000007</th>
    </tr>
    <tr>
      <th>datetime</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-01-03 09:31:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-04 09:31:00</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-05 09:31:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-06 09:31:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-09 09:31:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-10 09:31:00</th>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>-1000.0</td>
    </tr>
    <tr>
      <th>2017-01-11 09:31:00</th>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-12 09:31:00</th>
      <td>-1000.0</td>
      <td>0.0</td>
      <td>-1000.0</td>
      <td>-1000.0</td>
    </tr>
    <tr>
      <th>2017-01-13 09:31:00</th>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>-1000.0</td>
    </tr>
    <tr>
      <th>2017-01-16 09:31:00</th>
      <td>0.0</td>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-17 09:31:00</th>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-18 09:31:00</th>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-19 09:31:00</th>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-20 09:31:00</th>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-23 09:31:00</th>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-24 09:31:00</th>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-25 09:31:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-26 09:31:00</th>
      <td>-1000.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
user.get_account(a_1).daily_balance
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>code</th>
      <th>000001</th>
      <th>000002</th>
      <th>000004</th>
      <th>000007</th>
    </tr>
    <tr>
      <th>datetime</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-01-03 09:31:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-04 09:31:00</th>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>2000.0</td>
      <td>2000.0</td>
    </tr>
    <tr>
      <th>2017-01-05 09:31:00</th>
      <td>1000.0</td>
      <td>2000.0</td>
      <td>2000.0</td>
      <td>2000.0</td>
    </tr>
    <tr>
      <th>2017-01-06 09:31:00</th>
      <td>1000.0</td>
      <td>3000.0</td>
      <td>2000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-09 09:31:00</th>
      <td>1000.0</td>
      <td>4000.0</td>
      <td>3000.0</td>
      <td>4000.0</td>
    </tr>
    <tr>
      <th>2017-01-10 09:31:00</th>
      <td>2000.0</td>
      <td>3000.0</td>
      <td>2000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-11 09:31:00</th>
      <td>3000.0</td>
      <td>2000.0</td>
      <td>3000.0</td>
      <td>4000.0</td>
    </tr>
    <tr>
      <th>2017-01-12 09:31:00</th>
      <td>2000.0</td>
      <td>2000.0</td>
      <td>2000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-13 09:31:00</th>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>3000.0</td>
      <td>2000.0</td>
    </tr>
    <tr>
      <th>2017-01-16 09:31:00</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>2000.0</td>
      <td>2000.0</td>
    </tr>
    <tr>
      <th>2017-01-17 09:31:00</th>
      <td>0.0</td>
      <td>-1000.0</td>
      <td>3000.0</td>
      <td>2000.0</td>
    </tr>
    <tr>
      <th>2017-01-18 09:31:00</th>
      <td>1000.0</td>
      <td>-2000.0</td>
      <td>2000.0</td>
      <td>2000.0</td>
    </tr>
    <tr>
      <th>2017-01-19 09:31:00</th>
      <td>0.0</td>
      <td>-3000.0</td>
      <td>1000.0</td>
      <td>2000.0</td>
    </tr>
    <tr>
      <th>2017-01-20 09:31:00</th>
      <td>1000.0</td>
      <td>-4000.0</td>
      <td>2000.0</td>
      <td>2000.0</td>
    </tr>
    <tr>
      <th>2017-01-23 09:31:00</th>
      <td>0.0</td>
      <td>-3000.0</td>
      <td>3000.0</td>
      <td>2000.0</td>
    </tr>
    <tr>
      <th>2017-01-24 09:31:00</th>
      <td>1000.0</td>
      <td>-2000.0</td>
      <td>2000.0</td>
      <td>2000.0</td>
    </tr>
    <tr>
      <th>2017-01-25 09:31:00</th>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>2000.0</td>
    </tr>
    <tr>
      <th>2017-01-26 09:31:00</th>
      <td>0.0</td>
      <td>-1000.0</td>
      <td>2000.0</td>
      <td>2000.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
l=user.get_account(a_1).trade
```


```python
l.index
```




    Index(['2017-01-03 09:31:00', '2017-01-04 09:31:00', '2017-01-05 09:31:00',
           '2017-01-06 09:31:00', '2017-01-09 09:31:00', '2017-01-10 09:31:00',
           '2017-01-11 09:31:00', '2017-01-12 09:31:00', '2017-01-13 09:31:00',
           '2017-01-16 09:31:00', '2017-01-17 09:31:00', '2017-01-18 09:31:00',
           '2017-01-19 09:31:00', '2017-01-20 09:31:00', '2017-01-23 09:31:00',
           '2017-01-24 09:31:00', '2017-01-25 09:31:00', '2017-01-26 09:31:00'],
          dtype='object', name='datetime')


