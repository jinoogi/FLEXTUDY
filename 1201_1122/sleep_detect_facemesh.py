import cv2
import mediapipe as mp
import numpy as np

# MediaPipe 초기화
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5)
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

"""
이미지를 받아 눈이 감겼는지 판단하는 함수.
T/F로 감긴 여부를 반환하며, 오류시 상황에 맞는 에러메시지 반환
"""
def is_eyeclosed(image):
    try:
        # 1. 이미지를 RGB로 변환 (MediaPipe 입력 형식)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_detection_results = face_detection.process(image_rgb)
        for detection in face_detection_results.detections:
            # 얼굴의 경계 상자 추출
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape  # 이미지 크기
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

            # 얼굴 영역 자르기 및 확대
            face_crop = image[y:y + h, x:x + w]
            face_resized = cv2.resize(face_crop, (512, 512))  # 모델 입력을 위해 크기 조정

            # 얼굴 이미지를 RGB로 변환
            face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)

            # 2. Face Mesh 모델 적용
            results = face_mesh.process(face_rgb)

        if not results.multi_face_landmarks:
            return "face not detected error"  # 얼굴이 감지되지 않으면 "error" 반환

        # 3. 랜드마크 추출 및 눈 감음 여부 판단
        for face_landmarks in results.multi_face_landmarks:
            # 왼쪽 눈 좌표 (MediaPipe 눈 랜드마크 인덱스: 33, 160, 158, 133, 153, 144)
            left_eye_indices = [33, 160, 158, 133, 153, 144]
            left_eye = np.array(
                [[face_landmarks.landmark[i].x, face_landmarks.landmark[i].y] for i in left_eye_indices]
            )

            # 눈 가로 길이 및 세로 길이 계산
            left_eye_length = np.linalg.norm(left_eye[0] - left_eye[3])  # 눈 가로 길이
            left_eye_height1 = np.linalg.norm(left_eye[1] - left_eye[5])  # 눈 세로 길이 1
            left_eye_height2 = np.linalg.norm(left_eye[2] - left_eye[4])  # 눈 세로 길이 2

            # 디버깅용 비율 출력
            print(left_eye_height1 / left_eye_length, left_eye_height2 / left_eye_length)

            # 눈 감음 여부 판단
            if left_eye_height1 / left_eye_length < 0.12 and left_eye_height2 / left_eye_length < 0.12:
                return True  # 눈이 감겼음
            else:
                return False  # 눈이 열려 있음

        return "face landmark not detected error"  # 얼굴 랜드마크가 감지되지 않음

    except Exception as e:
        print(f"Error: {e}")
        return "error"  # 예외 발생 시 "error" 반환
