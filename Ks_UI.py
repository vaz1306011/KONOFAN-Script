from PyQt5 import QtCore, QtGui, QtWidgets


class Ks_UI:
    def setupUi(self, root):
        try:
            version = str(self.version)
        except NameError:
            version = ""

        root.setObjectName("root")
        self.setFixedSize(300, 300)

        self.version_label = QtWidgets.QLabel(version, root)
        self.version_label.move(10, 10)
        self.version_label.setFont(QtGui.QFont("Arial", 10))
        self.version_label.setObjectName("version_label")

        self.EAL_btn = QtWidgets.QPushButton(root)
        self.EAL_btn.setGeometry(QtCore.QRect(100, 50, 101, 31))
        self.EAL_btn.setObjectName("EALbtn")

        self.EBL_btn = QtWidgets.QPushButton(root)
        self.EBL_btn.setGeometry(QtCore.QRect(100, 100, 101, 31))
        self.EBL_btn.setObjectName("EBLbtn")

        self.BAL_btn = QtWidgets.QPushButton(root)
        self.BAL_btn.setGeometry(QtCore.QRect(100, 150, 101, 31))
        self.BAL_btn.setObjectName("BALbtn")

        self.stop_btn = QtWidgets.QPushButton(root)
        self.stop_btn.setGeometry(QtCore.QRect(100, 200, 101, 31))
        self.stop_btn.setObjectName("StopBtn")

        self.retranslateUi(root)
        QtCore.QMetaObject.connectSlotsByName(root)

    def retranslateUi(self, root):
        _translate = QtCore.QCoreApplication.translate
        root.setWindowTitle(_translate("root", "Konofan Script"))
        self.EAL_btn.setText(_translate("root", "刷活動小關卡"))
        self.EBL_btn.setText(_translate("root", "刷活動boss"))
        self.BAL_btn.setText(_translate("root", "刷競技場"))
        self.stop_btn.setText(_translate("root", "停止"))
