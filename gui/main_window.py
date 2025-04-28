import sys
import random
from gui.control_ui import Ui_MainWindow
from logic.serial_bt import bt_thread_start, return_receDATA
from logic.serial_bt import ser

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QVBoxLayout, QLineEdit, QTextEdit
)
from PyQt5.QtCore import QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import pyqtgraph as pg 
from pyqtgraph import PlotWidget, BarGraphItem

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # --- 멤버 변수 초기화 ---
        self.box_select = 1
        self.temp_thresh = [0, 0]
        self.humi_thresh = [0, 0]
        
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
        self.setup_graphs()

        # bar chart 만들기
        self.setup_bar_chart()
        
        # --- ComboBox 설정 ---
        self.ui.box_select.addItems(["Container 1", "Container 2"])
        self.ui.box_select.currentIndexChanged.connect(self.change_box_selection)
        
        # --- Temp, Humi 경계값 버튼 연결 ---
        self.ui.btn_temp.clicked.connect(self.send_temp_value)
        self.ui.btn_humi.clicked.connect(self.send_humi_value)

        # --- Command Line 엔터 입력 연결 ---
        self.ui.cmd_line.returnPressed.connect(self.send_command)

        # --- GUI 갱신용 타이머 ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(500)  # 1초마다 갱신

    def setup_graphs(self):
        # QWidget 안에 matplotlib 추가
        self.fig = Figure(figsize=(5,4))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        layout1 = QVBoxLayout(self.ui.chart_1)
        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.addWidget(self.canvas)

        # QWidget 안에 pyqtgraph 추가
        self.pg_plot = pg.PlotWidget()
        self.pg_plot.addLegend(offset=(10, 10))
        self.pg_plot.showGrid(x=True, y=True, alpha=0.3)
        self.pg_plot.setYRange(0, 70)  # y축 고정

        layout2 = QVBoxLayout(self.ui.chart_2)
        layout2.setContentsMargins(0, 0, 0, 0)
        layout2.addWidget(self.pg_plot)

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
        self.ax.clear()
        self.ax.plot(self.temp1_data, label='Temp1', color='orange')
        self.ax.plot(self.humi1_data, label='Humi1', color='cyan')
        self.ax.set_ylim(0, 70)
        self.ax.legend(loc='upper left')
        self.ax.set_title('Sensor 1 Random')
        self.canvas.draw()

        # --- pyqtgraph 그래프 업데이트 ---
        self.pg_plot.clear()
        x = list(range(len(self.temp2_data)))
        self.pg_plot.plot(x, self.temp2_data, pen='r', name='Temp2')
        self.pg_plot.plot(x, self.humi2_data, pen='b', name='Humi2')
        
        # -- bar chart 그래프 업데이트 ---
        self.update_bar_chart(LW, RW)
        
        # --- 수위 차이 감지 및 홰재 감지 경고 ---
        self.check_status(LW, RW, F)

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

    def send_humi_value(self):
        # Humi 전송 버튼 클릭 시 로그 기록
        self.humi_thresh[self.box_select-1] = int(self.ui.line_humi.text())
        self.append_log(f"[HUMI container {self.box_select}] {self.humi_thresh[self.box_select-1]} 전송 완료")
        # ✅ Bluetooth로 humi 값도 전송
        send_str = f"H{self.box_select}:{self.humi_thresh[self.box_select-1]:02d}\n"
        ser.write(send_str.encode())
        
    def send_command(self):
        # Command 입력 후 Enter 시 로그 기록
        self.cmd = self.ui.cmd_line.text()
        if self.cmd:
            self.append_log(f"> {self.cmd}")
            self.ui.cmd_line.clear()

    def append_log(self, text):
        # 로그창에 텍스트 추가 및 스크롤 최하단 이동
        current_log = self.ui.cmd_log.toHtml()
        
        # 만약 'Warning' 들어있으면 빨간색
        if '[Warning]' in text:
            new_line = f'<span style="color:red;">{text}</span><br>'
        elif '[Caution]' in text:
            new_line = f'<span style="color:yellow;">{text}</span><br>'
        else:
            new_line = f'<span style="color:white;">{text}</span><br>'
            
        updated_log = current_log + new_line
        self.ui.cmd_log.setHtml(updated_log)
        
        self.ui.cmd_log.verticalScrollBar().setValue(self.ui.cmd_log.verticalScrollBar().maximum())
        
    def setup_bar_chart(self):
        self.bar_plot = PlotWidget()

        # 배경 검정, 좌표계 제거
        self.bar_plot.setBackground('black')
        self.bar_plot.showAxis('left', False)
        self.bar_plot.showAxis('bottom', False)
        self.bar_plot.setMouseEnabled(x=False, y=False)
        self.bar_plot.setMenuEnabled(False)
        self.bar_plot.hideButtons()

        # 범위 설정
        self.bar_plot.setYRange(0, 2500)
        self.bar_plot.setXRange(-2, 2)

        layout = QVBoxLayout(self.ui.bar_chart)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.bar_plot)

        # Bar 초기화 (빈 채로 시작)
        self.bar_left = None
        self.bar_right = None
            
    def update_bar_chart(self, left_value, right_value):
        # 기존 bar 제거
        if self.bar_left:
            self.bar_plot.removeItem(self.bar_left)
        if self.bar_right:
            self.bar_plot.removeItem(self.bar_right)

        # 새로운 bar 추가
        self.bar_left = BarGraphItem(x=[-1], height=[left_value], width=0.6, brush='blue')
        self.bar_right = BarGraphItem(x=[1], height=[right_value], width=0.6, brush='red')

        self.bar_plot.addItem(self.bar_left)
        self.bar_plot.addItem(self.bar_right)
    
    def check_status(self, left_water, right_water, Fire_detect):
        # 처음이거나, 20회마다 한 번 출력
        self.warning_counter += 1
        
        if self.warning_counter == 1 or self.warning_counter >= self.warning_interval:
            self.warning_counter = 1
            diff = abs(left_water - right_water)
        
            if diff >= 1000:
                if left_water > right_water:  self.append_log(f"[Warning] Left Side High !!!")
                else :                        self.append_log(f"[Warning] Right Side High !!!")
            elif diff >= 300:
                if left_water > right_water:  self.append_log(f"[Caution] Left Side High !!!")
                else :                        self.append_log(f"[Caution] Right Side High !!!")
            else:
                pass
            
            if Fire_detect == 1: self.append_log("[Warning] Fire Detected!")