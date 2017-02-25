#该案例用于获取中证500成分股最近3年的半小时分钟数据，并保存到csv文件中
#请在使用前，先在D盘下建立名为“wsi_data”的文件夹
library(WindR);
w.start();

#获取中证500指数成分股
w_wset_data<-w.wset('sectorconstituent','date=20160317;windcode=000905.SH');
A_stcok_code<-w_wset_data$Data[,'wind_code'];

#循环获取每只股票的分钟数据
code_length<-length(A_stcok_code);
for(i in 1:code_length){
  code<-A_stcok_code[i];
  print(code);
  
  #调用Wind API接口获取分钟数据
  start_datetime<-"2013-05-01 09:00:00";
  end_datetime<-"2016-03-16 15:00:00";
  w_wsi_data<-w.wsi(code,"open,high,low,close,volume,amt,chg,pct_chg",start_datetime,end_datetime,"BarSize=30")
  
  #保存数据
  data_df<-data.frame(w_wsi_data);
  filepath<-paste('D:/wsi_data/wsi_data_',code,'.csv',sep="");
  write.table(data_df,filepath)
}  