classdef TESTQUANTAXIS< QAClassPackages
    properties
        
    end
    methods
        function TQ=TESTQUANTAXIS()
            
            TQ.MES.Str='[TestQUANTAXIS]:This is testing model, you can test different modules by changing class!\n';
           % notify(TQ,'QAMessage');
            fprintf(TQ.MES.Str);
        end
    end
end
