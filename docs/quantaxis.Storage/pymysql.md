前言
pymsql是Python中操作MySQL的模块，其使用方法和MySQLdb几乎相同。但目前pymysql支持python3.x而后者不支持3.x版本。
本文测试python版本：2.7.11。mysql版本：5.6.24
一、安装
?
1
pip3 install pymysql
二、使用操作
1、执行SQL

#!/usr/bin/env pytho
# -*- coding:utf-8 -*-
import pymysql
  
# 创建连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1', charset='utf8')
# 创建游标
cursor = conn.cursor()
  
# 执行SQL，并返回收影响行数
effect_row = cursor.execute("select * from tb7")
  
# 执行SQL，并返回受影响行数
#effect_row = cursor.execute("update tb7 set pass = '123' where nid = %s", (11,))
  
# 执行SQL，并返回受影响行数,执行多次
#effect_row = cursor.executemany("insert into tb7(user,pass,licnese)values(%s,%s,%s)", [("u1","u1pass","11111"),("u2","u2pass","22222")])
  
  
# 提交，不然无法保存新建或者修改的数据
conn.commit()
  
# 关闭游标
cursor.close()
# 关闭连接
conn.close()
注意：存在中文的时候，连接需要添加charset='utf8'，否则中文显示乱码。
2、获取查询数据

#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1')
cursor = conn.cursor()
cursor.execute("select * from tb7")
 
# 获取剩余结果的第一行数据
row_1 = cursor.fetchone()
print row_1
# 获取剩余结果前n行数据
# row_2 = cursor.fetchmany(3)
 
# 获取剩余结果所有数据
# row_3 = cursor.fetchall()
 
conn.commit()
cursor.close()
conn.close()
3、获取新创建数据自增ID
可以获取到最新自增的ID，也就是最后插入的一条数据ID

#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1')
cursor = conn.cursor()
effect_row = cursor.executemany("insert into tb7(user,pass,licnese)values(%s,%s,%s)", [("u3","u3pass","11113"),("u4","u4pass","22224")])
conn.commit()
cursor.close()
conn.close()
#获取自增id
new_id = cursor.lastrowid      
print new_id
4、移动游标
操作都是靠游标，那对游标的控制也是必须的

注：在fetch数据时按照顺序进行，可以使用cursor.scroll(num,mode)来移动游标位置，如：
 
cursor.scroll(1,mode='relative') # 相对当前位置移动
cursor.scroll(2,mode='absolute') # 相对绝对位置移动
 
5、fetch数据类型
关于默认获取的数据是元祖类型，如果想要或者字典类型的数据，即：

#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1')
#游标设置为字典类型
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute("select * from tb7")
 
row_1 = cursor.fetchone()
print row_1　　#{u'licnese': 213, u'user': '123', u'nid': 10, u'pass': '213'}
 
conn.commit()
cursor.close()
conn.close()
6、调用存储过程
a、调用无参存储过程

#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
 
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1')
#游标设置为字典类型
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
#无参数存储过程
cursor.callproc('p2')  #等价于cursor.execute("call p2()")
 
row_1 = cursor.fetchone()
print row_1
 
 
conn.commit()
cursor.close()
conn.close()
b、调用有参存储过程

#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
 
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
 
cursor.callproc('p1', args=(1, 22, 3, 4))
#获取执行完存储的参数,参数@开头
cursor.execute("select @p1,@_p1_1,@_p1_2,@_p1_3")  #{u'@_p1_1': 22, u'@p1': None, u'@_p1_2': 103, u'@_p1_3': 24}
row_1 = cursor.fetchone()
print row_1
 
 
conn.commit()
cursor.close()
conn.close()
三、关于pymysql防注入
 1、字符串拼接查询，造成注入
正常查询语句：

#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1')
cursor = conn.cursor()
user="u1"
passwd="u1pass"
#正常构造语句的情况
sql="select user,pass from tb7 where user='%s' and pass='%s'" % (user,passwd)
#sql=select user,pass from tb7 where user='u1' and pass='u1pass'
row_count=cursor.execute(sql) row_1 = cursor.fetchone()
print row_count,row_1
 
conn.commit()
cursor.close()
conn.close()
构造注入语句：

#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1')
cursor = conn.cursor()
 
user="u1' or '1'-- "
passwd="u1pass"
sql="select user,pass from tb7 where user='%s' and pass='%s'" % (user,passwd)
 
#拼接语句被构造成下面这样，永真条件，此时就注入成功了。因此要避免这种情况需使用pymysql提供的参数化查询。
#select user,pass from tb7 where user='u1' or '1'-- ' and pass='u1pass'
 
row_count=cursor.execute(sql)
row_1 = cursor.fetchone()
print row_count,row_1
 
 
conn.commit()
cursor.close()
conn.close()
 
 2、避免注入，使用pymysql提供的参数化语句
正常参数化查询

#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
 
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1')
cursor = conn.cursor()
user="u1"
passwd="u1pass"
#执行参数化查询
row_count=cursor.execute("select user,pass from tb7 where user=%s and pass=%s",(user,passwd))
row_1 = cursor.fetchone()
print row_count,row_1
 
conn.commit()
cursor.close()
conn.close()
构造注入，参数化查询注入失败。

#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1')
cursor = conn.cursor()
 
user="u1' or '1'-- "
passwd="u1pass"
#执行参数化查询
row_count=cursor.execute("select user,pass from tb7 where user=%s and pass=%s",(user,passwd))
#内部执行参数化生成的SQL语句，对特殊字符进行了加\转义，避免注入语句生成。
# sql=cursor.mogrify("select user,pass from tb7 where user=%s and pass=%s",(user,passwd))
# print sql
#select user,pass from tb7 where user='u1\' or \'1\'-- ' and pass='u1pass'被转义的语句。
 
row_1 = cursor.fetchone()
print row_count,row_1
 
conn.commit()
cursor.close()
conn.close()
结论：excute执行SQL语句的时候，必须使用参数化的方式，否则必然产生SQL注入漏洞。
3、使用存mysql储过程动态执行SQL防注入
使用MYSQL存储过程自动提供防注入，动态传入SQL到存储过程执行语句。

delimiter \\
DROP PROCEDURE IF EXISTS proc_sql \\
CREATE PROCEDURE proc_sql (
  in nid1 INT,
  in nid2 INT,
  in callsql VARCHAR(255)
  )
BEGIN
  set @nid1 = nid1;
  set @nid2 = nid2;
  set @callsql = callsql;
    PREPARE myprod FROM @callsql;
--   PREPARE prod FROM 'select * from tb2 where nid>? and nid<?';  传入的值为字符串，？为占位符
--   用@p1，和@p2填充占位符
    EXECUTE myprod USING @nid1,@nid2;
  DEALLOCATE prepare myprod;
 
END\\
delimiter ;

set @nid1=12;
set @nid2=15;
set @callsql = 'select * from tb7 where nid>? and nid<?';
CALL proc_sql(@nid1,@nid2,@callsql)
pymsql中调用

#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1')
cursor = conn.cursor()
mysql="select * from tb7 where nid>? and nid<?"
cursor.callproc('proc_sql', args=(11, 15, mysql))
 
rows = cursor.fetchall()
print rows #((12, 'u1', 'u1pass', 11111), (13, 'u2', 'u2pass', 22222), (14, 'u3', 'u3pass', 11113))
conn.commit()
cursor.close()
conn.close()
四、使用with简化连接过程
每次都连接关闭很麻烦，使用上下文管理，简化连接过程

#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
 
import pymysql
import contextlib
#定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='127.0.0.1', port=3306, user='root', passwd='', db='tkq1',charset='utf8'):
  conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
  cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
  try:
    yield cursor
  finally:
    conn.commit()
    cursor.close()
    conn.close()
 
# 执行sql
with mysql() as cursor:
  print(cursor)
  row_count = cursor.execute("select * from tb7")
  row_1 = cursor.fetchone()
  print row_count, row_1
总结
以上就是关于Python中pymysql模块的全部内容，希望对大家学习或使用python能有一定的帮助，如果有疑问大家可以留言交流。