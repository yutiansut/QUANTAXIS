classdef QUANTAXIS<handle
    % QUANTAXIS 2.0 alpha
    % by yutiansut
    % The Best Quantitative Toolbox Based on Matlab Ever
    % More Info: http://Quantaxis.yutiansut.com
    % recently QUANTAXIS 3.0 with QA Data Center
    properties
        w=windmatlab;
        % the fetch methods FET_
        FET %Struct
        %         FET.Data  FET.Codes  FET.Fields  FET.Times FET.Error Fet.Reqid
        FET_MYSQL
        FET_BAT
        %  DATA FILING  FIL_
        
        FIL
        %  Data Analysis ANA_
        ANA
        %   Account information ACC_
        ACC
        ACC_ID;
        ACC_Methods;
        ACC_Strategy;
        ACC_TotalAssest=1000000;
        ACC_Cash=1000000;  %initial cash
        ACC_Portfolio=0; %portfilio
        ACC_Trade;
        ACC_Trade_id=2;
        ACC_Amount=0;
        ACC_Account;
        ACC_Account_id=1;
        ACC_User;
        Custom;
        %  Message&Logs MES_
        MES
        MES_Str
        %  Evaluation EVA_
        EVA
        %  TRADING CORE TRA_
        TRA
        TRA_Id;
        
        %  System Message SYS_
        SYS
        %  Interaction INT_
        INT
        INT_MYSQL
        INT_MYSQL_LOCAL
        INT_MYSQL_CLOUD_SZ
        INT_MYSQL_CLOUD_QD
        INT_MYSQL_CUSTOM
        INT_Mail
        
    end
    events
        MESSAGE
        TRADE
        ACCOUNT
        EVALUATE
        MAIL
        SQL
        ANALYSIS
    end
    methods %Total
        function QA=QUANTAXIS()
            fprintf(' Welcome to QUANTAXIS 0.3.9 Beta\n CopyRight(c) 2017 yutiansut \n More Info http://www.yutiansut.com \n')
            addlistener(QA,'MESSAGE',@MESSAGEUPDATE);
            addlistener(QA,'SQL',@SQLSTATEMENT);
            addlistener(QA,'TRADE',@TRADECORE);
            addlistener(QA,'ACCOUNT',@ACCOUNTF);
            addlistener(QA,'ANALYSIS',@STRATEGY);
            addlistener(QA,'EVALUATE',@EVALUATION);
            QA.Initial
        end
        function Initial(QA)
            QA.MES.ID=1;
            QA.MES.Str='Finish Initial QUNATAXIS';
            disp(QA.MES.Str);
            notify(QA,'MESSAGE');
            QA.Interface_Mysql_Conn;
            QA.Login();
            disp(QA.MES.History);
        end
    end
    methods %DataFetch
        function Fetch(QA)
            
            QA.FET.Methods=input('Methods(1/2/3) \n 1.Custom \n 2.auto\n 3.update\n','s');
            QA.FET.Type=input('FETCH TYPE \n ts -get the ts data\n info \n cash\n','s');
            switch QA.FET.Methods
                
                case {'1'}
                    
                    QA.FET.Save=input('SAVE STATUS:\n 1.Save to Local\n 2.Save to Cloud\n ','s');
                    QA.FET.StockId=input('StockID:  ','s');
                    
                    switch QA.FET.Type
                        case {'ts'}
                            [QA.FET.Data,QA.FET.Codes,QA.FET.Fields,QA.FET.Times,QA.FET.Error,QA.FET.Reqid]=QA.w.wsd(QA.FET.StockId,...
                                'pre_close,open,high,low,close,volume,amt,chg,pct_chg,swing,vwap,turn,rel_ipo_chg,rel_ipo_pct_chg',...
                                '2000-01-01',datestr(today,'yyyy-mm-dd'),'Fill=Previous','Currency=CNY','PriceAdj=F');
                            if QA.FET.Save=='1' && QA.INT_MYSQL.Status==1
                                QA.SYS.SQL.Conn=QA.INT_MYSQL.Conn;
                                QA.FET.Stockid= regexp(QA.FET.StockId, '.S', 'split');
                                QA.FET.Stockid=char(QA.FET.Stockid{1,1});
                                QA.SYS.SQL.Tablename=[QA.FET.Stockid,'_',QA.FET.Type];
                                QA.SYS.SQL.Databasename=QA.INT_MYSQL.Databasename;
                                QA.SYS.SQL.Type=QA.FET.Type;
                                QA.SYS.SQL.Sqlquery=['CREATE TABLE if not exists`',QA.SYS.SQL.Databasename,'`.`',QA.SYS.SQL.Tablename, ...
                                    '` (`DATE`DOUBLE NULL,`PRE_CLOSE` DOUBLE NULL, `OPEN` DOUBLE NULL,  `HIGH` DOUBLE NULL,'...
                                    '  `LOW` DOUBLE NULL,  `CLOSE` DOUBLE NULL,  `VOLUME` DOUBLE NULL,  `AMT` DOUBLE NULL, '...
                                    '  `CHG` DOUBLE NULL,`PCT_CHG` DOUBLE NULL,  `SWING` DOUBLE NULL,  `VWAP` DOUBLE NULL, '...
                                    '`TURN` DOUBLE NULL, `REL_IPO_CHG` DOUBLE NULL,  `REL_IPO_PCT_CHG` DOUBLE NULL);'];
                                exec(QA.SYS.SQL.Conn,QA.SYS.SQL.Sqlquery);% NEW TABLE
                                QA.FET.Label=[{'DATE'},QA.FET.Fields'];
                                QA.FET.Insertdata=[QA.FET.Times,QA.FET.Data];
                                insert(QA.SYS.SQL.Conn,QA.SYS.SQL.Tablename,QA.FET.Label,QA.FET.Insertdata)
                                
                            end
                        case {'AMOUNT'}
                            [QA.FET.Data,QA.FET.Codes,QA.FET.Fields,QA.FET.Times,QA.FET.Error,QA.FET.Reqid]=QA.w.wsd(QA.FET.StockId,...
                                'mf_amt,mf_vol,mf_amt_ratio,mf_vol_ratio,mf_amt_close,mf_amt_open','2010-01-06',datestr(today,'yyyy-mm-dd'),'PriceAdj=F');
                            if QA.FET.Save=='1' && QA.INT_MYSQL.Status==1
                                QA.SYS.SQL.Conn=QA.INT_MYSQL.Conn;
                                QA.FET.Stockid= regexp(QA.FET.StockId, '.S', 'split');
                                QA.FET.Stockid=char(QA.FET.Stockid{1,1});
                                QA.SYS.SQL.Tablename=[QA.FET.Stockid,'_',QA.FET.Type];
                                QA.SYS.SQL.Databasename=QA.INT_MYSQL.Databasename;
                                QA.SYS.SQL.Type=QA.FET.Type;
                                QA.SYS.SQL.Sqlquery=['CREATE TABLE if not exists`',QA.SYS.SQL.Databasename,'`.`',QA.SYS.SQL.Tablename, ...
                                    '` (`DATE`DOUBLE NULL,`PRE_CLOSE` DOUBLE NULL, `OPEN` DOUBLE NULL,  `HIGH` DOUBLE NULL,'...
                                    '  `LOW` DOUBLE NULL,  `CLOSE` DOUBLE NULL,  `VOLUME` DOUBLE NULL,  `AMT` DOUBLE NULL, '...
                                    '  `CHG` DOUBLE NULL,`PCT_CHG` DOUBLE NULL,  `SWING` DOUBLE NULL,  `VWAP` DOUBLE NULL, '...
                                    '`TURN` DOUBLE NULL, `REL_IPO_CHG` DOUBLE NULL,  `REL_IPO_PCT_CHG` DOUBLE NULL);'];
                                exec(QA.SYS.SQL.Conn,QA.SYS.SQL.Sqlquery);% NEW TABLE
                                QA.FET.Label=[{'DATE'},QA.FET.Fields'];
                                QA.FET.Insertdata=[QA.FET.Times,QA.FET.Data];
                                insert(QA.SYS.SQL.Conn,QA.SYS.SQL.Tablename,QA.FET.Label,QA.FET.Insertdata)
                                
                            end
                            
                        case {'JISHU'}
                            
                            
                            [QA.FET.Data,QA.FET.Codes,QA.FET.Fields,QA.FET.Times,QA.FET.Error,QA.FET.Reqid]=QA.w.wsd(QA.FET.StockId,...
                                'ADTM,ATR,BBI,BBIBOLL,BIAS,BOLL,CCI,CDP,DMA,DMI,DPO,ENV,EXPMA,KDJ,slowKD,MA,MACD,MIKE,MTM,PRICEOSC,PVT,RC,ROC,RSI,SAR,SI,SOBV,SRMI,STD,TAPI,TRIX,VHF,VMA,VMACD,VOSC,VSTD,WVAD,vol_ratio',...
                                '2016-02-06','2016-03-07','ADTM_N1=23','ADTM_N2=8','ADTM_IO=1','ATR_N=14','ATR_IO=1','BBI_N1=3','BBI_N2=6','BBI_N3=12','BBI_N4=24',...
                                'BBIBOLL_N=10','BBIBOLL_Width=3','BBIBOLL_IO=1','BIAS_N=12','BOLL_N=26','BOLL_Width=2','BOLL_IO=1','CCI_N=14','CDP_IO=1','DMA_S=10',...
                                'DMA_L=50','DMA_N=10','DMA_IO=1','DMI_N=14','DMI_N1=6','DMI_IO=1','DPO_N=20','DPO_M=6','DPO_IO=1','ENV_N=14','ENV_IO=1','EXPMA_N=12',...
                                'KDJ_N=9','KDJ_M1=3','KDJ_M2=3','KDJ_IO=1','SlowKD_N1=9','SlowKD_N2=3','SlowKD_N3=3','SlowKD_N4=5','SlowKD_IO=1','MA_N=5','MACD_L=26',...
                                'MACD_S=12','MACD_N=9','MACD_IO=1','MIKE_N=12','MIKE_IO=1','MTM_interDay=6','MTM_N=6','MTM_IO=1','PRICEOSC_L=26','PRICEOSC_S=12',...
                                'RC_N=50','ROC_interDay=12','ROC_N=6','ROC_IO=1','RSI_N=6','SAR_N=4','SAR_SP=2','SAR_MP=20','SRMI_N=9','STD_N=26','TAPI_N=6','TAPI_IO=1',...
                                'TRIX_N1=12','TRIX_N2=20','TRIX_IO=1','VHF_N=28','VMA_N=5','VMACD_S=12','VMACD_L=26','VMACD_N=9','VMACD_IO=1','VOSC_S=12','VOSC_L=26',...
                                'VSTD_N=10','WVAD_N1=24','WVAD_N2=6','WVAD_IO=1','VolumeRatio_N=5','Fill=Previous','Currency=CNY','PriceAdj=F');
                            
                        case {'info'}
                            [QA.FET.Data,QA.FET.Codes,QA.FET.Fields,QA.FET.Times,QA.FET.Error,QA.FET.Reqid]=QA.w.wsd('000001.SZ','industry_gicscode','2016-03-04','2016-03-04','industryType=2','Fill=Previous','PriceAdj=F');
                        case {'cash'}
                            [QA.FET.Data,QA.FET.Codes,QA.FET.Fields,QA.FET.Times,QA.FET.Error,QA.FET.Reqid]=QA.w.wsd(QA.FET.StockId,'mf_amt,mf_vol,mf_amt_ratio,mf_vol_ratio,',...
                                'mf_amt_close,mf_amt_open','2000-01-01',datestr(today,'yyyy-mm-dd'),'Fill=Previous','PriceAdj=F');
                            if QA.FET.Save=='1' && QA.INT_MYSQL.Status==1
                                QA.SYS.SQL.Conn=QA.INT_MYSQL.Conn;
                                QA.FET.Stockid= regexp(QA.FET.StockId, '.S', 'split');
                                QA.FET.Stockid=char(QA.FET.Stockid{1,1});
                                QA.SYS.SQL.Tablename=[QA.FET.Stockid,'_',QA.FET.Type];
                                QA.SYS.SQL.Databasename=QA.INT_MYSQL.Databasename;
                                QA.SYS.SQL.Type=QA.FET.Type;
                                QA.SYS.SQL.Sqlquery=['CREATE TABLE if not exists`',QA.SYS.SQL.Databasename,'`.`',QA.SYS.SQL.Tablename, ...
                                    '` (`DATE`DOUBLE NULL,`MF_AMT` DOUBLE NULL, `MF_VOL` DOUBLE NULL,  `MF_AMT_RATIO` DOUBLE NULL,'...
                                    '  `MF_VOL_RATIO` DOUBLE NULL,  `MF_AMT_CLOSE` DOUBLE NULL,  `MF_AMT_OPEN` DOUBLE NULL);'];
                                exec(QA.SYS.SQL.Conn,QA.SYS.SQL.Sqlquery);% NEW TABLE
                                QA.FET.Label=[{'DATE'},QA.FET.Fields'];
                                QA.FET.Insertdata=[QA.FET.Times,QA.FET.Data];
                                insert(QA.SYS.SQL.Conn,QA.SYS.SQL.Tablename,QA.FET.Label,QA.FET.Insertdata)
                                
                            end
                    end
                case {'2'}
                    [QA.FET.Data,~,QA.FET.Fields,~,QA.FET.Error,QA.FET.Reqid]=QA.w.wset('SectorConstituent','date=20170222;sectorId=a001010100000000');
                    QA.MES.Str='Get Stock List';
                    disp(QA.MES.Str);
                    notify(QA,'MESSAGE');
                    QA.FET.Data=QA.FET.Data(:,2:3);
                    QA.FET.Fields=QA.FET.Fields(2:3,:);
                    QA.FET_BAT.LIST=QA.FET.Data(:,1);
                    QA.SYS.SQL.Tablename='StockList';
                    QA.SYS.SQL.Conn=QA.INT_MYSQL.Conn;
                    QA.SYS.SQL.Databasename=QA.INT_MYSQL.Databasename;
                    QA.SYS.SQL.Sqlquery=['DROP TABLE if exists `',QA.SYS.SQL.Databasename,'`.`',QA.SYS.SQL.Tablename,'`'];
                    exec(QA.SYS.SQL.Conn,QA.SYS.SQL.Sqlquery);
                    QA.SYS.SQL.Sqlquery=['CREATE TABLE if not exists`',QA.SYS.SQL.Databasename,'`.`',QA.SYS.SQL.Tablename,'` (`wind_code` TEXT NULL, `sec_name` TEXT NULL);'];
                    exec(QA.SYS.SQL.Conn,QA.SYS.SQL.Sqlquery);
                    insert(QA.SYS.SQL.Conn,QA.SYS.SQL.Tablename,QA.FET.Fields',QA.FET.Data)
                    QA.MES.Str='Finish Insert the StockList to SQL';
                    disp(QA.MES.Str);
                    notify(QA,'MESSAGE');
                    switch QA.FET.Type
                        case {'ts'}
                            for batid=1:size(QA.FET_BAT.LIST,1)
                                QA.FET.StockId=QA.FET_BAT.LIST(batid);
                                [QA.FET.Data,QA.FET.Codes,QA.FET.Fields,QA.FET.Times,QA.FET.Error,QA.FET.Reqid]=QA.w.wsd(QA.FET.StockId,'pre_close,open,high,low,close,volume,amt,chg,pct_chg,swing,vwap,turn,rel_ipo_chg,rel_ipo_pct_chg','2001-01-01',datestr(today,'yyyy-mm-dd'),'Fill=Previous','Currency=CNY','PriceAdj=F');
                                QA.MES.Str=['Finish get the data of',QA.FET.StockId];
                                disp(QA.MES.Str);
                                notify(QA,'MESSAGE');
                                if QA.INT_MYSQL.Status==1
                                    QA.MES.Str='SQL Connection Success, Start Saving';
                                    disp(QA.MES.Str);
                                    notify(QA,'MESSAGE');
                                    QA.SYS.SQL.Conn=QA.INT_MYSQL.Conn;
                                    QA.FET.Stockid= regexp(QA.FET.StockId, '.S', 'split');
                                    QA.FET.Stockid=char(QA.FET.Stockid{1,1}{1,1});
                                    
                                    QA.SYS.SQL.Tablename=[QA.FET.Stockid,'_',QA.FET.Type];
                                    QA.SYS.SQL.Databasename=QA.INT_MYSQL.Databasename;
                                    QA.SYS.SQL.Sqlquery=['CREATE TABLE if not exists`',QA.SYS.SQL.Databasename,'`.`',QA.SYS.SQL.Tablename,'` (`DATE`DOUBLE NULL,`PRE_CLOSE` DOUBLE NULL, `OPEN` DOUBLE NULL,  `HIGH` DOUBLE NULL,  `LOW` DOUBLE NULL,  `CLOSE` DOUBLE NULL,  `VOLUME` DOUBLE NULL,  `AMT` DOUBLE NULL,   `CHG` DOUBLE NULL,`PCT_CHG` DOUBLE NULL,  `SWING` DOUBLE NULL,  `VWAP` DOUBLE NULL,  `TURN` DOUBLE NULL, `REL_IPO_CHG` DOUBLE NULL,  `REL_IPO_PCT_CHG` DOUBLE NULL);'];
                                    exec(QA.SYS.SQL.Conn,QA.SYS.SQL.Sqlquery);%NEW TABLE
                                    QA.MES.Str=['Create Table',QA.SYS.SQL.Tablename];
                                    disp(QA.MES.Str);
                                    notify(QA,'MESSAGE');
                                    QA.FET.Label=[{'DATE'},QA.FET.Fields'];
                                    QA.FET.Insertdata=[QA.FET.Times,QA.FET.Data];
                                    insert(QA.SYS.SQL.Conn,QA.SYS.SQL.Tablename,QA.FET.Label,QA.FET.Insertdata)
                                    QA.MES.Str=['Insert Data',QA.SYS.SQL.Tablename];
                                    disp(QA.MES.Str);
                                    notify(QA,'MESSAGE');
                                    
                                end
                            end
                        case {'cash'}
                            for batid=613:size(QA.FET_BAT.LIST,1)
                                QA.FET.StockId=QA.FET_BAT.LIST(batid);
                                [QA.FET.Data,QA.FET.Codes,QA.FET.Fields,QA.FET.Times,QA.FET.Error,QA.FET.Reqid]=QA.w.wsd(QA.FET.StockId,'mf_amt,mf_vol,mf_amt_ratio,mf_vol_ratio,mf_amt_close,mf_amt_open','2000-01-01','2017-02-22','Fill=Previous','PriceAdj=F');
                                if  QA.INT_MYSQL.Status==1
                                    QA.MES.Str='SQL Connection Success, Start Saving';
                                    disp(QA.MES.Str);
                                    notify(QA,'MESSAGE');
                                    QA.SYS.SQL.Conn=QA.INT_MYSQL.Conn;
                                    QA.FET.Stockid= regexp(QA.FET.StockId, '.S', 'split');
                                    QA.FET.Stockid=char(QA.FET.Stockid{1,1}{1,1});
                                    QA.SYS.SQL.Tablename=[QA.FET.Stockid,'_',QA.FET.Type];
                                    QA.SYS.SQL.Databasename=QA.INT_MYSQL.Databasename;
                                    QA.SYS.SQL.Type=QA.FET.Type;
                                    QA.SYS.SQL.Sqlquery=['CREATE TABLE if not exists`',QA.SYS.SQL.Databasename,'`.`',QA.SYS.SQL.Tablename, ...
                                        '` (`DATE`DOUBLE NULL,`MF_AMT` DOUBLE NULL, `MF_VOL` DOUBLE NULL,  `MF_AMT_RATIO` DOUBLE NULL,'...
                                        '  `MF_VOL_RATIO` DOUBLE NULL,  `MF_AMT_CLOSE` DOUBLE NULL,  `MF_AMT_OPEN` DOUBLE NULL);'];
                                    exec(QA.SYS.SQL.Conn,QA.SYS.SQL.Sqlquery);% NEW TABLE
                                    QA.MES.Str=['Create Table',QA.SYS.SQL.Tablename];
                                    disp(QA.MES.Str);
                                    notify(QA,'MESSAGE');
                                    QA.FET.Label=[{'DATE'},QA.FET.Fields'];
                                    QA.FET.Insertdata=[QA.FET.Times,QA.FET.Data];
                                    insert(QA.SYS.SQL.Conn,QA.SYS.SQL.Tablename,QA.FET.Label,QA.FET.Insertdata)
                                    QA.MES.Str=['Insert Data',QA.SYS.SQL.Tablename];
                                    disp(QA.MES.Str);
                                    notify(QA,'MESSAGE');
                                end
                            end
                    end
                case {'3'}
                    switch QA.FET.Type
                        case {'ts'}
                            sqlquery='select `DATE` from `000001_ts`';
                            cursor=fetch(exec(QA.INT_MYSQL.Conn,sqlquery));
                            QA.FET.Date=cursor.Data;
                            if today>QA.FET.Date{end,1}
                                QA.FET.Datestart=datestr(QA.FET.Date{end,1}+1,'yyyy-mm-dd');
                                QA.FET.Dateend=datestr(today,'yyyy-mm-dd');
                                [QA.FET.Data,~,QA.FET.Fields,~,QA.FET.Error,QA.FET.Reqid]=QA.w.wset('SectorConstituent','date=20170222;sectorId=a001010100000000');
                                QA.MES.Str='Get Stock List';
                                disp(QA.MES.Str);
                                notify(QA,'MESSAGE');
                                QA.FET.Data=QA.FET.Data(:,2:3);
                                QA.FET.Fields=QA.FET.Fields(2:3,:);
                                QA.FET_BAT.LIST=QA.FET.Data(:,1);
                                QA.SYS.SQL.Tablename='StockList';
                                QA.SYS.SQL.Conn=QA.INT_MYSQL.Conn;
                                QA.SYS.SQL.Databasename=QA.INT_MYSQL.Databasename;
                                QA.SYS.SQL.Sqlquery=['DROP TABLE if exists `',QA.SYS.SQL.Databasename,'`.`',QA.SYS.SQL.Tablename,'`'];
                                exec(QA.SYS.SQL.Conn,QA.SYS.SQL.Sqlquery);
                                QA.SYS.SQL.Sqlquery=['CREATE TABLE if not exists`',QA.SYS.SQL.Databasename,'`.`',QA.SYS.SQL.Tablename,'` (`wind_code` TEXT NULL, `sec_name` TEXT NULL);'];
                                exec(QA.SYS.SQL.Conn,QA.SYS.SQL.Sqlquery);
                                insert(QA.SYS.SQL.Conn,QA.SYS.SQL.Tablename,QA.FET.Fields',QA.FET.Data)
                                QA.MES.Str='Finish Insert the StockList to SQL';
                                disp(QA.MES.Str);
                                notify(QA,'MESSAGE');
                                for batid=1:size(QA.FET_BAT.LIST,1)
                                    QA.FET.StockId=QA.FET_BAT.LIST(batid);
                                    [QA.FET.Data,QA.FET.Codes,QA.FET.Fields,QA.FET.Times,QA.FET.Error,QA.FET.Reqid]=QA.w.wsd(QA.FET.StockId,'pre_close,open,high,low,close,volume,amt,chg,pct_chg,swing,vwap,turn,rel_ipo_chg,rel_ipo_pct_chg',QA.FET.Datestart,QA.FET.Dateend,'Fill=Previous','Currency=CNY','PriceAdj=F');
                                    QA.MES.Str=['Finish get the data of',QA.FET.StockId];
                                    disp(QA.MES.Str);
                                    notify(QA,'MESSAGE');
                                    if QA.INT_MYSQL.Status==1
                                        QA.MES.Str='SQL Connection Success, Start Saving';
                                        disp(QA.MES.Str);
                                        notify(QA,'MESSAGE');
                                        QA.SYS.SQL.Conn=QA.INT_MYSQL.Conn;
                                        QA.FET.Stockid= regexp(QA.FET.StockId, '.S', 'split');
                                        QA.FET.Stockid=char(QA.FET.Stockid{1,1}{1,1});
                                        
                                        QA.SYS.SQL.Tablename=[QA.FET.Stockid,'_',QA.FET.Type];
                                        QA.SYS.SQL.Databasename=QA.INT_MYSQL.Databasename;
                                        QA.SYS.SQL.Sqlquery=['CREATE TABLE if not exists`',QA.SYS.SQL.Databasename,'`.`',QA.SYS.SQL.Tablename,'` (`DATE`DOUBLE NULL,`PRE_CLOSE` DOUBLE NULL, `OPEN` DOUBLE NULL,  `HIGH` DOUBLE NULL,  `LOW` DOUBLE NULL,  `CLOSE` DOUBLE NULL,  `VOLUME` DOUBLE NULL,  `AMT` DOUBLE NULL,   `CHG` DOUBLE NULL,`PCT_CHG` DOUBLE NULL,  `SWING` DOUBLE NULL,  `VWAP` DOUBLE NULL,  `TURN` DOUBLE NULL, `REL_IPO_CHG` DOUBLE NULL,  `REL_IPO_PCT_CHG` DOUBLE NULL);'];
                                        exec(QA.SYS.SQL.Conn,QA.SYS.SQL.Sqlquery);%NEW TABLE
                                        QA.MES.Str=['Create Table',QA.SYS.SQL.Tablename];
                                        disp(QA.MES.Str);
                                        notify(QA,'MESSAGE');
                                        QA.FET.Label=[{'DATE'},QA.FET.Fields'];
                                        QA.FET.Insertdata=[QA.FET.Times,QA.FET.Data];
                                        insert(QA.SYS.SQL.Conn,QA.SYS.SQL.Tablename,QA.FET.Label,QA.FET.Insertdata)
                                        QA.MES.Str=['Insert Data',QA.SYS.SQL.Tablename];
                                        disp(QA.MES.Str);
                                        notify(QA,'MESSAGE');
                                        
                                    end
                                end
                            else
                                disp('Nothing Update')
                            end
                        case {'cash'}
                    end
            end
        end
        
        
    end
    methods
        function SameIndustry(QA)
            sqlquery=['select',QA.ANA.Stockid];
            exec(sqlquery);
        end
        function Start(QA)
            disp('Welcome to QUANTAXIS Intelligent Analysis System')
            notify(QA,'ANALYSIS')
        end
    end
    methods %Interface Function
        function Interface_Mysql_Conn(QA)
            QA.INT_MYSQL.Choice=input('DataBase:\n1- Local  \n2-Custom \n Choose a DataBase:  ','s');
            QA.MES.Str=['MYSQL.Choice',QA.INT_MYSQL.Choice];
            disp(QA.MES.Str);
            notify(QA,'MESSAGE');
            switch QA.INT_MYSQL.Choice
                case {'1'}
                    QA.INT_MYSQL.Databasename='quantaxis';
                    QA.INT_MYSQL.Username='root';
                    QA.INT_MYSQL.Password ='940809';
                    QA.INT_MYSQL.Driver = 'com.mysql.jdbc.Driver';
                    QA.INT_MYSQL.Databaseurl = ['jdbc:mysql://localhost:3306/',QA.INT_MYSQL.Databasename];
                    QA.INT_MYSQL.Conn = database(QA.INT_MYSQL.Databasename,QA.INT_MYSQL.Username,QA.INT_MYSQL.Password,QA.INT_MYSQL.Driver,QA.INT_MYSQL.Databaseurl);
                    QA.INT_MYSQL.Status=isopen(QA.INT_MYSQL.Conn);
                    if QA.INT_MYSQL.Status==1
                        QA.MES.Str='Local Mysql Connection Success';
                        disp(QA.MES.Str);
                        notify(QA,'MESSAGE');
                        QA.INT_MYSQL_LOCAL=QA.INT_MYSQL;
                    end
           
                    
                case{'2'}
                    QA.INT_MYSQL.Databasename=input('Database:  ','s');
                    QA.INT_MYSQL.Username=input('UserName(example:root) \nName:  ','s');
                    QA.INT_MYSQL.Password =input('Password:  ','s');
                    QA.INT_MYSQL.Driver = 'com.mysql.jdbc.Driver';
                    QA.INT_MYSQL.Url=input('Url:  ','s');
                    QA.INT_MYSQL.Databaseurl = ['jdbc:mysql://',QA.INT_MYSQL.Url,':3306/',QA.INT_MYSQL.Databasename];
                    QA.INT_MYSQL.Conn = database(QA.INT_MYSQL.Databasename,QA.INT_MYSQL.Username,QA.INT_MYSQL.Password,QA.INT_MYSQL.Driver,QA.INT_MYSQL.Databaseurl);
                    QA.INT_MYSQL.Status=isopen(QA.INT_MYSQL.Conn);
                    if QA.INT_MYSQL.Status==1
                        QA.MES.Str='Custom Mysql Connection Success';
                        disp(QA.MES.Str);
                        notify(QA,'MESSAGE');
                        QA.INT_MYSQL_CUSTOM=QA.INT_MYSQL;
                    end
            end
            
            
        end

        
        
        
        
        
        function Interface_Mysql_Initial(QA)
            %Initial database
            %create table A.userlist 2.DataList
            if QA.INT_MYSQL.Status==1
                sqlquery=['CREATE TABLE `quantaxis`.`', 'StockList','` (`Name` TEXT NULL COMMENT '''',`FullID` TEXT NULL COMMENT '''',`DoubleID` DOUBLE NULL COMMENT '''');'];
                exec(QA.INT_MYSQL.Conn,sqlquery);
                sqlquery=['CREATE TABLE `quantaxis`.`', 'userlist','` (`Name` TEXT NULL COMMENT '''',`Password` TEXT NULL COMMENT '''');'];
                exec(QA.INT_MYSQL.Conn,sqlquery);
            end
        end
        function Interface_Mysql_Get(QA)
            if QA.INT_MYSQL.Status==1
                
            end
        end
        function Login(QA,varargin)
            register=input('QUANTAXIS 2.0 Alpha  Login or Register Y-REGISTER N-LOGIN(Y/N): ','s');
            
            
            sqlquery1=['CREATE TABLE if not exists `quantaxis`.`', 'userlist','` (`Userid` DOUBLE NULL,`Name` TEXT NULL COMMENT '''',`PassWord` TEXT NULL COMMENT '''',`Mail` TEXT NULL);'];
            exec(QA.INT_MYSQL.Conn,sqlquery1);
            if strcmpi(register,'Y')||strcmpi(register,'y')
                disp('========REGISTER========')
                QA.ACC_User.LoginName=input('--UserName--','s');
                str=['your input user name is:   ',QA.ACC_User.LoginName];
                disp(str)
                sqlquery=['select * from userlist where Name="',QA.ACC_User.LoginName,'"'];
                cursor=exec(QA.INT_MYSQL.Conn,sqlquery);
                cursor=fetch(cursor);
                QA.ACC_User.LoginResult=cursor.Data;
                
                if strcmpi(QA.ACC_User.LoginResult,'No Data')==0  %% NAME unique
                    QA.MES_Str='The User name is existed! Please Run Again';
                    disp(QA.MES.Str)
                    notify(QA,'MESSAGE')
                    QA.Login();
                else
                    disp('The User Name is OKAY Continue...')
                    QA.ACC_User.MailAddress=input('Mail Address:   ','s');
                    yanzhengn=ceil(20*rand(1))+1;
                    a=zeros(1,yanzhengn);
                    for i=1:yanzhengn
                        a(i)=ceil(95*rand(1))+32;
                    end
                    QA.ACC_User.UniqueName=char(a);
                    disp(QA.ACC_User.UniqueName)
                    QA.INT_Mail.subject='QUANTAXIS Code';
                    QAInterface_Mail(QA.ACC_User.MailAddress,QA.INT_Mail.subject,QA.ACC_User.UniqueName);
                    disp('QUANTAXIS CODE Sending....')
                    QA.ACC_User.UniqueNameinput=input('Please Input the Code  ','s');
                    if strcmpi(QA.ACC_User.UniqueName,QA.ACC_User.UniqueNameinput)==1
                        QA.MES.Str='Code is right!';
                        disp(QA.MES.Str)
                        notify(QA,'MESSAGE')
                        QA.ACC_User.LoginPassword=input('Please Input the Password:   ','s');
                        str=['your input password is:    ',QA.ACC_User.LoginPassword];
                        disp(str)
                        disp('Connecting to Server.....')
                    else
                        QA.MES.Str='Code is wrong';
                        disp(QA.MES.Str)
                        notify(QA,'MESSAGE')
                        QA.Login();
                    end
                    if isopen(QA.INT_MYSQL.Conn)==1
                        sqlquery='select userlist.Userid from userlist';
                        cursor=fetch(exec(QA.INT_MYSQL.Conn,sqlquery));
                        QA.ACC_User.id=cursor.Data;
                        if strcmpi(QA.ACC_User.id,'No Data')==1
                            QA.ACC_User.id=1000001;
                        else
                            QA.ACC_User.id=QA.ACC_User.id{end,1}+1;
                            
                            
                            Logintext={QA.ACC_User.id,QA.ACC_User.LoginName,QA.ACC_User.LoginPassword,QA.ACC_User.MailAddress};
                            insert(QA.INT_MYSQL.Conn,'userlist',{'Userid','Name','PassWord','Mail'},Logintext)
                        end
                    end
                    
                    sqlquery=['select * from userlist where Name="',QA.ACC_User.LoginName,'"'];
                    cursor=exec(QA.INT_MYSQL.Conn,sqlquery);
                    cursor=fetch(cursor);
                    QA.ACC_User.LoginResult=cursor.Data;
                    if strcmpi(QA.ACC_User.LoginResult,'No Data')==1
                        disp('Registion Failed!')
                        disp('Run Again');
                        QA.Login();
                    end
                    
                    QA.ACC_User.realpassword=QA.ACC_User.LoginResult(:,3);
                    
                    if strcmpi(QA.ACC_User.realpassword,QA.ACC_User.LoginPassword)==1
                        QA.MES.Str='Login Successful ! Any Question please turn to QQ279336410';
                        disp(QA.MES.Str)
                        notify(QA,'MESSAGE')
                        disp('[Email yutiansut@qq.com] [Website www.yutiansut.com] [QUANTAXIS Project quantaxis.yutiansut.com]')
                        disp('Please Login');
                        QA.Login();
                        clc
                        
                    else
                        disp('Registion Failed! Contact QQ 279336410')
                        disp('System Run again');
                        QA.Login();
                    end
                end
                
            else
                disp('========Login========')
                QA.ACC_User.LoginName=input('--UserName--','s');
                str=['your input user name is:   ',QA.ACC_User.LoginName];
                disp(str)
                QA.ACC_User.LoginPassword=input('--PassWord--','s');
                str=['your input password is:    ',QA.ACC_User.LoginPassword];
                disp(str)
                disp('Connecting to Server.....')
                sqlquery=['select * from userlist where Name="',QA.ACC_User.LoginName,'"'];
                cursor=exec(QA.INT_MYSQL.Conn,sqlquery);
                cursor=fetch(cursor);
                QA.ACC_User.LoginResult=cursor.Data;
                if strcmpi(QA.ACC_User.LoginResult,'No Data')==1
                    disp('No User Name in the Database!')
                    QA.Login();
                end
                
                QA.ACC_User.realpassword=QA.ACC_User.LoginResult(:,3);
                QA.ACC_User.LoginCompare=strcmpi(QA.ACC_User.realpassword,QA.ACC_User.LoginPassword);
                if QA.ACC_User.LoginCompare(1,:)==1
                    
                    QA.MES.Str='Login Successful ! Any Question please turn to QQ279336410';
                    disp(QA.MES.Str)
                    notify(QA,'MESSAGE')
                    disp('[Email yutiansut@qq.com] [Website www.yutiansut.com] [QUANTAXIS Project quantaxis.yutiansut.com]')
                else
                    disp('PassWord is Wrong...')
                    disp('You Still have one chance')
                    QA.ACC_User.LoginPassword=input('Please Input your Password  ','s');
                    sqlquery=['select * from userlist where Name="',QA.ACC_User.LoginName,'"'];
                    cursor=exec(QA.INT_MYSQL.Conn,sqlquery);
                    cursor=fetch(cursor);
                    QA.ACC_User.LoginResult=cursor.Data;
                    QA.ACC_User.realpassword=QA.ACC_User.LoginResult(:,3);
                    QA.ACC_User.LoginCompare=strcmpi(QA.ACC_User.realpassword,QA.ACC_User.LoginPassword);
                    if QA.ACC_User.LoginCompare(1,:)==0
                        disp('Login failed!')
                        QA.Login();
                    else
                        
                        QA.MES.Str='Login Successful ! Any Question please turn to QQ279336410';
                        disp(QA.MES.Str)
                        notify(QA,'MESSAGE')
                        disp('[Email yutiansut@qq.com] [Website www.yutiansut.com] [QuantAxis Project quantaxis.yutiansut.com]')
                        pause
                    end
                end
                
            end
            
        end
    end
    methods %Listener & Notify
        function QA=MESSAGEUPDATE(QA,varargin)
            QA.MES.History{QA.MES.ID,1}=datestr(now);
            QA.MES.History{QA.MES.ID,2}=QA.MES.Str;
            QA.MES.ID=QA.MES.ID+1;
        end
        function QA=DATAFETCH(QA,varargin)
            switch QA.FET.Source
                case {'wind'}
                case {'sina'}
                case {'SQL'}
            end
            
        end
        function QA=TRADECORE(QA,varargin)
            
            QA.TRA.SQL.Conn=QA.INT_MYSQL.Conn;
            QA.TRA.SQL.Tablename=[QA.TRA.id,'_','ts'];
            
            sqlquery=['select ', QA.TRA.SQL.Tablename,'.HIGH ,'...
                QA.TRA.SQL.Tablename,'.LOW, '...
                QA.TRA.SQL.Tablename,'.CLOSE '...
                'from quantaxis.',QA.TRA.SQL.Tablename,...
                ' where DATE=',num2str(QA.TRA.Date)];
            curs = fetch(exec(QA.INT_MYSQL.Conn,sqlquery));
            QA.TRA.Price=curs.Data;
            
            if QA.TRA.Bid<=QA.TRA.Price{1,1} && QA.TRA.Bid>=QA.TRA.Price{1,2}
                disp('Deal!')
                QA.TRA.status=QA.TRA.Position;  %-1buy 1sell
                if QA.TRA.status==-1
                    QA.TRA.Status='buy';
                end
                if QA.TRA.status==1
                    QA.TRA.Status='sell';
                end
                QA.MES.Str=['The Trading Varities is:',QA.TRA.id,',The Trading Date is:',datestr(QA.TRA.Date,'yyyymmdd'),...
                    ',Trading Price is:',num2str(QA.TRA.Bid),',Amount is:',num2str(QA.TRA.Amount),',Trading Towards is',QA.TRA.Status];
                disp(QA.MES.Str)
                
            end
            notify(QA,'ACCOUNT');
            
            notify(QA,'MESSAGE');
        end
        function QA=ACCOUNTF(QA,varargin)
            QA.ACC_Cash=QA.ACC_Cash+QA.TRA.status*QA.TRA.Bid*QA.TRA.Amount;
            
            QA.ACC_Trade{1,1}='Trading Varities';
            QA.ACC_Trade{1,2}='Trading Date';
            QA.ACC_Trade{1,3}='Price';
            QA.ACC_Trade{1,4}='Amount';
            QA.ACC_Trade{1,5}='Towards';
            QA.ACC_Trade{QA.ACC_Trade_id,1}=QA.TRA.id;
            QA.ACC_Trade{QA.ACC_Trade_id,2}=datestr(QA.TRA.Date,'yyyymmdd');
            QA.ACC_Trade{QA.ACC_Trade_id,3}=QA.TRA.Bid;
            QA.ACC_Trade{QA.ACC_Trade_id,4}=QA.TRA.Amount;
            QA.ACC_Trade{QA.ACC_Trade_id,5}=QA.TRA.Status;
            
            QA.ACC_Amount=QA.ACC_Amount-QA.TRA.status*QA.TRA.Amount;
            QA.ACC_Account{1,1}='TRA.id';
            QA.ACC_Account{1,2}='ACC_Amount';
            QA.ACC_Account{1,3}='Close_Price';
            QA.ACC_Account{1,4}='ACC_Amount*Close_Price';
            if strcmpi(QA.ACC_Account(:,1),QA.TRA.id)==0
                QA.ACC_Account_id=QA.ACC_Account_id+1;
            end
            QA.ACC_Account{QA.ACC_Account_id,1}=QA.TRA.id;
            QA.ACC_Account{QA.ACC_Account_id,2}=QA.ACC_Amount;
            QA.ACC_Account{QA.ACC_Account_id,3}=QA.TRA.Price{1,3};
            QA.ACC_Account{QA.ACC_Account_id,4}=QA.ACC_Amount*QA.TRA.Price{1,3};
            %             QA.ACC_Portfolio=QA.ACC_Account(2:end,4);
            QA.ACC_Portfolio=sum(cell2mat(QA.ACC_Account(2:end,4)));
            QA.ACC_TotalAssest(QA.ACC_Trade_id,1)=abs(QA.ACC_Portfolio)+QA.ACC_Cash;
            
            QA.ACC_Trade_id=QA.ACC_Trade_id+1;
            
        end
        function QA=STRATEGY(QA,varargin)
            QA.MES.Str='Start Strategy';
            disp(QA.MES.Str)
            notify(QA,'MESSAGE')
            QA.ACC_Strategy.type=input('Strategy type \n 1.Example \n 2.Custom \n 3.Custom Files \n','s');
            switch QA.ACC_Strategy.type;
                case {'1'}
                    disp('Simple MA Strategy')
                    
                    sqlquery='select stocklist.wind_code ,stocklist.sec_name from quantaxis.stocklist';
                    curs = fetch(exec(QA.INT_MYSQL.Conn,sqlquery));
                    
                    QA.ACC.StockList=curs.Data;
                    QA.ACC_ID=1;
                    QA.ACC.Type='ts';
                    QA.ACC.StockId=char(QA.ACC.StockList(1,1));
                    notify(QA,'SQL')
                    QA.ACC.StockId=char(QA.ACC.StockList(2,1));
                    notify(QA,'SQL')
                    QA.ACC_Methods.AnalysisID=1;
                    QA.ACC_Methods.AnalysisName=QA.ACC.UseData{QA.ACC_Methods.AnalysisID,1};
                    QA.ACC_Methods.AnalysisData=QA.ACC.UseData{QA.ACC_Methods.AnalysisID,2};
                    QA.ACC_Methods.AnalysisObj=cell2mat(QA.ACC_Methods.AnalysisData(:,2));
                    QA.ACC_Methods.Date=QA.ACC_Methods.AnalysisData(:,1);
                    
                    
                    ShortLen = 5;
                    LongLen = 20;
                    testx=QA.ACC_Methods.AnalysisObj;
                    [MA5, MA20] = movavg(testx', ShortLen, LongLen);
                    MA5(1:ShortLen-1) = QA.ACC_Methods.AnalysisObj(1:ShortLen-1);
                    MA20(1:LongLen-1) = QA.ACC_Methods.AnalysisObj(1:LongLen-1);
                    
                    
                    for t = LongLen:length(QA.ACC_Methods.AnalysisObj)
                        
                        %
                        SignalBuy = MA5(t)>MA5(t-1) && MA5(t)>MA20(t) && MA5(t-1)>MA20(t-1) && MA5(t-2)<=MA20(t-2);
                        %
                        SignalSell = MA5(t)<MA5(t-1) && MA5(t)<MA20(t) && MA5(t-1)<MA20(t-1) && MA5(t-2)>=MA20(t-2);
                        
                        %
                        if SignalBuy == 1  && QA.ACC_Cash>0
                            
                            
                            QA.MES.Str=['Decision -- Buy',QA.ACC_Methods.AnalysisName];
                            disp(QA.MES.Str)
                            notify(QA,'MESSAGE')
                            QA.TRA.id=QA.ACC_Methods.AnalysisName;
                            QA.TRA.Date=QA.ACC_Methods.Date(t);
                            QA.TRA.Date=QA.TRA.Date{1,1};
                            QA.TRA.Bid=QA.ACC_Methods.AnalysisObj(t);
                            QA.TRA.Amount=10000;
                            QA.TRA.Position=-1;
                            notify(QA,'TRADE')
                            
                        end
                        
                        %
                        if SignalSell == 1 && QA.ACC_Account{2,2}>0
                            %
                            
                            QA.MES.Str=['Decision -- SELL',QA.ACC_Methods.AnalysisName];
                            disp(QA.MES.Str)
                            notify(QA,'MESSAGE')
                            QA.TRA.id=QA.ACC_Methods.AnalysisName;
                            QA.TRA.Date=QA.ACC_Methods.Date(t);
                            QA.TRA.Date=QA.TRA.Date{1,1};
                            QA.TRA.Bid=QA.ACC_Methods.AnalysisObj(t);
                            QA.TRA.Amount=10000;
                            QA.TRA.Position=1;
                            notify(QA,'TRADE')
                        end
                        
                        
                        %
                        if t == length(QA.ACC_Methods.AnalysisObj) && QA.ACC_Account{2,2}>0
                            QA.MES.Str=['Decision -- SELL',QA.ACC_Methods.AnalysisName];
                            disp(QA.MES.Str)
                            notify(QA,'MESSAGE')
                            QA.TRA.id=QA.ACC_Methods.AnalysisName;
                            QA.TRA.Date=QA.ACC_Methods.Date(t);
                            QA.TRA.Date=QA.TRA.Date{1,1};
                            QA.TRA.Bid=QA.ACC_Methods.AnalysisObj(t);
                            QA.TRA.Amount=QA.ACC_Account{2,2};
                            QA.TRA.Position=1;
                            notify(QA,'TRADE')
                        end
                        
                    end
                    
                    notify(QA,'EVALUATE');
                    
                    
                    
                    
                case {'2'}
                    QA.MES.Str='Using Custom Strategy';
                    disp(QA.MES.Str)
                    notify(QA,'MESSAGE')
                    QA=QACustomStrategy(QA,varargin);
                case {'3'}
                    QA.MES.Str='Using Custom Strategy';
                    disp(QA.MES.Str)
                    notify(QA,'MESSAGE')
                    [filename, pathname] = uigetfile({'*.m';'*.p';'*.mat';'*.*'},'File Selector');
                    addpath(genpath(pathname))
                    savepath
                    a=regexp(filename,'.m','split');
                    a=char(a(1));
                    eval(a)
            end
        end
        function QA=SQLSTATEMENT(QA,varargin)
            
            QA.ACC.Stockid= regexp(QA.ACC.StockId, '.S', 'split');
            QA.ACC.Stockid=char(QA.ACC.Stockid{1,1});
            
            QA.ACC.SQL.Tablename=[QA.ACC.Stockid,'_',QA.ACC.Type];
            QA.ACC.SQL.Conn=QA.INT_MYSQL.Conn;
            sqlquery=['select ', QA.ACC.SQL.Tablename,'.DATE ,'...
                QA.ACC.SQL.Tablename,'.OPEN,'...
                QA.ACC.SQL.Tablename,'.HIGH,'...
                QA.ACC.SQL.Tablename,'.LOW,'...
                QA.ACC.SQL.Tablename,'.CLOSE '...
                'from quantaxis.',QA.ACC.SQL.Tablename];
            curs = fetch(exec(QA.INT_MYSQL.Conn,sqlquery));
            QA.ACC.Data=curs.Data;
            QA.ACC.UseData{QA.ACC_ID,1}=QA.ACC.Stockid;
            QA.ACC.UseData{QA.ACC_ID,2}=QA.ACC.Data;
            QA.ACC.UseData{QA.ACC_ID,3}=QA.ACC.StockId;
            QA.ACC_ID=QA.ACC_ID+1;
        end
        function QA=EVALUATION(QA,varargin)
            QA.ACC.id=QA.ACC_User.LoginResult{1,1};
            sqlquery=['SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = "quantaxis" and TABLE_NAME like "ac',num2str(QA.ACC.id),'s%" ;'];
            curs=fetch(exec(QA.INT_MYSQL.Conn,sqlquery));
            if strcmpi(curs.Data,'No Data')
                QA.ACC.strategyid=9000001;
            else
                QA.ACC.list=curs.Data{end,1};
                QA.ACC.strategyid=regexp(QA.ACC.list,'s','split');
                QA.ACC.strategyid=QA.ACC.strategyid{1,2};
                QA.ACC.strategyid=str2double(QA.ACC.strategyid)+1;
                
                
            end
            QA.ACC.strategyname=['ac',num2str(QA.ACC.id),'s',num2str(QA.ACC.strategyid)];
            sqlquery=['CREATE TABLE `quantaxis`.`',QA.ACC.strategyname ,'` (`Tradingvarieties` TEXT NULL ,`TradingDate` TEXT NULL ,'...
                '`Price` DOUBLE NULL ,`Amount` DOUBLE NULL ,`Towards` TEXT NULL);'];
            exec(QA.INT_MYSQL.Conn,sqlquery);
            QA.ACC.Trade=QA.ACC_Trade(2:end,:);
            insert(QA.INT_MYSQL.Conn,QA.ACC.strategyname,{'Tradingvarieties','TradingDate','Price','Amount','Towards'},QA.ACC.Trade);
            
        end
    end
end
function QAInterface_Mail(TargetAddress, subject, content)


SourceAddress='';
password='';

%% SMTP_Server Get
%ind = find( SourceAddress == '@', 1);
%temp = SourceAddress(ind+1:end);

FieldName ='mxhichina.com';%temp;
SMTP_Server = ['smtp.',FieldName];
disp('sending soon!');
%%
setpref('Internet','SMTP_Server',SMTP_Server);%SMTP
setpref('Internet','E_mail',SourceAddress);
setpref('Internet','SMTP_Username',SourceAddress);
setpref('Internet','SMTP_Password',password);

props = java.lang.System.getProperties;
props.setProperty('mail.smtp.auth','true');

sendmail(TargetAddress, subject, content);


end
