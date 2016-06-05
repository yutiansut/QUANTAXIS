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
            fprintf('[QACP]:===Initial the QUANTAXIS Class Package!===\n');
        end
    end
end