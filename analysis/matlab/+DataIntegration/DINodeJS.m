classdef DINodeJS <handle & Message.QMMes
    properties
        ING
    end
    methods
        function DN=DINodeJS()
        end
        function DN=DINodeJsStart(DN)
            
            [status, DN.MES.Str]=system('node DataCenter/bin/www.js','-echo');
            notify(DN,'QAMessage');
                
        end
    end
end