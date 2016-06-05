classdef DINodeJS <handle & Message.QMMes
    properties
        ING
    end
    methods
        function DN=DINodeJS()
        end
        function DN=DINodeJSStart(DN)
            [status, results]=system('node DataCenter/bin/www.js','-echo')
        end
    end
end