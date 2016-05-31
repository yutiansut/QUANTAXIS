obj=yutiansutQUANTAXIS();

obj.StockCode='600215';
obj.BeginDate='20040101';
obj.EndDate='20160228';
obj.StockID=2;
obj.SendMail=1;
obj.Filing=1;
obj.Analysis.id=1;
obj.Analysis.Strategy='Self';
notify(obj,'AnalysisState')
obj.tmun=2800;
obj.BatNum=1000;
obj.TargetAddress='yutiansut@qq.com';
obj.CEEMDAN_ID=3;


[StockTick,Header,StatusStr]=obj.StockTick();
obj.StockTSDay();
[obj,InitialDate] = obj.Index();
obj.GetCons();
[NoticeDataCell] =obj.StockNotice();
[SaveLog,ProbList,NewList] = obj.SaveStockTSDay();
obj.Bat();


%%策略文件以调用非类文件中的函数
toc;