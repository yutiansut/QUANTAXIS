# QUANTAXIS DataStorage

## QUANTAXIS DataStorage.QAMysql();

From the version 3.2.0, we introduce a new way of organize the quantaxis. In the former version,
we usually using different functions of same class to archieve this, however, this will definitely shortern the life cycle of code.
So, we try to make part of these function, and give everyone a class while using the subordinate way to connect them.

### How to use the DataStorage.QAMysql part?
```
 QM=DataStorage.Mysql();  %
```
this is the simplest way to using this, however, if you want to call it, you can use something like this:
```
 classdef QUANTAXIS<DataStorage.QAMysql
 end
```
then you can use the following code to using this:
```
QA=QUANTAXIS();
QA.QAMysqlConfig;
QA.QAMysqlConnection;
```
