import cv2
import time
from sleep_detect_facemesh import is_eyeclosed
from pose_estimate import is_legcrossed, is_chinrest
import switches

# cap = cv2.VideoCapture(0)

# 이미지 파일 불러오기
image_path = 'combined_image5.jpg'  # 분석할 이미지 파일 경로를 입력하세요
image = cv2.imread(image_path)

while True:
    # _, image = cap.read()
    if switches.switch_1_state == True:
        is_sleep = is_eyeclosed(image)
        print("is sleep?:", is_sleep)
    if switches.switch_2_state == True:    
        is_chin = is_chinrest(image)
        print("is chin rest?:", is_chin)
    if switches.switch_3_state == True:
        is_leg = is_legcrossed(image)
        print("is leg crossed?:", is_leg)
    
    # 누워있는자세 검사
    if switches.is_bluetooth_connected == True:
        switches.sock.settimeout(0.5)
        try:
            switches.sock.send("is_lying")
            response = switches.sock.recv(1024)
            data = response.decode()  # UTF-8 또는 해당 문자 인코딩으로 변환
            if (data == True):
                print("기댔을때 실행할 패널티 동작")
        except:
            switches.is_bluetooth_connected = False

    print("- "*50)
    time.sleep(5)