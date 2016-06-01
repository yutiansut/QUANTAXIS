classdef Trading < handle
    properties
        %% account system ��ʽ ACC_
        ACC_TotalAssest=1000000;
        ACC_Cash;
        ACC_Position
        ACC_Portfolio%�ֲ�����
        %% System ϵͳ���� ��quantaxis���ݻ�ȡ�� ��ʽ SYS_
        SYS_Date
        SYS_Price  %������  ���� ���� ���� ����
        SYS_Volum
        
        %% trade system  ��ʽ TRA_
        TRA_Time
        TRA_StockID
        TRA_Towards
        TRA_Price %
        TRA_Vol
        TRA_Tax
        %% message system  ��ʽ MES_
        MES_Time
        MES_Type
        MES_Text

        %% evaluation system ��ʽ EVA_
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
            disp('===Welcome to QUANTAXIS-Trading BOX by yutiansut ===')
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
            %% �˻�����ϵͳ
            
            
            
            
            
            
            
            
            
            
            
            
            
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
