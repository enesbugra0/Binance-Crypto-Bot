# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panel.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_giris(object):
    def setupUi(self, giris):
        giris.setObjectName("giris")
        giris.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(giris)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 73, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(21, 64, 32, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(101, 31, 137, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(101, 60, 137, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 40, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(630, 20, 111, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        giris.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(giris)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        giris.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(giris)
        self.statusbar.setObjectName("statusbar")
        giris.setStatusBar(self.statusbar)

        self.retranslateUi(giris)
        QtCore.QMetaObject.connectSlotsByName(giris)

    def retranslateUi(self, giris):
        _translate = QtCore.QCoreApplication.translate
        giris.setWindowTitle(_translate("giris", "Giriş Sayfası"))
        self.label.setText(_translate("giris", "Kullanıcı Adı:"))
        self.label_2.setText(_translate("giris", "Şifre:"))
        self.pushButton.setText(_translate("giris", "Giriş Yap"))
        self.pushButton_2.setText(_translate("giris", "Developer Login"))
