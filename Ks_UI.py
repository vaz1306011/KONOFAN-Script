from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *


class Ks_UI:
    class Tray(QSystemTrayIcon):
        def __init__(self, parent, icon: QIcon):
            super().__init__()

            self.setIcon(icon)
            self.setToolTip("KonofanScript")

            self.menu = QMenu()
            self.menu.addAction("還原主視窗", parent.show)
            self.menu.addAction("結束", QCoreApplication.instance().quit)
            self.setContextMenu(self.menu)

    def setup_ui(self, root) -> None:
        root.setObjectName("root")

        self.icon = QIcon("icon.ico")
        self.setWindowIcon(self.icon)
        self.setFixedSize(300, 300)

        self.tray = self.Tray(self, self.icon)
        self.tray.show()

        try:
            version = str(self.version)
        except NameError:
            version = ""

        self.version_label = QtWidgets.QLabel("版本：" + version, root)
        self.version_label.move(10, 10)
        self.version_label.setFont(QtGui.QFont("Arial", 11))
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

    def retranslateUi(self, root) -> None:
        _translate = QtCore.QCoreApplication.translate
        root.setWindowTitle(_translate("root", "Konofan Script"))
        self.EAL_btn.setText(_translate("root", "刷活動小關卡"))
        self.EBL_btn.setText(_translate("root", "刷活動boss"))
        self.BAL_btn.setText(_translate("root", "刷競技場"))
        self.stop_btn.setText(_translate("root", "停止"))
