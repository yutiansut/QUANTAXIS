
# coding:utf-8

# 本部分参考 https://github.com/foolcage/fooltrader/blob/master/docs/contract.md
# 目的将pytdx的财务数据列名转化成英文

class BalanceSheet():

    # 货币资金
    moneyFunds = float()
    # 交易性金融资产
    heldForTradingFinancialAssets = float()
    # 衍生金融资产
    derivative = float()
    # 应收票据
    billsReceivable = float()
    # 应收账款
    accountsReceivable = float()
    # 预付款项
    prepaidAccounts = float()
    # 应收利息
    interestReceivable = float()
    # 应收股利
    dividendReceivable = float()
    # 其他应收款
    otherReceivables = float()

    # 买入返售金融资产
    buyingBackTheSaleOfFinancialAssets = float()
    # 存货
    inventory = float()
    # 划分为持有待售的资产
    assetsForSale = float()
    # 一年内到期的非流动资产
    nonCurrentAssetsDueWithinOneYear = float()

    # 待摊费用
    unamortizedExpenditures = float()
    # 待处理流动资产损益
    waitDealIntangibleAssetsLossOrIncome = float()

    # 其他流动资产
    otherCurrentAssets = float()
    # 流动资产合计
    totalCurrentAssets = float()

    # 非流动资产

    # 发放贷款及垫款
    loansAndPaymentsOnBehalf = float()

    # 可供出售金融资产
    availableForSaleFinancialAssets = float()
    # 持有至到期投资
    heldToMaturityInvestment = float()
    # 长期应收款
    longTermReceivables = float()
    # 长期股权投资
    longTermEquityInvestment = float()
    # 投资性房地产
    investmentRealEstate = float()
    # 固定资产净额
    NetfixedAssets = float()
    # 在建工程
    constructionInProcess = float()
    # 工程物资
    engineerMaterial = float()
    # 固定资产清理
    fixedAssetsInLiquidation = float()
    # 生产性生物资产
    productiveBiologicalAssets = float()
    # 公益性生物资产
    nonProfitLivingAssets = float()
    # 油气资产
    oilAndGasAssets = float()
    # 无形资产
    intangibleAssets = float()
    # 开发支出
    developmentExpenditure = float()
    # 商誉
    goodwill = float()
    # 长期待摊费用
    longTermDeferredExpenses = float()
    # 递延所得税资产
    deferredIncomeTaxAssets = float()
    # 其他非流动资产
    OtherNonCurrentAssets = float()
    # 非流动资产合计
    nonCurrentAssets = float()
    # 资产总计
    totalAssets = float()

    # / *流动负债 * /
    # 短期借款
    shortTermBorrowing = float()
    # 交易性金融负债
    transactionFinancialLiabilities = float()
    # 应付票据
    billsPayable = float()
    # 应付账款
    accountsPayable = float()
    # 预收款项
    accountsReceivedInAdvance = float()
    # 应付手续费及佣金
    handlingChargesAndCommissionsPayable = float()
    # 应付职工薪酬
    employeeBenefitsPayable = float()
    # 应交税费
    taxesAndSurchargesPayable = float()
    # 应付利息
    interestPayable = float()
    # 应付股利
    dividendpayable = float()
    # 其他应付款
    otherPayables = float()
    # 预提费用
    withholdingExpenses = float()
    # 一年内的递延收益
    deferredIncomeWithinOneYear = float()
    # 应付短期债券
    shortTermDebenturesPayable = float()
    # 一年内到期的非流动负债
    nonCurrentLiabilitiesMaturingWithinOneYear = float()
    # 其他流动负债
    otherCurrentLiability = float()
    # 流动负债合计
    totalCurrentLiabilities = float()

    # / *非流动负债 * /
    # 长期借款
    LongTermBorrowing = float()
    # 应付债券
    bondPayable = float()
    # 长期应付款
    longTermPayables = float()
    # 长期应付职工薪酬
    longTermEmployeeBenefitsPayable = float()
    # 专项应付款
    specialPayable = float()
    # 预计非流动负债
    expectedNonCurrentLiabilities = float()
    # 递延所得税负债
    deferredIncomeTaxLiabilities = float()
    # 长期递延收益
    longTermDeferredRevenue = float()
    # 其他非流动负债
    otherNonCurrentLiabilities = float()
    # 非流动负债合计
    totalNonCurrentLiabilities = float()
    # 负债合计
    totalLiabilities = float()

    # / *所有者权益 * /
    # 实收资本(或股本)
    totalShareCapital = float()

    # 资本公积
    capitalSurplus = float()
    # 减：库存股
    treasuryStock = float()
    # 其他综合收益
    otherComprehensiveIncome = float()
    # 专项储备
    theSpecialReserve = float()

    # 盈余公积
    surplusReserves = float()
    # 一般风险准备
    generalRiskPreparation = float()
    # 未分配利润
    undistributedProfits = float()
    # 归属于母公司股东权益合计(净资产)
    bookValue = float()

    # 少数股东权益
    minorityBookValue = float()

    # 所有者权益(或股东权益)合计
    totalBookValue = float()

    # 负债和所有者权益(或股东权益)总计
    totalLiabilitiesAndOwnersEquity = float()



class IncomeStatement():

    # /*营业总收入*/
    # 营业收入
    operatingRevenue = float()
    # /*营业总成本*/
    operatingTotalCosts = float()
    # 营业成本
    operatingCosts = float()
    # 营业税金及附加
    businessTaxesAndSurcharges = float()
    # 销售费用
    sellingExpenses = float()
    # 管理费用
    ManagingCosts = float()
    # 财务费用
    financingExpenses = float()
    # 资产减值损失
    assetsDevaluation = float()
    # 公允价值变动收益
    incomeFromChangesInFairValue = float()
    # 投资收益
    investmentIncome = float()
    # 其中:对联营企业和合营企业的投资收益
    investmentIncomeFromRelatedEnterpriseAndJointlyOperating = float()
    # 汇兑收益
    exchangeGains = float()
    # /*营业利润*/
    operatingProfit = float()
    # 加:营业外收入
    nonOperatingIncome = float()
    # 减：营业外支出
    nonOperatingExpenditure = float()
    # 其中：非流动资产处置损失
    disposalLossOnNonCurrentLiability = float()
    # /*利润总额*/
    totalProfits = float()
    # 减：所得税费用
    incomeTaxExpense = float()
    # /*净利润*/
    netProfit = float()
    # 归属于母公司所有者的净利润
    netProfitAttributedToParentCompanyOwner = float()
    # 少数股东损益
    minorityInterestIncome = float()
    # /*每股收益*/
    # 基本每股收益(元/股)
    EPS = float()
    # 稀释每股收益(元/股)
    dilutedEPS = float()
    # /*其他综合收益*/
    otherComprehensiveIncome = float()
    # /*综合收益总额*/
    accumulatedOtherComprehensiveIncome = float()
    # 归属于母公司所有者的综合收益总额
    attributableToOwnersOfParentCompany = float()
    # 归属于少数股东的综合收益总额
    attributableToMinorityShareholders = float()


class CashFlowStatement():


    # /*一、经营活动产生的现金流量*/
    # 销售商品、提供劳务收到的现金
    cashFromSellingCommoditiesOrOfferingLabor = float()
    # 收到的税费返还
    refundOfTaxAndFeeReceived = float()
    # 收到的其他与经营活动有关的现金
    cashReceivedRelatingToOtherOperatingActivities = float()
    # 经营活动现金流入小计
    subTotalOfCashInflowsFromOperatingActivities = float()
    # 购买商品、接受劳务支付的现金
    cashPaidForGoodsAndServices = float()
    # 支付给职工以及为职工支付的现金
    cashPaidToAndOnBehalfOfemployees = float()
    # 支付的各项税费
    paymentsOfTaxesAndSurcharges = float()
    # 支付的其他与经营活动有关的现金
    cashPaidRelatingToOtherOperatingActivities = float()
    # 经营活动现金流出小计
    subTotalOfCashOutflowsFromOperatingActivities = float()
    # 经营活动产生的现金流量净额
    netCashFlowsFromOperatingActivities = float()
    # /*二、投资活动产生的现金流量*/
    # 收回投资所收到的现金
    cashReceivedFromDisposalOfInvestments = float()
    # 取得投资收益所收到的现金
    cashReceivedFromReturnsOnIvestments = float()
    # 处置固定资产、无形资产和其他长期资产所收回的现金净额
    netCashReceivedFromDisposalAssets = float()
    # 处置子公司及其他营业单位收到的现金净额
    netCashReceivedFromDisposalSubsidiaries = float()
    # 收到的其他与投资活动有关的现金
    cashReceivedFromOtherInvesting = float()
    # 投资活动现金流入小计
    subTotalOfCashInflowsFromInvesting = float()
    # 购建固定资产、无形资产和其他长期资产所支付的现金
    cashPaidToAcquireFixedAssets = float()
    # 投资所支付的现金
    cashPaidToAcquireInvestments = float()
    # 取得子公司及其他营业单位支付的现金净额
    netCashPaidToAcquireSubsidiaries = float()
    # 支付的其他与投资活动有关的现金
    cashPaidRelatingToOtherInvesting = float()
    # 投资活动现金流出小计
    subTotalOfCashOutflowsFromInvesting = float()
    # 投资活动产生的现金流量净额
    netCashFlowsFromInvesting = float()
    # /*三、筹资活动产生的现金流量*/
    # 吸收投资收到的现金
    cashReceivedFromCapitalContributions = float()
    # 其中：子公司吸收少数股东投资收到的现金
    cashReceivedFromMinorityShareholdersOfSubsidiaries = float()
    # 取得借款收到的现金
    cashReceivedFromBorrowings = float()
    # 发行债券收到的现金
    cashReceivedFromIssuingBonds = float()
    # 收到其他与筹资活动有关的现金
    cashReceivedRelatingToOtherFinancingActivities = float()
    # 筹资活动现金流入小计
    subTotalOfCashInflowsFromFinancingActivities = float()
    # 偿还债务支付的现金
    cashRepaymentsOfBorrowings = float()
    # 分配股利、利润或偿付利息所支付的现金
    cashPaymentsForInterestExpensesAndDistributionOfDividendsOrProfits = float()
    # 其中：子公司支付给少数股东的股利、利润
    cashPaymentsForDividendsOrProfitToMinorityShareholders = float()
    # 支付其他与筹资活动有关的现金
    cashPaymentsRelatingToOtherFinancingActivities = float()
    # 筹资活动现金流出小计
    subTotalOfCashOutflowsFromFinancingActivities = float()
    # 筹资活动产生的现金流量净额
    netCashFlowsFromFinancingActivities = float()
    # /*四、汇率变动对现金及现金等价物的影响*/
    effectOfForeignExchangeRate = float()
    # /*五、现金及现金等价物净增加额*/
    netIncreaseInCash = float()
    # 加:期初现金及现金等价物余额
    cashAtBeginningOfyear = float()
    # /*六、期末现金及现金等价物余额*/
    cashAtEndOfyear = float()
    # /*附注*/
    # 净利润
    netProfit = float()
    # 少数股东权益
    minorityBookValue = float()
    # 未确认的投资损失
    unrealisedInvestmentLosses = float()
    # 资产减值准备
    allowanceForAssetDevaluation = float()
    # 固定资产折旧、油气资产折耗、生产性物资折旧
    depreciationOfFixedAssets = float()
    # 无形资产摊销
    amorizationOfIntangibleAssets = float()
    # 长期待摊费用摊销
    longTermDeferredExpenses = float()
    # 待摊费用的减少
    decreaseOfDeferredExpenses = float()
    # 预提费用的增加
    IncreaseOfwithholdingExpenses = float()
    # 处置固定资产、无形资产和其他长期资产的损失
    lossOnDisposalOfFixedAssets = float()
    # 固定资产报废损失
    lossOnFixedAssetsDamaged = float()
    # 公允价值变动损失
    lossOnFairValueChange = float()
    # 递延收益增加（减：减少）
    changeOnDeferredRevenue = float()
    # 预计负债
    estimatedLiabilities = float()
    # 财务费用
    financingExpenses = float()
    # 投资损失
    investmentLoss = float()
    # 递延所得税资产减少
    decreaseOnDeferredIncomeTaxAssets = float()
    # 递延所得税负债增加
    increaseOnDeferredIncomeTaxLiabilities = float()
    # 存货的减少
    decreaseInInventories = float()
    # 经营性应收项目的减少
    decreaseInReceivablesUnderOperatingActivities = float()
    # 经营性应付项目的增加
    increaseInReceivablesUnderOperatingActivities = float()
    # 已完工尚未结算款的减少(减:增加)
    decreaseOnAmountDue = float()
    # 已结算尚未完工款的增加(减:减少)
    increaseOnSettlementNotYetCompleted = float()
    # 其他
    other = float()
    # 经营活动产生现金流量净额
    netCashFlowFromOperatingActivities = float()
    # 债务转为资本
    debtsTransferToCapital = float()
    # 一年内到期的可转换公司债券
    oneYearDueConvertibleBonds = float()
    # 融资租入固定资产
    financingRentToFixedAsset = float()
    # 现金的期末余额
    cashAtTheEndOfPeriod = float()
    # 现金的期初余额
    cashAtTheBeginningOfPeriod = float()
    # 现金等价物的期末余额
    cashEquivalentsAtTheEndOfPeriod = float()
    # 现金等价物的期初余额
    cashEquivalentsAtTheBeginningOfPeriod = float()
    # 现金及现金等价物的净增加额
    netIncreaseInCashAndCashEquivalents = float()

