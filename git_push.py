# coding:utf-8
import os

#
os.popen("git add .")
os.popen('git commit -m "push by python code" ')
os.popen('git push origin')


os.popen('git subtree push --prefix=QUANTAXIS_Trade \
     https://github.com/yutiansut/QUANTAXIS_Trade  master --squash')
os.popen('git subtree push --prefix=QUANTAXIS_DataTools \
     https://github.com/yutiansut/QUANTAXISDataTool  \
     master --squash')
os.popen('git subtree push --prefix=QUANTAXIS_Webkit \
    https://github.com/yutiansut/QUANTAXIS_Webkit  \
    master --squash')
