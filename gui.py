import sys
from PyQt5.Qt import *
from gui_template import Ui_MainWindow
from notifier import notifyAboutTheService
from config import getConfigInstance, generateConfigFile
from daemon import startTheServers, stopTheServers, resetTheThreads, reloadConfig

class YoutubeDownloader(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)
        # handling the menu exit button
        self.actionExit.triggered.connect(self.exit_app)

        # handling the start server button
        self.startServerButton.clicked.connect(self.start_server)
        # handling the stop | reset button
        self.stopOrResetButton.clicked.connect(self.stop_or_reset)

        self.actionStartServer.triggered.connect(self.getConfigData)
    
    def generateConfig(self):
        configurations = self.getConfigData()
        conf = getConfigInstance()
        conf['media_conf']['media_type'] = configurations[0]
        conf['media_conf']['media_quality'] = configurations[1]
        generateConfigFile(conf)
    
    def getConfigData(self):
        mediaTypeMap = {'Audio':'audio','Video':'video'}
        mediaQualityMap = {'Normal':'normal','High Quality':'hq'}
        mediaType = None
        mediaQuality = None
        for i in self.groupBoxMediaType.findChildren(QRadioButton):
            if i.isChecked():
                mediaType = i.text()

        for i in self.groupBoxMediaQuality.findChildren(QRadioButton):
            if i.isChecked():
                mediaQuality = i.text()
        
        return [mediaTypeMap[mediaType], mediaQualityMap[mediaQuality]]

        # for i in self.groupBoxMediaType.children():
        #     print(i)

    def disable_radio_buttons(self):
        self.groupBoxMediaType.setDisabled(True)
        self.groupBoxMediaQuality.setDisabled(True)

    def enable_radio_buttons(self):
        self.groupBoxMediaType.setDisabled(False)
        self.groupBoxMediaQuality.setDisabled(False)
    
    def start_server(self):
        #generating config from the radio butons
        self.generateConfig()
        # reloading config for the daemon server
        reloadConfig()
        # disabling radiobuttons after starting the server
        self.disable_radio_buttons()
        # handling double start server button click
        # button won't response if server is already running
        is_alive = startTheServers()
        if not is_alive:
            notifyAboutTheService("Server Started","Download server started successfully!")
    
    def stop_or_reset(self):
        # enabling radiobuttons after pressing stop | reset
        self.enable_radio_buttons()
        # handling duplicates buttons clicks
        is_stopped = stopTheServers()
        if is_stopped:
            resetTheThreads()
            notifyAboutTheService("Server Stopped!","Download server stopped!")
    
    def exit_app(self):
        stopTheServers()
        sys.exit(0)

app = QApplication(sys.argv)
form = YoutubeDownloader()
form.show()
sys.exit(app.exec_())