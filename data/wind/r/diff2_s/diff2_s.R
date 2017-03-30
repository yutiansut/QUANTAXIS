
if1code='IF1408.CFE'  #代码
if2code='IF1409.CFE'
gate1b=2;gate1c=1; gate2b=2;gate2c=1;

library(WindR)  #装载WindR
w.start(0,F);   #启动WindR
data<-w.tlogon('0000','0','w081263802','0000','cfe');#登录模拟交易
logonid=data$Data$LogonID; #得到登录ID

curpos=0;   #当前仓位状态
printcount=0;
while(TRUE)
{
		wsqout<-w.wsq(paste(if1code,if2code,sep=','),"rt_bid1,rt_ask1")
    if(wsqout$ErrorCode!=0)
    {
        print(wsqout);
        Sys.sleep(1);
        next;
    }
		data<-wsqout$Data;#取到的当前价格信息

    if(curpos==0){#没有持仓
				if(data$RT_BID1[1] - data$RT_ASK1[2]>gate1b){#以买价卖出if1，以卖价买入if2
					  w.torder(c(if1code,if2code),c('short','buy'),c(data$RT_BID1[1], data$RT_ASK1[2]),c(1,1),logonid=logonid);
					  curpos = 1;
					  print(paste('开仓：short',if1code, 'at ', data$RT_BID1[1],', buy',if2code,'at', data$RT_ASK1[2]));
    		}
				if(data$RT_BID1[2] - data$RT_ASK1[1]>gate2b){#以买价卖出if2，以卖价买入if1
					  w.torder(c(if2code,if1code),c('short','buy'),c(data$RT_BID1[2], data$RT_ASK1[1]),c(1,1),logonid=logonid);
					  print(paste('开仓：short',if2code, 'at ', data$RT_BID1[2],', buy',if1code,'at', data$RT_ASK1[1]));
					  curpos = -1;
    		}
		}else if(curpos==1){#已经卖出if1，买入了if2，检查是不是要平仓
				if(data$RT_ASK1[1] - data$RT_BID1[2]<gate1c){#以卖价平空if1，以买价平多if2
						w.torder(c(if1code,if2code),c('cover','sell'),c(data$RT_ASK1[1], data$RT_BID1[2]),c(1,1),logonid=logonid);
						curpos= 0;
						print(paste('平仓：cover',if1code, 'at ', data$RT_ASK1[1],', sell',if2code,'at', data$RT_BID1[2]));
    		}
    }else  if(curpos==-1){#已经卖出if2，买入了if1，检查是不是要平仓
				if(data$RT_ASK1[2] - data$RT_BID1[1]<gate2c){#以卖价平空if2，以买价平多if1
						w.torder(c(if2code,if1code),c('cover','sell'),c(data$RT_ASK1[2], data$RT_BID1[1]),c(1,1),logonid=logonid);
						curpos= 0;
						print(paste('平仓：cover',if2code, 'at ', data$RT_ASK1[1],', sell',if1code,'at', data$RT_BID1[2]));
    		}
    }
    printcount = printcount+1;
		if(printcount>80)
		{
			cat('\n');
			cat(paste('price=[',data$RT_BID1[1],data$RT_BID1[2],data$RT_ASK1[1],data$RT_ASK1[2],']'));
			printcount = 0;
		}else cat('.');
    Sys.sleep(1);
}