import sys
import random
import os

from gui.control_ui import Ui_MainWindow
from logic.serial_bt import bt_thread_start, return_receDATA
from logic.serial_bt import ser
from logic.csv_open import open_csv_folder
from logic.camera_manager import CameraManager, check_and_kill_video0
from logic.log_handler import append_log as external_append_log
from logic.status_check import check_status
from logic.graph_manager import *
from logic.threshold_table import setup_threshold_table

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QVBoxLayout, QLineEdit, QTextEdit, QTableWidgetItem, QSizePolicy, QHeaderView
)
from PyQt5.QtCore import QTimer, Qt, QDateTime
from PyQt5.QtGui import QColor, QImage, QPixmap
    
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # --- csv 저장 폴더 열기 ---
        self.ui.csv_open.triggered.connect(lambda: open_csv_folder())

        # --- /dev/video0 이 이미 실행 중이면 강제 종료 ---
        check_and_kill_video0()
        
        # --- 멤버 변수 초기화 ---
        self.box_select = 1
        self.temp_thresh = [25, 25]
        self.humi_thresh = [20, 20]
        
        # --- 데이터 버퍼 초기화 ---
        self.temp1_data = []
        self.humi1_data = []
        self.temp2_data = []
        self.humi2_data = []
        
        # --- cmd 관련 변수 초기화 ---
        self.cmd = ' '
        self.warning_counter = 0
        self.warning_interval = 6

        # --- cmd_log를 읽기 전용으로 설정 ---
        self.ui.cmd_log.setReadOnly(True)
        
        # Bluetooth 수신 스레드 시작
        bt_thread_start()
        
        # --- 그래프 만들기 (왼쪽: matplotlib / 오른쪽: pyqtgraph) ---
        self.ax1, self.canvas1 = matplotlib_init(self.ui.chart_1)
        self.pg_plot = pyqtgraph_init(self.ui.chart_2)


        # bar chart 만들기
        self.bar_plot, self.bar_left, self.bar_right = setup_bar_chart(self.ui.bar_chart)
        
        # --- ComboBox 설정 ---
        self.ui.box_select.addItems(["Container 1", "Container 2"])
        self.ui.box_select.currentIndexChanged.connect(self.change_box_selection)
        
        # --- Temp, Humi 경계값 버튼 연결 ---
        self.ui.btn_temp.clicked.connect(self.send_temp_value)
        self.ui.btn_humi.clicked.connect(self.send_humi_value)
        
        # --- threshold 표 만들기 ---
        setup_threshold_table(self.ui.threshold_table, self.temp_thresh, self.humi_thresh)

        # --- Command Line 엔터 입력 연결 ---
        self.ui.cmd_line.returnPressed.connect(self.send_command)

        # --- GUI 갱신용 타이머 ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(500)  # 1초마다 갱신
        
        # --- Status Bar DateTime ---
        self.setup_status_bar()
        
        # --- Camera Widget ---
        self.camera = CameraManager(self, log_callback=self.append_log)
        self.ui.camera_view.triggered.connect(self.camera.start_camera_view)

    def update_status(self):
        # --- 블루투스 수신 데이터 가져오기 ---
        rece_data = return_receDATA()
        if rece_data is None or any(v is None for v in rece_data):
            return  # 아직 데이터가 안 왔으면 skip

        T1, H1, T2, H2, F, LW, RW = rece_data
    
        # 데이터 추가
        self.temp1_data.append(T1)
        self.humi1_data.append(H1)
        self.temp2_data.append(T2)
        self.humi2_data.append(H2)
        
        # 30개까지만 유지
        if len(self.temp1_data) > 30: self.temp1_data.pop(0)
        if len(self.humi1_data) > 30: self.humi1_data.pop(0)
        if len(self.temp2_data) > 30: self.temp2_data.pop(0)
        if len(self.humi2_data) > 30: self.humi2_data.pop(0)

        # --- matplotlib 그래프 업데이트 ---
        matplotlib_update(self.ax1, self.canvas1, self.temp1_data, self.humi1_data, container=1)


        # --- pyqtgraph 그래프 업데이트 ---
        pyqtgraph_update(self.pg_plot, self.temp2_data, self.humi2_data, container=2)

        # -- bar chart 그래프 업데이트 ---
        self.bar_left, self.bar_right = update_bar_chart(
            self.bar_plot,
            self.bar_left,
            self.bar_right,
            left_value=LW,
            right_value=RW
        )
        
        # --- 수위 차이 감지 및 홰재 감지 경고 ---
        self.warning_counter = check_status(
            self.ui.cmd_log,
            left_water=LW,
            right_water=RW,
            fire_detect=F,
            warning_counter=self.warning_counter,
            warning_interval=self.warning_interval
        )

    def change_box_selection(self, index):
        self.box_select = index + 1
        # 선택된 box에 맞는 temp/humi 값을 LineEdit에 표시
        self.ui.line_temp.setText(str(self.temp_thresh[self.box_select-1]))
        self.ui.line_humi.setText(str(self.humi_thresh[self.box_select-1]))

    def send_temp_value(self):
        # Temp 전송 버튼 클릭 시 로그 기록
        self.temp_thresh[self.box_select-1] = int(self.ui.line_temp.text())
        self.append_log(f"[TEMP container {self.box_select}] {self.temp_thresh[self.box_select-1]} 전송 완료")
        # Bluetooth로 temp 값을 전송
        send_str = f"T{self.box_select}:{self.temp_thresh[self.box_select-1]:02d}\n"
        ser.write(send_str.encode())
        # 테이블 업데이트
        item = QTableWidgetItem(str(self.temp_thresh[self.box_select-1]))
        item.setTextAlignment(Qt.AlignCenter)
        self.ui.threshold_table.setItem(2, (self.box_select-1)*2, item)

    def send_humi_value(self):
        # Humi 전송 버튼 클릭 시 로그 기록
        self.humi_thresh[self.box_select-1] = int(self.ui.line_humi.text())
        self.append_log(f"[HUMI container {self.box_select}] {self.humi_thresh[self.box_select-1]} 전송 완료")
        # Bluetooth로 humi 값도 전송
        send_str = f"H{self.box_select}:{self.humi_thresh[self.box_select-1]:02d}\n"
        ser.write(send_str.encode())
        # 테이블 업데이트
        item = QTableWidgetItem(str(self.humi_thresh[self.box_select-1]))
        item.setTextAlignment(Qt.AlignCenter)
        self.ui.threshold_table.setItem(2, (self.box_select-1)*2 + 1, item)

    def send_command(self):
        # Command 입력 후 Enter 시 로그 기록
        self.cmd = self.ui.cmd_line.text()
        if self.cmd:
            self.append_log(f"> {self.cmd}")
            self.ui.cmd_line.clear()

    def append_log(self, text):
            external_append_log(self.ui.cmd_log, text)    
        
    def setup_status_bar(self):
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_status_bar_time)
        self.time_timer.start(1000)  # 1초마다 갱신

    def update_status_bar_time(self):
        now = QDateTime.currentDateTime()
        time_text = now.toString("yyyy-MM-dd hh:mm:ss")
        self.statusBar().showMessage(time_text)