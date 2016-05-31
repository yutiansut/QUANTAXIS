classdef FreeMarkets<handle
    
    % This is a free markets stimulation for fractal markets theory
    % This ia a subcomponents for QUANTAXIS Applications
    % Author: yutiansut
    % First Publish Date: 2016/5/28
    
    properties
        User;
        Price;
        BidPool;
        TS;
        Member=500;
        Bid;
    end
    events
        transaction
        ask %
        reply %
        message %
        listen %
        price %
    end
    
    
    methods
        function FM=FreeMarkets()
            addlistener(FM,'transaction',@TSBoard);
            addlistener(FM,'ask',@ASK);
            addlistener(FM,'reply',@REPLY);
            addlistener(FM,'price',@PRICE);
            addlistener(FM,'listen',@LISTEN);
            FM.Init;
            FM.BidPool.id=1;
            FM.Price.temp=50;
            
        end
        function FM=Init(FM,varargin)
            for i=1:FM.Member
                Name=['FM.User.Strategy',num2str(i)];
                eval([Name,'=[]']);
            end
        end
    end
    methods
        function FM=Try(FM,varargin)
            FM.BidPool.id=1;
            FM.Price.temp=50;
            roundID=0;
            FM.BidPool.Trade=[];
            FM.Price.History=[];
            notify(FM,'reply');
        end
        function FM=role(FM,varargin)
            
        end
    end
    methods  % listener
        function FM=TSBoard(FM,varargin)
            fprintf('Making Transaction\n');
            FM.Price.temp=FM.Bid.Price;
            notify(FM,'reply');
            if isempty(FM.Price.History)
                FM.Price.History=FM.Price.temp;
            else
                FM.Price.History(end+1,:)=FM.Price.temp;
            end
            
        end
        function FM=ASK(FM,varargin)  %ѯ�ۺ���  ���뱨�۵�
            FM.BidPool.id=FM.BidPool.id+1;
            FM.BidPool.Board{1,1}='BidPrice';
            FM.BidPool.Board{1,2}='Amount';
            FM.BidPool.Board{1,3}='BidDate';
            FM.BidPool.Board{1,4}='Varities';
            FM.BidPool.Board{1,5}='ID';
            FM.BidPool.Board{1,6}='SysTime';
            FM.BidPool.Board{FM.BidPool.id,1}=FM.Bid.Price;
            FM.BidPool.Board{FM.BidPool.id,2}=FM.Bid.Amount;
            FM.BidPool.Board{FM.BidPool.id,3}=FM.Bid.Date;
            FM.BidPool.Board{FM.BidPool.id,4}=FM.Bid.Varities;
            FM.BidPool.Board{FM.BidPool.id,5}=FM.Bid.ID;
            FM.BidPool.Board{FM.BidPool.id,6}=datestr(now,'yyyymmdd HH:MM:SS');
            
            if (isempty(FM.BidPool.Trade)||isempty(find(FM.BidPool.Trade(:,1)==FM.Bid.Price)))
                FM.BidPool.Trade(end+1,1)=FM.Bid.Price;
                FM.BidPool.Trade(end,2)=FM.Bid.Amount;
            else if FM.BidPool.Trade(find(FM.BidPool.Trade(:,1)==FM.Bid.Price),2)+FM.Bid.Amount==0;
                %FM.BidPool.Trade(find(FM.BidPool.Trade(:,1)==FM.Bid.Price),2)=FM.BidPool.Trade(find(FM.BidPool.Trade(:,1)==FM.Bid.Price),2)+FM.Bid.Amount;
                fprintf('Deal Success\n');
                
                end
            end
            
            % if bid-price is same and amount is diverse then we can hedge them and update the market price
            
            
            
        end
        function FM=REPLY(FM,varargin)
            
            for  roundID=1:50
                for id=1:FM.Member
                    bidPrice=['FM.User.Strategy',num2str(id),'.bid',num2str(roundID),'.price'];
                    eval([bidPrice,'=FM.Price.temp+(2*ceil(rand-0.5)-1)*0.5;']);
                    eval(['FM.Bid.Price=',bidPrice,';']);
                    bidAmount=['FM.User.Strategy',num2str(id),'.bid',num2str(roundID),'.amount'];
                    eval([bidAmount,'=5000*(2*ceil(rand-0.5)-1);']);
                    eval(['FM.Bid.Amount=',bidAmount,';']);
                    FM.Bid.Date=roundID;
                    FM.Bid.ID=['S',num2str(id),'-B',num2str(roundID)];
                    FM.Bid.Varities='Test-001';
                    notify(FM,'ask');
                end
                notify(FM,'transaction')
            end
            
            %    notify(FM,'transaction');
            
        end
        function FM=PRICE(FM,varargin)
            
        end
    end
    
    
end