import cv2
import os
import time
from sleep_detect_facemesh import is_eyeclosed
from pose_estimate import is_legcrossed, is_chinrest
import switches
from combine_image import combine_image
from imutils.video import VideoStream
import subprocess
from opposite_actuator_control import lift_table, lower_table, stop_table
from picamera2 import Picamera2

# 웹캠 비디오코덱, 해상도 설정
# subprocess.run(["v4l2-ctl", "-d", "/dev/video0", "--set-fmt-video=width=800,height=600,pixelformat=MJPG"])
# subprocess.run(["v4l2-ctl", "-d", "/dev/video0", "--set-parm=20"])


# 사용할 오디오파일 경로지정
sleep_audio = "/home/jinwook/sleep_detection/audio_files/sleep_warning.mp3"
chinrest_audio = "/home/jinwook/sleep_detection/audio_files/chinrest_warning.mp3"
legcrossed_audio = "/home/jinwook/sleep_detection/audio_files/legcrossed_warning.mp3"

# time.sleep(10)
# 상체웹캠 초기화
upper_cam = VideoStream(src='/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_77FC6BDF-video-index0').start()
# 하체 카메라모듈 초기화
pi_cam = Picamera2()
pi_cam.configure(pi_cam.create_preview_configuration(main={"size": (320, 240)}))
pi_cam.start()

# time.sleep(5)

eyeclosed_stack = 0
sleep_stack = 0
chinrest_stack = 0
legcrossed_stack = 0
lying_stack = 0

while True:
    upper_image = upper_cam.read()
    lower_image = pi_cam.capture_array()
    lower_image = cv2.cvtColor(lower_image, cv2.COLOR_BGR2RGB)  # OpenCV는 BGR 포맷 사용

    combined_image = combine_image(upper_image,lower_image)

    # 졸음방지기능
    if switches.switch_1_state == True:
        is_eye = is_eyeclosed(upper_image)
        print("is eye closed?:", is_eye)
        # 눈감았으면
        if is_eye == True:
            # 눈감음스택 올리고
            eyeclosed_stack += 1
            # 눈감음 2스택인데 처음조는거면 음성경고
            if sleep_stack == 0 and eyeclosed_stack >= 2 :
                sleep_stack += 1
                os.system(f"mpg123 {sleep_audio}")
            # 눈감음 2스택인데 전에도 졸았으면 책상, 의자기립
            elif sleep_stack >= 1 and eyeclosed_stack >= 2 :
                print("lift desk & chair")
                # 블루투스연결돼 있으면 의자기립명령
                if switches.is_bluetooth_connected == True:
                    switches.sock.settimeout(0.5)
                    try:
                        switches.sock.send("MotorActivate")
                    except:
                        switches.is_bluetooth_connected = False
                # 책상기립
                lift_table()
                # 의자 다 기립할때까지 책상도 sleep해줘야될듯.. 밑에 블루투스코드때매
                time.sleep(10)
        # 눈 안감았으면 눈감음스택 초기화
        elif is_eye == False:
            eyeclosed_stack = 0

    # 턱괴기방지기능
    if switches.switch_2_state == True:    
        is_chin = is_chinrest(combined_image)
        print("is chin rest?:", is_chin)
        if is_chin == True:
            chinrest_stack += 1
            if chinrest_stack >= 2 :
                os.system(f"mpg123 {chinrest_audio}")
        elif is_chin == False:
            chinrest_stack = 0

    # 다리꼬기방지기능
    if switches.switch_3_state == True:
        is_leg = is_legcrossed(combined_image)
        print("is leg crossed?:", is_leg)
        if is_leg == True:
            legcrossed_stack += 1
            if legcrossed_stack >= 2:
                os.system(f"mpg123 {legcrossed_audio}")
        elif is_leg == False:
            legcrossed_stack = 0
    
    # 누워있는자세 검사
    if switches.is_bluetooth_connected == True:
        switches.sock.settimeout(2)
        try:
            switches.sock.send("is_lying")
            response = switches.sock.recv(1024)
            data = response.decode().strip()  # UTF-8 또는 해당 문자 인코딩으로 변환
            
            # 눈이 감지될때만 사람이 있는거라는 로직
            result = is_eyeclosed(upper_image)
            if (data == "true") and ((result == True) or (result == False)) :
                lying_stack += 1
                if (lying_stack >= 2):
                    print("half lift chair")
                    switches.sock.send("PostureMotorActivate")
            else :
                lying_stack = 0
        except:
            switches.is_bluetooth_connected = False
            print("nothing recieved")

    print("- "*50)
    time.sleep(5)