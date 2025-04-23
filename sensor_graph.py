import RPi.GPIO as GPIO
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import random
import time

# 그래프에 표시할 최대 데이터 포인트 개수 설정
max_points = 50

# 초기 y 데이터는 NaN으로 채움
ydata = np.ones(max_points, dtype=float) * np.nan

# Figure와 Axes 객체 생성
fig, ax = plt.subplots()
ax.set_xlim(0, max_points-1)
ax.set_ylim(0, 512)  # 랜덤 범위에 맞게 y축 범위 조정 (예: 0 ~ 512)

# 빈 선(Line2D) 객체 생성
line, = ax.plot(np.arange(max_points), ydata, lw=2)

# 초기화 함수: 애니메이션 시작 전에 호출되어 선을 초기 상태로 만듦
def init():
    line.set_ydata(np.ones(max_points, dtype=float) * np.nan)
    return line,

# 애니메이션 함수: 매 프레임마다 호출되어 새로운 데이터를 생성하고 선을 업데이트 함
def animate(i):
    # 0부터 512 사이의 랜덤 정수 생성
    new_value = random.randint(0, 512)
    # 이전 데이터 배열을 오른쪽으로 한 칸 이동시키고, 마지막 자리에 새로운 값 추가
    ydata = np.r_[line.get_ydata()[1:], new_value]
    line.set_ydata(ydata)
    # 새로운 데이터 배열 확인하고 싶으면 print()로 출력할 수 있음
    print(ydata)
    return line,

# 애니메이션 FuncAnimation 설정
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=50, blit=True)

# 그래프 창을 열어서 애니메이션 실행
plt.show()