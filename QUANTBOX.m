classdef QUANTBOX< handle
    %yutiansutQUANTAXIS OOP代码重构版本
    %by yutiansut
    %www.yutiansut.com
    %2016/2/26-2016/2/28  1.2版本
    %2016/2/6  1.1 版本
    % 监听函数列表
    %     FetchState
    %     AnalysisState
    %     FilingState
    %     MessageUpdate  %%用于监听message数量
    
    properties
        
        
        %%  数据获取api
        %%  数据清洗api
        %%  消息记录api
        %%  交易系统api
        %%  评估系统api
        TRA=struct;
        TRA_Id;
        TRA_Time;
        TRA_StockID;
        TRA_Towards;
        TRA_Price; %
        TRA_Price_Total;
        TRA_Vol;
        TRA_Tax;
        TRA_Bid;
        %%  账户系统api  ACC_
        ACC=struct;
        ACC_TotalAssest=1000000;
        ACC_Cash=1000000;  %账户中的现金
        ACC_Position;  %账户中的股票
        ACC_Portfolio=0; %股票的总值
        ACC_Trade;
        ACC_Trade_id=2;
        ACC_accumulate;
        ACC_Price_Total;
        ACC_Price;
        ACC_Amount=0;
        ACC_Account;
        ACC_Account_id=1;
        %%  评估系统api  VAL_
        EVA=struct;
        EVA_Case;
        EVA_Price;
        EVA_Vol;
        EVA_Win;
        %% 系统承载  数据获取后自动放过来 -MYSQL连接
        SYS=struct;
        SYS_TS;
        SYS_TICK;
        
        
        
        StockCode;%股票代码
        StockCodeOut;
        StockID=1;
        Data;
        StockDataDouble;
        BeginDate;%
        EndDate;
        SaveFlag;
        Component;%成分股
        ConnLocal;
        ConnCloud;
        % 1 保存
        % 0 不保存
        NoticeType;
        URLchar;
        NoticeTypeWord;
        tsout;
        RunIndex;
        SendMail;
        % 1 发送邮件
        % 0 不发送邮件
        StatusCode=000;
        Result;
        Volum;
        %%状态参数
        % 000 初始化状态
        % 10x 网络连接
        % 	101 URL中无返回数据
        % 	102 MYSQL中无相关数据
        % 20x 本地数据
        % 	201 本地数据文件丢失
        % 	202 本地已有数据文件 需要更新
        % 	203 本地已有数据文件 无需更新
        % 30x 成功连接网络
        % 	301 下载数据为空
        % 	302 成功下载数据 但本地无法保存
        % 	303 成功下载数据并保存
        % 40x 邮件问题
        % 	401 邮件成功发送
        % 	402 邮件服务器出错
        % 5xx 数据清洗与环境准备
        %   51x StockTick数据
        %       510 Tick数据获取成功
        %       511 Tick数据获取成功，且符合数据清洗要求
        %       512 Tick数据获取成功，但长度不符合清洗要求
        %   52x StockTsday数据
        %       520 Tsday数据获取成功
        %       521 Tsday数据获取成功，且符合数据清洗要求
        %       522 Tsday数据获取成功，但长度不符合清洗要求
        %   53x StockNotice数据
        % 60x 数据分析
        MessageHistory={};
        str;
        TargetAddress;
        MessageID=1;
        Filing;
        Analysis;
        LoginName;
        LoginPassword;
        LoginResult;
        realpassword;
        LoginCompare;
        profitOut;
        portValue;
        myTrades;
        tmun=2800;
        datatempid;
        BatNum;
        BESTYFIT; %SVM优化IMF的各项BESTYFIT
        BESTYFIT_depth2;
        HURST; %hurst CEEMDAN分解后的指数
        HURST_depth2;
        besthursti; %CEEMDAN分解后的hurst=0.5的临界值的位置
        besthursti_depth2;
        ORGY;  %需要预测的原序列值 （扣减掉滞后阶数）
        ORGY_depth2;
        CEEMDAN_ID %CEEMDAN需要分解的股票个数
        
        BESTYFITANDY;%%第一列 FIT 第二列 Y
        BESTYFITANDY_depth2;
        MODES; %%%CEEMDAN的输出  使用的时候要转置
        MODES_depth2;
        ITS;  %%CEEMDAN的输出
        ITS_depth2;
        KernelType='rbf';
        SVRt;%%%SVR的滞后阶数选择
        BESTYFITANDY_Poly;
    end
    events  %设定一个监听 当
        FetchState
        AnalysisState
        FilingState
        MessageUpdate  %%用于监听message数量
        Mail
        StrategyA
        Account;
        Trade;
        Value;
    end
    
    methods %%For API
        %%主函数
        function obj=yutiansutQUANTAXIS(obj)
            disp('===欢迎使用QUANTAXIS 1.1 beta by yutiansut===')
            disp('==========QUANTAXIS体验版 限量注册中==========')
            disp('===更多信息 请访问http://www.yutiansut.com===')
            disp('==作者 余天 版本 1.1 beta 更新日期 2016/2/8==')
            register=input('限量注册中  是否注册 Y-注册 N-直接登录(Y/N): ','s');
            [~, obj.ConnLocal]=ConnectMysqlLocal;
            
            [~,conn]=ConnectMysqlCloud;
            obj.ConnCloud=conn;
            %需要注释掉
            % sqlquery=['CREATE TABLE `QUANTBOX`.`', 'UserList','` (`Name` TEXT NULL COMMENT '''',`PassWord` TEXT NULL COMMENT '''');'];
            %  cusorx=exec(obj.ConnCloud,sqlquery);
            
            
            %%
        
            %%
            addlistener(obj,'FetchState',@DFetch); %%listenerA1 状态改变和邮件监听
            addlistener(obj,'FilingState',@DFiling); %%进行数据清洗
            addlistener(obj,'AnalysisState',@DAnalysis);%%进行数据清洗
            addlistener(obj,'MessageUpdate',@MUpdate);
            addlistener(obj,'Mail',@QUANTMail);
            addlistener(obj,'StrategyA',@DStrategyA);
            addlistener(obj,'Account',@ACCOUNT);
            addlistener(obj,'Trade',@TRADE);
            addlistener(obj,'Value',@VALUE);
        end
        
        %%
        % For a function: functionName
        % lh = addlistener(eventSourceObj,'EventName',@functionName)
        % For an ordinary method called with an object of the class: obj.methodName
        % lh = addlistener(eventSourceObj,'EventName',@obj.methodName)
        % For a static method:ClassName.methodName
        % lh = addlistener(eventSourceObj,'EventName',@ClassName.methodName)
        % For a function in a package:PackageName.functionName
        % lh = addlistener(eventSourceObj,'EventName',@PackageName.functionName)
        
        % function Statetrigger(obj)
        % notify(obj,'xxxxx');
        % end
        
        
        %%
        function [StockTick,Header,StatusStr] = StockTick(obj)
            % 获取某只股票某日交易明细数据
            
            % StockCode:字符阵列型，表示证券代码，如'sh600000'
            % BeginDate:字符阵列型，表示希望获取股票数据所在时段的开始日期，如'2014-12-05'
            % http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=sh600000&date=2006-03-05
            % http://market.finance.sina.com.cn/downxls.php?date=2014-12-05&symbol=sh600000
            %% 输入输出预处理
            
            % 股票代码预处理，目标代码demo 'sh600588'
            if obj.StockCode(1,1) == '6'
                obj.StockCode = ['sh',obj.StockCode];
            end
            if obj.StockCode(1,1) == '0'|| obj.StockCode(1,1) == '3'
                obj.StockCode = ['sz',obj.StockCode];
            end
            
            ind = find(obj.BeginDate == '-',1);
            if isempty(ind)
                temp = [obj.BeginDate(1:4),'-',obj.BeginDate(5:6),'-',obj.BeginDate(7:end)];
                obj.BeginDate = temp;
            end
            StatusStr = [];
            StockTick = [];
            Header = {'成交时间','成交价','价格变动','成交量-手','成交额-元','性质'};
            %% 先检查本地是否已经存在该数据
            FolderStr = ['./DataBase/Stock/Tick_mat/',obj.StockCode,'_Tick'];
            FileString = [FolderStr,'/',obj.StockCode,'_Tick_',obj.BeginDate,'.mat'];
            FileExist = 0;
            if isdir( FolderStr )
                if exist(FileString, 'file') == 2
                    FileExist = 1;
                end
                
                if 1 == FileExist
                    obj.str = ['load ',FileString];
                    eval(obj.str);
                    return;
                end
            end
            %% urlread
            URL=['http://market.finance.sina.com.cn/downxls.php?date=',obj.BeginDate,'&symbol=',obj.StockCode];
            
            if verLessThan('matlab', '8.3')
                [obj.URLchar, status] = urlread_General(URL,'TimeOut', 60,'Charset', 'gb2312');
            else
                [obj.URLchar, status] = urlread(URL,'TimeOut', 60,'Charset', 'gb2312');
            end
            
            if status == 0
                obj.str = ['urlread error:数据获取失败！请检查网络连接情况或输入的参数！'];
                disp(obj.str);
                notify(obj,'MessageUpdate')
                StatusStr = obj.str;
                return;
            end
            
            expr = ['当天没有数据'];
            [matchstart,matchend,tokenindices,matchstring] = regexpi(obj.URLchar, expr);
            
            if ~isempty(matchstring)
                obj.str = ['当天没有数据！请检查输入的参数！'];
                disp(obj.str);
                notify(obj,'MessageUpdate')
                StatusStr = obj.str;
                return;
            end
            
            URLString = java.lang.String(obj.URLchar);
            %% 数据处理
            delimiter = obj.URLchar(6);
            
            % Result = textscan(URLchar, '%s %s %s %s %s %s', 'delimiter', '	','BufSize',4095*3);
            Result = textscan(obj.URLchar, '%s %s %s %s %s %s', 'delimiter', '	');
            
            temp = Result{1,1};
            if size(temp, 1) == 1
                obj.str = ['数据获取失败！可能数据为空或检查输入的参数！'];
                disp(obj.str);
                notify(obj,'MessageUpdate')
                StatusStr = obj.str;
                return;
            end
            
            temp = Result{1,1};
            temp = temp(2:end);
            DtimeStr = temp;
            temp = Result{1,2};
            temp = temp(2:end);
            Price = temp;
            temp = Result{1,3};
            temp = temp(2:end);
            PriceChg = temp;
            temp = Result{1,4};
            temp = temp(2:end);
            Vol = temp;
            temp = Result{1,5};
            temp = temp(2:end);
            Amt = temp;
            temp = Result{1,6};
            temp = temp(2:end);
            SellBuyFlag = temp;
            
            Len = size( DtimeStr,1 );
            StockTick = zeros(Len,6);
            
            DtimeStr = DtimeStr(end:(-1):1,:);
            Price = Price(end:(-1):1,:);
            PriceChg = PriceChg(end:(-1):1,:);
            Vol = Vol(end:(-1):1,:);
            Amt = Amt(end:(-1):1,:);
            SellBuyFlag = SellBuyFlag(end:(-1):1,:);
            
            for i = 1:Len
                
                tempT = DtimeStr{i};
                % control characters检查char(0:20)
                category = 'cntrl';
                tf = isstrprop(tempT, category);
                ind = find( tf==1 )';
                tempT(ind) = [];
                temp = [obj.BeginDate,' ',tempT];
                
                ind = find(tempT == ':');
                if ~isempty(ind) && length(ind) == 2
                    temp = datenum( temp, 'yyyy-mm-dd HH:MM:SS');
                elseif ~isempty(ind) && length(ind) == 1
                    temp = datenum( temp, 'yyyy-mm-dd HH:MM');
                end
                
                temp = datestr(temp,'yyyymmddHHMM.SS');
                temp = str2double(temp);
                ind = 1;
                if ~isempty(temp)
                    StockTick(i,ind) = temp;
                else
                    if i>1
                        StockTick(i,ind) = StockTick(i-1,ind);
                    end
                end
                
                temp = Price{i};
                % control characters检查char(0:20)
                category = 'cntrl';
                tf = isstrprop(temp, category);
                ind = find( tf==1 )';
                temp(ind) = [];
                temp = str2double(temp);
                ind = 2;
                if ~isempty(temp)
                    StockTick(i,ind) = temp;
                else
                    if i>1
                        StockTick(i,ind) = StockTick(i-1,ind);
                    end
                end
                
                temp = PriceChg{i};
                % control characters检查char(0:20)
                category = 'cntrl';
                tf = isstrprop(temp, category);
                ind = find( tf==1 )';
                temp(ind) = [];
                temp = str2double(temp);
                ind = 3;
                if ~isempty(temp)
                    StockTick(i,ind) = temp;
                else
                    if i>1
                        StockTick(i,ind) = StockTick(i-1,ind);
                    end
                end
                
                temp = Vol{i};
                % control characters检查char(0:20)
                category = 'cntrl';
                tf = isstrprop(temp, category);
                ind = find( tf==1 )';
                temp(ind) = [];
                temp = str2double(temp);
                ind = 4;
                if ~isempty(temp)
                    StockTick(i,ind) = temp;
                else
                    if i>1
                        StockTick(i,ind) = StockTick(i-1,ind);
                    end
                end
                
                temp = Amt{i};
                % control characters检查char(0:20)
                category = 'cntrl';
                tf = isstrprop(temp, category);
                ind = find( tf==1 )';
                temp(ind) = [];
                temp = str2double(temp);
                ind = 5;
                if ~isempty(temp)
                    StockTick(i,ind) = temp;
                else
                    if i>1
                        StockTick(i,ind) = StockTick(i-1,ind);
                    end
                end
                
                temp = SellBuyFlag{i};
                ind = 6;
                if strcmpi(temp,'买盘')
                    StockTick(i,ind) = 1;
                end
                if strcmpi(temp,'卖盘')
                    StockTick(i,ind) = -1;
                end
                if strcmpi(temp,'中性盘')
                    StockTick(i,ind) = 0;
                end
            end
            
            % StockTick = StockTick(end:(-1):1,:);
            %% 存储数据
            if 1 == obj.SaveFlag && ~isempty( StockTick )
                try
                    if ~isdir( FolderStr )
                        mkdir( FolderStr );
                    end
                    save(FileString,'StockTick','Header','-v7.3');
                    
                catch err
                    obj.str = ['日期时间：',datestr(now),' 数据保存失败：',err.message];
                    fprintf('%s\n',obj.str);
                    for i = 1:size(err.stack,1)
                        obj.str = ['FunName：',err.stack(i).name,' Line：',num2str(err.stack(i).line)];
                        fprintf('%s\n',obj.str);
                    end
                end
            end
            
            if isempty( StockTick )==0
                obj.str='数据获取成功 尝试启动trigger';
                disp(obj.str)
                notify(obj,'MessageUpdate')
                notify(obj,'FetchState');
                
            end
            
            QuantboxSendMail(obj.TargetAddress,obj.MessageHistory);
        end
        
        function obj=StockTSDay(obj)
            
            % Input:
            % StockCode:字符阵列型，表示证券代码，如sh600000
            % BeginDate:字符阵列型，表示希望获取股票数据所在时段的开始日期，如20140101
            % EndDate:字符阵列型，表示希望获取股票数据所在时段的结束日期，如20150101
            % Output:
            % StockDataDouble: 日期 开 高 低 收 量(股) 额(元) 复权因子（后复权因子）
            % 前复权因子 等于 后复权因子 的倒序排列
            % 涨跌幅复权方式
            % 后复权价格 = 交易价*后复权因子
            % 前复权价格 = 交易价/前复权因子
            
            % 获取数据所使用的URL
            % http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000562.phtml?year=1994&jidu=1
            % http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/000562.phtml?year=1995&jidu=4
            % http://biz.finance.sina.com.cn/stock/flash_hq/kline_data.php?symbol=sz000562&end_date=20150101&begin_date=19940101
            
            
            %  使用如下URL获取数据，可以获取自上市日开始的左右数据和复权因子 19900101 部分数据也有缺失
            % http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/000562.phtml?year=1995&jidu=4
            % 类似的所有来自新浪的数据源都会有部分数据缺失
            
            
            
            % 股票代码预处理，目标代码demo '600588'
            
            obj.StockCode(obj.StockCode=='.') = [];
            if strcmpi(obj.StockCode(1),'s')
                obj.StockCode = obj.StockCode(3:end);
            end
            if strcmpi(obj.StockCode(end),'h') ||  strcmpi(obj.StockCode(end),'z')
                obj.StockCode = obj.StockCode(1:end-2);
            end
            
            
            % 输入日期预处理
            if ~ischar( obj.BeginDate )
                obj.BeginDate = num2str(obj.BeginDate);
            end
            obj.BeginDate(obj.BeginDate == '-') = [];
            if ~ischar( obj.EndDate )
                obj.EndDate = num2str(obj.EndDate);
            end
            obj.EndDate(obj.EndDate == '-') = [];
            
            obj.StockDataDouble = [];
            adjfactor = [];
            
            
            %%
            % % http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/000562.phtml?year=1995&jidu=4
            
            sYear = str2double(obj.BeginDate(1:4));
            eYear = str2double(obj.EndDate(1:4));
            sM = str2double(obj.BeginDate(5:6));
            eM = str2double(obj.EndDate(5:6));
            for i = 1:4
                if sM>=3*i-2 && sM<=3*i
                    sJiDu = i;
                end
                if eM>=3*i-2 && eM<=3*i
                    eJiDu = i;
                end
            end
            
            Len = (eYear-sYear)*240+250;
            DTemp = cell(Len,8);
            rLen = 1;
            for i = sYear:eYear
                for j = 1:4
                    %             YearDemo = i
                    %             JiDuDemo = j
                    if i == sYear && j < sJiDu
                        continue;
                    end
                    if i == eYear && j > eJiDu
                        continue;
                    end
                    %             YearDemo = i
                    %             JiDuDemo = j
                    
                    URL = ...
                        ['http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/' ...
                        obj.StockCode '.phtml?year=' num2str(i) '&jidu=' num2str(j)];
                    
                    
                    
                    [~,TableCell] = GetTableFromWeb(URL);
                    
                    if iscell( TableCell ) && ~isempty(TableCell)
                        TableInd = 20;
                        FIndCell = TableCell{TableInd};
                    else
                        FIndCell = [];
                    end
                    
                    % 日期 开 高 收 低 量 额 复权因子
                    FIndCell = FIndCell(3:end,:);
                    FIndCell = FIndCell(end:(-1):1,:);
                    
                    if ~isempty(FIndCell)
                        LenTemp = size(FIndCell,1);
                        
                        DTemp(rLen:(rLen+LenTemp-1),:) = FIndCell;
                        rLen = rLen+LenTemp;
                    end
                end
            end
            DTemp(rLen:end,:) = [];
            % 由于新股刚上市或网络等原因，DTemp为空
            if isempty(DTemp)
                return;
            end
            % 日期 开 高 收 低 量 额 复权因子
            % 调整成
            % 日期 开 高 低 收 量 额 复权因子
            Low = DTemp(:,5);
            Close = DTemp(:,4);
            DTemp = [ DTemp(:,1:3),Low,Close,DTemp(:,6:end) ];
            
            sTemp = cell2mat(DTemp(:,1));
            sTemp = datestr( datenum(sTemp,'yyyy-mm-dd'),'yyyymmdd' );
            Date = str2num( sTemp );
            
            Temp = DTemp(:,2:end);
            Data = cellfun(@str2double,Temp);
            
            % 由后复权数据反向生成 除权除息数据
            for i = 1:4
                Data(:,i) = Data(:,i)./Data(:,7);
            end
            Data(:,1:4) = round( Data(:,1:4)*100 )/100;
            
            DTemp = [Date, Data];
            
            % BeginDate,EndDate
            sDate = str2double(obj.BeginDate);
            eDate = str2double(obj.EndDate);
            
            [~,sInd] = min( abs(DTemp(:,1)-sDate) );
            [~,eInd] = min( abs(DTemp(:,1)-eDate) );
            
            obj.StockDataDouble = DTemp(sInd:eInd,:);
            adjfactor = obj.StockDataDouble(:,end);
            if isempty( obj.StockDataDouble )==0
                obj.str='数据获取成功 尝试启动trigger';
                disp(obj.str)
                notify(obj,'MessageUpdate')
                notify(obj,'FetchState');
            end
            QuantboxSendMail(obj.TargetAddress,obj.MessageHistory);
        end
        function [OutputData,dStr] = GetCons(obj,varargin )
            OutputData = [];
            dStr = [];
            % %===输入参数检查 开始===
%            Flag=1;
%             if 0 == Flag
%                 str = ['请检查输入参数是否正确！'];
%                 disp(str)
%                 return;
%             end
%             
%             % %===输入参数检查 完毕===
%             
%             % 399704深证上游 399705深证中游 399706深证下游
%             % 399701深证F60 399702深证F120 399703深证F200
%             SpecialList = {'399704';'399705';'399706';'399701';'399702';'399703';};
%             
%             CustomList = {};
            
            FolderStr = ['./IndexCons'];
            if ~isdir( FolderStr )
                mkdir( FolderStr );
            end
            
            FileName = [obj.StockCode,'成分股'];
            FileString = [FolderStr,'/',FileName,'.xls'];
            FileExist = 0;
            if exist(FileString, 'file') == 2
                FileExist = 1;
            end
            if 1 == FileExist
                FileString = [FolderStr,'/',FileName,'(1)','.xls'];
            end
            
%             if obj.StockCode(1) == '3' && ~ismember(obj.StockCode,SpecialList)
%                 % http://www.cnindex.com.cn/docs/yb_399005.xls
%                 URL = ['http://www.cnindex.com.cn/docs/yb_',obj.StockCode,'.xls'];
%                 
%                 try
%                     outfilename = websave(FileString,URL);
%                 catch
%                     str = ['数据获取失败，请检查输入的指数代码！',obj.StockCode];
%                     disp(str);
%                     return;
%                 end
%                 
%                 [num,txt,raw] = xlsread(outfilename);
%                 
%                 dStr = raw{1,8};
%                 
%                 OutputData = raw(:,3:6);
%                 OutputData(1,:) = {'Code','Name','Weight','Industry'};
%                 
%             else
%                    URL = ['http://www.csindex.com.cn/sseportal/ps/zhs/hqjt/csi/',num2str(obj.StockCode),'cons.xls'];
%             
                URL = ['http://115.29.204.48/webdata/',num2str(obj.StockCode),'cons.xls'];
               
                try
                    outfilename = websave(FileString,URL);
                catch
                    obj.str = ['数据获取失败，请检查输入的指数代码！',obj.StockCode];
                    disp(obj.str);
                    return;
                end
                
                [~,sheets] = xlsfinfo(outfilename);
                dStr = ['更新时间：',sheets{1,1}];
                
                [~,~,raw] = xlsread(outfilename);
                
                obj.Component = raw;
                 obj.Component(1,:) = {'Code','Name','Name(Eng)','Exchange'};
                
%             end
%             
            
         
            
        end
        function [obj,InitialDate] = Index(obj)
            
            % Input:
            % StockCode:字符阵列型，表示证券代码，如sh000001
            % BeginDate:字符阵列型，表示希望获取股票数据所在时段的开始日期，如20140101
            % EndDate:字符阵列型，表示希望获取股票数据所在时段的结束日期，如20150101
            % Output:
            % Data: 日期 开 高 低 收 量(股) 额(元)
            
            % 获取数据所使用的URL
            % http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000001/type/S.phtml?year=1990&jidu=4
            % http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000300/type/S.phtml?year=2014&jidu=4
            %% 输入输出预处理
            
            GetInitialDateFlag = 0;
            
            if nargin < 3 || isempty(obj.EndDate)
                obj.EndDate = '20160101';
            end
            if nargin < 2 || isempty(obj.BeginDate)
                obj.BeginDate = '20040101';
            end
            if nargin < 1 || isempty(obj.StockCode)
                obj.StockCode = '600300';
            end
            
            % 代码预处理，目标代码demo '000001'
            if strcmpi(obj.StockCode(1),'s')
                obj.StockCode = obj.StockCode(3:end);
            end
            if strcmpi(obj.StockCode(end),'h') ||  strcmpi(obj.StockCode(end),'z')
                obj.StockCode = obj.StockCode(1:end-2);
            end
            
            % 日期时间预处理，目标形式 '20140101'
            obj.BeginDate(obj.BeginDate == '-') = [];
            obj.EndDate(obj.EndDate == '-') = [];
            
            obj.Data = [];
            InitialDate = '19900101';
            
            charset = 'gb2312';
            %% 获取初始日期
            if 1 == GetInitialDateFlag
                URL = ...
                    ['http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/' ...
                    obj.StockCode '/type/S.phtml?year=2014&jidu=4'];
                
                if verLessThan('matlab', '8.3')
                    [URLchar, status] = urlread_General(URL, 'Charset', charset, 'TimeOut', 60);
                else
                    [URLchar, status] = urlread(URL, 'Charset', charset, 'TimeOut', 60);
                end
                if status == 0
                    obj.str = ['urlread error:网页读取失败！请检查输入的网址或网络连接情况！'];
                    disp(obj.str);
                    return;
                end
                
                URLString = java.lang.String(URLchar);
                
                expr = ['<select name="year">','.*?', ...
                    '</select>'];
                Content = regexpi(URLchar, expr,'match');
                if ~isempty( Content )
                    Content = Content{1};
                    expr = ['<option value=','.*?', ...
                        '</option>'];
                    tContent = regexpi(Content, expr,'match');
                    if ~isempty( tContent )
                        tContent = tContent{length(tContent)};
                        expr = ['>','.*?', ...
                            '<'];
                        tC = regexpi(tContent, expr,'match');
                        tC = tC{1};
                        temp = tC(2:length(tC)-1);
                        InitialDate = [temp,'0101'];
                    end
                end
            end
            %% Get Data
            
            % http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000300/type/S.phtml?year=2014&jidu=4
            
            sYear = str2double(obj.BeginDate(1:4));
            eYear = str2double(obj.EndDate(1:4));
            sM = str2double(obj.BeginDate(5:6));
            eM = str2double(obj.EndDate(5:6));
            for i = 1:4
                if sM>=3*i-2 && sM<=3*i
                    sJiDu = i;
                end
                if eM>=3*i-2 && eM<=3*i
                    eJiDu = i;
                end
            end
            
            Len = (eYear-sYear)*240+250;
            DTemp = cell(Len,7);
            rLen = 1;
            for i = sYear:eYear
                for j = 1:4
                    %             YearDemo = i
                    %             JiDuDemo = j
                    if i == sYear && j < sJiDu
                        continue;
                    end
                    if i == eYear && j > eJiDu
                        continue;
                    end
                    %             YearDemo = i
                    %             JiDuDemo = j
                    
                    URL = ...
                        ['http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/' ...
                        obj.StockCode '/type/S.phtml?year=' num2str(i) '&jidu=' num2str(j)];
                    
                    [~,TableCell] = GetTableFromWeb(URL);
                    
                    if iscell( TableCell ) && ~isempty(TableCell) && size(TableCell,1)>4
                        TableInd = 5;
                        FIndCell = TableCell{TableInd};
                    else
                        FIndCell = [];
                    end
                    
                    % 日期 开 高 收 低 量 额
                    FIndCell = FIndCell(3:end,:);
                    FIndCell = FIndCell(end:(-1):1,:);
                    
                    if ~isempty(FIndCell)
                        LenTemp = size(FIndCell,1);
                        
                        DTemp(rLen:(rLen+LenTemp-1),:) = FIndCell;
                        rLen = rLen+LenTemp;
                    end
                end
            end
            DTemp(rLen:end,:) = [];
            % 由于新上市或网络等原因，DTemp为空
            if isempty(DTemp)
                return;
            end
            % 日期 开 高 收 低 量 额
            % 调整成
            % 日期 开 高 低 收 量 额
            Low = DTemp(:,5);
            Close = DTemp(:,4);
            DTemp = [ DTemp(:,1:3),Low,Close,DTemp(:,6:end) ];
            
            sTemp = cell2mat(DTemp(:,1));
            sTemp = datestr( datenum(sTemp,'yyyy-mm-dd'),'yyyymmdd' );
            Date = str2num( sTemp );
            
            Temp = DTemp(:,2:end);
            obj.Data = cellfun(@str2double,Temp);
            
            DTemp = [Date, obj.Data];
            
            % BeginDate,EndDate
            sDate = str2double(obj.BeginDate);
            eDate = str2double(obj.EndDate);
            
            [~,sInd] = min( abs(DTemp(:,1)-sDate) );
            [~,eInd] = min( abs(DTemp(:,1)-eDate) );
            
            obj.Data = DTemp(sInd:eInd,:);
        end
        function [NoticeDataCell] = StockNotice(obj)
            
            %{
http://www.cninfo.com.cn/search/stockfulltext.jsp?
orderby=date11
&noticeType=0107&keyword=
&startTime=2005-01-01&endTime=2014-12-31
&stockCode=600588&pageNo=1
            %}
            %% 输入输出预处理
            Charset = 'gb2312';
            
            
            % 股票代码预处理，目标代码demo '600588'
            if strcmpi(obj.StockCode(1),'s')
                obj.StockCode = obj.StockCode(3:end);
            end
            if strcmpi(obj.StockCode(end),'h') ||  strcmpi(obj.StockCode(end),'z')
                obj.StockCode = obj.StockCode(1:end-2);
            end
            
            % 日期预处理，目标形式2014-12-29
            ind = find( obj.BeginDate == '-',1 );
            if isempty(ind)
                obj.BeginDate = [obj.BeginDate(1:4),'-',obj.BeginDate(5:6),'-',obj.BeginDate(7:end)];
            end
            ind = find( obj.EndDate == '-',1 );
            if isempty(ind)
                obj.EndDate = [obj.EndDate(1:4),'-',obj.EndDate(5:6),'-',obj.EndDate(7:end)];
            end
            
            NoticeDataCell = [];
            %% NoticeTypeCell
            
            NoticeTypeCell = {'010301','年度报告'; ...
                '010303','半年度报告'; ...
                '010305','一季度报告'; ...
                '010307','三季度报告'; ...
                '0102','首次公开发行及上市'; ...
                '0105','配股'; ...
                '0107','增发'; ...
                '0109','可转换债券'; ...
                '0110','权证相关公告'; ...
                '0111','其它融资'; ...
                '0113','权益及限制出售股份'; ...
                '0115','股权变动'; ...
                '0117','交易'; ...
                '0119','股东大会'; ...
                '0121','澄清、风险、业绩预告'; ...
                '0125','特别处理和退市'; ...
                '0127','补充及更正'; ...
                '0129','中介机构报告'; ...
                '0131','上市公司制度'; ...
                '0123','其它重大事项'; ...
                };
            %% NoticeDataCell
            
            Head = {'StockCode','DateTime','Title','NoticeType','FileURL','FileSize'};
            NoticeDataCell = [Head;NoticeDataCell];
            Rnum = size(NoticeTypeCell,1);
            
            % 1:Rnum
            for i = 1:Rnum
                
                obj.str = ['========='];
                disp(obj.str);
                notify(obj,'MessageUpdate')
                i
                NoticeTypeCell{i,2}
                obj.str = ['============'];
                disp(obj.str);
                notify(obj,'MessageUpdate')
                
                obj.NoticeType = NoticeTypeCell{i,1};
                %     NoticeType = [];
                tCell = [];
                if strcmpi(obj.NoticeType,'All')
                    obj.NoticeType = [];
                end
                
                Head = {'StockCode','DateTime','Title','NoticeType','FileURL','FileSize'};
                NoticeTypeCell = {'010301','年度报告'; ...
                    '010303','半年度报告'; ...
                    '010305','一季度报告'; ...
                    '010307','三季度报告'; ...
                    '0102','首次公开发行及上市'; ...
                    '0105','配股'; ...
                    '0107','增发'; ...
                    '0109','可转换债券'; ...
                    '0110','权证相关公告'; ...
                    '0111','其它融资'; ...
                    '0113','权益及限制出售股份'; ...
                    '0115','股权变动'; ...
                    '0117','交易'; ...
                    '0119','股东大会'; ...
                    '0121','澄清、风险、业绩预告'; ...
                    '0125','特别处理和退市'; ...
                    '0127','补充及更正'; ...
                    '0129','中介机构报告'; ...
                    '0131','上市公司制度'; ...
                    '0123','其它重大事项'; ...
                    };
                if ~isempty(obj.NoticeType)
                    Temp = cellfun(@(x)strcmpi(x,obj.NoticeType),NoticeTypeCell(:,1));
                    obj.NoticeTypeWord = NoticeTypeCell{Temp,2};
                else
                    obj.NoticeTypeWord = [];
                end
                %% URL生成
                
                %{
                    http://www.cninfo.com.cn/search/stockfulltext.jsp?
                    orderby=date11
                    &noticeType=0107&keyword=
                    &startTime=2005-01-01&endTime=2014-12-31
                    &stockCode=600588&pageNo=1
                %}
                
                
                URL = ['http://www.cninfo.com.cn/search/stockfulltext.jsp?orderby=date11', ...
                    '&noticeType=',obj.NoticeType,'&keyword=',...
                    '&startTime=',obj.BeginDate,'&endTime=',obj.EndDate,'&stockCode=',obj.StockCode, ...
                    '&pageNo=1'];
                
                %% 数据获取
                Charset = 'gb2312';
                if verLessThan('matlab', '8.3')
                    [obj.URLchar, status] = urlread_General(URL, 'Charset', Charset, 'TimeOut', 60);
                else
                    [obj.URLchar, status] = urlread(URL, 'Charset', Charset, 'TimeOut', 60);
                end
                if status == 0
                    obj.str = ['urlread error:网页读取失败！请检查输入的网址或网络连接情况！'];
                    disp(obj.str);
                    notify(obj,'MessageUpdate')
                    return;
                end
                
                % URLString = java.lang.String(URLchar);
                
                expr = ['<span class="count"','.*?', ...
                    '</span>'];
                Temp = regexpi(obj.URLchar, expr,'match');
                Temp = Temp{1};
                
                expr = ['共','.*?', ...
                    '条'];
                Temp = regexpi(obj.URLchar, expr,'match');
                Temp = Temp{1};
                Temp = Temp(2:end-1);
                Temp = str2num(Temp);
                if Temp == 0
                    return;
                end
                %% 正则处理
                
                %% 输入输出预处理
                if isempty( obj.URLchar )
                    DataCell = [];
                    return;
                end
                DataCell = [];
                Head = {'StockCode','DateTime','Title','NoticeType','FileURL','FileSize'};
                %%
                
                % &rsv_page=2
                expr = ['<td class="qsgg">','.*?',...
                    '</tr>'];
                [matchstart,matchend,tokenindices,matchstring,tokenstring,tokenname,splitstring] = ...
                    regexpi(obj.URLchar, expr);
                Len = numel(matchstring);
                if Len>0
                    
                    ColNum = length(Head);
                    DataCell = cell(Len, ColNum);
                    % Head = {'DateTime','StockCode','Title','NoticeType','FileURL','FileSize'};
                    for i = 1:Len
                        
                        DebugItermNum = i
                        
                        DataCell{i,1} = obj.StockCode;
                        DataCell{i,4} = obj.NoticeTypeWord;
                        StringTemp = matchstring{i};
                        
                        expr = ['<a href=','.*?',...
                            '</a>'];
                        TitleURL = regexpi(StringTemp, expr,'match');
                        if ~isempty(TitleURL)
                            TitleURL = TitleURL{1};
                            
                            expr = ['>','.*?',...
                                '</a>'];
                            out = regexpi(TitleURL, expr,'match');
                            out = out{1};
                            temp = out(2:end-length('</a>'));
                            % % % 简易预处理清洗，剔除<em> </em>
                            expr = ['<.*?em>'];
                            replace = '';
                            temp = regexprep(temp,expr,replace);
                            % Title
                            DataCell{i,3} = temp;
                            
                            expr = ['"'];
                            out = regexpi(TitleURL, expr,'split');
                            out = out{2};
                            temp = out;
                            % URL
                            DataCell{i,5} = ['http://www.cninfo.com.cn/',temp];
                        else
                            % Title
                            DataCell{i,3} = [];
                            % URL
                            DataCell{i,5} = [];
                        end
                        
                        % % FileSize
                        expr = ['<img','.*?',...
                            '</td>'];
                        out = regexpi(StringTemp, expr,'match');
                        if ~isempty(out)
                            out = out{1};
                            expr = ['width=16> (','.*?',...
                                ') </td>'];
                            out = regexpi(out, expr,'match');
                            out = out{1};
                            ind = (1+length('width=16> (')):(length(out)-length(') </td>'));
                            temp = out(ind);
                        else
                            temp = [];
                        end
                        DataCell{i,6} = temp;
                        
                        % % DateTime
                        expr = ['<td class="ggsj"','.*?',...
                            '</td>'];
                        DateTime = regexpi(StringTemp, expr,'match');
                        if ~isempty(DateTime)
                            DateTime = DateTime{1};
                            expr = ['>','.*?',...
                                '</td>'];
                            out = regexpi(DateTime, expr,'match');
                            out = out{1};
                            expr = ['&nbsp;'];
                            out = regexprep(out, expr,'');
                            temp = out(2:end-length('</td>'));
                        else
                            temp = [];
                        end
                        DataCell{i,2} = temp;
                    end
                    
                    DataCell = [Head;DataCell];
                    
                    
                end
                
                %% 获取其他页码的搜索结果
                
                DCell = [];
                
                expr = ['onclick=','''','goPage(','.*?', ...
                    '<'];
                PageStr = regexpi(obj.URLchar, expr,'match');
                if ~isempty(PageStr)
                    PageStr = PageStr(end);
                    PageStr = PageStr{1};
                    
                    expr = ['>','.*?', ...
                        '<'];
                    MatchStr = regexpi(PageStr, expr,'match');
                    MatchStr = MatchStr{1};
                    MatchStr = regexprep(MatchStr,'>','');
                    MatchStr = regexprep(MatchStr,'<','');
                    Len = str2double(MatchStr);
                else
                    Len = 0;
                end
                
                if Len > 1
                    % 2:Len
                    for i = 2:Len
                        
                        PageNumDebug = i
                        
                        tURL = ['http://www.cninfo.com.cn/search/stockfulltext.jsp?orderby=date11', ...
                            '&noticeType=',obj.NoticeType,'&keyword=',...
                            '&startTime=',obj.BeginDate,'&endTime=',obj.EndDate,'&stockCode=',obj.StockCode, ...
                            '&pageNo=',num2str(i)];
                        
                        if verLessThan('matlab', '8.3')
                            [obj.URLchar, status] = urlread_General(tURL, 'Charset', Charset, 'TimeOut', 60);
                        else
                            [obj.URLchar, status] = urlread(tURL, 'Charset', Charset, 'TimeOut', 60);
                        end
                        
                        if status == 0
                            obj.str = ['urlread error:网页读取失败！请检查输入的网址或网络连接情况！'];
                            disp(obj.str);
                            notify(obj,'MessageUpdate')
                            obj.URLchar = [];
                        end
                        
                        
                        %% 输入输出预处理
                        if isempty( obj.URLchar )
                            tData = [];
                            return;
                        end
                        tData = [];
                        Head = {'StockCode','DateTime','Title','NoticeType','FileURL','FileSize'};
                        %%
                        
                        % &rsv_page=2
                        expr = ['<td class="qsgg">','.*?',...
                            '</tr>'];
                        [matchstart,matchend,tokenindices,matchstring,tokenstring,tokenname,splitstring] = ...
                            regexpi(URLchar, expr);
                        Len = numel(matchstring);
                        if Len>0
                            
                            ColNum = length(Head);
                            tData = cell(Len, ColNum);
                            % Head = {'DateTime','StockCode','Title','NoticeType','FileURL','FileSize'};
                            for i = 1:Len
                                
                                DebugItermNum = i
                                
                                tData{i,1} = obj.StockCode;
                                tData{i,4} = obj.NoticeTypeWord;
                                StringTemp = matchstring{i};
                                
                                expr = ['<a href=','.*?',...
                                    '</a>'];
                                TitleURL = regexpi(StringTemp, expr,'match');
                                if ~isempty(TitleURL)
                                    TitleURL = TitleURL{1};
                                    
                                    expr = ['>','.*?',...
                                        '</a>'];
                                    out = regexpi(TitleURL, expr,'match');
                                    out = out{1};
                                    temp = out(2:end-length('</a>'));
                                    % % % 简易预处理清洗，剔除<em> </em>
                                    expr = ['<.*?em>'];
                                    replace = '';
                                    temp = regexprep(temp,expr,replace);
                                    % Title
                                    tData{i,3} = temp;
                                    
                                    expr = ['"'];
                                    out = regexpi(TitleURL, expr,'split');
                                    out = out{2};
                                    temp = out;
                                    % URL
                                    tData{i,5} = ['http://www.cninfo.com.cn/',temp];
                                else
                                    % Title
                                    tData{i,3} = [];
                                    % URL
                                    tData{i,5} = [];
                                end
                                
                                % % FileSize
                                expr = ['<img','.*?',...
                                    '</td>'];
                                out = regexpi(StringTemp, expr,'match');
                                if ~isempty(out)
                                    out = out{1};
                                    expr = ['width=16> (','.*?',...
                                        ') </td>'];
                                    out = regexpi(out, expr,'match');
                                    out = out{1};
                                    ind = (1+length('width=16> (')):(length(out)-length(') </td>'));
                                    temp = out(ind);
                                else
                                    temp = [];
                                end
                                tData{i,6} = temp;
                                
                                % % DateTime
                                expr = ['<td class="ggsj"','.*?',...
                                    '</td>'];
                                DateTime = regexpi(StringTemp, expr,'match');
                                if ~isempty(DateTime)
                                    DateTime = DateTime{1};
                                    expr = ['>','.*?',...
                                        '</td>'];
                                    out = regexpi(DateTime, expr,'match');
                                    out = out{1};
                                    expr = ['&nbsp;'];
                                    out = regexprep(out, expr,'');
                                    temp = out(2:end-length('</td>'));
                                else
                                    temp = [];
                                end
                                tData{i,2} = temp;
                            end
                            
                            tData = [Head;tData];
                            
                            
                        end
                        DCell = [DCell;tData(2:end,:)];
                    end
                end
                
                %% 输出
                
                tCell = [DataCell;DCell];
                
                if isempty(tCell)
                    return;
                end
                
                temp1 = tCell(1,:);
                temp2 = tCell(end:(-1):2,:);
                
                tCell = [temp1;temp2];
                
                NoticeDataCell = [NoticeDataCell;tCell(2:end,:)];
            end
            
            if size(NoticeDataCell,1) == 1
                NoticeDataCell = [];
                return;
            end
            %%  NoticeDataCell按照时间进行排序
            tH = NoticeDataCell(1,:);
            tD = NoticeDataCell(2:end,:);
            
            Temp = cellfun( @Dstr2Dnum,tD(:,2) );
            [~,I] = sort(Temp);
            
            temp = tD(I,:);
            NoticeDataCell = [tH;temp];
            if isempty(NoticeDataCell)==0
                notify(obj,'FetchState');
            end
            QuantboxSendMail(obj.TargetAddress,obj.MessageHistory);
        end
    end
    methods %%For Saving
        function [SaveLog,ProbList,NewList] = SaveStockTSDay(obj)
            % by LiYang_faruto
            % Email:farutoliyang@foxmail.com
            % 2014/12/12
            % AdjFlag 0:除权时序数据 1:前复权时序数据 2:后复权时序数据
            % XRDFlag 0:不获取除权除息信息 1:获取除权除息信息
            %% 输入输出预处理
            XRDFlag = 1;
            AdjFlag = 0;
            SaveLog = [];
            ProbList = [];
            NewList = [];
            sqlquery=['select * from StockList'];
            cursor=exec(conn,sqlquery);
            cursor=fetch(cursor);
            StockList=cursor.Data;
            Len = size(StockList, 1);
            obj.StockCode = StockList(:,1);
            
            
            if 1 == XRDFlag
                AdjFlag = 0;
            end
            Date_G = '19900101';
            %%
            % 除权时序数据
            if 0 == AdjFlag
                FolderStr = ['./DataBase/Stock/Day_ExDividend_mat'];
                if ~isdir( FolderStr )
                    mkdir( FolderStr );
                end
                
                ticID = tic;
                for i = 1:Len
                    disp('======')
                    RunIndex = i
                    Scode = obj.StockCode{i}
                    
                    obj.str= ['RunIndex',num2str(RunIndex)];
                    notify(obj,'FetchState');
                    obj.str=['Scode',Scode];
                    notify(obj,'FetchState');
                    
                    disp('============')
                    
                    % DebugMode
                    DebugMode_OnOff = 0;
                    if 1 == DebugMode_OnOff
                        if strcmpi(Scode,'sh603011')~=1
                            continue;
                        end
                        
                    end
                    
                    FileString = [FolderStr,'/',obj.StockCode{i},'_D_ExDiv.mat'];
                    FileExist = 0;
                    if exist(FileString, 'file') == 2
                        FileExist = 1;
                    end
                    
                    % 本地数据存在，进行尾部更新添加
                    if 1 == FileExist
                        try
                            
                            MatObj = matfile(FileString,'Writable',true);
                            [nrows, ~]=size(MatObj,'StockData');
                            
                            OffSet = 4;
                            
                            if nrows-OffSet>1
                                
                                len = nrows;
                                Temp = MatObj.StockData(len-OffSet,1);
                                DateTemp = datestr( datenum(num2str(Temp),'yyyymmdd'),'yyyymmdd' );
                                
                                StockCodeInput = Scode;
                                obj.BeginDate = DateTemp;
                                obj.EndDate = datestr(today, 'yyyymmdd');
                                
                                StockDataDouble = GetStockTSDay_Web(StockCodeInput,obj.BeginDate,obj.EndDate);
                                if isempty(StockDataDouble)
                                    obj.str = [ obj.StockCode{i},'-',StockName{i}, ' 数据获取失败，请检查！' ];
                                    disp(obj.str);
                                    notify(obj,'FetchState');
                                    LenTemp = size( ProbList,1 )+1;
                                    
                                    ProbList{LenTemp,1} = Scode;
                                    continue;
                                end
                                
                                MatObj.StockData = ...
                                    [MatObj.StockData(1:nrows-OffSet-1,:);StockDataDouble];
                                
                            else % % 本地数据存在，但为空
                                LenTemp = size( NewList,1 )+1;
                                
                                NewList{LenTemp,1} = Scode;
                                
                                % 获取上市日期
                                StockCodeInput = Scode;
                                IPOdate = GetBasicInfo_Mat(StockCodeInput,[],[],'Stock','IPOdate');
                                if ~isempty(IPOdate)
                                    DateTemp = IPOdate;
                                else
                                    DateTemp = Date_G;
                                end
                                DateTemp = num2str(DateTemp);
                                
                                StockCodeInput = Scode;
                                obj.BeginDate = DateTemp;
                                obj.EndDate = datestr(today, 'yyyymmdd');
                                
                                StockDataDouble = GetStockTSDay_Web(StockCodeInput,obj.BeginDate,obj.EndDate);
                                if isempty(StockDataDouble)
                                    obj.str = [ obj.StockCode{i},'-',StockName{i}, ' 数据获取失败，请检查！' ];
                                    disp(obj.str);
                                    notify(obj,'FetchState');
                                    LenTemp = size( ProbList,1 )+1;
                                    
                                    ProbList{LenTemp,1} = Scode;
                                    continue;
                                end
                                
                                StockData = StockDataDouble;
                                
                                save(FileString,'StockData', '-v7.3');
                                MatObj.StockData = StockDataDouble;
                                
                            end
                        catch
                            obj.str = [ obj.StockCode{i},'-',StockName{i}, ' 数据载入失败或其他原因数据更新失败，将重新下载数据！' ];
                            disp(obj.str);
                            notify(obj,'FetchState');
                            FileExist = 0;
                        end
                    end
                    
                    % 本地数据不存在
                    if 0 == FileExist
                        LenTemp = size( NewList,1 )+1;
                        
                        NewList{LenTemp,1} = Scode;
                        
                        % 获取上市日期
                        StockCodeInput = Scode;
                        IPOdate = GetBasicInfo_Mat(StockCodeInput,[],[],'Stock','IPOdate');
                        if ~isempty(IPOdate)
                            DateTemp = IPOdate;
                        else
                            DateTemp = Date_G;
                        end
                        DateTemp = num2str(DateTemp);
                        
                        StockCodeInput = Scode;
                        obj.BeginDate = DateTemp;
                        obj.EndDate = datestr(today, 'yyyymmdd');
                        
                        StockDataDouble = GetStockTSDay_Web(StockCodeInput,obj.BeginDate,obj.EndDate);
                        if isempty(StockDataDouble)
                            obj.str = [ obj.StockCode{i},'-',StockName{i}, ' 数据获取失败，请检查！' ];
                            disp(obj.str);
                            LenTemp = size( ProbList,1 )+1;
                            
                            ProbList{LenTemp,1} = Scode;
                            continue;
                        end
                        
                        StockData = StockDataDouble;
                        
                        save(FileString,'StockData', '-v7.3');
                        
                    end
                    
                    NewListLen = size(NewList,1)
                    ProbListLen = size(ProbList,1)
                    
                    elapsedTimeTemp = toc(ticID);
                    obj.str = [ '循环已经累计耗时', num2str(elapsedTimeTemp), ' seconds(',num2str(elapsedTimeTemp/60), ' minutes)',...
                        '(',num2str(elapsedTimeTemp/60/60), ' hours)',];
                    disp(obj.str);
                    notify(obj,'FetchState');
                    obj.str = ['Now Time:',datestr(now,'yyyy-mm-dd HH:MM:SS')];
                    disp(obj.str);
                    notify(obj,'FetchState');
                end
                
            end
            %% 前复权时序数据
            %             if 1 == AdjFlag
            %                 FolderStrD_Ex = ['./DataBase/Stock/Day_ExDividend_mat'];
            %                 FolderStr = ['./DataBase/Stock/Day_ForwardAdj_mat'];
            %                 if ~isdir( FolderStr )
            %                     mkdir( FolderStr );
            %                 end
            %
            %                 ticID = tic;
            %                 for i = 1:Len
            %                     disp('======')
            %                     RunIndex = i
            %                     Scode = StockCode{i}
            %                     Sname = StockName{i}
            %                     obj.str= ['RunIndex',num2str(RunIndex)];
            %                     notify(obj,'FetchState');
            %                     obj.str=['Scode',Scode];
            %                     notify(obj,'FetchState');
            %                     obj.str=['Sname',Sname];
            %                     notify(obj,'FetchState');
            %                     disp('============')
            %
            %                     FileStringD_Ex = [FolderStrD_Ex,'/',Scode,'_D_ExDiv.mat'];
            %                     FileString = [FolderStr,'/',Scode,'_D_ForwardAdj.mat'];
            %
            %                     FileExist = 0;
            %                     if exist(FileStringD_Ex, 'file') == 2
            %                         FileExist = 1;
            %                     end
            %
            %                     % % 本地数据存在，进行尾部更新添加
            %                     if 1 == FileExist
            %                         try
            %                             str = ['load ',FileStringD_Ex];
            %                             eval(str);
            %
            %                             if ~isempty(StockData)
            %
            %                                 XRD_Data = [];
            %
            %                                 [StockDataXRD, factor] = CalculateStockXRD(StockData, XRD_Data, AdjFlag);
            %                                 StockData = StockDataXRD;
            %                                 save(FileString,'StockData', '-v7.3');
            %                             end
            %                         catch
            %                             obj.str = [ StockCode{i},'-',StockName{i}, ' 数据载入失败或其他原因数据更新失败' ];
            %                             disp(obj.str);
            %                             notify(obj,'FetchState')
            %                             FileExist = 0;
            %                         end
            %                     end
            %
            %                     NewListLen = size(NewList,1)
            %                     ProbListLen = size(ProbList,1)
            %
            %                     elapsedTimeTemp = toc(ticID);
            %                     str = [ '循环已经累计耗时', num2str(elapsedTimeTemp), ' seconds(',num2str(elapsedTimeTemp/60), ' minutes)',...
            %                         '(',num2str(elapsedTimeTemp/60/60), ' hours)',];
            %                     disp(str);
            %                     str = ['Now Time:',datestr(now,'yyyy-mm-dd HH:MM:SS')];
            %                     disp(str);
            %                 end
            %             end
            %%
            %             %% 后复权时序数据
            %             if 2 == AdjFlag
            %                 FolderStrD_Ex = ['./DataBase/Stock/Day_ExDividend_mat'];
            %                 FolderStr = ['./DataBase/Stock/Day_BackwardAdj_mat'];
            %                 if ~isdir( FolderStr )
            %                     mkdir( FolderStr );
            %                 end
            %
            %                 ticID = tic;
            %                 for i = 1:Len
            %                     disp('======')
            %                     RunIndex = i
            %                     Scode = StockCode{i}
            %                     Sname = StockName{i}
            %                     disp('============')
            %
            %                     FileStringD_Ex = [FolderStrD_Ex,'/',StockCode{i},'_D_ExDiv.mat'];
            %                     FileString = [FolderStr,'/',StockCode{i},'_D_BackwardAdj.mat'];
            %
            %                     FileExist = 0;
            %                     if exist(FileStringD_Ex, 'file') == 2
            %                         FileExist = 1;
            %                     end
            %
            %                     % % 本地数据存在，进行尾部更新添加
            %                     if 1 == FileExist
            %                         try
            %                             str = ['load ',FileStringD_Ex];
            %                             eval(str);
            %
            %                             if ~isempty(StockData)
            %
            %                                 XRD_Data = [];
            %
            %                                 [StockDataXRD, factor] = CalculateStockXRD(StockData, XRD_Data, AdjFlag);
            %                                 StockData = StockDataXRD;
            %                                 save(FileString,'StockData', '-v7.3');
            %                             end
            %                         catch
            %                             str = [ StockCode{i},'-',StockName{i}, ' 数据载入失败或其他原因数据更新失败' ];
            %                             disp(str);
            %                             FileExist = 0;
            %                         end
            %                     end
            %
            %                     NewListLen = size(NewList,1)
            %                     ProbListLen = size(ProbList,1)
            %
            %                     elapsedTimeTemp = toc(ticID);
            %                     str = [ '循环已经累计耗时', num2str(elapsedTimeTemp), ' seconds(',num2str(elapsedTimeTemp/60), ' minutes)',...
            %                         '(',num2str(elapsedTimeTemp/60/60), ' hours)',];
            %                     disp(str);
            %                     str = ['Now Time:',datestr(now,'yyyy-mm-dd HH:MM:SS')];
            %                     disp(str);
            %                 end
            %             end
            %% 获取除权除息信息
            if 1 == XRDFlag
                FolderStr = ['./DataBase/Stock/XRDdata_mat'];
                if ~isdir( FolderStr )
                    mkdir( FolderStr );
                end
                ticID = tic;
                for i = 1:Len
                    disp('======')
                    RunIndex = i
                    Scode = obj.StockCode{i}
                    
                    obj.str= ['RunIndex',num2str(RunIndex)];
                    notify(obj,'FetchState');
                    obj.str=['Scode',Scode];
                    notify(obj,'FetchState');
                    
                    disp('============')
                    
                    FileString = [FolderStr,'/',obj.StockCode{i},'_XRD.mat'];
                    
                    StockCodeInput = Scode;
                    [ Web_XRD_Data , Web_XRD_Cell_1 , Web_XRD_Cell_2 ] = GetStockXRD_Web(StockCodeInput);
                    
                    if isempty(Web_XRD_Data)
                        str = [ StockCode{i},'-',StockName{i}, ' 数据获取失败或该股票无除权除息信息，请检查！' ];
                        disp(str);
                        LenTemp = size( ProbList,1 )+1;
                        
                        ProbList{LenTemp,1} = Scode;
                    else
                        save(FileString,'Web_XRD_Data','Web_XRD_Cell_1','Web_XRD_Cell_2', '-v7.3');
                    end
                    
                    NewListLen = size(NewList,1)
                    ProbListLen = size(ProbList,1)
                    
                    elapsedTimeTemp = toc(ticID);
                    obj.str = [ '循环已经累计耗时', num2str(elapsedTimeTemp), ' seconds(',num2str(elapsedTimeTemp/60), ' minutes)',...
                        '(',num2str(elapsedTimeTemp/60/60), ' hours)',];
                    disp(obj.str);
                    notify(obj,'FetchState');
                end
            end
            %% 发送邮件通知
            
            % str = datestr(now,'yyyy-mm-dd HH:MM:SS');
            % if AdjFlag == 1
            %     subject = [str,' 股票日线数据（前复权）更新完毕'];
            % else
            %     subject = [str,' 股票日线数据（不复权）更新完毕'];
            % end
            %
            % content = [];
            % content{1,1} = [str,' 股票日线数据更新完毕'];
            %
            % Temp = StockD.DataCell;
            % Temp = Temp(end,1);
            % if iscell(Temp)
            %     Temp = Temp{1};
            % end
            % str = [ '股票日线数据已更新至', num2str(Temp) ];
            % content{length(content)+1,1} = str;
            % if ~isempty(IndNew)
            %     content{length(content)+1,1} = '新增加个股：';
            %     for i = 1: length(IndNew);
            %         content{length(content)+1,1} = cell2mat( StockList(IndNew(i),:) );
            %     end
            % end
            % str = [ '共耗时', num2str(elapsedTime), ' seconds(',num2str(elapsedTime/60), ' minutes)', ...
            %        '(',num2str(elapsedTime/60/60), ' hours)'];
            % content{length(content)+1,1} = str;
            % str = [ '个股数量为', num2str(length(StockList)) ];
            % content{length(content)+1,1} = str;
            %
            % TargetAddress = 'faruto@foxmail.com'; %目标邮箱地址
            % MatlabSentMail(subject, content, TargetAddress);
        end
    end
    methods %%For 集成式数据清洗
        function obj=Bat(obj,varigin)
            sqlquery='select * from StockList';
            cursor=exec(obj.ConnCloud,sqlquery);
            cursor=fetch(cursor);
            StockList=cursor.Data;
            
            Len = size(StockList, 1);
            StockCodeList = StockList(:,2);
            for i = 1:6
                disp('======')
                obj.RunIndex = i;
                i
                Scode = StockCodeList{i}
                obj.StockCode=Scode;
                
                disp('============')
                
                Date_G = '20040101';
                
                DateTemp = num2str(Date_G);
                
                StockCodeInput = Scode;
                obj.BeginDate = DateTemp;
                obj.EndDate = datestr(today, 'yyyymmdd');
                
                obj.StockDataDouble = GetStockTSDay_Web(StockCodeInput,obj.BeginDate,obj.EndDate);
                if isempty(obj.StockDataDouble)
                    obj.str = [ obj.StockCode,'-', ' 数据获取失败，请检查！' ];
                    disp(obj.str);
                    notify(obj,'MessageUpdate')
                    
                    continue;
                end
                notify(obj,'FetchState')
                
            end
            if obj.Filing==1
                notify(obj,'FilingState')
            end
        end
    end
    methods (Access = private) %% for EVENTS % MOST IMPORTANT
        function obj=MUpdate(obj,varargin)
            obj.MessageHistory{obj.MessageID,1}=datestr(now);
            obj.MessageHistory{obj.MessageID,2}=obj.str;
            obj.MessageID=obj.MessageID+1;
            
        end
        function obj=QUANTMail(obj)
            aaaa=1;
            QuantboxSendMail('yutiansut@qq.com',num2str(aaaa))
            aaaa=aaaa+1;
        end
        function obj = DFetch(obj,varargin)
            obj.str='Data Fetch Success';
            disp(obj.str)
            notify(obj,'MessageUpdate')
            switch obj.StatusCode
                case 510
                    disp('Tick data fetched successfully')
                    notify(obj,'MessageUpdate')
                case 520
                    disp('Tsday data fetched successfully')
                    notify(obj,'MessageUpdate')
            end
            obj.StockCodeOut{1,1}='StockID';
            obj.StockCodeOut{1,2}='StockTSData';
            obj.StockCodeOut{1,3}='Mean TS';
            obj.StockCodeOut{1,4}='Volum';
            obj.StockCodeOut{1,5}='StockTick';
            obj.StockCodeOut{obj.StockID,1}=obj.StockCode;
            obj.StockCodeOut{obj.StockID,2}=obj.StockDataDouble;
            temp=obj.StockDataDouble(:,2:5);
            obj.StockCodeOut{obj.StockID,3}=mean(temp,2);
            obj.StockCodeOut{obj.StockID,4}=obj.StockDataDouble(:,6);
            obj.SYS_TS=obj.StockCodeOut;
            if size(temp,1)>obj.tmun
                
               
                obj.StockID=obj.StockID+1;
                 disp(num2str(obj.StockID))
            end
            obj.str='Mail to Server';
            disp(obj.str)
            notify(obj,'MessageUpdate')
        end
        
        function obj = DFiling(obj,varargin)
            
            obj.str='Start DataFiling';
            disp(obj.str)
            notify(obj,'MessageUpdate')
            %%进行数据清洗
            %%Step1 日期规整 所有交易日统一
            obj.datatempid=size(obj.StockCodeOut,1);
            x=zeros(obj.datatempid-1,obj.tmun);
            for j=2:obj.datatempid
                atemp=obj.StockCodeOut{j,3};
                atemp=atemp(1:obj.tmun,1);
                x(j-1,:)=atemp';
            end
            obj.Result=x';
            
            if obj.Analysis==1
                notify(obj,'AnalysisState')
            end
        end
        function obj = DAnalysis(obj,varargin)
            
            obj.str='Start DataAnalysis';
            disp(obj.str)
            notify(obj,'MessageUpdate')
            d=501;              % Starting Date
            window=500;         % Size of moving window for defining pairs
            t=1.5;              % Threshold value for defining abnormal behavior
            ut=5;               % Peridiocity of pairs updates
            C=30;               % Trading cost per trade (in units of price (e.g. dollars))
            maxPeriod=5;        % maximum periods to hold the positions
            Capital=10000;
            [obj.profitOut,obj.portValue,obj.myTrades]=pairstrading(obj.Result,Capital,d,window,t,ut,C,maxPeriod);
        end
        function obj=DStrategyA(obj,varargin)
            load('obj.mat')
            obj.CEEMDAN_ID=3;
            obj.SVRt=120;
            %               for jj=6:10
            jj=6;
            testx=obj.Result(:,jj);
            hurst_origin=EstimateHurst(testx');
            [modes,obj.ITS]=ceemdan(testx',0.2,500,5000);
            totallvar=zeros(12,1);
            totalstd=zeros(12,1);
            BESTYFITX=zeros(length(testx)-obj.SVRt,12);
            obj.HURST=zeros(12,1);
            %% depth1
            for i=1:12
                obj.HURST(i,1)=EstimateHurst(modes(i,:));
                if obj.HURST(i,1)<0.5
                    obj.besthursti=i;
                end
                [lvar,leastvar,lstd,leaststd,BESTYFIT,OrgY,id]=findleastvarl(modes(i,:)',obj.SVRt);
                BESTYFITX(:,i)=BESTYFIT;
                obj.ORGY(:,i)=OrgY;
                
            end
            obj.MODES{jj,1}=modes;
            obj.BESTYFITANDY{1,1}='BESTYFITX';
            obj.BESTYFITANDY{1,2}='ORGY';
            obj.BESTYFITANDY{1,3}='HURST';
            obj.BESTYFITANDY{1,4}='besthursti';
            obj.BESTYFITANDY{1,5}='MODES';
            obj.BESTYFITANDY{1,6}='totallvar';
            obj.BESTYFITANDY{1,7}='lvar';
            obj.BESTYFITANDY{1,8}='totalstd';
            obj.BESTYFITANDY{1,9}='lstd';
            obj.BESTYFITANDY{1,10}='HUSRT Under 0.5';
            obj.BESTYFITANDY{1,11}='HUSRT Above 0.5';
            obj.BESTYFITANDY{1,12}='Original Under 0.5';
            obj.BESTYFITANDY{1,13}='Original Above 0.5';
            obj.BESTYFITANDY{jj+1,1}=BESTYFITX;
            obj.BESTYFITANDY{jj+1,2}=obj.ORGY;
            obj.BESTYFITANDY{jj+1,3}=obj.HURST;
            obj.BESTYFITANDY{jj+1,4}=obj.besthursti;
            obj.BESTYFITANDY{jj+1,5}=modes;
            obj.BESTYFITANDY{jj+1,6}=totallvar;
            obj.BESTYFITANDY{jj+1,7}=lvar;
            obj.BESTYFITANDY{jj+1,8}=totalstd;
            obj.BESTYFITANDY{jj+1,9}=lstd;
            l1=sum(BESTYFITX(:,1:obj.besthursti),2);
            l2=sum(BESTYFITX(:,obj.besthursti+1:12),2);
            obj.BESTYFITANDY{jj+1,10}=l1;
            obj.BESTYFITANDY{jj+1,11}=l2;
            l1x=sum(modes(1:obj.besthursti,:),1)';
            l2x=sum(modes(obj.besthursti+1:12,:),1)';
            l1x=l1x(obj.SVRt+1:end,:);
            l2x=l2x(obj.SVRt+1:end,:);
            obj.BESTYFITANDY{jj+1,12}=l1x;
            obj.BESTYFITANDY{jj+1,13}=l2x;
            obj.StockID=obj.StockCodeOut(jj+1,1);
            figure  %画图
            subplot(2,1,1);
            plot(l1x)
            hold on
            plot(l1)
            legend('Original Data','Process with SVR')
            titletext=[char(obj.StockID),'--Hurst< 0.5'];
            title(titletext)
            subplot(2,1,2);
            plot(l2x)
            hold on
            plot(l2)
            titletext=[char(obj.StockID),'--Hurst> 0.5'];
            title(titletext)
            
            title('Hurst> 0.5')
            %     %% depth2
            %     Depth2L=sum(modes(1:obj.besthursti,:),1)';
            %     hurst_origin_depth2=EstimateHurst(Depth2L');
            %     [modes_depth2,obj.ITS_depth2]=ceemdan(Depth2L',0.2,500,5000);
            %     figure
            %     plot(modes_depth2')
            %     title('Depth 2 CEEMDAN')
            %     CEEMDAN_Depth2_ID=size(modes_depth2,1);
            %     totallvar_depth2=zeros(CEEMDAN_Depth2_ID,1);
            %     totalstd_depth2=zeros(CEEMDAN_Depth2_ID,1);
            %     BESTYFITX_depth2=zeros(length(testx)-obj.SVRt,CEEMDAN_Depth2_ID);
            %     obj.HURST_depth2=zeros(CEEMDAN_Depth2_ID,1);
            %     for i=1:CEEMDAN_Depth2_ID
            %         obj.HURST_depth2(i,1)=EstimateHurst(modes_depth2(i,:));
            %         if obj.HURST_depth2(i,1)<0.5
            %             obj.besthursti_depth2=i;
            %         end
            %         [lvar_depth2,leastvar_depth2,lstd_depth2,leaststd_depth2,BESTYFIT_depth2,OrgY_depth2,id_depth2]=findleastvarl(modes(i,:)',obj.SVRt);
            %         BESTYFITX_depth2(:,i)=BESTYFIT_depth2;
            %         obj.ORGY_depth2(:,i)=OrgY_depth2;
            %
            %     end
            %     obj.MODES_depth2{jj,1}=modes_depth2;
            %     obj.BESTYFITANDY_depth2{1,1}='BESTYFITX_depth2';
            %     obj.BESTYFITANDY_depth2{1,2}='ORGY_depth2';
            %     obj.BESTYFITANDY_depth2{1,3}='HURST_depth2';
            %     obj.BESTYFITANDY_depth2{1,4}='besthursti_depth2';
            %     obj.BESTYFITANDY_depth2{1,5}='MODES_depth2';
            %     obj.BESTYFITANDY_depth2{1,6}='totallvar_depth2';
            %     obj.BESTYFITANDY_depth2{1,7}='lvar_depth2';
            %     obj.BESTYFITANDY_depth2{1,8}='totalstd_depth2';
            %     obj.BESTYFITANDY_depth2{1,9}='lstd_depth2';
            %     obj.BESTYFITANDY_depth2{1,10}='HUSRT Under 0.5_depth2';
            %     obj.BESTYFITANDY_depth2{1,11}='HUSRT Above 0.5_depth2';
            %     obj.BESTYFITANDY_depth2{1,12}='Original Under 0.5_depth2';
            %     obj.BESTYFITANDY_depth2{1,13}='Original Under 0.5_depth2';
            %     obj.BESTYFITANDY_depth2{jj+1,1}=BESTYFITX_depth2;
            %     obj.BESTYFITANDY_depth2{jj+1,2}=obj.ORGY_depth2;
            %     obj.BESTYFITANDY_depth2{jj+1,3}=obj.HURST_depth2;
            %     obj.BESTYFITANDY_depth2{jj+1,4}=obj.besthursti_depth2;
            %     obj.BESTYFITANDY_depth2{jj+1,5}=modes_depth2;
            %     obj.BESTYFITANDY_depth2{jj+1,6}=totallvar_depth2;
            %     obj.BESTYFITANDY_depth2{jj+1,7}=lvar_depth2;
            %     obj.BESTYFITANDY_depth2{jj+1,8}=totalstd_depth2;
            %     obj.BESTYFITANDY_depth2{jj+1,9}=lstd_depth2;
            %     l1_depth2=sum(BESTYFITX_depth2(:,1:obj.besthursti_depth2),2);
            %     l2_depth2=sum(BESTYFITX_depth2(:,obj.besthursti_depth2+1:12),2);
            %     obj.BESTYFITANDY_depth2{jj+1,10}=l1_depth2;
            %     obj.BESTYFITANDY_depth2{jj+1,11}=l2_depth2;
            %     l1x_depth2=sum(modes_depth2(1:obj.besthursti_depth2,:),1)';
            %     l2x_depth2=sum(modes_depth2(obj.besthursti_depth2+1:12,:),1)';
            %     l1x_depth2=l1x_depth2(obj.SVRt+1:end,:);
            %     l2x_depth2=l2x_depth2(obj.SVRt+1:end,:);
            %     obj.BESTYFITANDY_depth2{jj+1,12}=l1x_depth2;
            %     obj.BESTYFITANDY_depth2{jj+1,13}=l2x_depth2;
            %     obj.StockID=obj.StockCodeOut(jj+1,1);
            %     figure  %画图
            %     subplot(2,1,1);
            %     plot(l1x_depth2)
            %     hold on
            %     plot(l1_depth2)
            %     legend('Original Data','Process with SVR')
            %     titletext=[char(obj.StockID),'--Hurst< 0.5-depth2'];
            %     title(titletext)
            %     subplot(2,1,2);
            %     plot(l2x_depth2)
            %     hold on
            %     plot(l2_depth2)
            %     titletext=[char(obj.StockID),'--Hurst> 0.5-depth2'];
            %     title(titletext)
            %     %%
            %
            %     figure  %画图
            %     subplot(3,2,1);
            %     plot(modes')
            %     title('CEEMDAN-Depth=1')
            %     subplot(3,2,2);
            %     plot(modes_depth2')
            %     title('CEEMDAN-Depth=2')
            %     subplot(3,2,3);
            %     plot(l1x)
            %     hold on
            %     plot(l1)
            %     legend('Original Data','Process with SVR')
            %     titletext=[char(obj.StockID),'--Hurst< 0.5'];
            %     title(titletext)
            %     subplot(3,2,5);
            %     plot(l2x)
            %     hold on
            %     plot(l2)
            %     legend('Original Data','Process with SVR')
            %     titletext=[char(obj.StockID),'--Hurst> 0.5'];
            %     title(titletext)
            %
            %     title('Hurst> 0.5')
            %     subplot(3,2,4);
            %     plot(l1x_depth2)
            %     hold on
            %     plot(l1_depth2)
            %     legend('Original Data','Process with SVR')
            %     titletext=[char(obj.StockID),'--Hurst< 0.5-depth2'];
            %     title(titletext)
            %     subplot(3,2,6);
            %     plot(l2x_depth2)
            %     hold on
            %     plot(l2_depth2)portvrisk
            %     legend('Original Data','Process with SVR')
            %     titletext=[char(obj.StockID),'--Hurst> 0.5-depth2'];
            %     title(titletext)
            %
            
            
            %               end
        end
        function obj=ACCOUNT(obj,varargin)
            obj.ACC_Cash=obj.ACC_Cash+obj.TRA.status*obj.TRA.Bid*obj.TRA.Amount;
           
            obj.ACC_Trade{1,1}='交易品种代码';
            obj.ACC_Trade{1,2}='交易日期';
            obj.ACC_Trade{1,3}='成交价格';
            obj.ACC_Trade{1,4}='交易数量';
            obj.ACC_Trade{1,5}='方向';
            obj.ACC_Trade{obj.ACC_Trade_id,1}=obj.TRA.id;
            obj.ACC_Trade{obj.ACC_Trade_id,2}=obj.TRA.Date;
            obj.ACC_Trade{obj.ACC_Trade_id,3}=obj.TRA.Bid;
            obj.ACC_Trade{obj.ACC_Trade_id,4}=obj.TRA.Amount;
            obj.ACC_Trade{obj.ACC_Trade_id,5}=obj.TRA.Status;
            
            index_id=find(strcmpi(obj.SYS_TS(:,1),obj.ACC.id));
            obj.ACC_Price_Total=obj.SYS_TS{index_id,2};  %
            index_date=find(obj.TRA_Price_Total(:,1)==obj.ACC.Date);
            obj.ACC_Price=obj.TRA_Price_Total(index_date,5);
            obj.ACC_Amount=obj.ACC_Amount-obj.TRA.status*obj.ACC.Amount;
            obj.ACC_Account{1,1}='TRA.id';
            obj.ACC_Account{1,2}='ACC_Amount';
            obj.ACC_Account{1,3}='ACC_Price';
            obj.ACC_Account{1,4}='ACC_Amount*ACC_Price';
            if strcmpi(obj.ACC_Account(:,1),obj.TRA.id)==0
                obj.ACC_Account_id=obj.ACC_Account_id+1;
            end
            obj.ACC_Account{obj.ACC_Account_id,1}=obj.TRA.id;
            obj.ACC_Account{obj.ACC_Account_id,2}=obj.ACC_Amount;
            obj.ACC_Account{obj.ACC_Account_id,3}=obj.ACC_Price;
            obj.ACC_Account{obj.ACC_Account_id,4}=obj.ACC_Amount*obj.ACC_Price;
%             obj.ACC_Portfolio=obj.ACC_Account(2:end,4);
            obj.ACC_Portfolio=sum(cell2mat(obj.ACC_Account(2:end,4)));
            obj.ACC_TotalAssest(obj.ACC_Trade_id,1)=abs(obj.ACC_Portfolio)+obj.ACC_Cash;
            
            obj.ACC_Trade_id=obj.ACC_Trade_id+1;
            
        end
        function obj=TRADE(obj,varargin)
            obj.TRA=obj.ACC;
            index_id=find(strcmpi(obj.SYS_TS(:,1),obj.ACC.id));
            obj.TRA_Price_Total=obj.SYS_TS{index_id,2};  %
            index_date=find(obj.TRA_Price_Total(:,1)==obj.ACC.Date);
            obj.TRA_Price=obj.TRA_Price_Total(index_date,2:5);
            obj.TRA_Bid=obj.ACC.Bid;
            if obj.TRA_Bid<=obj.TRA_Price(1,2) &&obj.TRA_Bid>=obj.TRA_Price(1,3)
                disp('成交')
                obj.TRA.status=obj.ACC_Position;  %-1buy 1sell
                if obj.TRA.status==-1
                    obj.TRA.Status='买入';
                end
                if obj.TRA.status==1
                    obj.TRA.Status='卖出';
                end
                obj.str=['交易品种代码:',obj.TRA.id,',交易日期是:',num2str(obj.TRA.Date),',交易价格:',num2str(obj.TRA.Bid),',交易量:',num2str(obj.TRA.Amount),',交易方向：',obj.TRA.Status];
            end
            notify(obj,'Account');
            notify(obj,'MessageUpdate');
        end
        function obj=VALUE(obj,varargin)
        end
    end
    
end
%% 辅助函数
function [TableTotalNum,TableCell] = GetTableFromWeb(URL,CharsetString)

%
% History:
% Function GetTableFromWeb is based on the very very good "pick of the week" from August 20th, 2010
% (http://www.mathworks.com/matlabcentral/fileexchange/22465-get-html-table-data-into-matlab) by Jeremy Barry.
% It is inspired by the restrictions of the original function and should users help, who had problems with the
% loading time of the requested webpage. So the workaround doesn't use the internal webbrowser by Matlab but
% takes the urlread function to import and analyze the table-webdata.
%
% To get table data, it is necessary to know from which url you want to read in the data and from which
% table. If you have an url but no idea which table with the specified tablenummer has the data use the
% originalfuntion getTableFromWeb
% (http://www.mathworks.com/matlabcentral/fileexchange/22465-get-html-table-data-into-matlab) to check which
% tablenumber with content you are interestred in.
%
% The first example(at the end of description) gets actual departure information by german railways for the
% railwaystation Frankfurt Hbf (coded by ibnr, international railway station number).
% The second example belongs to the orinigal example by Jeremy Barry and gets financial information.
%
% There are two input arguments:
% URL  -- is the string of the requested webpage
% nr_table    -- number of table to get and to put in out_table
%
% Ouput argument:
% out_table  -- is a cell array of requested data
%
% Example:
%
% % German Railways-travelling information example
%  ibnr       = 8098105;   % IBNR  railway station: Frankfurt-Hbf   (for more ibnr see: http://www.ibnr.de.vu/)
%  URL = [ 'http://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?rt=1&ld=10000&evaId=', num2str(ibnr) ,'&boardType=dep&time=actual&productsDefault=1111000000&start=yes'];      % question string fo calling actual departure information for Frankfurt HBF
%  nr_table   = 2;  % Table with the travelinformation data
%  out_table  = GetTableFromWeb(URL, nr_table)
%
% % Finance example
% % run getTableDataScript to see, which table is number 7 (Valuation Measures)
% URL = ('http://finance.yahoo.com/q/ks?s=GOOG');
% nr_table   = 7;
% out_table  = GetTableFromWeb(URL, nr_table)
%
%
% Bugs and suggestions:
%    Please send to Sven Koerner: koerner(underline)sven(add)gmx.de
%
% Modified by Sven Koerner: koerner(underline)sven(add)gmx.de
% Date: 2010/12/06
%
% License additional conditions:
%
% Because of Redistribution and binary modification see the following original license:
%
% Copyright (c) 2010, The MathWorks, Inc.
% All rights reserved.
%
% Redistribution and use in source and binary forms, with or without
% modification, are permitted provided that the following conditions are
% met:
%
%     * Redistributions of source code must retain the above copyright
%       notice, this list of conditions and the following disclaimer.
%     * Redistributions in binary form must reproduce the above copyright
%       notice, this list of conditions and the following disclaimer in
%       the documentation and/or other materials provided with the distribution
%     * Neither the name of the The MathWorks, Inc. nor the names
%       of its contributors may be used to endorse or promote products derived
%       from this software without specific prior written permission.
%
% THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
% AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
% IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
% ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
% LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
% CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
% SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
% INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
% CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
% ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
% POSSIBILITY OF SUCH DAMAGE.
%
%
%  Additional Data:
%%% The original function is getTableFromWeb
% Inputs - none
% Outputs - data from selected table
%
% Usage:
% * Navigate to a webpage using the MATLAB web browser (note: this will NOT
% work with any other browser)
% * Once at the location of the table you want, execute this function
% (getTableFromWeb)
% * Click on the MATLAB logo next to the table you want to import
%
% This function takes no input arguments.  The varargin is so that when
% getting the data from a table it can identify which table you have
% chosen.
% Copyright 2008 - 2010 The MathWorks, Inc.
%% 输入输出预处理
if nargin<2 || isempty( CharsetString )
    CharsetString = 'gb2312';
end
TableTotalNum = 0;
TableCell = [];

% Modification: do not open the Matlab-Browser
% % % newBrowser = 0;
% % % activeBrowser = [];
% % % if ~newBrowser
% % %     % User doesn't want a new browser, so find the active browser.
% % %     activeBrowser = com.mathworks.mde.webbrowser.WebBrowser.getActiveBrowser;
% % % end
% % % if isempty(activeBrowser)
% % %     % If there is no active browser, create a new one.
% % %     activeBrowser = com.mathworks.mde.webbrowser.WebBrowser.createBrowser(showToolbar, showAddressBox);
% % % end


%% Modification: read the html content via urlread and not via active browser
%%% Call functionality to update the HTML with MATLAB hooks to grab data
%%% urlText    = activeBrowser.getHtmlText;
%%% newUrlText = updateHTML(urlText);
%%% activeBrowser.setHtmlText(newUrlText);


%% Uncomment to see the requested html-document
% web (URL);

%%  begin modified code
if verLessThan('matlab', '8.3')
    [URLchar, status] = urlread_General(URL, 'Charset', CharsetString, 'TimeOut', 60);
else
    [URLchar, status] = urlread(URL, 'Charset', CharsetString, 'TimeOut', 60);
end
if status == 0
    str = 'urlread error:网页读取失败！请检查输入的网址或网络连接情况！';
    disp(str);
    
    return;
end

urlText = java.lang.String( URLchar );         % get the urlcontent

[i, newUrlText] = updateHTML(urlText);                           % in i is the number of tables
TableTotalNum = i;

if TableTotalNum>1
    TableCell = cell(TableTotalNum,1);
    for run = 1:TableTotalNum
        TableCell{run} = getHTMLTable(run, newUrlText);
    end
end

end
% Modification: get the number of all tables and the modified urltext
function [i, newUrlText] = updateHTML(url)
% Output:   i               --> number of tables in url
%           newUrlText      --> modified output text

%% Setup
%% Modification
% Set the location to the icon
% iconLocation = which('matlab.ico');
% iconLocation = ['file://' regexptranslate('escape', iconLocation)];
%%
% Convert the Java string to a character array for MATLAB
pageString = reshape(url.toCharArray, 1, []);
%% Regular expressions used in replacements
noDataTable = 'replaceMeFirst'; %used for tables with no visible data
%dataTable = ['<a href="matlab:getTableFromWeb(replaceMe)"><img src="' iconLocation '" align="left" name="MLIcon"/></a>'];
% Modification
dataTable = '<a href="matlab:GetTableFromWeb(replaceMe)"></a>';

%% Find all tables
tables = regexprep(pageString, '(<table[^>]*>(?:(?>[^<]+)|<(?!table[^>]*>))*?</table)', [noDataTable '$1']);

%%
% Remove the text in front of tables with no data
tables = regexprep(tables, [noDataTable '(<table[^>]*>(?:<[^>]*>\s*)+?)</table[^>]*>'], '$1');

% Add the string for accessing MATLAB in front of tables with data
tables = regexprep(tables, noDataTable, dataTable);

% Find all of the table with data tags and provide them with a unique
% identifier for grabbing the data
dataTableID = regexp(tables, 'replaceMe', 'tokens');
for i = 1:length(dataTableID)
    tables = regexprep(tables, 'replaceMe', num2str(i), 'once');
end
%% output
% Output the new HTML
newUrlText = tables;
end
% SUBFunction
function out = getHTMLTable(tableID, pageString)

% Get the HTML text from the browser window and conver to MATLAB character
% array
% Modifaction: get the content without Matlab webbrowser
% % % activeBrowser = com.mathworks.mde.webbrowser.WebBrowser.getActiveBrowser;
% % % pageString = reshape(activeBrowser.getHtmlText.toCharArray, 1, []);

% Pattern for finding MATLAB hooks
%pattern = ['<a href="matlab:getTableFromWeb\(' num2str(tableID) '\)'];
%% 初始化
out = [];
%% Modifction
pattern = ['<a href="matlab:GetTableFromWeb\(' num2str(tableID) '\)'];

% Find data from the table
[~,~,~,match] = regexp(pageString, [pattern '.*?<table[^>]*>.*?(<tr.*?>).*?</table[^>]*>' ], 'once');
anyData = strtrim(regexprep(match, '<.*?>', ''));

if(isempty(anyData))
    r = regexp(pageString, [pattern '.*?</table><table[^>]*>(.*?)</table'], 'tokens', 'once');
else
    r = regexp(pageString, [pattern '(.*?)</table'], 'tokens');
end

% Convert any data in cell arrays to characters
if ~isempty(r)
    while(iscell(r))
        r = r{1};
    end
else
    return;
end

%Establish a row index
rowind = 0;

% Build cell aray of table data
try
    rows = regexpi(r, '<tr.*?>(.*?)</tr>', 'tokens');
    
    % LY_faruto add code 2014.12.04
    if isempty(rows)
        rows = regexpi(r, '(.*?)</tr>', 'tokens');
    end
    
    for i = 1:numel(rows)
        colind = 0;
        if (isempty(regexprep(rows{i}{1}, '<.*?>', '')))
            continue
        else
            rowind = rowind + 1;
        end
        
        headers = regexpi(rows{i}{1}, '<th.*?>(.*?)</th>', 'tokens');
        if ~isempty(headers)
            for j = 1:numel(headers)
                colind = colind + 1;
                data = regexprep(headers{j}{1}, '<.*?>', '');
                if (~strcmpi(data,'&nbsp;'))
                    out{rowind,colind} = strtrim(data);
                end
            end
            continue
        end
        cols = regexpi(rows{i}{1}, '<td.*?>(.*?)</td>', 'tokens');
        for j = 1:numel(cols)
            if(rowind==1)
                if(isempty(cols{j}{1}))
                    continue
                else
                    colind = colind + 1;
                end
            else
                colind = j;
            end
            data = regexprep(cols{j}{1}, '&nbsp;', ' ');
            data = regexprep(data, '<.*?>', '');
            
            if (~isempty(data))
                out{rowind,colind} = strtrim(data) ;
            end
        end
    end
    
catch err
    rethrow(err);
end
end
function [Chinese] = isChinese(ch)
% 对于GB2312的字符（就是我们平时所说的区位），一个汉字对应于两个字节。 每个字节都是大于A0（十六进制,即160），
% 倘若，第一个字节大于A0，而第二个字节小于A0，那么它应当不是汉字（仅仅对于GB2312)
info = unicode2native(ch,'GB2312');
bytes = size(info,2);
Chinese = 0;
if (bytes == 2)
    if(info(1)>160 & info(2)>160)
        Chinese = 1;
    end
end
end
function header = http_createHeader(name,value)
%http_createHeader Simple function for creating input header to urlread2
%
%   header = http_createHeader(name,value)
%
%   CODE: header = struct('name',name,'value',value);
%
%   See Also:
%       urlread2

header = struct('name',name,'value',value);
end
function [str,header] = http_paramsToString(params,encodeOption)
%http_paramsToString Creates string for a POST or GET requests
%
%   [queryString,header] = http_paramsToString(params, *encodeOption)
%
%   INPUTS
%   =======================================================================
%   params: cell array of property/value pairs
%           NOTE: If the input is in a 2 column matrix, then first column
%           entries are properties and the second column entries are
%           values, however this is NOT necessary (generally linear)
%   encodeOption: (default 1)
%           1 - the typical URL encoding scheme (Java call)
%
%   OUTPUTS
%   =======================================================================
%   queryString: querystring to add onto URL (LACKS "?", see example)
%   header     : the header that should be attached for post requests when
%                using urlread2
%
%   EXAMPLE:
%   ==============================================================
%   params = {'cmd' 'search' 'db' 'pubmed' 'term' 'wtf batman'};
%   queryString = http_paramsToString(params);
%   queryString => cmd=search&db=pubmed&term=wtf+batman
%
%   IMPORTANT: This function does not filter parameters, sort them,
%   or remove empty inputs (if necessary), this must be done before hand

if ~exist('encodeOption','var')
    encodeOption = 1;
end

if size(params,2) == 2 && size(params,1) > 1
    params = params';
    params = params(:);
end

str = '';
for i=1:2:length(params)
    if (i == 1), separator = ''; else separator = '&'; end
    switch encodeOption
        case 1
            param  = urlencode(params{i});
            value  = urlencode(params{i+1});
            %         case 2
            %             param    = oauth.percentEncodeString(params{i});
            %             value    = oauth.percentEncodeString(params{i+1});
            %               header = http_getContentTypeHeader(1);
        otherwise
            error('Case not used')
    end
    str = [str separator param '=' value]; %#ok<AGROW>
end

switch encodeOption
    case 1
        header = http_createHeader('Content-Type','application/x-www-form-urlencoded');
end


end
function URLHexCode = Unicode2URLHexCode(unicodestr,encoding)
% by LiYang_faruto
% Email:farutoliyang@foxmail.com
% 2014/01/01
%% 输入输出预处理
if nargin < 2
    encoding = 'GB2312';
end
if nargin < 1
    unicodestr = '百度一下';
end

URLHexCode = [];
%% 转换

temp = unicode2native(unicodestr,encoding);

HexTemp = dec2hex(temp);

StrTemp =[];
for i = 1:size(HexTemp,1)
    
    StrTemp = [StrTemp,'%',HexTemp(i,:)];
end

URLHexCode = StrTemp;
end
function URLHexCode = Unicode2URLHexCode_Ch(InputString,encoding)
% 仅将输入的字符串中的中文字符转换成GB2312编码
% by LiYang_faruto
% Email:farutoliyang@foxmail.com
% 2014/12/12
%% 输入输出预处理
if nargin < 2
    encoding = 'GB2312';
end
if nargin < 1
    InputString = 'BD百度Tt一下SS';
end
if isempty(InputString)
    URLHexCode = [];
    return;
end

URLHexCode = [];
%% 转换
Len = length(InputString);
isFlag = isChineseChar(InputString,encoding);
for i = 1:Len
    if isFlag(i) == 1
        
        temp = unicode2native(InputString(i),encoding);
        
        HexTemp = dec2hex(temp);
        
        StrTemp =[];
        for i = 1:size(HexTemp,1)
            
            StrTemp = [StrTemp,'%',HexTemp(i,:)];
        end
        
        URLHexCode = [URLHexCode,StrTemp];
        
    else
        URLHexCode = [URLHexCode,InputString(i)];
    end
end
end
function DataCell = URLcharParse(URLchar)
% by LiYang_faruto
% Email:farutoliyang@foxmail.com
% 2015/01/01
%% 输入输出预处理
if isempty( URLchar )
    DataCell = [];
    return;
end
DataCell = [];
%%

% &rsv_page=2
expr = ['<div class="result" id=.*?>','.*?',...
    '</div>'];
[matchstart,matchend,tokenindices,matchstring,tokenstring,tokenname,splitstring] =regexpi(URLchar, expr);
Len = numel(matchstring);
if Len>=1
    ColNum = 4;
    DataCell = cell(Len, ColNum);
    for i = 1:Len
        StringTemp = matchstring{i};
        
        expr = ['<a href=','.*?','</a>'];
        TitleURL = regexpi(StringTemp, expr,'match');
        TitleURL = TitleURL{1};
        
        expr = ['>','.*?',...
            '</a>'];
        out = regexpi(TitleURL, expr,'match');
        out = out{1};
        temp = out(2:end-4);
        % % % 简易预处理清洗，剔除<em> </em>
        expr = ['<.*?em>'];
        replace = '';
        temp = regexprep(temp,expr,replace);
        % Title
        DataCell{i,2} = temp;
        
        expr = ['"'];
        out = regexpi(TitleURL, expr,'split');
        out = out{2};
        temp = out;
        % URL
        DataCell{i,4} = temp;
        
        
        expr = ['<p class="c-author">','.*?',...
            '</p>'];
        AuthorDate = regexpi(StringTemp, expr,'match');
        AuthorDate = AuthorDate{1};
        expr = ['>','.*?',...
            '</p>'];
        out = regexpi(AuthorDate, expr,'match');
        out = out{1};
        temp = out(2:end-4);
        
        expr = ['&nbsp;&nbsp;'];
        out = regexpi(temp, expr,'split');
        if numel(out) == 2
            %　Author Source
            DataCell{i,3} = out{1};
            % DateTime
            DataCell{i,1} = out{2};
        else
            % 有的可能没有Author i.e. 网站名称（作者名称）没有
            %　Author Source
            DataCell{i,3} = [];
            % DateTime
            DataCell{i,1} = out{1};
        end
    end
    Head = {'DateTime','Title','Source','URL'};
    DataCell = [Head;DataCell];
    
    
end
end
function [ Web_XRD_Data , Web_XRD_Cell_1 , Web_XRD_Cell_2 ] = GetStockXRD_Web(StockCode)
% Modified by LiYang_faruto
% based on Chandeman
%% 调用格式：
%       [ Web_XRD_Data , Web_XRD_Cell_1 , Web_XRD_Cell_2 ] = F_Stock_XRD_DataImport(StockCode,Stock_Name)
% 输入： StockCode → 股票代码 StockCode = '600001';
%        Stock_Name → 股票名称
% 输出:  Web_XRD_Data → 除权除夕数值型数据
%        Web_XRD_Cell_1 → 分红送股文本型数据
%        Web_XRD_Cell_2 → 配股文本型数据
% http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/600083.phtml
% http://stockdata.stock.hexun.com/2009_fhzzgb_600588.shtml
%
%% 输入输出预处理
if nargin < 1 || isempty(StockCode)
    StockCode = '600588';
end

% 股票代码预处理，目标代码demo '600588'
if strcmpi(StockCode(1),'s')
    StockCode = StockCode(3:end);
end
if strcmpi(StockCode(end),'h') ||  strcmpi(StockCode(end),'z')
    StockCode = StockCode(1:end-2);
end

Web_XRD_Data = [];
Web_XRD_Cell_1 = [];
Web_XRD_Cell_2 = [];
%% 网页读取
URL = ['http://vip.stock.finance.sina.com.cn/corp/'...
    'go.php/vISSUE_ShareBonus/stockid/'...
    StockCode ,'.phtml'];
if verLessThan('matlab', '8.3')
    [Web_Url_Countent, status] = urlread_General(URL, 'TimeOut', 60,'Charset', 'gb2312');
else
    [Web_Url_Countent, status] = urlread(URL, 'TimeOut', 60,'Charset', 'gb2312');
end
if status == 0
    str = ['urlread error:网页读取失败！请检查输入的网址或网络连接情况！'];
    disp(str);
    return;
end

Web_Url_Expression = '<tbody>.*</a></td>';
[~,Web_Url_Matches] = ...
    regexp(Web_Url_Countent,Web_Url_Expression,'tokens','match');

%% 数据提取

Web_Ori_Countent = char(Web_Url_Matches);
Web_Ori_Expression = '>';
[~,Web_Ori_Matches] = regexp(Web_Ori_Countent,Web_Ori_Expression,'match','split');

%% 数据整理

Web_Ori_Matches_length = length(Web_Ori_Matches);
Intermediate_variable_k = Web_Ori_Matches_length;
Intermediate_variable_Matches = char(Web_Ori_Matches);
if isempty(Intermediate_variable_Matches)
    fprintf([StockCode,'→暂无除权除息数据\n'])
    Web_XRD_Data = [];
    Web_XRD_Cell_1 = [];
    Web_XRD_Cell_2 = [];
    return;
end

% 找出分红增股&配股临界位置

for Intermediate_variable_i = 1 : length(Intermediate_variable_Matches(:,1))
    if strcmp(Intermediate_variable_Matches(Web_Ori_Matches_length + 1 - Intermediate_variable_i,1:7) , '<strong')
        Intermediate_variable_k = Web_Ori_Matches_length + 1 - Intermediate_variable_i;
        break
    end
end

% 分红

Intermediate_variable_j = 1;
Intermediate_variable_q1 = repmat(1:7,1,ceil(Web_Ori_Matches_length/7))';
for Intermediate_variable_i = 1 : Intermediate_variable_k
    if ~isempty(str2num(Intermediate_variable_Matches(Intermediate_variable_i,1))) || Intermediate_variable_Matches(Intermediate_variable_i,1) == '-'
        Web_XRD_Cell_1{ceil(Intermediate_variable_j/7),Intermediate_variable_q1(Intermediate_variable_j)} =  ...
            Intermediate_variable_Matches(Intermediate_variable_i,1:find(Intermediate_variable_Matches(Intermediate_variable_i,:)=='<')-1);
        Intermediate_variable_j = Intermediate_variable_j + 1;
    end
end

Web_XRD_Cell_1 = [{'公告日期','送股（股）','转增（股）','派息（税前）（元）',...
    '除权除息日', '股权登记日','红股上市日'};Web_XRD_Cell_1];

% 找出无效数据

[Web_XRD_Cell_1_Row_1,Web_XRD_Cell_1_Column_1] = size(Web_XRD_Cell_1);
Intermediate_variable_j = 0;
Intermediate_variable_l = ones(Web_XRD_Cell_1_Row_1,1);
for Intermediate_variable_i = 1 : Web_XRD_Cell_1_Row_1
    if strcmp(Web_XRD_Cell_1(Intermediate_variable_i,5),'--') || ...
            strcmp(Web_XRD_Cell_1(Intermediate_variable_i,5),'除权除息日')
        Intermediate_variable_l(Intermediate_variable_i,1) = 0;
        Intermediate_variable_j = Intermediate_variable_j + 1;
    end
end

% 将分红增股文本数据转成数值型数据

temp = Web_XRD_Cell_1(Intermediate_variable_l==1,5);
if isempty( temp )
    fprintf([StockCode,'→暂无除权除息数据\n'])
    Web_XRD_Data = [];
    Web_XRD_Cell_1 = [];
    Web_XRD_Cell_2 = [];
    return;
end

Web_XRD_Data = zeros(Web_XRD_Cell_1_Row_1 - Intermediate_variable_j ,6);
Web_XRD_Data(:,1)  = datenum(Web_XRD_Cell_1(Intermediate_variable_l==1,5));          % 除权除息日

Web_XRD_Data(:,2)  = cellfun(@str2num,Web_XRD_Cell_1(Intermediate_variable_l==1,2)); % 送股
Web_XRD_Data(:,3)  = cellfun(@str2num,Web_XRD_Cell_1(Intermediate_variable_l==1,3)); % 转增
Web_XRD_Data(:,4)  = cellfun(@str2num,Web_XRD_Cell_1(Intermediate_variable_l==1,4)); % 派息

%% 配股数据处理

% 配股
[~,TableCell] = GetTableFromWeb(URL);

TableInd = 20;
TempCell = TableCell{TableInd};
TempCell = TempCell(3,:);

if size(TempCell,2) == 1 || strcmpi(TempCell{1,1},'暂时没有数据！')
    Web_XRD_Cell_2 = [];
else
    TempCell = TempCell(:,1:9);
    
    Web_XRD_Cell_2 = [{'公告日期','配股方案（每10股配股股数）','配股价格（元）',...
        '基准股本（万股）','除权除息日','股权登记日','缴款起始日','缴款终止日',...
        '配股上市日'};TempCell];
    
    % 合并分红增股与配股数据
    
    [Web_XRD_Cell_2_Row,Web_XRD_Cell_2_Column_2] = size(Web_XRD_Cell_2);
    Intermediate_variable_XRDCell2 = zeros(Web_XRD_Cell_2_Row-1,3);
    Intermediate_variable_XRDCell2(:,1) = datenum(Web_XRD_Cell_2(2:end,5));
    Intermediate_variable_XRDCell2(:,2) = cellfun(@str2num,Web_XRD_Cell_2(2:end,2));
    Intermediate_variable_XRDCell2(:,3) = cellfun(@str2num,Web_XRD_Cell_2(2:end,3));
    
    for Intermediate_variable_i = 1 : Web_XRD_Cell_2_Row-1
        Intermediate_variable_location = ...
            find(Web_XRD_Data(:,1)==Intermediate_variable_XRDCell2(Intermediate_variable_i,1));
        if ~isempty(Intermediate_variable_location)
            Web_XRD_Data(Intermediate_variable_location,5:6) = ...
                Intermediate_variable_XRDCell2(Intermediate_variable_i,2:3);
        else
            Web_XRD_Data(end+1,:) = ...
                [Intermediate_variable_XRDCell2(Intermediate_variable_i,1),0,0,0,...
                Intermediate_variable_XRDCell2(Intermediate_variable_i,2:3)];
        end
    end
end

% if Intermediate_variable_k ~= Web_Ori_Matches_length
%
%     Intermediate_variable_j = 1;
%     Intermediate_variable_q2 = repmat(1:9,1,ceil(Web_Ori_Matches_length/9))';
%     for Intermediate_variable_i = Intermediate_variable_k : Web_Ori_Matches_length
%         if ~isempty(str2num(Intermediate_variable_Matches(Intermediate_variable_i,1))) || Intermediate_variable_Matches(Intermediate_variable_i,1) == '-'
%             Web_XRD_Cell_2{ceil(Intermediate_variable_j/9),Intermediate_variable_q2(Intermediate_variable_j)} =  ...
%                 Intermediate_variable_Matches(Intermediate_variable_i,1:find(Intermediate_variable_Matches(Intermediate_variable_i,:)=='<')-1);
%             Intermediate_variable_j = Intermediate_variable_j + 1;
%         end
%     end
%
%     Web_XRD_Cell_2 = [{'公告日期','配股方案（每10股配股股数）','配股价格（元）',...
%         '基准股本（万股）','除权除息日','股权登记日','缴款起始日','缴款终止日',...
%         '配股上市日'};Web_XRD_Cell_2];
%
%     % 合并分红增股与配股数据
%
%     [Web_XRD_Cell_2_Row,Web_XRD_Cell_2_Column_2] = size(Web_XRD_Cell_2);
%     Intermediate_variable_XRDCell2 = zeros(Web_XRD_Cell_2_Row-1,3);
%     Intermediate_variable_XRDCell2(:,1) = datenum(Web_XRD_Cell_2(2:end,5));
%     Intermediate_variable_XRDCell2(:,2) = cellfun(@str2num,Web_XRD_Cell_2(2:end,2));
%     Intermediate_variable_XRDCell2(:,3) = cellfun(@str2num,Web_XRD_Cell_2(2:end,3));
%
%     for Intermediate_variable_i = 1 : Web_XRD_Cell_2_Row-1
%         Intermediate_variable_location = ...
%             find(Web_XRD_Data(:,1)==Intermediate_variable_XRDCell2(Intermediate_variable_i,1));
%         if ~isempty(Intermediate_variable_location)
%             Web_XRD_Data(Intermediate_variable_location,5:6) = ...
%                 Intermediate_variable_XRDCell2(Intermediate_variable_i,2:3);
%         else
%             Web_XRD_Data(end+1,:) = ...
%                 [Intermediate_variable_XRDCell2(Intermediate_variable_i,1),0,0,0,...
%                 Intermediate_variable_XRDCell2(Intermediate_variable_i,2:3)];
%         end
%     end
% else
%     Web_XRD_Cell_2 = [];
% end

Web_XRD_Data(:,1)  = str2num( datestr(Web_XRD_Data(:,1),'yyyymmdd') );

Web_XRD_Data = sortrows(Web_XRD_Data,1);
end
function [s,status] = urlread_General(url,varargin)
%URLREAD Returns the contents of a URL as a string.
%   S = URLREAD('URL') reads the content at a URL into a string, S.  If the
%   server returns binary data, the string will contain garbage.
%
%   S = URLREAD('URL','method',PARAMS) passes information to the server as
%   part of the request.  The 'method' can be 'get', or 'post' and PARAMS is a
%   cell array of param/value pairs.
%
%   S = URLREAD(...,'Timeout',T) sets a timeout, in seconds, when the function
%   will error rather than continue to wait for the server to respond or send
%   data.
%
%   [S,STATUS] = URLREAD(...) catches any errors and returns 1 if the file
%   downloaded successfully and 0 otherwise.
%
%   Examples:
%   s = urlread('http://www.mathworks.com')
%   s = urlread('ftp://ftp.mathworks.com/README')
%   s = urlread(['file:///' fullfile(prefdir,'history.m')])
%
%   From behind a firewall, use the Preferences to set your proxy server.
%
%   See also URLWRITE.

%   Matthew J. Simoneau, 13-Nov-2001
%   Copyright 1984-2011 The MathWorks, Inc.

% Do we want to throw errors or catch them?
if nargout == 2
    catchErrors = true;
else
    catchErrors = false;
end

[s,status] = urlreadwrite_General(mfilename,catchErrors,url,varargin{:});
end
function [urlConnection,errorid,errormsg] = urlreadwrite(fcn,urlChar)
%URLREADWRITE A helper function for URLREAD and URLWRITE.

%   Matthew J. Simoneau, June 2005
%   Copyright 1984-2007 The MathWorks, Inc.
%   $Revision: 1.1.6.4 $ $Date: 2009/02/10 21:04:47 $

% Default output arguments.
urlConnection = [];
errorid = '';
errormsg = '';

% Determine the protocol (before the ":").
protocol = urlChar(1:min(find(urlChar==':'))-1);

% Try to use the native handler, not the ice.* classes.
switch protocol
    case 'http'
        try
            handler = sun.net.www.protocol.http.Handler;
        catch exception %#ok
            handler = [];
        end
    case 'https'
        try
            handler = sun.net.www.protocol.https.Handler;
        catch exception %#ok
            handler = [];
        end
    otherwise
        handler = [];
end

% Create the URL object.
try
    if isempty(handler)
        url = java.net.URL(urlChar);
    else
        url = java.net.URL([],urlChar,handler);
    end
catch exception %#ok
    errorid = ['MATLAB:' fcn ':InvalidUrl'];
    errormsg = 'Either this URL could not be parsed or the protocol is not supported.';
    return
end

% Get the proxy information using MathWorks facilities for unified proxy
% prefence settings.
mwtcp = com.mathworks.net.transport.MWTransportClientPropertiesFactory.create();
proxy = mwtcp.getProxy();


% Open a connection to the URL.
if isempty(proxy)
    urlConnection = url.openConnection;
else
    urlConnection = url.openConnection(proxy);
end
end
function [output,status] = urlreadwrite_General(fcn,catchErrors,varargin)
%URLREADWRITE A helper function for URLREAD and URLWRITE.

%   Matthew J. Simoneau, June 2005
% 	Sharath Prabhal,     September 2012
%   Copyright 1984-2012 The MathWorks, Inc.

% This function requires Java.
error(javachk('jvm',fcn))
import com.mathworks.mlwidgets.io.InterruptibleStreamCopier;

% Be sure the proxy settings are set.
com.mathworks.mlwidgets.html.HTMLPrefs.setProxySettings

% Parse inputs.
inputs = parseInputs(fcn,varargin);
urlChar = inputs.url;

% Set default outputs.
output = '';
status = 0;

% GET method.  Tack param/value to end of URL.
for i = 1:2:numel(inputs.get)
    if (i == 1), separator = '?'; else separator = '&'; end
    param = char(java.net.URLEncoder.encode(inputs.get{i}));
    value = char(java.net.URLEncoder.encode(inputs.get{i+1}));
    urlChar = [urlChar separator param '=' value];
end

% Create a urlConnection.
[urlConnection,errorid] = getUrlConnection(urlChar,inputs.timeout,...
    inputs.useragent,inputs.authentication, inputs.username, inputs.password);
if isempty(urlConnection)
    if catchErrors, return
    else error(mm(fcn,errorid));
    end
end

% POST method.  Write param/values to server.
if ~isempty(inputs.post)
    try
        urlConnection.setDoOutput(true);
        urlConnection.setRequestProperty( ...
            'Content-Type','application/x-www-form-urlencoded');
        printStream = java.io.PrintStream(urlConnection.getOutputStream);
        for i=1:2:length(inputs.post)
            if (i > 1), printStream.print('&'); end
            param = char(java.net.URLEncoder.encode(inputs.post{i}));
            value = char(java.net.URLEncoder.encode(inputs.post{i+1}));
            printStream.print([param '=' value]);
        end
        printStream.close;
    catch
        if catchErrors, return
        else error(mm(fcn,'PostFailed'));
        end
    end
end

% Get the outputStream.
switch fcn
    case 'urlread_General'
        outputStream = java.io.ByteArrayOutputStream;
    case 'urlwrite_General'
        [file,outputStream] = getFileOutputStream(inputs.filename);
end

% Read the data from the connection.
try
    inputStream = urlConnection.getInputStream;
    % This StreamCopier is unsupported and may change at any time.
    isc = InterruptibleStreamCopier.getInterruptibleStreamCopier;
    isc.copyStream(inputStream,outputStream);
    inputStream.close;
    outputStream.close;
catch e
    outputStream.close;
    if strcmp(fcn,'urlwrite_General')
        delete(file);
    end
    if catchErrors
        return
    elseif strfind(e.message,'java.net.SocketTimeoutException:')
        error(mm(fcn,'Timeout'));
    elseif strfind(e.message,'java.net.UnknownHostException:')
        host = regexp(e.message,'java.net.UnknownHostException: ([^\n\r]*)','tokens','once');
        error(mm(fcn,'UnknownHost',host{1}));
    elseif strfind(e.message,'java.io.FileNotFoundException:')
        error(mm(fcn,'FileNotFound'));
    elseif strfind(e.message,'java.net.Authenticator.requestPasswordAuthentication')
        error(mm(fcn,'BasicAuthenticationFailed'));
    else
        error(mm(fcn,'ConnectionFailed'));
    end
end

if isempty(inputs.charset)
    contentType = char(urlConnection.getContentType);
    charsetMatch = regexp(contentType,'charset=([A-Za-z0-9\-\.:_])*','tokens','once');
    if isempty(charsetMatch)
        if strncmp(urlChar,'file:',4)
            charset = char(java.lang.System.getProperty('file.encoding'));
        else
            charset = 'UTF-8';
        end
    else
        charset = charsetMatch{1};
    end
else
    charset = inputs.charset;
end

switch fcn
    case 'urlread_General'
        output = native2unicode(typecast(outputStream.toByteArray','uint8'),charset);
    case 'urlwrite_General'
        output = char(file.getAbsolutePath);
end
status = 1;


    function m = mm(fcn,id,varargin)
        m = message(['MATLAB:' fcn ':' id],varargin{:});
        
        function results = parseInputs(fcn,args)
            p = inputParser;
            p.addRequired('url',@(x)validateattributes(x,{'char'},{'nonempty'}))
            if strcmp(fcn,'urlwrite_General')
                p.addRequired('filename',@(x)validateattributes(x,{'char'},{'nonempty'}))
            end
            p.addParamValue('get',{},@(x)checkpv(fcn,x))
            p.addParamValue('post',{},@(x)checkpv(fcn,x))
            p.addParamValue('timeout',[],@isnumeric)
            p.addParamValue('useragent',[],@ischar)
            p.addParamValue('charset',[],@ischar)
            p.addParamValue('authentication', [], @ischar)
            p.addParamValue('username', [], @ischar)
            p.addParamValue('password', [], @ischar)
            p.FunctionName = fcn;
            p.parse(args{:})
            results = p.Results;
            
            function checkpv(fcn,params)
                if mod(length(params),2) == 1
                    error(mm(fcn,'InvalidInput'));
                end
                
                function [urlConnection,errorid] = getUrlConnection(urlChar,timeout,...
                        userAgent,authentication,userName,password)
                    
                    import org.apache.commons.codec.binary.Base64;
                    % Default output arguments.
                    urlConnection = [];
                    errorid = '';
                    
                    % Determine the protocol (before the ":").
                    protocol = urlChar(1:find(urlChar==':',1)-1);
                    
                    % Try to use the native handler, not the ice.* classes.
                    switch protocol
                        case 'http'
                            try
                                handler = sun.net.www.protocol.http.Handler;
                            catch exception %#ok
                                handler = [];
                            end
                        case 'https'
                            try
                                handler = sun.net.www.protocol.https.Handler;
                            catch exception %#ok
                                handler = [];
                            end
                        otherwise
                            handler = [];
                    end
                    
                    % Create the URL object.
                    try
                        if isempty(handler)
                            url = java.net.URL(urlChar);
                        else
                            url = java.net.URL([],urlChar,handler);
                        end
                    catch exception %#ok
                        errorid = 'InvalidUrl';
                        return
                    end
                    
                    % Get the proxy information using the MATLAB proxy API.
                    proxy = com.mathworks.webproxy.WebproxyFactory.findProxyForURL(url);
                    
                    % Open a connection to the URL.
                    if isempty(proxy)
                        urlConnection = url.openConnection;
                    else
                        urlConnection = url.openConnection(proxy);
                    end
                    
                    % Set MATLAB as the User Agent
                    if isempty(userAgent)
                        userAgent = ['MATLAB R' version('-release') ' '  version('-description')];
                    end
                    urlConnection.setRequestProperty('User-Agent', userAgent);
                    
                    % If username and password exists, perform basic authentication
                    if strcmpi(authentication,'Basic')
                        usernamePassword = [userName ':' password];
                        usernamePasswordBytes = int8(usernamePassword)';
                        usernamePasswordBase64 = char(Base64.encodeBase64(usernamePasswordBytes)');
                        urlConnection.setRequestProperty('Authorization', ['Basic ' usernamePasswordBase64]);
                    end
                    
                    % Set the timeout.
                    if (nargin > 2 && ~isempty(timeout))
                        % Handle any numeric datatype and convert.
                        milliseconds = int32(double(timeout)*1000);
                        % Java inteprets 0 as no timeout. This would be confusing if we rounded
                        % to 0 from something else, e.g. "'timeout',.0001".
                        if milliseconds == 0
                            milliseconds = int32(1);
                        end
                        urlConnection.setConnectTimeout(milliseconds);
                        urlConnection.setReadTimeout(milliseconds);
                    end
                    
                    function [file,fileOutputStream] = getFileOutputStream(location)
                        % Specify the full path to the file so that getAbsolutePath will work when the
                        % current directory is not the startup directory and urlwrite is given a
                        % relative path.
                        file = java.io.File(location);
                        if ~file.isAbsolute
                            location = fullfile(pwd,location);
                            file = java.io.File(location);
                        end
                        
                        try
                            % Make sure the path isn't nonsense.
                            file = file.getCanonicalFile;
                            % Open the output file.
                            fileOutputStream = java.io.FileOutputStream(file);
                        catch
                            error(mm('urlwrite_General','InvalidOutputLocation',char(file.getAbsolutePath)));
                        end
                    end
                end
            end
        end
    end
end
function [f,status] = urlwrite_General(url,filename,varargin)
%URLWRITE Save the contents of a URL to a file.
%   URLWRITE(URL,FILENAME) saves the contents of a URL to a file.  FILENAME
%   can specify the complete path to a file.  If it is just the name, it will
%   be created in the current directory.
%
%   F = URLWRITE(...) returns the path to the file.
%
%   F = URLWRITE(...,METHOD,PARAMS) passes information to the server as
%   part of the request.  The 'method' can be 'get', or 'post' and PARAMS is a
%   cell array of param/value pairs.
%
%   URLWRITE(...,'Timeout',T) sets a timeout, in seconds, when the function
%   will error rather than continue to wait for the server to respond or send
%   data.
%
%   [F,STATUS] = URLWRITE(...) catches any errors and returns the error code.
%
%   Examples:
%   urlwrite('http://www.mathworks.com/',[tempname '.html'])
%   urlwrite('ftp://ftp.mathworks.com/README','readme.txt')
%   urlwrite(['file:///' fullfile(prefdir,'history.m')],'myhistory.m')
%
%   From behind a firewall, use the Preferences to set your proxy server.
%
%   See also URLREAD.

%   Matthew J. Simoneau, 13-Nov-2001
%   Copyright 1984-2011 The MathWorks, Inc.

% Do we want to throw errors or catch them?
if nargout == 2
    catchErrors = true;
else
    catchErrors = false;
end

[f,status] = urlreadwrite_General(mfilename,catchErrors,url,filename,varargin{:});
end
%% SQL CONNECTION
function [status,conn]=ConnectMysqlLocal()
databasename = 'quantbox';
username = 'root';
password = '940809';
driver = 'com.mysql.jdbc.Driver';
databaseurl = 'jdbc:mysql://localhost:3306/quantbox';
%% 建立 SQL 连接
conn = database(databasename, username, password, driver, databaseurl);
status=isopen(conn);
%% 连接判定：1 已连接 | 0 未连接
if isopen(conn)==1
    str='本地服务器连接成功';
    disp(str)
else
    str='本地服务器连接失败 请联系QQ279336410';
    disp(str)
    
end
end
function [status,conn]=ConnectMysqlCloud()
databasename = 'QUANTBOX';
username = 'root';
password = 'KlLn0NBkKn';
driver = 'com.mysql.jdbc.Driver';
databaseurl = 'jdbc:mysql://112.74.111.65:3306/QUANTBOX';
%% 建立 SQL 连接
conn = database(databasename, username, password, driver, databaseurl);
status=isopen(conn);
%% 连接判定：1 已连接 | 0 未连接
if isopen(conn)==1
    str='远程服务器连接成功';
    disp(str)
else
    str='远程服务器连接失败 请联系QQ279336410';
    disp(str)
end
end

%% Mail
function QuantboxSendMail(TargetAddress, content)
%by yutiansut
%2015/10
SourceAddress='yutiansut@163.com';
password='940809a950519';

%% SMTP_Server Get
ind = find( SourceAddress == '@', 1);
temp = SourceAddress(ind+1:end);
FieldName = temp;
SMTP_Server = ['smtp.',FieldName];
str='邮件正在发送中!';
disp(str);

%%
setpref('Internet','SMTP_Server',SMTP_Server);%SMTP服务器，记住要改成自己邮箱的smtp（百度一下就行了）
setpref('Internet','E_mail',SourceAddress);
setpref('Internet','SMTP_Username',SourceAddress);
setpref('Internet','SMTP_Password',password);

props = java.lang.System.getProperties;
props.setProperty('mail.smtp.auth','true');

sendmail(TargetAddress, 'Message from QUANTAXIS by yutiansut', content);
end
%% GET DATA SUBFUNCTION
function [DataOutput, Status] = GetBasicInfo_Mat(Code,BeginDate,EndDate,Type,Field)
% 获取基本信息 比如IPOdate
% by LiYang_faruto
% Email:farutoliyang@foxmail.com
% 2015/03/01
% % Input:
%
% Type
% Stock：获取股票数据 Future:获取期货数据
% StockIndex：获取股票相关指数数据
% FutureIndex：获取期货相关指数数据
% Field
% IPOdate
% Name
%% 输入输出预处理
DataOutput = [];
Status = [];
Status = 0;

if nargin < 5 || isempty(Field)
    Field = 'IPOdate';
end
if nargin < 4|| isempty(Type)
    Type = 'Stock';
end
if nargin < 3 || isempty(EndDate)
    EndDate = '20150101';
end
if nargin < 2 || isempty(BeginDate)
    BeginDate = '20140101';
end
if nargin < 1 || isempty(Code)
    Code = 'sh600588';
end

if strcmpi(Type,'Stock') || strcmpi(Type,'gp') ...
        || strcmpi(Type,'gupiao') || strcmpi(Type,'s')
    % 代码预处理，目标代码demo 'sh600588'
    if Code(1,1) == '6'
        Code = ['sh',Code];
    end
    if Code(1,1) == '0'|| Code(1,1) == '3'
        Code = ['sz',Code];
    end
    
end

% 日期时间预处理，目标形式 '20140101'
BeginDate(BeginDate == '-') = [];
EndDate(EndDate == '-') = [];

BeginDate = str2double(BeginDate);
EndDate = str2double(EndDate);
if BeginDate>EndDate
    str = ['开始日期需要小于等于结束日期，请检查输入参数！'];
    disp(str);
    return;
end
%% 获取股票数据
if strcmpi(Type,'Stock') || strcmpi(Type,'gp') ...
        || strcmpi(Type,'gupiao') || strcmpi(Type,'s')
    
    CodeInput = Code;
    
    % % 获取上市日期
    if strcmpi(Field, 'IPOdate')
        
        IPOdate = [];
        FolderStr_StockInfo = ['./DataBase/Stock/StockInfo_mat'];
        FileString_StockInfo = [FolderStr_StockInfo,'/',CodeInput,'_StockInfo.mat'];
        if exist(FileString_StockInfo, 'file') == 2
            str = ['load ',FileString_StockInfo];
            eval(str);
            
            IPOdate = StockInfo.IPOdate;
            
        end
        
        DataOutput = IPOdate;
    end
    
    % % 获取股票名称
    if strcmpi(Field, 'Name')
        FileString = 'StockList.mat';
        MatObj = matfile(FileString,'Writable',true);
        [nrows, ncols]=size(MatObj,'StockList');
        
        if nrows>1
            CodeDouble = str2num( CodeInput(3:end) );
            
            SearchIndex = MatObj.StockList(:,3);
            
            SearchIndex = cell2mat(SearchIndex);
            
            ind = find( SearchIndex==CodeDouble,1 );
            if ~isempty(ind)
                
                DataOutput = MatObj.StockList(ind,1);
                
            end
            
        end
        
    end
    
end
end
function [StockDataDouble,adjfactor] = GetStockTSDay_Web(StockCode,BeginDate,EndDate)
% by LiYang_faruto
% Email:farutoliyang@foxmail.com
% 2014/12/12
% Input:
% StockCode:字符阵列型，表示证券代码，如sh600000
% BeginDate:字符阵列型，表示希望获取股票数据所在时段的开始日期，如20140101
% EndDate:字符阵列型，表示希望获取股票数据所在时段的结束日期，如20150101
% Output:
% StockDataDouble: 日期 开 高 低 收 量(股) 额(元) 复权因子（后复权因子）
% 前复权因子 等于 后复权因子 的倒序排列
% 涨跌幅复权方式
% 后复权价格 = 交易价*后复权因子
% 前复权价格 = 交易价/前复权因子

% 获取数据所使用的URL
% http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000562.phtml?year=1994&jidu=1
% http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/000562.phtml?year=1995&jidu=4
% http://biz.finance.sina.com.cn/stock/flash_hq/kline_data.php?symbol=sz000562&end_date=20150101&begin_date=19940101
%% URL选择设定

URLflag = 2;

% 1 使用如下URL获取数据，但最多只能获取到20000101之后的数据，且无法获取成交额和复权因子，且数据有缺失
% http://biz.finance.sina.com.cn/stock/flash_hq/kline_data.php?symbol=sz000562&end_date=20150101&begin_date=19940101
% 2 使用如下URL获取数据，可以获取自上市日开始的左右数据和复权因子 19900101 部分数据也有缺失
% http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/000562.phtml?year=1995&jidu=4
% 类似的所有来自新浪的数据源都会有部分数据缺失
%% 输入输出预处理
if nargin < 3 || isempty(EndDate)
    EndDate = '20150101';
end
if nargin < 2 || isempty(BeginDate)
    BeginDate = '20100101';
end
if nargin < 1 || isempty(StockCode)
    StockCode = 'sh600588';
end

% 股票代码预处理，目标代码demo 'sh600588'
if 1 == URLflag
    if StockCode(1,1) == '6'
        StockCode = ['sh',StockCode];
    end
    if StockCode(1,1) == '0'|| StockCode(1,1) == '3'
        StockCode = ['sz',StockCode];
    end
end

% 股票代码预处理，目标代码demo '600588'
if 2 == URLflag
    StockCode(StockCode=='.') = [];
    if strcmpi(StockCode(1),'s')
        StockCode = StockCode(3:end);
    end
    if strcmpi(StockCode(end),'h') ||  strcmpi(StockCode(end),'z')
        StockCode = StockCode(1:end-2);
    end
end

% 输入日期预处理
if ~ischar( BeginDate )
    BeginDate = num2str(BeginDate);
end
BeginDate(BeginDate == '-') = [];
if ~ischar( EndDate )
    EndDate = num2str(EndDate);
end
EndDate(EndDate == '-') = [];

StockDataDouble = [];
adjfactor = [];

%% URLflag = 2
if 2 == URLflag
    % % http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/000562.phtml?year=1995&jidu=4
    
    sYear = str2double(BeginDate(1:4));
    eYear = str2double(EndDate(1:4));
    sM = str2double(BeginDate(5:6));
    eM = str2double(EndDate(5:6));
    for i = 1:4
        if sM>=3*i-2 && sM<=3*i
            sJiDu = i;
        end
        if eM>=3*i-2 && eM<=3*i
            eJiDu = i;
        end
    end
    
    Len = (eYear-sYear)*240+250;
    DTemp = cell(Len,8);
    rLen = 1;
    for i = sYear:eYear
        for j = 1:4
            %             YearDemo = i
            %             JiDuDemo = j
            if i == sYear && j < sJiDu
                continue;
            end
            if i == eYear && j > eJiDu
                continue;
            end
            %             YearDemo = i
            %             JiDuDemo = j
            
            URL = ...
                ['http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/' ...
                StockCode '.phtml?year=' num2str(i) '&jidu=' num2str(j)];
            
            [~,TableCell] = GetTableFromWeb(URL);
            
            if iscell( TableCell ) && ~isempty(TableCell)
                TableInd = 20;
                FIndCell = TableCell{TableInd};
            else
                FIndCell = [];
            end
            
            % 日期 开 高 收 低 量 额 复权因子
            FIndCell = FIndCell(3:end,:);
            FIndCell = FIndCell(end:(-1):1,:);
            
            if ~isempty(FIndCell)
                LenTemp = size(FIndCell,1);
                
                DTemp(rLen:(rLen+LenTemp-1),:) = FIndCell;
                rLen = rLen+LenTemp;
            end
        end
    end
    DTemp(rLen:end,:) = [];
    % 由于新股刚上市或网络等原因，DTemp为空
    if isempty(DTemp)
        return;
    end
    % 日期 开 高 收 低 量 额 复权因子
    % 调整成
    % 日期 开 高 低 收 量 额 复权因子
    Low = DTemp(:,5);
    Close = DTemp(:,4);
    DTemp = [ DTemp(:,1:3),Low,Close,DTemp(:,6:end) ];
    
    sTemp = cell2mat(DTemp(:,1));
    sTemp = datestr( datenum(sTemp,'yyyy-mm-dd'),'yyyymmdd' );
    Date = str2num( sTemp );
    
    Temp = DTemp(:,2:end);
    Data = cellfun(@str2double,Temp);
    
    % 由后复权数据反向生成 除权除息数据
    for i = 1:4
        Data(:,i) = Data(:,i)./Data(:,7);
    end
    Data(:,1:4) = round( Data(:,1:4)*100 )/100;
    
    DTemp = [Date, Data];
    
    % BeginDate,EndDate
    sDate = str2double(BeginDate);
    eDate = str2double(EndDate);
    
    [~,sInd] = min( abs(DTemp(:,1)-sDate) );
    [~,eInd] = min( abs(DTemp(:,1)-eDate) );
    
    StockDataDouble = DTemp(sInd:eInd,:);
    adjfactor = StockDataDouble(:,end);
end
%% URLflag = 1
if 1 == URLflag
    URL=['http://biz.finance.sina.com.cn/stock/flash_hq/kline_data.php?symbol=' StockCode '&end_date=' EndDate '&begin_date=' BeginDate];
    
    [URLchar, status] = urlread(URL,'TimeOut', 60);
    if status == 0
        str = ['urlread error:网页读取失败！请检查输入的网址或网络连接情况！'];
        disp(str);
        return;
    end
    URLString = java.lang.String(URLchar);
    
    expr = ['<content d=','.*?',...
        'bl="" />'];
    [matchstart,matchend,tokenindices,matchstring,tokenstring,tokenname,splitstring] = regexpi(URLchar, expr);
    Len = numel(matchstring);
    StockDataDouble = zeros(Len,6);
    
    for i = 1:Len
        strtemp = matchstring{i};
        
        [sind, eind] = regexpi(strtemp, 'd=.*? o');
        temp = strtemp(sind+3:eind-3);
        temp = temp([1:4,6:7,9:10]);
        StockDataDouble(i,1) = str2num(temp);
        
        [sind, eind] = regexpi(strtemp, 'o=.*? h');
        temp = strtemp(sind+3:eind-3);
        StockDataDouble(i,2) = str2num(temp);
        
        [sind, eind] = regexpi(strtemp, 'h=.*? c');
        temp = strtemp(sind+3:eind-3);
        StockDataDouble(i,3) = str2num(temp);
        
        [sind, eind] = regexpi(strtemp, 'l=.*? v');
        temp = strtemp(sind+3:eind-3);
        StockDataDouble(i,4) = str2num(temp);
        
        [sind, eind] = regexpi(strtemp, 'c=.*? l');
        temp = strtemp(sind+3:eind-3);
        StockDataDouble(i,5) = str2num(temp);
        
        [sind, eind] = regexpi(strtemp, 'v=.*? b');
        temp = strtemp(sind+3:eind-3);
        StockDataDouble(i,6) = str2num(temp);
    end
end
end
function [Data,InitialDate] = GetIndexTSDay_Web(StockCode,BeginDate,EndDate,GetInitialDateFlag)
% by LiYang_faruto
% Email:farutoliyang@foxmail.com
% 2015/01/01
% Input:
% StockCode:字符阵列型，表示证券代码，如sh000001
% BeginDate:字符阵列型，表示希望获取股票数据所在时段的开始日期，如20140101
% EndDate:字符阵列型，表示希望获取股票数据所在时段的结束日期，如20150101
% Output:
% Data: 日期 开 高 低 收 量(股) 额(元)

% 获取数据所使用的URL
% http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000001/type/S.phtml?year=1990&jidu=4
% http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000300/type/S.phtml?year=2014&jidu=4
%% 输入输出预处理
if nargin < 4 || isempty(GetInitialDateFlag)
    GetInitialDateFlag = 0;
end
if nargin < 3 || isempty(EndDate)
    EndDate = '20150101';
end
if nargin < 2 || isempty(BeginDate)
    BeginDate = '20140101';
end
if nargin < 1 || isempty(StockCode)
    StockCode = 'sh000001';
end

% 代码预处理，目标代码demo '000001'
if strcmpi(StockCode(1),'s')
    StockCode = StockCode(3:end);
end
if strcmpi(StockCode(end),'h') ||  strcmpi(StockCode(end),'z')
    StockCode = StockCode(1:end-2);
end

% 日期时间预处理，目标形式 '20140101'
BeginDate(BeginDate == '-') = [];
EndDate(EndDate == '-') = [];

Data = [];
InitialDate = '19900101';

charset = 'gb2312';
%% 获取初始日期
if 1 == GetInitialDateFlag
    URL = ...
        ['http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/' ...
        StockCode '/type/S.phtml?year=2014&jidu=4'];
    
    if verLessThan('matlab', '8.3')
        [URLchar, status] = urlread_General(URL, 'Charset', charset, 'TimeOut', 60);
    else
        [URLchar, status] = urlread(URL, 'Charset', charset, 'TimeOut', 60);
    end
    if status == 0
        str = ['urlread error:网页读取失败！请检查输入的网址或网络连接情况！'];
        disp(str);
        return;
    end
    
    URLString = java.lang.String(URLchar);
    
    expr = ['<select name="year">','.*?', ...
        '</select>'];
    Content = regexpi(URLchar, expr,'match');
    if ~isempty( Content )
        Content = Content{1};
        expr = ['<option value=','.*?', ...
            '</option>'];
        tContent = regexpi(Content, expr,'match');
        if ~isempty( tContent )
            tContent = tContent{length(tContent)};
            expr = ['>','.*?', ...
                '<'];
            tC = regexpi(tContent, expr,'match');
            tC = tC{1};
            temp = tC(2:length(tC)-1);
            InitialDate = [temp,'0101'];
        end
    end
end
%% Get Data

% http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000300/type/S.phtml?year=2014&jidu=4

sYear = str2double(BeginDate(1:4));
eYear = str2double(EndDate(1:4));
sM = str2double(BeginDate(5:6));
eM = str2double(EndDate(5:6));
for i = 1:4
    if sM>=3*i-2 && sM<=3*i
        sJiDu = i;
    end
    if eM>=3*i-2 && eM<=3*i
        eJiDu = i;
    end
end

Len = (eYear-sYear)*240+250;
DTemp = cell(Len,7);
rLen = 1;
for i = sYear:eYear
    for j = 1:4
        %             YearDemo = i
        %             JiDuDemo = j
        if i == sYear && j < sJiDu
            continue;
        end
        if i == eYear && j > eJiDu
            continue;
        end
        %             YearDemo = i
        %             JiDuDemo = j
        
        URL = ...
            ['http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/' ...
            StockCode '/type/S.phtml?year=' num2str(i) '&jidu=' num2str(j)];
        
        [~,TableCell] = GetTableFromWeb(URL);
        
        if iscell( TableCell ) && ~isempty(TableCell) && size(TableCell,1)>4
            TableInd = 5;
            FIndCell = TableCell{TableInd};
        else
            FIndCell = [];
        end
        
        % 日期 开 高 收 低 量 额
        FIndCell = FIndCell(3:end,:);
        FIndCell = FIndCell(end:(-1):1,:);
        
        if ~isempty(FIndCell)
            LenTemp = size(FIndCell,1);
            
            DTemp(rLen:(rLen+LenTemp-1),:) = FIndCell;
            rLen = rLen+LenTemp;
        end
    end
end
DTemp(rLen:end,:) = [];
% 由于新上市或网络等原因，DTemp为空
if isempty(DTemp)
    return;
end
% 日期 开 高 收 低 量 额
% 调整成
% 日期 开 高 低 收 量 额
Low = DTemp(:,5);
Close = DTemp(:,4);
DTemp = [ DTemp(:,1:3),Low,Close,DTemp(:,6:end) ];

sTemp = cell2mat(DTemp(:,1));
sTemp = datestr( datenum(sTemp,'yyyy-mm-dd'),'yyyymmdd' );
Date = str2num( sTemp );

Temp = DTemp(:,2:end);
Data = cellfun(@str2double,Temp);

DTemp = [Date, Data];

% BeginDate,EndDate
sDate = str2double(BeginDate);
eDate = str2double(EndDate);

[~,sInd] = min( abs(DTemp(:,1)-sDate) );
[~,eInd] = min( abs(DTemp(:,1)-eDate) );

Data = DTemp(sInd:eInd,:);
end
%% 编译P文件
%fun = fullfile('yuiansutQUANTAXIS.m');
%pcode(fun);
%%
%%初始化数据库 USERLIST
%sqlquery=['CREATE TABLE `QUANTBOX`.`', 'StockList','` (`Name` TEXT NULL COMMENT '''',`FullID` TEXT NULL COMMENT '''',`DoubleID` DOUBLE NULL COMMENT '''');'];
%cusor=exec(conn,sqlquery);
%insert(conn,'StockList',{'Name','FullID','DoubleID'},StockList)
%% 策略用
%% 策略A
function [n]=trades(x)

[n1,n2]=size(x);

n=zeros(n1,n2);
x=abs(x);

for j=1:n2
    for i=1:n1-1
        if x(i,j)*x(i+1,j)==0&&abs(x(i+1,j))==1
            n(i+1,j)=1;
        end
    end
end
end
function [profitOut,portValue,myTrades]=pairstrading(x,Capital,d,window,t,ut,C,maxPeriod)

%  Classical Pairs Trading Using MatLab
%
% DESCRIPTION:
%     This function performs the classical pairs trading framework over a
%     matrix of prices using MatLab. The basic idea of pairs trading is to
%     take advantage of market mean reversion behavior in order to make
%     profit out of short and long positions. More details about this type
%     of quantitative trading strategy can be found at the pdf document in
%     the zip file. This function will calculate the total payoff from
%     using a certain ammount of capital in each positions. We also include
%     transaction costs in the function.
%
%     Empirical results regarding Classical Pairs Trading can be found at:
%
%     GATEV, E., GOETZMANN, W. N., ROUWENHORST, K. G. Pairs Trading:
%     Performance of a Relative Value Arbitrage Rule. Working Paper, Yale
%     School of Management. Available at SSRN:
%     http://ssrn.com/abstract=141615, 1999.
%
%     PERLIN, M. S. Evaluation of Pairs Trading Strategy at Brazilian
%     Financial Market. Unpublished Working Paper, 2006. Available at:
%     http://ssrn.com/abstract=952242
%
%       USAGE:
% [Results_Total,Results_Long,Results_Short]=pairstrading(x,Capital,d,window,t,ut,C,maxPeriod);
%
%       INPUT:
%               x - A matrix with the prices of all tested assets in the
%               pairs trading framework. The rows represents the time and
%               the collums represents each asset.
%
%               Capital - How much money is invested in each trade (same unit
%               as the prices in x (e.g. 1,000 dollars).
%
%               d - The first trading period of the matrix. For example,
%               supose you have a matrix x with size [1500,40] (1500 prices
%               for 40 assets) and you stablish that d=200, then the
%               obervation 200 is the first trading period.
%
%               window - The size of the rolling window that will be used
%               to find the pairs. Using the last example, if d=200 and
%               window=100, then, for the trading period of 200, the
%               algorithm is going to use the observations 100:199 as a
%               training period.
%
%               t - The threshold parameter which determines what is a
%               unusual behavior.
%
%               ut - The periodicy that the function will updates the pairs of stocks. As
%               an example, if d=200, window=100 and ut=25, then the
%               function will update the pairs for each stock at
%               observations 225,250 and so on.
%
%               C - Transaction Cost, in money unit (e.g. dollar). This is
%               how much cost to set a long or a short position (e.g. 15
%               dollars).
%
%               maxPeriod - Maximum time period to hold any of the postions
%               (e.g. 5 day
%
%
%       OUTPUT:
%               profitOut - A structure containing the profits from the
%               trade
%
%               myTrades  - A structure containing the trades%
%
%   Author: Marcelo Scherer Perlin
%   Email:  marceloperlin@gmail.com
%   ICMA Centre / Reading University
[n1,n2]=size(x);

if nargin<8
    error('The function needs 8 arguments');
end

if n2==1
    error('The function accepts a matrix of prices as input, not a vector');
end

if d<=window
    error('The value of d should be lower than window, otherwise there will be missing observations for first trading day)');
end

if t<=0
    error('The value of t (threshold) should be higher than 0');
end

if ut<=0
    error('The value of ut should be higher than zero');
end

if C<0
    error('The value of C (money transaction cost) should be positive');
end

if maxPeriod<0
    error('The value of maxPerid should be an integer and positive');
end

% Calculation of first execution parameters

ut2=ut;
ut1=ut;
k1=1;

dist=zeros(n1-d+1,n2);

fprintf(1,'\nPerforming Pairs Trading. Please Hold.\n')

% Main Engine
pairsVec=cell(n1-d,1);
myTrades={};
anyPos=zeros(n1-d+1,n2);
idxTrades=1;
for k=1:n1-d
    
    % x2 is the training period for each time t. It evolves with k and
    % doesn't use the information of the observation d, which is the first
    % trading period in the simulation
    
    x2=x(d-window+k-1:d+k-2,:);
    
    x3=normdata(x2);         % Normalization of x2
    
    % Find/change the Pairs for each k periods based on the quadratic error criteria.
    
    if k==1||ut==1
        [p]=pairs(x3);
    else
        if k==ut1
            [p]=pairs(x3);
        end
    end
    
    pairsVec{k,1}=p;    % saving vectors of pairs
    
    % Trade in each day according to the logic of pairs trading
    
    for i=1:n2
        dist(k,i)=x3(window,i)-x3(window,p(i,1));
    end
    
    [idx]=find(abs(dist(k,:))>t);
    
    for i=1:length(idx)
        
        if (k==1)||(anyPos(k-1,idx(i))==0)  % if any position is already open, dont trade
            myTrades{idxTrades,1}.assetsNumber=[idx(i) p(idx(i))];
            myTrades{idxTrades,1}.obsNumber=d+k-1;
            
            if (dist(k,idx(i))>0)
                myTrades{idxTrades,1}.directionTrade=[-1  1];
            else
                myTrades{idxTrades,1}.directionTrade=[ 1 -1];
            end
            
            idxTrades=idxTrades+1;
        end
        
        anyPos(k,idx(i))=1;
        anyPos(k,p(idx(i)))=1;
        
    end
    
    % Output to screen
    
    nTrades=length(idx);
    
    fprintf(1,['\nObservation #',num2str(k),' -> Found ',num2str(nTrades), ' Diverging Pair(s).']);
    if k==ut1
        k1=k1+1;
        ut1=k1*ut2;
        fprintf(' Updating Pairs.')
    end
    
end

% Calculating profits..

fprintf(1,'\n\nCalculating Profits from trades...\n');

if isempty(myTrades)
    error('No trade found. Please input a lower value for t, or increase number of observations in sample.');
end

[profitOut,portValue,myTrades]=findProfit(x,d,[zeros(d-1,n2);dist],t,myTrades,Capital,C,maxPeriod,pairsVec);

figure(1)
plot([portValue.timeSeriesComb portValue.timeSeriesLong portValue.timeSeriesShort],'LineWidth',2);
legend('Combined', 'Just Long','Just Short','Location','nw');
xlabel('Time');
ylabel('Accumulated Profits');

% Printing results to prompt

fprintf(1,'\n\n ********* Calculations Finished *********\n');

fprintf(1,'\nLong Positions Results:\n');
fprintf(1,'\n Total Profit (minus transaction costs): %4.2f',(profitOut.totalProfitLong));
fprintf(1,'\n Number of Trades: %4i',size(myTrades,1));
fprintf(1,'\n Average Return per trade: %4.2f%%',mean(portValue.timeSeriesRetLong)*100);
fprintf(1,'\n Standard Deviation of Return per trade: %4.2f%%',std(portValue.timeSeriesRetLong)*100);

fprintf(1,'\n\nShort Positions Results:\n');
fprintf(1,'\n Total Profit (minus transaction costs): %4.2f',(profitOut.totalProfitShort));
fprintf(1,'\n Number of Trades: %4i',size(myTrades,1));
fprintf(1,'\n Average Return per trade: %4.2f%%',mean(portValue.timeSeriesRetShort)*100);
fprintf(1,'\n Standard Deviation of Return per trade: %4.2f%%',std(portValue.timeSeriesRetShort)*100);

fprintf(1,'\n\nCombined Positions Results:\n');
fprintf(1,'\n Total Profit (minus transaction costs): %4.2f',(profitOut.totalProfitComb));
fprintf(1,'\n Number of Trades: %4i',size(myTrades,1)*2);
fprintf(1,'\n Number of Periods with at least one open Positon: %4i (%4.2f%% of total trading time)',portValue.nDays.anyPos,portValue.nDays.anyPos./(n1-d)*100);
fprintf(1,'\n Number of Periods with at least one Trade: %4i (%4.2f%% of total trading time)',portValue.nDays.trades,portValue.nDays.trades./(n1-d)*100);
fprintf(1,'\n Average Number of Trades each Period: %4.2f',mean(portValue.nTrades(:,2)));
fprintf(1,'\n Average Return per trade: %4.2f%%',mean(portValue.timeSeriesRetComb)*100);
fprintf(1,'\n Standard Deviation of Return per trade: %4.2f%%',std(portValue.timeSeriesRetComb)*100);

fprintf(1,'\n');
end
function [pairs]=pairs(x)

[n2]=size(x,2);

Qdist=zeros(n2,n2);

for i=1:n2
    for j=1:i-1
        Qdist(i,j)=sum((x(:,i)-x(:,j)).^2);
        Qdist(j,i)=Qdist(i,j);
    end
    Qdist(i,i)=nan;
end

[~,n]=min(Qdist);
pairs(:,1)=n';

end
function [New_x]=normdata(x)

[n2]=size(x,2);

for i=1:n2
    ret=[0 ;(x(2:end,i)-x(1:end-1,i))./x(1:end-1,i)];
    New_x(:,i)=cumprod(1+ret);  % normalizing price series to P(t=0)=1
    
    mean_x=mean(New_x(:,i));
    std_x=std(New_x(:,i));
    
    New_x(:,i)=(New_x(:,i)-mean_x)/std_x;   % normalizing again
    
end
end
function [profitOut,portValue,myTrades]=findProfit(x,d,dist,t,myTrades,Capital,C,maxPeriod,pairsVec)

[nr,nc]=size(x);
nTrades=size(myTrades,1);
timeVec=zeros(nTrades,1);

longPos_Buy =zeros(nTrades,1);
shortPos_Buy=zeros(nTrades,1);

longPos_Sell =zeros(nTrades,1);
shortPos_Sell=zeros(nTrades,1);
anyPos=zeros(nr,nc);

%  iterate over the trades and find the bought and sold price for long and
% short positions

for i=1:nTrades
    
    longIdx=myTrades{i}.assetsNumber(myTrades{i}.directionTrade==1);
    shortIdx=myTrades{i}.assetsNumber(myTrades{i}.directionTrade==-1);
    
    timeVec(i,1)=myTrades{i}.obsNumber;
    
    longPos_Buy(i,1)=x(myTrades{i}.obsNumber,longIdx);
    shortPos_Sell(i,1)=x(myTrades{i}.obsNumber,shortIdx);
    
    myIdx=0;
    while 1 % iterate forward in time until position is closed
        
        myIdx=myIdx+1;
        
        if (abs(dist(myTrades{i}.obsNumber+myIdx,myTrades{i}.assetsNumber(1)))<t)   % if spread converges, close position
            break;
        end
        
        if ((myIdx+myTrades{i}.obsNumber)==nr)  % if trades passes number of observations, close position
            break;
        end
        
        asset1=myTrades{i}.assetsNumber(1);
        asset2=myTrades{i}.assetsNumber(2);
        myObs=myTrades{i}.obsNumber-d+1+myIdx;
        
        if (pairsVec{myObs}(asset1,1))~=asset2    % if pairs has changed from t to t+1, close position
            break
        end
        
        if myIdx>(maxPeriod-1)  % if number of holding period is higher than maxPeriod, break
            break;
        end
    end
    
    anyPos(timeVec(i,1):timeVec(i,1)+myIdx,[longIdx;shortIdx])=1;
    
    longPos_Sell(i,1)=x(myTrades{i}.obsNumber+myIdx,longIdx);
    shortPos_Buy(i,1) =x(myTrades{i}.obsNumber+myIdx,shortIdx);
    
    myTrades{i}.posHold=myIdx-1;
    
    if (myTrades{i}.directionTrade(1)==1)
        myTrades{i}.buyPrices =[longPos_Buy(i,1) shortPos_Buy(i,1)];
        myTrades{i}.sellPrice=[longPos_Sell(i,1) shortPos_Sell(i,1)];
    else
        myTrades{i}.buyPrices =[shortPos_Buy(i,1)  longPos_Buy(i,1)];
        myTrades{i}.sellPrice =[shortPos_Sell(i,1) longPos_Sell(i,1)];
    end
    
end

ProfitLong =Capital.*(longPos_Sell-longPos_Buy)./longPos_Buy-C;
ProfitShort=Capital.*(shortPos_Sell-shortPos_Buy)./shortPos_Sell-C;
ProfitComb=ProfitLong+ProfitShort;

profitOut.totalProfitLong =sum(ProfitLong);
profitOut.totalProfitShort=sum(ProfitShort);
profitOut.totalProfitComb =sum(ProfitComb);

uniqueTime=unique(timeVec);
n=size(uniqueTime,1);

portValue_Trades_Total=zeros(nr-d+1,1);
portValue_Trades_Long=zeros(nr-d+1,1);
portValue_Trades_Short=zeros(nr-d+1,1);
for i=1:n
    
    idx=uniqueTime(i);
    total=sum(ProfitComb((idx)==timeVec));
    long =sum(ProfitLong((idx)==timeVec));
    short=sum(ProfitShort((idx)==timeVec));
    
    portValue_Trades_Total(idx-d+1,1)=total;
    portValue_Trades_Long(idx-d+1,1)=long;
    portValue_Trades_Short(idx-d+1,1)=short;
    
    nTrades(i,1)=idx;
    nTrades(i,2)=(sum(timeVec==idx))*2;
    
end

% Passing output to structure

portValue.timeSeriesComb =(cumsum(portValue_Trades_Total));
portValue.timeSeriesLong =(cumsum(portValue_Trades_Long));
portValue.timeSeriesShort=(cumsum(portValue_Trades_Short));

portValue.timeSeriesRetComb =ProfitComb./Capital;   % this assumes that the short positions dont need capital for funding.
% the only capital needed is for long positions.
portValue.timeSeriesRetLong =ProfitLong./Capital;
portValue.timeSeriesRetShort=ProfitShort./Capital;

portValue.nDays.trades=size(uniqueTime,1);
portValue.nDays.anyPos=sum(sum(anyPos,2)~=0);

portValue.nTrades=nTrades;
end
%% 策略B  EMD EEMD CEEMDAN & HURST
function [hurst] = EstimateHurst(data0)   % data set

data=data0;         % make a local copy

[M,npoints]=size(data0);

yvals=zeros(1,npoints);
xvals=zeros(1,npoints);
data2=zeros(1,npoints);

index=0;
binsize=1;

while npoints>4
    
    y=std(data);
    index=index+1;
    xvals(index)=binsize;
    yvals(index)=binsize*y;
    
    npoints=fix(npoints/2);
    binsize=binsize*2;
    for ipoints=1:npoints % average adjacent points in pairs
        data2(ipoints)=(data(2*ipoints)+data((2*ipoints)-1))*0.5;
    end
    data=data2(1:npoints);
    
end % while

xvals=xvals(1:index);
yvals=yvals(1:index);

logx=log(xvals);
logy=log(yvals);

p2=polyfit(logx,logy,1);
hurst=p2(1); % Hurst exponent is the slope of the linear fit of log-log plot

return;
end
function [modes,its]=ceemdan(x,Nstd,NR,MaxIter)

% WARNING: for this code works it is necessary to include in the same
%directoy the file emd.m developed by Rilling and Flandrin.
%This file is available at %http://perso.ens-lyon.fr/patrick.flandrin/emd.html
%We use the default stopping criterion.
%We use the last modification: 3.2007
% 
% This version was run on Matlab 7.10.0 (R2010a)
%----------------------------------------------------------------------
%   INPUTs
%   x: signal to decompose
%   Nstd: noise standard deviation
%   NR: number of realizations
%   MaxIter: maximum number of sifting iterations allowed.
%
%  OUTPUTs
%  modes: contain the obtained modes in a matrix with the rows being the modes        
%   its: contain the sifting iterations needed for each mode for each realization (one row for each realization)
% -------------------------------------------------------------------------
%  Syntax
%
%  modes=ceemdan(x,Nstd,NR,MaxIter)
%  [modes its]=ceemdan(x,Nstd,NR,MaxIter)
%
%--------------------------------------------------------------------------
% This algorithm was presented at ICASSP 2011, Prague, Czech Republic
% Plese, if you use this code in your work, please cite the paper where the
% algorithm was first presented. 
% If you use this code, please cite:
%
% M.E.TORRES, M.A. COLOMINAS, G. SCHLOTTHAUER, P. FLANDRIN,
%  "A complete Ensemble Empirical Mode decomposition with adaptive noise," 
%  IEEE Int. Conf. on Acoust., Speech and Signal Proc. ICASSP-11, pp. 4144-4147, Prague (CZ)
%
% -------------------------------------------------------------------------
% Date: June 06,2011
% Authors:  Torres ME, Colominas MA, Schlotthauer G, Flandrin P.
% For problems with the code, please contact the authors:   
% To:  macolominas(AT)bioingenieria.edu.ar 
% CC:  metorres(AT)santafe-conicet.gov.ar
% -------------------------------------------------------------------------

x=x(:)';
desvio_x=std(x);
x=x/desvio_x;

modes=zeros(size(x));
temp=zeros(size(x));
aux=zeros(size(x));
acum=zeros(size(x));
iter=zeros(NR,round(log2(length(x))+5));

for i=1:NR
    white_noise{i}=randn(size(x));%creates the noise realizations
end;

for i=1:NR
    modes_white_noise{i}=emd(white_noise{i});%calculates the modes of white gaussian noise
end;

for i=1:NR %calculates the first mode
    temp=x+Nstd*white_noise{i};
    [temp, o, it]=emd(temp,'MAXMODES',1,'MAXITERATIONS',MaxIter);
    temp=temp(1,:);
    aux=aux+temp/NR;
    iter(i,1)=it;
end;

modes=aux; %saves the first mode
k=1;
aux=zeros(size(x));
acum=sum(modes,1);

while  nnz(diff(sign(diff(x-acum))))>2 %calculates the rest of the modes
    for i=1:NR
        tamanio=size(modes_white_noise{i});
        if tamanio(1)>=k+1
            noise=modes_white_noise{i}(k,:);
            noise=noise/std(noise);
            noise=Nstd*noise;
            try
                [temp, o, it]=emd(x-acum+std(x-acum)*noise,'MAXMODES',1,'MAXITERATIONS',MaxIter);
                temp=temp(1,:);
            catch
                it=0;
                temp=x-acum;
            end;
        else
            [temp, o, it]=emd(x-acum,'MAXMODES',1,'MAXITERATIONS',MaxIter);
            temp=temp(1,:);
        end;
        aux=aux+temp/NR;
    iter(i,k+1)=it;    
    end;
    modes=[modes;aux];
    aux=zeros(size(x));
    acum=zeros(size(x));
    acum=sum(modes,1);
    k=k+1;
end;
modes=[modes;(x-acum)];
[a b]=size(modes);
iter=iter(:,1:a);
modes=modes*desvio_x;
its=iter;
end
function [modos,its]=eemd(x,Nstd,NR,MaxIter)
%%
%--------------------------------------------------------------------------
%WARNING: this code needs to include in the same
%directoy the file emd.m developed by Rilling and Flandrin.
%This file is available at %http://perso.ens-lyon.fr/patrick.flandrin/emd.html
%We use the default stopping criterion.
%We use the last modification: 3.2007
% -------------------------------------------------------------------------
%  OUTPUT
%   modos: contain the obtained modes in a matrix with the rows being the modes
%   its: contain the iterations needed for each mode for each realization
%
%  INPUT
%  x: signal to decompose
%  Nstd: noise standard deviation
%  NR: number of realizations
%  MaxIter: maximum number of sifting iterations allowed.
% -------------------------------------------------------------------------
%   Syntax
%
%   modos=eemd(x,Nstd,NR,MaxIter)
%  [modos its]=eemd(x,Nstd,NR,MaxIter)
% -------------------------------------------------------------------------
%  NOTE:   if Nstd=0 and NR=1, the EMD decomposition is obtained.
% -------------------------------------------------------------------------
% EEMD was introduced in 
% Wu Z. and Huang N.
% "Ensemble Empirical Mode Decomposition: A noise-assisted data analysis method". 
% Advances in Adaptive Data Analysis. vol 1. pp 1-41, 2009.
%--------------------------------------------------------------------------
% The present EEMD implementation was used in
% M.E.TORRES, M.A. COLOMINAS, G. SCHLOTTHAUER, P. FLANDRIN,
%  "A complete Ensemble Empirical Mode decomposition with adaptive noise," 
%  IEEE Int. Conf. on Acoust., Speech and Signal Proc. ICASSP-11, pp. 4144-4147, Prague (CZ)
%
% in order to compare the performance of the new method CEEMDAN with the performance of the EEMD.
%
% -------------------------------------------------------------------------
% Date: June 06,2011
% Authors:  Torres ME, Colominas MA, Schlotthauer G, Flandrin P.
% For problems with the code, please contact the authors:   
% To:  macolominas(AT)bioingenieria.edu.ar 
% CC:  metorres(AT)santafe-conicet.gov.ar
% -------------------------------------------------------------------------
%  This version was run on Matlab 7.10.0 (R2010a)
%--------------------------------------------------------------------------

desvio_estandar=std(x);
x=x/desvio_estandar;
xconruido=x+Nstd*randn(size(x));
[modos, o, it]=emd(xconruido,'MAXITERATIONS',MaxIter);
modos=modos/NR;
iter=it;
if NR>=2
    for i=2:NR
        xconruido=x+Nstd*randn(size(x));
        [temp, ort, it]=emd(xconruido,'MAXITERATIONS',MaxIter);
        temp=temp/NR;
        lit=length(it);
        [p liter]=size(iter);
        if lit<liter
            it=[it zeros(1,liter-lit)];
        end;
        if liter<lit
            iter=[iter zeros(p,lit-liter)];
        end;
        
        iter=[iter;it];
        
        [filas columnas]=size(temp);
        [alto ancho]=size(modos);
        diferencia=alto-filas;
        if filas>alto
            modos=[modos; zeros(abs(diferencia),ancho)];
        end;
        if alto>filas
            temp=[temp;zeros(abs(diferencia),ancho)];
        end;
        
        modos=modos+temp;
    end;
end;
its=iter;
modos=modos*desvio_estandar;
end

%%
%EMD  computes Empirical Mode Decomposition
%
%
%   Syntax
%
%
% IMF = EMD(X)
% IMF = EMD(X,...,'Option_name',Option_value,...)
% IMF = EMD(X,OPTS)
% [IMF,ORT,NB_ITERATIONS] = EMD(...)
%
%
%   Description
%
%
% IMF = EMD(X) where X is a real vector computes the Empirical Mode
% Decomposition [1] of X, resulting in a matrix IMF containing 1 IMF per row, the
% last one being the residue. The default stopping criterion is the one proposed
% in [2]:
%
%   at each point, mean_amplitude < THRESHOLD2*envelope_amplitude
%   &
%   mean of boolean array {(mean_amplitude)/(envelope_amplitude) > THRESHOLD} < TOLERANCE
%   &
%   |#zeros-#extrema|<=1
%
% where mean_amplitude = abs(envelope_max+envelope_min)/2
% and envelope_amplitude = abs(envelope_max-envelope_min)/2
% 
% IMF = EMD(X) where X is a complex vector computes Bivariate Empirical Mode
% Decomposition [3] of X, resulting in a matrix IMF containing 1 IMF per row, the
% last one being the residue. The default stopping criterion is similar to the
% one proposed in [2]:
%
%   at each point, mean_amplitude < THRESHOLD2*envelope_amplitude
%   &
%   mean of boolean array {(mean_amplitude)/(envelope_amplitude) > THRESHOLD} < TOLERANCE
%
% where mean_amplitude and envelope_amplitude have definitions similar to the
% real case
%
% IMF = EMD(X,...,'Option_name',Option_value,...) sets options Option_name to
% the specified Option_value (see Options)
%
% IMF = EMD(X,OPTS) is equivalent to the above syntax provided OPTS is a struct 
% object with field names corresponding to option names and field values being the 
% associated values 
%
% [IMF,ORT,NB_ITERATIONS] = EMD(...) returns an index of orthogonality
%                       ________
%         _  |IMF(i,:).*IMF(j,:)|
%   ORT = \ _____________________
%         /
%         ?       || X ||?%        i~=j
%
% and the number of iterations to extract each mode in NB_ITERATIONS
%
%
%   Options
%
%
%  stopping criterion options:
%
% STOP: vector of stopping parameters [THRESHOLD,THRESHOLD2,TOLERANCE]
% if the input vector's length is less than 3, only the first parameters are
% set, the remaining ones taking default values.
% default: [0.05,0.5,0.05]
%
% FIX (int): disable the default stopping criterion and do exactly <FIX> 
% number of sifting iterations for each mode
%
% FIX_H (int): disable the default stopping criterion and do <FIX_H> sifting 
% iterations with |#zeros-#extrema|<=1 to stop [4]
%
%  bivariate/complex EMD options:
%
% COMPLEX_VERSION: selects the algorithm used for complex EMD ([3])
% COMPLEX_VERSION = 1: "algorithm 1"
% COMPLEX_VERSION = 2: "algorithm 2" (default)
% 
% NDIRS: number of directions in which envelopes are computed (default 4)
% rem: the actual number of directions (according to [3]) is 2*NDIRS
% 
%  other options:
%
% T: sampling times (line vector) (default: 1:length(x))
%
% MAXITERATIONS: maximum number of sifting iterations for the computation of each
% mode (default: 2000)
%
% MAXMODES: maximum number of imfs extracted (default: Inf)
%
% DISPLAY: if equals to 1 shows sifting steps with pause
% if equals to 2 shows sifting steps without pause (movie style)
% rem: display is disabled when the input is complex
%
% INTERP: interpolation scheme: 'linear', 'cubic', 'pchip' or 'spline' (default)
% see interp1 documentation for details
%
% MASK: masking signal used to improve the decomposition according to [5]
%
%
%   Examples
%
%
%X = rand(1,512);
%
%IMF = emd(X);
%
%IMF = emd(X,'STOP',[0.1,0.5,0.05],'MAXITERATIONS',100);
%
%T=linspace(0,20,1e3);
%X = 2*exp(i*T)+exp(3*i*T)+.5*T;
%IMF = emd(X,'T',T);
%
%OPTIONS.DISLPAY = 1;
%OPTIONS.FIX = 10;
%OPTIONS.MAXMODES = 3;
%[IMF,ORT,NBITS] = emd(X,OPTIONS);
%
%
%   References
%
%
% [1] N. E. Huang et al., "The empirical mode decomposition and the
% Hilbert spectrum for non-linear and non stationary time series analysis",
% Proc. Royal Soc. London A, Vol. 454, pp. 903-995, 1998
%
% [2] G. Rilling, P. Flandrin and P. Gon鏰lves
% "On Empirical Mode Decomposition and its algorithms",
% IEEE-EURASIP Workshop on Nonlinear Signal and Image Processing
% NSIP-03, Grado (I), June 2003
%
% [3] G. Rilling, P. Flandrin, P. Gon鏰lves and J. M. Lilly.,
% "Bivariate Empirical Mode Decomposition",
% Signal Processing Letters (submitted)
%
% [4] N. E. Huang et al., "A confidence limit for the Empirical Mode
% Decomposition and Hilbert spectral analysis",
% Proc. Royal Soc. London A, Vol. 459, pp. 2317-2345, 2003
%
% [5] R. Deering and J. F. Kaiser, "The use of a masking signal to improve 
% empirical mode decomposition", ICASSP 2005
%
%
% See also
%  emd_visu (visualization),
%  emdc, emdc_fix (fast implementations of EMD),
%  cemdc, cemdc_fix, cemdc2, cemdc2_fix (fast implementations of bivariate EMD),
%  hhspectrum (Hilbert-Huang spectrum)
%
%
% G. Rilling, last modification: 3.2007
% gabriel.rilling@ens-lyon.fr


function [imf,ort,nbits] = emd(varargin)

[x,t,sd,sd2,tol,MODE_COMPLEX,ndirs,display_sifting,sdt,sd2t,r,imf,k,nbit,NbIt,MAXITERATIONS,FIXE,FIXE_H,MAXMODES,INTERP,mask] = init(varargin{:});

if display_sifting
  fig_h = figure;
end


%main loop : requires at least 3 extrema to proceed
while (~stop_EMD(r,MODE_COMPLEX,ndirs) && (k < MAXMODES+1 || MAXMODES == 0) && ~any(mask))

  % current mode
  m = r;

  % mode at previous iteration
  mp = m;

  %computation of mean and stopping criterion
  if FIXE
    [stop_sift,moyenne] = stop_sifting_fixe(t,m,INTERP,MODE_COMPLEX,ndirs);
  elseif FIXE_H
    stop_count = 0;
    [stop_sift,moyenne] = stop_sifting_fixe_h(t,m,INTERP,stop_count,FIXE_H,MODE_COMPLEX,ndirs);
  else
    [stop_sift,moyenne] = stop_sifting(m,t,sd,sd2,tol,INTERP,MODE_COMPLEX,ndirs);
  end

  % in case the current mode is so small that machine precision can cause
  % spurious extrema to appear
  if (max(abs(m))) < (1e-10)*(max(abs(x)))
    if ~stop_sift
      warning('emd:warning','forced stop of EMD : too small amplitude')
    else
      disp('forced stop of EMD : too small amplitude')
    end
    break
  end


  % sifting loop
  while ~stop_sift && nbit<MAXITERATIONS
    if(~MODE_COMPLEX && nbit>MAXITERATIONS/5 && mod(nbit,floor(MAXITERATIONS/10))==0 && ~FIXE && nbit > 100)
      disp(['mode ',int2str(k),', iteration ',int2str(nbit)])
      if exist('s','var')
        disp(['stop parameter mean value : ',num2str(s)])
      end
      [im,iM] = extr(m);
      disp([int2str(sum(m(im) > 0)),' minima > 0; ',int2str(sum(m(iM) < 0)),' maxima < 0.'])
    end

    %sifting
    m = m - moyenne;

    %computation of mean and stopping criterion
    if FIXE
      [stop_sift,moyenne] = stop_sifting_fixe(t,m,INTERP,MODE_COMPLEX,ndirs);
    elseif FIXE_H
      [stop_sift,moyenne,stop_count] = stop_sifting_fixe_h(t,m,INTERP,stop_count,FIXE_H,MODE_COMPLEX,ndirs);
    else
      [stop_sift,moyenne,s] = stop_sifting(m,t,sd,sd2,tol,INTERP,MODE_COMPLEX,ndirs);
    end

    % display
    if display_sifting && ~MODE_COMPLEX
      NBSYM = 2;
      [indmin,indmax] = extr(mp);
      [tmin,tmax,mmin,mmax] = boundary_conditions(indmin,indmax,t,mp,mp,NBSYM);
      envminp = interp1(tmin,mmin,t,INTERP);
      envmaxp = interp1(tmax,mmax,t,INTERP);
      envmoyp = (envminp+envmaxp)/2;
      if FIXE || FIXE_H
        display_emd_fixe(t,m,mp,r,envminp,envmaxp,envmoyp,nbit,k,display_sifting)
      else
        sxp=2*(abs(envmoyp))./(abs(envmaxp-envminp));
        sp = mean(sxp);
        display_emd(t,m,mp,r,envminp,envmaxp,envmoyp,s,sp,sxp,sdt,sd2t,nbit,k,display_sifting,stop_sift)
      end
    end

    mp = m;
    nbit=nbit+1;
    NbIt=NbIt+1;

    if(nbit==(MAXITERATIONS-1) && ~FIXE && nbit > 100)
      if exist('s','var')
        warning('emd:warning',['forced stop of sifting : too many iterations... mode ',int2str(k),'. stop parameter mean value : ',num2str(s)])
      else
        warning('emd:warning',['forced stop of sifting : too many iterations... mode ',int2str(k),'.'])
      end
    end

  end % sifting loop
  imf(k,:) = m;
  if display_sifting
    disp(['mode ',int2str(k),' stored'])
  end
  nbits(k) = nbit;
  k = k+1;


  r = r - m;
  nbit=0;


end %main loop

if any(r) && ~any(mask)
  imf(k,:) = r;
end

ort = io(x,imf);

if display_sifting
  close
end
end

%---------------------------------------------------------------------------------------------------
% tests if there are enough (3) extrema to continue the decomposition
function stop = stop_EMD(r,MODE_COMPLEX,ndirs)
if MODE_COMPLEX
  for k = 1:ndirs
    phi = (k-1)*pi/ndirs;
    [indmin,indmax] = extr(real(exp(i*phi)*r));
    ner(k) = length(indmin) + length(indmax);
  end
  stop = any(ner < 3);
else
  [indmin,indmax] = extr(r);
  ner = length(indmin) + length(indmax);
  stop = ner < 3;
end
end

%---------------------------------------------------------------------------------------------------
% computes the mean of the envelopes and the mode amplitude estimate
function [envmoy,nem,nzm,amp] = mean_and_amplitude(m,t,INTERP,MODE_COMPLEX,ndirs)
NBSYM = 2;
if MODE_COMPLEX
  switch MODE_COMPLEX
    case 1
      for k = 1:ndirs
        phi = (k-1)*pi/ndirs;
        y = real(exp(-i*phi)*m);
        [indmin,indmax,indzer] = extr(y);
        nem(k) = length(indmin)+length(indmax);
        nzm(k) = length(indzer);
        [tmin,tmax,zmin,zmax] = boundary_conditions(indmin,indmax,t,y,m,NBSYM);
        envmin(k,:) = interp1(tmin,zmin,t,INTERP);
        envmax(k,:) = interp1(tmax,zmax,t,INTERP);
      end
      envmoy = mean((envmin+envmax)/2,1);
      if nargout > 3
        amp = mean(abs(envmax-envmin),1)/2;
      end
    case 2
      for k = 1:ndirs
        phi = (k-1)*pi/ndirs;
        y = real(exp(-i*phi)*m);
        [indmin,indmax,indzer] = extr(y);
        nem(k) = length(indmin)+length(indmax);
        nzm(k) = length(indzer);
        [tmin,tmax,zmin,zmax] = boundary_conditions(indmin,indmax,t,y,y,NBSYM);
        envmin(k,:) = exp(i*phi)*interp1(tmin,zmin,t,INTERP);
        envmax(k,:) = exp(i*phi)*interp1(tmax,zmax,t,INTERP);
      end
      envmoy = mean((envmin+envmax),1);
      if nargout > 3
        amp = mean(abs(envmax-envmin),1)/2;
      end
  end
else
  [indmin,indmax,indzer] = extr(m);
  nem = length(indmin)+length(indmax);
  nzm = length(indzer);
  [tmin,tmax,mmin,mmax] = boundary_conditions(indmin,indmax,t,m,m,NBSYM);
  envmin = interp1(tmin,mmin,t,INTERP);
  envmax = interp1(tmax,mmax,t,INTERP);
  envmoy = (envmin+envmax)/2;
  if nargout > 3
    amp = mean(abs(envmax-envmin),1)/2;
  end
end
end

%-------------------------------------------------------------------------------
% default stopping criterion
function [stop,envmoy,s] = stop_sifting(m,t,sd,sd2,tol,INTERP,MODE_COMPLEX,ndirs)
try
  [envmoy,nem,nzm,amp] = mean_and_amplitude(m,t,INTERP,MODE_COMPLEX,ndirs);
  sx = abs(envmoy)./amp;
  s = mean(sx);
  stop = ~((mean(sx > sd) > tol | any(sx > sd2)) & (all(nem > 2)));
  if ~MODE_COMPLEX
    stop = stop && ~(abs(nzm-nem)>1);
  end
catch
  stop = 1;
  envmoy = zeros(1,length(m));
  s = NaN;
end
end

%-------------------------------------------------------------------------------
% stopping criterion corresponding to option FIX
function [stop,moyenne]= stop_sifting_fixe(t,m,INTERP,MODE_COMPLEX,ndirs)
try
  moyenne = mean_and_amplitude(m,t,INTERP,MODE_COMPLEX,ndirs);
  stop = 0;
catch
  moyenne = zeros(1,length(m));
  stop = 1;
end
end

%-------------------------------------------------------------------------------
% stopping criterion corresponding to option FIX_H
function [stop,moyenne,stop_count]= stop_sifting_fixe_h(t,m,INTERP,stop_count,FIXE_H,MODE_COMPLEX,ndirs)
try
  [moyenne,nem,nzm] = mean_and_amplitude(m,t,INTERP,MODE_COMPLEX,ndirs);
  if (all(abs(nzm-nem)>1))
    stop = 0;
    stop_count = 0;
  else
    stop_count = stop_count+1;
    stop = (stop_count == FIXE_H);
  end
catch
  moyenne = zeros(1,length(m));
  stop = 1;
end
end

%-------------------------------------------------------------------------------
% displays the progression of the decomposition with the default stopping criterion
function display_emd(t,m,mp,r,envmin,envmax,envmoy,s,sb,sx,sdt,sd2t,nbit,k,display_sifting,stop_sift)
subplot(4,1,1)
plot(t,mp);hold on;
plot(t,envmax,'--k');plot(t,envmin,'--k');plot(t,envmoy,'r');
title(['IMF ',int2str(k),';   iteration ',int2str(nbit),' before sifting']);
set(gca,'XTick',[])
hold  off
subplot(4,1,2)
plot(t,sx)
hold on
plot(t,sdt,'--r')
plot(t,sd2t,':k')
title('stop parameter')
set(gca,'XTick',[])
hold off
subplot(4,1,3)
plot(t,m)
title(['IMF ',int2str(k),';   iteration ',int2str(nbit),' after sifting']);
set(gca,'XTick',[])
subplot(4,1,4);
plot(t,r-m)
title('residue');
disp(['stop parameter mean value : ',num2str(sb),' before sifting and ',num2str(s),' after'])
if stop_sift
  disp('last iteration for this mode')
end
if display_sifting == 2
  pause(0.01)
else
  pause
end
end

%---------------------------------------------------------------------------------------------------
% displays the progression of the decomposition with the FIX and FIX_H stopping criteria
function display_emd_fixe(t,m,mp,r,envmin,envmax,envmoy,nbit,k,display_sifting)
subplot(3,1,1)
plot(t,mp);hold on;
plot(t,envmax,'--k');plot(t,envmin,'--k');plot(t,envmoy,'r');
title(['IMF ',int2str(k),';   iteration ',int2str(nbit),' before sifting']);
set(gca,'XTick',[])
hold  off
subplot(3,1,2)
plot(t,m)
title(['IMF ',int2str(k),';   iteration ',int2str(nbit),' after sifting']);
set(gca,'XTick',[])
subplot(3,1,3);
plot(t,r-m)
title('residue');
if display_sifting == 2
  pause(0.01)
else
  pause
end
end

%---------------------------------------------------------------------------------------
% defines new extrema points to extend the interpolations at the edges of the
% signal (mainly mirror symmetry)
function [tmin,tmax,zmin,zmax] = boundary_conditions(indmin,indmax,t,x,z,nbsym)
	
	lx = length(x);
	
	if (length(indmin) + length(indmax) < 3)
		error('not enough extrema')
	end

    % boundary conditions for interpolations :

	if indmax(1) < indmin(1)
    	if x(1) > x(indmin(1))
			lmax = fliplr(indmax(2:min(end,nbsym+1)));
			lmin = fliplr(indmin(1:min(end,nbsym)));
			lsym = indmax(1);
		else
			lmax = fliplr(indmax(1:min(end,nbsym)));
			lmin = [fliplr(indmin(1:min(end,nbsym-1))),1];
			lsym = 1;
		end
	else

		if x(1) < x(indmax(1))
			lmax = fliplr(indmax(1:min(end,nbsym)));
			lmin = fliplr(indmin(2:min(end,nbsym+1)));
			lsym = indmin(1);
		else
			lmax = [fliplr(indmax(1:min(end,nbsym-1))),1];
			lmin = fliplr(indmin(1:min(end,nbsym)));
			lsym = 1;
		end
	end
    
	if indmax(end) < indmin(end)
		if x(end) < x(indmax(end))
			rmax = fliplr(indmax(max(end-nbsym+1,1):end));
			rmin = fliplr(indmin(max(end-nbsym,1):end-1));
			rsym = indmin(end);
		else
			rmax = [lx,fliplr(indmax(max(end-nbsym+2,1):end))];
			rmin = fliplr(indmin(max(end-nbsym+1,1):end));
			rsym = lx;
		end
	else
		if x(end) > x(indmin(end))
			rmax = fliplr(indmax(max(end-nbsym,1):end-1));
			rmin = fliplr(indmin(max(end-nbsym+1,1):end));
			rsym = indmax(end);
		else
			rmax = fliplr(indmax(max(end-nbsym+1,1):end));
			rmin = [lx,fliplr(indmin(max(end-nbsym+2,1):end))];
			rsym = lx;
		end
	end
    
	tlmin = 2*t(lsym)-t(lmin);
	tlmax = 2*t(lsym)-t(lmax);
	trmin = 2*t(rsym)-t(rmin);
	trmax = 2*t(rsym)-t(rmax);
    
	% in case symmetrized parts do not extend enough
	if tlmin(1) > t(1) || tlmax(1) > t(1)
		if lsym == indmax(1)
			lmax = fliplr(indmax(1:min(end,nbsym)));
		else
			lmin = fliplr(indmin(1:min(end,nbsym)));
		end
		if lsym == 1
			error('bug')
		end
		lsym = 1;
		tlmin = 2*t(lsym)-t(lmin);
		tlmax = 2*t(lsym)-t(lmax);
	end   
    
	if trmin(end) < t(lx) || trmax(end) < t(lx)
		if rsym == indmax(end)
			rmax = fliplr(indmax(max(end-nbsym+1,1):end));
		else
			rmin = fliplr(indmin(max(end-nbsym+1,1):end));
		end
	if rsym == lx
		error('bug')
	end
		rsym = lx;
		trmin = 2*t(rsym)-t(rmin);
		trmax = 2*t(rsym)-t(rmax);
	end 
          
	zlmax =z(lmax); 
	zlmin =z(lmin);
	zrmax =z(rmax); 
	zrmin =z(rmin);
     
	tmin = [tlmin t(indmin) trmin];
	tmax = [tlmax t(indmax) trmax];
	zmin = [zlmin z(indmin) zrmin];
	zmax = [zlmax z(indmax) zrmax];
end
    
%---------------------------------------------------------------------------------------------------
%extracts the indices of extrema
function [indmin, indmax, indzer] = extr(x,t)

if(nargin==1)
  t=1:length(x);
end

m = length(x);

if nargout > 2
  x1=x(1:m-1);
  x2=x(2:m);
  indzer = find(x1.*x2<0);

  if any(x == 0)
    iz = find( x==0 );
    indz = [];
    if any(diff(iz)==1)
      zer = x == 0;
      dz = diff([0 zer 0]);
      debz = find(dz == 1);
      finz = find(dz == -1)-1;
      indz = round((debz+finz)/2);
    else
      indz = iz;
    end
    indzer = sort([indzer indz]);
  end
end

d = diff(x);

n = length(d);
d1 = d(1:n-1);
d2 = d(2:n);
indmin = find(d1.*d2<0 & d1<0)+1;
indmax = find(d1.*d2<0 & d1>0)+1;


% when two or more successive points have the same value we consider only one extremum in the middle of the constant area
% (only works if the signal is uniformly sampled)

if any(d==0)

  imax = [];
  imin = [];

  bad = (d==0);
  dd = diff([0 bad 0]);
  debs = find(dd == 1);
  fins = find(dd == -1);
  if debs(1) == 1
    if length(debs) > 1
      debs = debs(2:end);
      fins = fins(2:end);
    else
      debs = [];
      fins = [];
    end
  end
  if length(debs) > 0
    if fins(end) == m
      if length(debs) > 1
        debs = debs(1:(end-1));
        fins = fins(1:(end-1));

      else
        debs = [];
        fins = [];
      end
    end
  end
  lc = length(debs);
  if lc > 0
    for k = 1:lc
      if d(debs(k)-1) > 0
        if d(fins(k)) < 0
          imax = [imax round((fins(k)+debs(k))/2)];
        end
      else
        if d(fins(k)) > 0
          imin = [imin round((fins(k)+debs(k))/2)];
        end
      end
    end
  end

  if length(imax) > 0
    indmax = sort([indmax imax]);
  end

  if length(imin) > 0
    indmin = sort([indmin imin]);
  end

end
end

%---------------------------------------------------------------------------------------------------

function ort = io(x,imf)
% ort = IO(x,imf) computes the index of orthogonality
%
% inputs : - x    : analyzed signal
%          - imf  : empirical mode decomposition

n = size(imf,1);

s = 0;

for i = 1:n
  for j =1:n
    if i~=j
      s = s + abs(sum(imf(i,:).*conj(imf(j,:)))/sum(x.^2));
    end
  end
end

ort = 0.5*s;
end
%---------------------------------------------------------------------------------------------------

function [x,t,sd,sd2,tol,MODE_COMPLEX,ndirs,display_sifting,sdt,sd2t,r,imf,k,nbit,NbIt,MAXITERATIONS,FIXE,FIXE_H,MAXMODES,INTERP,mask] = init(varargin)

x = varargin{1};
if nargin == 2
  if isstruct(varargin{2})
    inopts = varargin{2};
  else
    error('when using 2 arguments the first one is the analyzed signal X and the second one is a struct object describing the options')
  end
elseif nargin > 2
  try
    inopts = struct(varargin{2:end});
  catch
    error('bad argument syntax')
  end
end

% default for stopping
defstop = [0.05,0.5,0.05];

opt_fields = {'t','stop','display','maxiterations','fix','maxmodes','interp','fix_h','mask','ndirs','complex_version'};

defopts.stop = defstop;
defopts.display = 0;
defopts.t = 1:max(size(x));
defopts.maxiterations = 2000;
defopts.fix = 0;
defopts.maxmodes = 0;
defopts.interp = 'spline';
defopts.fix_h = 0;
defopts.mask = 0;
defopts.ndirs = 4;
defopts.complex_version = 2;

opts = defopts;



if(nargin==1)
  inopts = defopts;
elseif nargin == 0
  error('not enough arguments')
end


names = fieldnames(inopts);
for nom = names'
  if ~any(strcmpi(char(nom), opt_fields))
    error(['bad option field name: ',char(nom)])
  end
  if ~isempty(eval(['inopts.',char(nom)])) % empty values are discarded
    eval(['opts.',lower(char(nom)),' = inopts.',char(nom),';'])
  end
end

t = opts.t;
stop = opts.stop;
display_sifting = opts.display;
MAXITERATIONS = opts.maxiterations;
FIXE = opts.fix;
MAXMODES = opts.maxmodes;
INTERP = opts.interp;
FIXE_H = opts.fix_h;
mask = opts.mask;
ndirs = opts.ndirs;
complex_version = opts.complex_version;

if ~isvector(x)
  error('X must have only one row or one column')
end

if size(x,1) > 1
  x = x.';
end

if ~isvector(t)
  error('option field T must have only one row or one column')
end

if ~isreal(t)
  error('time instants T must be a real vector')
end

if size(t,1) > 1
  t = t';
end

if (length(t)~=length(x))
  error('X and option field T must have the same length')
end

if ~isvector(stop) || length(stop) > 3
  error('option field STOP must have only one row or one column of max three elements')
end

if ~all(isfinite(x))
  error('data elements must be finite')
end

if size(stop,1) > 1
  stop = stop';
end

L = length(stop);
if L < 3
  stop(3)=defstop(3);
end

if L < 2
  stop(2)=defstop(2);
end


if ~ischar(INTERP) || ~any(strcmpi(INTERP,{'linear','cubic','spline'}))
  error('INTERP field must be ''linear'', ''cubic'', ''pchip'' or ''spline''')
end

%special procedure when a masking signal is specified
if any(mask)
  if ~isvector(mask) || length(mask) ~= length(x)
    error('masking signal must have the same dimension as the analyzed signal X')
  end

  if size(mask,1) > 1
    mask = mask.';
  end
  opts.mask = 0;
  imf1 = emd(x+mask,opts);
  imf2 = emd(x-mask,opts);
  if size(imf1,1) ~= size(imf2,1)
    warning('emd:warning',['the two sets of IMFs have different sizes: ',int2str(size(imf1,1)),' and ',int2str(size(imf2,1)),' IMFs.'])
  end
  S1 = size(imf1,1);
  S2 = size(imf2,1);
  if S1 ~= S2
    if S1 < S2
      tmp = imf1;
      imf1 = imf2;
      imf2 = tmp;
    end
    imf2(max(S1,S2),1) = 0;
  end
  imf = (imf1+imf2)/2;

end


sd = stop(1);
sd2 = stop(2);
tol = stop(3);

lx = length(x);

sdt = sd*ones(1,lx);
sd2t = sd2*ones(1,lx);

if FIXE
  MAXITERATIONS = FIXE;
  if FIXE_H
    error('cannot use both ''FIX'' and ''FIX_H'' modes')
  end
end

MODE_COMPLEX = ~isreal(x)*complex_version;
if MODE_COMPLEX && complex_version ~= 1 && complex_version ~= 2
  error('COMPLEX_VERSION parameter must equal 1 or 2')
end


% number of extrema and zero-crossings in residual
ner = lx;
nzr = lx;

r = x;

if ~any(mask) % if a masking signal is specified "imf" already exists at this stage
  imf = [];
end
k = 1;

% iterations counter for extraction of 1 mode
nbit=0;

% total iterations counter
NbIt=0;
end
%---------------------------------------------------------------------------------------------------
%%
function [lvar,leastvar,lstd,leaststd,BESTYFit,ORGY,id]=findleastvarl(s,t)

%t阶滞后变量SVM 求YFIT 并找出最好的那个YFit
%%size(StockCodeDouble,1)
% 	StockCode_G = StockCodeDouble(k,1);
% 	StockCode = num2str(StockCode_G);
% 	EndDate = '20160101';
% 	BeginDate = '20150101';
% 	[StockDataDouble,adjfactor] = GetStockTSDay_Web(StockCode,BeginDate,EndDate);
% 	FolderStr = ['./DataBase/svmtest/stock'];
% 	YNAME=[FolderStr,'/','Y',StockCode,'.mat'];
% 	YFitName=[FolderStr,'/','YFit',StockCode,'.mat'];
% 	ErName=[FolderStr,'/','ERRORABS',StockCode,'.mat'];
% 	LName=[FolderStr,'/','ErrorPecentage',StockCode,'.mat'];
% 	LAVERAGERNAME=[FolderStr,'/','ErrorAVERAGER',StockCode,'.mat'];
% 	LVARNAME=[FolderStr,'/','ErrorVAR',StockCode,'.mat'];
% 	LSTDNAME=[FolderStr,'/','ErrorSTD',StockCode,'.mat'];

% totalvar=ones(ll,t);

% if ((~isempty(StockData)) && (size(StockData,1)>t))%%%stockData单列数据


le=length(s);%%求出长度

%%% Data Structured
   lengthtemp=size(s,1);
    lengthtemp=lengthtemp-t;
    X=ones(lengthtemp,t);  %%Final Matrix
    er=ones(lengthtemp,t);
    l=ones(lengthtemp,t);
    YFit=ones(lengthtemp,t);
    Y=ones(lengthtemp,t);
    laverage=ones(lengthtemp,t);
    lvar=ones(lengthtemp,t);
    lstd=ones(lengthtemp,t);
    

for i=1:t  %the no i
 
    for j=1:i
        X(:,j)=s(j:le-t+j-1,1);
    end
    Y=s(t+1:le,1);
    mdl = fitrsvm(X(:,1:i),Y,'Standardize',true,'KernelFunction','rbf');
    YFit(:,i) = predict(mdl,X(:,1:i));
    er(:,i) = Y-YFit(:,i);
    l(:,i) =er(:,i)./Y;
    laverage(1,i)=mean(l(:,i));
    laverage=laverage(1,:);
    lvar(1,i)=var(l(:,i));
    lvar=lvar(1,:);
    lstd(1,i)=std(l(:,i));
    lstd=lstd(1,:);
    
    
end
%%%save
% 		save(YNAME,'Y', '-v7.3');
% 		save(YFitName,'YFit', '-v7.3');
% 		save(ErName,'er', '-v7.3');
% 		save(LName,'l', '-v7.3');
% 		save(LAVERAGERNAME,'laverage', '-v7.3');
% 		save(LVARNAME,'lvar', '-v7.3');
% 		save(LSTDNAME,'lstd', '-v7.3');
%%%plot
%     h=figure;
%     plottitle=['Results by SVM 滤波效果'];
%     subplot(611);
%     plot(Y);
%     title(plottitle)
%     subplot(612);
%     plot(YFit);
%     subplot(613);
%     plot(YFit(:,7));
%     hold on
%     plot(YFit(:,15));
%     hold on
%     plot(YFit(:,30));
%     hold on
%     plot(YFit(:,50));
%     subplot(614);
%     plot(l)
%     subplot(615);
%     plot(l(:,7));
%     hold on
%     plot(l(:,15));
%     hold on
%     plot(l(:,30));
%     hold on
%     plot(l(:,50));
%     subplot(616);
%     plot(lvar)
%     hold on
%     plot(laverage)
%     % 		set(h,'visible','off');
%     % 		saveas(h,[FolderStr,'/PIC/',StockCode,'.jpg']);
[leastvar,~]=min(lvar);
[leaststd,id]=min(lstd);
BESTYFit=YFit(:,id);
ORGY=Y;
%
%     h2=figure;
%     subplot(211);
%     bar(lvar)
%     subplot(212);
%     bar(lstd)
%

%     h3=figure;
%     plot(BESTYFit)
%     plot(s)
%     title('Best DIMENSION')

end


