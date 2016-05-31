function QA=QACustomStrategy(QA,varargin)
sqlquery='select stocklist.wind_code ,stocklist.sec_name from quantaxis.stocklist';
curs = fetch(exec(QA.INT_MYSQL.Conn,sqlquery));

QA.ACC.StockList=curs.Data;
QA.ACC_ID=1;

QA.ACC.Type='ts';
QA.ACC.StockId=char(QA.ACC.StockList(1,1));
notify(QA,'SQL')
QA.ACC.StockId=char(QA.ACC.StockList(2,1));
notify(QA,'SQL')

%% ACC_Methods

QA.ACC_Methods.AnalysisID=1;
QA.ACC_Methods.AnalysisName=QA.ACC.UseData{QA.ACC_Methods.AnalysisID,1};
QA.ACC_Methods.AnalysisData=QA.ACC.UseData{QA.ACC_Methods.AnalysisID,2};
QA.ACC_Methods.AnalysisObj=cell2mat(QA.ACC_Methods.AnalysisData(:,2));
testx=QA.ACC_Methods.AnalysisObj;
% hurst_origin=EstimateHurst(testx');
[modes,QA.ACC_Methods.ITS]=ceemdan(testx',0.2,500,5000);
le_modes=size(modes,1);
% totallvar=zeros(le_modes,1);
% totalstd=zeros(le_modes,1);
QA.ACC_Methods.SVRt=130;
% BESTYFITX=zeros(length(testx)-QA.ACC_Methods.SVRt,le_modes);
QA.ACC_Methods.HURST=zeros(le_modes,1);

for i=1:le_modes
    QA.ACC_Methods.HURST(i,1)=EstimateHurst(modes(i,:));
%     if QA.ACC_Methods.HURST(i,1)<0.5
%         QA.ACC_Methods.besthursti=i;
%         [arimapredict,~]=yuARIMA(modes(i,:)');
%         QA.ACC_Methods.ArimaPREDICT(:,i)=arimapredict(:,QA.ACC_Methods.SVRt+1:end)';
%     end
%     if QA.ACC_Methods.HURST(i,1)>=0.5
    [~,~,~,~,BESTYFIT,~,~]=findleastvarl(modes(i,:)',QA.ACC_Methods.SVRt);
    QA.ACC_Methods.SVRPREDICT(:,i)=BESTYFIT;
    
%    end
end

QA.ACC_Methods.Date=QA.ACC_Methods.AnalysisData(QA.ACC_Methods.SVRt+1:end,1);
QA.ACC_Methods.Predict=sum(QA.ACC_Methods.ArimaPREDICT,2)+sum(QA.ACC_Methods.SVRPREDICT,2);
QA.ACC_Methods.AnalysisObj=QA.ACC_Methods.AnalysisObj(QA.ACC_Methods.SVRt+1:end,1);

%% 分析结束 进入策略
for traid=6:size(QA.ACC_Methods.Predict,1)
    if QA.ACC_Methods.Predict(traid-5)>QA.ACC_Methods.AnalysisObj(traid-5) && ...
            QA.ACC_Methods.Predict(traid-4)>QA.ACC_Methods.AnalysisObj(traid-4) && ...
            QA.ACC_Methods.Predict(traid-3)>QA.ACC_Methods.AnalysisObj(traid-3) && ...
            QA.ACC_Methods.Predict(traid-2)>QA.ACC_Methods.AnalysisObj(traid-2) && ...
            QA.ACC_Methods.Predict(traid-1)>QA.ACC_Methods.AnalysisObj(traid-1)
        % buy
        QA.MES.Str=['Decision -- Buy',QA.ACC_Methods.AnalysisName];
        disp(QA.MES.Str)
        notify(QA,'MESSAGE')
         QA.TRA.id=QA.ACC_Methods.AnalysisName;
         QA.TRA.Date=QA.ACC_Methods.Date(traid);
         QA.TRA.Date=QA.TRA.Date{1,1};
         QA.TRA.Bid=QA.ACC_Methods.AnalysisObj(traid);
         QA.TRA.Amount=100000;
         QA.TRA.Position=-1;
        notify(QA,'TRADE')
    end
    if QA.ACC_Methods.Predict(traid-5)<QA.ACC_Methods.AnalysisObj(traid-5) && ...
            QA.ACC_Methods.Predict(traid-4)<QA.ACC_Methods.AnalysisObj(traid-4) && ...
            QA.ACC_Methods.Predict(traid-3)<QA.ACC_Methods.AnalysisObj(traid-3) && ...
            QA.ACC_Methods.Predict(traid-2)<QA.ACC_Methods.AnalysisObj(traid-2) && ...
            QA.ACC_Methods.Predict(traid-1)<QA.ACC_Methods.AnalysisObj(traid-1)
        % buy
        QA.MES.Str=['Decision -- Sell',QA.ACC_Methods.AnalysisName];
        disp(QA.MES.Str)
        notify(QA,'MESSAGE')
         QA.TRA.id=QA.ACC_Methods.AnalysisName;
         QA.TRA.Date=QA.ACC_Methods.Date(traid);
         QA.TRA.Date=QA.TRA.Date{1,1};
         QA.TRA.Bid=QA.ACC_Methods.AnalysisObj(traid);
         QA.TRA.Amount=100000;
         QA.TRA.Position=1;
        notify(QA,'TRADE')
    end
    
end
end