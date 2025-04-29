import cv2

def start_camera():
    cap = cv2.VideoCapture(0)  # 0번 카메라 열기
    if not cap.isOpened():
        print("카메라 열기 실패")
        return

    print("카메라 ON (종료하려면 q를 누르세요)")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임 읽기 실패")
            break
        cv2.imshow('Webcam', frame)

        # 'q' 키 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def wait_for_signal():
    print("신호를 기다리는 중입니다... (s를 누르면 웹캠 ON)")
    while True:
        key = input(">> ")
        if key == 's':
            start_camera()

wait_for_signal()
