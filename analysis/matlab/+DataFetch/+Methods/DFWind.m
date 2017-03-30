classdef DFWind < DataFetch.Methods.Core.DFCore & Message.QMMes
    % by yutiansut
    % 2016/6/5
    
    properties
        w
    end
    events
        DFwindhistory

    end
    methods
        function DW=DFWind()
            DW.w=windmatlab;
            DW.DFWindInit();
            
        end
        function DW=DFWindInit(DW)
            DW.MES.Str='[DFWind]:Initializating DFWind!\n';
            fprintf(DW.MES.Str);
            notify(DW,'QAMessage')
            addlistener(DW,'DFwindhistory',@DFWindHistory);

        end
    end
    methods
        function DW=DFWindHistory(DW,varargin)
            fprintf('[DFWind]:Using DFWindHistory, the API will be \n');
            if isempty(DW.FET.StockId)
                DW.FET.StockId=input('Please input the Stock ID, example 600000.SH\nThe StockId:','s');
            end
            
            [DW.FET.Data,DW.FET.Codes,DW.FET.Fields,DW.FET.Times,DW.FET.Error,DW.FET.Reqid]=DW.w.wsd(DW.FET.StockId,...
                'pre_close,open,high,low,close,volume,amt,chg,pct_chg,swing,vwap,turn,rel_ipo_chg,rel_ipo_pct_chg',...
                DW.FET.StartDate,DW.FET.EndDate,'Fill=Previous','Currency=CNY','PriceAdj=F');
            
        end
    end
    methods
        % help
        function DW=DFWindHELP(DW)
            fprintf('[DFWINDHELP]:This is HELP Documents \n ')
            DW.FET.HELPOption=input('SELECT the one you interested:\n 1.WindHistory\n==:','s');
            switch DW.FET.HELPOption
                case {'1'}
                    fprintf('API ==WindHistory\n');
            end
        end
    end
end