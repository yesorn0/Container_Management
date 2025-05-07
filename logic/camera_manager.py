import os
import subprocess
import cv2

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

from gui.camera_ui import Ui_camera_widget
from logic.log_handler import append_log

# 전역 변수 정의
cap = None
camera_window = None
camera_ui = None
camera_timer = None
flag = 0

def start_camera_view(parent):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        append_log(parent.ui.cmd_log, "[Warning] 카메라 열기 실패")
        return

    camera_window = QWidget()
    camera_ui = Ui_camera_widget()
    camera_ui.setupUi(camera_window)
    camera_window.show()

    def update_camera_frame():
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)
                camera_ui.camera.setPixmap(pixmap)
                camera_ui.camera.setScaledContents(True)
            else:
                append_log(parent.ui.cmd_log, "[Warning] 프레임 읽기 실패")

    timer = QTimer()
    timer.timeout.connect(update_camera_frame)
    timer.start(30)
# def start_camera_view(log_widget, parent):
#     global cap, camera_window, camera_ui, camera_timer
    
#     # 기존 점유 프로세스 제거
#     check_and_kill_video0()
    
#     # 비디오 캡처 객체 생성
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("카메라 열기 실패")
#         append_log(log_widget, f"[Warning] 카메라 열기 실패")
#         return

#     # 새 창(camera_widget) 띄우기 
#     camera_window = QWidget()
#     camera_ui = Ui_camera_widget()
#     camera_ui.setupUi(camera_window)

#     camera_window.show() 

#     # 프레임 업데이트 타이머
#     camera_timer = QTimer()
#     camera_timer.timeout.connect(update_camera_frame)
#     camera_timer.start(30)
#     if flag == 1:
#         append_log(log_widget, f"[Warning] 프레임 읽기 실패")
#         flag = 0
    
# def update_camera_frame():
#     global cap, camera_ui
    
#     if cap is not None and cap.isOpened():
#         ret, frame = cap.read()
#         if ret:
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             h, w, ch = frame.shape
#             bytes_per_line = ch * w
#             q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
#             pixmap = QPixmap.fromImage(q_img)

#             # 여기서 camera_ui의 widget에 그림
#             camera_ui.camera.setScaledContents(True)
#             camera_ui.camera.setPixmap(pixmap)
#         else:
#             print("프레임 읽기 실패")
#             flag = 1
            
def check_and_kill_video0():
    try:
        # /dev/video0을 잡고 있는 프로세스 찾기
        result = subprocess.run(['fuser', '/dev/video0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.stdout.strip():
            pids = result.stdout.strip().split()
            print(f"/dev/video0을 사용하는 프로세스 발견: {pids}")

            for pid in pids:
                try:
                    os.kill(int(pid), 9)
                    print(f"프로세스 {pid} 강제 종료 성공")
                except Exception as e:
                    print(f"프로세스 {pid} 종료 실패: {e}")
        else:
            print("/dev/video0을 점유하는 프로세스가 없습니다.")

    except Exception as e:
        print(f"check_and_kill_video0 실패: {e}")