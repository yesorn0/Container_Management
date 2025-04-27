# 수위 센서 2개 달아서 왼쪽, 오른쪽 침수 상태 확인
# stm -> 라즈베리 : 온도, 습도, 불꽃감지 flag, 수위센서 값 전송 (왼, 오)
# 라즈베리 -> stm : 온도 경계값, 습도 경계값

import serial
import time
import threading

# 시리얼 포트 설정
ser = serial.Serial('/dev/rfcomm0', 9600, timeout=1.0)

T1 = None
H1 = None
T2 = None
H2 = None
F = None
LW = None
RW = None

# 수신 데이터 리턴 함수
def return_receDATA():
    return [T1, H1, T2, H2, F, LW, RW]


# 송신 스레드
def send_thread():
    while True:
        try:
            ser.write(b"abcdefghijklmnopqrst")
            time.sleep(2)

        except serial.SerialException:
            print("송신 중 에러 발생")
            break

# 수신 스레드
def receive_thread():
    global T1, H1, T2, H2, F, LW, RW
    while True:
        try:
            if ser.in_waiting:
                recv_data = ser.readline().decode().strip()
                print(f"Received: {recv_data}")
                T1 = int(recv_data[3:5])
                H1 = int(recv_data[10:12])
                T2 = int(recv_data[17:19])
                H2 = int(recv_data[24:26])
                F  = int(recv_data[30:31])
                LW = int(recv_data[36:40])
                RW = int(recv_data[45:49])

                print(f"T1: {T1}, H1: {H1}, T2: {T2}, H2: {H2}, F: {F}, LW: {LW}, RW: {RW}")
                
        except serial.SerialException:
            print("수신 중 에러 발생")
            break

def bt_thread_start():
    send = threading.Thread(target=send_thread)
    send.start()
    recv = threading.Thread(target=receive_thread)
    recv.start()


if __name__ == "__main__":
    bt_thread_start()