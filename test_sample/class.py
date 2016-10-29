

from PyQt5.QtWidgets import *
import sys

def main():
	app = QApplication(sys.argv)
	
	w = QWidget()
	bb = [QPushButton, QCheckBox]	# クラスの配列
	b = bb[1]("test", w)			# インスタンス化
	w.show()
	
	sys.exit(app.exec_() )

if __name__ == '__main__':
	main()