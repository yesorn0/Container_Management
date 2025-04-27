import sys
import random
from gui.control_ui import Ui_MainWindow

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
        self.temp_thresh = []
        self.humi_thresh = []
        self.cmd = ' '
        
        # --- 데이터 버퍼 초기화 ---
        self.temp1_data = []
        self.humi1_data = []
        self.temp2_data = []
        self.humi2_data = []

        # --- cmd_log를 읽기 전용으로 설정 ---
        self.ui.cmd_log.setReadOnly(True)
        
        # --- 그래프 만들기 (왼쪽: matplotlib / 오른쪽: pyqtgraph) ---
        self.setup_graphs()

        # bar chart 만들기
        self.setup_bar_chart()
        
        # --- Temp, Humi 경계값 버튼 연결 ---
        self.ui.btn_temp.clicked.connect(self.send_temp_value)
        self.ui.btn_humi.clicked.connect(self.send_humi_value)

        # --- Command Line 엔터 입력 연결 ---
        self.ui.cmd_line.returnPressed.connect(self.send_command)

        # --- 그래프 갱신용 타이머 ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graphs)
        self.timer.start(1000)  # 1초마다 갱신

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

    def update_graphs(self):
        # --- 새로운 센서 데이터 생성 (임의) ---
        new_temp1 = random.uniform(20, 30)
        new_humi1 = random.uniform(40, 60)
        new_temp2 = random.uniform(20, 30)
        new_humi2 = random.uniform(40, 60)

        self.temp1_data.append(new_temp1)
        self.humi1_data.append(new_humi1)
        self.temp2_data.append(new_temp2)
        self.humi2_data.append(new_humi2)
        
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
        left = random.uniform(0, 100)    # -50도 ~ 50도
        right = random.uniform(0, 100)

        self.update_bar_chart(left, right)

    def send_temp_value(self, idx):
        # Temp 전송 버튼 클릭 시 로그 기록
        self.temp_thresh[idx] = self.ui.line_temp.text()
        self.append_log(f"[TEMP] {self.temp_thresh[idx]} 전송 완료")

    def send_humi_value(self):
        # Humi 전송 버튼 클릭 시 로그 기록
        self.humi_value = self.ui.line_humi.text()
        self.append_log(f"[HUMI] {self.humi_value} 전송 완료")

    def send_command(self):
        # Command 입력 후 Enter 시 로그 기록
        self.cmd = self.ui.cmd_line.text()
        if self.cmd:
            self.append_log(f"> {self.cmd}")
            self.ui.cmd_line.clear()

    def append_log(self, text):
        # 로그창에 텍스트 추가 및 스크롤 최하단 이동
        current_log = self.ui.cmd_log.toPlainText()
        updated_log = current_log + text + "\n"
        self.ui.cmd_log.setPlainText(updated_log)
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
        self.bar_plot.setYRange(0, 100)
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