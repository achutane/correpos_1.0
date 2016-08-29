#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.initUI()
        
    def initUI(self):               
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QTextEditSample')    

        self.w = QWidget()

        label = QLabel('履歴:')
        self.text = QTextEdit(self)
        hbox =QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(self.text)

        self.w.setLayout(hbox)
        self.setCentralWidget(self.w)

        self.timer = QTimer()
        QObject.connect(self.timer,SIGNAL("timeout()"),self.countup)
        self.timer.start(1000)

        self.show()

    def countup(self):
        self.text.append("a")

def main():
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()