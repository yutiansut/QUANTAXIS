disp('Using Corr Strategy')
sqlquery='select `wind_code` from `stocklist`';
cursor=fetch(exec(QA.INT_MYSQL.Conn,sqlquery));
QA.Custom.Fetch.Stocklist.data=cursor.Data;
QA.Custom.Fetch.Stocklist.length=size(QA.Custom.Fetch.Stocklist.data,1);

sqlquery='select `DATE` from `000001_ts`';
cursor=fetch(exec(QA.INT_MYSQL.Conn,sqlquery));
QA.Custom.Fetch.Date.data=cursor.Data;
QA.Custom.Fetch.Date.length=size(QA.Custom.Fetch.Date.data,1);
QA.Custom.Strategy.corraccumulate=zeros(QA.Custom.Fetch.Stocklist.length,QA.Custom.Fetch.Stocklist.length);
sqlquery='SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = "quantaxis" and TABLE_NAME like "%ts"';
curs=fetch(exec(QA.INT_MYSQL.Conn,sqlquery));
QA.Custom.Fetch.tstable=curs.Data;
tic
for k=1:15
    xxx=tic;
    QA.Custom.Strategy.dateinit(:,k)=1500+unidrnd(QA.Custom.Fetch.Date.length-2001);
    QA.Custom.Strategy.dateinitx=QA.Custom.Fetch.Date.data{QA.Custom.Strategy.dateinit(:,k),1};
    
    for i=1:size(QA.Custom.Fetch.tstable,1)
        QA.Custom.Fetch.tstablename=QA.Custom.Fetch.tstable{i,1};
        sqlquery=['SELECT CLOSE FROM ',QA.Custom.Fetch.tstablename,' where DATE>',num2str(QA.Custom.Strategy.dateinitx),' LIMIT 0,200'];
        curs=fetch(exec(QA.INT_MYSQL.Conn,sqlquery));  %%
        QA.Custom.Strategy.data100(:,i)=curs.Data;
    end
    
    QA.Custom.Strategy.corrcoef{k,1}=corrcoef(cell2mat(QA.Custom.Strategy.data100));
    
    %%
    x=QA.Custom.Strategy.corrcoef{k,1};
    for i=1:QA.Custom.Fetch.Stocklist.length
        for j=1:QA.Custom.Fetch.Stocklist.length
            if i<=j
                x(i,j)=0;
            end    
        end
    end
    for j=1:550
        [a,b]=find(x==max(max(x)));
        QA.Custom.BestPotiflo(2*k-1,j)=a(1);
        QA.Custom.BestPotiflo(2*k,j)=b(1);
        QA.Custom.BestPotiflox(k,j)=x(a(1),b(1));
        
        for i=1:length(a)
            x(a(i),b(i))=0;
            x(b(i),a(i))=0;
        end   
    end
    ll=toc(xxx);
    disp(num2str(ll));
    clear QA.Custom.Strategy
    str=['循环已经进行到第',num2str(k),'单次循环耗时',num2str(ll)];
    MatlabSendMail(str,str)
    
end
clear QA.Custom.Strategy
toc
for l=1:k
    scatter(QA.Custom.BestPotiflo(2*l-1,:),QA.Custom.BestPotiflo(2*l,:))
    hold on
end


bestpot=zeros(30,550);
for i=1:30
   bestpot(1,1+550*(i-1):550*i)=BestPotiflo(2i-1,1:550);
end
 






