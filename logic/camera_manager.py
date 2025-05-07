import cv2
import subprocess
import os

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget

from gui.camera_ui import Ui_camera_widget 

class CameraManager:
    def __init__(self, parent, log_callback=None):
        self.parent = parent
        self.cap = None
        self.camera_timer = None
        self.camera_window = None
        self.camera_ui = None
        self.log_callback = log_callback 

    def start_camera_view(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("카메라 열기 실패")
            if self.log_callback:
                self.log_callback("[Warning] 카메라 열기 실패")
            return

        self.camera_window = QWidget()
        self.camera_ui = Ui_camera_widget()
        self.camera_ui.setupUi(self.camera_window)
        self.camera_window.show()

        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.update_camera_frame)
        self.camera_timer.start(30)

    def update_camera_frame(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)
                self.camera_ui.camera.setScaledContents(True)
                self.camera_ui.camera.setPixmap(pixmap)
            else:
                print("프레임 읽기 실패")
                if self.log_callback:
                    self.log_callback("[Warning] 프레임 읽기 실패")
                    
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