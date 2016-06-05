classdef DFCore < Message.QMMes & handle
    % this function only be used to set the properties
    % by yutiansut
    % 2016/6/5
    properties
        FET
    end
    methods
        function DFC=DFCore()
            fprintf('[DFCore]:Using DFCore, this function has properities of FET \n')
            DFC.FET.StockId=[];
            DFC.FET.StartDate='2000-01-01';
            DFC.FET.EndDate=datestr(today,'yyyy-mm-dd');
        end
    end
    
end