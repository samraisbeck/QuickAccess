from PySide import QtCore, QtGui
import yaml
from subprocess import *
import os, sys
from widgetInternet import WidgetInternet

class ProgramManager(QtGui.QMainWindow):
    def __init__(self):
        super(ProgramManager, self).__init__()
        self.programs = None
        self.keys = []
        self.readConfig()
        self._InternetOptions = WidgetInternet(parent=self)
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
        grid = QtGui.QGridLayout()
        self._createToolbar()

        label = QtGui.QLabel('QuickAccess', parent=self)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(13)
        label.setFont(font)
        grid.addWidget(label, 0, 0, alignment=QtCore.Qt.AlignHCenter)

        grid.addWidget(self._InternetOptions, 1, 0, alignment=QtCore.Qt.AlignHCenter)

        separator = QtGui.QFrame()
        separator.setFrameShape(QtGui.QFrame.HLine)
        separator.setFrameShadow(QtGui.QFrame.Sunken)
        grid.addWidget(separator, 2, 0)

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

    def _createToolbar(self):
        m = QtGui.QMenu('Options', parent=self)
        option = QtGui.QAction('View History', m)
        # option.setShortcut('Ctrl+H')
        option.setStatusTip('View URL history.')
        option.triggered.connect(self.viewHistory)
        m.addAction(option)

        option = QtGui.QAction('Delete History', m)
        # option.setShortcut('Ctrl+L')
        option.setStatusTip('Delete current URL history.')
        option.triggered.connect(self._InternetOptions.clearHistory)
        m.addAction(option)

        self.menuBar().addMenu(m)

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

    def viewHistory(self):
        history = self._InternetOptions.history
        grid = QtGui.QGridLayout()
        grid.addWidget(QtGui.QLabel('URL History', parent=None),0, 0, alignment=QtCore.Qt.AlignHCenter)
        edit = QtGui.QTextEdit(parent=None)
        edit.setReadOnly(True)
        editStr = ''
        if len(history) == 0:
            editStr += 'History is empty!'
        for item in history:
            editStr += item[0]+' -> '+str(item[1])+'\n'
        edit.setText(editStr)
        grid.addWidget(edit)
        Qw = QtGui.QWidget(parent=self)
        Qw.setLayout(grid)
        Qw.setWindowFlags(QtCore.Qt.Window)
        Qw.show()

    def closeEvent(self, event):
        history = self._InternetOptions.history
        if not history == []:
            with open('history.txt', 'w') as f:
                for item in history:
                    f.write(item[0]+' '+str(item[1])+'\n')
                f.close()
        super(ProgramManager, self).closeEvent(event)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = ProgramManager()
    app.exec_()
