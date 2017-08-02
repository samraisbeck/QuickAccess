from PySide import QtCore, QtGui
import yaml
from subprocess import *
import os, sys

class ProgramManager(QtGui.QMainWindow):
    def __init__(self):
        super(ProgramManager, self).__init__()
        self.programs = None
        self.keys = []
        self.readConfig()
        self._initUI()

    def readConfig(self):
        try:
            with open('config.yaml', 'r') as f:
                try:
                    self.programs = yaml.safe_load(f)
                except yaml.YAMLError:
                    print 'Could not read config.yaml.'
                    raise
        except IOError:
            print 'Could not find the config.yaml file.'
            raise
        if self.programs is not None:
            self.keys = self.programs.keys()


    def _initUI(self):
        if self.programs == None:
            print 'No programs configured. Exiting...'
            sys.exit(0)
        cols = 3
        label = QtGui.QLabel('QuickAccess for Windows', parent=self)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(13)
        label.setFont(font)
        grid = QtGui.QGridLayout()
        grid.addWidget(label, 0, 0, alignment=QtCore.Qt.AlignHCenter)
        hbox = QtGui.QHBoxLayout()
        self.urlText = QtGui.QLineEdit()
        self.urlText.setPlaceholderText('www.google.ca')
        self.urlText.setToolTip('Enter a URL or click Launch to go to Google.')
        self.connect(self.urlText, QtCore.SIGNAL('returnPressed()'), self.launchInternet)
        self.secretCheck = QtGui.QCheckBox('Incognito?', parent=self)
        self.secretCheck.setChecked(False)
        self.secretCheck.setToolTip('Launch incognito (Chrome only)')
        hbox.addWidget(self.secretCheck)
        hbox.addWidget(self.urlText, parent=self)
        button = QtGui.QPushButton('Launch', parent=self)
        button.clicked.connect(self.launchInternet)
        hbox.addWidget(button)
        grid.addLayout(hbox, 1, 0, alignment=QtCore.Qt.AlignHCenter)
        separator = QtGui.QFrame()
        separator.setFrameShape(QtGui.QFrame.HLine)
        separator.setFrameShadow(QtGui.QFrame.Sunken)
        grid.addWidget(separator, 2, 0, 1, cols)
        buttonGrid = QtGui.QGridLayout()
        for i in range(len(self.programs)):
            button = QtGui.QPushButton(self.keys[i], parent=self)
            self.connect(button, QtCore.SIGNAL('pressed()'), self.launchProgram)
            buttonGrid.addWidget(button, i/cols, i%cols)
        grid.addLayout(buttonGrid, 3, 0)
        Qw = QtGui.QWidget()
        Qw.setLayout(grid)
        self.setCentralWidget(Qw)
        self.setWindowTitle('QuickAccess for '+os.environ['USERNAME']+' on '+os.environ['COMPUTERNAME'])
        self.show()

    def launchProgram(self):
        button = self.sender()
        text = button.text()
        try:
            if self.programs[text][-3:] == '.py':
                Popen([sys.executable, self.programs[text]], cwd = os.path.dirname(self.programs[text]))
            elif os.sep[0] in self.programs[text]:
            # this is the case where we give something you would double click to start, like an executable
                Popen([self.programs[text]], cwd = os.path.dirname(self.programs[text]))
            else:
            # this is the case where we give a program name like "chrome".
                os.system("start "+self.programs[text])
        except:
            print "Could not open "+self.programs[text]
            raise

    def launchInternet(self):
        url = self.urlText.text()
        if not 'https' in url:
            url = 'https://'+url
        if url == 'https://':
            url = 'https://google.ca'
        if self.secretCheck.isChecked():
            try:
                os.system('start chrome '+url+' --incognito')
            except:
                print 'Chrome not installed! Can\'t go incognito'
        else:
            try:
                os.system('start '+url)
            except:
                raise

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = ProgramManager()
    app.exec_()
