import cv2

upper_cam = cv2.VideoCapture(0)
lower_cam = cv2.VideoCapture(2)

if not upper_cam.isOpened():
    print("Upper webcam (index 0)을 열 수 없습니다.")
if not lower_cam.isOpened():
    print("Lower webcam (index 2)을 열 수 없습니다.")

# 각각의 웹캠에서 이미지를 읽어오기
_, upper_image = upper_cam.read()
_, lower_image = lower_cam.read()

if upper_image is None:
    print("Upper webcam에서 이미지를 읽어오지 못했습니다.")
if lower_image is None:
    print("Lower webcam에서 이미지를 읽어오지 못했습니다.")

upper_cam.release()
lower_cam.release()
