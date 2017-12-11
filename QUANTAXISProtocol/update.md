# QUANTAXIS更新
<!-- TOC -->

- [QUANTAXIS更新](#quantaxis更新)
    - [更新QUANTAXIS (python)](#更新quantaxis-python)
    - [更新QUANTAXIS_Webkit (nodejs)](#更新quantaxis_webkit-nodejs)

<!-- /TOC -->
由于目前项目还在开发中,所以需要使用Git来更新项目:

点击右上角的Star和watch来持续跟踪项目进展~

常规更新:
```
cd QUANTAXIS
git pull
```

如果本地有进行更改,遇到更新失败:

(注意: 最好不要在本地修改该项目文件,如果需要做一些自定义功能,可以进fork[在项目的右上角])

```
git reset --hard origin/master
git pull
```


## 更新QUANTAXIS (python)

一般而言,本地开发模式 更新完代码就无需考虑pip install 重新安装的问题, 但如果涉及 setup.py的更新 则需要

```
cd QUANTAXIS
pip install -e .
```



## 更新QUANTAXIS_Webkit (nodejs)

当更新了package.json文件时,项目需要重新 npm install 来安装和更新依赖项

当出现报错时

```
cd QUANTAXIS_Webkit/web
npm install 

```
一般可以解决问题