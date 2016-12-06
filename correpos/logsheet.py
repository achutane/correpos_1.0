from sheet import sheet
import config
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import datetime
import pyaudio
import wave
import cv2
import math
import copy
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

class logSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
     # 映像表示

        self.log_w = QWidget(self)

        self.monthbutton = QPushButton("今月",self)
        self.monthbutton.move(30,50)
        self.monthbutton.clicked.connect(self.on_clicked_backtomonth)

        self.daybutton = QPushButton("今日",self)
        self.daybutton.move(180,50)
        self.daybutton.clicked.connect(self.on_clicked_backtoday)

        self.changebutton = QPushButton("指定に変更",self)
        self.changebutton.move(230,6)
        self.changebutton.resize(100,25)
        self.changebutton.clicked.connect(self.on_clicked_change)

        font = QFont()
        font.setPointSize(18)
        font1 = QFont()
        font1.setPointSize(13)
        self.yearLabel = QLabel(self)
        self.monthLabel = QLabel(self)
        self.dayLabel = QLabel(self)

        self.yearLabel.setText("年")
        self.yearLabel.setFont(font1)
        #self.yearLabel.move(65, 15)
        self.monthLabel.setText("月")
        self.monthLabel.setFont(font1)
        #self.monthLabel.move(125, 15)
        self.dayLabel.setText("日")
        self.dayLabel.setFont(font1)
        #self.dayLabel.move(180, 15)

        self.combo_y = QComboBox(self)
        #self.combo_y.move(10,10)
        self.combo_m = QComboBox(self)
        #self.combo_m.move(85,10)
        self.combo_d = QComboBox(self)
        #self.combo_d.move(140,10)

        for var in range(2016,2050):
            self.combo_y.addItem(str(var))

        for var in range(1,13):
            self.combo_m.addItem(str(var))

        for var in range(0,31):
            self.combo_d.addItem(str(var))    
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.combo_y)
        self.hbox.addWidget(self.yearLabel)
        self.hbox.addWidget(self.combo_m)
        self.hbox.addWidget(self.monthLabel)
        self.hbox.addWidget(self.combo_d)
        self.hbox.addWidget(self.dayLabel)
        #self.hbox.addWidget(self.changebutton)
        self.log_w.setLayout(self.hbox)

        
        self.logLabel = QLabel(self)
        self.logLabel.move(570, 15)
        self.logLabel.resize(200,20)
        self.logLabel.setFont(font1)

        self.logLabel2 = QLabel(self)
        self.logLabel2.setFont(font)
        self.logLabel2.move(60, 90)
        #self.logLabel2.setColor(QColor(255, 0, 0))
        #self.logLabel2.setText("<font size= "18" color="white"> <b> </b></font>");

        self.logLabel3 = QLabel(self)
        self.logLabel3.setFont(font)
        self.logLabel3.move(40, 450)

        self.dpi = 55
        self.fig = Figure((13,8), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)
        self.canvas.move(300,40)
        self.canvas.setVisible(False)

        self.noticeLabel = QLabel(self)
        self.noticeLabel.move(0,130)
        #self.noticeLabel.resize(10,10)
        self.pmap1 = QPixmap("fig1.png")
        self.pmap2 = QPixmap("fig2.png")
        self.pmap3 = QPixmap("fig3.png")
        
        #self.noticeLabel.setPixmap(self.pmap3)


    def on_clicked_change(self):

        count = 0 
        count1 = 0
        self.countarray_day = np.array([0]*24)
        self.hour = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
        self.hourlabel = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]

        self.countarray_day1 = np.array([0]*32)
        self.day = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
        self.daylabel = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

        df = pd.read_csv('log.csv')
        df = df['0']
        for var in range(0,len(df.index)-1):
            if (int(self.combo_d.currentText()) == int(pd.to_datetime(df.values[var]).day)) and (int(self.combo_m.currentText()) == int(pd.to_datetime(df.values[var]).month)) and (int(self.combo_y.currentText()) == int(pd.to_datetime(df.values[var]).year)):
                self.countarray_day[int(pd.to_datetime(df.values[var]).hour)] += 1
                count += 1

        for var in range(0,len(df.index)-1):
            if  (int(self.combo_m.currentText()) == int(pd.to_datetime(df.values[var]).month)) and (int(self.combo_y.currentText()) == int(pd.to_datetime(df.values[var]).year)):   
                self.countarray_day1[int(pd.to_datetime(df.values[var]).day)] += 1
                count1 += 1
            
        if (int(self.combo_d.currentText()) == 0):
            self.axes = self.fig.add_subplot(111)   
            self.data = self.countarray_day1
            self.axes.clear()
            self.axes.grid()
            self.axes.bar(self.day,self.data,tick_label = self.daylabel, align = "center",width = 0.4)
            self.axes.set_ylabel("frequency")
            self.axes.set_xlabel("Day")
            self.canvas.draw()
            self.canvas.setVisible(True)
            self.logLabel.setText(str("   "+self.combo_y.currentText())+"年"+str(self.combo_m.currentText())+"月の記録")
            
            if(count1>=50):
                self.noticeLabel.setPixmap(self.pmap3)
                self.logLabel2.setText("この月の総計: "+str(count1)+"  回 ")
                self.logLabel3.setText(" これから頑張っでね！！")
            elif(count1<=20):
                self.noticeLabel.setPixmap(self.pmap1)
                self.logLabel2.setText("この月の総計: "+str(count1)+"  回　")
                self.logLabel3.setText("       よくやった！！　　")
            else:
                self.noticeLabel.setPixmap(self.pmap2)
                self.logLabel2.setText("この月の総計: "+str(count1)+"  回　")
                self.logLabel3.setText("        良い感じ！！     ")

        else:
            self.axes = self.fig.add_subplot(111) 
            self.data = self.countarray_day
            self.axes.clear()
            self.axes.grid()
            self.axes.bar(self.hour,self.data,tick_label = self.hourlabel, align = "center",width = 0.4)
            self.axes.set_ylabel("frequency")
            self.axes.set_xlabel("Time")
            self.canvas.draw()
            self.canvas.setVisible(True)
            
            self.logLabel.setText(str(self.combo_y.currentText())+"年"+str(self.combo_m.currentText())+"月"+str(self.combo_d.currentText())+"日の記録")
            if(count>=5):
                self.noticeLabel.setPixmap(self.pmap3)
                self.logLabel2.setText("この日の総計: "+str(count)+"  回　")
                self.logLabel3.setText(" これから頑張っでね！!")
            elif(count<=2):
                self.noticeLabel.setPixmap(self.pmap1)
                self.logLabel2.setText("この日の総計: "+str(count)+"  回　")
                self.logLabel3.setText("      よくやった！！　　")
            else:
                self.noticeLabel.setPixmap(self.pmap2)
                self.logLabel2.setText("この日の総計: "+str(count)+"  回　")
                self.logLabel3.setText("        良い感じ！！　  ")

    def on_clicked_backtomonth(self):
        self.start() 


    def on_clicked_backtoday(self):

        count =0 
        d = datetime.datetime.today()
        year=d.strftime("%Y")
        month=d.strftime("%m")
        day=d.strftime("%d") 
        self.countarray_day = np.array([0]*24)
        self.hour = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
        self.hourlabel = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
        df = pd.read_csv('log.csv')
        df = df['0']

        for var in range(0,len(df.index)-1):
             if ((d.day == pd.to_datetime(df.values[var]).day) and (d.month == pd.to_datetime(df.values[var]).month) and (d.year == pd.to_datetime(df.values[var]).year)):
                self.countarray_day[pd.to_datetime(df.values[var]).hour] += 1
                count += 1
        self.axes = self.fig.add_subplot(111)
        self.data = self.countarray_day
        self.axes.clear()
        self.axes.grid()
        self.axes.bar(self.hour,self.data,tick_label = self.hourlabel, align = "center",width = 0.4)
        self.axes.set_ylabel("frequency")
        self.axes.set_xlabel("Time")
        self.canvas.draw()
        self.canvas.setVisible(True)
        self.logLabel.setText(year+"年"+month+"月"+day+"日の記録     ")
        
        if(count>=5):
            self.noticeLabel.setPixmap(self.pmap3)
            self.logLabel2.setText("今日の総計: "+str(count)+"  回　　")
            self.logLabel3.setText(" これから頑張っでね！！　")
        elif(count<=2):
            self.noticeLabel.setPixmap(self.pmap1)
            self.logLabel2.setText("今日の総計: "+str(count)+"  回　")
            self.logLabel3.setText("       よくやった！！　　")
        else:
            self.noticeLabel.setPixmap(self.pmap2)
            self.logLabel2.setText("今日の総計: "+str(count)+"  回　")
            self.logLabel3.setText("       良い感じ！！    　")


    def stop(self):
        super().stop()




        
    def start(self):

        super().start()
        count =0 
        d = datetime.datetime.today()
        year=d.strftime("%Y")
        month=d.strftime("%m")
        self.countarray_day = np.array([0]*32)
        self.day = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
        self.daylabel = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
        df = pd.read_csv('log.csv')
        df = df['0']

        for var in range(0,len(df.index)-1):
            if ((d.month == pd.to_datetime(df.values[var]).month) and (d.year == pd.to_datetime(df.values[var]).year)):
                self.countarray_day[pd.to_datetime(df.values[var]).day] += 1
                count += 1
        self.axes = self.fig.add_subplot(111)
        self.data = self.countarray_day
        self.axes.clear()
        self.axes.grid()
        self.axes.bar(self.day,self.data,tick_label = self.daylabel, align = "center",width = 0.4)
        self.axes.set_ylabel("frequency")
        self.axes.set_xlabel("Day")
        self.canvas.draw()
        self.canvas.setVisible(True)
        self.logLabel.setText("   "+year+"年"+month+"月の記録")
        
        if(count>=50):
            self.noticeLabel.setPixmap(self.pmap3)
            self.logLabel2.setText("今月の総計: "+str(count)+" 回　 ")
            self.logLabel3.setText(" これから頑張っでね！！")
        elif(count<=20):
            self.noticeLabel.setPixmap(self.pmap1)
            self.logLabel2.setText("今月の総計: "+str(count)+" 回　　")
            self.logLabel3.setText("        よくやった！！   ")
        else:
            self.noticeLabel.setPixmap(self.pmap2)
            self.logLabel2.setText("今月の総計: "+str(count)+" 回　　")
            self.logLabel3.setText("        良い感じ！！　   ")