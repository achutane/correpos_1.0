#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QApplication
from PyQt5.QtCore import QCoreApplication

APPNAME = "CORREPOS"
VERSION = "0.0.1"

WINDOW_W = 800
WINDOW_H = 600


class myWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle(APPNAME)
		self.move(300,100)
		self.setFixedSize(WINDOW_W, WINDOW_H)

		button = QPushButton("a", self)
		button.resize(button.sizeHint() )
		button.clicked.connect(QCoreApplication.instance().quit)
		button.move(50,50)


		self.show()


def main():
	app = QApplication(sys.argv)

	initWindow = myWindow()

	sys.exit(app.exec_())



if __name__ == '__main__':
	main()