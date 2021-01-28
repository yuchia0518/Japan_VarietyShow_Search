# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myui_v5.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import re
from bs4 import BeautifulSoup
import requests
from PyQt5.QtCore import Qt, QSize


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(770, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 20, 781, 281))
        self.groupBox.setObjectName("groupBox")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.groupBox)
        self.calendarWidget.setGeometry(QtCore.QRect(10, 50, 351, 181))
        self.calendarWidget.setObjectName("calendarWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(400, 170, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(310, 240, 131, 32))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(60, 30, 241, 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(500, 140, 101, 16))
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(15, 350, 740, 200))  # left, top, width, height
        # self.scrollArea.setMinimumSize(QtCore.QSize(0, 1000))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(15, 350, 300, 200))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 770, 24))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.Vbox = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "輸入任何關鍵字"))
        self.pushButton.setText(_translate("MainWindow", "搜尋"))
        self.label.setText(_translate("MainWindow", "日期搜尋（預設為自選日期至今日）"))
        self.label_2.setText(_translate("MainWindow", "關鍵字搜尋"))
        self.menu.setTitle(_translate("MainWindow", "綜藝節目搜尋程式"))


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.listview)

    def get_chosenDate_soup(self, date_num, keyword):

        page = 1
        title_list = []
        link_list = []

        while True:
            base_url = 'https://jshow.tv/more-post/page/' + str(page)
            print(page)
            response = requests.get(base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            div_titles = soup.find_all('div', class_='des')
            video_date_num = int()
            date_pattern = re.compile(r'\d\d\d\d\d\d')
            try:
                for div_title in div_titles:
                    video_date_num = date_pattern.search(div_title.getText()).group(0)
                    if keyword in div_title.getText():
                        print('keyword_pass')
                        for div_child in div_title.children:
                            print('div_child: ' + div_child.getText())
                            if date_pattern.search(div_child.getText()[-6:]) is not None:
                                print('date pattern pass!')
                                title_list.append(div_title.getText())
                                link_list.append(div_title.find_previous_sibling('div').findChild('a')['href'])
                                print(div_title.getText())
                                print(div_title.find_previous_sibling('div').findChild('a')['href'])
                                print(video_date_num)
                                break
                            else:
                                print('date pattern not pass!!')



            except Exception as e:
                print(e)

            print(video_date_num)
            print(date_num)
            if int(video_date_num) >= int(date_num):
                page += 1
                print('page: ' + str(page))
            else:
                break

        return title_list, link_list

    def listview(self):
        self.clearLayout(self.Vbox)
        datenum = self.calendarWidget.selectedDate().toString("yyMMdd")
        keyword = self.lineEdit.text()
        title_list, link_list = self.get_chosenDate_soup(int(datenum), keyword)
        # linkTemplate = '<a href={0}>{1}</a>'
        try:
            for title, link in zip(title_list, link_list):

                video_title = str(title).split('内容：')[0][0:-6]
                video_cast = '出演： ' + str(title).split('出演：')[1]
                video_content = '內容： ' + str(title).split('出演：')[0].split('内容：')[1]
                video_date = str(title).split('内容：')[0][-6:]
                # print(video_date)
                # print(video_title)
                # print(video_cast)
                # print(video_content)

                date_label = QLabel(video_date)
                title_label = QLabel('<a href = ' + link + '>' + video_title + '</a>')
                cast_label = QLabel(video_cast)
                content_label = QLabel(video_content)
                # link_label = QLabel("<a href='http://stackoverflow.com'>stackoverflow</a>")
                title_label.setOpenExternalLinks(True)

                video_widgets = [title_label, cast_label, content_label]
                for video_widget in video_widgets:
                    self.Vbox.addWidget(video_widget)
        except:
            print('somethings wrong')

            # self.Vbox.addWidget(tit)
            # self.Vbox.addWidget(link_label)
            # self.Vbox.addWidget(link_label)

            # self.setLayout(self.scrollArea)
            # print(title)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
