# QUANTAXIS DATABASE 说明

<!-- vscode-markdown-toc -->
* 1. [适用的database](#database)
* 2. [database的安全说明:](#database:)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

##  1. <a name='database'></a>适用的database

- [x] MongoDB
- [ ] MYSQL
- [ ] MSSQL
- [ ] INFLUXDB
- [ ] SQLITE3
- [ ] LEVELDB

##  2. <a name='database:'></a>database的安全说明:

推荐对于database的端口号/验证等进行安全性部署,在部署到生产环境中时,考虑不要开放数据库端口号

- 数据库的admin验证
- 数据库端口号更改
- 服务器关闭数据库的端口,采用中间件访问

