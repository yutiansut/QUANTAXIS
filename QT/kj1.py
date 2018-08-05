from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow_Login(object):
    def setupUi(self, MainWindow_Login):
        pass
    def retranslateUi(self, MainWindow_Login):
        pass




class Ui_Dialog(QtWidgets.QWidget,Ui_Dialog):
    def __init__(self):
        super(Ui_Dialog,self).__init__()
        self.setupUi(self)
    #定义登出按钮的功能
    def logoutEvent(self):
        self.hide()           #隐藏此窗口
        self.log = loginWindow() 
        self.log.show()       #显示登录窗口
                              #必须加上self

class loginWindow(QtWidgets.QMainWindow,Ui_MainWindow_Login):
    def __init__(self):
        super(loginWindow,self).__init__()
        self.setupUi(self)
    #定义登录按钮的功能
    def loginEvent(self):
        self.hide()
        self.dia = Ui_Dialog()
        self.dia.show()
        #self.dia.exec_()
        #pyqt5下show()方法有所改变，不再使用exec_()方法。

#运行窗口Login
if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    login_show=loginWindow()
    login_show.show()
    sys.exit(app.exec_())