import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table Test")
        self.setGeometry(100, 100, 500, 300)

        # 예시 temp_thresh, humi_thresh
        self.temp_thresh = [25, 30]
        self.humi_thresh = [60, 55]

        self.setup_table()

    def setup_table(self):
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setGeometry(50, 50, 400, 150)  # 위치(x,y) + 크기(w,h)

        # --- 병합 설정 (Container 1, Container 2) ---
        self.tableWidget.setSpan(0, 0, 1, 2)
        self.tableWidget.setSpan(0, 2, 1, 2)

        # --- 1행 Container 이름 ---
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Container 1"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("Container 2"))

        # --- 2행 Temp, Humi 텍스트 ---
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Temp"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("Humi"))
        self.tableWidget.setItem(1, 2, QTableWidgetItem("Temp"))
        self.tableWidget.setItem(1, 3, QTableWidgetItem("Humi"))

        # --- 3행 Threshold 값 표시 ---
        self.tableWidget.setItem(2, 0, QTableWidgetItem(str(self.temp_thresh[0])))
        self.tableWidget.setItem(2, 1, QTableWidgetItem(str(self.humi_thresh[0])))
        self.tableWidget.setItem(2, 2, QTableWidgetItem(str(self.temp_thresh[1])))
        self.tableWidget.setItem(2, 3, QTableWidgetItem(str(self.humi_thresh[1])))

        # --- 헤더 숨기기 ---
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)

        # --- 셀 가운데 정렬 ---
        for row in range(3):
            for col in range(4):
                item = self.tableWidget.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())
