from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt

def append_log(widget, text):
    # 로그창에 텍스트 추가 및 스크롤 최하단 이동
    current_log = widget.toHtml()
    
    # 만약 'Warning' 들어있으면 빨간색
    if '[Warning]' in text:
        new_line = f'<span style="color:red;">{text}</span><br>'
    elif '[Caution]' in text:
        new_line = f'<span style="color:yellow;">{text}</span><br>'
    else:
        new_line = f'<span style="color:white;">{text}</span><br>'
        
    updated_log = current_log + new_line
    widget.setHtml(updated_log)
    
    widget.verticalScrollBar().setValue(widget.verticalScrollBar().maximum())