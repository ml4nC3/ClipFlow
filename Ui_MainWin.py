# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(575, 782)
        MainWindow.setMinimumSize(QtCore.QSize(575, 0))
        MainWindow.setMaximumSize(QtCore.QSize(575, 1000))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbl_back_image = QtWidgets.QLabel(self.centralwidget)
        self.lbl_back_image.setGeometry(QtCore.QRect(0, -10, 571, 611))
        self.lbl_back_image.setText("")
        self.lbl_back_image.setPixmap(QtGui.QPixmap("images/ClipFlowBackground.jpg"))
        self.lbl_back_image.setObjectName("lbl_back_image")
        self.gb_lever = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_lever.setGeometry(QtCore.QRect(330, 430, 131, 71))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.gb_lever.setFont(font)
        self.gb_lever.setStyleSheet("background-color: None;")
        self.gb_lever.setObjectName("gb_lever")
        self.lbl_lever = QtWidgets.QLabel(self.gb_lever)
        self.lbl_lever.setGeometry(QtCore.QRect(10, 20, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_lever.setFont(font)
        self.lbl_lever.setStyleSheet("background-color: rgb(170, 0, 0);\n"
"color: rgb(240, 240, 240);")
        self.lbl_lever.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_lever.setObjectName("lbl_lever")
        self.btn_lever = QtWidgets.QPushButton(self.gb_lever)
        self.btn_lever.setEnabled(True)
        self.btn_lever.setGeometry(QtCore.QRect(10, 40, 111, 23))
        self.btn_lever.setObjectName("btn_lever")
        self.gb_flow = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_flow.setGeometry(QtCore.QRect(90, 480, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.gb_flow.setFont(font)
        self.gb_flow.setObjectName("gb_flow")
        self.lbl_flow_value = QtWidgets.QLabel(self.gb_flow)
        self.lbl_flow_value.setGeometry(QtCore.QRect(6, 22, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_flow_value.setFont(font)
        self.lbl_flow_value.setStyleSheet("background-color: rgb(85, 170, 255);\n"
"color: rgb(255, 255, 255);")
        self.lbl_flow_value.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_flow_value.setObjectName("lbl_flow_value")
        self.gb_events = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_events.setGeometry(QtCore.QRect(5, 550, 561, 151))
        self.gb_events.setStyleSheet("")
        self.gb_events.setObjectName("gb_events")
        self.cmbx_event_selector = QtWidgets.QComboBox(self.gb_events)
        self.cmbx_event_selector.setGeometry(QtCore.QRect(80, 30, 131, 22))
        self.cmbx_event_selector.setObjectName("cmbx_event_selector")
        self.lbl_event_selector = QtWidgets.QLabel(self.gb_events)
        self.lbl_event_selector.setGeometry(QtCore.QRect(10, 30, 71, 21))
        self.lbl_event_selector.setObjectName("lbl_event_selector")
        self.btn_event_start = QtWidgets.QPushButton(self.gb_events)
        self.btn_event_start.setEnabled(False)
        self.btn_event_start.setGeometry(QtCore.QRect(121, 60, 91, 23))
        self.btn_event_start.setObjectName("btn_event_start")
        self.btn_event_create = QtWidgets.QPushButton(self.gb_events)
        self.btn_event_create.setEnabled(False)
        self.btn_event_create.setGeometry(QtCore.QRect(10, 60, 91, 23))
        self.btn_event_create.setObjectName("btn_event_create")
        self.lbl_leak = QtWidgets.QLabel(self.gb_events)
        self.lbl_leak.setGeometry(QtCore.QRect(10, 120, 71, 21))
        self.lbl_leak.setObjectName("lbl_leak")
        self.spinBox_leak_flowrate = QtWidgets.QSpinBox(self.gb_events)
        self.spinBox_leak_flowrate.setGeometry(QtCore.QRect(80, 120, 61, 22))
        self.spinBox_leak_flowrate.setObjectName("spinBox_leak_flowrate")
        self.btn_leak_add = QtWidgets.QPushButton(self.gb_events)
        self.btn_leak_add.setEnabled(False)
        self.btn_leak_add.setGeometry(QtCore.QRect(150, 120, 61, 23))
        self.btn_leak_add.setObjectName("btn_leak_add")
        self.line_leak = QtWidgets.QFrame(self.gb_events)
        self.line_leak.setGeometry(QtCore.QRect(10, 93, 201, 16))
        self.line_leak.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_leak.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_leak.setObjectName("line_leak")
        self.btn_event_delete = QtWidgets.QPushButton(self.gb_events)
        self.btn_event_delete.setEnabled(False)
        self.btn_event_delete.setGeometry(QtCore.QRect(230, 120, 141, 23))
        self.btn_event_delete.setObjectName("btn_event_delete")
        self.btn_event_delete_all = QtWidgets.QPushButton(self.gb_events)
        self.btn_event_delete_all.setEnabled(False)
        self.btn_event_delete_all.setGeometry(QtCore.QRect(400, 120, 151, 23))
        self.btn_event_delete_all.setObjectName("btn_event_delete_all")
        self.tree_events = QtWidgets.QTreeWidget(self.gb_events)
        self.tree_events.setGeometry(QtCore.QRect(230, 20, 321, 91))
        self.tree_events.setObjectName("tree_events")
        self.lbl_event_selector.raise_()
        self.cmbx_event_selector.raise_()
        self.btn_event_start.raise_()
        self.btn_event_create.raise_()
        self.lbl_leak.raise_()
        self.spinBox_leak_flowrate.raise_()
        self.btn_leak_add.raise_()
        self.line_leak.raise_()
        self.btn_event_delete.raise_()
        self.btn_event_delete_all.raise_()
        self.tree_events.raise_()
        self.gb_serial = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_serial.setGeometry(QtCore.QRect(5, 709, 561, 51))
        self.gb_serial.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gb_serial.setObjectName("gb_serial")
        self.lbl_com_port = QtWidgets.QLabel(self.gb_serial)
        self.lbl_com_port.setGeometry(QtCore.QRect(240, 20, 61, 21))
        self.lbl_com_port.setObjectName("lbl_com_port")
        self.lineEdit_com_port = QtWidgets.QLineEdit(self.gb_serial)
        self.lineEdit_com_port.setGeometry(QtCore.QRect(300, 20, 81, 20))
        self.lineEdit_com_port.setObjectName("lineEdit_com_port")
        self.lbl_baudrate = QtWidgets.QLabel(self.gb_serial)
        self.lbl_baudrate.setGeometry(QtCore.QRect(390, 20, 41, 21))
        self.lbl_baudrate.setObjectName("lbl_baudrate")
        self.lbl_com_status = QtWidgets.QLabel(self.gb_serial)
        self.lbl_com_status.setGeometry(QtCore.QRect(10, 20, 51, 21))
        self.lbl_com_status.setObjectName("lbl_com_status")
        self.lbl_com_status_text = QtWidgets.QLabel(self.gb_serial)
        self.lbl_com_status_text.setGeometry(QtCore.QRect(50, 20, 181, 21))
        self.lbl_com_status_text.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.lbl_com_status_text.setObjectName("lbl_com_status_text")
        self.spinBox_baudrate = QtWidgets.QSpinBox(self.gb_serial)
        self.spinBox_baudrate.setGeometry(QtCore.QRect(440, 20, 111, 22))
        self.spinBox_baudrate.setMinimum(110)
        self.spinBox_baudrate.setMaximum(256000)
        self.spinBox_baudrate.setProperty("value", 9600)
        self.spinBox_baudrate.setObjectName("spinBox_baudrate")
        self.gb_battery = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_battery.setGeometry(QtCore.QRect(489, 70, 61, 351))
        self.gb_battery.setObjectName("gb_battery")
        self.vslider_battery = QtWidgets.QSlider(self.gb_battery)
        self.vslider_battery.setGeometry(QtCore.QRect(20, 30, 22, 271))
        self.vslider_battery.setMaximum(5000)
        self.vslider_battery.setSingleStep(100)
        self.vslider_battery.setPageStep(1)
        self.vslider_battery.setSliderPosition(5000)
        self.vslider_battery.setOrientation(QtCore.Qt.Vertical)
        self.vslider_battery.setObjectName("vslider_battery")
        self.lbl_battery_voltage = QtWidgets.QLabel(self.gb_battery)
        self.lbl_battery_voltage.setGeometry(QtCore.QRect(6, 313, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_battery_voltage.setFont(font)
        self.lbl_battery_voltage.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.lbl_battery_voltage.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_battery_voltage.setObjectName("lbl_battery_voltage")
        self.gb_interface = QtWidgets.QGroupBox(self.centralwidget)
        self.gb_interface.setGeometry(QtCore.QRect(120, 130, 261, 221))
        self.gb_interface.setStyleSheet("background-color: None;\n"
"color: rgb(240, 240, 240);")
        self.gb_interface.setObjectName("gb_interface")
        self.btn_off = QtWidgets.QPushButton(self.gb_interface)
        self.btn_off.setGeometry(QtCore.QRect(95, 112, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_off.setFont(font)
        self.btn_off.setStyleSheet("color: None;")
        self.btn_off.setObjectName("btn_off")
        self.lbl_green_led = QtWidgets.QLabel(self.gb_interface)
        self.lbl_green_led.setGeometry(QtCore.QRect(104, 159, 21, 21))
        self.lbl_green_led.setStyleSheet("background-color: rgb(0, 60, 0);")
        self.lbl_green_led.setText("")
        self.lbl_green_led.setObjectName("lbl_green_led")
        self.lbl_red_led = QtWidgets.QLabel(self.gb_interface)
        self.lbl_red_led.setGeometry(QtCore.QRect(130, 159, 21, 21))
        self.lbl_red_led.setStyleSheet("background-color: rgb(120, 0, 0);")
        self.lbl_red_led.setText("")
        self.lbl_red_led.setObjectName("lbl_red_led")
        self.lbl_time_count = QtWidgets.QLabel(self.gb_interface)
        self.lbl_time_count.setGeometry(QtCore.QRect(211, 205, 47, 13))
        self.lbl_time_count.setText("")
        self.lbl_time_count.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_time_count.setObjectName("lbl_time_count")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Clip Flow Simulator"))
        self.gb_lever.setTitle(_translate("MainWindow", "Levier"))
        self.lbl_lever.setText(_translate("MainWindow", "Levé"))
        self.btn_lever.setText(_translate("MainWindow", "Réarmer"))
        self.gb_flow.setTitle(_translate("MainWindow", "Débit"))
        self.lbl_flow_value.setText(_translate("MainWindow", "0 L/s"))
        self.gb_events.setTitle(_translate("MainWindow", "Evènements"))
        self.lbl_event_selector.setText(_translate("MainWindow", "Evènement :"))
        self.btn_event_start.setText(_translate("MainWindow", "Lancer"))
        self.btn_event_create.setText(_translate("MainWindow", "Créer"))
        self.lbl_leak.setText(_translate("MainWindow", "Fuite (mL/s) :"))
        self.btn_leak_add.setText(_translate("MainWindow", "Ajouter"))
        self.btn_event_delete.setText(_translate("MainWindow", "Supprimer"))
        self.btn_event_delete_all.setText(_translate("MainWindow", "Tout Supprimer"))
        self.tree_events.headerItem().setText(0, _translate("MainWindow", "Evènements"))
        self.tree_events.headerItem().setText(1, _translate("MainWindow", "Débit (L/s)"))
        self.tree_events.headerItem().setText(2, _translate("MainWindow", "Temps restant (s)"))
        self.gb_serial.setTitle(_translate("MainWindow", "Communication série"))
        self.lbl_com_port.setText(_translate("MainWindow", "Port série :"))
        self.lineEdit_com_port.setText(_translate("MainWindow", "COM2"))
        self.lbl_baudrate.setText(_translate("MainWindow", "Vitesse :"))
        self.lbl_com_status.setText(_translate("MainWindow", "Statut :"))
        self.lbl_com_status_text.setText(_translate("MainWindow", "Déconnecté"))
        self.gb_battery.setTitle(_translate("MainWindow", "Pile"))
        self.lbl_battery_voltage.setText(_translate("MainWindow", "5V"))
        self.gb_interface.setTitle(_translate("MainWindow", "Interface"))
        self.btn_off.setText(_translate("MainWindow", "OFF"))

