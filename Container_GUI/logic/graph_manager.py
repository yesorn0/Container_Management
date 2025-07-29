from PyQt5.QtWidgets import QVBoxLayout

import pyqtgraph as pg
from pyqtgraph import PlotWidget, BarGraphItem

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def matplotlib_init(widget):
    # QWidget 안에 matplotlib 추가
    fig = Figure(figsize=(5,4))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(canvas)
    
    return ax, canvas
    
def matplotlib_update(ax, canvas, temp, humi, container):
    # --- matplotlib 그래프 업데이트 ---
    ax.clear()
    ax.plot(temp, label=f"Temp{container}", color='orange')
    ax.plot(humi, label=f"Humi{container}", color='cyan')
    ax.set_ylim(0, 70)
    ax.legend(loc='upper left')
    ax.set_title(f"Container {container}")
    canvas.draw()
    
def pyqtgraph_init(widget):
    # QWidget 안에 pyqtgraph 추가
    pg_plot = pg.PlotWidget()
    pg_plot.addLegend(offset=(10, 10))
    pg_plot.showGrid(x=True, y=True, alpha=0.3)
    pg_plot.setYRange(0, 70)  # y축 고정

    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(pg_plot)
    return pg_plot

def pyqtgraph_update(pg_plot, temp, humi, container):
    # --- pyqtgraph 그래프 업데이트 ---
    pg_plot.clear()
    x = list(range(len(temp)))
    pg_plot.plot(x, temp, pen='r', name=f"Temp{container}")
    pg_plot.plot(x, humi, pen='b', name=f"Humi{container}")
    
def setup_bar_chart(widget):
    bar_plot = PlotWidget()

    # 배경 검정, 좌표계 제거
    bar_plot.setBackground('black')
    bar_plot.showAxis('left', False)
    bar_plot.showAxis('bottom', False)
    bar_plot.setMouseEnabled(x=False, y=False)
    bar_plot.setMenuEnabled(False)
    bar_plot.hideButtons()

    # 범위 설정
    bar_plot.setYRange(0, 2500)
    bar_plot.setXRange(-2, 2)

    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(bar_plot)

    # Bar 초기화 (빈 채로 시작)
    return bar_plot, None, None
        
def update_bar_chart(bar_plot, bar_left, bar_right, left_value, right_value):
    # 기존 bar 제거
    if bar_left:
        bar_plot.removeItem(bar_left)
    if bar_right:
        bar_plot.removeItem(bar_right)

    # 새로운 bar 추가
    bar_left = BarGraphItem(x=[-1], height=[left_value], width=0.6, brush='blue')
    bar_right = BarGraphItem(x=[1], height=[right_value], width=0.6, brush='red')

    bar_plot.addItem(bar_left)
    bar_plot.addItem(bar_right)
    
    return bar_left, bar_right