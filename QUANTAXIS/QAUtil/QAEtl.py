try:
    import pymssql
except:
    print('no module named mssql')


def QA_util_process_financial(deal_date, type='all'):

    sql1 = '''
    with f as (
    select code,  CONVERT(varchar(100), report_date, 23) as report_date,
     totalAssets,
    intangibleAssets,
    goodwill,
    longTermDeferredExpenses,
    fixedAssets,
    interestReceivables,
    inventory,
    accountsReceivables,
    prepayments,
    totalLiquidAssets,
    interestPayable,
    totalCurrentLiabilities,
    totalLiabilities,
    operatingRevenue,
    operatingCosts,
    taxAndSurcharges,
    operatingProfit,
    netProfit,
    financialCosts,
    netProfitsBelongToParentCompanyOwner,
    netProfitAfterExtraordinaryGainsAndLosses,
    cashInflowsFromOperatingActivities,
    cashOutflowsFromOperatingActivities,
    netCashFlowsFromOperatingActivities,
    depreciationForFixedAssets,
    subsidyIncome,
    interestCoverageRatio,
    totalProfit,
    cashPaymentsForDistrbutionOfDividendsOrProfits,
    cashForThePurchaseConstructionPaymentFixedIntangibleTermAssets,
    disposalOfNetCashForRecoveryFixedIntangibleLongTermAssets
    ,Iif(interestCoverageRatio = 1,netProfit,netProfit/(interestCoverageRatio-1)) as interest
    ,currentRatio
    ,acidTestRatio
    ,cashRatio
    ,salesCosts
    ,managementCosts
    ,explorationCosts
    ,incomeTax
    ,assestsDevaluation
    ,interCompanyReceivables
     from stock_financial)
     SELECT a.code,a.report_date,substring(CAST(CONVERT(varchar(100),DATEADD(year,-1, a.report_date), 23) AS nchar),1,7) as lastyear
      ,substring(CAST(CONVERT(varchar(100), DATEADD(month,-3, a.report_date), 23) AS nchar),1,7) as lag1
      ,substring(CAST(CONVERT(varchar(100), dateadd(ms,-3,DATEADD(yy, DATEDIFF(yy,0,a.report_date), 0)) , 23) AS nchar),1,7) as yesyear,
       (a.totalAssets+b.totalAssets)/2 AS avgTotalAssets
      ,(a.fixedAssets+b.fixedAssets)/2 AS avgFixedAssets
    , (a.goodwill+b.goodwill)/2 AS avgGoodwill
    , (a.inventory+b.inventory)/2  as avgInventory
    ,(a.totalLiquidAssets+b.totalLiquidAssets)/2AS avgTotalLiquidAssets
    , (a.totalLiabilities+b.totalLiabilities)/2 AS avgTotalLiabilities
    , (a.accountsReceivables+b.accountsReceivables)/2 AS avgAccountsReceivables
    ,(a.interCompanyReceivables+b.interCompanyReceivables)/2 AS avgInterCompanyReceivables
    ,(a.prepayments+b.prepayments)/2  as avgPrepayments
    ,(a.totalCurrentLiabilities+b.totalCurrentLiabilities)/2 as avgTotalCurrentLiabilities
    
    ,e.operatingRevenue - b.operatingRevenue + a.operatingRevenue AS operatingRevenue_TTM
    ,e.operatingCosts - b.operatingCosts + a.operatingCosts AS operatingCosts_TTM
    ,e.taxAndSurcharges - b.taxAndSurcharges + a.taxAndSurcharges AS taxAndSurcharges_TTM
    ,e.salesCosts - b.salesCosts + a.salesCosts AS salesCosts_TTM
    ,e.managementCosts - b.managementCosts + a.managementCosts AS managementCosts_TTM
    ,e.explorationCosts - b.explorationCosts + a.explorationCosts AS explorationCosts_TTM
    ,e.financialCosts - b.financialCosts + a.financialCosts AS financialCosts_TTM
    ,e.assestsDevaluation - b.assestsDevaluation + a.assestsDevaluation AS assestsDevaluation_TTM
    ,e.operatingProfit - b.operatingProfit + a.operatingProfit AS operatingProfit_TTM
    ,e.totalProfit - b.totalProfit + a.totalProfit AS totalProfit_TTM
    ,e.incomeTax - b.incomeTax + a.incomeTax AS incomeTax_TTM
    ,e.netProfit - b.netProfit + a.netProfit AS netProfit_TTM
    ,e.netProfitAfterExtraordinaryGainsAndLosses - b.netProfitAfterExtraordinaryGainsAndLosses + a.netProfitAfterExtraordinaryGainsAndLosses AS netProfitAfterExtraordinaryGainsAndLosses_TTM
    ,e.interest - b.interest + a.interest AS interest_TTM
    ,e.depreciationForFixedAssets - b.depreciationForFixedAssets + a.depreciationForFixedAssets AS depreciationForFixedAssets_TTM
    ,e.netCashFlowsFromOperatingActivities - b.netCashFlowsFromOperatingActivities + a.netCashFlowsFromOperatingActivities AS netCashFlowsFromOperatingActivities_TTM
    
    ,a.totalAssets
    ,a.interest
    ,b.interest as interest_lastyear
    ,d.interest as interest_lag1
    ,e.interest  as interest_yesyear
    ,a.intangibleAssets
    ,a.salesCosts
    ,a.managementCosts
    ,a.explorationCosts
    ,a.incomeTax
    ,b.salesCosts as salesCosts_lastyear
    ,b.managementCosts as managementCosts_lastyear
    ,b.explorationCosts as explorationCosts_lastyear
    ,b.incomeTax as incomeTax_lastyear
    
    ,d.salesCosts as salesCosts_lag1
    ,d.managementCosts as managementCosts_lag1
    ,d.explorationCosts as explorationCosts_lag1
    ,d.incomeTax as incomeTax_lag1
    
    ,e.salesCosts as salesCosts_yesyear
    ,e.managementCosts as managementCosts_yesyear
    ,e.explorationCosts as explorationCosts_yesyear
    ,e.incomeTax as incomeTax_yesyear
    
    ,a.interCompanyReceivables 
    ,b.interCompanyReceivables as interCompanyReceivables_lastyear
    ,d.interCompanyReceivables as interCompanyReceivables_lag1
    ,e.interCompanyReceivables as interCompanyReceivables_yesyear
    
    ,a.goodwill,
    a.longTermDeferredExpenses,
    a.fixedAssets,
    a.interestReceivables,
    a.inventory,
    a.accountsReceivables,
    a.prepayments,
    a.totalLiquidAssets,
    a.interestPayable,
    a.totalCurrentLiabilities,
    a.totalLiabilities,
    a.operatingRevenue,
    a.operatingCosts,
    a.taxAndSurcharges,
    a.operatingProfit,
    a.netProfit,
    a.financialCosts,
    a.netProfitsBelongToParentCompanyOwner,
    a.netProfitAfterExtraordinaryGainsAndLosses,
    a.cashInflowsFromOperatingActivities,
    a.cashOutflowsFromOperatingActivities,
    a.netCashFlowsFromOperatingActivities,
    a.depreciationForFixedAssets,
    a.subsidyIncome,
    a.interestCoverageRatio,
    a.totalProfit,
    a.cashPaymentsForDistrbutionOfDividendsOrProfits,
    a.cashForThePurchaseConstructionPaymentFixedIntangibleTermAssets,
    a.disposalOfNetCashForRecoveryFixedIntangibleLongTermAssets,
    a.netProfit-a.netProfitAfterExtraordinaryGainsAndLosses as extraordinaryGainsAndLosses,
    b.totalAssets as totalAssets_lastyear,
    b.intangibleAssets as intangibleAssets_lastyear,
    b.goodwill as goodwill_lastyear,
    b.longTermDeferredExpenses as longTermDeferredExpenses_lastyear,
    b.fixedAssets as fixedAssets_lastyear,
    b.interestReceivables as interestReceivables_lastyear,
    b.inventory as inventory_lastyear,
    b.accountsReceivables as accountsReceivables_lastyear,
    b.prepayments as prepayments_lastyear,
    b.totalLiquidAssets as totalLiquidAssets_lastyear,
    b.interestPayable as interestPayable_lastyear,
    b.totalCurrentLiabilities as totalCurrentLiabilities_lastyear,
    b.totalLiabilities as totalLiabilities_lastyear,
    b.operatingRevenue as operatingRevenue_lastyear,
    b.operatingCosts as operatingCosts_lastyear,
    b.taxAndSurcharges as taxAndSurcharges_lastyear,
    b.operatingProfit as operatingProfit_lastyear,
    b.netProfit as netProfit_lastyear,
    b.financialCosts as financialCosts_lastyear,
    b.netProfitsBelongToParentCompanyOwner as netProfitsBelongToParentCompanyOwner_lastyear,
    b.netProfitAfterExtraordinaryGainsAndLosses as netProfitAfterExtraordinaryGainsAndLosses_lastyear,
    b.cashInflowsFromOperatingActivities as cashInflowsFromOperatingActivities_lastyear,
    b.cashOutflowsFromOperatingActivities as cashOutflowsFromOperatingActivities_lastyear,
    b.netCashFlowsFromOperatingActivities as netCashFlowsFromOperatingActivities_lastyear,
    b.depreciationForFixedAssets as depreciationForFixedAssets_lastyear,
    b.subsidyIncome as subsidyIncome_lastyear,
    b.interestCoverageRatio as interestCoverageRatio_lastyear,
    b.totalProfit as totalProfit_lastyear,
    b.cashPaymentsForDistrbutionOfDividendsOrProfits as cashPaymentsForDistrbutionOfDividendsOrProfits_lastyear,
    b.cashForThePurchaseConstructionPaymentFixedIntangibleTermAssets as cashForThePurchaseConstructionPaymentFixedIntangibleTermAssets_lastyear,
    b.disposalOfNetCashForRecoveryFixedIntangibleLongTermAssets as disposalOfNetCashForRecoveryFixedIntangibleLongTermAssets_lastyear,
    b.netProfit-b.netProfitAfterExtraordinaryGainsAndLosses as extraordinaryGainsAndLosses_lastyear,
    d.totalAssets as totalAssets_lag1,
    d.intangibleAssets as intangibleAssets_lag1,
    d.goodwill as goodwill_lag1,
    d.longTermDeferredExpenses as longTermDeferredExpenses_lag1,
    d.fixedAssets as fixedAssets_lag1,
    d.interestReceivables as interestReceivables_lag1,
    d.inventory as inventory_lag1,
    d.accountsReceivables as accountsReceivables_lag1,
    d.prepayments as prepayments_lag1,
    d.totalLiquidAssets as totalLiquidAssets_lag1,
    d.interestPayable as interestPayable_lag1,
    d.totalCurrentLiabilities as totalCurrentLiabilities_lag1,
    d.totalLiabilities as totalLiabilities_lag1,
    d.operatingRevenue as operatingRevenue_lag1,
    d.operatingCosts as operatingCosts_lag1,
    d.taxAndSurcharges as taxAndSurcharges_lag1,
    d.operatingProfit as operatingProfit_lag1,
    d.netProfit as netProfit_lag1,
    d.financialCosts as financialCosts_lag1,
    d.netProfitsBelongToParentCompanyOwner as netProfitsBelongToParentCompanyOwner_lag2,
    d.netProfitAfterExtraordinaryGainsAndLosses as netProfitAfterExtraordinaryGainsAndLosses_lag1,
    d.cashInflowsFromOperatingActivities as cashInflowsFromOperatingActivities_lag1,
    d.cashOutflowsFromOperatingActivities as cashOutflowsFromOperatingActivities_lag1,
    d.netCashFlowsFromOperatingActivities as netCashFlowsFromOperatingActivities_lag1,
    d.depreciationForFixedAssets as depreciationForFixedAssets_lag1,
    d.subsidyIncome as subsidyIncome_lag1,
    d.interestCoverageRatio as interestCoverageRatio_lag1,
    d.totalProfit as totalProfit_lag1,
    d.cashPaymentsForDistrbutionOfDividendsOrProfits as cashPaymentsForDistrbutionOfDividendsOrProfits_lag1,
    d.cashForThePurchaseConstructionPaymentFixedIntangibleTermAssets as cashForThePurchaseConstructionPaymentFixedIntangibleTermAssets_lag1,
    d.disposalOfNetCashForRecoveryFixedIntangibleLongTermAssets as disposalOfNetCashForRecoveryFixedIntangibleLongTermAssets_lag1,
    d.netProfit-d.netProfitAfterExtraordinaryGainsAndLosses as extraordinaryGainsAndLosses_lag1,
    e.totalAssets as totalAssets_yesyear,
    e.intangibleAssets as intangibleAssets_yesyear,
    e.goodwill as goodwill_yesyear,
    e.longTermDeferredExpenses as longTermDeferredExpenses_yesyear,
    e.fixedAssets as fixedAssets_yesyear,
    e.interestReceivables as interestReceivables_yesyear,
    e.inventory as inventory_yesyear,
    e.accountsReceivables as accountsReceivables_yesyear,
    e.prepayments as prepayments_yesyear,
    e.totalLiquidAssets as totalLiquidAssets_yesyear,
    e.interestPayable as interestPayable_yesyear,
    e.totalCurrentLiabilities as totalCurrentLiabilities_yesyear,
    e.totalLiabilities as totalLiabilities_yesyear,
    e.operatingRevenue as operatingRevenue_yesyear,
    e.operatingCosts as operatingCosts_yesyear,
    e.taxAndSurcharges as taxAndSurcharges_yesyear,
    e.operatingProfit as operatingProfit_yesyear,
    e.netProfit as netProfit_yesyear,
    e.financialCosts as financialCosts_yesyear,
    e.netProfitsBelongToParentCompanyOwner as netProfitsBelongToParentCompanyOwner_yesyear,
    e.netProfitAfterExtraordinaryGainsAndLosses as netProfitAfterExtraordinaryGainsAndLosses_yesyear,
    e.cashInflowsFromOperatingActivities as cashInflowsFromOperatingActivities_yesyear,
    e.cashOutflowsFromOperatingActivities as cashOutflowsFromOperatingActivities_yesyear,
    e.netCashFlowsFromOperatingActivities as netCashFlowsFromOperatingActivities_yesyear,
    e.depreciationForFixedAssets as depreciationForFixedAssets_yesyear,
    e.subsidyIncome as subsidyIncome_yesyear,
    e.interestCoverageRatio as interestCoverageRatio_yesyear,
    e.totalProfit as totalProfit_yesyear,
    e.cashPaymentsForDistrbutionOfDividendsOrProfits as cashPaymentsForDistrbutionOfDividendsOrProfits_yesyear,
    e.cashForThePurchaseConstructionPaymentFixedIntangibleTermAssets as cashForThePurchaseConstructionPaymentFixedIntangibleTermAssets_yesyear,
    e.disposalOfNetCashForRecoveryFixedIntangibleLongTermAssets as disposalOfNetCashForRecoveryFixedIntangibleLongTermAssets_yesyear,
    e.netProfit-e.netProfitAfterExtraordinaryGainsAndLosses as extraordinaryGainsAndLosses_yesyear
    into stock_financial_TTM  from (select * from f where CONVERT(varchar(100),DATEADD(year,-1, report_date), 23) >= '2000101') a left join 
      f b on 
       substring(CAST(CONVERT(varchar(100), b.report_date, 23) AS nchar),1,7) = substring(CAST(CONVERT(varchar(100),DATEADD(year,-1, a.report_date), 23) AS nchar),1,7) and a.code = b.code
        left join f d on 
     substring(CAST(CONVERT(varchar(100), d.report_date, 23) AS nchar),1,7) =  substring(CAST(CONVERT(varchar(100), DATEADD(month,-3, a.report_date), 23) AS nchar),1,7)  and a.code = d.code
       left join f e on 
         substring(CAST(CONVERT(varchar(100), e.report_date, 23) AS nchar),1,7) = 
     substring(CAST(CONVERT(varchar(100), dateadd(ms,-3,DATEADD(yy, DATEDIFF(yy,0,a.report_date), 0)) , 23) AS nchar),1,7)  and a.code = e.code
                    ;
                    '''

    sql2 = '''
    with t as (
                select   code
                , report_date
                ,totalAssets
                ,avgTotalAssets
                  ,fixedAssets
                  ,avgFixedAssets
                , goodwill
                , avgGoodwill
                , inventory
                , avgInventory
                ,totalLiquidAssets
                , avgTotalLiquidAssets
                ,totalLiabilities
                , avgTotalLiabilities
                ,accountsReceivables
                , avgAccountsReceivables
                ,interCompanyReceivables
                ,avgInterCompanyReceivables
                ,prepayments
                ,avgPrepayments
                ,totalCurrentLiabilities
                ,avgTotalCurrentLiabilities
                ,netCashFlowsFromOperatingActivities
                ,netProfit
                ,operatingRevenue_TTM
                ,operatingCosts_TTM
                ,taxAndSurcharges_TTM
                ,salesCosts_TTM
                ,managementCosts_TTM
                ,explorationCosts_TTM
                ,financialCosts_TTM
                ,assestsDevaluation_TTM
                ,operatingProfit_TTM
                ,totalProfit_TTM
                ,incomeTax_TTM
                ,netProfit_TTM
                ,netProfitAfterExtraordinaryGainsAndLosses_TTM
                ,interest_TTM
                ,depreciationForFixedAssets_TTM
                ,netCashFlowsFromOperatingActivities_TTM
                ---盈利能力
                ,iif(avgTotalAssets-avgGoodwill-avgtotalLiabilities <=0,0,(netProfitAfterExtraordinaryGainsAndLosses_TTM) 
                / (avgTotalAssets-avgGoodwill-avgtotalLiabilities)) as ROE
                ,iif(operatingCosts_TTM <=0 ,0, operatingRevenue_TTM / operatingCosts_TTM) as grossMargin
                
                ,iif(avgTotalAssets-avgGoodwill <=0 ,0, netProfitAfterExtraordinaryGainsAndLosses_TTM
                / (avgTotalAssets-avgGoodwill)) as ROA
                
                ---运营模式
                ,iif(avgTotalAssets-avgGoodwill <=0 ,0, avgFixedAssets/(avgTotalAssets-avgGoodwill)) AS avgFiexdOfAssets
                ,iif(avgTotalAssets <=0 ,0, avgFixedAssets/avgTotalAssets) AS fiexdOfAssets
                ,iif(avgTotalCurrentLiabilities <=0 ,0,(avgTotalLiquidAssets - avgInventory - avgPrepayments)/ avgTotalCurrentLiabilities) AS acidTestRatio
                
                ---运营效率
                ,iif(avgAccountsReceivables <=0 ,0,operatingRevenue_TTM/avgAccountsReceivables) as turnoverRatioOfReceivable
                ,iif(avgInventory <=0 ,0,operatingRevenue_TTM / avgInventory) as turnoverRatioOfInventory
                ,iif(avgTotalAssets <=0 ,0,operatingRevenue_TTM / avgTotalAssets) as turnoverRatioOfTotalAssets
                ,iif(operatingRevenue_TTM-totalProfit_TTM <=0 ,0,depreciationForFixedAssets_TTM/(operatingRevenue_TTM-totalProfit_TTM)) as depreciationOftotalCosts
                
                ---利润质量
                ,iif(netProfit <=0 ,0,(netCashFlowsFromOperatingActivities)/netProfit) AS cashOfnetProfit
                ,iif(netProfit_TTM <=0 ,0,(netCashFlowsFromOperatingActivities_TTM)/netProfit_TTM) AS cashOfnetProfit_TTM
                ,iif(interest_TTM <=0 ,0,(netCashFlowsFromOperatingActivities_TTM)/interest_TTM) as cashOfinterest
                
                ---偿债能力
                ,iif(totalAssets <=0 ,0,totalLiabilities/totalAssets) as assetsLiabilitiesRatio
                ,iif(totalCurrentLiabilities <=0 ,0,totalLiabilities/totalCurrentLiabilities) as tangibleAssetDebtRatio
                ,iif(totalCurrentLiabilities <=0 ,0,(totalLiquidAssets -inventory - accountsReceivables - prepayments)/totalCurrentLiabilities) AS cashRatio
                
                 from stock_financial_TTM),
                 rp as
                 (select h.*,
                isnull(lead(send_date,1) over(partition by code order by report_date),CONVERT(varchar(100), GETDATE(), 23)) as end_date
                from (
                select code, report_date
                , min(real_date) as send_date 
                from stock_calendar 
                group by code, report_date)h)
                SELECT a.code,industry,name,area
                ,a.report_date,substring(CAST(CONVERT(varchar(100),DATEADD(year,-1, a.report_date), 23) AS nchar),1,7) as lastyear
                  ,substring(CAST(CONVERT(varchar(100), DATEADD(month,-3, a.report_date), 23) AS nchar),1,7) as lag1
                  ,substring(CAST(CONVERT(varchar(100), dateadd(ms,-3,DATEADD(yy, DATEDIFF(yy,0,a.report_date), 0)) , 23) AS nchar),1,7) as yesyear,
                  send_date,end_date
                 ,a.totalAssets
                 ,a.avgTotalAssets
                 ,a.fixedAssets
                 ,a.avgFixedAssets
                 ,a.goodwill
                 ,a.avgGoodwill
                 ,a.inventory
                 ,a.avgInventory
                 ,a.totalLiquidAssets
                 ,a.avgTotalLiquidAssets
                 ,a.totalLiabilities
                 ,a.avgTotalLiabilities
                 ,a.accountsReceivables
                 ,a.avgAccountsReceivables
                 ,a.interCompanyReceivables
                 ,a.avgInterCompanyReceivables
                 ,a.prepayments
                 ,a.avgPrepayments
                 ,a.totalCurrentLiabilities
                 ,a.avgTotalCurrentLiabilities
                 ,a.netCashFlowsFromOperatingActivities
                ,a.netProfit
                 ---增长
                 ---收入增长
                ,a.operatingRevenue_TTM
                ,a.operatingProfit_TTM
                ,a.totalProfit_TTM
                ,a.netProfit_TTM
                ,a.netProfitAfterExtraordinaryGainsAndLosses_TTM
                ,a.netCashFlowsFromOperatingActivities_TTM
                 ---成本变化
                ,a.operatingCosts_TTM
                ,a.taxAndSurcharges_TTM
                ,a.salesCosts_TTM
                ,a.managementCosts_TTM
                ,a.explorationCosts_TTM
                ,a.financialCosts_TTM
                ,a.assestsDevaluation_TTM
                ,a.incomeTax_TTM
                ,a.interest_TTM
                ,a.depreciationForFixedAssets_TTM
                
                 ---收入增长
                ,b.operatingRevenue_TTM	as	operatingRevenue_TTMlastyear
                ,b.operatingProfit_TTM	as	operatingProfit_TTMlastyear
                ,b.totalProfit_TTM	as	totalProfit_TTMlastyear
                ,b.netProfit_TTM	as	netProfit_TTMlastyear
                ,b.netProfitAfterExtraordinaryGainsAndLosses_TTM	as	netProfitAfterExtraordinaryGainsAndLosses_TTMlastyear
                ,b.netCashFlowsFromOperatingActivities_TTM	as	netCashFlowsFromOperatingActivities_TTMlastyear
                 ---成本变化
                ,b.operatingCosts_TTM	as	operatingCosts_TTMlastyear
                ,b.taxAndSurcharges_TTM	as	taxAndSurcharges_TTMlastyear
                ,b.salesCosts_TTM	as	salesCosts_TTMlastyear
                ,b.managementCosts_TTM	as	managementCosts_TTMlastyear
                ,b.explorationCosts_TTM	as	explorationCosts_TTMlastyear
                ,b.financialCosts_TTM	as	financialCosts_TTMlastyear
                ,b.assestsDevaluation_TTM	as	assestsDevaluation_TTMlastyear
                ,b.incomeTax_TTM	as	incomeTax_TTMlastyear
                ,b.interest_TTM	as	interest_TTMlastyear
                ,b.depreciationForFixedAssets_TTM	as	depreciationForFixedAssets_TTMlastyear
                
                 ---收入增长
                ,d.operatingRevenue_TTM	as	operatingRevenue_TTMlastq
                ,d.operatingProfit_TTM	as	operatingProfit_TTMlastq
                ,d.totalProfit_TTM	as	totalProfit_TTMlastq
                ,d.netProfit_TTM	as	netProfit_TTMlastq
                ,d.netProfitAfterExtraordinaryGainsAndLosses_TTM	as	netProfitAfterExtraordinaryGainsAndLosses_TTMlastq
                ,d.netCashFlowsFromOperatingActivities_TTM	as	netCashFlowsFromOperatingActivities_TTMlastq
                 ---成本变化
                ,d.operatingCosts_TTM	as	operatingCosts_TTMlastq
                ,d.taxAndSurcharges_TTM	as	taxAndSurcharges_TTMlastq
                ,d.salesCosts_TTM	as	salesCosts_TTMlastq
                ,d.managementCosts_TTM	as	managementCosts_TTMlastq
                ,d.explorationCosts_TTM	as	explorationCosts_TTMlastq
                ,d.financialCosts_TTM	as	financialCosts_TTMlastq
                ,d.assestsDevaluation_TTM	as	assestsDevaluation_TTMlastq
                ,d.incomeTax_TTM	as	incomeTax_TTMlastq
                ,d.interest_TTM	as	interest_TTMlastq
                ,d.depreciationForFixedAssets_TTM	as	depreciationForFixedAssets_TTMlastq
                
                  ---盈利能力		
                ,a.ROE		
                ,a.grossMargin		
                ,a.ROA		
                        
                ,a.avgFiexdOfAssets		
                ,a.fiexdOfAssets		
                ,a.acidTestRatio		
                        
                ,a.turnoverRatioOfReceivable		
                ,a.turnoverRatioOfInventory		
                ,a.turnoverRatioOfTotalAssets		
                ,a.depreciationOftotalCosts		
                    
                ,a.cashOfnetProfit		
                ,a.cashOfnetProfit_TTM		
                ,a.cashOfinterest		
                    
                ,a.assetsLiabilitiesRatio		
                ,a.tangibleAssetDebtRatio		
                ,a.cashRatio			
                    
                ,b.ROE	as	ROE_lastyear
                ,b.grossMargin	as	grossMargin_lastyear
                ,b.ROA	as	ROA_lastyear
                
                ,b.avgFiexdOfAssets	as	avgFiexdOfAssets_lastyear
                ,b.fiexdOfAssets	as	fiexdOfAssets_lastyear
                ,b.acidTestRatio	as	acidTestRatio_lastyear
                
                ,b.turnoverRatioOfReceivable	as	turnoverRatioOfReceivable_lastyear
                ,b.turnoverRatioOfInventory	as	turnoverRatioOfInventory_lastyear
                ,b.turnoverRatioOfTotalAssets	as	turnoverRatioOfTotalAssets_lastyear
                ,b.depreciationOftotalCosts	as	depreciationOftotalCosts_lastyear
                
                ,b.cashOfnetProfit	as	cashOfnetProfit_lastyear
                ,b.cashOfnetProfit_TTM	as	cashOfnetProfit_TTM_lastyear
                ,b.cashOfinterest	as	cashOfinterest_lastyear
                
                ,b.assetsLiabilitiesRatio	as	assetsLiabilitiesRatio_lastyear
                ,b.tangibleAssetDebtRatio	as	tangibleAssetDebtRatio_lastyear
                ,b.cashRatio	as	cashRatio_lastyear
                
                ,d.ROE		as	ROE_lastq
                ,d.grossMargin		as	grossMargin_q
                ,d.ROA	as	ROA_lastq
                
                ,d.avgFiexdOfAssets	as	avgFiexdOfAssets_lastq
                ,d.fiexdOfAssets	as	fiexdOfAssets_lastq
                ,d.acidTestRatio	as	acidTestRatio_lastq
                
                ,d.turnoverRatioOfReceivable	as	turnoverRatioOfReceivable_lastq
                ,d.turnoverRatioOfInventory	as	turnoverRatioOfInventory_lastq
                ,d.turnoverRatioOfTotalAssets	as	turnoverRatioOfTotalAssets_lastq
                ,d.depreciationOftotalCosts	as	depreciationOftotalCosts_lastq
                
                ,d.cashOfnetProfit	as	cashOfnetProfit_lastq
                ,d.cashOfnetProfit_TTM	as	cashOfnetProfit_TTM_lastq
                ,d.cashOfinterest	as	cashOfinterest_lastq
                
                ,d.assetsLiabilitiesRatio	as	assetsLiabilitiesRatio_lastq
                ,d.tangibleAssetDebtRatio	as	tangibleAssetDebtRatio_lastq
                ,d.cashRatio	as	cashRatio_lastq
                 into stock_financial_analysis
                  FROM t a left join 
                  t b on 
                   substring(CAST(CONVERT(varchar(100), b.report_date, 23) AS nchar),1,7) = substring(CAST(CONVERT(varchar(100),DATEADD(year,-1, a.report_date), 23) AS nchar),1,7) and a.code = b.code
                    left join t d on 
                 substring(CAST(CONVERT(varchar(100), d.report_date, 23) AS nchar),1,7) =  substring(CAST(CONVERT(varchar(100), DATEADD(month,-3, a.report_date), 23) AS nchar),1,7)  and a.code = d.code
                 left join rp c on 
                  c.report_date = a.report_date and a.code = c.code
                  left join stock_info f
                  on a.code = f.code;
                    '''
    sql3 = """
            select CONVERT(varchar(100), a.date, 23) as date, a.[open] as opens, a.high as high, a.low as low, a.[close] as closes,a.volume * 100 as volume,a.code,
            b.shares_after * 10000 as shares,
            round(a.[close]*b.shares_after * 10000,2) AS total_market
            ,industry,name,area
            ,report_date,lastyear
             ,lag1
             ,send_date,c.end_date
             ,totalAssets
             ,avgTotalAssets
             ,fixedAssets
             ,avgFixedAssets
             ,goodwill
             ,avgGoodwill
             ,inventory
             ,avgInventory
             ,totalLiquidAssets
             ,avgTotalLiquidAssets
             ,totalLiabilities
             ,avgTotalLiabilities
             ,accountsReceivables
             ,avgAccountsReceivables
             ,interCompanyReceivables
             ,avgInterCompanyReceivables
             ,prepayments
             ,avgPrepayments
             ,totalCurrentLiabilities
             ,avgTotalCurrentLiabilities
             ,netCashFlowsFromOperatingActivities
            ,netProfit
             ---增长
             ---收入增长
            ,operatingRevenue_TTM
            ,operatingProfit_TTM
            ,totalProfit_TTM
            ,netProfit_TTM
            ,netProfitAfterExtraordinaryGainsAndLosses_TTM
            ,netCashFlowsFromOperatingActivities_TTM
             ---成本变化
            ,operatingCosts_TTM
            ,taxAndSurcharges_TTM
            ,salesCosts_TTM
            ,managementCosts_TTM
            ,explorationCosts_TTM
            ,financialCosts_TTM
            ,assestsDevaluation_TTM
            ,incomeTax_TTM
            ,interest_TTM
            ,depreciationForFixedAssets_TTM
            
            
            ,operatingRevenue_TTMlastyear
            ,operatingProfit_TTMlastyear
            ,totalProfit_TTMlastyear
            ,netProfit_TTMlastyear
            ,netProfitAfterExtraordinaryGainsAndLosses_TTMlastyear
            ,netCashFlowsFromOperatingActivities_TTMlastyear
            
            ,operatingCosts_TTMlastyear
            ,taxAndSurcharges_TTMlastyear
            ,salesCosts_TTMlastyear
            ,managementCosts_TTMlastyear
            ,explorationCosts_TTMlastyear
            ,financialCosts_TTMlastyear
            ,assestsDevaluation_TTMlastyear
            ,incomeTax_TTMlastyear
            ,interest_TTMlastyear
            ,depreciationForFixedAssets_TTMlastyear
            
            
            ,operatingRevenue_TTMlastq
            ,operatingProfit_TTMlastq
            ,totalProfit_TTMlastq
            ,netProfit_TTMlastq
            ,netProfitAfterExtraordinaryGainsAndLosses_TTMlastq
            ,netCashFlowsFromOperatingActivities_TTMlastq
            
            ,operatingCosts_TTMlastq
            ,taxAndSurcharges_TTMlastq
            ,salesCosts_TTMlastq
            ,managementCosts_TTMlastq
            ,explorationCosts_TTMlastq
            ,financialCosts_TTMlastq
            ,assestsDevaluation_TTMlastq
            ,incomeTax_TTMlastq
            ,interest_TTMlastq
            ,depreciationForFixedAssets_TTMlastq
            
              ---盈利能力
            ,ROE
            ,grossMargin
            ,ROA
            
            ,avgFiexdOfAssets
            ,fiexdOfAssets
            ,acidTestRatio
            
            ,turnoverRatioOfReceivable
            ,turnoverRatioOfInventory
            ,turnoverRatioOfTotalAssets
            ,depreciationOftotalCosts
             
            ,cashOfnetProfit
            ,cashOfnetProfit_TTM
            ,cashOfinterest
            
            ,assetsLiabilitiesRatio
            ,tangibleAssetDebtRatio
            ,cashRatio
            
            ,ROE_lastyear
            ,grossMargin_lastyear
            ,ROA_lastyear
            
            ,avgFiexdOfAssets_lastyear
            ,fiexdOfAssets_lastyear
            ,acidTestRatio_lastyear
            
            ,turnoverRatioOfReceivable_lastyear
            ,turnoverRatioOfInventory_lastyear
            ,turnoverRatioOfTotalAssets_lastyear
            ,depreciationOftotalCosts_lastyear
            
            ,cashOfnetProfit_lastyear
            ,cashOfnetProfit_TTM_lastyear
            ,cashOfinterest_lastyear
            
            ,assetsLiabilitiesRatio_lastyear
            ,tangibleAssetDebtRatio_lastyear
            ,cashRatio_lastyear
            
            ,ROE_lastq
            ,grossMargin_q
            ,ROA_lastq
            
            ,avgFiexdOfAssets_lastq
            ,fiexdOfAssets_lastq
            ,acidTestRatio_lastq
            
            ,turnoverRatioOfReceivable_lastq
            ,turnoverRatioOfInventory_lastq
            ,turnoverRatioOfTotalAssets_lastq
            ,depreciationOftotalCosts_lastq
            
            ,cashOfnetProfit_lastq
            ,cashOfnetProfit_TTM_lastq
            ,cashOfinterest_lastq
            
            ,assetsLiabilitiesRatio_lastq
            ,tangibleAssetDebtRatio_lastq
            ,cashRatio_lastq
             into stock_analysis_data
            from stock_market_day a 
            left join (
            select code, date,iif(shares_before =0, lead(shares_before) over(partition by code order by date),shares_before) as shares_before,
            shares_after,
            isnull(lead(date) over(partition by code order by date),CONVERT(varchar(100), GETDATE(), 23)) as end_date from (
            select code, date, max(shares_after) as shares_after, max(shares_before) as shares_before
             FROM ( 
            select h.* from(
            select code,CONVERT(varchar(100), date, 23) as date,shares_after,shares_before, count(*) as abb
            from stock_xdxr 
            where (shares_after > 0 or shares_before > 0) and shares_after != shares_before 
            GROUP BY code,date,shares_after,shares_before
            union 
            SELECT code, cast(cast(timeToMarket as nvarchar) as date ), 0 as shares_after, 0 as share_before, 1 as abb FROM stock_info WHERE timeToMarket != 0
            )h)g group by code, date)m )b on a.code = b.code and a.date > b.date and a.date <= b.end_date
            left join stock_financial_analysis c
            on a.code = c.code 
            and c.send_date < CONVERT(varchar(100), a.date, 23) 
            and c.end_date >= CONVERT(varchar(100), a.date, 23);
        """

    conn = pymssql.connect(user="sa", password="123456",
                           host="localhost", database="quantaxis", charset="utf8")
    cursor = conn.cursor()
    if type == 'all' or type == 'financial':
        cursor.execute('''drop table stock_financial_TTM;''')
        cursor.execute(sql1)
        cursor.execute('''drop table stock_financial_analysis;''')
        cursor.execute(sql2)
        print("financial TTM report has been stored")
    else:
        pass
    if type == 'all' or type == 'analysis':
        cursor.execute('''drop table stock_analysis_data;''')
        cursor.execute(sql3)
        print('analysis data has been stored')
    else:
        pass
    cursor.close()
    conn.commit()
    conn.close()


def to_mongo_data():
    pass
