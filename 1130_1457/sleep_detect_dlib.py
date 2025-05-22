import dlib
import cv2
from imutils import face_utils 

# 한 번만 초기화
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)


"""
이미지를 받아 눈이 감겼는지 판단하는 함수.
T/F로 감긴 여부를 반환하며, 오류시 "error"반환
"""
def is_eyeclosed(image):
    # 정상실행시 T/F 반환
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        # 한 프레임에 여러 사람의 얼굴이 있을 수 있으니까 반복문으로 처리
        for face in faces:
            shape = predictor(gray, face)
            # full_object_detection 객체라서 넘파이배열로 형변환
            shape = face_utils.shape_to_np(shape)

            left_eye = shape[36:42]
            left_eye_length = cv2.norm(left_eye[0] - left_eye[3])
            left_eye_height1 = cv2.norm(left_eye[1] - left_eye[5])
            left_eye_height2 = cv2.norm(left_eye[2] - left_eye[4])

            print(left_eye_height1/left_eye_length,left_eye_height2/left_eye_length)

            if( left_eye_height1/left_eye_length < 0.2 and left_eye_height2/left_eye_length < 0.2 ):
                return True
            else:
                return False
    # 오류시 "error 반환"
    except:
        return "error" 
