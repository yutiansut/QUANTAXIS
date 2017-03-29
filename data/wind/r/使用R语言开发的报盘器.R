# w.wsq+w.wss + callback demo
# Honghai Zhu 2013
#

require(WindR)
require(graphics)


drawaxs<-function()
{
  global.oldbg<<-par("bg")
  global.oldfg<<-par("fg")
  
  global.oldplt<<-par("plt")
  global.oldpin<<-par("pin")
  global.oldcol<<-par("col")
  global.oldps<<-par("ps")  
  
  par(col="#777777",bg="black",fg="white",plt=c(0.005,0.995,0.005,0.995))
  par(pin=c(4,5),ps=12)
  
  plot.new()
  plot(c(0,400),c(0,500),xlab="",ylab="",xaxt="n",yaxt="n",type="n",asp=1,xaxs="i",yaxs="i")  
}

drawbg<-function()
{
  rect(0,0,400,500,col="black")
  y=5;
  #text(10,y,labels="High",adj=c(0,0))
  #text(190,y,labels="10.04",adj=c(1,0))
  #text(210,y,labels="LOW",adj=c(0,0))
  #text(390,y,labels="9.84",adj=c(1,0))
  
  xlabel=c(10,210)
  deltay=25;
  ybase=5
  #text(xlabel,rep(ybase,2),c("High","Low"),adj=c(0,0))
  
  text(rep(xlabel,6),ybase+rep(0:5,each=2)*deltay,
       c("HIGH","LOW","Avg Price","Open","Total","Amplitude","OutSize","InSize"
         ,"Current Lots","Vol. Ratio","Total Lots","Turnover"
         ),adj=c(0,0))
  #text(rep(xlabel,6),ybase+rep(0:5,each=2)*deltay,
  #     c("最高","最低","均价","开盘","总额","振幅","外盘","内盘"
  #       ,"现手","量比","总手","换手"
  #     ),adj=c(0,0))
  
  
  ybase<-ybase+6*deltay;
  
  
  #rect(0,0+1,100,100,col='blue')
  lines(c(1,400),c(ybase-5,ybase-5),col="#808080")
  text(rep(10,10),ybase+(0:9)*deltay,c("Bid 5","Bid 4","Bid 3","Bid 2","Bid 1"
                                       ,"Ask 1","Ask 2","Ask 3","Ask 4","Ask 5")
       ,adj=c(0,0))
  #text(rep(10,10),ybase+(0:9)*deltay,c("买五","买四","买三","买二","买一"
  #                                     ,"卖一","卖二","卖三","卖四","卖五")
  #     ,adj=c(0,0))
  lines(c(1,400),c(ybase+5*deltay-5,ybase+5*deltay-5),col="#808080")
  ybase<-ybase+10*deltay;
  lines(c(1,400),c(ybase-5,ybase-5),col="#808080")
  
  #par(bg=oldbg,ps=oldps,col=oldcol)
  #par(fg=oldfg)
  #par(pin=oldpin,plt=oldplt)
}

getnamebycode<-function(code)
{
  data<-w.wss(code,"sec_name")
  if(data$ErrorCode==0)
    return (as.character(data$Data$SEC_NAME[[1]]))
  else
    return (NULL)
}
init_data<-function(code)
{
  out<-list();
  out$RequestID=0;
  out$CODE=code;
  out$SEC_NAME=getnamebycode(code);
  out$RT_HIGH=NA;
  out$RT_LOW=NA
  out$RT_VWAP=NA
  out$RT_OPEN=NA
  out$RT_AMT=NA
  out$RT_SWING=NA
  out$RT_UPWARD_VOL=NA
  out$RT_DOWNWARD_VOL=NA
  out$RT_LAST_VOL=NA
  out$RT_VOL_RATIO=NA
  out$RT_VOL=NA
  out$RT_TURN=NA
  out$RT_BSIZE5=NA
  out$RT_BSIZE4=NA
  out$RT_BSIZE3=NA
  out$RT_BSIZE2=NA
  out$RT_BSIZE1 =NA
  out$RT_BID5 =NA
  out$RT_BID4 =NA
  out$RT_BID3 =NA
  out$RT_BID2=NA
  out$RT_BID1 =NA
  out$RT_ASK5 =NA
  out$RT_ASK4 =NA
  out$RT_ASK3 =NA
  out$RT_ASK2 =NA
  out$RT_ASK1 =NA
  out$RT_ASIZE5 =NA
  out$RT_ASIZE4 =NA
  out$RT_ASIZE3 =NA
  out$RT_ASIZE2 =NA
  out$RT_ASIZE1 =NA
  out$RT_LAST=NA
  out$RT_PRE_CLOSE =NA
  out$RT_CHG =NA
  out$RT_PCT_CHG=NA
  return(out)
}

#gStockData<-init_data()

wsqcallback<-function(data)
{
  #  data包含如下信息
  #  $RequestID 订阅请求ID 
  #  $Field 数据中对应的指标名
  #  $Code 数据中对应的代码 
  #  $Time 返回数据对应的时间.
  #  $ErrorCode   函数运行的错误ID.
  #  $Data   返回的数据结果, 为三维数组,对应指标Field、代码Code、时间Time三个维度    
  if(data$ErrorCode!=0)
  {
    return()
  }
  #if(data$RequestID!=gStockData$RequestID)
  #{
  #  return();
  #}
  
  if(length(data$Code)!=1 || data$Code[[1]]!=gStockData$CODE)
  {
    return ();
  }
  
  updatename<-unlist(data$Field);
  gStockData[updatename]<<-unlist(data$Data)
  
  fname=c("RT_VOL","RT_UPWARD_VOL","RT_DOWNWARD_VOL","RT_LAST_VOL",
          "RT_ASIZE5","RT_ASIZE4","RT_ASIZE3","RT_ASIZE2","RT_ASIZE1",
          "RT_BSIZE5","RT_BSIZE4","RT_BSIZE3","RT_BSIZE2","RT_BSIZE1"
          );
  for(nn in updatename){
    
      if(any(nn==fname)>0){
        gStockData[[nn]]<<-gStockData[[nn]]/100
      }
  }
  
  if(any("RT_AMT"==updatename)>0)
    gStockData[["RT_AMT"]]<<-gStockData[["RT_AMT"]]/10000

  #.........draw.........
  drawbg()
  drawvalues()
  #print(data)
  print("update...")
}
startwsq<-function()
{
  data<-w.wsq(gStockData$CODE,"rt_high,rt_low,rt_vwap,rt_open,rt_amt,rt_swing,rt_upward_vol,rt_downward_vol,rt_last_vol,rt_vol_ratio,rt_vol,rt_turn,rt_bsize5,rt_bsize4,rt_bsize3,rt_bsize2,rt_bsize1,rt_bid5,rt_bid4,rt_bid3,rt_bid2,rt_bid1,rt_ask5,rt_ask4,rt_ask3,rt_ask2,rt_ask1,rt_asize5,rt_asize4,rt_asize3,rt_asize2,rt_asize1,rt_last,rt_pre_close,rt_chg,rt_pct_chg"
                         ,func=wsqcallback)
  if(data$ErrorCode!=0)
  {
    print("call wsq error!")
    return()
  }
  
  gStockData$RequestID<<-data$RequestID;
  print(gStockData$RequestID)
}
stopwsq<-function()
{
  if(gStockData$RequestID[[1]]!=0)
    w.cancelRequest(gStockData$RequestID)
  gStockData$RequestID<<-0;
}

getPriceColor<-function(v)
{
  if(v>gStockData$RT_PRE_CLOSE+0.00001)  return("red")
  if(v<gStockData$RT_PRE_CLOSE-0.00001)  return("green")
  
  return("white")
}
drawYellowInt<-function(v,x,y,ps=12,adj=c(1,0),col="yellow")
{
  oldps=par("ps")
  par(ps=ps)
  for(i in 1:length(v))
    if(!is.na(v[[i]]))
      text(x[[i]],y[[i]],labels=format(v[[i]],digits=3,nsmall=0),adj=adj,col=col,ps=ps)
  par(ps=oldps)
  
}

drawYellow4<-function(v,x,y,ps=12,adj=c(1,0),col="yellow")
{
  oldps=par("ps")
  par(ps=ps)
  for(i in 1:length(v))
    if(!is.na(v[[i]]))
      text(x[[i]],y[[i]],labels=format(v[[i]],digits=3,nsmall=4,scientific=FALSE),adj=adj,col=col,ps=ps)
  par(ps=oldps)
  
}

drawPercentValue<-function(v,x,y,ps=12,adj=c(1,0),col="yellow")
{
  oldps=par("ps")
  par(ps=ps)  
  for(i in 1:length(v))
  {
    if(!is.na(v[[i]]))
    {
      label<-sprintf("%0.2f%%",v[[i]]*100)
      text(x[[i]],y[[i]],labels=label,adj=adj,col=col,ps=ps)
    }
  }
  par(ps=oldps)  
}
drawPriceValue<-function(v,x,y,ps=12,adj=c(1,0))
{
  for(i in 1:length(v))
  if(!is.na(v[[i]]))
    text(x[[i]],y[[i]],labels=format(v[[i]],digits=1,nsmall=2),adj=adj,col=getPriceColor(v[[i]]),ps=ps)
}
drawvalues<-function()
{
  y=5;
  #text(10,y,labels="High",adj=c(0,0))
  #text(190,y,labels="10.04",adj=c(1,0))
  #text(210,y,labels="LOW",adj=c(0,0))
  #text(390,y,labels="9.84",adj=c(1,0))
  
  xlabel=c(190,390)
  dy=25;
  yb=5
  x1=190;x2=390
  y=yb;
  
  drawPriceValue(gStockData[c("RT_HIGH","RT_LOW","RT_VWAP","RT_OPEN")]
                 ,c(x1,x2,x1,x2),c(y,y,y+dy,y+dy))
  x1=200;
  y=yb+6*dy;
  drawPriceValue(gStockData[c("RT_BID5","RT_BID4","RT_BID3","RT_BID2","RT_BID1"
                            ,"RT_ASK1","RT_ASK2","RT_ASK3","RT_ASK4","RT_ASK5"
                            )]
  ,rep(x1,10),0:9*dy+y,adj=c(0,0))


  drawYellowInt(gStockData[c("RT_BSIZE5","RT_BSIZE4","RT_BSIZE3","RT_BSIZE2","RT_BSIZE1"
                             ,"RT_ASIZE1","RT_ASIZE2","RT_ASIZE3","RT_ASIZE4","RT_ASIZE5"
  )]
                ,rep(x2,10),0:9*dy+y)

  
  x1=190
  y=yb+dy*2;
  drawYellowInt(gStockData[c("RT_AMT","RT_UPWARD_VOL","RT_DOWNWARD_VOL","RT_LAST_VOL"
                             ,"RT_VOL_RATIO","RT_VOL"
  )]
                ,c(x1,x1,x2,x1,x2,x1),c(0,1,1,2,2,3)*dy+y)
  
  drawPercentValue(gStockData[c("RT_SWING","RT_TURN")]
  ,c(x2,x2),c(0,3)*dy+y)
  
  y=yb+dy*16
  drawPercentValue(gStockData["RT_PCT_CHG"]
                    ,x2,y,col=getPriceColor(gStockData["RT_LAST"]),ps=16)
  
  drawYellow4(gStockData["RT_CHG"]
                ,x2,y+dy,col=getPriceColor(gStockData["RT_LAST"]),ps=16)
  
  drawYellow4(gStockData["RT_LAST"]
                ,10,y,adj=c(0,0),col=getPriceColor(gStockData["RT_LAST"]),ps=26)  
  
  oldps=par("ps")
  par(ps=26)
  text(10,y+dy*2,labels=gStockData$SEC_NAME,adj=c(0,0),col="yellow")
  #strsplit(gStockData$CODE,"\\.")
  text(390,y+dy*2,labels=strsplit(gStockData$CODE,"\\.")[[1]][[1]],adj=c(1,0),col="yellow")
  par(ps=oldps)
}

#code must be a stock
testrealtime<-function(code)
{
  drawaxs();
  gStockData<<-init_data(code)
  startwsq()

  drawbg()
  drawvalues() 
}

#code must be a stock
dotest<-function(code="600000.SH")
{
  w.start(showmenu=FALSE);
  testrealtime(code)
  print("stopwsq() to stop...")
}
dotest();