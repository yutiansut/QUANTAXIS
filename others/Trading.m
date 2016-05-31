classdef Trading < handle
    properties
        %% account system 格式 ACC_
        ACC_TotalAssest=1000000;
        ACC_Cash;
        ACC_Position
        ACC_Portfolio%持仓组合
        %% System 系统数据 从quantaxis数据获取来 格式 SYS_
        SYS_Date
        SYS_Price  %按列来  开盘 最高 最低 收盘
        SYS_Volum
        
        %% trade system  格式 TRA_
        TRA_Time
        TRA_StockID
        TRA_Towards
        TRA_Price %
        TRA_Vol
        TRA_Tax
        %% message system  格式 MES_
        MES_Time
        MES_Type
        MES_Text

        %% evaluation system 格式 EVA_
        EVA_Case
        EVA_Price
        EVA_Vol
        EVA_Win
        
    end
    events
        Account;
        Trade;
        Message;
        Value;
    end
    methods
        function tra=Trading()
            disp('===Welcome to QUANTAXIS-Trading BOX by yutiansut & chendie===')
            addlistener(tra,'Account',@ACCOUNT);
            addlistener(tra,'Trade',@TRADE);
            addlistener(tra,'Message',@MESSAGE);
            addlistener(tra,'Value',@VALUE);
        end
        
        
        function tra=Strategy(tra,varargin)
            disp('Start')
            if tra.ACC_TotalAssest==1000000
                 notify(tra,'Account');
                   disp('1111')
            end
           
          
        end
    end
    methods%(Access = private)
        
        function tra=ACCOUNT(tra,varargin)
            disp('account')
            %% 账户表达系统
            
            
            
            
            
            
            
            
            
            
            
            
            
        end
        function tra=TRADE(tra,varargin)
            disp('trade')
            
            
        end
        function tra=MESSAGE(tra,varargin)
            disp('message')
        end
        function tra=VALUE(tra,varargin)
            disp('value')
        end
        
    end
end
