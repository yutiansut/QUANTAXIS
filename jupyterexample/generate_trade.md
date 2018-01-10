

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
        if random.random()<0.3:
            market.insert_order(account_id=a_1, amount=1000, price=None, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT, time=date, code=code,
                                order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.BUY, market_type=QA.MARKET_TYPE.STOCK_DAY,
                                data_type=QA.MARKETDATA_TYPE.DAY, broker_name=QA.BROKER_TYPE.BACKETEST)
        else:
            try:
                print(user.get_account(a_1).sell_available.get(code,0))
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
    

    Bad REPSONSE 218.75.126.9
    

    QUANTAXIS>> === The BEST SERVER ===
     stock_ip 115.238.90.165 future_ip 61.152.107.141
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
    < QA_Order datetime:2017-01-03 09:31:00 code:000001 price:9.16 towards:1 btype:0x01 order_id:Order_jwd6abQM account:Acc_Q2nTwdDW status:300 >===== SETTLED None =====
    
    ===== SETTLED None =====
    1000.0
    0< QA_Order datetime:2017-01-05 09:31:00 code:000001 price:9.17 towards:-1 btype:0x01 order_id:Order_MEZmuAS6 account:Acc_Q2nTwdDW status:300 >
    
    0
    0
    ===== SETTLED None =====
    0.0
    0< QA_Order datetime:2017-01-06 09:31:00 code:000002 price:20.64 towards:1 btype:0x01 order_id:Order_QPNR2bhr account:Acc_Q2nTwdDW status:300 >
    
    ===== SETTLED None =====< QA_Order datetime:2017-01-06 09:31:00 code:000007 price:25.45 towards:1 btype:0x01 order_id:Order_6MLOD9sg account:Acc_Q2nTwdDW status:300 >
    
    0.0
    1000.0
    1000.0< QA_Order datetime:2017-01-09 09:31:00 code:000002 price:20.66 towards:-1 btype:0x01 order_id:Order_Bp2t8SfF account:Acc_Q2nTwdDW status:300 >
    
    ===== SETTLED None =====
    < QA_Order datetime:2017-01-09 09:31:00 code:000004 price:43.01 towards:1 btype:0x01 order_id:Order_tJfQDUKj account:Acc_Q2nTwdDW status:300 >0.0
    
    < QA_Order datetime:2017-01-09 09:31:00 code:000007 price:25.09 towards:-1 btype:0x01 order_id:Order_W6iIOYJo account:Acc_Q2nTwdDW status:300 >0.0
    
    ===== SETTLED None =====< QA_Order datetime:2017-01-10 09:31:00 code:000004 price:43.25 towards:1 btype:0x01 order_id:Order_0M7pY4RQ account:Acc_Q2nTwdDW status:300 >
    
    0.0
    < QA_Order datetime:2017-01-10 09:31:00 code:000007 price:24.79 towards:1 btype:0x01 order_id:Order_Zud0fmbn account:Acc_Q2nTwdDW status:300 >0.0
    
    1000.0
    1000.0< QA_Order datetime:2017-01-11 09:31:00 code:000004 price:42.45 towards:-1 btype:0x01 order_id:Order_rE5DgiGz account:Acc_Q2nTwdDW status:300 >
    
    ===== SETTLED None =====
    < QA_Order datetime:2017-01-11 09:31:00 code:000007 price:24.85 towards:-1 btype:0x01 order_id:Order_Eudq2tNY account:Acc_Q2nTwdDW status:300 >
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    

    < QA_Order datetime:2017-01-12 09:31:00 code:000001 price:9.15 towards:1 btype:0x01 order_id:Order_UuMhpE5B account:Acc_Q2nTwdDW status:300 >

    QUANTAXIS>> code 000002 date 2017-01-12 price None order_model close amount_model by_amount

    
    

    
    

    1000.0
    0.0< QA_Order datetime:2017-01-12 09:31:00 code:000004 price:42.05 towards:-1 btype:0x01 order_id:Order_rUENH54P account:Acc_Q2nTwdDW status:300 >
    
    ===== SETTLED None =====
    1000.0
    0.0< QA_Order datetime:2017-01-13 09:31:00 code:000001 price:9.16 towards:-1 btype:0x01 order_id:Order_Al9JbVa8 account:Acc_Q2nTwdDW status:300 >
    
    0.0
    < QA_Order datetime:2017-01-13 09:31:00 code:000004 price:41.0 towards:1 btype:0x01 order_id:Order_JQ14OW2N account:Acc_Q2nTwdDW status:300 >===== SETTLED None =====
    
    0.0
    0.0
    1000.0
    0.0< QA_Order datetime:2017-01-16 09:31:00 code:000004 price:38.26 towards:-1 btype:0x01 order_id:Order_I47Er3in account:Acc_Q2nTwdDW status:300 >
    
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    QUANTAXIS>> code 000007 date 2017-01-16 price None order_model close amount_model by_amount
    

    ===== SETTLED None =====
    0.0
    0.0
    0.0
    0.0
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    QUANTAXIS>> code 000007 date 2017-01-17 price None order_model close amount_model by_amount
    

    ===== SETTLED None =====
    0.0
    0.0
    0.0< QA_Order datetime:2017-01-18 09:31:00 code:000004 price:37.15 towards:1 btype:0x01 order_id:Order_vxPaKuZb account:Acc_Q2nTwdDW status:300 >
    
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    QUANTAXIS>> code 000007 date 2017-01-18 price None order_model close amount_model by_amount
    

    ===== SETTLED None =====
    0.0
    1000.0< QA_Order datetime:2017-01-19 09:31:00 code:000002 price:20.6 towards:1 btype:0x01 order_id:Order_YFTPt5jH account:Acc_Q2nTwdDW status:300 >
    
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    

    < QA_Order datetime:2017-01-19 09:31:00 code:000004 price:35.69 towards:-1 btype:0x01 order_id:Order_H21ocZ5q account:Acc_Q2nTwdDW status:300 >

    QUANTAXIS>> code 000007 date 2017-01-19 price None order_model close amount_model by_amount

    
    

    
    

    ===== SETTLED None =====
    0.0
    1000.0
    0.0< QA_Order datetime:2017-01-20 09:31:00 code:000002 price:20.68 towards:-1 btype:0x01 order_id:Order_FMDtsGn9 account:Acc_Q2nTwdDW status:300 >
    
    0.0
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    QUANTAXIS>> code 000007 date 2017-01-20 price None order_model close amount_model by_amount
    

    ===== SETTLED None =====
    0.0
    0.0
    < QA_Order datetime:2017-01-23 09:31:00 code:000002 price:20.74 towards:1 btype:0x01 order_id:Order_SxeuKmRh account:Acc_Q2nTwdDW status:300 >
    0.0
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    QUANTAXIS>> code 000007 date 2017-01-23 price None order_model close amount_model by_amount
    

    ===== SETTLED None =====
    1000.0< QA_Order datetime:2017-01-24 09:31:00 code:000001 price:9.27 towards:1 btype:0x01 order_id:Order_H79EP6Ld account:Acc_Q2nTwdDW status:300 >
    
    0.0
    < QA_Order datetime:2017-01-24 09:31:00 code:000002 price:20.69 towards:-1 btype:0x01 order_id:Order_w9WXpNQu account:Acc_Q2nTwdDW status:300 >0.0
    
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    QUANTAXIS>> code 000007 date 2017-01-24 price None order_model close amount_model by_amount
    

    ===== SETTLED None =====
    1000.0
    0.0< QA_Order datetime:2017-01-25 09:31:00 code:000001 price:9.26 towards:-1 btype:0x01 order_id:Order_Ot6U0EoW account:Acc_Q2nTwdDW status:300 >
    
    0.0
    0.0
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    QUANTAXIS>> code 000007 date 2017-01-25 price None order_model close amount_model by_amount
    

    ===== SETTLED None =====
    0.0
    0.0< QA_Order datetime:2017-01-26 09:31:00 code:000002 price:20.68 towards:1 btype:0x01 order_id:Order_A3ZBxmfE account:Acc_Q2nTwdDW status:300 >
    
    0.0
    

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    QUANTAXIS>> code 000007 date 2017-01-26 price None order_model close amount_model by_amount
    

    ===== SETTLED None =====
    [['2017-01-03 15:00:00', '000001', 9.16, 1000.0, 'Order_jwd6abQM', 'Trade_fKcr852C', 13.74], ['2017-01-05 15:00:00', '000001', 9.17, -1000.0, 'Order_MEZmuAS6', 'Trade_pYBEK34V', 13.754999999999999], ['2017-01-06 15:00:00', '000002', 20.64, 1000.0, 'Order_QPNR2bhr', 'Trade_JptrFeHZ', 30.96], ['2017-01-06 15:00:00', '000007', 25.45, 1000.0, 'Order_6MLOD9sg', 'Trade_JR67v3IS', 38.175], ['2017-01-09 15:00:00', '000002', 20.66, -1000.0, 'Order_Bp2t8SfF', 'Trade_HpGnldrh', 30.99], ['2017-01-09 15:00:00', '000004', 43.01, 1000.0, 'Order_tJfQDUKj', 'Trade_dh86K9BZ', 64.515], ['2017-01-09 15:00:00', '000007', 25.09, -1000.0, 'Order_W6iIOYJo', 'Trade_8S2Xdtxn', 37.635000000000005], ['2017-01-10 15:00:00', '000004', 43.25, 1000.0, 'Order_0M7pY4RQ', 'Trade_vYNXDuZz', 64.875], ['2017-01-10 15:00:00', '000007', 24.79, 1000.0, 'Order_Zud0fmbn', 'Trade_h5J4GRy2', 37.185], ['2017-01-11 15:00:00', '000004', 42.45, -1000.0, 'Order_rE5DgiGz', 'Trade_vyHzgTRU', 63.67500000000001], ['2017-01-11 15:00:00', '000007', 24.85, -1000.0, 'Order_Eudq2tNY', 'Trade_b5BeyLqv', 37.275000000000006], ['2017-01-12 15:00:00', '000001', 9.15, 1000.0, 'Order_UuMhpE5B', 'Trade_EbJUv9e1', 13.725000000000001], ['2017-01-12 15:00:00', '000004', 42.05, -1000.0, 'Order_rUENH54P', 'Trade_nxK4hc3N', 63.07499999999999], ['2017-01-13 15:00:00', '000001', 9.16, -1000.0, 'Order_Al9JbVa8', 'Trade_3O7hElGr', 13.74], ['2017-01-13 15:00:00', '000004', 41.0, 1000.0, 'Order_JQ14OW2N', 'Trade_QBMpVfcL', 61.5], ['2017-01-16 15:00:00', '000004', 38.26, -1000.0, 'Order_I47Er3in', 'Trade_icX9ICOR', 57.38999999999999], ['2017-01-18 15:00:00', '000004', 37.15, 1000.0, 'Order_vxPaKuZb', 'Trade_wISYX6cB', 55.724999999999994], ['2017-01-19 15:00:00', '000002', 20.6, 1000.0, 'Order_YFTPt5jH', 'Trade_NXrbQzsY', 30.900000000000002], ['2017-01-19 15:00:00', '000004', 35.69, -1000.0, 'Order_H21ocZ5q', 'Trade_8hqs3FXm', 53.535], ['2017-01-20 15:00:00', '000002', 20.68, -1000.0, 'Order_FMDtsGn9', 'Trade_DtUirlEm', 31.02], ['2017-01-23 15:00:00', '000002', 20.74, 1000.0, 'Order_SxeuKmRh', 'Trade_ejsQa7Si', 31.11], ['2017-01-24 15:00:00', '000001', 9.27, 1000.0, 'Order_H79EP6Ld', 'Trade_Wt0QfGco', 13.905], ['2017-01-24 15:00:00', '000002', 20.69, -1000.0, 'Order_w9WXpNQu', 'Trade_gnFQ4rJb', 31.035000000000004], ['2017-01-25 15:00:00', '000001', 9.26, -1000.0, 'Order_Ot6U0EoW', 'Trade_VCo24tPj', 13.889999999999999], ['2017-01-26 15:00:00', '000002', 20.68, 1000.0, 'Order_A3ZBxmfE', 'Trade_6UgTK5DO', 31.02]]
    [1000000, 990826.26, 999982.505, 979311.545, 953823.37, 974452.38, 931377.865, 956430.23, 913115.355, 888288.1699999999, 930674.4949999999, 955487.2199999999, 946323.4949999999, 988310.4199999999, 997456.6799999999, 956395.1799999999, 994597.7899999999, 957392.065, 936761.1649999999, 972397.6299999999, 993046.6099999999, 972275.4999999999, 962991.5949999999, 983650.5599999998, 992896.6699999998, 972185.6499999998]
    972185.6499999998
                   datetime    code  price  amount        order_id  \
    0   2017-01-03 15:00:00  000001   9.16  1000.0  Order_jwd6abQM   
    1   2017-01-05 15:00:00  000001   9.17 -1000.0  Order_MEZmuAS6   
    2   2017-01-06 15:00:00  000002  20.64  1000.0  Order_QPNR2bhr   
    3   2017-01-06 15:00:00  000007  25.45  1000.0  Order_6MLOD9sg   
    4   2017-01-09 15:00:00  000002  20.66 -1000.0  Order_Bp2t8SfF   
    5   2017-01-09 15:00:00  000004  43.01  1000.0  Order_tJfQDUKj   
    6   2017-01-09 15:00:00  000007  25.09 -1000.0  Order_W6iIOYJo   
    7   2017-01-10 15:00:00  000004  43.25  1000.0  Order_0M7pY4RQ   
    8   2017-01-10 15:00:00  000007  24.79  1000.0  Order_Zud0fmbn   
    9   2017-01-11 15:00:00  000004  42.45 -1000.0  Order_rE5DgiGz   
    10  2017-01-11 15:00:00  000007  24.85 -1000.0  Order_Eudq2tNY   
    11  2017-01-12 15:00:00  000001   9.15  1000.0  Order_UuMhpE5B   
    12  2017-01-12 15:00:00  000004  42.05 -1000.0  Order_rUENH54P   
    13  2017-01-13 15:00:00  000001   9.16 -1000.0  Order_Al9JbVa8   
    14  2017-01-13 15:00:00  000004  41.00  1000.0  Order_JQ14OW2N   
    15  2017-01-16 15:00:00  000004  38.26 -1000.0  Order_I47Er3in   
    16  2017-01-18 15:00:00  000004  37.15  1000.0  Order_vxPaKuZb   
    17  2017-01-19 15:00:00  000002  20.60  1000.0  Order_YFTPt5jH   
    18  2017-01-19 15:00:00  000004  35.69 -1000.0  Order_H21ocZ5q   
    19  2017-01-20 15:00:00  000002  20.68 -1000.0  Order_FMDtsGn9   
    20  2017-01-23 15:00:00  000002  20.74  1000.0  Order_SxeuKmRh   
    21  2017-01-24 15:00:00  000001   9.27  1000.0  Order_H79EP6Ld   
    22  2017-01-24 15:00:00  000002  20.69 -1000.0  Order_w9WXpNQu   
    23  2017-01-25 15:00:00  000001   9.26 -1000.0  Order_Ot6U0EoW   
    24  2017-01-26 15:00:00  000002  20.68  1000.0  Order_A3ZBxmfE   
    
              trade_id  commission_fee  
    0   Trade_fKcr852C          13.740  
    1   Trade_pYBEK34V          13.755  
    2   Trade_JptrFeHZ          30.960  
    3   Trade_JR67v3IS          38.175  
    4   Trade_HpGnldrh          30.990  
    5   Trade_dh86K9BZ          64.515  
    6   Trade_8S2Xdtxn          37.635  
    7   Trade_vYNXDuZz          64.875  
    8   Trade_h5J4GRy2          37.185  
    9   Trade_vyHzgTRU          63.675  
    10  Trade_b5BeyLqv          37.275  
    11  Trade_EbJUv9e1          13.725  
    12  Trade_nxK4hc3N          63.075  
    13  Trade_3O7hElGr          13.740  
    14  Trade_QBMpVfcL          61.500  
    15  Trade_icX9ICOR          57.390  
    16  Trade_wISYX6cB          55.725  
    17  Trade_NXrbQzsY          30.900  
    18  Trade_8hqs3FXm          53.535  
    19  Trade_DtUirlEm          31.020  
    20  Trade_ejsQa7Si          31.110  
    21  Trade_Wt0QfGco          13.905  
    22  Trade_gnFQ4rJb          31.035  
    23  Trade_VCo24tPj          13.890  
    24  Trade_6UgTK5DO          31.020  
    code
    000001       0.0
    000002    1000.0
    000004       0.0
    000007       0.0
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
      <td>2017-01-03 15:00:00</td>
      <td>000001</td>
      <td>9.16</td>
      <td>1000.0</td>
      <td>Order_jwd6abQM</td>
      <td>Trade_fKcr852C</td>
      <td>13.740</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017-01-05 15:00:00</td>
      <td>000001</td>
      <td>9.17</td>
      <td>-1000.0</td>
      <td>Order_MEZmuAS6</td>
      <td>Trade_pYBEK34V</td>
      <td>13.755</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-01-06 15:00:00</td>
      <td>000002</td>
      <td>20.64</td>
      <td>1000.0</td>
      <td>Order_QPNR2bhr</td>
      <td>Trade_JptrFeHZ</td>
      <td>30.960</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017-01-06 15:00:00</td>
      <td>000007</td>
      <td>25.45</td>
      <td>1000.0</td>
      <td>Order_6MLOD9sg</td>
      <td>Trade_JR67v3IS</td>
      <td>38.175</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017-01-09 15:00:00</td>
      <td>000002</td>
      <td>20.66</td>
      <td>-1000.0</td>
      <td>Order_Bp2t8SfF</td>
      <td>Trade_HpGnldrh</td>
      <td>30.990</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2017-01-09 15:00:00</td>
      <td>000004</td>
      <td>43.01</td>
      <td>1000.0</td>
      <td>Order_tJfQDUKj</td>
      <td>Trade_dh86K9BZ</td>
      <td>64.515</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2017-01-09 15:00:00</td>
      <td>000007</td>
      <td>25.09</td>
      <td>-1000.0</td>
      <td>Order_W6iIOYJo</td>
      <td>Trade_8S2Xdtxn</td>
      <td>37.635</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2017-01-10 15:00:00</td>
      <td>000004</td>
      <td>43.25</td>
      <td>1000.0</td>
      <td>Order_0M7pY4RQ</td>
      <td>Trade_vYNXDuZz</td>
      <td>64.875</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2017-01-10 15:00:00</td>
      <td>000007</td>
      <td>24.79</td>
      <td>1000.0</td>
      <td>Order_Zud0fmbn</td>
      <td>Trade_h5J4GRy2</td>
      <td>37.185</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2017-01-11 15:00:00</td>
      <td>000004</td>
      <td>42.45</td>
      <td>-1000.0</td>
      <td>Order_rE5DgiGz</td>
      <td>Trade_vyHzgTRU</td>
      <td>63.675</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2017-01-11 15:00:00</td>
      <td>000007</td>
      <td>24.85</td>
      <td>-1000.0</td>
      <td>Order_Eudq2tNY</td>
      <td>Trade_b5BeyLqv</td>
      <td>37.275</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2017-01-12 15:00:00</td>
      <td>000001</td>
      <td>9.15</td>
      <td>1000.0</td>
      <td>Order_UuMhpE5B</td>
      <td>Trade_EbJUv9e1</td>
      <td>13.725</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2017-01-12 15:00:00</td>
      <td>000004</td>
      <td>42.05</td>
      <td>-1000.0</td>
      <td>Order_rUENH54P</td>
      <td>Trade_nxK4hc3N</td>
      <td>63.075</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2017-01-13 15:00:00</td>
      <td>000001</td>
      <td>9.16</td>
      <td>-1000.0</td>
      <td>Order_Al9JbVa8</td>
      <td>Trade_3O7hElGr</td>
      <td>13.740</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2017-01-13 15:00:00</td>
      <td>000004</td>
      <td>41.00</td>
      <td>1000.0</td>
      <td>Order_JQ14OW2N</td>
      <td>Trade_QBMpVfcL</td>
      <td>61.500</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2017-01-16 15:00:00</td>
      <td>000004</td>
      <td>38.26</td>
      <td>-1000.0</td>
      <td>Order_I47Er3in</td>
      <td>Trade_icX9ICOR</td>
      <td>57.390</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2017-01-18 15:00:00</td>
      <td>000004</td>
      <td>37.15</td>
      <td>1000.0</td>
      <td>Order_vxPaKuZb</td>
      <td>Trade_wISYX6cB</td>
      <td>55.725</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2017-01-19 15:00:00</td>
      <td>000002</td>
      <td>20.60</td>
      <td>1000.0</td>
      <td>Order_YFTPt5jH</td>
      <td>Trade_NXrbQzsY</td>
      <td>30.900</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2017-01-19 15:00:00</td>
      <td>000004</td>
      <td>35.69</td>
      <td>-1000.0</td>
      <td>Order_H21ocZ5q</td>
      <td>Trade_8hqs3FXm</td>
      <td>53.535</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2017-01-20 15:00:00</td>
      <td>000002</td>
      <td>20.68</td>
      <td>-1000.0</td>
      <td>Order_FMDtsGn9</td>
      <td>Trade_DtUirlEm</td>
      <td>31.020</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2017-01-23 15:00:00</td>
      <td>000002</td>
      <td>20.74</td>
      <td>1000.0</td>
      <td>Order_SxeuKmRh</td>
      <td>Trade_ejsQa7Si</td>
      <td>31.110</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2017-01-24 15:00:00</td>
      <td>000001</td>
      <td>9.27</td>
      <td>1000.0</td>
      <td>Order_H79EP6Ld</td>
      <td>Trade_Wt0QfGco</td>
      <td>13.905</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2017-01-24 15:00:00</td>
      <td>000002</td>
      <td>20.69</td>
      <td>-1000.0</td>
      <td>Order_w9WXpNQu</td>
      <td>Trade_gnFQ4rJb</td>
      <td>31.035</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2017-01-25 15:00:00</td>
      <td>000001</td>
      <td>9.26</td>
      <td>-1000.0</td>
      <td>Order_Ot6U0EoW</td>
      <td>Trade_VCo24tPj</td>
      <td>13.890</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2017-01-26 15:00:00</td>
      <td>000002</td>
      <td>20.68</td>
      <td>1000.0</td>
      <td>Order_A3ZBxmfE</td>
      <td>Trade_6UgTK5DO</td>
      <td>31.020</td>
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
    000002    1000.0
    000004       0.0
    000007       0.0
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
      <th>2017-01-03 15:00:00</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-05 15:00:00</th>
      <td>-1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-06 15:00:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-09 15:00:00</th>
      <td>0.0</td>
      <td>-1000.0</td>
      <td>1000.0</td>
      <td>-1000.0</td>
    </tr>
    <tr>
      <th>2017-01-10 15:00:00</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-11 15:00:00</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>-1000.0</td>
      <td>-1000.0</td>
    </tr>
    <tr>
      <th>2017-01-12 15:00:00</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-13 15:00:00</th>
      <td>-1000.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-16 15:00:00</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-18 15:00:00</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-19 15:00:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-20 15:00:00</th>
      <td>0.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-23 15:00:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-24 15:00:00</th>
      <td>1000.0</td>
      <td>-1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-25 15:00:00</th>
      <td>-1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-26 15:00:00</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
user.get_account(a_1).daily_hold
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
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-01-03</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-05</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-06</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-09</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-10</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>2000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-11</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-12</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-13</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-16</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-18</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-19</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-20</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-23</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-24</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-25</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-26</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
market.insert_order(account_id=a_1, amount=2000, price=None, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT, time='2017-01-27', code='000001',
                    order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.SELL, market_type=QA.MARKET_TYPE.STOCK_DAY,
                    data_type=QA.MARKETDATA_TYPE.DAY, broker_name=QA.BROKER_TYPE.BACKETEST)
```

    QUANTAXIS>> MARKET WARING: SOMEING WRONG WITH ORDER 
     
    QUANTAXIS>> code 000001 date 2017-01-27 price None order_model close amount_model by_amount
    


```python
    market._settle(QA.BROKER_TYPE.BACKETEST)
```

    ===== SETTLED None =====
    


```python
user.get_account(a_1).daily_hold
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
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-01-03</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-05</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-06</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-09</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-10</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>2000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-11</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-12</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-13</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-16</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-18</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-19</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-20</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-23</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-24</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-25</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-26</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
data=QA.QA_fetch_stock_day_adv(['000001','000002','000004','000007'],'2017-01-03','2017-01-26')
```


```python
md=data.pivot('close')
md
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
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-01-03</th>
      <td>9.16</td>
      <td>20.73</td>
      <td>44.45</td>
      <td>26.10</td>
    </tr>
    <tr>
      <th>2017-01-04</th>
      <td>9.16</td>
      <td>20.85</td>
      <td>44.70</td>
      <td>26.47</td>
    </tr>
    <tr>
      <th>2017-01-05</th>
      <td>9.17</td>
      <td>20.93</td>
      <td>44.44</td>
      <td>26.24</td>
    </tr>
    <tr>
      <th>2017-01-06</th>
      <td>9.13</td>
      <td>20.64</td>
      <td>43.96</td>
      <td>25.45</td>
    </tr>
    <tr>
      <th>2017-01-09</th>
      <td>9.15</td>
      <td>20.66</td>
      <td>43.01</td>
      <td>25.09</td>
    </tr>
    <tr>
      <th>2017-01-10</th>
      <td>9.15</td>
      <td>20.58</td>
      <td>43.25</td>
      <td>24.79</td>
    </tr>
    <tr>
      <th>2017-01-11</th>
      <td>9.14</td>
      <td>20.40</td>
      <td>42.45</td>
      <td>24.85</td>
    </tr>
    <tr>
      <th>2017-01-12</th>
      <td>9.15</td>
      <td>NaN</td>
      <td>42.05</td>
      <td>24.61</td>
    </tr>
    <tr>
      <th>2017-01-13</th>
      <td>9.16</td>
      <td>21.81</td>
      <td>41.00</td>
      <td>23.81</td>
    </tr>
    <tr>
      <th>2017-01-16</th>
      <td>9.14</td>
      <td>21.00</td>
      <td>38.26</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-01-17</th>
      <td>9.15</td>
      <td>20.80</td>
      <td>37.37</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-01-18</th>
      <td>9.17</td>
      <td>20.92</td>
      <td>37.15</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-01-19</th>
      <td>9.18</td>
      <td>20.60</td>
      <td>35.69</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-01-20</th>
      <td>9.22</td>
      <td>20.68</td>
      <td>36.48</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-01-23</th>
      <td>9.22</td>
      <td>20.74</td>
      <td>37.56</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-01-24</th>
      <td>9.27</td>
      <td>20.69</td>
      <td>38.63</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-01-25</th>
      <td>9.26</td>
      <td>20.61</td>
      <td>38.25</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-01-26</th>
      <td>9.33</td>
      <td>20.68</td>
      <td>38.29</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




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
      <td>2017-01-03 15:00:00</td>
      <td>000001</td>
      <td>9.16</td>
      <td>1000.0</td>
      <td>Order_jwd6abQM</td>
      <td>Trade_fKcr852C</td>
      <td>13.740</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017-01-05 15:00:00</td>
      <td>000001</td>
      <td>9.17</td>
      <td>-1000.0</td>
      <td>Order_MEZmuAS6</td>
      <td>Trade_pYBEK34V</td>
      <td>13.755</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-01-06 15:00:00</td>
      <td>000002</td>
      <td>20.64</td>
      <td>1000.0</td>
      <td>Order_QPNR2bhr</td>
      <td>Trade_JptrFeHZ</td>
      <td>30.960</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017-01-06 15:00:00</td>
      <td>000007</td>
      <td>25.45</td>
      <td>1000.0</td>
      <td>Order_6MLOD9sg</td>
      <td>Trade_JR67v3IS</td>
      <td>38.175</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017-01-09 15:00:00</td>
      <td>000002</td>
      <td>20.66</td>
      <td>-1000.0</td>
      <td>Order_Bp2t8SfF</td>
      <td>Trade_HpGnldrh</td>
      <td>30.990</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2017-01-09 15:00:00</td>
      <td>000004</td>
      <td>43.01</td>
      <td>1000.0</td>
      <td>Order_tJfQDUKj</td>
      <td>Trade_dh86K9BZ</td>
      <td>64.515</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2017-01-09 15:00:00</td>
      <td>000007</td>
      <td>25.09</td>
      <td>-1000.0</td>
      <td>Order_W6iIOYJo</td>
      <td>Trade_8S2Xdtxn</td>
      <td>37.635</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2017-01-10 15:00:00</td>
      <td>000004</td>
      <td>43.25</td>
      <td>1000.0</td>
      <td>Order_0M7pY4RQ</td>
      <td>Trade_vYNXDuZz</td>
      <td>64.875</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2017-01-10 15:00:00</td>
      <td>000007</td>
      <td>24.79</td>
      <td>1000.0</td>
      <td>Order_Zud0fmbn</td>
      <td>Trade_h5J4GRy2</td>
      <td>37.185</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2017-01-11 15:00:00</td>
      <td>000004</td>
      <td>42.45</td>
      <td>-1000.0</td>
      <td>Order_rE5DgiGz</td>
      <td>Trade_vyHzgTRU</td>
      <td>63.675</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2017-01-11 15:00:00</td>
      <td>000007</td>
      <td>24.85</td>
      <td>-1000.0</td>
      <td>Order_Eudq2tNY</td>
      <td>Trade_b5BeyLqv</td>
      <td>37.275</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2017-01-12 15:00:00</td>
      <td>000001</td>
      <td>9.15</td>
      <td>1000.0</td>
      <td>Order_UuMhpE5B</td>
      <td>Trade_EbJUv9e1</td>
      <td>13.725</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2017-01-12 15:00:00</td>
      <td>000004</td>
      <td>42.05</td>
      <td>-1000.0</td>
      <td>Order_rUENH54P</td>
      <td>Trade_nxK4hc3N</td>
      <td>63.075</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2017-01-13 15:00:00</td>
      <td>000001</td>
      <td>9.16</td>
      <td>-1000.0</td>
      <td>Order_Al9JbVa8</td>
      <td>Trade_3O7hElGr</td>
      <td>13.740</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2017-01-13 15:00:00</td>
      <td>000004</td>
      <td>41.00</td>
      <td>1000.0</td>
      <td>Order_JQ14OW2N</td>
      <td>Trade_QBMpVfcL</td>
      <td>61.500</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2017-01-16 15:00:00</td>
      <td>000004</td>
      <td>38.26</td>
      <td>-1000.0</td>
      <td>Order_I47Er3in</td>
      <td>Trade_icX9ICOR</td>
      <td>57.390</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2017-01-18 15:00:00</td>
      <td>000004</td>
      <td>37.15</td>
      <td>1000.0</td>
      <td>Order_vxPaKuZb</td>
      <td>Trade_wISYX6cB</td>
      <td>55.725</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2017-01-19 15:00:00</td>
      <td>000002</td>
      <td>20.60</td>
      <td>1000.0</td>
      <td>Order_YFTPt5jH</td>
      <td>Trade_NXrbQzsY</td>
      <td>30.900</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2017-01-19 15:00:00</td>
      <td>000004</td>
      <td>35.69</td>
      <td>-1000.0</td>
      <td>Order_H21ocZ5q</td>
      <td>Trade_8hqs3FXm</td>
      <td>53.535</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2017-01-20 15:00:00</td>
      <td>000002</td>
      <td>20.68</td>
      <td>-1000.0</td>
      <td>Order_FMDtsGn9</td>
      <td>Trade_DtUirlEm</td>
      <td>31.020</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2017-01-23 15:00:00</td>
      <td>000002</td>
      <td>20.74</td>
      <td>1000.0</td>
      <td>Order_SxeuKmRh</td>
      <td>Trade_ejsQa7Si</td>
      <td>31.110</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2017-01-24 15:00:00</td>
      <td>000001</td>
      <td>9.27</td>
      <td>1000.0</td>
      <td>Order_H79EP6Ld</td>
      <td>Trade_Wt0QfGco</td>
      <td>13.905</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2017-01-24 15:00:00</td>
      <td>000002</td>
      <td>20.69</td>
      <td>-1000.0</td>
      <td>Order_w9WXpNQu</td>
      <td>Trade_gnFQ4rJb</td>
      <td>31.035</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2017-01-25 15:00:00</td>
      <td>000001</td>
      <td>9.26</td>
      <td>-1000.0</td>
      <td>Order_Ot6U0EoW</td>
      <td>Trade_VCo24tPj</td>
      <td>13.890</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2017-01-26 15:00:00</td>
      <td>000002</td>
      <td>20.68</td>
      <td>1000.0</td>
      <td>Order_A3ZBxmfE</td>
      <td>Trade_6UgTK5DO</td>
      <td>31.020</td>
    </tr>
  </tbody>
</table>
</div>




```python
user.get_account(a_1).cash_table

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
      <th>cash</th>
      <th>datetime</th>
      <th>date</th>
    </tr>
    <tr>
      <th>datetime</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-01-03 15:00:00</th>
      <td>990826</td>
      <td>2017-01-03 15:00:00</td>
      <td>2017-01-03</td>
    </tr>
    <tr>
      <th>2017-01-05 15:00:00</th>
      <td>999983</td>
      <td>2017-01-05 15:00:00</td>
      <td>2017-01-05</td>
    </tr>
    <tr>
      <th>2017-01-06 15:00:00</th>
      <td>979312</td>
      <td>2017-01-06 15:00:00</td>
      <td>2017-01-06</td>
    </tr>
    <tr>
      <th>2017-01-06 15:00:00</th>
      <td>953823</td>
      <td>2017-01-06 15:00:00</td>
      <td>2017-01-06</td>
    </tr>
    <tr>
      <th>2017-01-09 15:00:00</th>
      <td>974452</td>
      <td>2017-01-09 15:00:00</td>
      <td>2017-01-09</td>
    </tr>
    <tr>
      <th>2017-01-09 15:00:00</th>
      <td>931378</td>
      <td>2017-01-09 15:00:00</td>
      <td>2017-01-09</td>
    </tr>
    <tr>
      <th>2017-01-09 15:00:00</th>
      <td>956430</td>
      <td>2017-01-09 15:00:00</td>
      <td>2017-01-09</td>
    </tr>
    <tr>
      <th>2017-01-10 15:00:00</th>
      <td>913115</td>
      <td>2017-01-10 15:00:00</td>
      <td>2017-01-10</td>
    </tr>
    <tr>
      <th>2017-01-10 15:00:00</th>
      <td>888288</td>
      <td>2017-01-10 15:00:00</td>
      <td>2017-01-10</td>
    </tr>
    <tr>
      <th>2017-01-11 15:00:00</th>
      <td>930674</td>
      <td>2017-01-11 15:00:00</td>
      <td>2017-01-11</td>
    </tr>
    <tr>
      <th>2017-01-11 15:00:00</th>
      <td>955487</td>
      <td>2017-01-11 15:00:00</td>
      <td>2017-01-11</td>
    </tr>
    <tr>
      <th>2017-01-12 15:00:00</th>
      <td>946323</td>
      <td>2017-01-12 15:00:00</td>
      <td>2017-01-12</td>
    </tr>
    <tr>
      <th>2017-01-12 15:00:00</th>
      <td>988310</td>
      <td>2017-01-12 15:00:00</td>
      <td>2017-01-12</td>
    </tr>
    <tr>
      <th>2017-01-13 15:00:00</th>
      <td>997457</td>
      <td>2017-01-13 15:00:00</td>
      <td>2017-01-13</td>
    </tr>
    <tr>
      <th>2017-01-13 15:00:00</th>
      <td>956395</td>
      <td>2017-01-13 15:00:00</td>
      <td>2017-01-13</td>
    </tr>
    <tr>
      <th>2017-01-16 15:00:00</th>
      <td>994598</td>
      <td>2017-01-16 15:00:00</td>
      <td>2017-01-16</td>
    </tr>
    <tr>
      <th>2017-01-18 15:00:00</th>
      <td>957392</td>
      <td>2017-01-18 15:00:00</td>
      <td>2017-01-18</td>
    </tr>
    <tr>
      <th>2017-01-19 15:00:00</th>
      <td>936761</td>
      <td>2017-01-19 15:00:00</td>
      <td>2017-01-19</td>
    </tr>
    <tr>
      <th>2017-01-19 15:00:00</th>
      <td>972398</td>
      <td>2017-01-19 15:00:00</td>
      <td>2017-01-19</td>
    </tr>
    <tr>
      <th>2017-01-20 15:00:00</th>
      <td>993047</td>
      <td>2017-01-20 15:00:00</td>
      <td>2017-01-20</td>
    </tr>
    <tr>
      <th>2017-01-23 15:00:00</th>
      <td>972275</td>
      <td>2017-01-23 15:00:00</td>
      <td>2017-01-23</td>
    </tr>
    <tr>
      <th>2017-01-24 15:00:00</th>
      <td>962992</td>
      <td>2017-01-24 15:00:00</td>
      <td>2017-01-24</td>
    </tr>
    <tr>
      <th>2017-01-24 15:00:00</th>
      <td>983651</td>
      <td>2017-01-24 15:00:00</td>
      <td>2017-01-24</td>
    </tr>
    <tr>
      <th>2017-01-25 15:00:00</th>
      <td>992897</td>
      <td>2017-01-25 15:00:00</td>
      <td>2017-01-25</td>
    </tr>
    <tr>
      <th>2017-01-26 15:00:00</th>
      <td>972186</td>
      <td>2017-01-26 15:00:00</td>
      <td>2017-01-26</td>
    </tr>
  </tbody>
</table>
</div>




```python
user.get_account(a_1).daily_cash
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
      <th>cash</th>
      <th>datetime</th>
      <th>date</th>
    </tr>
    <tr>
      <th>datetime</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-01-03 15:00:00</th>
      <td>990826</td>
      <td>2017-01-03 15:00:00</td>
      <td>2017-01-03</td>
    </tr>
    <tr>
      <th>2017-01-05 15:00:00</th>
      <td>999983</td>
      <td>2017-01-05 15:00:00</td>
      <td>2017-01-05</td>
    </tr>
    <tr>
      <th>2017-01-06 15:00:00</th>
      <td>953823</td>
      <td>2017-01-06 15:00:00</td>
      <td>2017-01-06</td>
    </tr>
    <tr>
      <th>2017-01-09 15:00:00</th>
      <td>956430</td>
      <td>2017-01-09 15:00:00</td>
      <td>2017-01-09</td>
    </tr>
    <tr>
      <th>2017-01-10 15:00:00</th>
      <td>888288</td>
      <td>2017-01-10 15:00:00</td>
      <td>2017-01-10</td>
    </tr>
    <tr>
      <th>2017-01-11 15:00:00</th>
      <td>955487</td>
      <td>2017-01-11 15:00:00</td>
      <td>2017-01-11</td>
    </tr>
    <tr>
      <th>2017-01-12 15:00:00</th>
      <td>988310</td>
      <td>2017-01-12 15:00:00</td>
      <td>2017-01-12</td>
    </tr>
    <tr>
      <th>2017-01-13 15:00:00</th>
      <td>956395</td>
      <td>2017-01-13 15:00:00</td>
      <td>2017-01-13</td>
    </tr>
    <tr>
      <th>2017-01-16 15:00:00</th>
      <td>994598</td>
      <td>2017-01-16 15:00:00</td>
      <td>2017-01-16</td>
    </tr>
    <tr>
      <th>2017-01-18 15:00:00</th>
      <td>957392</td>
      <td>2017-01-18 15:00:00</td>
      <td>2017-01-18</td>
    </tr>
    <tr>
      <th>2017-01-19 15:00:00</th>
      <td>972398</td>
      <td>2017-01-19 15:00:00</td>
      <td>2017-01-19</td>
    </tr>
    <tr>
      <th>2017-01-20 15:00:00</th>
      <td>993047</td>
      <td>2017-01-20 15:00:00</td>
      <td>2017-01-20</td>
    </tr>
    <tr>
      <th>2017-01-23 15:00:00</th>
      <td>972275</td>
      <td>2017-01-23 15:00:00</td>
      <td>2017-01-23</td>
    </tr>
    <tr>
      <th>2017-01-24 15:00:00</th>
      <td>983651</td>
      <td>2017-01-24 15:00:00</td>
      <td>2017-01-24</td>
    </tr>
    <tr>
      <th>2017-01-25 15:00:00</th>
      <td>992897</td>
      <td>2017-01-25 15:00:00</td>
      <td>2017-01-25</td>
    </tr>
    <tr>
      <th>2017-01-26 15:00:00</th>
      <td>972186</td>
      <td>2017-01-26 15:00:00</td>
      <td>2017-01-26</td>
    </tr>
  </tbody>
</table>
</div>




```python
user.get_account(a_1).daily_hold
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
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-01-03</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-05</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-06</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-09</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-10</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>2000.0</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2017-01-11</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-12</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-13</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-16</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-18</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-19</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-20</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-23</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-24</th>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-25</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-01-26</th>
      <td>0.0</td>
      <td>1000.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
data=user.get_account(a_1).daily_hold
```


```python
market_data=QA.QA_fetch_stock_day_adv(list(data.columns),data.index[0],data.index[-1])
```


```python
(market_data.to_qfq().pivot('close')*data).sum(axis=1)+user.get_account(a_1).daily_cash.set_index('date').cash
```

    c:\quantaxis\QUANTAXIS\QAData\data_fq.py:53: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      bfq_data['if_trade'] = 1
    




    date
    2017-01-03    999986
    2017-01-04       NaN
    2017-01-05    999983
    2017-01-06    999913
    2017-01-09    999440
    2017-01-10    999578
    2017-01-11    997937
    2017-01-12    997460
    2017-01-13    997395
    2017-01-16    994598
    2017-01-17       NaN
    2017-01-18    994542
    2017-01-19    992998
    2017-01-20    993047
    2017-01-23    993015
    2017-01-24    992921
    2017-01-25    992897
    2017-01-26    992866
    dtype: object


