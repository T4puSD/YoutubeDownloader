import sys
from PyQt5.Qt import *
from gui_template import Ui_MainWindow
from debugger import logging
from notifier import notifyAboutTheService
from config import initConfigInstance, generateConfigFile, constructConfig
from daemon import startTheServers, stopTheServers, resetTheThreads, reloadConfig

class YoutubeDownloader(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # generating the configure.ini file
        initConfigInstance()

        self.setupUi(self)
        # handling the menu exit button
        self.actionExit.triggered.connect(self.exit_app)

        # handling the start server button
        self.startServerButton.clicked.connect(self.start_server)
        # handling the stop | reset button
        self.stopOrResetButton.clicked.connect(self.stop_or_reset)

        self.actionStartServer.triggered.connect(self.getMediaConfig)
        self.lineEditDownloadDirectoryShow.setText(self.getDownloadLocationConfig()[0])
        
        self.toolButtonDirectoryChoose.clicked.connect(self.getDirectory)

    def getDirectory(self):
        file = QFileDialog.getExistingDirectory(self,'Choose Download Directory',self.getDownloadLocationConfig()[0])
        if file:
            self.lineEditDownloadDirectoryShow.setText(file)
            config = constructConfig(file)
            # print(config['conf'].get('download_dir'))
            generateConfigFile(config)
            logging.debug("Changed download directory to: {}".format(file))
    
    def generateMediaConfig(self):
        configurations = self.getMediaConfig()
        conf = initConfigInstance()
        conf['media_conf']['media_type'] = configurations[0]
        conf['media_conf']['media_quality'] = configurations[1]
        generateConfigFile(conf)

    def getDownloadLocationConfig(self):
        config = initConfigInstance()
        download_dir = config['conf'].get('download_dir')
        downlaod_audio = config['conf'].get('download_dir_audio')
        downlaod_video = config['conf'].get('download_dir_video')
        return [download_dir,downlaod_audio,downlaod_video]

    
    def getMediaConfig(self):
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

    def disable_buttons(self):
        self.lineEditDownloadDirectoryShow.setReadOnly(True)
        self.toolButtonDirectoryChoose.setEnabled(False)
        self.groupBoxMediaType.setDisabled(True)
        self.groupBoxMediaQuality.setDisabled(True)

    def enable_buttons(self):
        self.lineEditDownloadDirectoryShow.setReadOnly(False)
        self.toolButtonDirectoryChoose.setEnabled(True)
        self.groupBoxMediaType.setDisabled(False)
        self.groupBoxMediaQuality.setDisabled(False)
    
    def start_server(self):
        #generating config from the radio butons
        self.generateMediaConfig()
        # reloading config for the daemon server
        # reloading download directories
        reloadConfig()
        
        # disabling radiobuttons after starting the server
        self.disable_buttons()
        # handling double start server button click
        # button won't response if server is already running
        is_alive = startTheServers()
        if not is_alive:
            notifyAboutTheService("Server Started","Download server started successfully!")
    
    def stop_or_reset(self):
        # enabling radiobuttons after pressing stop | reset
        self.enable_buttons()
        # handling duplicates buttons clicks
        is_stopped = stopTheServers()
        if is_stopped:
            resetTheThreads()
            notifyAboutTheService("Server Stopped!","Download server stopped!")
    
    # handling exit menu button click
    def exit_app(self):
        logging.debug("Closing GUI")
        stopTheServers()
        sys.exit(0)
    # handling x button on the main window
    def closeEvent(self, event):
        stopTheServers()
        logging.debug("Closing GUI")
        event.accept()

app = QApplication(sys.argv)
form = YoutubeDownloader()
form.show()
sys.exit(app.exec_())