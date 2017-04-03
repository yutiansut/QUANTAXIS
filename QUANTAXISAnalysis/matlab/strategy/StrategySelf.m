%% 用户自定义策略

%% QUANTAXIS 1.2 用户自定义策略
%% APIS
% obj.StockCodeOut  
% 格式：ID-TSDay-Mean-Volum-StockTick-XRD1-MeanXRD1-XRD2-MeanXRD2-Date 
% obj.Result 除权数据
% obj.Result_XRD1 前复权数据 基于复权因子 
% obj.Result_XRD2 前复权数据 基于经典算法 

%% 一个简单的示例策略
function obj=StrategySelf(obj,varargin)
d=501;              % Starting Date
window=500;         % Size of moving window for defining pairs
t=1.5;              % Threshold value for defining abnormal behavior
ut=5;               % Peridiocity of pairs updates
C=30;               % Trading cost per trade (in units of price (e.g. dollars))
maxPeriod=5;        % maximum periods to hold the positions
Capital=10000;
[obj.profitOut,obj.portValue,obj.myTrades]=pairstrading(obj.Result,Capital,d,window,t,ut,C,maxPeriod);
end

%% 策略A
function [n]=trades(x)

[n1,n2]=size(x);

n=zeros(n1,n2);
x=abs(x);

for j=1:n2
    for i=1:n1-1
        if x(i,j)*x(i+1,j)==0&&abs(x(i+1,j))==1
            n(i+1,j)=1;
        end
    end
end
end
function [profitOut,portValue,myTrades]=pairstrading(x,Capital,d,window,t,ut,C,maxPeriod)

%  Classical Pairs Trading Using MatLab
%
% DESCRIPTION:
%     This function performs the classical pairs trading framework over a
%     matrix of prices using MatLab. The basic idea of pairs trading is to
%     take advantage of market mean reversion behavior in order to make
%     profit out of short and long positions. More details about this type
%     of quantitative trading strategy can be found at the pdf document in
%     the zip file. This function will calculate the total payoff from
%     using a certain ammount of capital in each positions. We also include
%     transaction costs in the function.
%
%     Empirical results regarding Classical Pairs Trading can be found at:
%
%     GATEV, E., GOETZMANN, W. N., ROUWENHORST, K. G. Pairs Trading:
%     Performance of a Relative Value Arbitrage Rule. Working Paper, Yale
%     School of Management. Available at SSRN:
%     http://ssrn.com/abstract=141615, 1999.
%
%     PERLIN, M. S. Evaluation of Pairs Trading Strategy at Brazilian
%     Financial Market. Unpublished Working Paper, 2006. Available at:
%     http://ssrn.com/abstract=952242
%
%       USAGE:
% [Results_Total,Results_Long,Results_Short]=pairstrading(x,Capital,d,window,t,ut,C,maxPeriod);
%
%       INPUT:
%               x - A matrix with the prices of all tested assets in the
%               pairs trading framework. The rows represents the time and
%               the collums represents each asset.
%
%               Capital - How much money is invested in each trade (same unit
%               as the prices in x (e.g. 1,000 dollars).
%
%               d - The first trading period of the matrix. For example,
%               supose you have a matrix x with size [1500,40] (1500 prices
%               for 40 assets) and you stablish that d=200, then the
%               obervation 200 is the first trading period.
%
%               window - The size of the rolling window that will be used
%               to find the pairs. Using the last example, if d=200 and
%               window=100, then, for the trading period of 200, the
%               algorithm is going to use the observations 100:199 as a
%               training period.
%
%               t - The threshold parameter which determines what is a
%               unusual behavior.
%
%               ut - The periodicy that the function will updates the pairs of stocks. As
%               an example, if d=200, window=100 and ut=25, then the
%               function will update the pairs for each stock at
%               observations 225,250 and so on.
%
%               C - Transaction Cost, in money unit (e.g. dollar). This is
%               how much cost to set a long or a short position (e.g. 15
%               dollars).
%
%               maxPeriod - Maximum time period to hold any of the postions
%               (e.g. 5 day
%
%
%       OUTPUT:
%               profitOut - A structure containing the profits from the
%               trade
%
%               myTrades  - A structure containing the trades%
%
%   Author: Marcelo Scherer Perlin
%   Email:  marceloperlin@gmail.com
%   ICMA Centre / Reading University
[n1,n2]=size(x);

if nargin<8
    error('The function needs 8 arguments');
end

if n2==1
    error('The function accepts a matrix of prices as input, not a vector');
end

if d<=window
    error('The value of d should be lower than window, otherwise there will be missing observations for first trading day)');
end

if t<=0
    error('The value of t (threshold) should be higher than 0');
end

if ut<=0
    error('The value of ut should be higher than zero');
end

if C<0
    error('The value of C (money transaction cost) should be positive');
end

if maxPeriod<0
    error('The value of maxPerid should be an integer and positive');
end

% Calculation of first execution parameters

ut2=ut;
ut1=ut;
k1=1;

dist=zeros(n1-d+1,n2);

fprintf(1,'\nPerforming Pairs Trading. Please Hold.\n')

% Main Engine
pairsVec=cell(n1-d,1);
myTrades={};
anyPos=zeros(n1-d+1,n2);
idxTrades=1;
for k=1:n1-d
    
    % x2 is the training period for each time t. It evolves with k and
    % doesn't use the information of the observation d, which is the first
    % trading period in the simulation
    
    x2=x(d-window+k-1:d+k-2,:);
    
    x3=normdata(x2);         % Normalization of x2
    
    % Find/change the Pairs for each k periods based on the quadratic error criteria.
    
    if k==1||ut==1
        [p]=pairs(x3);
    else
        if k==ut1
            [p]=pairs(x3);
        end
    end
    
    pairsVec{k,1}=p;    % saving vectors of pairs
    
    % Trade in each day according to the logic of pairs trading
    
    for i=1:n2
        dist(k,i)=x3(window,i)-x3(window,p(i,1));
    end
    
    [idx]=find(abs(dist(k,:))>t);
    
    for i=1:length(idx)
        
        if (k==1)||(anyPos(k-1,idx(i))==0)  % if any position is already open, dont trade
            myTrades{idxTrades,1}.assetsNumber=[idx(i) p(idx(i))];
            myTrades{idxTrades,1}.obsNumber=d+k-1;
            
            if (dist(k,idx(i))>0)
                myTrades{idxTrades,1}.directionTrade=[-1  1];
            else
                myTrades{idxTrades,1}.directionTrade=[ 1 -1];
            end
            
            idxTrades=idxTrades+1;
        end
        
        anyPos(k,idx(i))=1;
        anyPos(k,p(idx(i)))=1;
        
    end
    
    % Output to screen
    
    nTrades=length(idx);
    
    fprintf(1,['\nObservation #',num2str(k),' -> Found ',num2str(nTrades), ' Diverging Pair(s).']);
    if k==ut1
        k1=k1+1;
        ut1=k1*ut2;
        fprintf(' Updating Pairs.')
    end
    
end

% Calculating profits..

fprintf(1,'\n\nCalculating Profits from trades...\n');

if isempty(myTrades)
    error('No trade found. Please input a lower value for t, or increase number of observations in sample.');
end

[profitOut,portValue,myTrades]=findProfit(x,d,[zeros(d-1,n2);dist],t,myTrades,Capital,C,maxPeriod,pairsVec);

figure(1)
plot([portValue.timeSeriesComb portValue.timeSeriesLong portValue.timeSeriesShort],'LineWidth',2);
legend('Combined', 'Just Long','Just Short','Location','nw');
xlabel('Time');
ylabel('Accumulated Profits');

% Printing results to prompt

fprintf(1,'\n\n ********* Calculations Finished *********\n');

fprintf(1,'\nLong Positions Results:\n');
fprintf(1,'\n Total Profit (minus transaction costs): %4.2f',(profitOut.totalProfitLong));
fprintf(1,'\n Number of Trades: %4i',size(myTrades,1));
fprintf(1,'\n Average Return per trade: %4.2f%%',mean(portValue.timeSeriesRetLong)*100);
fprintf(1,'\n Standard Deviation of Return per trade: %4.2f%%',std(portValue.timeSeriesRetLong)*100);

fprintf(1,'\n\nShort Positions Results:\n');
fprintf(1,'\n Total Profit (minus transaction costs): %4.2f',(profitOut.totalProfitShort));
fprintf(1,'\n Number of Trades: %4i',size(myTrades,1));
fprintf(1,'\n Average Return per trade: %4.2f%%',mean(portValue.timeSeriesRetShort)*100);
fprintf(1,'\n Standard Deviation of Return per trade: %4.2f%%',std(portValue.timeSeriesRetShort)*100);

fprintf(1,'\n\nCombined Positions Results:\n');
fprintf(1,'\n Total Profit (minus transaction costs): %4.2f',(profitOut.totalProfitComb));
fprintf(1,'\n Number of Trades: %4i',size(myTrades,1)*2);
fprintf(1,'\n Number of Periods with at least one open Positon: %4i (%4.2f%% of total trading time)',portValue.nDays.anyPos,portValue.nDays.anyPos./(n1-d)*100);
fprintf(1,'\n Number of Periods with at least one Trade: %4i (%4.2f%% of total trading time)',portValue.nDays.trades,portValue.nDays.trades./(n1-d)*100);
fprintf(1,'\n Average Number of Trades each Period: %4.2f',mean(portValue.nTrades(:,2)));
fprintf(1,'\n Average Return per trade: %4.2f%%',mean(portValue.timeSeriesRetComb)*100);
fprintf(1,'\n Standard Deviation of Return per trade: %4.2f%%',std(portValue.timeSeriesRetComb)*100);

fprintf(1,'\n');
end
function [pairs]=pairs(x)

[n2]=size(x,2);

Qdist=zeros(n2,n2);

for i=1:n2
    for j=1:i-1
        Qdist(i,j)=sum((x(:,i)-x(:,j)).^2);
        Qdist(j,i)=Qdist(i,j);
    end
    Qdist(i,i)=nan;
end

[~,n]=min(Qdist);
pairs(:,1)=n';

end
function [New_x]=normdata(x)

[n2]=size(x,2);

for i=1:n2
    ret=[0 ;(x(2:end,i)-x(1:end-1,i))./x(1:end-1,i)];
    New_x(:,i)=cumprod(1+ret);  % normalizing price series to P(t=0)=1
    
    mean_x=mean(New_x(:,i));
    std_x=std(New_x(:,i));
    
    New_x(:,i)=(New_x(:,i)-mean_x)/std_x;   % normalizing again
    
end
end
function [profitOut,portValue,myTrades]=findProfit(x,d,dist,t,myTrades,Capital,C,maxPeriod,pairsVec)

[nr,nc]=size(x);
nTrades=size(myTrades,1);
timeVec=zeros(nTrades,1);

longPos_Buy =zeros(nTrades,1);
shortPos_Buy=zeros(nTrades,1);

longPos_Sell =zeros(nTrades,1);
shortPos_Sell=zeros(nTrades,1);
anyPos=zeros(nr,nc);

%  iterate over the trades and find the bought and sold price for long and
% short positions

for i=1:nTrades
    
    longIdx=myTrades{i}.assetsNumber(myTrades{i}.directionTrade==1);
    shortIdx=myTrades{i}.assetsNumber(myTrades{i}.directionTrade==-1);
    
    timeVec(i,1)=myTrades{i}.obsNumber;
    
    longPos_Buy(i,1)=x(myTrades{i}.obsNumber,longIdx);
    shortPos_Sell(i,1)=x(myTrades{i}.obsNumber,shortIdx);
    
    myIdx=0;
    while 1 % iterate forward in time until position is closed
        
        myIdx=myIdx+1;
        
        if (abs(dist(myTrades{i}.obsNumber+myIdx,myTrades{i}.assetsNumber(1)))<t)   % if spread converges, close position
            break;
        end
        
        if ((myIdx+myTrades{i}.obsNumber)==nr)  % if trades passes number of observations, close position
            break;
        end
        
        asset1=myTrades{i}.assetsNumber(1);
        asset2=myTrades{i}.assetsNumber(2);
        myObs=myTrades{i}.obsNumber-d+1+myIdx;
        
        if (pairsVec{myObs}(asset1,1))~=asset2    % if pairs has changed from t to t+1, close position
            break
        end
        
        if myIdx>(maxPeriod-1)  % if number of holding period is higher than maxPeriod, break
            break;
        end
    end
    
    anyPos(timeVec(i,1):timeVec(i,1)+myIdx,[longIdx;shortIdx])=1;
    
    longPos_Sell(i,1)=x(myTrades{i}.obsNumber+myIdx,longIdx);
    shortPos_Buy(i,1) =x(myTrades{i}.obsNumber+myIdx,shortIdx);
    
    myTrades{i}.posHold=myIdx-1;
    
    if (myTrades{i}.directionTrade(1)==1)
        myTrades{i}.buyPrices =[longPos_Buy(i,1) shortPos_Buy(i,1)];
        myTrades{i}.sellPrice=[longPos_Sell(i,1) shortPos_Sell(i,1)];
    else
        myTrades{i}.buyPrices =[shortPos_Buy(i,1)  longPos_Buy(i,1)];
        myTrades{i}.sellPrice =[shortPos_Sell(i,1) longPos_Sell(i,1)];
    end
    
end

ProfitLong =Capital.*(longPos_Sell-longPos_Buy)./longPos_Buy-C;
ProfitShort=Capital.*(shortPos_Sell-shortPos_Buy)./shortPos_Sell-C;
ProfitComb=ProfitLong+ProfitShort;

profitOut.totalProfitLong =sum(ProfitLong);
profitOut.totalProfitShort=sum(ProfitShort);
profitOut.totalProfitComb =sum(ProfitComb);

uniqueTime=unique(timeVec);
n=size(uniqueTime,1);

portValue_Trades_Total=zeros(nr-d+1,1);
portValue_Trades_Long=zeros(nr-d+1,1);
portValue_Trades_Short=zeros(nr-d+1,1);
for i=1:n
    
    idx=uniqueTime(i);
    total=sum(ProfitComb((idx)==timeVec));
    long =sum(ProfitLong((idx)==timeVec));
    short=sum(ProfitShort((idx)==timeVec));
    
    portValue_Trades_Total(idx-d+1,1)=total;
    portValue_Trades_Long(idx-d+1,1)=long;
    portValue_Trades_Short(idx-d+1,1)=short;
    
    nTrades(i,1)=idx;
    nTrades(i,2)=(sum(timeVec==idx))*2;
    
end

% Passing output to structure

portValue.timeSeriesComb =(cumsum(portValue_Trades_Total));
portValue.timeSeriesLong =(cumsum(portValue_Trades_Long));
portValue.timeSeriesShort=(cumsum(portValue_Trades_Short));

portValue.timeSeriesRetComb =ProfitComb./Capital;   % this assumes that the short positions dont need capital for funding.
% the only capital needed is for long positions.
portValue.timeSeriesRetLong =ProfitLong./Capital;
portValue.timeSeriesRetShort=ProfitShort./Capital;

portValue.nDays.trades=size(uniqueTime,1);
portValue.nDays.anyPos=sum(sum(anyPos,2)~=0);

portValue.nTrades=nTrades;
end
