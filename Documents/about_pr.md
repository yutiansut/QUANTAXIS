# 关于给QUANTAXIS 提交PR


当你使用QUNATAXIS的时候,遇到的各种问题和自定义需求,除了可以通过[GITHUB ISSUE](https://github.com/QUANTAXIS/QUANTAXIS/issues)和QQ 群来提问和发布需求,你也可以自己动手,修改QUNATAXIS代码,通过向QUANTAXIS组织提交PR,让你的代码帮助到更多的人~

## 如何提交PR

1. 注册一个GITHUB账号, 通过邮箱验证
2. FORK QUANTAXIS/QUANTAXIS项目到自己的账户中
3. git clone 你的账户/quantaxis 到本地进行修改
4. 输入命令提交代码
```git
#该操作在本地命令行中完成
git config --global user.name 你的github账户名
git config --global user.password 你的github密码
git config --global user.email 你的邮箱

git add .
git commit -m '代码提交内容'
git push origin master
```
5. 在QUANTAXIS/QUANTAXIS页面上点击 pull request
6. 提交代码
7. 等待审核通过

![](http://pic.yutiansut.com/PR1.png)
![](http://pic.yutiansut.com/PR2.png)
![](http://pic.yutiansut.com/PR3.png)