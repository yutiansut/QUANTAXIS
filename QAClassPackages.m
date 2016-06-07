classdef QAClassPackages < DataFetch.DFMain & DataIntegration.DINodeJS & ...
        DataStorage.DSMysql
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

        end
    end
end