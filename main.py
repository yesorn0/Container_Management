from gui.main_window import Main
from logic.serial_bt import *
from logic.data_handler import *
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    print("raspi start")
    
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    
    # DB 저장 스레드
    db_thread_start()
    
    sys.exit(app.exec_())