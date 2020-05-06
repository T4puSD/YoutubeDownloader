from gui_template import Ui_MainWindow
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
class YoutubeGui(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super(YoutubeGui,self).__init__(parent=parent, flags=flags)
        # self.setupUi(self)
        self.actionExit.triggered.connect(self.exitApp)
    
    def exitApp(self):
        sys.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = YoutubeGui()
    form.show()
    app.exec_()