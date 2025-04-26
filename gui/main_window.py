import sys
from control_ui import Ui_MainWindow
import random

from PyQt5.QtWidgets import (
	QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QVBoxLayout, QLineEdit, QTextEdit
)
from PyQt5.QtCore import QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import pyqtgraph as pg 

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # --- 그래프 만들기 L/R ---
        self.setup_graphs()
        
        # --- Temp, Humi 경계값 송수신 ---
        self.ui.btn_temp.clicked.connect(self.send_temp_value)
        self.ui.btn_humi.clicked.connect(self.send_humi_value)
        
        # --- Command Log ---
        self.ui.cmd_line.returnPressed.connect(self.send_command)
        
        # --- Data Update Timer ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graphs)
        self.timer.start(1000) # 1 초마다 Update
        
        self.temp_data = []
        self.humi_data = []
        
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
        self.pg_plot.showGrid(x=True, y=True)
        self.pg_plot.setYRange(30, 70)  # y축 범위 지정
        self.pg_curve = self.pg_plot.plot(pen='r')
        
        layout2 = QVBoxLayout(self.ui.chart_2)
        layout2.setContentsMargins(0, 0, 0, 0)
        layout2.addWidget(self.pg_plot)
        
    def update_graphs(self):
        new_temp = random.uniform(20, 30)
        new_humi = random.uniform(40, 60)
        
        self.temp_data.append(new_temp)
        self.humi_data.append(new_humi)
        
        if len(self.temp_data) > 30:
            self.temp_data.pop(0)
        if len(self.humi_data) > 30:
            self.humi_data.pop(0)
        
        # --- matplotlib Update ---
        self.ax.clear()
        self.ax.plot(self.temp_data, color='orange')
        self.ax.set_ylim(15, 35)
        self.ax.set_title('Temperature')
        self.canvas.draw()
        
        # --- PyQtGraph Update ---
        x = list(range(len(self.humi_data)))
        self.pg_curve.setData(x, self.humi_data)
        
    def send_temp_value(self):
        temp_value = self.ui.line_temp.text()
        self.append_log(f"[TEMP] {temp_value} 전송 완료")
    
    def send_humi_value(self):
        humi_value = self.ui.line_humi.text()
        self.append_log(f"[HUMI] {humi_value} 전송 완료")
    
    def send_command(self):
        cmd = self.ui.cmd_line.text()
        if cmd:
            self.append_log(f"> {cmd}")
            self.ui.cmd_line.clear()
            
    def append_log(self, text):
        current_log = self.ui.cmd_log.toPlainText()
        updated_log = current_log + text + "\n"
        self.ui.cmd_log.setPlainText(updated_log)
        self.ui.cmd_log.verticalScrollBar().setValue(self.ui.cmd_log.verticalScrollBar().maximum())

    
if __name__ == "__main__":
    app = QApplication([])
    window = Main()
    window.show()
    app.exec()