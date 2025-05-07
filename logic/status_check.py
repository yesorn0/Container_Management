from logic.log_handler import append_log

def check_status(widget, left_water, right_water, Fire_detect, warning_counter, warning_interval):
    # 처음이거나, 20회마다 한 번 출력
    warning_counter += 1
    
    if warning_counter == 1 or warning_counter >= warning_interval:
        warning_counter = 1
        diff = abs(left_water - right_water)
    
        if diff >= 1000:
            if left_water > right_water:  append_log(f"[Warning] Right Side HIGH !!!")
            else :                        append_log(f"[Warning] Left Side High !!!")
        elif diff >= 300:
            if left_water > right_water:  append_log(f"[Caution] Right Side High !!!")
            else :                        append_log(f"[Caution] Left Side High !!!")
        else:
            pass
        
        if Fire_detect == 1: append_log("[Warning] Fire Detected!")
        
    return warning_counter