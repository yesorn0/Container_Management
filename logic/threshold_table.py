from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView

def setup_threshold_table(table_widget, temp_thresh, humi_thresh):
    # --- 테이블 기본 설정 ---
    table_widget.setRowCount(3)
    table_widget.setColumnCount(4)

    # --- 1행 병합 (Container1 / Container2) ---
    table_widget.setSpan(0, 0, 1, 2)
    table_widget.setSpan(0, 2, 1, 2)

    # --- 1행: Container 타이틀 ---
    table_widget.setItem(0, 0, QTableWidgetItem("Container 1"))
    table_widget.setItem(0, 2, QTableWidgetItem("Container 2"))

    # --- 2행: Temp, Humi 타이틀 ---
    table_widget.setItem(1, 0, QTableWidgetItem("Temp"))
    table_widget.setItem(1, 1, QTableWidgetItem("Humi"))
    table_widget.setItem(1, 2, QTableWidgetItem("Temp"))
    table_widget.setItem(1, 3, QTableWidgetItem("Humi"))

    # --- 3행: 실제 Threshold 값 ---
    table_widget.setItem(2, 0, QTableWidgetItem(str(temp_thresh[0])))
    table_widget.setItem(2, 1, QTableWidgetItem(str(humi_thresh[0])))
    table_widget.setItem(2, 2, QTableWidgetItem(str(temp_thresh[1])))
    table_widget.setItem(2, 3, QTableWidgetItem(str(humi_thresh[1])))

    # --- 가운데 정렬 ---
    for row in range(3):
        for col in range(4):
            item = table_widget.item(row, col)
            if item:
                item.setTextAlignment(Qt.AlignCenter)
    
    # 0번째 행 (Container 1, Container 2) 색상 바꾸기
    for col in range(4):
        item = table_widget.item(0, col)
        if item:
            item.setBackground(QColor("#555555"))  # 짙은 회색 배경

    # --- 크기 정책: 테이블이 GUI 크기에 맞게 커지도록 ---
    sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    table_widget.setSizePolicy(sizePolicy)

    # --- 헤더 숨기기 ---
    table_widget.horizontalHeader().setVisible(False)
    table_widget.verticalHeader().setVisible(False)

    # --- 모든 열을 Stretch (균등분할) ---
    table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # --- 스크롤바 끄기 (깔끔하게) ---
    table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)