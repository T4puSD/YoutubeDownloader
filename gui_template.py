from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(819, 725)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.left_frame = QtWidgets.QFrame(self.centralwidget)
        self.left_frame.setAutoFillBackground(False)
        self.left_frame.setStyleSheet("background-color: rgb(244, 67, 54);")
        self.left_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.left_frame.setObjectName("left_frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.left_frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_3 = QtWidgets.QFrame(self.left_frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(20, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_6.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.left_frame)
        self.frame_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBoxMediaType = QtWidgets.QGroupBox(self.frame_4)
        self.groupBoxMediaType.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxMediaType.setFont(font)
        self.groupBoxMediaType.setStyleSheet("color: rgb(255, 255, 255);")
        self.groupBoxMediaType.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBoxMediaType.setFlat(False)
        self.groupBoxMediaType.setCheckable(False)
        self.groupBoxMediaType.setChecked(False)
        self.groupBoxMediaType.setObjectName("groupBoxMediaType")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBoxMediaType)
        self.verticalLayout_4.setContentsMargins(4, -1, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton_audio = QtWidgets.QRadioButton(self.groupBoxMediaType)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.radioButton_audio.setFont(font)
        self.radioButton_audio.setStyleSheet("color: rgb(255, 255, 255);")
        self.radioButton_audio.setChecked(True)
        self.radioButton_audio.setObjectName("radioButton_audio")
        self.horizontalLayout.addWidget(self.radioButton_audio)
        self.radioButton_video = QtWidgets.QRadioButton(self.groupBoxMediaType)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.radioButton_video.setFont(font)
        self.radioButton_video.setStyleSheet("color: rgb(255, 255, 255);\n"
"border: none;")
        self.radioButton_video.setObjectName("radioButton_video")
        self.horizontalLayout.addWidget(self.radioButton_video)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addWidget(self.groupBoxMediaType)
        self.groupBoxMediaQuality = QtWidgets.QGroupBox(self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxMediaQuality.setFont(font)
        self.groupBoxMediaQuality.setFlat(False)
        self.groupBoxMediaQuality.setObjectName("groupBoxMediaQuality")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBoxMediaQuality)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame = QtWidgets.QFrame(self.groupBoxMediaQuality)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.radioButtonNormalQuality = QtWidgets.QRadioButton(self.frame)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.radioButtonNormalQuality.setFont(font)
        self.radioButtonNormalQuality.setChecked(True)
        self.radioButtonNormalQuality.setObjectName("radioButtonNormalQuality")
        self.horizontalLayout_4.addWidget(self.radioButtonNormalQuality)
        self.radioButtonHighQuality = QtWidgets.QRadioButton(self.frame)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.radioButtonHighQuality.setFont(font)
        self.radioButtonHighQuality.setObjectName("radioButtonHighQuality")
        self.horizontalLayout_4.addWidget(self.radioButtonHighQuality)
        self.horizontalLayout_3.addWidget(self.frame)
        self.verticalLayout_5.addWidget(self.groupBoxMediaQuality)
        self.verticalLayout_6.addWidget(self.frame_4)
        self.startServerButton = QtWidgets.QPushButton(self.left_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startServerButton.sizePolicy().hasHeightForWidth())
        self.startServerButton.setSizePolicy(sizePolicy)
        self.startServerButton.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.startServerButton.setObjectName("startServerButton")
        self.verticalLayout_6.addWidget(self.startServerButton)
        self.gridLayout.addWidget(self.left_frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 819, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionStartServer = QtWidgets.QAction(MainWindow)
        self.actionStartServer.setObjectName("actionStartServer")
        self.actionCloseServer = QtWidgets.QAction(MainWindow)
        self.actionCloseServer.setObjectName("actionCloseServer")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionUserManual = QtWidgets.QAction(MainWindow)
        self.actionUserManual.setObjectName("actionUserManual")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionStartServer)
        self.menuFile.addAction(self.actionCloseServer)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionUserManual)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Youtube Downloader"))
        self.label.setText(_translate("MainWindow", "Youtube Downloader"))
        self.label_2.setText(_translate("MainWindow", "Download in Audio or Video"))
        self.groupBoxMediaType.setTitle(_translate("MainWindow", "Please choose which format do you want to download?"))
        self.radioButton_audio.setText(_translate("MainWindow", "Audio"))
        self.radioButton_video.setText(_translate("MainWindow", "Video"))
        self.groupBoxMediaQuality.setTitle(_translate("MainWindow", "Please choose the media quality"))
        self.radioButtonNormalQuality.setText(_translate("MainWindow", "Normal"))
        self.radioButtonHighQuality.setText(_translate("MainWindow", "High Quality"))
        self.startServerButton.setText(_translate("MainWindow", "Start"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionStartServer.setText(_translate("MainWindow", "Start Server"))
        self.actionCloseServer.setText(_translate("MainWindow", "Close Server"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionUserManual.setText(_translate("MainWindow", "User Manual"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
