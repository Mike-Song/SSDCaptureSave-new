# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Tasks\Work\SSDCaptureSave\SSDCaptureSave.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(945, 615)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(945, 614))
        MainWindow.setMaximumSize(QtCore.QSize(945, 615))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(927, 552))
        self.tabWidget.setMaximumSize(QtCore.QSize(927, 552))
        self.tabWidget.setObjectName("tabWidget")
        self.tabConfig = QtWidgets.QWidget()
        self.tabConfig.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tabConfig.setObjectName("tabConfig")
        self.label_SampleRate = QtWidgets.QLabel(self.tabConfig)
        self.label_SampleRate.setGeometry(QtCore.QRect(20, 60, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_SampleRate.setFont(font)
        self.label_SampleRate.setObjectName("label_SampleRate")
        self.comboBox_SampleRate = QtWidgets.QComboBox(self.tabConfig)
        self.comboBox_SampleRate.setGeometry(QtCore.QRect(140, 50, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_SampleRate.setFont(font)
        self.comboBox_SampleRate.setMouseTracking(True)
        self.comboBox_SampleRate.setTabletTracking(True)
        self.comboBox_SampleRate.setEditable(True)
        self.comboBox_SampleRate.setObjectName("comboBox_SampleRate")
        self.comboBox_SampleRate.addItem("")
        self.comboBox_SampleRate.addItem("")
        self.comboBox_SampleRate.addItem("")
        self.comboBox_Clock = QtWidgets.QComboBox(self.tabConfig)
        self.comboBox_Clock.setGeometry(QtCore.QRect(140, 100, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_Clock.setFont(font)
        self.comboBox_Clock.setObjectName("comboBox_Clock")
        self.comboBox_Clock.addItem("")
        self.comboBox_Clock.addItem("")
        self.label_Clock = QtWidgets.QLabel(self.tabConfig)
        self.label_Clock.setGeometry(QtCore.QRect(20, 110, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_Clock.setFont(font)
        self.label_Clock.setObjectName("label_Clock")
        self.comboBox_Trigger = QtWidgets.QComboBox(self.tabConfig)
        self.comboBox_Trigger.setGeometry(QtCore.QRect(140, 150, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_Trigger.setFont(font)
        self.comboBox_Trigger.setObjectName("comboBox_Trigger")
        self.comboBox_Trigger.addItem("")
        self.comboBox_Trigger.addItem("")
        self.label_Trigger = QtWidgets.QLabel(self.tabConfig)
        self.label_Trigger.setGeometry(QtCore.QRect(20, 160, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_Trigger.setFont(font)
        self.label_Trigger.setObjectName("label_Trigger")
        self.tabWidget.addTab(self.tabConfig, "")
        self.tabRealTime = QtWidgets.QWidget()
        self.tabRealTime.setObjectName("tabRealTime")
        self.widget_Signal_RealTime = QtWidgets.QWidget(self.tabRealTime)
        self.widget_Signal_RealTime.setGeometry(QtCore.QRect(119, 0, 801, 521))
        self.widget_Signal_RealTime.setInputMethodHints(QtCore.Qt.ImhNone)
        self.widget_Signal_RealTime.setObjectName("widget_Signal_RealTime")
        self.radioButton_CHA_RealTime = QtWidgets.QRadioButton(self.tabRealTime)
        self.radioButton_CHA_RealTime.setGeometry(QtCore.QRect(10, 30, 91, 17))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_CHA_RealTime.sizePolicy().hasHeightForWidth())
        self.radioButton_CHA_RealTime.setSizePolicy(sizePolicy)
        self.radioButton_CHA_RealTime.setMinimumSize(QtCore.QSize(72, 17))
        self.radioButton_CHA_RealTime.setChecked(True)
        self.radioButton_CHA_RealTime.setObjectName("radioButton_CHA_RealTime")
        self.radioButton_CHB_RealTime = QtWidgets.QRadioButton(self.tabRealTime)
        self.radioButton_CHB_RealTime.setGeometry(QtCore.QRect(10, 50, 91, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_CHB_RealTime.sizePolicy().hasHeightForWidth())
        self.radioButton_CHB_RealTime.setSizePolicy(sizePolicy)
        self.radioButton_CHB_RealTime.setMinimumSize(QtCore.QSize(82, 23))
        self.radioButton_CHB_RealTime.setChecked(False)
        self.radioButton_CHB_RealTime.setObjectName("radioButton_CHB_RealTime")
        self.checkBox_ShowGrid_RealTime = QtWidgets.QCheckBox(self.tabRealTime)
        self.checkBox_ShowGrid_RealTime.setGeometry(QtCore.QRect(10, 80, 91, 17))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_ShowGrid_RealTime.sizePolicy().hasHeightForWidth())
        self.checkBox_ShowGrid_RealTime.setSizePolicy(sizePolicy)
        self.checkBox_ShowGrid_RealTime.setMinimumSize(QtCore.QSize(71, 17))
        self.checkBox_ShowGrid_RealTime.setChecked(True)
        self.checkBox_ShowGrid_RealTime.setObjectName("checkBox_ShowGrid_RealTime")
        self.pushButton_Start_RealTime = QtWidgets.QPushButton(self.tabRealTime)
        self.pushButton_Start_RealTime.setEnabled(True)
        self.pushButton_Start_RealTime.setGeometry(QtCore.QRect(20, 430, 81, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Start_RealTime.sizePolicy().hasHeightForWidth())
        self.pushButton_Start_RealTime.setSizePolicy(sizePolicy)
        self.pushButton_Start_RealTime.setMinimumSize(QtCore.QSize(81, 23))
        self.pushButton_Start_RealTime.setObjectName("pushButton_Start_RealTime")
        self.pushButton_Stop_RealTime = QtWidgets.QPushButton(self.tabRealTime)
        self.pushButton_Stop_RealTime.setEnabled(True)
        self.pushButton_Stop_RealTime.setGeometry(QtCore.QRect(20, 460, 82, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Stop_RealTime.sizePolicy().hasHeightForWidth())
        self.pushButton_Stop_RealTime.setSizePolicy(sizePolicy)
        self.pushButton_Stop_RealTime.setMinimumSize(QtCore.QSize(82, 23))
        self.pushButton_Stop_RealTime.setObjectName("pushButton_Stop_RealTime")
        self.groupBox_Scale = QtWidgets.QGroupBox(self.tabRealTime)
        self.groupBox_Scale.setGeometry(QtCore.QRect(10, 170, 91, 51))
        self.groupBox_Scale.setObjectName("groupBox_Scale")
        self.lineEdit_Scale = QtWidgets.QLineEdit(self.groupBox_Scale)
        self.lineEdit_Scale.setGeometry(QtCore.QRect(10, 20, 41, 20))
        self.lineEdit_Scale.setObjectName("lineEdit_Scale")
        self.label_3 = QtWidgets.QLabel(self.groupBox_Scale)
        self.label_3.setGeometry(QtCore.QRect(60, 20, 21, 16))
        self.label_3.setObjectName("label_3")
        self.groupBox_Ref = QtWidgets.QGroupBox(self.tabRealTime)
        self.groupBox_Ref.setGeometry(QtCore.QRect(10, 110, 91, 51))
        self.groupBox_Ref.setObjectName("groupBox_Ref")
        self.lineEdit_RefLevel = QtWidgets.QLineEdit(self.groupBox_Ref)
        self.lineEdit_RefLevel.setGeometry(QtCore.QRect(10, 20, 41, 20))
        self.lineEdit_RefLevel.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.lineEdit_RefLevel.setObjectName("lineEdit_RefLevel")
        self.label_7 = QtWidgets.QLabel(self.groupBox_Ref)
        self.label_7.setGeometry(QtCore.QRect(60, 20, 21, 16))
        self.label_7.setObjectName("label_7")
        self.groupBox_StartFreq = QtWidgets.QGroupBox(self.tabRealTime)
        self.groupBox_StartFreq.setGeometry(QtCore.QRect(10, 240, 91, 51))
        self.groupBox_StartFreq.setObjectName("groupBox_StartFreq")
        self.lineEdit_StartFreq = QtWidgets.QLineEdit(self.groupBox_StartFreq)
        self.lineEdit_StartFreq.setGeometry(QtCore.QRect(10, 20, 41, 20))
        self.lineEdit_StartFreq.setObjectName("lineEdit_StartFreq")
        self.label_8 = QtWidgets.QLabel(self.groupBox_StartFreq)
        self.label_8.setGeometry(QtCore.QRect(60, 20, 21, 16))
        self.label_8.setObjectName("label_8")
        self.groupBox_StopFreq = QtWidgets.QGroupBox(self.tabRealTime)
        self.groupBox_StopFreq.setGeometry(QtCore.QRect(10, 310, 91, 51))
        self.groupBox_StopFreq.setObjectName("groupBox_StopFreq")
        self.lineEdit_StopFreq = QtWidgets.QLineEdit(self.groupBox_StopFreq)
        self.lineEdit_StopFreq.setGeometry(QtCore.QRect(10, 20, 41, 20))
        self.lineEdit_StopFreq.setObjectName("lineEdit_StopFreq")
        self.label_9 = QtWidgets.QLabel(self.groupBox_StopFreq)
        self.label_9.setGeometry(QtCore.QRect(60, 20, 21, 16))
        self.label_9.setObjectName("label_9")
        self.groupBox_RealTimeSetting = QtWidgets.QGroupBox(self.tabRealTime)
        self.groupBox_RealTimeSetting.setGeometry(QtCore.QRect(0, 10, 111, 371))
        self.groupBox_RealTimeSetting.setObjectName("groupBox_RealTimeSetting")
        self.pushButton_Save_RealTime = QtWidgets.QPushButton(self.tabRealTime)
        self.pushButton_Save_RealTime.setEnabled(True)
        self.pushButton_Save_RealTime.setGeometry(QtCore.QRect(20, 490, 82, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Save_RealTime.sizePolicy().hasHeightForWidth())
        self.pushButton_Save_RealTime.setSizePolicy(sizePolicy)
        self.pushButton_Save_RealTime.setMinimumSize(QtCore.QSize(82, 23))
        self.pushButton_Save_RealTime.setObjectName("pushButton_Save_RealTime")
        self.groupBox_RealTimeSetting.raise_()
        self.widget_Signal_RealTime.raise_()
        self.radioButton_CHA_RealTime.raise_()
        self.radioButton_CHB_RealTime.raise_()
        self.checkBox_ShowGrid_RealTime.raise_()
        self.pushButton_Start_RealTime.raise_()
        self.pushButton_Stop_RealTime.raise_()
        self.groupBox_Scale.raise_()
        self.groupBox_Ref.raise_()
        self.groupBox_StartFreq.raise_()
        self.groupBox_StopFreq.raise_()
        self.pushButton_Save_RealTime.raise_()
        self.tabWidget.addTab(self.tabRealTime, "")
        self.tab_Files = QtWidgets.QWidget()
        self.tab_Files.setObjectName("tab_Files")
        self.tableView_SSD = QtWidgets.QTableView(self.tab_Files)
        self.tableView_SSD.setGeometry(QtCore.QRect(10, 40, 940, 210))
        self.tableView_SSD.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView_SSD.setObjectName("tableView_SSD")
        self.tableView_Local = QtWidgets.QTableView(self.tab_Files)
        self.tableView_Local.setGeometry(QtCore.QRect(10, 290, 940, 231))
        self.tableView_Local.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView_Local.setObjectName("tableView_Local")
        self.layoutWidget = QtWidgets.QWidget(self.tab_Files)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 260, 891, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_LocalFiles = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_LocalFiles.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_LocalFiles.setObjectName("horizontalLayout_LocalFiles")
        self.label_Local = QtWidgets.QLabel(self.layoutWidget)
        self.label_Local.setObjectName("label_Local")
        self.horizontalLayout_LocalFiles.addWidget(self.label_Local)
        self.lineEdit_LocalFolder = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_LocalFolder.setReadOnly(True)
        self.lineEdit_LocalFolder.setObjectName("lineEdit_LocalFolder")
        self.horizontalLayout_LocalFiles.addWidget(self.lineEdit_LocalFolder)
        self.pushButton_Local_Browse = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Local_Browse.setObjectName("pushButton_Local_Browse")
        self.horizontalLayout_LocalFiles.addWidget(self.pushButton_Local_Browse)
        self.layoutWidget1 = QtWidgets.QWidget(self.tab_Files)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 10, 591, 25))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_SSDFiles = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_SSDFiles.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_SSDFiles.setSpacing(20)
        self.horizontalLayout_SSDFiles.setObjectName("horizontalLayout_SSDFiles")
        self.label_SSD = QtWidgets.QLabel(self.layoutWidget1)
        self.label_SSD.setObjectName("label_SSD")
        self.horizontalLayout_SSDFiles.addWidget(self.label_SSD)
        self.pushButton_SSD_Search = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_SSD_Search.setFont(font)
        self.pushButton_SSD_Search.setObjectName("pushButton_SSD_Search")
        self.horizontalLayout_SSDFiles.addWidget(self.pushButton_SSD_Search)
        self.pushButton_StartCapture = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_StartCapture.setEnabled(True)
        self.pushButton_StartCapture.setObjectName("pushButton_StartCapture")
        self.horizontalLayout_SSDFiles.addWidget(self.pushButton_StartCapture)
        self.pushButton_StopCapture = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_StopCapture.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.pushButton_StopCapture.setObjectName("pushButton_StopCapture")
        self.horizontalLayout_SSDFiles.addWidget(self.pushButton_StopCapture)
        self.pushButton_ReadTest = QtWidgets.QPushButton(self.tab_Files)
        self.pushButton_ReadTest.setGeometry(QtCore.QRect(620, 10, 91, 23))
        self.pushButton_ReadTest.setObjectName("pushButton_ReadTest")
        self.tabWidget.addTab(self.tab_Files, "")
        self.tab_Play = QtWidgets.QWidget()
        self.tab_Play.setObjectName("tab_Play")
        self.widget_Signal = QtWidgets.QWidget(self.tab_Play)
        self.widget_Signal.setGeometry(QtCore.QRect(10, 0, 911, 471))
        self.widget_Signal.setObjectName("widget_Signal")
        self.groupBox_Playback = QtWidgets.QGroupBox(self.tab_Play)
        self.groupBox_Playback.setGeometry(QtCore.QRect(0, 470, 911, 51))
        self.groupBox_Playback.setObjectName("groupBox_Playback")
        self.layoutWidget2 = QtWidgets.QWidget(self.groupBox_Playback)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 20, 901, 31))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_Playback = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_Playback.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_Playback.setSpacing(10)
        self.horizontalLayout_Playback.setObjectName("horizontalLayout_Playback")
        self.radioButton_CHA = QtWidgets.QRadioButton(self.layoutWidget2)
        self.radioButton_CHA.setChecked(True)
        self.radioButton_CHA.setObjectName("radioButton_CHA")
        self.horizontalLayout_Playback.addWidget(self.radioButton_CHA)
        self.radioButton_CHB = QtWidgets.QRadioButton(self.layoutWidget2)
        self.radioButton_CHB.setObjectName("radioButton_CHB")
        self.horizontalLayout_Playback.addWidget(self.radioButton_CHB)
        self.checkBox_ShowGrid = QtWidgets.QCheckBox(self.layoutWidget2)
        self.checkBox_ShowGrid.setChecked(True)
        self.checkBox_ShowGrid.setObjectName("checkBox_ShowGrid")
        self.horizontalLayout_Playback.addWidget(self.checkBox_ShowGrid)
        self.pushButton_StartReplay = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_StartReplay.setEnabled(True)
        self.pushButton_StartReplay.setObjectName("pushButton_StartReplay")
        self.horizontalLayout_Playback.addWidget(self.pushButton_StartReplay)
        self.pushButton_PauseReplay = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_PauseReplay.setEnabled(True)
        self.pushButton_PauseReplay.setObjectName("pushButton_PauseReplay")
        self.horizontalLayout_Playback.addWidget(self.pushButton_PauseReplay)
        self.pushButton_StopReply = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_StopReply.setEnabled(True)
        self.pushButton_StopReply.setObjectName("pushButton_StopReply")
        self.horizontalLayout_Playback.addWidget(self.pushButton_StopReply)
        self.horizontalSlider = QtWidgets.QSlider(self.layoutWidget2)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout_Playback.addWidget(self.horizontalSlider)
        self.label_TotalTime = QtWidgets.QLabel(self.layoutWidget2)
        self.label_TotalTime.setObjectName("label_TotalTime")
        self.horizontalLayout_Playback.addWidget(self.label_TotalTime)
        self.tabWidget.addTab(self.tab_Play, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 945, 23))
        self.menubar.setObjectName("menubar")
        self.menuMain = QtWidgets.QMenu(self.menubar)
        self.menuMain.setObjectName("menuMain")
        self.menuPlay = QtWidgets.QMenu(self.menubar)
        self.menuPlay.setObjectName("menuPlay")
        self.menuCard_Type = QtWidgets.QMenu(self.menubar)
        self.menuCard_Type.setObjectName("menuCard_Type")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.action3G = QtWidgets.QAction(MainWindow)
        self.action3G.setCheckable(True)
        self.action3G.setObjectName("action3G")
        self.action100M = QtWidgets.QAction(MainWindow)
        self.action100M.setCheckable(True)
        self.action100M.setObjectName("action100M")
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setCheckable(True)
        self.actionStart.setObjectName("actionStart")
        self.actionStop = QtWidgets.QAction(MainWindow)
        self.actionStop.setCheckable(True)
        self.actionStop.setObjectName("actionStop")
        self.menuMain.addAction(self.actionOpen)
        self.menuPlay.addAction(self.actionStart)
        self.menuPlay.addAction(self.actionStop)
        self.menuCard_Type.addAction(self.action3G)
        self.menuCard_Type.addAction(self.action100M)
        self.menubar.addAction(self.menuMain.menuAction())
        self.menubar.addAction(self.menuPlay.menuAction())
        self.menubar.addAction(self.menuCard_Type.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Signal Capture and Save"))
        self.label_SampleRate.setText(_translate("MainWindow", "Sample Rate:"))
        self.comboBox_SampleRate.setCurrentText(_translate("MainWindow", "3G"))
        self.comboBox_SampleRate.setItemText(0, _translate("MainWindow", "3G"))
        self.comboBox_SampleRate.setItemText(1, _translate("MainWindow", "100M"))
        self.comboBox_SampleRate.setItemText(2, _translate("MainWindow", "50M"))
        self.comboBox_Clock.setItemText(0, _translate("MainWindow", "Internal"))
        self.comboBox_Clock.setItemText(1, _translate("MainWindow", "External"))
        self.label_Clock.setText(_translate("MainWindow", "Clock:"))
        self.comboBox_Trigger.setItemText(0, _translate("MainWindow", "Internal"))
        self.comboBox_Trigger.setItemText(1, _translate("MainWindow", "External"))
        self.label_Trigger.setText(_translate("MainWindow", "Trigger:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabConfig), _translate("MainWindow", "Configuration"))
        self.radioButton_CHA_RealTime.setText(_translate("MainWindow", "Channel A"))
        self.radioButton_CHB_RealTime.setText(_translate("MainWindow", "Channel B"))
        self.checkBox_ShowGrid_RealTime.setText(_translate("MainWindow", "Show Grid"))
        self.pushButton_Start_RealTime.setText(_translate("MainWindow", "Start"))
        self.pushButton_Stop_RealTime.setText(_translate("MainWindow", "Stop"))
        self.groupBox_Scale.setTitle(_translate("MainWindow", "Scale/div:"))
        self.lineEdit_Scale.setText(_translate("MainWindow", "10"))
        self.label_3.setText(_translate("MainWindow", "dBm"))
        self.groupBox_Ref.setTitle(_translate("MainWindow", "Ref Level:"))
        self.lineEdit_RefLevel.setText(_translate("MainWindow", "0"))
        self.label_7.setText(_translate("MainWindow", "dBm"))
        self.groupBox_StartFreq.setTitle(_translate("MainWindow", "Start Freq:"))
        self.lineEdit_StartFreq.setText(_translate("MainWindow", "100"))
        self.label_8.setText(_translate("MainWindow", "MHz"))
        self.groupBox_StopFreq.setTitle(_translate("MainWindow", "Stop Freq:"))
        self.lineEdit_StopFreq.setText(_translate("MainWindow", "1400"))
        self.label_9.setText(_translate("MainWindow", "MHz"))
        self.groupBox_RealTimeSetting.setTitle(_translate("MainWindow", "Settings"))
        self.pushButton_Save_RealTime.setText(_translate("MainWindow", "Save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRealTime), _translate("MainWindow", "Real Time Capture"))
        self.label_Local.setText(_translate("MainWindow", "Local Files:"))
        self.pushButton_Local_Browse.setText(_translate("MainWindow", "Browse..."))
        self.label_SSD.setText(_translate("MainWindow", "SSD Files:"))
        self.pushButton_SSD_Search.setText(_translate("MainWindow", "Search..."))
        self.pushButton_StartCapture.setText(_translate("MainWindow", "Start Capture"))
        self.pushButton_StopCapture.setText(_translate("MainWindow", "Stop Capture"))
        self.pushButton_ReadTest.setText(_translate("MainWindow", "Test Read SSD"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Files), _translate("MainWindow", "File Manager"))
        self.groupBox_Playback.setTitle(_translate("MainWindow", "Playback:"))
        self.radioButton_CHA.setText(_translate("MainWindow", "Channel A"))
        self.radioButton_CHB.setText(_translate("MainWindow", "Channel B"))
        self.checkBox_ShowGrid.setText(_translate("MainWindow", "Show Grid"))
        self.pushButton_StartReplay.setText(_translate("MainWindow", "Start"))
        self.pushButton_PauseReplay.setText(_translate("MainWindow", "Pause"))
        self.pushButton_StopReply.setText(_translate("MainWindow", "Stop"))
        self.label_TotalTime.setText(_translate("MainWindow", "TotalTime"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Play), _translate("MainWindow", "Signal Playback"))
        self.menuMain.setTitle(_translate("MainWindow", "File"))
        self.menuPlay.setTitle(_translate("MainWindow", "Capture"))
        self.menuCard_Type.setTitle(_translate("MainWindow", "Card Type"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.action3G.setText(_translate("MainWindow", "3G"))
        self.action100M.setText(_translate("MainWindow", "100M"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionStop.setText(_translate("MainWindow", "Stop"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
