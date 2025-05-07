from PyQt5.QtWidgets import QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import pyqtgraph as pg 
from pyqtgraph import PlotWidget, BarGraphItem

# QWidget 안에 matplotlib 추가
def setup_matplotlib(canvas_target_widget):
    fig = Figure(figsize=(5,4))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    layout = QVBoxLayout(canvas_target_widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(canvas)
    
    return fig, ax, canvas

# matplotlib 업데이트
def update_matplotlib(ax, canvas, series, ylim=(10, 50), title=None):
    ax.clear()
    for data, label, color in series:
        ax.plot(data, label=label, color=color)
    ax.set_ylim(*ylim)
    if title:
        ax.set_title(title)
    ax.legend(loc='upper left')
    canvas.draw()
    # ax.clear()
    # ax.plot(temp1_data, label='Temp1', color='orange')
    # ax.plot(humi1_data, label='Humi1', color='cyan')
    # ax.set_ylim(10, 50)
    # ax.legend(loc='upper left')
    # canvas.draw()


# QWidget 안에 pyqtgraph 추가
def setup_pyqtgraph(target_widget):
    pg_plot = pg.PlotWidget()
    pg_plot.addLegend(offset=(10, 10))
    pg_plot.showGrid(x=True, y=True, alpha=0.3)
    pg_plot.setYRange(10, 50)  # y축 고정

    layout = QVBoxLayout(target_widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(pg_plot)
 
    return pg_plot

# pyqtgraph 업데이트
def update_pyqtgraph(pg_plot, x, series):
    pg_plot.clear()
    for y, name, pen in series:
        pg_plot.plot(x, y, pen=pen, name=name)
    # pg_plot.clear()
    # x = list(range(len(temp2_data)))
    # pg_plot.plot(x, temp2_data, pen='r', name='Temp2')
    # pg_plot.plot(x, humi2_data, pen='b', name='Humi2')

# QGroupBox 안에 pyqtgraph (bar) 추가
def setup_bar_chart(target_widget):
    bar_plot = PlotWidget()
    
    bar_plot.setBackground('black')
    bar_plot.showAxis('left', False)
    bar_plot.showAxis('bottom', False)
    bar_plot.setMouseEnabled(x=False, y=False)
    bar_plot.setMenuEnabled(False)
    bar_plot.hideButtons()

    # 범위 설정
    bar_plot.setYRange(0, 2500)
    bar_plot.setXRange(-2, 2)

    layout = QVBoxLayout(target_widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(bar_plot)

    return bar_plot

def update_bar_chart(bar_plot, left_value, right_value, prev_left=None, prev_right=None):
    # 기존 bar 제거
    if prev_left:
        bar_plot.removeItem(prev_left)
    if prev_right:
        bar_plot.removeItem(prev_right)

    # 새로운 bar 추가
    bar_left = BarGraphItem(x=[-1], height=[left_value], width=0.6, brush='blue')
    bar_right = BarGraphItem(x=[1], height=[right_value], width=0.6, brush='red')

    bar_plot.addItem(bar_left)
    bar_plot.addItem(bar_right)
 
    return bar_left, bar_right
