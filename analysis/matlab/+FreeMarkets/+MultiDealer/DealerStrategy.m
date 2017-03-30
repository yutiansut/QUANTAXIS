classdef DealerStrategy < handle
    % by yutiansut
    % behavior of market dealers
    % 2016/6/1
    % 
    %     for i=1:5000
    %         TM.RandomxStrategy()
    %         TM.RandomiStrategy()
    %         price(i)=TM.PriceDS.x;
    %     end
    properties
        PriceDS
        AmountDS
    end
    events
        
    end
    methods
        function DS=DealerStrategy()
            
        end
    end
    
    methods
        function DS = RandomStrategy(DS,varargin)
            DS.PriceDS.x=DS.PriceDS.x+(2*ceil(rand-0.5)-1)*0.5;
            DS.AmountDS.Output=5000*(2*ceil(rand-0.5)-1);
        end
        function DS = RandomNStrategy(DS,varargin)
            DS.PriceDS.x=DS.PriceDS.x+(2*ceil(randn-0.5)-1)*0.5;
        end
        function DS = RandomxStrategy(DS,varargin)
            DS.PriceDS.x=DS.PriceDS.x+rand*0.5;
        end
        function DS = RandomiStrategy(DS,varargin)
            DS.PriceDS.x=DS.PriceDS.x+randi(2)*0.5;
        end
        function DS=Randomx(DS,varargin)
%                    'beta'  or 'Beta',
%        'bino'  or 'Binomial',
%        'burr'  or 'Burr',
%        'chi2'  or 'Chisquare',
%        'exp'   or 'Exponential',
%        'ev'    or 'Extreme Value',
%        'f'     or 'F',
%        'gam'   or 'Gamma',
%        'gev'   or 'Generalized Extreme Value',
%        'gp'    or 'Generalized Pareto',
%        'geo'   or 'Geometric',
%        'hn'    or 'Half Normal',
%        'hyge'  or 'Hypergeometric',
%        'logn'  or 'Lognormal',
%        'nbin'  or 'Negative Binomial',
%        'ncf'   or 'Noncentral F',
%        'nct'   or 'Noncentral t',
%        'ncx2'  or 'Noncentral Chi-square',
%        'norm'  or 'Normal',
%        'poiss' or 'Poisson',
%        'rayl'  or 'Rayleigh',
%        'stable'or 'Stable',
%        't'     or 'T',
%        'unif'  or 'Uniform',
%        'unid'  or 'Discrete Uniform',
%        'wbl'   or 'Weibull'.
            DS.PriceDS.x=DS.PriceDS.x+(2*ceil(bino-0.5)-1)*0.5;
        end
    end
end 