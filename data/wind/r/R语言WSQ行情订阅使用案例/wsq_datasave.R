# wsq行情订阅使用案例
# 说明：
# 该案例是演示wsq实时行情订阅的使用，订阅模式主要由两部分组成，一部分是用wsq函数订阅所需要的行情，
# 另一部分是编写自己的回调函数，用于处理实时推送过来的行情数据
# myCallback<-function(out) 即为本案例所使用的回调函数，回调函数有且只能有一个参数：out
# out的数据结构如下：
# out$Data 存放行情数据
# out$Field 存放行情数据对应的指标
# out$Code 存放行情对应的code
# out$Time 存放本地时间，注意这个不是行情对应的时间，要获取行情对应的时间，请订阅rt_time指标
# out$RequestID 存放对应wsq请求的RequestID
# out$RequestState 状态字段，使用时无需处理
# out$ErrorCode 错误码，如果为0表示运行正常

# 取消订阅可使用w.cancelRequest(requestID),如果想取消全部订阅，可使用w.cancelRequest(0)

library(WindR)
w.start(0,F);

logfile<-file("c:\\R2wsqdataif.data", "w")
begintime=0;
sscount =0;

#用于处理行情的回调函数
myCallback<-function(out)
{
    if(out$ErrorCode){#如果ErrorCode不为0，表明有错误发生
      cat("Error\n",file=logfile);
        return ();
    }
    
    if(any(out$Field=="RT_TIME"))
    {
            begintime <<- out$Data[out$Field=="RT_TIME"];
    }
    
     cat(begintime,file=logfile);
     cat(begintime);

    if(any(out$Field=="RT_LAST"))
    {
      v = out$Data[out$Field=="RT_LAST"];
      cat(" ",file=logfile);
      cat(v,file=logfile);
      
      cat(" ");
      cat(v);
    }
    cat("\n",file=logfile);
    sscount <<- sscount+1;
    cat("------");
    cat(sscount);
    cat("\n");
}


#订阅行情
w.wsq("SPTAUUSDOZ.IDC","rt_time,rt_last",func=myCallback)