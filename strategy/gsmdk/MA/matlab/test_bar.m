clear;
% 请注意修改成您的注册掘金用户名和密码
username = 'demo@myquant.cn';
pwd = '123456';

global bar_5;
global bar_20;
global MA5;
global MA20;

% 请注意第五个参数strategy_id需要更改成您本地终端生成的ID，否则在终端上看不到策略的连接状态和下单。
ret = gm.Init(username,pwd,MDMode.MD_MODE_SIMULATED,'SZSE.000001.bar.60','110ca5d6-a8a1-11e5-a82d-bc855616490f','localhost:8001');

if ret ~= 0
    disp('初始化失败!');
    disp(ret);
    return;
end

gm.SetBarHandle(@OnBar);
gm.SetLoginHandle(@OnLogin);
gm.SetErrorHandle(@OnError);
gm.SetOrderHandle(@OnOrder);

gm.Run();