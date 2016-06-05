# 关于超类 Message.QMMES

Attention: 请谨慎使用QMMES组件<br>
消息函数通过不断的调用QAMessage事件
```
当前类(QA/TQ).MES.Str='something';
notify(当前类,'QAMessage');
```
事件会被发送给Message.QMMES系统，并被记录下来

查看消息历史
```
QA.MES.History
```