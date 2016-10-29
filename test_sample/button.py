
from PyQt5.QtWidgets import *
import sys

class MyButton(QPushButton):
	def __init__(self, *args):
		super().__init__(*args)
		self.parent = args[1]
		self.clicked.connect( self.pushed )
		
	def pushed(self):
		a = QPushButton("test", self.parent)
		a.move(300,300)
		a.resize(100,100)
		a.show()
		self.parent.adjustSize()
	

def main():
	app = QApplication(sys.argv)
	
	w = QWidget()
	b = MyButton("close", w)
	w.show()
	
	sys.exit(app.exec_() )

if __name__ == '__main__':
	main()