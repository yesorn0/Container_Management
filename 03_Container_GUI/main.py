import sys
from control_ui import Ui_MainWindow
from PyQt5.QtWidgets import (
	QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QLineEdit, QTextEdit
)

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # --- 그래프 만들기 ---
        
        # --- 버튼 시그널 연결 ---
        
if __name__ == "__main__":
    app = QApplication([])
    window = Main()
    window.show()
    app.exec()