from functools import partial

from PyQt4 import QtCore, QtGui
from mainwindow import _fromUtf8

from pcc import run


class Manager:
    def __init__(self, ui_mainwindow, mainwindow):
        self.ui_mainwindow = ui_mainwindow
        self.ui_mainwindow.window = mainwindow


    def actionOpen_cliecked(self):
        code_path = QtGui.QFileDialog.getOpenFileName(
            self.ui_mainwindow.window,
            'Open Code',
            filter = '*.c'
        )
        with open(code_path) as f:
            self.ui_mainwindow.codeTextEdit.setText(f.read())


    def actionCompile_cliecked(self):
        code = self.ui_mainwindow.codeTextEdit.toPlainText()
        if code:
            tokens, lexical_errors = run(code)

            self.ui_mainwindow.tokenListWidget.clear()
            self.ui_mainwindow.lexerrListWidget.clear()

            for token in tokens:
                text = "%s:%s: %s" % (token.line, token.column, token.text)
                self.ui_mainwindow.tokenListWidget.addItem(text)
            for error in lexical_errors:
                self.ui_mainwindow.lexerrListWidget.addItem(error.error_msg)



    def run(self):
        self.ui_mainwindow.actionOpen.triggered.connect(self.actionOpen_cliecked)
        self.ui_mainwindow.actionCompile.triggered.connect(self.actionCompile_cliecked)

        self.ui_mainwindow.window.show()
