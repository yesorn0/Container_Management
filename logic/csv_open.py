import os
import platform
import subprocess
from PyQt5.QtWidgets import QMessageBox

def open_csv_folder():
    folder_path = os.path.join(os.getcwd(), "csv_data")

    if not os.path.exists(folder_path):
        QMessageBox.warning("폴더 없음", f"{folder_path} 경로가 존재하지 않습니다.")
        return

    system = platform.system()

    try:
        subprocess.Popen(["xdg-open", folder_path]) # Linux
    except Exception as e:
        QMessageBox.critical("오류", f"폴더를 여는 중 오류 발생: {e}")
