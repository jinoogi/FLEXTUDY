import cv2
import mediapipe as mp
import numpy as np

# BlazePose 모델 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, model_complexity=1, min_detection_confidence=0.5)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5)

"""
다리꼬았는지 하체 선간의 접점으로 판단하는 알고리즘
"""
def intersection_algorithm(landmarks):

    # 왼쪽 엉덩이-무릎 선
    left_hip = np.array([landmarks[23].x, landmarks[23].y])
    left_knee = np.array([landmarks[25].x, landmarks[25].y])

    # 오른쪽 엉덩이-무릎 선
    right_hip = np.array([landmarks[24].x, landmarks[24].y])
    right_knee = np.array([landmarks[26].x, landmarks[26].y])

    # 왼쪽 무릎-발목 선
    left_ankle = np.array([landmarks[27].x, landmarks[27].y])

    # 오른쪽 무릎-발목 선
    right_ankle = np.array([landmarks[28].x, landmarks[28].y])

    # 오른쪽 발목-발끝(엄지발가락) 선
    right_foot_thumb = np.array([landmarks[32].x, landmarks[32].y])
    # 오른쪽 발목-뒤꿈치 선
    right_heel = np.array([landmarks[30].x, landmarks[30].y])

    # 왼쪽 발목-발끝(엄지발가락) 선
    left_foot_thumb = np.array([landmarks[31].x, landmarks[31].y])
    # 왼쪽 발목-뒤꿈치 선
    left_heel = np.array([landmarks[29].x, landmarks[29].y])

    def do_lines_intersect(p1, p2, q1, q2):
        """두 선분이 교차하는지 확인"""
        def ccw(a, b, c):
            return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

        return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

    # 왼쪽 다리가 오른쪽 다리 위로 교차하는지 (엉덩이-무릎, 무릎-발목, 발목-발끝, 발목-뒤꿈치 포함)
    is_left_crossing = (
        do_lines_intersect(left_hip, left_knee, right_knee, right_ankle) or
        do_lines_intersect(left_hip, left_knee, right_ankle, right_foot_thumb) or
        do_lines_intersect(left_hip, left_knee, right_ankle, right_heel) or
        do_lines_intersect(left_knee, left_ankle, right_knee, right_ankle) or
        do_lines_intersect(left_knee, left_ankle, right_ankle, right_foot_thumb) or
        do_lines_intersect(left_knee, left_ankle, right_ankle, right_heel)
    )

    # 오른쪽 다리가 왼쪽 다리 위로 교차하는지 (엉덩이-무릎, 무릎-발목, 발목-발끝, 발목-뒤꿈치 포함)
    is_right_crossing = (
        do_lines_intersect(right_hip, right_knee, left_knee, left_ankle) or
        do_lines_intersect(right_hip, right_knee, left_ankle, left_foot_thumb) or
        do_lines_intersect(right_hip, right_knee, left_ankle, left_heel) or
        do_lines_intersect(right_knee, right_ankle, left_knee, left_ankle) or
        do_lines_intersect(right_knee, right_ankle, left_ankle, left_foot_thumb) or
        do_lines_intersect(right_knee, right_ankle, left_ankle, left_heel)
    )

    return is_left_crossing or is_right_crossing

"""
다리꼬았는지 여부 판단하는 함수
T/F로 다리꼰 여부를 반환하며, 오류시 상황에 맞는 에러메시지 반환
"""
def is_legcrossed(image):
    try:
        # BGR 이미지를 RGB로 변환
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            is_crossing = intersection_algorithm(landmarks)

            if is_crossing:
                return True
            else:
                return False
        return "no person landmark"
    except:
        return "error"




"""
턱괴었는지 턱과 손사이 거리로 판단하는 알고리즘
"""
def face_hand_algorithm_with_pose(pose_results, face_mesh_results, image):
    # 이미지 크기 가져오기
    image_width = image.shape[1]
    image_height = image.shape[0]

    pose_landmarks = pose_results.pose_landmarks.landmark

    # 왼쪽 어깨(11번)와 오른쪽 어깨(12번) 좌표 추출 및 픽셀 변환
    left_shoulder = np.array([
        pose_landmarks[11].x * image_width,
        pose_landmarks[11].y * image_height
    ])
    right_shoulder = np.array([
        pose_landmarks[12].x * image_width,
        pose_landmarks[12].y * image_height
    ])

    # 어깨 너비 계산 (2D 픽셀 거리)
    shoulder_width = np.linalg.norm(left_shoulder - right_shoulder)

    # 얼굴의 턱 랜드마크 좌표들 (152: 턱 끝, 365: 오른쪽 턱, 135: 왼쪽 턱) 픽셀 단위 변환
    face_landmarks = face_mesh_results.multi_face_landmarks[0]
    chin_landmarks_indices = [152, 365, 135]
    chin_landmarks = [
        np.array([
            face_landmarks.landmark[idx].x * image_width,
            face_landmarks.landmark[idx].y * image_height
        ])
        for idx in chin_landmarks_indices
    ]

    # Pose 모델에서 손 랜드마크 좌표 (15~22번: 손, 손가락 끝 포함)
    hand_landmarks_indices = [15, 16, 17, 18, 19, 20, 21, 22]
    hand_positions = [
        np.array([
            pose_landmarks[idx].x * image_width,
            pose_landmarks[idx].y * image_height
        ])
        for idx in hand_landmarks_indices
    ]

    # 턱 랜드마크와 손 랜드마크 간 거리 계산
    for hand in hand_positions:
        for chin in chin_landmarks:
            distance = np.linalg.norm(chin - hand)  # 픽셀 단위 거리 계산
            
            # 거리 임계값 설정 (픽셀 기준으로 비교)
            if distance / shoulder_width < 0.2:  # 비율 조정 가능
                return True  # 턱 괴기 동작 탐지됨
    return False
"""
턱 괴었는지 여부 판단하는 함수
T/F로 턱 괸 여부를 반환하며, 오류시 상황에 맞는 에러메시지 반환
"""
def is_chinrest(image):
    try:
        # BGR 이미지를 RGB로 변환
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pose_results = pose.process(image_rgb)
        face_mesh_results = face_mesh.process(image_rgb)
        # 턱 괴기 탐지
        is_chin_resting = face_hand_algorithm_with_pose(pose_results, face_mesh_results, image)
        # 결과 표시
        if is_chin_resting:
            return True
        else:
            return False
    except:
        return "error"