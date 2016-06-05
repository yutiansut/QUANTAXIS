classdef QAClassPackages < DataFetch.DFMain 
    properties
    end
    events
    end
    methods
        function QACP=QAClassPackages()
            QACP.QACPInit();
        end
        
        
        function QACP=QACPInit(QACP)
            QACP.MES.Str='[QACP]:===Initial the QUANTAXIS Class Package!===\n';
            fprintf(QACP.MES.Str);
            notify(QACP,'QAMessage');
            notify(QACP,'QAMessage');
        end
    end
end