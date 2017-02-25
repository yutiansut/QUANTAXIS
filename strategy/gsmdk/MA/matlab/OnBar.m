function [  ] = OnBar( bar )
global bar_5;
global bar_20;
global MA5;
global MA20;

Max_position = 100000;
Min_position = 100;
judge = 0;

if length(bar_5) < 4
    bar_5(end+1) = table2array(bar(1,'close'));
    MA5(end+1) = 0;
    judge = 1;
elseif length(bar_5) == 4
    bar_5(end+1) = table2array(bar(1,'close'));
    MA5(end+1) = sum(bar_5) / 5;
else
    bar_5(end+1) = table2array(bar(1,'close'));
    bar_5(1) = [];
    MA5(end+1) = sum(bar_5) / 5;
    %disp(MA5(end));
end

if length(bar_20) < 19
    bar_20(end+1) = table2array(bar(1,'close'));
    MA20(end+1) = 0;
    judge = 1;
elseif length(bar_20) == 19
    bar_20(end+1) = table2array(bar(1,'close'));
    MA20(end+1) = sum(bar_20) / 20;
else
    bar_20(end+1) = table2array(bar(1,'close'));
    bar_20(1) = [];
    MA20(end+1) = sum(bar_20) / 20;
    %disp(MA20(end));
end

if judge
    return;
end

%MA5上穿MA20买入
position = gm.GetPosition('SZSE','000001',OrderSide.Bid);
if MA5(end-1) <= MA20(end-1) && MA5(end) > MA20(end)
    if ~isempty(position) && table2array(position(1,'volume')) < Max_position
        gm.OpenLong('SZSE','000001',0,100);
        x = sprintf('MA5由 %d 变为 %d，MA20由 %d 变为 %d，MA5上穿MA20，市价买入100股',MA5(end-1),MA5(end),MA20(end-1),MA20(end));
        disp(x);  
    elseif isempty(position)
        gm.OpenLong('SZSE','000001',0,100);
        x = sprintf('MA5由 %d 变为 %d，MA20由 %d 变为 %d，MA5上穿MA20，市价买入100股',MA5(end-1),MA5(end),MA20(end-1),MA20(end));
        disp(x);
    elseif table2array(position(1,'volume')) >= Max_position
        gm.OpenLong('SZSE','000001',0,100);
        x = sprintf('MA5由 %d 变为 %d，MA20由 %d 变为 %d，MA5上穿MA20，但超过最大仓位，无法买入',MA5(end-1),MA5(end),MA20(end-1),MA20(end));
        disp(x);
    end
end
    
%MA5下穿MA20卖出
position = gm.GetPosition('SZSE','000001',OrderSide.Bid);
if MA5(end-1) >= MA20(end-1) && MA5(end) < MA20(end)
    if isempty(position)
        x = sprintf('MA5由 %d 变为 %d，MA20由 %d 变为 %d，MA5下穿MA20，但仓位为0无法卖出',MA5(end-1),MA5(end),MA20(end-1),MA20(end));
        disp(x);
    elseif table2array(position(1,'volume')) >= Min_position
        gm.CloseLong('SZSE','000001',0,100);
        x = sprintf('MA5由 %d 变为 %d，MA20由 %d 变为 %d，MA5下穿MA20，市价卖出100股',MA5(end-1),MA5(end),MA20(end-1),MA20(end));
        disp(x);
    elseif table2array(position(1,'volume')) < Min_position
        x = sprintf('MA5由 %d 变为 %d，MA20由 %d 变为 %d，MA5下穿MA20，但仓位低于最低仓位无法卖出',MA5(end-1),MA5(end),MA20(end-1),MA20(end));
        disp(x);
    end
end

end