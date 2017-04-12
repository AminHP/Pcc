#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build'))

from PyQt4 import QtCore, QtGui
from mainwindow import Ui_MainWindow

from manager import Manager


app = QtGui.QApplication(sys.argv)
mainwindow = QtGui.QMainWindow()
ui_mainwindow = Ui_MainWindow()
ui_mainwindow.setupUi(mainwindow)

manager = Manager(ui_mainwindow, mainwindow)
manager.run()

sys.exit(app.exec_())
