classdef QMMes< handle
    properties
        MES
        ID=1;
    end
    events
        QAMessage
    end
    methods
        function QM=QMMes()
            addlistener(QM,'QAMessage',@QAMESSAGE);
           
            
        end
    end
    methods
        function QM=QMMesInit(QM)
         
            QM.ID=1;
            QM.MES.History=[];
        end
        function QM=QAMESSAGE(QM,varargin)
%             if exist('MessageID')==0
%                 disp('!!!!');
%                 MessageID=1;
%             end
            QM.MES.History{QM.ID,1}=datestr(now);
            QM.MES.History{QM.ID,2}=QM.MES.Str;
            QM.ID=QM.ID+1;
             disp('[SYSTEM MESSAGE]:Message Record !')
        end
    end
end