import sys
from PyQt5.Qt import *
from gui_template import Ui_MainWindow
from notifier import notifyAboutTheService
from daemon import startTheServers, stopTheServers, resetTheThreads

class YoutubeDownloader(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self);
        # handling the menu exit button
        self.actionExit.triggered.connect(self.exit_app)

        # handling the start server button
        self.startServerButton.clicked.connect(self.start_server)
        # handling the stop | reset button
        self.stopOrResetButton.clicked.connect(self.stop_or_reset)
    
    def start_server(self):
        # handling double start server button click
        # button won't response if server is already running
        is_alive = startTheServers()
        if not is_alive:
            notifyAboutTheService("Server Started","Download server started successfully!")
    
    def stop_or_reset(self):
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