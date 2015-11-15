# -*- coding: utf-8 -*-

import logging

# PySide is my GUI (and your too)
from PySide import QtCore
from PySide import QtGui

from libs import data


class MainWindow(QtGui.QMainWindow):
    # create window, controls, set properties, etc.
    def __init__(self):
        self.temp=False
        logging.info('create MainWindow')
        super(MainWindow, self).__init__(None)
        self.setWindowTitle(u'Pharmacy')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        # disable resizing
        self.setFixedSize(self.sizeHint())

        # create main layout
        self.layout = QtGui.QGridLayout()
        central_widget = QtGui.QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        self.data = data.DataProvider()

        logging.info('MainWindow created')

    def __del__(self):
        del self.data

if __name__ == '__main__':
    # create Qt Application and show GUI
    app = QtGui.QApplication([])
    main_window = MainWindow()
    main_window.show()
    logging.info('execute QApplication')
    app.exec_()

    # need to destroy QApplication
    # Unset main window also just to be safe

    logging.info('destroy QApplication and QMainWindow')
    del main_window
    del app
    logging.info('exit')


