# QUANTAXIS的小白级别教程

此篇安装纯粹写给刚学习编程/对python不熟悉/金融系的童靴们, 如果已经有一定的基础,知道怎么倒腾系统,路径,命令行,git等操作,可以直接去[install](install.md)

作者本来也是金融系出身,代码这些属于自己摸索,清楚一路上的艰难,所以我们一切从最简单的说起:


1. quantaxis 是一个开源的python库, 你可以调用和引入(import), 可以自己修改里面的源代码并提交给[官方组织](htttps://github.com/quantaxis)来贡献自己的力量和想法
2. quantaxis依赖Python3环境,所以你需要先安装一个python环境
3. quantaxis在本地存储了日线/分钟线/财务等等数据, 因此你需要准备一个数据库
4. quantaxis解决的是一个基础的框架性问题, 可以帮你自动更新/清洗数据, 给你回测/分析提供支持, 但是quantaxis不是一个可以直接运行了就赚钱的东西... 因此你还是需要自己实现你的想法
5. quantaxis的使用和调试主要通过python的 ```jupyter notebook``` 你可以直接使用jupyter来调试你的代码
6. quantaxis 100% 纯开源,并不收费, 你可以放心使用.

在以上的一些基本概念了解以后, 我们进入正题:

## 了解windows命令行:

按住 win+R键, 调出```运行```窗口

输入powershell

或者cmd

即可进入命令行, 命令行是windows中运行程序/配置服务中必备的工具

![](http://pic.yutiansut.com/powershell.png)

## 安装python

我们推荐使用anaconda来安装python, anaconda是一个集成的python环境

(由于anaconda较大而官网的速度较慢,推荐去清华的anaconda镜像站下载)

[清华镜像ANACONDA链接](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)


anaconda安装的时候 注意:

敲黑板! 一定都要选上, 不然需要自己手动配置path, 如果不是很了解path的童靴一定要都选上

![](http://pic.yutiansut.com/anaconda_install_win.png)

在安装ANACONDA的过程中,注意勾选```add to path```选项,将python的执行路径加入系统路径中

在安装完成后,可以使用```python -V```来验证是否成功

```bash
λ  python -V
Python 3.6.3 :: Anaconda, Inc.
```

## 安装quantaxis

打开命令行输入

```
pip install quantaxis -i https://pypi.doubanio.com/simple
```

在这个过程中, 你会遇到各种报错:

- 如果出现```ModuleNotFoundError``` 一般是这个模块还没有安装起来,
- 如果出现```VC14 required ``` 等字样,说明此包需要编译

遇到这种情况, 直接访问 [python winodws wheel](https://www.lfd.uci.edu/~gohlke/pythonlibs/)

在页面上按住 ```ctrl+f```键, 调出搜索框 ,搜索你需要的包 :

![](http://pic.yutiansut.com/QQ%E6%88%AA%E5%9B%BE20180708143617.png)

然后点击进入

![](http://pic.yutiansut.com/winwheel.png)

下载whl文件到本地, 使用命令行进入本地目录:

使用 pip install 安装这个文件

```
pip install 你下载的文件.whl
```

![](http://pic.yutiansut.com/pipwhl.png)


然后再继续 


```
pip install quantaxis -i https://pypi.doubanio.com/simple
```

直至成功


## 安装数据库




