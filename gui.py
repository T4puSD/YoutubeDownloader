from PyQt5.Qt import *
from gui_template import Ui_MainWindow
import sys
from daemon import startTheServer

class YoutubeDownloader(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self);

        self.actionExit.triggered.connect(self.exitApp)
        # self.actionCloseServer.triggered.connect()
        self.startServerButton.clicked.connect(startTheServer)
    
    def exitApp(self):
        sys.exit(0)

app = QApplication(sys.argv)
form = YoutubeDownloader()
form.show()
sys.exit(app.exec_())