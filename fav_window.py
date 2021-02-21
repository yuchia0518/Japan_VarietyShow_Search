# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fav_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

dbfile = "J_VarietyShow.db"

class Ui_FavWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 449)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 50, 481, 192))
        self.listWidget.setObjectName("listWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(50, 250, 271, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 20, 211, 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(330, 250, 82, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add_listItem)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 290, 491, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 310, 481, 91))
        self.groupBox.setObjectName("groupBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.listWidget.itemClicked.connect(self.itemClicked)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.vbox = QtWidgets.QHBoxLayout(MainWindow)
        # self.vbox.setGeometry(QtCore.QRect(0, 0, 500, 500))
        self.groupBox.setLayout(self.vbox)
        # self.groupBox.setAlignment(QtCore.Qt.Horizontal)
        # self.vbox.setAlignment(QtCore.Qt.AlignCenter)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "我的收藏關鍵字"))
        self.pushButton.setText(_translate("MainWindow", "新增收藏"))
        self.groupBox.setTitle(_translate("MainWindow", "此次搜尋關鍵字 "))

        conn = sqlite3.connect(dbfile)
        rows = conn.execute("select keyword from Fav;")
        for row in rows:
            for field in row:
                self.listWidget.addItem(field)
                print("{}\t".format(field), end="")
            print()
        conn.close()

    def add_listItem(self):

        conn = sqlite3.connect(dbfile)
        sql_str = "insert into Fav(keyword) values('{}');".format('test')
        conn.execute(sql_str)
        conn.commit()
        conn.close()

        addinput = self.lineEdit.text()

        if addinput != '':
            self.listWidget.addItem(addinput)
            self.lineEdit.clear()

    def itemClicked(self, item):
        self.label_item = QtWidgets.QLabel()
        self.label_item.setText(item.text())
        # self.label_item.setAlignment(QtCore.Qt.AlignLeft)
        self.vbox.addWidget(self.label_item)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_FavWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
