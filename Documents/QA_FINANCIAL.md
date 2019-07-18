# QUANTAXIS 的一般/高级财务方法


1.QA.QA_fetch_financial_report(code,report_date)

其中, report_date 是需要手动指定的财务时间, 可以是单个时间,也可以是一列时间:
  > '2018-03-31'  或者['2017-03-31','2017-06-30','2017-09-31','2017-12-31','2018-03-31']
  > 此方法的意义在于指定特定的财务时间(如年报)
  
返回的是一个MultiIndex的dataframe
 
2.QA.QA_fetch_financial_report_adv(code,start,end)

支持随意的跨时间索引, start 和end不用刻意指定

如果end不写,则start参数等同于report_date的用法

返回的是QA_DataStruct_Financial 类

3. QA_DataStruct_Financial 类, 可以直接加载在基础方法返回的dataframe中

> QDF.get_report_by_date(code,date) 返回某个股票的某个时间点的财报

> QDF.get_key(code,date,key) 返回某个股票某个时间点的财报的某个指标



```python
import QUANTAXIS as QA
import pandas as pd

```
```python
res=QA.QA_fetch_financial_report(['000001','600100'],['2017-03-31','2017-06-30','2017-09-31','2017-12-31','2018-03-31'])
```


```python
res
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>EPS</th>
      <th>deductEPS</th>
      <th>undistributedProfitPerShare</th>
      <th>netAssetsPerShare</th>
      <th>capitalReservePerShare</th>
      <th>ROE</th>
      <th>operatingCashFlowPerShare</th>
      <th>moneyFunds</th>
      <th>tradingFinancialAssets</th>
      <th>billsReceivables</th>
      <th>...</th>
      <th>netProfitLastYear</th>
      <th>277</th>
      <th>278</th>
      <th>279</th>
      <th>280</th>
      <th>281</th>
      <th>282</th>
      <th>_id</th>
      <th>code</th>
      <th>report_date</th>
    </tr>
    <tr>
      <th>report_date</th>
      <th>code</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-03-31</th>
      <th>000001</th>
      <td>0.3100</td>
      <td>0.3100</td>
      <td>4.05</td>
      <td>10.9400</td>
      <td>3.29</td>
      <td>2.992</td>
      <td>-6.700</td>
      <td>7.121477e+11</td>
      <td>4.404400e+10</td>
      <td>NaN</td>
      <td>...</td>
      <td>2.272700e+10</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>6.955837e+08</td>
      <td>2.89</td>
      <td>0.3617</td>
      <td>5b3edccc50d2c15048795415</td>
      <td>000001</td>
      <td>2017-03-31</td>
    </tr>
    <tr>
      <th>2017-06-30</th>
      <th>000001</th>
      <td>0.6800</td>
      <td>0.6800</td>
      <td>4.26</td>
      <td>11.1500</td>
      <td>3.29</td>
      <td>6.100</td>
      <td>-7.470</td>
      <td>7.522773e+11</td>
      <td>4.908300e+10</td>
      <td>NaN</td>
      <td>...</td>
      <td>2.286100e+10</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>7.684470e+08</td>
      <td>6.21</td>
      <td>0.3670</td>
      <td>5b3edcce50d2c15048796114</td>
      <td>000001</td>
      <td>2017-06-30</td>
    </tr>
    <tr>
      <th>2017-12-31</th>
      <th>000001</th>
      <td>1.3000</td>
      <td>1.3000</td>
      <td>4.64</td>
      <td>11.7706</td>
      <td>3.29</td>
      <td>11.474</td>
      <td>-6.920</td>
      <td>7.506320e+11</td>
      <td>3.957500e+10</td>
      <td>NaN</td>
      <td>...</td>
      <td>2.318900e+10</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>1.071157e+09</td>
      <td>11.62</td>
      <td>0.2348</td>
      <td>5b3edcd150d2c15048797c47</td>
      <td>000001</td>
      <td>2017-12-31</td>
    </tr>
    <tr>
      <th>2018-03-31</th>
      <th>000001</th>
      <td>0.3300</td>
      <td>0.3300</td>
      <td>4.69</td>
      <td>11.8500</td>
      <td>3.29</td>
      <td>3.242</td>
      <td>2.410</td>
      <td>6.699981e+11</td>
      <td>7.684500e+10</td>
      <td>NaN</td>
      <td>...</td>
      <td>2.357000e+10</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>9.828775e+08</td>
      <td>2.79</td>
      <td>0.3818</td>
      <td>5b3edcd250d2c15048798a07</td>
      <td>000001</td>
      <td>2018-03-31</td>
    </tr>
    <tr>
      <th>2017-03-31</th>
      <th>600100</th>
      <td>-0.0908</td>
      <td>-0.1030</td>
      <td>2.57</td>
      <td>7.1879</td>
      <td>3.15</td>
      <td>-1.263</td>
      <td>-0.885</td>
      <td>7.738101e+09</td>
      <td>9.173491e+08</td>
      <td>90043088.0</td>
      <td>...</td>
      <td>-1.169131e+09</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>4.155126e+07</td>
      <td>-1.25</td>
      <td>-0.1030</td>
      <td>5b3edccc50d2c15048795c3a</td>
      <td>600100</td>
      <td>2017-03-31</td>
    </tr>
    <tr>
      <th>2017-06-30</th>
      <th>600100</th>
      <td>-0.0407</td>
      <td>-0.0598</td>
      <td>2.37</td>
      <td>6.9775</td>
      <td>3.15</td>
      <td>-0.584</td>
      <td>-1.124</td>
      <td>8.756578e+09</td>
      <td>7.745308e+08</td>
      <td>52524456.0</td>
      <td>...</td>
      <td>-7.752181e+08</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>4.842445e+07</td>
      <td>-0.56</td>
      <td>0.0432</td>
      <td>5b3edcce50d2c15048796987</td>
      <td>600100</td>
      <td>2017-06-30</td>
    </tr>
    <tr>
      <th>2017-12-31</th>
      <th>600100</th>
      <td>0.0350</td>
      <td>-0.0115</td>
      <td>2.45</td>
      <td>7.1765</td>
      <td>3.10</td>
      <td>0.487</td>
      <td>0.153</td>
      <td>9.766134e+09</td>
      <td>5.818680e+08</td>
      <td>117617800.0</td>
      <td>...</td>
      <td>1.036393e+08</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>4.0</td>
      <td>5.628596e+07</td>
      <td>0.48</td>
      <td>0.0791</td>
      <td>5b3edcd150d2c150487984ca</td>
      <td>600100</td>
      <td>2017-12-31</td>
    </tr>
    <tr>
      <th>2018-03-31</th>
      <th>600100</th>
      <td>-0.0756</td>
      <td>-0.0871</td>
      <td>2.37</td>
      <td>7.1433</td>
      <td>3.20</td>
      <td>-1.058</td>
      <td>-0.757</td>
      <td>7.666613e+09</td>
      <td>5.546273e+08</td>
      <td>97230120.0</td>
      <td>...</td>
      <td>1.487741e+08</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>4.165037e+07</td>
      <td>-1.06</td>
      <td>-0.0871</td>
      <td>5b3edcd250d2c15048799289</td>
      <td>600100</td>
      <td>2018-03-31</td>
    </tr>
  </tbody>
</table>
<p>8 rows × 285 columns</p>
</div>




```python
res_adv=QA.QA_fetch_financial_report_adv('000001','2017-01-01','2018-05-01')
```


```python
res_adv
```




    < QA_DataStruct_Financial >




```python
res_adv.data
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>EPS</th>
      <th>deductEPS</th>
      <th>undistributedProfitPerShare</th>
      <th>netAssetsPerShare</th>
      <th>capitalReservePerShare</th>
      <th>ROE</th>
      <th>operatingCashFlowPerShare</th>
      <th>moneyFunds</th>
      <th>tradingFinancialAssets</th>
      <th>billsReceivables</th>
      <th>...</th>
      <th>netProfitLastYear</th>
      <th>277</th>
      <th>278</th>
      <th>279</th>
      <th>280</th>
      <th>281</th>
      <th>282</th>
      <th>_id</th>
      <th>code</th>
      <th>report_date</th>
    </tr>
    <tr>
      <th>report_date</th>
      <th>code</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-03-31</th>
      <th>000001</th>
      <td>0.31</td>
      <td>0.31</td>
      <td>4.05</td>
      <td>10.9400</td>
      <td>3.29</td>
      <td>2.992</td>
      <td>-6.70</td>
      <td>7.121477e+11</td>
      <td>4.404400e+10</td>
      <td>NaN</td>
      <td>...</td>
      <td>2.272700e+10</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>6.955837e+08</td>
      <td>2.89</td>
      <td>0.3617</td>
      <td>5b3edccc50d2c15048795415</td>
      <td>000001</td>
      <td>2017-03-31</td>
    </tr>
    <tr>
      <th>2017-06-30</th>
      <th>000001</th>
      <td>0.68</td>
      <td>0.68</td>
      <td>4.26</td>
      <td>11.1500</td>
      <td>3.29</td>
      <td>6.100</td>
      <td>-7.47</td>
      <td>7.522773e+11</td>
      <td>4.908300e+10</td>
      <td>NaN</td>
      <td>...</td>
      <td>2.286100e+10</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>7.684470e+08</td>
      <td>6.21</td>
      <td>0.3670</td>
      <td>5b3edcce50d2c15048796114</td>
      <td>000001</td>
      <td>2017-06-30</td>
    </tr>
    <tr>
      <th>2017-09-30</th>
      <th>000001</th>
      <td>1.06</td>
      <td>1.06</td>
      <td>4.64</td>
      <td>11.5400</td>
      <td>3.29</td>
      <td>8.782</td>
      <td>-9.20</td>
      <td>7.265024e+11</td>
      <td>4.132700e+10</td>
      <td>NaN</td>
      <td>...</td>
      <td>2.303300e+10</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>8.339691e+08</td>
      <td>9.60</td>
      <td>0.3854</td>
      <td>5b3edccf50d2c15048796eaa</td>
      <td>000001</td>
      <td>2017-09-30</td>
    </tr>
    <tr>
      <th>2017-12-31</th>
      <th>000001</th>
      <td>1.30</td>
      <td>1.30</td>
      <td>4.64</td>
      <td>11.7706</td>
      <td>3.29</td>
      <td>11.474</td>
      <td>-6.92</td>
      <td>7.506320e+11</td>
      <td>3.957500e+10</td>
      <td>NaN</td>
      <td>...</td>
      <td>2.318900e+10</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>1.071157e+09</td>
      <td>11.62</td>
      <td>0.2348</td>
      <td>5b3edcd150d2c15048797c47</td>
      <td>000001</td>
      <td>2017-12-31</td>
    </tr>
    <tr>
      <th>2018-03-31</th>
      <th>000001</th>
      <td>0.33</td>
      <td>0.33</td>
      <td>4.69</td>
      <td>11.8500</td>
      <td>3.29</td>
      <td>3.242</td>
      <td>2.41</td>
      <td>6.699981e+11</td>
      <td>7.684500e+10</td>
      <td>NaN</td>
      <td>...</td>
      <td>2.357000e+10</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>9.828775e+08</td>
      <td>2.79</td>
      <td>0.3818</td>
      <td>5b3edcd250d2c15048798a07</td>
      <td>000001</td>
      <td>2018-03-31</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 285 columns</p>
</div>




```python
fds=QA.QA_DataStruct_Financial(res)
```


```python
fds
```




    < QA_DataStruct_Financial >




```python
fds.get_key('600100','2017-03-31','ROE')
```




    -1.2630000114




```python
fds.get_report_by_date('600100','2017-03-31')
```




    EPS                                                            -0.0908
    deductEPS                                                       -0.103
    undistributedProfitPerShare                                       2.57
    netAssetsPerShare                                               7.1879
    capitalReservePerShare                                            3.15
    ROE                                                             -1.263
    operatingCashFlowPerShare                                       -0.885
    moneyFunds                                                  7.7381e+09
    tradingFinancialAssets                                     9.17349e+08
    billsReceivables                                           9.00431e+07
    accountsReceivables                                        7.19131e+09
    prepayments                                                1.51541e+09
    otherReceivables                                           9.41644e+08
    interCompanyReceivables                                            NaN
    interestReceivables                                                  0
    dividendsReceivables                                       1.68134e+07
    inventory                                                  9.57452e+09
    expendableBiologicalAssets                                         NaN
    noncurrentAssetsDueWithinOneYear                                     0
    otherLiquidAssets                                          3.17298e+09
    totalLiquidAssets                                          3.11582e+10
    availableForSaleSecurities                                 2.92698e+09
    heldToMaturityInvestments                                            0
    longTermReceivables                                        8.95877e+08
    longTermEquityInvestment                                   1.33009e+10
    investmentRealEstate                                       1.45896e+07
    fixedAssets                                                3.26195e+09
    constructionInProgress                                     6.67087e+08
    engineerMaterial                                                     0
    fixedAssetsCleanUp                                                   0
                                                            ...           
    socialSecurityNumber                                               NaN
    socialSecurityShareholding                                         NaN
    privateEquityNumber                                                  1
    privateEquityShareholding                                  8.00007e+06
    financialCompanyNumber                                             NaN
    financialCompanyShareholding                                       NaN
    pensionInsuranceAgencyNumber                                       NaN
    pensionInsuranceAgencyShareholfing                                 NaN
    totalNumberOfTopTenCirculationShareholders                 5.85248e+08
    firstLargeCirculationShareholdersNumber                    4.73639e+08
    freeCirculationStock                                       1.72424e+09
    limitedCirculationAShares                                  7.66017e+08
    generalRiskPreparation                                             NaN
    otherComprehensiveIncome                                  -2.10654e+08
    totalComprehensiveIncome                                  -5.05396e+08
    shareholdersOwnershipOfAParentCompany                      2.13041e+10
    bankInstutionNumber                                                NaN
    bankInstutionShareholding                                          NaN
    corporationNumber                                                    1
    corporationShareholding                                    4.73639e+08
    netProfitLastYear                                         -1.16913e+09
    277                                                                NaN
    278                                                                NaN
    279                                                                  3
    280                                                        4.15513e+07
    281                                                              -1.25
    282                                                             -0.103
    _id                                           5b3edccc50d2c15048795c3a
    code                                                            600100
    report_date                                        2017-03-31 00:00:00
    Name: (2017-03-31 00:00:00, 600100), Length: 285, dtype: object




```python


```
