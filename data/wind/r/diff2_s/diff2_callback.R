#在回调函数中进行交易

require(WindR)

init_data<-function(code1,code2,gate1b,gate1c,gate2b,gate2c)
{
  out<-list();
  out$RequestID <- 0;
  
  out$child1 <- list();
  out$child1$CODE=toupper(code1);
  out$child1$RT_DATE=0;
  out$child1$RT_TIME=0;
  out$child1$RT_BSIZE1 =0;
  out$child1$RT_BID1 =0;
  out$child1$RT_ASK1 =0;
  out$child1$RT_ASIZE1 =0;
  
  out$child2 <- list();
  out$child2$CODE=toupper(code2);
  out$child2$RT_DATE=0;
  out$child2$RT_TIME=0;
  out$child2$RT_BSIZE1 =0;
  out$child2$RT_BID1 =0;
  out$child2$RT_ASK1 =0;
  out$child2$RT_ASIZE1 <- 0;

  
  out$gate1 <- c(gate1b,gate1c);
  out$gate2 <- c(gate2b,gate2c);
  
  out$lastTime <- Sys.time();
  out$printcount <- 0;
  out$curpos <- 0 ;

  return(out)
}

printdot<-function(sc)
{
   if(sc<80){cat('.');return(sc+1);}
   else{cat('\n');return (0);}
}
diffcallback<-function(data)
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
  
  if(length(data$Code)>2 )
  {
    return ();
  }
  
  updatename<-unlist(data$Field);
  if(data$Code[[1]]==gStockData$child1$CODE )
  {
  	gStockData$child1[updatename]<<- data$Data[,1,1];
  }else if(data$Code[[1]]==gStockData$child2$CODE )
  {
  	gStockData$child2[updatename]<<- data$Data[,1,1];
  }  
  if(length(data$Code)>1)
  {
	  if(data$Code[[2]]==gStockData$child1$CODE )
	  {
	  	gStockData$child1[updatename]<<- data$Data[,2,1];
	  }else if(data$Code[[2]]==gStockData$child2$CODE )
	  {
	  	gStockData$child2[updatename]<<- data$Data[,2,1];
	  }   
  }
  
  if( as.integer(gStockData$lastTime - Sys.time())>=-1 ){#不需要这么频繁
    gStockData$printcount <<- printdot(gStockData$printcount);
  	return();
  }
  
  a=Sys.time()
  gStockData$lastTime <<- a;
  nowdate=as.integer(format(a,'%Y%m%d'))
  nowtime=as.integer(format(a,'%H%M%S'))
  if(gStockData$child1$RT_DATE != nowdate || nowdate != gStockData$child1$RT_DATE )
  {
      print(nowdate);
      print('date is not same!');
      return();
   }
	
	diff1= gStockData$child1$RT_TIME - gStockData$child2$RT_TIME;
	diff2= gStockData$child1$RT_TIME - nowtime;

  if(diff1< -10000 || diff1>10000 || diff2< -200 || diff2>200 || nowtime<91515 || nowtime>151445 || (nowtime>112945 && nowtime<130000) )
  {
      print(nowtime);
      print('time is not right!');
      return();
  }  
  
  if1code<- gStockData$child1$CODE;
  if2code<- gStockData$child2$CODE;
  
  if(gStockData$curpos==0){#没有持仓
						if(gStockData$child1$RT_BID1 - gStockData$child2$RT_ASK1>gStockData$gate1[1]){#以买价卖出if1，以卖价买入if2
							  data<-w.torder(c(if1code,if2code),c('short','buy'),c(gStockData$child1$RT_BID1, gStockData$child2$RT_ASK1),c(1,1),logonid=logonid);
							  print(data);
							  gStockData$curpos <<- 1;
							  print(paste('开仓：short',if1code, 'at ', gStockData$child1$RT_BID1,', buy',if2code,'at', gStockData$child2$RT_ASK1));
		    		}
						if(gStockData$child2$RT_BID1 - gStockData$child1$RT_ASK1>gStockData$gate2[1]){#以买价卖出if2，以卖价买入if1
							  data<-w.torder(c(if2code,if1code),c('short','buy'),c(gStockData$child2$RT_BID1, gStockData$child1$RT_ASK1),c(1,1),logonid=logonid);
							  print(data);
							  print(paste('开仓：short',if2code, 'at ', gStockData$child2$RT_BID1,', buy',if1code,'at', gStockData$child1$RT_ASK1));
							  gStockData$curpos <<- -1;
		    		}
	 }else if(gStockData$curpos==1){#已经卖出if1，买入了if2，检查是不是要平仓
						if(gStockData$child1$RT_ASK1 - gStockData$child2$RT_BID1<gStockData$gate1[2]){#以卖价平空if1，以买价平多if2
								data<-w.torder(c(if1code,if2code),c('cover','sell'),c(gStockData$child1$RT_ASK1, gStockData$child2$RT_BID1),c(1,1),logonid=logonid);
								print(data);
								gStockData$curpos<<- 0;
								print(paste('平仓：cover',if1code, 'at ', gStockData$child1$RT_ASK1,', sell',if2code,'at', gStockData$child2$RT_BID1));
		    		}
	 }else  if(gStockData$curpos==-1){#已经卖出if2，买入了if1，检查是不是要平仓
						if(gStockData$child2$RT_ASK1 - gStockData$child1$RT_BID1<gStockData$gate2[2]){#以卖价平空if2，以买价平多if1
								data<-w.torder(c(if2code,if1code),c('cover','sell'),c(gStockData$child2$RT_ASK1, gStockData$child1$RT_BID1),c(1,1),logonid=logonid);
								print(data);
								gStockData$curpos<<- 0;
								print(paste('平仓：cover',if2code, 'at ', gStockData$child1$RT_ASK1,', sell',if1code,'at', gStockData$child2$RT_BID1));
		    		}
	}  
	
  gStockData$printcount <<- printdot(gStockData$printcount);
  return();
  
}
startrun<-function(code1="if1408.cfe",code2="if1409.cfe",gate1b=2,gate1c=1,gate2b=2,gate2c=1)
{
	library(WindR);
	gStockData<<-init_data(code1,code2,gate1b,gate1c,gate2b,gate2c)
  w.start(showmenu=FALSE);
  data<-w.tlogon('0000','0','w081263802','0000','cfe');#登录模拟交易
	logonid<<-data$Data$LogonID; #得到登录ID
	
  data<-w.wsq(c(gStockData$child1$CODE,gStockData$child2$CODE),"rt_date,rt_time,rt_bsize1,rt_bid1,rt_ask1,rt_asize1",func=diffcallback)
  if(data$ErrorCode!=0)
  {
    print("call wsq error!")
    return()
  }
  
  gStockData$RequestID<<-data$RequestID;
  print(gStockData$RequestID)
}
stoprun<-function()
{
  if(gStockData$RequestID[[1]]!=0)
    w.cancelRequest(gStockData$RequestID)
  gStockData$RequestID<<-0;
}

print('请输入startrun()运行，输入stoprun()停止');