from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTextEdit

# 로그창에 텍스트 추가 및 스크롤 최하단 이동
def append_log(log_widget, text):
    current_log = log_widget.toHtml()
    
    # 만약 'Warning' 들어있으면 빨간색, 'Caution' 들어있으면 노란색
    if '[Warning]' in text:
        new_line = f'<span style="color:red;">{text}</span><br>'
    elif '[Caution]' in text:
        new_line = f'<span style="color:yellow;">{text}</span><br>'
    else:
        new_line = f'<span style="color:white;">{text}</span><br>'
        
    updated_log = current_log + new_line
    log_widget.setHtml(updated_log)
    
    log_widget.verticalScrollBar().setValue(log_widget.verticalScrollBar().maximum())