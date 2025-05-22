import cv2
import os
import time
from sleep_detect_facemesh import is_eyeclosed
from pose_estimate import is_legcrossed, is_chinrest
import switches
from combine_image import combine_image
from imutils.video import VideoStream
import subprocess

def check_camera_settings(device):
    result = subprocess.run(["v4l2-ctl", "-d", device, "--all"], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Settings for {device}:")
        print(result.stdout)  # 카메라 설정 출력
    else:
        print(f"Failed to retrieve settings for {device}")
        print(result.stderr)

check_camera_settings("/dev/video0")
check_camera_settings("/dev/video2")

subprocess.run(["v4l2-ctl", "-d", "/dev/video0", "--set-fmt-video=width=160,height=120,pixelformat=MJPG"])
subprocess.run(["v4l2-ctl", "-d", "/dev/video0", "--set-parm=1"])
subprocess.run(["v4l2-ctl", "-d", "/dev/video2", "--set-fmt-video=width=160,height=120,pixelformat=MJPG"])
subprocess.run(["v4l2-ctl", "-d", "/dev/video2", "--set-parm=1"])

check_camera_settings("/dev/video0")
check_camera_settings("/dev/video2")

# 사용할 오디오파일 경로지정
sleep_audio = "/home/jinwook/sleep_detection/audio_files/sleep_warning.mp3"
chinrest_audio = "/home/jinwook/sleep_detection/audio_files/chinrest_warning.mp3"
legcrossed_audio = "/home/jinwook/sleep_detection/audio_files/legcrossed_warning.mp3"

time.sleep(10)

print("point1")
upper_cam = VideoStream(src=0)
# upper_cam.stream.set(cv2.CAP_PROP_FRAME_WIDTH,320)
# upper_cam.stream.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
# upper_cam.stream.set(cv2.CAP_PROP_FPS, 20)
upper_cam.start()
print("point2")
lower_cam = VideoStream(src=2)
# lower_cam.stream.set(cv2.CAP_PROP_FRAME_WIDTH,320)
# lower_cam.stream.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
# lower_cam.stream.set(cv2.CAP_PROP_FPS, 1)
lower_cam.start()
print("point3")


# # 이미지 파일 불러오기
# image_path = 'combined_image5.jpg'  # 분석할 이미지 파일 경로를 입력하세요
# image = cv2.imread(image_path)

time.sleep(5)

while True:
    upper_image = upper_cam.read()
    lower_image = lower_cam.read()

    # # 빈 프레임 확인
    # if upper_image is None or lower_image is None:
    #     print("빈 프레임이 감지되었습니다. 다음 프레임을 기다립니다...")
    #     continue

    # 알맹이 있을때만
    if upper_image and lower_image :
        print("들어옴")
        combined_image = combine_image(upper_image,lower_image)

    if switches.switch_1_state == True:
        is_sleep = is_eyeclosed(upper_image)
        print("is sleep?:", is_sleep)

        # if is_sleep == True:
        #     os.system(f"mpg123 {sleep_audio}")

    if switches.switch_2_state == True:    
        is_chin = is_chinrest(combined_image)
        print("is chin rest?:", is_chin)

        # if is_chin == True:
        #     os.system(f"mpg123 {chinrest_audio}")

    if switches.switch_3_state == True:
        is_leg = is_legcrossed(combined_image)
        print("is leg crossed?:", is_leg)

        # if is_leg == True:
        #     os.system(f"mpg123 {legcrossed_audio}")

    
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