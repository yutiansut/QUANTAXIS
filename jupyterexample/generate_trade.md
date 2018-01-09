

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
    < QA_Order datetime:2017-01-03 09:31:00 code:000001 price:9.16 towards:1 btype:0x01 order_id:Order_t3ynV6vB account:Acc_qodhKjYA status:300 >
    ===== SETTLED None =====
    < QA_Order datetime:2017-01-03 09:31:00 code:000002 price:20.73 towards:1 btype:0x01 order_id:Order_braSVeKA account:Acc_qodhKjYA status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-03 09:31:00 code:000004 price:44.45 towards:1 btype:0x01 order_id:Order_C124PhsZ account:Acc_qodhKjYA status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-04 09:31:00 code:000002 price:20.85 towards:1 btype:0x01 order_id:Order_8g0UGjDQ account:Acc_qodhKjYA status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-04 09:31:00 code:000004 price:44.7 towards:1 btype:0x01 order_id:Order_vYJLuCnQ account:Acc_qodhKjYA status:300 >
    ===== SETTLED None =====< QA_Order datetime:2017-01-05 09:31:00 code:000001 price:9.17 towards:1 btype:0x01 order_id:Order_8LQWCP2b account:Acc_qodhKjYA status:300 >
    
    ===== SETTLED None =====< QA_Order datetime:2017-01-06 09:31:00 code:000002 price:20.64 towards:1 btype:0x01 order_id:Order_dPyHiRTv account:Acc_qodhKjYA status:300 >
    
    < QA_Order datetime:2017-01-06 09:31:00 code:000004 price:43.96 towards:1 btype:0x01 order_id:Order_jeVmYhoQ account:Acc_qodhKjYA status:300 >
    ===== SETTLED None =====
    < QA_Order datetime:2017-01-09 09:31:00 code:000001 price:9.15 towards:-1 btype:0x01 order_id:Order_dHTN10cY account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    
    

    
    

    < QA_Order datetime:2017-01-09 09:31:00 code:000002 price:20.66 towards:-1 btype:0x01 order_id:Order_NZeJ68Hy account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> code 000002 date 2017-01-12 price None order_model close amount_model by_amount

    
    

    
    

    < QA_Order datetime:2017-01-09 09:31:00 code:000004 price:43.01 towards:-1 btype:0x01 order_id:Order_H1N2PX67 account:Acc_qodhKjYA status:300 >
    ===== SETTLED None =====
    < QA_Order datetime:2017-01-10 09:31:00 code:000001 price:9.15 towards:-1 btype:0x01 order_id:Order_V17SDEi5 account:Acc_qodhKjYA status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-10 09:31:00 code:000002 price:20.58 towards:1 btype:0x01 order_id:Order_x3ykpEwX account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    
    

    
    

    < QA_Order datetime:2017-01-10 09:31:00 code:000004 price:43.25 towards:1 btype:0x01 order_id:Order_zhDQw7d3 account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> code 000007 date 2017-01-16 price None order_model close amount_model by_amount

    
    

    
    

    < QA_Order datetime:2017-01-10 09:31:00 code:000007 price:24.79 towards:1 btype:0x01 order_id:Order_qFKbLnW0 account:Acc_qodhKjYA status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-11 09:31:00 code:000001 price:9.14 towards:1 btype:0x01 order_id:Order_12J38Vlw account:Acc_qodhKjYA status:300 >
    < QA_Order datetime:2017-01-11 09:31:00 code:000002 price:20.4 towards:1 btype:0x01 order_id:Order_kBd3e1iF account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    
    

    
    

    < QA_Order datetime:2017-01-11 09:31:00 code:000004 price:42.45 towards:1 btype:0x01 order_id:Order_6Imcwb23 account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> code 000007 date 2017-01-17 price None order_model close amount_model by_amount

    
    

    
    

    < QA_Order datetime:2017-01-11 09:31:00 code:000007 price:24.85 towards:1 btype:0x01 order_id:Order_9kU6YWij account:Acc_qodhKjYA status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-12 09:31:00 code:000001 price:9.15 towards:1 btype:0x01 order_id:Order_d9je3k7i account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    
    

    
    

    < QA_Order datetime:2017-01-12 09:31:00 code:000004 price:42.05 towards:-1 btype:0x01 order_id:Order_HLFxkYcJ account:Acc_qodhKjYA status:300 >
    

    QUANTAXIS>> code 000007 date 2017-01-18 price None order_model close amount_model by_amount

    < QA_Order datetime:2017-01-12 09:31:00 code:000007 price:24.61 towards:1 btype:0x01 order_id:Order_q3OZN0jg account:Acc_qodhKjYA status:300 >

    
    

    
    < QA_Order datetime:2017-01-13 09:31:00 code:000001 price:9.16 towards:-1 btype:0x01 order_id:Order_KW40qstA account:Acc_qodhKjYA status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-13 09:31:00 code:000002 price:21.81 towards:-1 btype:0x01 order_id:Order_BngMZyx9 account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    
    

    
    

    < QA_Order datetime:2017-01-13 09:31:00 code:000004 price:41.0 towards:-1 btype:0x01 order_id:Order_EMCIJ0Np account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> code 000007 date 2017-01-19 price None order_model close amount_model by_amount

    
    

    
    

    < QA_Order datetime:2017-01-16 09:31:00 code:000002 price:21.0 towards:1 btype:0x01 order_id:Order_5TJwiYMQ account:Acc_qodhKjYA status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-16 09:31:00 code:000004 price:38.26 towards:1 btype:0x01 order_id:Order_cdLzWyT4 account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    
    

    
    

    < QA_Order datetime:2017-01-17 09:31:00 code:000001 price:9.15 towards:1 btype:0x01 order_id:Order_pR9gvJHx account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> code 000007 date 2017-01-20 price None order_model close amount_model by_amount

    
    

    
    

    < QA_Order datetime:2017-01-17 09:31:00 code:000002 price:20.8 towards:-1 btype:0x01 order_id:Order_Hb14fNMQ account:Acc_qodhKjYA status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-17 09:31:00 code:000004 price:37.37 towards:-1 btype:0x01 order_id:Order_eNVLOiUH account:Acc_qodhKjYA status:300 >
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    < QA_Order datetime:2017-01-18 09:31:00 code:000001 price:9.17 towards:1 btype:0x01 order_id:Order_dZc7DpmE account:Acc_qodhKjYA status:300 >

    
    

    
    

    QUANTAXIS>> code 000007 date 2017-01-23 price None order_model close amount_model by_amount

    < QA_Order datetime:2017-01-18 09:31:00 code:000002 price:20.92 towards:-1 btype:0x01 order_id:Order_mnFckbO5 account:Acc_qodhKjYA status:300 >

    
    

    
    ===== SETTLED None =====< QA_Order datetime:2017-01-18 09:31:00 code:000004 price:37.15 towards:1 btype:0x01 order_id:Order_ACNrVR7o account:Acc_qodhKjYA status:300 >
    
    < QA_Order datetime:2017-01-19 09:31:00 code:000001 price:9.18 towards:-1 btype:0x01 order_id:Order_ARKqokz0 account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    

    
    

    QUANTAXIS>> code 000007 date 2017-01-24 price None order_model close amount_model by_amount

    < QA_Order datetime:2017-01-19 09:31:00 code:000002 price:20.6 towards:1 btype:0x01 order_id:Order_KoN0Xi5h account:Acc_qodhKjYA status:300 >

    
    

    
    ===== SETTLED None =====
    < QA_Order datetime:2017-01-19 09:31:00 code:000004 price:35.69 towards:-1 btype:0x01 order_id:Order_6M4VSkD7 account:Acc_qodhKjYA status:300 >
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     

    < QA_Order datetime:2017-01-20 09:31:00 code:000001 price:9.22 towards:-1 btype:0x01 order_id:Order_KPp9BCE0 account:Acc_qodhKjYA status:300 >

    
    

    
    

    QUANTAXIS>> code 000007 date 2017-01-25 price None order_model close amount_model by_amount

    < QA_Order datetime:2017-01-20 09:31:00 code:000002 price:20.68 towards:-1 btype:0x01 order_id:Order_57go34Ez account:Acc_qodhKjYA status:300 >

    
    

    
    < QA_Order datetime:2017-01-20 09:31:00 code:000004 price:36.48 towards:1 btype:0x01 order_id:Order_Cnr7ZX92 account:Acc_qodhKjYA status:300 >===== SETTLED None =====
    
    < QA_Order datetime:2017-01-23 09:31:00 code:000001 price:9.22 towards:1 btype:0x01 order_id:Order_d7zOPegF account:Acc_qodhKjYA status:300 >
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    

    < QA_Order datetime:2017-01-23 09:31:00 code:000002 price:20.74 towards:-1 btype:0x01 order_id:Order_FBhUSY1R account:Acc_qodhKjYA status:300 >

    QUANTAXIS>> code 000007 date 2017-01-26 price None order_model close amount_model by_amount

    
    

    
    

    < QA_Order datetime:2017-01-23 09:31:00 code:000004 price:37.56 towards:-1 btype:0x01 order_id:Order_l1aOzjgy account:Acc_qodhKjYA status:300 >
    ===== SETTLED None =====< QA_Order datetime:2017-01-24 09:31:00 code:000001 price:9.27 towards:1 btype:0x01 order_id:Order_knrICGO0 account:Acc_qodhKjYA status:300 >
    
    < QA_Order datetime:2017-01-24 09:31:00 code:000002 price:20.69 towards:-1 btype:0x01 order_id:Order_vZSU16CH account:Acc_qodhKjYA status:300 >
    < QA_Order datetime:2017-01-24 09:31:00 code:000004 price:38.63 towards:1 btype:0x01 order_id:Order_m0vaxgJ9 account:Acc_qodhKjYA status:300 >
    < QA_Order datetime:2017-01-25 09:31:00 code:000001 price:9.26 towards:-1 btype:0x01 order_id:Order_BCuRf0wg account:Acc_qodhKjYA status:300 >
    < QA_Order datetime:2017-01-25 09:31:00 code:000002 price:20.61 towards:1 btype:0x01 order_id:Order_JFP0rwkj account:Acc_qodhKjYA status:300 >
    < QA_Order datetime:2017-01-25 09:31:00 code:000004 price:38.25 towards:1 btype:0x01 order_id:Order_rDNI4cFT account:Acc_qodhKjYA status:300 >
    < QA_Order datetime:2017-01-26 09:31:00 code:000001 price:9.33 towards:1 btype:0x01 order_id:Order_C6INtGAy account:Acc_qodhKjYA status:300 >
    < QA_Order datetime:2017-01-26 09:31:00 code:000002 price:20.68 towards:-1 btype:0x01 order_id:Order_T7IZhBbW account:Acc_qodhKjYA status:300 >
    < QA_Order datetime:2017-01-26 09:31:00 code:000004 price:38.29 towards:-1 btype:0x01 order_id:Order_WKrcN0QE account:Acc_qodhKjYA status:300 >
    [['2017-01-03 09:31:00', '000001', 9.16, 1000.0, 'Order_t3ynV6vB', 'Trade_yWxiImZJ', 13.74], ['2017-01-03 09:31:00', '000002', 20.73, 1000.0, 'Order_braSVeKA', 'Trade_ZG8EnP4b', 31.095000000000002], ['2017-01-03 09:31:00', '000004', 44.45, 1000.0, 'Order_C124PhsZ', 'Trade_qDPVeGvX', 66.67500000000001], ['2017-01-04 09:31:00', '000002', 20.85, 1000.0, 'Order_8g0UGjDQ', 'Trade_QEeS78mr', 31.275000000000006], ['2017-01-04 09:31:00', '000004', 44.7, 1000.0, 'Order_vYJLuCnQ', 'Trade_u0ratNUF', 67.05000000000001], ['2017-01-05 09:31:00', '000001', 9.17, 1000.0, 'Order_8LQWCP2b', 'Trade_t8RPsJFv', 13.754999999999999], ['2017-01-06 09:31:00', '000002', 20.64, 1000.0, 'Order_dPyHiRTv', 'Trade_5mDyjKP7', 30.96], ['2017-01-06 09:31:00', '000004', 43.96, 1000.0, 'Order_jeVmYhoQ', 'Trade_Ud9WTr2V', 65.94], ['2017-01-09 09:31:00', '000001', 9.15, -1000.0, 'Order_dHTN10cY', 'Trade_zt4wOBm0', 13.725000000000001], ['2017-01-09 09:31:00', '000002', 20.66, -1000.0, 'Order_NZeJ68Hy', 'Trade_sYAHd75i', 30.99], ['2017-01-09 09:31:00', '000004', 43.01, -1000.0, 'Order_H1N2PX67', 'Trade_hslCMG6f', 64.515], ['2017-01-10 09:31:00', '000001', 9.15, -1000.0, 'Order_V17SDEi5', 'Trade_daICNsYg', 13.725000000000001], ['2017-01-10 09:31:00', '000002', 20.58, 1000.0, 'Order_x3ykpEwX', 'Trade_a7U2G36s', 30.869999999999997], ['2017-01-10 09:31:00', '000004', 43.25, 1000.0, 'Order_zhDQw7d3', 'Trade_94hXcG1A', 64.875], ['2017-01-10 09:31:00', '000007', 24.79, 1000.0, 'Order_qFKbLnW0', 'Trade_BFHtabe9', 37.185], ['2017-01-11 09:31:00', '000001', 9.14, 1000.0, 'Order_12J38Vlw', 'Trade_RdSlHFxC', 13.71], ['2017-01-11 09:31:00', '000002', 20.4, 1000.0, 'Order_kBd3e1iF', 'Trade_VOMqf1a4', 30.599999999999998], ['2017-01-11 09:31:00', '000004', 42.45, 1000.0, 'Order_6Imcwb23', 'Trade_gKujeCc0', 63.67500000000001], ['2017-01-11 09:31:00', '000007', 24.85, 1000.0, 'Order_9kU6YWij', 'Trade_4qJFUA6y', 37.275000000000006], ['2017-01-12 09:31:00', '000001', 9.15, 1000.0, 'Order_d9je3k7i', 'Trade_dXN9ZFmt', 13.725000000000001], ['2017-01-12 09:31:00', '000004', 42.05, -1000.0, 'Order_HLFxkYcJ', 'Trade_cepozdbr', 63.07499999999999], ['2017-01-12 09:31:00', '000007', 24.61, 1000.0, 'Order_q3OZN0jg', 'Trade_D8ThHx5B', 36.915000000000006], ['2017-01-13 09:31:00', '000001', 9.16, -1000.0, 'Order_KW40qstA', 'Trade_RtoO8Das', 13.74], ['2017-01-13 09:31:00', '000002', 21.81, -1000.0, 'Order_BngMZyx9', 'Trade_OhAkzb0P', 32.715], ['2017-01-13 09:31:00', '000004', 41.0, -1000.0, 'Order_EMCIJ0Np', 'Trade_wT6amIdf', 61.5], ['2017-01-16 09:31:00', '000002', 21.0, 1000.0, 'Order_5TJwiYMQ', 'Trade_NYHSXGIf', 31.5], ['2017-01-16 09:31:00', '000004', 38.26, 1000.0, 'Order_cdLzWyT4', 'Trade_Jc9W8lZ6', 57.38999999999999], ['2017-01-17 09:31:00', '000001', 9.15, 1000.0, 'Order_pR9gvJHx', 'Trade_fk15SGjy', 13.725000000000001], ['2017-01-17 09:31:00', '000002', 20.8, -1000.0, 'Order_Hb14fNMQ', 'Trade_BvTZ1Mqf', 31.200000000000003], ['2017-01-17 09:31:00', '000004', 37.37, -1000.0, 'Order_eNVLOiUH', 'Trade_k7ZHisNI', 56.055], ['2017-01-18 09:31:00', '000001', 9.17, 1000.0, 'Order_dZc7DpmE', 'Trade_jGrs1IxQ', 13.754999999999999], ['2017-01-18 09:31:00', '000002', 20.92, -1000.0, 'Order_mnFckbO5', 'Trade_EW0qKtiy', 31.380000000000006], ['2017-01-18 09:31:00', '000004', 37.15, 1000.0, 'Order_ACNrVR7o', 'Trade_dlD8hvcB', 55.724999999999994], ['2017-01-19 09:31:00', '000001', 9.18, -1000.0, 'Order_ARKqokz0', 'Trade_YoZ3xFnE', 13.77], ['2017-01-19 09:31:00', '000002', 20.6, 1000.0, 'Order_KoN0Xi5h', 'Trade_ZOwTWLsP', 30.900000000000002], ['2017-01-19 09:31:00', '000004', 35.69, -1000.0, 'Order_6M4VSkD7', 'Trade_9JXeMYp8', 53.535], ['2017-01-20 09:31:00', '000001', 9.22, -1000.0, 'Order_KPp9BCE0', 'Trade_Vq5ODe0I', 13.830000000000002], ['2017-01-20 09:31:00', '000002', 20.68, -1000.0, 'Order_57go34Ez', 'Trade_mux4vfe2', 31.02], ['2017-01-20 09:31:00', '000004', 36.48, 1000.0, 'Order_Cnr7ZX92', 'Trade_PNBW7y45', 54.72], ['2017-01-23 09:31:00', '000001', 9.22, 1000.0, 'Order_d7zOPegF', 'Trade_y8hAqPfE', 13.830000000000002], ['2017-01-23 09:31:00', '000002', 20.74, -1000.0, 'Order_FBhUSY1R', 'Trade_6dhFT1ib', 31.11], ['2017-01-23 09:31:00', '000004', 37.56, -1000.0, 'Order_l1aOzjgy', 'Trade_o3xjFlPW', 56.34], ['2017-01-24 09:31:00', '000001', 9.27, 1000.0, 'Order_knrICGO0', 'Trade_c1IxZz4k', 13.905], ['2017-01-24 09:31:00', '000002', 20.69, -1000.0, 'Order_vZSU16CH', 'Trade_cvjTohVH', 31.035000000000004], ['2017-01-24 09:31:00', '000004', 38.63, 1000.0, 'Order_m0vaxgJ9', 'Trade_dhZ781qy', 57.945], ['2017-01-25 09:31:00', '000001', 9.26, -1000.0, 'Order_BCuRf0wg', 'Trade_0A7nU23T', 13.889999999999999], ['2017-01-25 09:31:00', '000002', 20.61, 1000.0, 'Order_JFP0rwkj', 'Trade_5R9jBgWx', 30.915000000000003], ['2017-01-25 09:31:00', '000004', 38.25, 1000.0, 'Order_rDNI4cFT', 'Trade_lXWg4wJj', 57.375], ['2017-01-26 09:31:00', '000001', 9.33, 1000.0, 'Order_C6INtGAy', 'Trade_fXzUwt8N', 13.995000000000001], ['2017-01-26 09:31:00', '000002', 20.68, -1000.0, 'Order_T7IZhBbW', 'Trade_6XYrvqxU', 31.02], ['2017-01-26 09:31:00', '000004', 38.29, -1000.0, 'Order_WKrcN0QE', 'Trade_NnkTfl12', 57.435]]
    [1000000, 990826.26, 970065.165, 925548.49, 904667.215, 859900.1649999999, 850716.4099999999, 830045.45, 786019.51, 795155.785, 815784.795, 858730.28, 867866.555, 847255.685, 803940.81, 779113.625, 769959.915, 749529.3150000001, 707015.64, 682128.365, 672964.64, 714951.5650000001, 690304.65, 699450.91, 721228.1950000001, 762166.6950000001, 741135.1950000001, 702817.805, 693654.0800000001, 714422.8800000001, 751736.8250000001, 742553.0700000001, 763441.6900000001, 726235.9650000001, 735402.1950000001, 714771.295, 750407.76, 759613.93, 780262.91, 743728.1900000001, 734494.3600000001, 755203.2500000001, 792706.9100000001, 783423.0050000001, 804081.9700000001, 765394.0250000001, 774640.1350000001, 753999.2200000001, 715691.8450000001, 706347.8500000001, 726996.8300000001, 765229.395]
    765229.395
                   datetime    code  price  amount        order_id  \
    0   2017-01-03 09:31:00  000001   9.16  1000.0  Order_t3ynV6vB   
    1   2017-01-03 09:31:00  000002  20.73  1000.0  Order_braSVeKA   
    2   2017-01-03 09:31:00  000004  44.45  1000.0  Order_C124PhsZ   
    3   2017-01-04 09:31:00  000002  20.85  1000.0  Order_8g0UGjDQ   
    4   2017-01-04 09:31:00  000004  44.70  1000.0  Order_vYJLuCnQ   
    5   2017-01-05 09:31:00  000001   9.17  1000.0  Order_8LQWCP2b   
    6   2017-01-06 09:31:00  000002  20.64  1000.0  Order_dPyHiRTv   
    7   2017-01-06 09:31:00  000004  43.96  1000.0  Order_jeVmYhoQ   
    8   2017-01-09 09:31:00  000001   9.15 -1000.0  Order_dHTN10cY   
    9   2017-01-09 09:31:00  000002  20.66 -1000.0  Order_NZeJ68Hy   
    10  2017-01-09 09:31:00  000004  43.01 -1000.0  Order_H1N2PX67   
    11  2017-01-10 09:31:00  000001   9.15 -1000.0  Order_V17SDEi5   
    12  2017-01-10 09:31:00  000002  20.58  1000.0  Order_x3ykpEwX   
    13  2017-01-10 09:31:00  000004  43.25  1000.0  Order_zhDQw7d3   
    14  2017-01-10 09:31:00  000007  24.79  1000.0  Order_qFKbLnW0   
    15  2017-01-11 09:31:00  000001   9.14  1000.0  Order_12J38Vlw   
    16  2017-01-11 09:31:00  000002  20.40  1000.0  Order_kBd3e1iF   
    17  2017-01-11 09:31:00  000004  42.45  1000.0  Order_6Imcwb23   
    18  2017-01-11 09:31:00  000007  24.85  1000.0  Order_9kU6YWij   
    19  2017-01-12 09:31:00  000001   9.15  1000.0  Order_d9je3k7i   
    20  2017-01-12 09:31:00  000004  42.05 -1000.0  Order_HLFxkYcJ   
    21  2017-01-12 09:31:00  000007  24.61  1000.0  Order_q3OZN0jg   
    22  2017-01-13 09:31:00  000001   9.16 -1000.0  Order_KW40qstA   
    23  2017-01-13 09:31:00  000002  21.81 -1000.0  Order_BngMZyx9   
    24  2017-01-13 09:31:00  000004  41.00 -1000.0  Order_EMCIJ0Np   
    25  2017-01-16 09:31:00  000002  21.00  1000.0  Order_5TJwiYMQ   
    26  2017-01-16 09:31:00  000004  38.26  1000.0  Order_cdLzWyT4   
    27  2017-01-17 09:31:00  000001   9.15  1000.0  Order_pR9gvJHx   
    28  2017-01-17 09:31:00  000002  20.80 -1000.0  Order_Hb14fNMQ   
    29  2017-01-17 09:31:00  000004  37.37 -1000.0  Order_eNVLOiUH   
    30  2017-01-18 09:31:00  000001   9.17  1000.0  Order_dZc7DpmE   
    31  2017-01-18 09:31:00  000002  20.92 -1000.0  Order_mnFckbO5   
    32  2017-01-18 09:31:00  000004  37.15  1000.0  Order_ACNrVR7o   
    33  2017-01-19 09:31:00  000001   9.18 -1000.0  Order_ARKqokz0   
    34  2017-01-19 09:31:00  000002  20.60  1000.0  Order_KoN0Xi5h   
    35  2017-01-19 09:31:00  000004  35.69 -1000.0  Order_6M4VSkD7   
    36  2017-01-20 09:31:00  000001   9.22 -1000.0  Order_KPp9BCE0   
    37  2017-01-20 09:31:00  000002  20.68 -1000.0  Order_57go34Ez   
    38  2017-01-20 09:31:00  000004  36.48  1000.0  Order_Cnr7ZX92   
    39  2017-01-23 09:31:00  000001   9.22  1000.0  Order_d7zOPegF   
    40  2017-01-23 09:31:00  000002  20.74 -1000.0  Order_FBhUSY1R   
    41  2017-01-23 09:31:00  000004  37.56 -1000.0  Order_l1aOzjgy   
    42  2017-01-24 09:31:00  000001   9.27  1000.0  Order_knrICGO0   
    43  2017-01-24 09:31:00  000002  20.69 -1000.0  Order_vZSU16CH   
    44  2017-01-24 09:31:00  000004  38.63  1000.0  Order_m0vaxgJ9   
    45  2017-01-25 09:31:00  000001   9.26 -1000.0  Order_BCuRf0wg   
    46  2017-01-25 09:31:00  000002  20.61  1000.0  Order_JFP0rwkj   
    47  2017-01-25 09:31:00  000004  38.25  1000.0  Order_rDNI4cFT   
    48  2017-01-26 09:31:00  000001   9.33  1000.0  Order_C6INtGAy   
    49  2017-01-26 09:31:00  000002  20.68 -1000.0  Order_T7IZhBbW   
    50  2017-01-26 09:31:00  000004  38.29 -1000.0  Order_WKrcN0QE   
    
              trade_id  commission_fee  
    0   Trade_yWxiImZJ          13.740  
    1   Trade_ZG8EnP4b          31.095  
    2   Trade_qDPVeGvX          66.675  
    3   Trade_QEeS78mr          31.275  
    4   Trade_u0ratNUF          67.050  
    5   Trade_t8RPsJFv          13.755  
    6   Trade_5mDyjKP7          30.960  
    7   Trade_Ud9WTr2V          65.940  
    8   Trade_zt4wOBm0          13.725  
    9   Trade_sYAHd75i          30.990  
    10  Trade_hslCMG6f          64.515  
    11  Trade_daICNsYg          13.725  
    12  Trade_a7U2G36s          30.870  
    13  Trade_94hXcG1A          64.875  
    14  Trade_BFHtabe9          37.185  
    15  Trade_RdSlHFxC          13.710  
    16  Trade_VOMqf1a4          30.600  
    17  Trade_gKujeCc0          63.675  
    18  Trade_4qJFUA6y          37.275  
    19  Trade_dXN9ZFmt          13.725  
    20  Trade_cepozdbr          63.075  
    21  Trade_D8ThHx5B          36.915  
    22  Trade_RtoO8Das          13.740  
    23  Trade_OhAkzb0P          32.715  
    24  Trade_wT6amIdf          61.500  
    25  Trade_NYHSXGIf          31.500  
    26  Trade_Jc9W8lZ6          57.390  
    27  Trade_fk15SGjy          13.725  
    28  Trade_BvTZ1Mqf          31.200  
    29  Trade_k7ZHisNI          56.055  
    30  Trade_jGrs1IxQ          13.755  
    31  Trade_EW0qKtiy          31.380  
    32  Trade_dlD8hvcB          55.725  
    33  Trade_YoZ3xFnE          13.770  
    34  Trade_ZOwTWLsP          30.900  
    35  Trade_9JXeMYp8          53.535  
    36  Trade_Vq5ODe0I          13.830  
    37  Trade_mux4vfe2          31.020  
    38  Trade_PNBW7y45          54.720  
    39  Trade_y8hAqPfE          13.830  
    40  Trade_6dhFT1ib          31.110  
    41  Trade_o3xjFlPW          56.340  
    42  Trade_c1IxZz4k          13.905  
    43  Trade_cvjTohVH          31.035  
    44  Trade_dhZ781qy          57.945  
    45  Trade_0A7nU23T          13.890  
    46  Trade_5R9jBgWx          30.915  
    47  Trade_lXWg4wJj          57.375  
    48  Trade_fXzUwt8N          13.995  
    49  Trade_6XYrvqxU          31.020  
    50  Trade_NnkTfl12          57.435  
    code
    000001    3000.0
    000002       0.0
    000004    3000.0
    000007    3000.0
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
      <td>000001</td>
      <td>9.16</td>
      <td>1000.0</td>
      <td>Order_t3ynV6vB</td>
      <td>Trade_yWxiImZJ</td>
      <td>13.740</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017-01-03 09:31:00</td>
      <td>000002</td>
      <td>20.73</td>
      <td>1000.0</td>
      <td>Order_braSVeKA</td>
      <td>Trade_ZG8EnP4b</td>
      <td>31.095</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-01-03 09:31:00</td>
      <td>000004</td>
      <td>44.45</td>
      <td>1000.0</td>
      <td>Order_C124PhsZ</td>
      <td>Trade_qDPVeGvX</td>
      <td>66.675</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017-01-04 09:31:00</td>
      <td>000002</td>
      <td>20.85</td>
      <td>1000.0</td>
      <td>Order_8g0UGjDQ</td>
      <td>Trade_QEeS78mr</td>
      <td>31.275</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017-01-04 09:31:00</td>
      <td>000004</td>
      <td>44.70</td>
      <td>1000.0</td>
      <td>Order_vYJLuCnQ</td>
      <td>Trade_u0ratNUF</td>
      <td>67.050</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2017-01-05 09:31:00</td>
      <td>000001</td>
      <td>9.17</td>
      <td>1000.0</td>
      <td>Order_8LQWCP2b</td>
      <td>Trade_t8RPsJFv</td>
      <td>13.755</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2017-01-06 09:31:00</td>
      <td>000002</td>
      <td>20.64</td>
      <td>1000.0</td>
      <td>Order_dPyHiRTv</td>
      <td>Trade_5mDyjKP7</td>
      <td>30.960</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2017-01-06 09:31:00</td>
      <td>000004</td>
      <td>43.96</td>
      <td>1000.0</td>
      <td>Order_jeVmYhoQ</td>
      <td>Trade_Ud9WTr2V</td>
      <td>65.940</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2017-01-09 09:31:00</td>
      <td>000001</td>
      <td>9.15</td>
      <td>-1000.0</td>
      <td>Order_dHTN10cY</td>
      <td>Trade_zt4wOBm0</td>
      <td>13.725</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2017-01-09 09:31:00</td>
      <td>000002</td>
      <td>20.66</td>
      <td>-1000.0</td>
      <td>Order_NZeJ68Hy</td>
      <td>Trade_sYAHd75i</td>
      <td>30.990</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2017-01-09 09:31:00</td>
      <td>000004</td>
      <td>43.01</td>
      <td>-1000.0</td>
      <td>Order_H1N2PX67</td>
      <td>Trade_hslCMG6f</td>
      <td>64.515</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2017-01-10 09:31:00</td>
      <td>000001</td>
      <td>9.15</td>
      <td>-1000.0</td>
      <td>Order_V17SDEi5</td>
      <td>Trade_daICNsYg</td>
      <td>13.725</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2017-01-10 09:31:00</td>
      <td>000002</td>
      <td>20.58</td>
      <td>1000.0</td>
      <td>Order_x3ykpEwX</td>
      <td>Trade_a7U2G36s</td>
      <td>30.870</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2017-01-10 09:31:00</td>
      <td>000004</td>
      <td>43.25</td>
      <td>1000.0</td>
      <td>Order_zhDQw7d3</td>
      <td>Trade_94hXcG1A</td>
      <td>64.875</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2017-01-10 09:31:00</td>
      <td>000007</td>
      <td>24.79</td>
      <td>1000.0</td>
      <td>Order_qFKbLnW0</td>
      <td>Trade_BFHtabe9</td>
      <td>37.185</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2017-01-11 09:31:00</td>
      <td>000001</td>
      <td>9.14</td>
      <td>1000.0</td>
      <td>Order_12J38Vlw</td>
      <td>Trade_RdSlHFxC</td>
      <td>13.710</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2017-01-11 09:31:00</td>
      <td>000002</td>
      <td>20.40</td>
      <td>1000.0</td>
      <td>Order_kBd3e1iF</td>
      <td>Trade_VOMqf1a4</td>
      <td>30.600</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2017-01-11 09:31:00</td>
      <td>000004</td>
      <td>42.45</td>
      <td>1000.0</td>
      <td>Order_6Imcwb23</td>
      <td>Trade_gKujeCc0</td>
      <td>63.675</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2017-01-11 09:31:00</td>
      <td>000007</td>
      <td>24.85</td>
      <td>1000.0</td>
      <td>Order_9kU6YWij</td>
      <td>Trade_4qJFUA6y</td>
      <td>37.275</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2017-01-12 09:31:00</td>
      <td>000001</td>
      <td>9.15</td>
      <td>1000.0</td>
      <td>Order_d9je3k7i</td>
      <td>Trade_dXN9ZFmt</td>
      <td>13.725</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2017-01-12 09:31:00</td>
      <td>000004</td>
      <td>42.05</td>
      <td>-1000.0</td>
      <td>Order_HLFxkYcJ</td>
      <td>Trade_cepozdbr</td>
      <td>63.075</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2017-01-12 09:31:00</td>
      <td>000007</td>
      <td>24.61</td>
      <td>1000.0</td>
      <td>Order_q3OZN0jg</td>
      <td>Trade_D8ThHx5B</td>
      <td>36.915</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2017-01-13 09:31:00</td>
      <td>000001</td>
      <td>9.16</td>
      <td>-1000.0</td>
      <td>Order_KW40qstA</td>
      <td>Trade_RtoO8Das</td>
      <td>13.740</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2017-01-13 09:31:00</td>
      <td>000002</td>
      <td>21.81</td>
      <td>-1000.0</td>
      <td>Order_BngMZyx9</td>
      <td>Trade_OhAkzb0P</td>
      <td>32.715</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2017-01-13 09:31:00</td>
      <td>000004</td>
      <td>41.00</td>
      <td>-1000.0</td>
      <td>Order_EMCIJ0Np</td>
      <td>Trade_wT6amIdf</td>
      <td>61.500</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2017-01-16 09:31:00</td>
      <td>000002</td>
      <td>21.00</td>
      <td>1000.0</td>
      <td>Order_5TJwiYMQ</td>
      <td>Trade_NYHSXGIf</td>
      <td>31.500</td>
    </tr>
    <tr>
      <th>26</th>
      <td>2017-01-16 09:31:00</td>
      <td>000004</td>
      <td>38.26</td>
      <td>1000.0</td>
      <td>Order_cdLzWyT4</td>
      <td>Trade_Jc9W8lZ6</td>
      <td>57.390</td>
    </tr>
    <tr>
      <th>27</th>
      <td>2017-01-17 09:31:00</td>
      <td>000001</td>
      <td>9.15</td>
      <td>1000.0</td>
      <td>Order_pR9gvJHx</td>
      <td>Trade_fk15SGjy</td>
      <td>13.725</td>
    </tr>
    <tr>
      <th>28</th>
      <td>2017-01-17 09:31:00</td>
      <td>000002</td>
      <td>20.80</td>
      <td>-1000.0</td>
      <td>Order_Hb14fNMQ</td>
      <td>Trade_BvTZ1Mqf</td>
      <td>31.200</td>
    </tr>
    <tr>
      <th>29</th>
      <td>2017-01-17 09:31:00</td>
      <td>000004</td>
      <td>37.37</td>
      <td>-1000.0</td>
      <td>Order_eNVLOiUH</td>
      <td>Trade_k7ZHisNI</td>
      <td>56.055</td>
    </tr>
    <tr>
      <th>30</th>
      <td>2017-01-18 09:31:00</td>
      <td>000001</td>
      <td>9.17</td>
      <td>1000.0</td>
      <td>Order_dZc7DpmE</td>
      <td>Trade_jGrs1IxQ</td>
      <td>13.755</td>
    </tr>
    <tr>
      <th>31</th>
      <td>2017-01-18 09:31:00</td>
      <td>000002</td>
      <td>20.92</td>
      <td>-1000.0</td>
      <td>Order_mnFckbO5</td>
      <td>Trade_EW0qKtiy</td>
      <td>31.380</td>
    </tr>
    <tr>
      <th>32</th>
      <td>2017-01-18 09:31:00</td>
      <td>000004</td>
      <td>37.15</td>
      <td>1000.0</td>
      <td>Order_ACNrVR7o</td>
      <td>Trade_dlD8hvcB</td>
      <td>55.725</td>
    </tr>
    <tr>
      <th>33</th>
      <td>2017-01-19 09:31:00</td>
      <td>000001</td>
      <td>9.18</td>
      <td>-1000.0</td>
      <td>Order_ARKqokz0</td>
      <td>Trade_YoZ3xFnE</td>
      <td>13.770</td>
    </tr>
    <tr>
      <th>34</th>
      <td>2017-01-19 09:31:00</td>
      <td>000002</td>
      <td>20.60</td>
      <td>1000.0</td>
      <td>Order_KoN0Xi5h</td>
      <td>Trade_ZOwTWLsP</td>
      <td>30.900</td>
    </tr>
    <tr>
      <th>35</th>
      <td>2017-01-19 09:31:00</td>
      <td>000004</td>
      <td>35.69</td>
      <td>-1000.0</td>
      <td>Order_6M4VSkD7</td>
      <td>Trade_9JXeMYp8</td>
      <td>53.535</td>
    </tr>
    <tr>
      <th>36</th>
      <td>2017-01-20 09:31:00</td>
      <td>000001</td>
      <td>9.22</td>
      <td>-1000.0</td>
      <td>Order_KPp9BCE0</td>
      <td>Trade_Vq5ODe0I</td>
      <td>13.830</td>
    </tr>
    <tr>
      <th>37</th>
      <td>2017-01-20 09:31:00</td>
      <td>000002</td>
      <td>20.68</td>
      <td>-1000.0</td>
      <td>Order_57go34Ez</td>
      <td>Trade_mux4vfe2</td>
      <td>31.020</td>
    </tr>
    <tr>
      <th>38</th>
      <td>2017-01-20 09:31:00</td>
      <td>000004</td>
      <td>36.48</td>
      <td>1000.0</td>
      <td>Order_Cnr7ZX92</td>
      <td>Trade_PNBW7y45</td>
      <td>54.720</td>
    </tr>
    <tr>
      <th>39</th>
      <td>2017-01-23 09:31:00</td>
      <td>000001</td>
      <td>9.22</td>
      <td>1000.0</td>
      <td>Order_d7zOPegF</td>
      <td>Trade_y8hAqPfE</td>
      <td>13.830</td>
    </tr>
    <tr>
      <th>40</th>
      <td>2017-01-23 09:31:00</td>
      <td>000002</td>
      <td>20.74</td>
      <td>-1000.0</td>
      <td>Order_FBhUSY1R</td>
      <td>Trade_6dhFT1ib</td>
      <td>31.110</td>
    </tr>
    <tr>
      <th>41</th>
      <td>2017-01-23 09:31:00</td>
      <td>000004</td>
      <td>37.56</td>
      <td>-1000.0</td>
      <td>Order_l1aOzjgy</td>
      <td>Trade_o3xjFlPW</td>
      <td>56.340</td>
    </tr>
    <tr>
      <th>42</th>
      <td>2017-01-24 09:31:00</td>
      <td>000001</td>
      <td>9.27</td>
      <td>1000.0</td>
      <td>Order_knrICGO0</td>
      <td>Trade_c1IxZz4k</td>
      <td>13.905</td>
    </tr>
    <tr>
      <th>43</th>
      <td>2017-01-24 09:31:00</td>
      <td>000002</td>
      <td>20.69</td>
      <td>-1000.0</td>
      <td>Order_vZSU16CH</td>
      <td>Trade_cvjTohVH</td>
      <td>31.035</td>
    </tr>
    <tr>
      <th>44</th>
      <td>2017-01-24 09:31:00</td>
      <td>000004</td>
      <td>38.63</td>
      <td>1000.0</td>
      <td>Order_m0vaxgJ9</td>
      <td>Trade_dhZ781qy</td>
      <td>57.945</td>
    </tr>
    <tr>
      <th>45</th>
      <td>2017-01-25 09:31:00</td>
      <td>000001</td>
      <td>9.26</td>
      <td>-1000.0</td>
      <td>Order_BCuRf0wg</td>
      <td>Trade_0A7nU23T</td>
      <td>13.890</td>
    </tr>
    <tr>
      <th>46</th>
      <td>2017-01-25 09:31:00</td>
      <td>000002</td>
      <td>20.61</td>
      <td>1000.0</td>
      <td>Order_JFP0rwkj</td>
      <td>Trade_5R9jBgWx</td>
      <td>30.915</td>
    </tr>
    <tr>
      <th>47</th>
      <td>2017-01-25 09:31:00</td>
      <td>000004</td>
      <td>38.25</td>
      <td>1000.0</td>
      <td>Order_rDNI4cFT</td>
      <td>Trade_lXWg4wJj</td>
      <td>57.375</td>
    </tr>
    <tr>
      <th>48</th>
      <td>2017-01-26 09:31:00</td>
      <td>000001</td>
      <td>9.33</td>
      <td>1000.0</td>
      <td>Order_C6INtGAy</td>
      <td>Trade_fXzUwt8N</td>
      <td>13.995</td>
    </tr>
    <tr>
      <th>49</th>
      <td>2017-01-26 09:31:00</td>
      <td>000002</td>
      <td>20.68</td>
      <td>-1000.0</td>
      <td>Order_T7IZhBbW</td>
      <td>Trade_6XYrvqxU</td>
      <td>31.020</td>
    </tr>
    <tr>
      <th>50</th>
      <td>2017-01-26 09:31:00</td>
      <td>000004</td>
      <td>38.29</td>
      <td>-1000.0</td>
      <td>Order_WKrcN0QE</td>
      <td>Trade_NnkTfl12</td>
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
    000001    3000.0
    000002       0.0
    000004    3000.0
    000007    3000.0
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
      <td>1000.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-04 09:31:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-05 09:31:00</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-06 09:31:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-09 09:31:00</th>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-10 09:31:00</th>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-11 09:31:00</th>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-12 09:31:00</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>-1000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-13 09:31:00</th>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-16 09:31:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-17 09:31:00</th>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-18 09:31:00</th>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-19 09:31:00</th>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-20 09:31:00</th>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-23 09:31:00</th>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-24 09:31:00</th>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-25 09:31:00</th>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-26 09:31:00</th>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>-1000.0</td>
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
      <td>1000.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-04 09:31:00</th>
      <td>1000.0</td>
      <td>2000.0</td>
      <td>2000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-05 09:31:00</th>
      <td>2000.0</td>
      <td>2000.0</td>
      <td>2000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-06 09:31:00</th>
      <td>2000.0</td>
      <td>3000.0</td>
      <td>3000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-09 09:31:00</th>
      <td>1000.0</td>
      <td>2000.0</td>
      <td>2000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-10 09:31:00</th>
      <td>0.0</td>
      <td>3000.0</td>
      <td>3000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-11 09:31:00</th>
      <td>1000.0</td>
      <td>4000.0</td>
      <td>4000.0</td>
      <td>2000.0</td>
    </tr>
    <tr>
      <th>2017-01-12 09:31:00</th>
      <td>2000.0</td>
      <td>4000.0</td>
      <td>3000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-13 09:31:00</th>
      <td>1000.0</td>
      <td>3000.0</td>
      <td>2000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-16 09:31:00</th>
      <td>1000.0</td>
      <td>4000.0</td>
      <td>3000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-17 09:31:00</th>
      <td>2000.0</td>
      <td>3000.0</td>
      <td>2000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-18 09:31:00</th>
      <td>3000.0</td>
      <td>2000.0</td>
      <td>3000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-19 09:31:00</th>
      <td>2000.0</td>
      <td>3000.0</td>
      <td>2000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-20 09:31:00</th>
      <td>1000.0</td>
      <td>2000.0</td>
      <td>3000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-23 09:31:00</th>
      <td>2000.0</td>
      <td>1000.0</td>
      <td>2000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-24 09:31:00</th>
      <td>3000.0</td>
      <td>0.0</td>
      <td>3000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-25 09:31:00</th>
      <td>2000.0</td>
      <td>1000.0</td>
      <td>4000.0</td>
      <td>3000.0</td>
    </tr>
    <tr>
      <th>2017-01-26 09:31:00</th>
      <td>3000.0</td>
      <td>0.0</td>
      <td>3000.0</td>
      <td>3000.0</td>
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


