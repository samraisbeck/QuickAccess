from PySide import QtCore, QtGui
import yaml
from subprocess import *
import os, sys

class WidgetInternet(QtGui.QWidget):
    def __init__(self, parent=None):
        super(WidgetInternet, self).__init__(parent)
        self.history = []
        self.readHistory()
        self._initUI()

    def _initUI(self):
        hbox = QtGui.QHBoxLayout()
        self.urlText = QtGui.QLineEdit()
        self.urlText.setPlaceholderText('www.google.ca')
        self.urlText.setToolTip('Enter a URL or click Launch to go to Google.')
        self._updateTextCompletion()
        self.connect(self.urlText, QtCore.SIGNAL('returnPressed()'), self.launchInternet)
        self.secretCheck = QtGui.QCheckBox('Incognito?', parent=self)
        self.secretCheck.setChecked(False)
        self.secretCheck.setToolTip('Launch incognito (Chrome only)')
        hbox.addWidget(self.secretCheck)
        hbox.addWidget(self.urlText, parent=self)
        button = QtGui.QPushButton('Launch', parent=self)
        button.clicked.connect(self.launchInternet)
        hbox.addWidget(button)
        self.setLayout(hbox)

    def _updateTextCompletion(self):
        # Can't seem to find a way to just add items to the completer or change the
        # list of strings it contains. So, just overwrite it I guess
        completer = QtGui.QCompleter([item[0] for item in self.history], parent=self)
        # completer.setCompletionMode(QtGui.QCompleter.InlineCompletion)
        self.urlText.setCompleter(completer)

    def launchInternet(self):
        urlBase = self.urlText.text()
        if not 'https' in urlBase:
            url = 'https://'+urlBase
        if url == 'https://':
            urlBase = 'google.ca'
            url = 'https://google.ca'
        if (not '.' in urlBase) or (' ' in urlBase):
            searchStr = ''
            for char in urlBase:
                if char == ' ':
                    searchStr += '+'
                else:
                    searchStr += char
            urlBase = 'google.ca' # for history purposes
            url = 'https://'+urlBase+'/search?q='+searchStr
        if self.secretCheck.isChecked():
            try:
                os.system('start chrome '+url+' --incognito')
            except:
                print 'Chrome not installed! Can\'t go incognito'
            pass
        else:
            try:
                os.system('start '+url)
                self.addToHistory(urlBase)
            except:
                raise

    def addToHistory(self, urlBase):
        """I don't mind having to loop through even if history gets big,
        because if the user launches a program, this adding to history process is
        basically taking place in the background.
        I originally intended to use a dictionary for the history but realized they
        are unordered and to make the URL completion easy, it should be in order."""
        index = -1
        affectedCompletion = False
        for i in range(len(self.history)):
            if self.history[i][0] == urlBase:
                self.history[i][1] += 1
                index = i
                break
        if index == -1:
            self.history.append([urlBase, 1])
            affectedCompletion = True
        else:
            _range = range(index)
            # We only check history entries before the one we just added, since the
            # ones after will all have less hits
            for i in reversed(_range):
                if self.history[i][1] < self.history[index][1]:
                    temp = self.history[i]
                    self.history[i] = self.history[index]
                    self.history[index] = temp
                    index = i
                    affectedCompletion = True
        if affectedCompletion:
            self._updateTextCompletion()

    def clearHistory(self):
        confirmed = QtGui.QMessageBox.question(self, 'Confirmation', 'Are you sure you want to clear the history? You\n'+\
                                               ' will lose the autocompletion data.', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if confirmed == QtGui.QMessageBox.Yes:
            try:
                # This will make an empty history file if none is there
                f = open('history.txt', 'w')
                f.close()
                self.history = []
                self._updateTextCompletion()
            except:
                print 'Something went wrong. Nothing should go wrong here...\n\n'
                raise

    def readHistory(self):
        try:
            with open('history.txt', 'r') as f:
                for line in f:
                    for word in line.split():
                        try:
                            occur = int(word)
                            self.history.append([url, occur])
                        except ValueError:
                            # expected value error
                            url = word
            f.close()
        except IOError:
            print 'No history file! One will be made after you search your first website.'
