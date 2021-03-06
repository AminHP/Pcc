from functools import partial

from PyQt4 import QtCore, QtGui
from mainwindow import _fromUtf8

from pcc import run
import highlighter

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
        h = highlighter.CHighlighter (self.ui_mainwindow.codeTextEdit.document())

        with open(code_path) as f:
            self.ui_mainwindow.codeTextEdit.setPlainText(f.read())


    def actionCompile_cliecked(self):
        code = self.ui_mainwindow.codeTextEdit.toPlainText()
        name = str(self.ui_mainwindow.nameLineEdit.text())

        if code:
            tokens, lexical_errors, parsing_errors, convert_error = run(code, name)

            if convert_error:
                msg = QtGui.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText(str(convert_error))
                msg.setStandardButtons(QtGui.QMessageBox.Ok)
                msg.exec_()
            else:

                self.ui_mainwindow.tokenListWidget.clear()
                self.ui_mainwindow.lexerListWidget.clear()
                self.ui_mainwindow.parserListWidget.clear()

                for (sym, token) in tokens:
                    text = "%s:%s: %s -> %s" % (token.line, token.column, sym, token.text)
                    self.ui_mainwindow.tokenListWidget.addItem(text)
                for error in lexical_errors:
                    self.ui_mainwindow.lexerListWidget.addItem(error.error_msg)
                for error in parsing_errors:
                    self.ui_mainwindow.parserListWidget.addItem(error.error_msg)



    def run(self):
        self.ui_mainwindow.actionOpen.triggered.connect(self.actionOpen_cliecked)
        self.ui_mainwindow.actionCompile.triggered.connect(self.actionCompile_cliecked)

        self.ui_mainwindow.window.show()
