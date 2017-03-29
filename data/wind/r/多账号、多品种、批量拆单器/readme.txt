该案例是一个能够把一篮子股票、期货拆成小单、分配给多个账号，然后进行下单的工具。


程序基于WindR开发。

账户要先使用w.tlogon登陆，多个账号则登陆多次；篮子则用Basket<-data.frame方式赋值。

如下：

library(WindR)
w.start(0,F);
w.tlogon('0000',0,c('w081263801','w081263802'),0,c('sh','cfe'));

Code<-c('600000.sh','600177.sh','IF1412.CFE','TF1412.CFE');
TradeSide<-c('buy','buy','buy','short');
Weight<-c(100,100,1,1);
Basket<-data.frame(Code=Code,TradeSide=TradeSide,Weight=Weight,stringsAsFactors = FALSE)

免责声明：
       该应用案例仅供参考，任何人因使用本案例而产生的风险及损失由使用者自行承担，应用案例提供者不负任何责任。