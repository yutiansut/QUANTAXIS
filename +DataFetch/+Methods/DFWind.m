classdef DFWind < handle
    
    properties
        w
    end
    events
    end
    methods
        function DW=DFWind()
            DW.w=windmatlab;
        end
    end
    methods
        function DW=DFWindHistory(DW,varargin)
            [QA.FET.Data,QA.FET.Codes,QA.FET.Fields,QA.FET.Times,QA.FET.Error,QA.FET.Reqid]=QA.w.wsd(QA.FET.StockId,...
                                'pre_close,open,high,low,close,volume,amt,chg,pct_chg,swing,vwap,turn,rel_ipo_chg,rel_ipo_pct_chg',...
                                '2000-01-01',datestr(today,'yyyy-mm-dd'),'Fill=Previous','Currency=CNY','PriceAdj=F');
                           
        end
    end
end