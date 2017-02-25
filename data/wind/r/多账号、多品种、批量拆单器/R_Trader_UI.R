##Wind 专业下单器
#功能简介：对篮子里的股票、期货证券等分账号、随机拆分下单。下单的价格、账号顺序、账号多少等可以手工设置。
#          还可以清仓、查看仓位、撤单等功能。
#
#作者：zhu honghai，hhzhu@wind.com.cn
#时间：20131016
#欢迎大家提出各种建议

library(WindR) #装载WindR接口
library(stats) #主要用来参数随机数
require(tcltk) #用来绘制界面

#为了使得界面再次进入的时候数据不产生巨变，这里故意不清除数据
# gData.AccountData<<-NULL;
# gData.BasketData<<-NULL;
# gData.PositionData<<-NULL;
# gData.LogonIDs<<-NULL;
# gData.LogonAccount<<-NULL;
# gData.OrderRequests<<-NULL;
# gData.OrderResult<<-NULL;

w.start(0,F);#启动Wind接口，其中F表示不显示导航界面。

#用户应手工准备好登录账号和篮子，如下：
#w.tlogon('0000',0,c('w081263801','000100000080','000100000081','000100000180','000100000181','w081263802'),0,c('sh','sh','sh','cfe','cfe','cfe'));
#Code<-c('600000.sh','000001.sz','600177.sh','IF1312.CFE','TF1312.CFE');
#TradeSide<-c('buy','buy','sell','short','sell');
#Weight<-c(100,100,100,1,1);
#Basket<-data.frame(Code=Code,TradeSide=TradeSide,Weight=Weight,stringsAsFactors = FALSE)
tkmessageBox(message = '请使用w.tlogon登录所有账户，并准备篮子如：Basket<-data.frame(Code=c("600177.sh","600000.sh"),TradeSide="buy",Weight=1)');


###############################################################################
#以下是具体操作工具函数

PressedImportAccount <- function()   #用户按了“导入账号”后调用的函数
{
  retsetTotalVolume();               #先把下单总量清0
  
  #清除登录表格
  tkconfigure(table.logonIDs ,state='normal');
  tkconfigure(table.logonIDs ,rows=1);
  gData.AccountData<<-NULL;
  gData.PositionData<<-NULL;        #清仓位
  #remove('gData.PositionData',envir=.GlobalEnv)
  
  if(doImportAccount()==0 || is.null(gData.AccountData)) #导入账号
  {
    tkconfigure(table.logonIDs ,state='disabled');
    print('没有能导入数据');
    showposition();
    return();
  }
  showposition();  #显示仓位
  
  #显示账号表格
  tkconfigure(table.logonIDs ,rows=length(gData.AccountData[,1])+1);
  for(i in 1:length(gData.AccountData[,1])){
    tkset(table.logonIDs ,paste(i,0,sep=','),i);
    for(j in 1:5){#length(gData.AccountData[1,])){
      tkset(table.logonIDs ,paste(i,j,sep=','),gData.AccountData[i,j]);
    }
  }
  tkconfigure(table.logonIDs ,state='disabled');
  
  #重新绘制篮子表格
  RefillBasketTable();
  
  
}

PressedImportBasket <- function()  #用户按了“导入篮子”后调用的函数
{
  retsetTotalVolume();         #先把下单总量清0
  
  #清除篮子表格内容
  gData.BasketData<<-NULL;     
  RefillBasketTable();
  
  #获取数据
  if(length(ls(.GlobalEnv,pattern='^Basket$'))>0 ) #从Basket篮子里导入数据
    doImportBasket(Basket);  
  
  #再次绘制篮子表格
  RefillBasketTable();
}

PressedExecOrder <- function()#用户按了“执行下单”后调用的函数   
{
  gData.OrderResult<<-NULL;
  gData.OrderRequests<<-NULL;
  
  #先检查初始状态！
  if(  length(ls(.GlobalEnv,pattern='^gData[.]AccountData$'))<=0
       ||length(ls(.GlobalEnv,pattern='^gData[.]BasketData$'))<=0
       ||length(ls(.GlobalEnv,pattern='^gData[.]PositionData$'))<=0
       ||length(gData.AccountData[,1])<=0
       ||length(gData.BasketData[,1])<=0
  )
  {
    msg<-'账号、篮子或仓位初始状态不对！';
    print(msg);
    tkmessageBox(message=msg);
    return(0);
  }
  
  #先获得并检测所有变量
  laccountorder<-as.integer(tclvalue(rbacc.value));     #账号下单次序
  
  lpricestrategy<-as.integer(tclvalue(rbbas.value));    #价格策略按钮
  lpriceaddcount<-as.integer(tclvalue(basketadd.value ));#价格加价量
  
  lvolumestrategy<-as.integer(tclvalue(rbvolume.value));#数量策略选项
  lvolumemin<-as.integer(tclvalue(rbvolumemin.value));  #随机分配最小量
  lvolumemax<-as.integer(tclvalue(rbvolumemax.value));  #随机分配最大量
  
  ltotalamountstrategy<-as.integer(tclvalue(rborderamount.value)); #下单总量控制选项
  lordercapital<-as.double(tclvalue(rbordercap.value)); #下单总金额
  lordermultipy<-as.double(tclvalue(rbordermul.value)); #委托数量倍数
  if(  (ltotalamountstrategy==1 && lordermultipy<=0)     
       ||(ltotalamountstrategy==0 && lordercapital<=100) #下单总量不能为0
  )
  {
    tkmessageBox(message = ifelse(ltotalamountstrategy==0,'委托资金必须大于100',"委托倍数必须大于0!"))
    return(0);			
  }
  
  lsplitorder<-as.integer(tclvalue(cksplitorder.value));       #拆单可选按钮
  lsplitordermin<-as.integer(tclvalue(cksplitordermin.value)); #最小手数
  lsplitordermax<-as.integer(tclvalue(cksplitordermax.value)); #最大手数
  if(lsplitordermin<=0) 
    lsplitordermin=1;
  
  if(lsplitordermax<lsplitordermin)
    lsplitordermax=lsplitordermin;
  
  
  if(updateRealTimePrice()==0)  #更新篮子里股票价格信息                          
  {
    print('价格更新失败，不能交易!');
    tkmessageBox(message = "价格更新失败，不能交易!")
    return(0);		    	
  }
  
  #1）每个账户有个统计计数AccountSelect，用来统计分配的品种数量，这主要用于“一个品种一个账号”选项
  #2) "一个品种一个账号”策略是从一对合格的账号中选择AccountSelect最小的那个
  #3) “每账户数量相同”,"按总资产比例分配“，”按可用资产比例分配“，“随机分配”都相似，在允许的账户中分配
  #4) 若拆单选项选好后，则在每个账户的分配额下，拆成小额
  #5）“账户下单次序”选项在最后单子已经准备好发出前才有效。每次从账号中获得一个单子，因为Wind支持向量下单，
  #   所以可以把所有单子全部一次下完
  #
  #具体来说如下操作：
  #1）初始化AccountSelect等
  #1b)计算出每个品种交易数量
  #2）对篮子里每一品种，做3-6
  #3）得到所有可下单的账户
  #4）按照数量策略分配量：考虑资金是否足够、每手股数等，最后扣除该资金
  #5）调整AccountSelect
  #6）对每个账户的总量进行拆单
  #7）按照”账号下单次序“依次从每个账户的单子中选择一个组织成最终的单子。
  
  initAccountOrder();#初始化AccountSelect等
  totalvolumes<-getTotalVolumes(ltotalamountstrategy,lordercapital,lordermultipy);#1b)计算出每个品种交易数量
  print('准备下单总量为:');
  print(data.frame(Code=gData.BasketData$Code,TradeSide=gData.BasketData$TradeSide,Volume=totalvolumes));
  
  totalvolumes[is.na(totalvolumes)]<-0;
  
  if(sum(totalvolumes)<=0)
  {
    msg<-'不能下单，因为下单量都为0！';
    print(msg);
    tkmessageBox(message = msg)
    return();
  }
  
  for(i in 1:length(gData.BasketData[,1]))#2）对篮子里每一品种，做3-6
  {
    if(totalvolumes[i]<=0.0001)
    {
      next; 
    }
    
    validaccounts<-getValidAccounts(i);#3）得到所有可下单的账户
    if(is.null(validaccounts)){
      msg<-paste('对于',gData.BasketData$Code[[i]],'(',gData.BasketData$TradeSide[[i]],'),没有效的账户可以用来下单!',sep='');
      print(msg);
      tkmessageBox(message = msg)
      return(0);
    }
    
    #4）按照数量策略分配量：考虑资金是否足够、每手股数等，最后扣除该资金
    eachvolumes<-dispatchAmongAccounts(i,validaccounts,totalvolumes[i],ltotalamountstrategy,lvolumestrategy,lvolumemin,lvolumemax);
    if(is.null(eachvolumes))
    {
      msg<-paste('对于',gData.BasketData$Code[[i]],'(',gData.BasketData$TradeSide[[i]],' ',totalvolumes[i],'),不能分配给账号下单!',sep='');
      print(msg);
      tkmessageBox(message = msg)
      return(0);    		
    }
    
    #5）调整AccountSelect 已经在dispatchAmongAccounts处理了
    if(length(eachvolumes[,1])<=0)
    {
      print(paste('不能对',gData.BasketData$Code[[i]],'（总量为',totalvolumes[i],')下单！',sep=''));
      next;
    }

    #6）对每个账户的总量进行拆单
    outvolumes<-splitOrderInAccount(i,eachvolumes$volume,lsplitorder,lsplitordermin,lsplitordermax);
    for(eachv in 1:length(eachvolumes[,1]))
    {#把单子放到全局变量gData.tAccountToOrders中。
      taccountindex<-eachvolumes$accountindex[eachv]
      if(is.null(gData.tAccountToOrders[[taccountindex]]))
      {
        gData.tAccountToOrders[[taccountindex]]<<-list( basketindex=list(i),volumes=list(outvolumes[[eachv]]));
      }
      else{
        gData.tAccountToOrders[[taccountindex]]$basketindex<<-append(gData.tAccountToOrders[[taccountindex]]$basketindex, i);
        gData.tAccountToOrders[[taccountindex]]$volumes<<-append(gData.tAccountToOrders[[taccountindex]]$volumes, list(outvolumes[[eachv]]));
      }
    }
    
  }
  
  
  #7）按照”账号下单次序“依次从每个账户的单子中选择一个组织成最终的单子。
  orders<-generateOrders(laccountorder,lpricestrategy,lpriceaddcount)
  
  if(is.null(orders) || length(orders$codes)<=0)
  {
    print('不能下单，因为没有产生有效的下单数据！');
    return();
  }
  print(orders);
  
  #return;
  
  #8)下单
  showFields<-'RequestID,SecurityCode,TradeSide,OrderPrice,OrderVolume,LogonID,ErrorCode,ErrorMsg';
  lout<-w.torder(orders$code,orders$tradeside,orders$price,orders$volume,logonid=orders$logonid,showfields=showFields);
  
  retsetTotalVolume(); #把下单总量清0
  
  gData.OrderRequests<<-lout$Data
  gData.OrderRequests$LogonID<<-orders$logonid;
  if(lout$ErrorCode!=0)
  {
    print(lout);
    tkmessageBox(message = '下单过程中出现错误!');
    return(0);
  }
  
  print('下单结果在gData.OrderRequests变量中');
  showExeResult();#显示执行结果
}

PressedQueryOrder <- function()#用户按了“查询下单结果”按钮后调用的函数
{
  getOrderResult();  #获取下单结果
  showOrderResult(); #显示下单结果
}

PressedQueryPosition <- function() #用户按了“查询持仓”后调用的函数
{
  gData.PositionData <<- NULL; 
  if(  length(ls(.GlobalEnv,pattern='^gData[.]LogonIDs$'))<=0 || is.null(gData.LogonIDs))  
  {
    message = "gData.LogonIDs初始状态不对，请先导入账号!";
    print(message);
    tkmessageBox(message = message);
    showposition(); 
  }
  getPositions(gData.LogonIDs); #获取仓位信息
  showposition();               #显示仓位信息
  
}

PressedCancelOrder <- function()#用户按了“全部撤单”后调用的函数
{
  canelOrders();     #撤单操作
  getOrderResult();  #重新获取下单结果
  showOrderResult(); #显示下单结果
}

Pressedclearposition<-function()#用户按了“全部清仓”后调用的函数
{
  gData.OrderResult<<-NULL;
  gData.OrderRequests<<-NULL;
  clearPositions();#清仓操作
  
  RefillBasketTable();#清仓命令会把清仓的内容放到篮子中，然后再对篮子下单，因此需要重新绘制篮子表格
}

RefillBasketTable<-function()  #显示篮子表格
{
  tkconfigure(table.basket ,state='normal');
  tkconfigure(table.basket ,rows=1);
  
  #首先检查gData.BasketData是否存在
  if(length(ls(.GlobalEnv,pattern='^gData[.]BasketData$'))<=0
     ||is.null(gData.BasketData))
  {
    tkconfigure(table.basket ,state='disabled');
    return();
  }
  
  tkconfigure(table.basket ,rows=length(gData.BasketData[,1])+1);
  for(i in 1:length(gData.BasketData[,1])){#设置表格内容
    tkset(table.basket ,paste(i,0,sep=','),i);
    for(j in 1:5){#length(gData.BasketData[1,])){
      tkset(table.basket ,paste(i,j,sep=','),as.character(gData.BasketData[i,j]));
    }
  }
  tkconfigure(table.basket ,state='disabled');
}


retsetTotalVolume<-function()  #清除下单总量
{
  #先把下单总量地方清0
  tclvalue(rbordercap.value) <-"0";
  tclvalue(rbordermul.value) <-"0";
  if(tclvalue(rbvolume.value)=='2')
    tclvalue(rbvolume.value)<-"1";
}



doImportAccount <- function() #执行导入账号
{
  #首先获取所有登录账号，用户应使用w.tlogon方式登录所有账户
  ret<-w.tquery('LogonID');
  
  logonids<-0;
  if(ret$ErrorCode==0){
    logonids<-ret$Data$LogonID;
  }
  
  if(ret$ErrorCode!=0 || any(logonids==0))
  {
    tkmessageBox(message = "查询账号tquery(7) 出现错误!")
    print(ret);
    return(0);
  }
  
  #丢掉重复LogonAccount的LogonID
  logonft<-factor(ret$Data$LogonAccount);
  if(length(logonids)!=nlevels(logonft))#有重复的，需要去除
  {
    logonids<-rep(0,nlevels(logonft))
    for(i in 1:nlevels(logonft))
    {
      logonids[i]<-ret$Data$LogonID[ret$Data$LogonAccount==levels(logonft)[i]][1]     
    }
  }
  
  #获取所有登录账号的股东账户信息，从而决定市场类型
  #gData.LogonIDs 为登录账号信息；
  #gData.LogonAccount为股东账号信息
  #gData.Logon_XXX 为某个LogonID支持的市场类型，主要为了显示。
  ret<-w.tquery('Account',logonid=logonids,showfields='LogonID,ErrorCode,AssetAccount,AccountType,MarketType');
  if(ret$ErrorCode!=0 || any(logonids==0))
  {
    tkmessageBox(message = "Querying Account/tquery(5) error!")
    print(ret);
    return(0);
  }    
  
  gData.LogonIDs<<-logonids;
  gData.LogonAccount<<-ret$Data;
  for(id in logonids){
    lvl<-levels(factor(ret$Data$MarketType[ret$Data$LogonID==id]));
    if(length(lvl)==0){
      print(ret);
      tkmessageBox(message = paste("查询账号中股东账户信息出错! (LogonID=",id,sep=''))
      return(0);
    }
    
    #填充gData.Logon_XX
    assign( paste('gData.Logon_',id,sep=''),lvl,envir=.GlobalEnv)
  }
  
  #获取资金信息
  ret<-w.tquery('Capital',logonid=logonids,showfields='LogonID,AvailableFund,TotalAsset,AssetAccount,MoneyType,ErrorCode,BalanceFund');
  index<-is.nan(ret$Data$TotalAsset);
  ret$Data$TotalAsset[index]<-ret$Data$BalanceFund[index];
  
  if(ret$ErrorCode!=0 || length(ret$Data[,1])!=length(logonids) || any(is.nan(ret$Data$AvailableFund)) 
     ||any(is.nan(ret$Data$TotalAsset))||any(ret$Data$MoneyType!='CNY')  )
  {
    print(ret);
    tkmessageBox(message = "Querying Capital/tquery(0) error or multi-capital information return!")
    return(0);
  }
  
  pasteget<-function(id){ 
    v=get(paste('gData.Logon_',id,sep=''),envir=.GlobalEnv);
    return(paste( v,sep="",collapse=';'));
  }
  
  #准备gData.AccountData变量
  gData.AccountData<<-data.frame(ret$Data[,1:4],  MarketType=unlist(lapply(logonids,pasteget)) ,MoneyType=ret$Data$MoneyType,stringsAsFactors = FALSE);
  
  #获取持仓信息
  getPositions(logonids);
  
  return(1);
}

getPositions<-function(logonids)#获取持仓信息
{
  if(is.null(logonids) || length(logonids)<=0)
  {
    gData.PositionData<<-NULL;
    return();
  }
  #获取持仓信息
  retname<-"LogonID,SecurityCode,SecurityAvail,TradeSide,EnableVolume,TodayRealVolume,MoneyType,SecurityBalance,SecurityForzen,SecurityVolume,CostPrice,LastPrice,SecurityName,ErrorCode"
  ret<-w.tquery('position',logonid=logonids,showfields=retname);
  
  #统一股票期货的可用证券、总持仓量信息
  index<-which(is.nan(ret$Data$SecurityAvail));
  ret$Data$SecurityAvail[index]<-ret$Data$EnableVolume[index];    
  
  index<-which(is.nan(ret$Data$SecurityVolume));
  ret$Data$SecurityVolume[index]<-ret$Data$EnableVolume[index];  

  #统一买卖方向
  ret$Data$TradeSide[is.nan(ret$Data$TradeSide)|ret$Data$TradeSide=='NaN']<-'Buy';  
  ret$Data$TradeSide<-tolower(ret$Data$TradeSide);#小写化交易方向
  ret$Data$SecurityCode<-toupper(ret$Data$SecurityCode);##大写化证券代码
  
  #把有效的正确持仓信息留下来
  index<-which( (ret$Data$SecurityVolume>0 | ret$Data$SecurityAvail >0 ) & ret$Data$SecurityCode!='NAN')
  gData.PositionData<<-ret$Data[index,];
  #gData.PositionData<<-ret$Data[ret$Data$SecurityCode!='NAN',];
}

updateRealTimePrice<-function()#更新实时价格信息
{
  if(length(ls(.GlobalEnv,pattern='^gData[.]BasketData$'))<=0 || length(gData.BasketData[,1])<=0)
    return(1);	 #成功，因为不需要更新
  
  #取实时价格信息
  lret<-w.wsq(gData.BasketData$Code,'rt_high_limit,rt_low_limit,rt_ask1,rt_bid1,rt_latest,rt_susp_flag,rt_pre_close');
  if(lret$ErrorCode!=0)
  {
    print('WSQ call error!');
    print(lret);
    return(0);
  }
  
  gData.BasketData$PriceHighLimit<<-lret$Data$RT_HIGH_LIMIT;#涨停价
  gData.BasketData$PriceLowLimit<<-lret$Data$RT_LOW_LIMIT   #跌停价
  gData.BasketData$PriceAsk1<<-lret$Data$RT_ASK1            #卖一价
  gData.BasketData$PriceBid1<<-lret$Data$RT_BID1            #买一价
  gData.BasketData$PriceLatest<<-lret$Data$RT_LATEST        #最新价
  gData.BasketData$Is_Suspended<<-lret$Data$RT_SUSP_FLAG%%10    #停牌标识,最后一位为0表示没有停牌
  
  #需要考虑涨停、跌停、停牌、无报价情况。。。。。。。
  gData.BasketData$PriceAsk1[gData.BasketData$PriceAsk1<0.0001] <<- gData.BasketData$PriceHighLimit[gData.BasketData$PriceAsk1<0.0001];
  gData.BasketData$PriceBid1[gData.BasketData$PriceBid1<0.0001] <<- gData.BasketData$PriceLowLimit[gData.BasketData$PriceBid1<0.0001];
  
  #由于涨跌停价指标现在正处于测试状态，临时有如下判断
  gData.BasketData$PriceHighLimit[gData.BasketData$PriceHighLimit<0.0001] <<- 10000000;
  gData.BasketData$PriceLowLimit[gData.BasketData$PriceLowLimit<0.0001] <<- 0.00001;

  k= (gData.BasketData$PriceHighLimit  - gData.BasketData$PriceLowLimit)/(gData.BasketData$PriceHighLimit  + gData.BasketData$PriceLowLimit);
  
  k[k>0.2]=0.2;
  k[k<0.2 & k>=0.11]=0.15;
  k[k<0.11 & k>=0.09]=0.1;
  k[k<0.09 & k>=0.075]=0.08;
  k[k<0.075 & k>=0.045]=0.05;
  k[k<0.045 & k>=0.035]=0.04;
  k[k<0.035 & k>=0.025]=0.03;
  k[k<0.025 & k>=0.015]=0.02;
  k[k<0.015 ]=0.01;
  
  lret$Data$RT_PRE_CLOSE[lret$Data$RT_PRE_CLOSE<0.0001] <- 100;
  
  gData.BasketData$PriceHighLimit <<- floor(lret$Data$RT_PRE_CLOSE *(1+k)/ gData.BasketData$Mfprice)*gData.BasketData$Mfprice;
  gData.BasketData$PriceLowLimit <<- floor(lret$Data$RT_PRE_CLOSE *(1-k)/ gData.BasketData$Mfprice)*gData.BasketData$Mfprice;
  
  #gData.BasketData$PriceHighLimit[gData.BasketData$PriceHighLimit<gData.BasketData$PriceAsk1] <<- gData.BasketData$PriceAsk1[gData.BasketData$PriceHighLimit<gData.BasketData$PriceAsk1];
  #gData.BasketData$PriceLowLimit[gData.BasketData$PriceLowLimit>gData.BasketData$PriceBid1] <<- gData.BasketData$PriceBid1[gData.BasketData$PriceLowLimit>gData.BasketData$PriceBid1];
  #
  
  return(1);
}

doImportBasket <- function(Basket)#导入篮子
{
  #从Basket (包含Code,TradeSide,Weight三项的data.frame格式）中导入数据。
  #Code<-c('600000.sh','000001.sz','600177.sh','IF1312.CFE','TF1312.CFE');
  #TradeSide<-c('buy','buy','sell','short','sell');
  #Weight<-c(100,100,100,1,1);
  #Basket<-data.frame(Code=Code,TradeSide=TradeSide,Weight=Weight,stringsAsFactors = FALSE)
  
  gData.BasketData<<-NULL;

  #首先检查Basket是否存在
  if(is.null(Basket))
    return();
  
  Code=NULL;
  tryCatch( 
    {	
      Code=toupper(as.character(Basket$Code));
      if(length(Code)>0)
      {
        gData.BasketData<<-data.frame(Code=Code
                                      ,Name=rep('未获得',length(Code))
                                      ,TradeSide=tolower(as.character(Basket$TradeSide))
                                      ,Weight=Basket$Weight
                                      ,Position=rep(NA,length(Code))
                                      ,LeastVolume=rep(100,length(Code))
                                      ,Mfprice=rep(0.01,length(Code))
                                      ,PriceMultiplier=rep(1,length(Code))
                                      ,PriceHighLimit=rep(0,length(Code))
                                      ,PriceLowLimit=rep(0,length(Code))
                                      ,PriceAsk1=rep(0,length(Code))
                                      ,PriceBid1=rep(0,length(Code))
                                      ,PriceLatest=rep(0,length(Code))
                                      ,Is_Suspended=rep(0,length(Code))
                                      ,stringsAsFactors = FALSE
        );
      }else{
        Code=NULL;
      }
    }
    ,error={Code=NULL;}
  )
  
  if(is.null(Code))
  {
    gData.BasketData<<-NULL;
    return();
  }
  
  updateRealTimePrice();#更新价格信息
  
  #设置一手股数，期货为1，股票为100
  shszindex=grep('[.]S[HZ]$',Code);
  if(length(shszindex)<1)
  {
    gData.BasketData$LeastVolume<<-1;
  }else
    gData.BasketData$LeastVolume[0-shszindex]<<-1;  #期货设置成1
  
  #设置品种名称等参数 
  lret<-w.wss(Code,'sec_name,mfprice,tunit,contractmultiplier,ftmargins');
  if(lret$ErrorCode==0)
  {
    gData.BasketData$Name<<-lret$Data$SEC_NAME;   #股票名称
    lret$Data$CONTRACTMULTIPLIER[is.nan(lret$Data$CONTRACTMULTIPLIER)]<-1     #期货乘数
    gData.BasketData$PriceMultiplier<<-as.numeric(lret$Data$CONTRACTMULTIPLIER);
    
    lret$Data$FTMARGINS[lret$Data$FTMARGINS=='NaN'|is.nan(lret$Data$FTMARGINS)]<-'100%'  #保证金
    lmarginindex<-gregexpr('[[:digit:]]+[.]?[[:digit:]]*%$',lret$Data$FTMARGINS)
    #lmargintext<-substring(lret$Data$FTMARGINS,lmarginindex);
    lmarginvalue<-rep(1.0,length(lmarginindex));
    for( i in 1:length(lmarginindex))
    { 
      startp <- lmarginindex[[i]][[1]];
      lmarginvalue[i]<-as.numeric(substring(lret$Data$FTMARGINS[[i]],startp,startp+attr(lmarginindex[[i]],'match.length')-2))/100.0;
    }
    
    lret$Data$TUNIT[lret$Data$TUNIT=='NaN'|is.nan(lret$Data$TUNIT)]<-'1'   #交易单位
    ltunit<-strsplit(lret$Data$TUNIT,'[[:alpha:]]')
    lret$Data$MFPRICE[lret$Data$MFPRICE=='NaN' |is.nan(lret$Data$MFPRICE)]<-'0.01';#最小变动点数
    lmfprice<-strsplit(lret$Data$MFPRICE,'[[:alpha:]]');
    for(i in 1:length(Code))
    {
      #一手需要的价格到资金乘数
      gData.BasketData$PriceMultiplier[i]<<-gData.BasketData$PriceMultiplier[i]*as.numeric(ltunit[[i]][1])*lmarginvalue[i];
      gData.BasketData$Mfprice[i]<<-as.numeric(lmfprice[[i]][1]);#最小变动点数
    }
    
  }else{
    tkmessageBox(message = "WSS没有正确获得基本信息，该篮子不能直接执行!")
    print(lret);
  }
  
  #检查持仓数据
  if(length(ls(.GlobalEnv,pattern='^gData[.]PositionData$'))<=0
     ||length(gData.PositionData$SecurityCode)<=0
  )
    return();		
  
  #更新篮子里最大交易量信息
  for(i in 1:length(Code))
  {
    tradeside<- gData.BasketData$TradeSide[[i]];
    #print(tradeside)
    if(tradeside=="buy"){#只由总金额决定
      tradeside="sell";
      next;
    }else if(tradeside=="sell"){
      tradeside="buy";
    }else if(tradeside=="cover"){
      tradeside="short";
    }else if(tradeside=="short"){#只由总金额决定
      tradeside="cover";
      next;
    }else{
      tkmessageBox(message = paste('Bad TradeSide ("',tradeside,'") !',sep=''));
      return();
    }
    
    tempframe<-gData.PositionData[gData.PositionData$SecurityCode==Code[i]&gData.PositionData$TradeSide==tradeside,];
    #print(paste(Code[i],tradeside,sum(tempframe$SecurityAvail)));
    gData.BasketData$Position[[i]]<<-sum(tempframe$SecurityAvail);
  }
  
  return(1);
}



clearPositions<-function()#把仓位作为标准，准备篮子，下单。期间会剔除停牌股票
{#清除所有仓位
  
  #得到持仓
  if(  length(ls(.GlobalEnv,pattern='^gData[.]AccountData$'))<=0
       ||length(ls(.GlobalEnv,pattern='^gData[.]PositionData$'))<=0
       ||length(gData.AccountData[,1])<=0
       ||length(gData.PositionData[,1])<=0
  )
  {
    print('初始状态不对，或者持仓数据为空！');
    return(0);
  }
  
  laccountorder<-as.integer(tclvalue(rbacc.value));#账号下单次序
  
  #先获得并检测所有变量
  lpricestrategy<-as.integer(tclvalue(rbbas.value)); #价格策略按钮
  lpriceaddcount<-as.integer(tclvalue(basketadd.value ));#价格加价量
  
  lvolumestrategy<-as.integer(tclvalue(rbvolume.value));#数量策略选项
  
  lsplitorder<-as.integer(tclvalue(cksplitorder.value));#拆单可选按钮
  lsplitordermin<-as.integer(tclvalue(cksplitordermin.value));#最小手数
  lsplitordermax<-as.integer(tclvalue(cksplitordermax.value));#最大手数
  if(lsplitordermin<=0) 
    lsplitordermin=1;
  
  if(lsplitordermax<lsplitordermin)
    lsplitordermax=lsplitordermin;
  
  #按照持仓量和交易方向反方向准备篮子
  tradeside<-gData.PositionData$TradeSide;
  indexs<-which((tradeside=='buy'|tradeside=='short')&gData.PositionData$SecurityAvail>0);
  positions<-gData.PositionData[indexs,];
  
  tradeside<-positions$TradeSide;
  tradeside[tradeside=='buy']<-'sell';
  tradeside[tradeside=='short']<-'cover';
  
  fpos<- factor(paste(positions$SecurityCode,positions$TradeSide));
  findex<-tapply(1:length(positions$SecurityCode),fpos,function(x){x[1]});
  
  basket<-data.frame(Code=positions$SecurityCode[findex],TradeSide=tradeside[findex]
                     ,Weight=as.numeric(tapply(positions$SecurityAvail,fpos,sum))
                     ,stringsAsFactors = FALSE);
  doImportBasket(basket); #导入篮子
  
  if(updateRealTimePrice()==0)#更新篮子里股票价格信息     
  {
    print('价格更新失败，不能交易!');
    tkmessageBox(message = "价格更新失败，不能交易!")
    return(0);		    	
  }
  
  initAccountOrder();#初始化AccountSelect等
  
  
  #按照价格设置、拆单情况准备单子
  #按照账号顺序下单
  ltotalamountstrategy=2;
  totalvolumes<-getTotalVolumes(2,0,0);#1b)计算出每个品种交易数量
  print('准备下单总量为:');
  print(data.frame(Code=gData.BasketData$Code,TradeSide=gData.BasketData$TradeSide,Volume=totalvolumes));
  
  totalvolumes[is.na(totalvolumes)]<-0
  if(sum(totalvolumes)<=0)
  {
    msg<-'不能下单，因为下单量都为0！';
    print(msg);
    tkmessageBox(message = msg)
    return();
  }
  
  for(i in 1:length(gData.BasketData[,1]))#2）对篮子里每一品种，做3-6
  {
    validaccounts<-getValidAccounts(i);#3）得到所有可下单的账户
    
    eachvolumes<-dispatchAmongAccounts(i,validaccounts,totalvolumes[i],2,0,0,0);
    
    #6）对每个账户的总量进行拆单
    outvolumes<-splitOrderInAccount(i,eachvolumes$volume,lsplitorder,lsplitordermin,lsplitordermax);
    for(eachv in 1:length(eachvolumes[,1]))
    {#把单子放到全局变量gData.tAccountToOrders中。
      taccountindex<-eachvolumes$accountindex[eachv]
      if(is.null(gData.tAccountToOrders[[taccountindex]]))
      {
        gData.tAccountToOrders[[taccountindex]]<<-list( basketindex=list(i),volumes=list(outvolumes[[eachv]]));
      }
      else{
        gData.tAccountToOrders[[taccountindex]]$basketindex<<-append(gData.tAccountToOrders[[taccountindex]]$basketindex, i);
        gData.tAccountToOrders[[taccountindex]]$volumes<<-append(gData.tAccountToOrders[[taccountindex]]$volumes, list(outvolumes[[eachv]]));
      }
    }
    
  }
  
  
  #7）按照”账号下单次序“依次从每个账户的单子中选择一个组织成最终的单子。
  orders<-generateOrders(laccountorder,lpricestrategy,lpriceaddcount)
  
  print(orders);
  
  #8)下单
  showFields<-'RequestID,SecurityCode,TradeSide,OrderPrice,OrderVolume,LogonID,ErrorCode,ErrorMsg';
  lout<-w.torder(orders$code,orders$tradeside,orders$price,orders$volume,logonid=orders$logonid,showfields=showFields);
  
  retsetTotalVolume();#把下单总量清0
  
  gData.OrderRequests<<-lout$Data
  gData.OrderRequests$LogonID<<-orders$logonid;
  if(lout$ErrorCode!=0)
  {
    print(lout);
    tkmessageBox(message = '下单过程中出现错误!');
    return(0);
  }
  
  print('下单结果在gData.OrderRequests变量中');
  showExeResult(); 
  
}

#初始化账户选择的各种变量
initAccountOrder <-function()#iaccountorder,ivolumestrategy)
{
  #print(paste('initAccountOrder(iaccountorder=',iaccountorder,',ivolumestrategy=',ivolumestrategy,')',sep=''));
  #gData.tAccountIndex<<-1;
  gData.tAccountSelect<<-rep(0,length(gData.AccountData[,1]));
  gData.tAccountCapital<<-gData.AccountData;
  gData.tPosition<<-gData.PositionData;
  gData.tAccountToOrders<<-vector('list',length(gData.AccountData[,1]));
}

#返回能够允许basketindex对应品种下单的账户序号和可操作总量
getValidAccounts <-function(basketindex)
{
  #print(paste('getValidAccounts(basketindex=',basketindex,')',sep=''));
  
  #1)先获得代码,并根据账号市场类型获得所有可能账户index
  code<- gData.BasketData$Code[[basketindex]];
  
  #获得交易方向情况
  tt<-getPositionTradeSide(gData.BasketData$TradeSide[[basketindex]]);
  tradeside<-tt$tradeSide;
  tradetype<-tt$tradeType;#0 to buy by capital, 1 to sell from position
  
  if(tradetype==1)
  {#返回有持仓的账户
    tempframe<-gData.tPosition[gData.tPosition$SecurityCode==code&gData.tPosition$TradeSide==tradeside,];
    accountids<-tempframe$LogonID;
    if(length(accountids)==0)
    {
      return (NULL);
    }
    accountindex<-rep(0,length(accountids));
    indexs<-1:length(accountids);
    for(i in indexs){
      accountindex[i]<-which(gData.LogonIDs==accountids[i]);
    }
    return( data.frame(accountindex=accountindex,maxvolume=tempframe$SecurityAvail,position=rep(1,length(accountindex))));
    
  }else{
    #对每个账号，检查它是否可以交易该品种，然后看是否有资金
    marktype<-strsplit(code,'[.]');
    marktype<-marktype[[1]][[length(marktype[[1]])]]
    
    logonidf<-factor(gData.LogonAccount$LogonID[gData.LogonAccount$MarketType==marktype])
    accountids=as.integer(levels(logonidf));				 
    
    accountindex<-rep(0,length(accountids));
    indexs<-1:length(accountids);
    maxvolume=rep(0,length(accountids));
    
    tprice<-gData.BasketData$PriceHighLimit[basketindex]*gData.BasketData$PriceMultiplier[basketindex]
    
    for(i in indexs){
      lacindx<-which(gData.LogonIDs==accountids[i]);
      accountindex[i]<-lacindx;
      
      #if(tradetype==0)#买，用涨停价计算
      {
        maxvolume[i]<- gData.tAccountCapital$AvailableFund[lacindx]/tprice;
        #}else{#用
      }
    }
    return( data.frame(accountindex=accountindex,maxvolume=maxvolume,position=rep(0,length(accountindex))));
  }
}


fupdateposition<-function(basketindex,outvolumes,validaccounts) #由于下单变化影响仓位
{
  if(length(validaccounts$maxvolume)==0 || any(outvolumes>validaccounts$maxvolume))
  {
    print('Error in dispatchAmongAccounts');
    print(validaccounts);
    return(NULL);
  }
  taccountindex<-validaccounts$accountindex[outvolumes>0];
  gData.tAccountSelect[taccountindex] <<- gData.tAccountSelect[taccountindex]+1;
  
  #print(validaccounts);
  #print('here');
  if(validaccounts$position[1]==0)
  {#减去资金
    gData.tAccountCapital$AvailableFund[validaccounts$accountindex] <<- gData.tAccountCapital$AvailableFund[validaccounts$accountindex] -
      outvolumes * gData.BasketData$PriceMultiplier[basketindex]*gData.BasketData$PriceHighLimit[basketindex]
  }else{#减去持仓。。。
    tradeside<-getPositionTradeSide(gData.BasketData$TradeSide[[basketindex]])$tradeSide;
    for(j in 1:length(validaccounts[,1]))
    {
      logonid<- gData.AccountData$LogonID[validaccounts$accountindex[j]];
      tempindex<-which(gData.tPosition$SecurityCode==gData.BasketData$Code[[basketindex]]
                       &gData.tPosition$TradeSide==tradeside & gData.tPosition$LogonID==logonid);
      gData.tPosition[tempindex,]$SecurityAvail<<-gData.tPosition[tempindex,]$SecurityAvail - outvolumes[j];
    }
  }
  return( data.frame(accountindex=taccountindex,volume=outvolumes[outvolumes>0]) );  
}
#4）按照数量策略分配量：考虑资金是否足够、每手股数等，最后扣除该资金,#5）调整AccountSelect
dispatchAmongAccounts <-function(basketindex,validaccounts,totalvolume,totalamountstrategy,volumestrategy,volumemin,volumemax)
{
  #print(paste('dispatchAmongAccounts(basketindex=',basketindex
  #               ,',validaccounts=',validaccounts,',totalvolume=',totalvolume
  #               ,',volumestrategy=',volumestrategy,',volumemin=',volumemin
  #               ,',volumemax=',volumemax,')',sep=''));
  if(totalamountstrategy==2)
  {#清仓位
    outvolumes<-validaccounts$maxvolume;
    taccountindex<-validaccounts$accountindex[outvolumes>0];
    gData.tAccountSelect[taccountindex] <<- gData.tAccountSelect[taccountindex]+1;
    
    #减去持仓。。。
    tradeside<-getPositionTradeSide(gData.BasketData$TradeSide[[basketindex]])$tradeSide;
    for(j in 1:length(validaccounts[,1]))
    {
      logonid<- gData.AccountData$LogonID[validaccounts$accountindex[j]];
      tempindex<-which(gData.tPosition$SecurityCode==gData.BasketData$Code[[basketindex]]
                       &gData.tPosition$TradeSide==tradeside & gData.tPosition$LogonID==logonid);
      gData.tPosition$SecurityAvail[tempindex]<<-0;
    }
    return( data.frame(accountindex=taccountindex,volume=outvolumes[outvolumes>0]) );      
  }
  if(volumestrategy==0)
  {#所有账号一样多
    eachvolume<-totalvolume/length(validaccounts[,1]);
    eachvolume<-floor(0.01+eachvolume/gData.BasketData$LeastVolume[basketindex])*gData.BasketData$LeastVolume[basketindex]
    outvolumes<-rep(eachvolume,length(validaccounts[,1]));
    outvolumes[1]<-eachvolume + totalvolume - eachvolume*length(validaccounts[,1]);
    
    return (fupdateposition(basketindex,outvolumes,validaccounts))
  }
  
  if(volumestrategy==1)
  {#只有一个账号
    
    tvalidaccountindexindex<-which.min(gData.tAccountSelect[validaccounts$accountindex])
    tvalidaccountindex<-validaccounts$accountindex[tvalidaccountindexindex];
    
    outvolumes<-round(totalvolume/gData.BasketData$LeastVolume[basketindex])*gData.BasketData$LeastVolume[basketindex]
    
    if(outvolumes>validaccounts$maxvolume[tvalidaccountindexindex])
    {
      print('Error in dispatchAmongAccounts');
      print(validaccounts);
      print(tvalidaccountindex);
      print(outvolumes);
      return(NULL);
    }
    
    gData.tAccountSelect[tvalidaccountindex]<<-gData.tAccountSelect[tvalidaccountindex]+1;
    
    #print(validaccounts);
    #减去持仓，或者减去资金
    if(validaccounts$position[1]==0)
    {
      gData.tAccountCapital$AvailableFund[tvalidaccountindex] <<- gData.tAccountCapital$AvailableFund[tvalidaccountindex] -
        outvolumes * gData.BasketData$PriceMultiplier[basketindex]*gData.BasketData$PriceHighLimit[basketindex]
    }else{#减去持仓。。。
      tradeside<-getPositionTradeSide(gData.BasketData$TradeSide[[basketindex]])$tradeSide;
      logonid<- gData.AccountData$LogonID[tvalidaccountindex];
      tempindex<-which(gData.tPosition$SecurityCode==gData.BasketData$Code[[basketindex]] & gData.tPosition$TradeSide==tradeside & gData.tPosition$LogonID==logonid);
      gData.tPosition[tempindex,]$SecurityAvail<<-gData.tPosition[tempindex,]$SecurityAvail - outvolumes;
    }
    
    return( data.frame(accountindex=tvalidaccountindex,volume=outvolumes) );
  }
  if(volumestrategy==2)
  {#按总资产比例分配
    ratiov<- gData.AccountData$TotalAsset[validaccounts$accountindex]/sum(gData.AccountData$TotalAsset[validaccounts$accountindex]);
    maxi<- which.max(validaccounts$maxvolume)
    
    outvolumes<-floor(0.01+ratiov*totalvolume/gData.BasketData$LeastVolume[basketindex])*gData.BasketData$LeastVolume[basketindex];
    outvolumes[maxi]<- outvolumes[maxi]+ totalvolume - sum(outvolumes);
    
    return (fupdateposition(basketindex,outvolumes,validaccounts))
  }
  if(volumestrategy==3)
  {#按可用产比例分配
    ratiov<- gData.AccountData$AvailableFund[validaccounts$accountindex]/sum(gData.AccountData$AvailableFund[validaccounts$accountindex]);
    maxi<- which.max(validaccounts$maxvolume)
    
    outvolumes<-floor(0.01+ratiov*totalvolume/gData.BasketData$LeastVolume[basketindex])*gData.BasketData$LeastVolume[basketindex];
    outvolumes[maxi]<- outvolumes[maxi]+ totalvolume - sum(outvolumes);
    return (fupdateposition(basketindex,outvolumes,validaccounts))
    
  }
  if(volumestrategy==4)
  {#随机分配
    
    totalvolume = floor(0.01+totalvolume/gData.BasketData$LeastVolume[basketindex]);
    
    eachvolume<-totalvolume/length(validaccounts[,1]);
    eachvolume<-floor(0.01+eachvolume)
    
    if(volumemin<1)
      volumemin = 1;
    if(volumemin >eachvolume)
      volumemin = eachvolume
    
    deltamax<-totalvolume - volumemin*length(validaccounts[,1]);;
    ratio<- runif(length(validaccounts[,1]),0.01,deltamax);
    deltvol<-floor(deltamax*ratio/sum(ratio));
    deltvol[1]<-deltvol[1]+deltamax-sum(deltvol)
    outvolumes<-deltvol+volumemin;
    
    outvolumes = outvolumes*gData.BasketData$LeastVolume[basketindex];
    
    return (fupdateposition(basketindex,outvolumes,validaccounts));
  }
  else{
    tkmessageBox(message = "目前数量策略只支持每账户数量相同或一个品种一个账号!")
    return(NULL);    
  }    
  
}

#4）计算出每个品种交易数量
getTotalVolumes <-function(totalamountstrategy,ordercapital,ordermultipy)
{
  #		print(paste('getTotalVolumes(totalamountstrategy=',totalamountstrategy
  #		               ,',ordercapital=',ordercapital,',ordermultipy=',ordermultipy,')',sep=''));
  
  if(totalamountstrategy==2)
  {#清空篮子股票仓位
    volumes<-rep(0,length(gData.BasketData$Weight));
    indexs<-which(gData.BasketData$TradeSide=='sell' | gData.BasketData$TradeSide=='cover');
    volumes[indexs]<-gData.BasketData$Position[indexs]*ifelse(gData.BasketData$Is_Suspended[indexs]!=0,0,1);
    return( volumes);
  }
  
  if(totalamountstrategy==0)
  {#按资金总量，此时篮子里
    #先计算 篮子比例下当前需要资金总额。
    tcapital<-gData.BasketData$PriceHighLimit*gData.BasketData$PriceMultiplier*gData.BasketData$Weight;
    tcapitalsum<-sum(tcapital);
    
    #计算乘数
    ordermultipy<- ordercapital/tcapitalsum;
  }
  
  volumes<-gData.BasketData$Weight*ordermultipy;
  
  volumes<-round(volumes/gData.BasketData$LeastVolume)*gData.BasketData$LeastVolume*ifelse(gData.BasketData$Is_Suspended!=0,0,1);
  
  return( volumes);
}

getPositionTradeSide<-function(orderTradeSide)#根据交易方向得到持仓方向
{
  tradetype=0;#0 to buy by capital, 1 to sell from position
  
  if(orderTradeSide=="buy" ){#只由总金额决定
    orderTradeSide="";
  }else if(orderTradeSide=="sell"){
    orderTradeSide="buy";
    tradetype=1;
  }else if(orderTradeSide=="cover"){
    orderTradeSide="short";
    tradetype=1;
  }else if(orderTradeSide=="short"){#只由总金额决定
    orderTradeSide="";
  }else{
    orderTradeSide="";
  } 
  return( list(tradeSide=orderTradeSide,tradeType=tradetype));
}


#6）对每个账户的总量进行拆单
splitOrderInAccount <-function(basketindex,totalvolumes,splitorder,splitordermin,splitordermax)
{
  print(paste('splitOrderInAccount(basketindex=',basketindex
              ,',totalvolumes=',totalvolumes,',splitorder=',splitorder
              ,',splitordermin=',splitordermin,',splitordermax=',splitordermax,')',sep=''));
  if(splitorder==0)
    return(as.list(totalvolumes));
  
  leastVolume<-gData.BasketData$LeastVolume[basketindex];
  totalvolumes<-round(totalvolumes/leastVolume)*leastVolume
  
  if(splitordermin<1) splitordermin=1;
  if(splitordermax<splitordermin) splitordermax=splitordermin;
  
  outvolumes<-vector('list',length(totalvolumes));
  
  for(i in 1:length(totalvolumes))
  {
    eachvolumes<-c();
    eachtotal<-totalvolumes[i];
    while(eachtotal>=0.1)
    {
      lvolume<-leastVolume*round(runif(1,splitordermin,splitordermax));
      if(lvolume>eachtotal)
        lvolume = eachtotal;
      eachvolumes<-append(eachvolumes,lvolume);
      eachtotal<- eachtotal-lvolume;
    }
    outvolumes[[i]]<-eachvolumes;
  }
  
  return (outvolumes);
}

#6）对每个账户的总量进行拆单
generateOrders <-function(accountorder,pricestrategy,priceaddcount)
{
  print(paste('generateOrders(accountorder=',accountorder
              ,',pricestrategy=',pricestrategy,',priceaddcount=',priceaddcount
              ,')',sep=''));
  
  lempty<-FALSE;
  if(priceaddcount<1)
    priceaddcount<-1;
  
  #首先获得总量
  lcount<-0;
  for(i in 1:length(gData.tAccountToOrders))
  {
    if(is.null(gData.tAccountToOrders[[i]]))
      next;
    
    for(j in 1:length( 	gData.tAccountToOrders[[i]]$volumes) )
    {
      lcount <- lcount + length(gData.tAccountToOrders[[i]]$volumes[[j]]);
    }
  }
  
  outcodes<-vector('character',lcount);	
  outtradeside<-vector('character',lcount);
  outprice<-vector('double',lcount);
  outvolume<-vector('numeric',lcount);
  outlogonid<-vector('character',lcount);
  outindex<-0;
  
  #litrcount<-lcount;
  lbeginaccountindex<-1;
  
  #if(accountorder==0){#次序不变
  accountindex<-1:length(gData.tAccountToOrders);  
  
  if(accountorder==4){#按资金优先
    accountindex<-accountindex[order(gData.AccountData$TotalAsset,decreasing=TRUE)];
  }
  while(outindex<lcount)
  {
    if(accountorder==1)#依次变化
    {
      if(lbeginaccountindex<=1){
        accountindex<-1:length(gData.tAccountToOrders);
      }else{
        accountindex<-c(lbeginaccountindex:length(gData.tAccountToOrders),1:(lbeginaccountindex-1) );
        lbeginaccountindex<- lbeginaccountindex+1;
      }
    }else if(accountorder==2)#随机
    {
      accountindex<-sample.int(length(gData.tAccountToOrders));
    }
    
    for(laccounti in accountindex)
    {
      if(is.null(gData.tAccountToOrders[[laccounti]]) || length(gData.tAccountToOrders[[laccounti]]$volumes)==0 )
      {
        next;
      }
      
      basketindex<-gData.tAccountToOrders[[laccounti]]$basketindex[[1]] ;
      
      outindex <- outindex+1;
      outvolume[outindex]<-gData.tAccountToOrders[[laccounti]]$volumes[[1]][[1]];
      if(length(gData.tAccountToOrders[[laccounti]]$volumes[[1]])<=1)
      {
        gData.tAccountToOrders[[laccounti]]$volumes[[1]]<<-NULL;
        gData.tAccountToOrders[[laccounti]]$basketindex[[1]]<<-NULL;
      }else{
        gData.tAccountToOrders[[laccounti]]$volumes[[1]]<<-gData.tAccountToOrders[[laccounti]]$volumes[[1]][-1];
        #gData.tAccountToOrders[[laccounti]]$basketindex[[1]]<<-NULL;  				
      }
      
      
      outcodes[outindex]<- gData.BasketData$Code[basketindex];
      outtradeside[outindex]<- gData.BasketData$TradeSide[basketindex];
      
      if(pricestrategy==1)#本方价位
      {
        if( outtradeside[outindex] == 'buy' || outtradeside[outindex] == 'cover')
        {#买一价
          outprice[outindex]<- gData.BasketData$PriceBid1[basketindex]
        }else{#卖一价
          outprice[outindex]<- gData.BasketData$PriceAsk1[basketindex]
        }
      }else if(pricestrategy==2)#市价
      {
        outprice[outindex]<-0;
      }else if(pricestrategy==3){#涨跌停价
        if( outtradeside[outindex] == 'buy' || outtradeside[outindex] == 'cover')
        {#买一价
          outprice[outindex]<- gData.BasketData$PriceHighLimit[basketindex]
        }else{#卖一价
          outprice[outindex]<- gData.BasketData$PriceLowLimit[basketindex]
        }
      }else{#对手价加加
        if( outtradeside[outindex] == 'buy' || outtradeside[outindex] == 'cover')
        {#买一价
          outprice[outindex]<- gData.BasketData$PriceAsk1[basketindex] + priceaddcount *gData.BasketData$Mfprice[basketindex]
          if(outprice[outindex]>gData.BasketData$PriceHighLimit[basketindex])
            outprice[outindex]<- gData.BasketData$PriceHighLimit[basketindex]
        }else{#卖一价
          outprice[outindex]<- gData.BasketData$PriceBid1[basketindex] - priceaddcount *gData.BasketData$Mfprice[basketindex]
          if(outprice[outindex]<gData.BasketData$PriceLowLimit[basketindex])
            outprice[outindex]<- gData.BasketData$PriceLowLimit[basketindex]  					
        }
      }
      
      outlogonid[outindex]<-gData.AccountData$LogonID[laccounti];
    }
  }
  
  return (data.frame(codes=outcodes,tradeside=outtradeside,price=outprice,volume=outvolume,logonid=outlogonid));
  
}

showposition<-function()#显示持仓
{
  if(  length(ls(.GlobalEnv,pattern='^gData[.]PositionData$'))<=0 || is.null(gData.PositionData) || length(gData.PositionData[,1])<1)
  {
    print('没有找到gData.PositionData、或无持仓！');
    tkconfigure(table.ExeResults ,state='normal');
    tkconfigure(table.ExeResults ,rows=0);
    tkconfigure(table.ExeResults ,cols=0);
    tkconfigure(table.ExeResults ,state='disabled');       
    return(0);
  }

  
  out<-data.frame(Num='#',Code='证券代码',Name='证券名称',TradeSide='持仓方向',Available='可交易量',SecurityVolume='持仓量',stringsAsFactors = FALSE);#, CostPrice='成本价'
  for(i in 1:length(gData.PositionData[,1])){
    whichindex<- which(out$Code==gData.PositionData$SecurityCode[i]& 
                         out$TradeSide==gData.PositionData$TradeSide[i]);
    
    if(length(whichindex)<=0)
    {
      numindex<-length(out[,1]);
      out[numindex+1,]<-data.frame(Num=as.character(numindex),Code=as.character(gData.PositionData$SecurityCode[i])
                                   ,Name=as.character(gData.PositionData$SecurityName[i]),TradeSide=as.character(gData.PositionData$TradeSide[i])
                                   ,Available=as.character(gData.PositionData$SecurityAvail[i])#,CostPrice=as.character(gData.PositionData$CostPrice[i])
                                   ,SecurityVolume=as.character(gData.PositionData$SecurityVolume[i])
                                   ,stringsAsFactors = FALSE);
      next;
    }
    #print(gData.PositionData[i,]);
    
    out$Available[[whichindex]]<-as.character(as.numeric(out$Available[[whichindex]]) + as.numeric(gData.PositionData$SecurityAvail[i]));
    out$SecurityVolume[[whichindex]]<-as.character(as.numeric(out$SecurityVolume[[whichindex]]) + as.numeric(gData.PositionData$SecurityVolume[i]));
  }
  
  #清除登录表格
  tkconfigure(table.ExeResults ,state='normal');
  tkconfigure(table.ExeResults ,rows=length(out[,1]));
  tkconfigure(table.ExeResults ,cols=6);
  for(i in 1:length(out[,1])){
    for(j in 1:6){#length(gData.AccountData[1,])){
      tkset(table.ExeResults ,paste((i-1),(j-1),sep=','),out[i,j]);
    }
  }
  tkconfigure(table.ExeResults ,state='disabled');	 
}

showExeResult<-function()#显示委托下单结果
{
  if(  length(ls(.GlobalEnv,pattern='^gData[.]OrderRequests$'))<=0 || is.null(gData.OrderRequests))
  {
    print('没有找到gData.OrderRequests！');
    tkconfigure(table.ExeResults ,state='normal');
    tkconfigure(table.ExeResults ,rows=0);
    tkconfigure(table.ExeResults ,cols=0);
    tkconfigure(table.ExeResults ,state='disabled');       
    return(0);
  }
  
  titles<-c('#','登录ID','证券代码','委托方向','委托价','委托量','错误号','错误信息');
  tkconfigure(table.ExeResults ,state='normal');
  tkconfigure(table.ExeResults ,rows=1+length(gData.OrderRequests[,1]));
  tkconfigure(table.ExeResults ,cols=length(titles));
  
  for(j in 1:length(titles))
  {
    tkset(table.ExeResults ,paste(0,j-1,sep=','),titles[j]);
  }
  for(i in 1:length(gData.OrderRequests[,1])){
    tkset(table.ExeResults ,paste(i,0,sep=','),i);
    
    tkset(table.ExeResults ,paste(i,1,sep=','),as.character(gData.OrderRequests$LogonID[i]));       
    tkset(table.ExeResults ,paste(i,2,sep=','),as.character(gData.OrderRequests$SecurityCode[i]));       
    tkset(table.ExeResults ,paste(i,3,sep=','),as.character(gData.OrderRequests$TradeSide[i]));       
    tkset(table.ExeResults ,paste(i,4,sep=','),as.character(gData.OrderRequests$OrderPrice[i]));       
    tkset(table.ExeResults ,paste(i,5,sep=','),as.character(gData.OrderRequests$OrderVolume[i]));       
    tkset(table.ExeResults ,paste(i,6,sep=','),as.character(gData.OrderRequests$ErrorCode[i]));       
    tkset(table.ExeResults ,paste(i,7,sep=','),as.character(gData.OrderRequests$ErrorMsg[i]));       
    
    #for(j in 1:7){#length(gData.BasketData[1,])){
    #    tkset(table.ExeResults ,paste(i,j,sep=','),as.character(gData.BasketData[i,j]));
    #}
  }
  tkconfigure(table.ExeResults ,state='disabled');	     
}


getOrderResult<-function()#查询委托下单结果
{
  gData.OrderResult<<-NULL;
  
  if(  length(ls(.GlobalEnv,pattern='^gData[.]OrderRequests$'))<=0 || is.null(gData.OrderRequests) || length(gData.OrderRequests$RequestID)<=0)
  {
    print('没有找到有效gData.OrderRequests，请先正确下单！');
    tkconfigure(table.ExeResults ,state='normal');
    tkconfigure(table.ExeResults ,rows=0);
    tkconfigure(table.ExeResults ,cols=0);
    tkconfigure(table.ExeResults ,state='disabled');       
    return(0);
  }  
  
  showFields<-'LogonID,SecurityCode,TradeSide,OrderPrice,OrderVolume,TradedPrice, TradedVolume, CancelVolume, OrderStatus,ErrorMsg,LastPrice,RequestID,OrderNumber,SecurityName,ErrorCode';
  tret<-w.tquery(2,requestid=gData.OrderRequests$RequestID,LogonID=gData.OrderRequests$LogonID,showfields=showFields)
  
  
  if(tret$ErrorCode!=0)
  {
    print('以RequestID查询出错！')
    print(tret);
    return;
  }
  tret2<-w.tquery(2,ordernumber=tret$Data$OrderNumber,LogonID=tret$Data$LogonID,showfields=showFields);
  if(is.null(tret2$Data) || length(tret2$Data[,1])!=length(tret$Data$LogonID))
  {
    print('以OrderNumber查询出错！');
    print(tret2);
    return;
  }
  
  gData.OrderResult<<-tret2$Data;
  
  gData.OrderResult$RequestID<<-gData.OrderRequests$RequestID;
  gData.OrderResult$SecurityCode<<-gData.OrderRequests$SecurityCode;
  gData.OrderResult$TradeSide<<-gData.OrderRequests$TradeSide;
  gData.OrderResult$OrderPrice<<-gData.OrderRequests$OrderPrice;
  gData.OrderResult$OrderVolume<<-gData.OrderRequests$OrderVolume;
  
  indexs<-which(tret$Data$OrderNumber=='NaN');
  gData.OrderResult$OrderStatus[indexs]<<-tret$Data$OrderStatus[indexs];
  gData.OrderResult$ErrorMsg[indexs]<<-tret$Data$ErrorMsg[indexs];
  gData.OrderResult$ErrorCode[indexs]<<-tret$Data$ErrorCode[indexs];
  gData.OrderResult$LogonID[indexs]<<- tret$Data$LogonID[indexs];
  
  gData.OrderResult$ErrorMsg<<- substr(gData.OrderResult$ErrorMsg,1,10);
  
  gData.OrderResult$TradedPrice[is.nan(gData.OrderResult$TradedPrice)] <<-0;
  gData.OrderResult$TradedVolume[is.nan(gData.OrderResult$TradedVolume)] <<-0;
  gData.OrderResult$CancelVolume[is.nan(gData.OrderResult$CancelVolume)] <<-0;
  gData.OrderResult$LastPrice[is.nan(gData.OrderResult$LastPrice)] <<-0;
  
}

showOrderResult<-function()#显示委托下单结果
{#显示下单的结果，先通过RequestID获得OrderNumber，有OrderNumber后去获取执行情况。
  
  if(  length(ls(.GlobalEnv,pattern='^gData[.]OrderResult$'))<=0 || is.null(gData.OrderResult))
  {
    print('没有找到gData.OrderResult！');
    tkconfigure(table.ExeResults ,state='normal');
    tkconfigure(table.ExeResults ,rows=0);
    tkconfigure(table.ExeResults ,cols=0);
    tkconfigure(table.ExeResults ,state='disabled');       
    return(0);
  }
  
  #LogonID,SecurityCode,TradeSide,OrderPrice,OrderVolume,TradedPrice, TradedVolume, CancelVolume, OrderStatus,ErrorMsg,
  
  titles<-c('#','登录ID','证券代码','交易方向','委托价','委托量','交易价','交易量','撤销量','下单状态','错误信息');
  tkconfigure(table.ExeResults ,state='normal');
  tkconfigure(table.ExeResults ,rows=1+length(gData.OrderResult[,1]));
  tkconfigure(table.ExeResults ,cols=length(titles));
  
  for(j in 1:length(titles))
  {
    tkset(table.ExeResults ,paste(0,j-1,sep=','),titles[j]);
  }
  for(i in 1:length(gData.OrderResult[,1])){
    tkset(table.ExeResults ,paste(i,0,sep=','),i);
    for(j in 1:(length(titles)-1))
    {
      tkset(table.ExeResults ,paste(i,j,sep=','),as.character(gData.OrderResult[i,j]));       
    }
    
    #     tkset(table.ExeResults ,paste(i,1,sep=','),as.character(gData.OrderResult$LogonID[i]));       
    #     tkset(table.ExeResults ,paste(i,2,sep=','),as.character(gData.OrderResult$SecurityCode[i]));       
    #     tkset(table.ExeResults ,paste(i,3,sep=','),as.character(gData.OrderResult$TradeSide[i]));       
    #     tkset(table.ExeResults ,paste(i,4,sep=','),as.character(gData.OrderResult$OrderPrice[i]));       
    #     tkset(table.ExeResults ,paste(i,5,sep=','),as.character(gData.OrderResult$OrderVolume[i]));       
    #     tkset(table.ExeResults ,paste(i,6,sep=','),as.character(gData.OrderResult$ErrorCode[i]));       
    #     tkset(table.ExeResults ,paste(i,7,sep=','),as.character(gData.OrderResult$ErrorMsg[i]));       
    
  }
  tkconfigure(table.ExeResults ,state='disabled');	     
}


canelOrders<-function()#针对已经下单，全部撤单
{
  gData.OrderResult<<-NULL;
  
  if(  length(ls(.GlobalEnv,pattern='^gData[.]OrderRequests$'))<=0 || is.null(gData.OrderRequests) || length(gData.OrderRequests$RequestID)<=0)
  {
    msg<-'没有下单！不需要撤单！';
    print(msg);
    tkconfigure(table.ExeResults ,state='normal');
    tkconfigure(table.ExeResults ,rows=0);
    tkconfigure(table.ExeResults ,cols=0);
    tkconfigure(table.ExeResults ,state='disabled');       
    tkmessageBox(message = msg)
    return(0);
  }  
  
  #查询下单结果
  showFields<-'LogonID,SecurityCode,TradeSide,OrderPrice,OrderVolume,TradedPrice, TradedVolume, CancelVolume, OrderStatus,ErrorMsg,LastPrice,RequestID,OrderNumber,SecurityName,ErrorCode';
  tret<-w.tquery(2,requestid=gData.OrderRequests$RequestID,LogonID=gData.OrderRequests$LogonID,showfields=showFields)
  
  if(tret$ErrorCode!=0)
  {
    msg<-'以RequestID查询出错，没有撤单！'
    print(msg)
    print(tret);
    tkmessageBox(message = msg)
    return;
  }
  
  #全部撤单
  tret2<-w.tcancel(tret$Data$OrderNumber,logonid=tret$Data$LogonID);
  
  #有时下单过程本身很长时间才有反应，也就是OrderNumber没有能得到，此时需要等待
  begintime<-Sys.time();
  dealAll=FALSE;
  while(Sys.time()-begintime<10)#最长10秒内不停重新获取下单结果，直到OrderNumber得到
  {
    retryret<-tret$Data[ (tret$Data$OrderNumber=='NaN'&tret$Data$OrderStatus!='Invalid'),]
    if(length(retryret[,1])<=0)
    {
      dealAll=TRUE;
      break;
    }
    #还有一些单子下出去后没有回来
    print('还有一些单子下出去后没有回馈');
    Sys.sleep(0.5);
    
    tret<-w.tquery(2,requestid=retryret$RequestID,LogonID=retryret$LogonID,showfields=showFields)
    if(is.null(tret$Data) || length(tret$Data)<1)
    {
      print('出错了！');
      break;
    }
    
    if(any(tret$Data$OrderNumber!='NaN')){#得到OrderNumber后撤单
      tret2<-w.tcancel(tret$Data$OrderNumber,logonid=tret$Data$LogonID);
    }
  }
  
  if(!dealAll){
    retryret<-tret$Data[ (tret$Data$OrderNumber=='NaN'&tret$Data$OrderStatus!='Invalid'),]
    msg<-'有一些单子没有能发出撤单请求！'
    print(retryret);
  }else
    msg<-'撤单命令已经发出，请稍后查询下单结果！'
  print(msg);
  tkmessageBox(message = msg)
  
}

#################################################################################
#################################################################################
#以下是界面程序
tclRequire("Tktable")   #导入Table库
tt <- tktoplevel(width=740,height=600)  #设置窗口大小
tktitle(tt)<-'Wind 专业下单器（多账号、组合、对冲下单）' 
frameOverall <- tkframe(tt,width=740,height=600)
tkplace(frameOverall,x=0,y=0);

##以下准备导入账号，账户下单次序界面
frame.accountsel <- tkframe(frameOverall,width=130,height=140)
frame.rbaccount <- tkframe(frame.accountsel ,relief="groove",borderwidth=2,width=130,height=100)
rbacc.value <- tclVar("accountorder")
tclvalue(rbacc.value) <-"0";

rbacc.same <- tkradiobutton(frame.rbaccount ,variable=rbacc.value,text='次序不变',value="0")#,state='normal')
rbacc.diff <- tkradiobutton(frame.rbaccount ,variable=rbacc.value,text='依次变化',value="1")
rbacc.rand <- tkradiobutton(frame.rbaccount ,variable=rbacc.value,text='次序随机',value="2")
rbacc.capi <- tkradiobutton(frame.rbaccount ,variable=rbacc.value,text='资金优先',value="3" )#,state='disabled'
tkgrid(rbacc.same ,sticky="w");
tkgrid(rbacc.diff ,sticky="w");
tkgrid(rbacc.rand ,sticky="w");
tkgrid(rbacc.capi ,sticky="w");

button.accountsel <- tkbutton(frame.accountsel, text = "导入账号", command = PressedImportAccount )

label.accountsel<-tklabel(frame.accountsel ,text='账号下单次序:');
tkplace(button.accountsel,x=5,y=0,width=120,height=22);
tkplace(label.accountsel,x=0,y=22,height=18);
tkplace(frame.rbaccount ,x=0,y=40,width=130);
tkplace(frame.accountsel ,x=0,y=0,width=130,height=140);


##以下登陆帐户表格
tclName.LogonIDArr<-'TCLLogonIDs';

.Tcl(paste("set ",tclName.LogonIDArr,"(0,0) \"#\"",sep=""))
.Tcl(paste("set ",tclName.LogonIDArr,"(0,1) \"LogonID\"",sep=""))
.Tcl(paste("set ",tclName.LogonIDArr,"(0,2) \"可用资金\"",sep=""))
.Tcl(paste("set ",tclName.LogonIDArr,"(0,3) \"资金总量\"",sep=""))
.Tcl(paste("set ",tclName.LogonIDArr,"(0,4) \"资金账号\"",sep=""))
.Tcl(paste("set ",tclName.LogonIDArr,"(0,5) \"账号类型\"",sep=""))
#.Tcl(paste("set ",tclName.LogonIDArr,"(0,6) \"经纪商\"",sep=""))

frame.tbllogonIDs<- tkframe(frameOverall,width=740)
table.logonIDs <- tkwidget(frame.tbllogonIDs,"table",variable=tclName.LogonIDArr,cols="6",titlerows="1"
                    ,titlecols="1",selectmode="extended",background="white"
                    ,xscrollcommand=function(...) tkset(xscr.logonIDs ,...),yscrollcommand=function(...) tkset(yscr.logonIDs ,...)
                    ,height=140,rows=1,colstretchmode="unset"
			  						,selecttype='row',state='disabled'
                    )

xscr.logonIDs <-tkscrollbar(frame.tbllogonIDs,orient="horizontal", command=function(...)tkxview(table.logonIDs ,...))
yscr.logonIDs <- tkscrollbar(frame.tbllogonIDs,command=function(...)tkyview(table.logonIDs ,...))

#tkplace(tklabel(frame.status,text="状态："),x=0,y=0,width=60);
tkplace(table.logonIDs,x=0,y=0,width=590,height=120)
tkplace(yscr.logonIDs,x=590,y=0,width=20,height=120)
tkplace(xscr.logonIDs,x=0,y=120,width=610,height=20)
tkplace(frame.tbllogonIDs,x=130,y=0,width=610,height=140);


##以下导入篮子，价格策略界面
frame.basketsel<- tkframe(frameOverall,width=130,height=148)
frame.rbbasket <- tkframe(frame.basketsel,relief="groove",borderwidth=2,width=130,height=110)
rbbas.value <- tclVar("basketorder")
tclvalue(rbbas.value) <-"0";

rbbas.add <- tkradiobutton(frame.rbbasket ,variable=rbbas.value,text='对手价加减',value="0")#,state='normal')
rbbas.buy1 <- tkradiobutton(frame.rbbasket ,variable=rbbas.value,text='本方价位',value="1")#,state='normal')
rbbas.last <- tkradiobutton(frame.rbbasket ,variable=rbbas.value,text='市价',value="2")#,state='normal')
rbbas.most <- tkradiobutton(frame.rbbasket ,variable=rbbas.value,text='涨/跌停价',value="3")#,state='normal' )
tkgrid(rbbas.add ,sticky="w");

basketadd.value <- tclVar("basketaddvalue")
tclvalue(basketadd.value ) <-1;
entry.basketadd <-tkentry(frame.rbbasket ,width="5",textvariable=basketadd.value )
label.basketadd<-tklabel(frame.rbbasket ,text="价位");
tkgrid(entry.basketadd,label.basketadd,padx=2,sticky='we')
tkgrid.configure(label.basketadd,sticky='w')
tkgrid(rbbas.buy1 ,sticky="w");
tkgrid(rbbas.last ,sticky="w");
tkgrid(rbbas.most,sticky="w" );

button.basketsel <- tkbutton(frame.basketsel, text = "导入篮子", command = PressedImportBasket )

label.basketsel<-tklabel(frame.basketsel,text='价格策略:');
tkplace(button.basketsel ,x=5,y=0,width=120,height=20);
tkplace(label.basketsel,x=0,y=20,height=18);
tkplace(frame.rbbasket ,x=0,y=38,width=130,height=120);
tkplace(frame.basketsel,x=0,y=140,width=130,height=158);


##以下篮子表格
#Code<-c('600000.sh','000001.sz','600177.sh');
#TradeSide<-c('buy','buy','sell');
#Weight<-c('100','100','100');
#Basket<-data.frame(Code=Code,TradeSide=TradeSide,Weight=Weight)

tclName.basketArr<-'TCLBasket';

.Tcl(paste("set ",tclName.basketArr,"(0,0) \"#\"",sep=""))
.Tcl(paste("set ",tclName.basketArr,"(0,1) \"证券代码\"",sep=""))
.Tcl(paste("set ",tclName.basketArr,"(0,2) \"证券名称\"",sep=""))
.Tcl(paste("set ",tclName.basketArr,"(0,3) \"买卖方向\"",sep=""))
.Tcl(paste("set ",tclName.basketArr,"(0,4) \"数量(股/比例)\"",sep=""))
.Tcl(paste("set ",tclName.basketArr,"(0,5) \"可交易量\"",sep=""))

frame.tbbasket<- tkframe(frameOverall,width=740)
table.basket<- tkwidget(frame.tbbasket,"table",variable=tclName.basketArr,cols="6",titlerows="1"
                    ,titlecols="1",selectmode="extended",background="white"
                    ,xscrollcommand=function(...) tkset(xscr.basket,...),yscrollcommand=function(...) tkset(yscr.basket,...)
                    ,height=148,rows=1,colstretchmode="unset"
                    ,selecttype='row',state='disabled'
                    )

xscr.basket<-tkscrollbar(frame.tbbasket,orient="horizontal", command=function(...)tkxview(table.basket,...))
yscr.basket<- tkscrollbar(frame.tbbasket,command=function(...)tkyview(table.basket,...))

#tkplace(tklabel(frame.status,text="状态："),x=0,y=0,width=60);
tkplace(table.basket,x=0,y=0,width=590,height=128)
tkplace(yscr.basket,x=590,y=0,width=20,height=128)
tkplace(xscr.basket,x=0,y=128,width=610,height=20)
tkplace(frame.tbbasket,x=130,y=150,width=610,height=148);

##以下数量策略界面
frame.Topvolume<- tkframe(frameOverall,width=740)
frame.volume<- tkframe(frame.Topvolume,relief="groove",borderwidth=2,width=680)
rbvolume.value <- tclVar("ordervolume")
tclvalue(rbvolume.value) <-"0";

rbvolume.samestock <- tkradiobutton(frame.volume,variable=rbvolume.value,text='每账户数量相同',value="0")#,state='normal')
rbvolume.single <- tkradiobutton(frame.volume,variable=rbvolume.value,text='一个品种一个账号',value="1")
rbvolume.totalasset <- tkradiobutton(frame.volume,variable=rbvolume.value,text='按总资产比例分配',value="2")#,state='disabled')
rbvolume.valueasset <- tkradiobutton(frame.volume,variable=rbvolume.value,text='按可用资产比例分配',value="3")#,state='disabled')

tkgrid(rbvolume.samestock,rbvolume.single ,rbvolume.totalasset ,rbvolume.valueasset ,padx=2,sticky='w')


frame.randvalues <- tkframe(frame.volume)
rbvolume.rand <- tkradiobutton(frame.randvalues,variable=rbvolume.value,text='随机分配：最小',value="4")#,state='disabled')
rbvolumemax.value <- tclVar("rbvolumemaxvalue")
rbvolumemin.value <- tclVar("rbvolumeminvalue")
tclvalue(rbvolumemin.value ) <-1;
tclvalue(rbvolumemax.value ) <-9999999;
entry.rbvolumemin<-tkentry(frame.randvalues ,width="7",textvariable=rbvolumemin.value )
entry.rbvolumemax<-tkentry(frame.randvalues ,width="7",textvariable=rbvolumemax.value )
label.rbvolumemiddle<-tklabel(frame.randvalues ,text="手,最大");
label.rbvolumemax<-tklabel(frame.randvalues ,text="手");
tkgrid(rbvolume.rand,entry.rbvolumemin,label.rbvolumemiddle,entry.rbvolumemax,label.rbvolumemax,padx=1,sticky='we')

cksplitorder.value <- tclVar("cksplitorder")#拆单按钮选择值
cksplitordermin.value <- tclVar("cksplitorderminvalue")
cksplitordermax.value <- tclVar("cksplitordermaxvalue")
tclvalue(cksplitorder.value ) <-0;
tclvalue(cksplitordermin.value ) <-1;
tclvalue(cksplitordermax.value ) <-9999999;

frame.splitorder <- tkframe(frame.volume)#拆单按钮输入框需要的frame
cksplitorder<-tkcheckbutton(frame.splitorder,text='拆单：最小',variable=cksplitorder.value);
entry.cksplitordermin<-tkentry(frame.splitorder ,width="7",textvariable=cksplitordermin.value )
entry.cksplitordermax<-tkentry(frame.splitorder ,width="7",textvariable=cksplitordermax.value )
label.cksplitordermiddle<-tklabel(frame.splitorder ,text="手,最大");
label.cksplitordermax<-tklabel(frame.splitorder ,text="手");
tkgrid(cksplitorder,entry.cksplitordermin,label.cksplitordermiddle,entry.cksplitordermax,label.cksplitordermax,padx=1,sticky='we')

tkgrid(frame.randvalues,frame.splitorder,columnspan=2,padx=2,sticky='we')

#tkgrid.configure(frame.randvalues,columnspan=2);

label.rbvolume<-tklabel(frame.Topvolume,text='数量策略:');
tkplace(label.rbvolume,x=0,y=0);
tkplace(frame.volume,x=60,y=0,width=680);
tkplace(frame.Topvolume,x=0,y=300,width=740,height=50);


##以下下单总量控制
frame.orderamount<- tkframe(frameOverall,width=740)
frame.raorderamount<- tkframe(frame.orderamount,relief="groove",borderwidth=2,width=680)
frame.capitalamount<- tkframe(frame.raorderamount)
frame.ordermultiply<- tkframe(frame.raorderamount)

rborderamount.value <- tclVar("rborderamount")
tclvalue(rborderamount.value) <-"1";

rbordercap.value <- tclVar("ordercapitalamount")
tclvalue(rbordercap.value) <-"0";
rbordermul.value <- tclVar("orderamountmultiply")
tclvalue(rbordermul.value) <-"0";

rborder.cap<- tkradiobutton(frame.capitalamount,variable=rborderamount.value,text='总金额(按委托比例)',value="0")#,state='disabled'
rborder.mul<- tkradiobutton(frame.ordermultiply,variable=rborderamount.value,text='按委托数量倍数*',value="1")#,state='normal')
rborder.clear<-tkradiobutton(frame.raorderamount,variable=rborderamount.value,text='清空篮子内证券的仓位',value="2")#,state='normal')

entry.rbordercap<-tkentry(frame.capitalamount,width="10",textvariable=rbordercap.value )
entry.rbordermul<-tkentry(frame.ordermultiply,width="10",textvariable=rbordermul.value )
label.money<-tklabel(frame.capitalamount,text="元");

tkgrid(rborder.cap,entry.rbordercap,label.money,padx=2,sticky='w')
tkgrid(rborder.mul,entry.rbordermul,padx=2,sticky='w')
#tkgrid.configure(frame.capitalamount,frame.ordermultiply,sticky='we');
tkgrid(frame.capitalamount,frame.ordermultiply,rborder.clear,sticky='we');

label.orderamount<-tklabel(frame.orderamount,text='下单总量:');
tkplace(label.orderamount,x=0,y=0);
tkplace(frame.raorderamount,x=60,y=0,width=680);
tkplace(frame.orderamount,x=0,y=350,width=740,height=40);

###########################################################
###以下按钮
frame.buttons<- tkframe(frameOverall ,relief="groove",borderwidth=2,width=130)
btn.order <- tkbutton(frame.buttons, text = "执行下单", command = PressedExecOrder)
btn.queryorder <- tkbutton(frame.buttons, text = "查询下单结果", command = PressedQueryOrder)
btn.queryposition <- tkbutton(frame.buttons, text = "查询持仓", command = PressedQueryPosition)
btn.cancelorder <- tkbutton(frame.buttons, text = "全部撤单", command = PressedCancelOrder)
btn.repairorder <- tkbutton(frame.buttons, text = "补单",state='disabled')#, command = PressedOK)
btn.clearposition <- tkbutton(frame.buttons, text = "全部清仓", command = Pressedclearposition)

tkgrid(btn.order,padx=10,sticky='we',ipadx=15,pady=4);
tkgrid(btn.queryorder,padx=10,sticky='we',ipadx=15,pady=4);
tkgrid(btn.queryposition,padx=10,sticky='we',ipadx=15,pady=4);
tkgrid(btn.cancelorder,padx=10,sticky='we',ipadx=15,pady=4);
tkgrid(btn.repairorder ,padx=10,sticky='we',ipadx=15,pady=4);
tkgrid(btn.clearposition ,padx=10,sticky='we',ipadx=15,pady=4);

#tkgrid.configure(btn.repairorder ,sticky='wens',ipadx=15)

tkplace(frame.buttons,x=0,y=390,width=130,height=210);

label.resultlabel<-tklabel(frameOverall,text='执行结果:');
tkplace(label.resultlabel,x=130,y=390,width=90,height=18);


tclName.ExeResults<-'TCLExeResults';

.Tcl(paste("set ",tclName.ExeResults,"(0,0) \"#\"",sep=""))
.Tcl(paste("set ",tclName.ExeResults,"(0,1) \"\"",sep=""))
.Tcl(paste("set ",tclName.ExeResults,"(0,2) \"\"",sep=""))
.Tcl(paste("set ",tclName.ExeResults,"(0,3) \"\"",sep=""))
.Tcl(paste("set ",tclName.ExeResults,"(0,4) \"\"",sep=""))
.Tcl(paste("set ",tclName.ExeResults,"(0,5) \"\"",sep=""))
#.Tcl(paste("set ",tclName.ExeResults,"(0,6) \"\"",sep=""))

frame.ExeResults<- tkframe(frameOverall ,width=610)#,relief="groove",borderwidth=2
table.ExeResults <- tkwidget(frame.ExeResults,"table",variable=tclName.ExeResults,cols="6",titlerows="1"
                    ,titlecols="1",selectmode="extended",background="white"
                    ,xscrollcommand=function(...) tkset(xscr.ExeResults ,...),yscrollcommand=function(...) tkset(yscr.ExeResults ,...)
                    ,height=140,rows=1,colstretchmode="unset"
			  						,selecttype='row',state='disabled'
                    )

xscr.ExeResults <-tkscrollbar(frame.ExeResults,orient="horizontal", command=function(...)tkxview(table.ExeResults ,...))
yscr.ExeResults <- tkscrollbar(frame.ExeResults,command=function(...)tkyview(table.ExeResults ,...))

tkplace(table.ExeResults,x=0,y=0,width=590,height=170)
tkplace(yscr.ExeResults,x=590,y=0,width=20,height=170)
tkplace(xscr.ExeResults,x=0,y=170,width=610,height=20)
tkplace(frame.ExeResults,x=130,y=410,width=610,height=190);
######################################################
