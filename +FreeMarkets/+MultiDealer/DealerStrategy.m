classdef DealerStrategy < Handle
    % by yutiansut
    % behavior of market dealers
    % 2016/6/1  
    properties
        
    end
    events
    
    end
    methods
        function DS=DealerStrategy()
            
        end
    end
    
    methods(access='public')
        function DS = RandomStrategy(DS,varargin)
            DS.Price.Output=DS.Price.Input+(2*ceil(rand-0.5)-1)*0.5;
            DS.Amount.Output=5000*(2*ceil(rand-0.5)-1);
        end
        function DS = RandomNStrategy(DS,varargin)
            
            
        end
    end
end