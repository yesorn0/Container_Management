import os
import platform
import subprocess
from PyQt5.QtWidgets import QMessageBox

def open_csv_folder(self):
    folder_path = os.path.join(os.getcwd(), "csv_data")

    if not os.path.exists(folder_path):
        QMessageBox.warning(self, "폴더 없음", f"{folder_path} 경로가 존재하지 않습니다.")
        return

    system = platform.system()

    try:
        if system == "Windows":
            os.startfile(folder_path)
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", folder_path])
        else:  # Linux
            subprocess.Popen(["xdg-open", folder_path])
    except Exception as e:
        QMessageBox.critical(self, "오류", f"폴더를 여는 중 오류 발생: {e}")
