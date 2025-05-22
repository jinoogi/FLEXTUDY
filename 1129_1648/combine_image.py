import cv2

def combine_image(image1,image2):

    # 이미지의 너비와 높이를 일치시키기 위해 리사이즈 (필요에 따라 조정)
    height = min(image1.shape[0], image2.shape[0])  # 두 이미지 중 더 작은 높이로 설정
    width = min(image1.shape[1], image2.shape[1])   # 두 이미지 중 더 작은 너비로 설정

    image1_resized = cv2.resize(image1, (width, height))
    image2_resized = cv2.resize(image2, (width, height))

    # 두 이미지를 위아래로 붙이기
    combined_image = cv2.vconcat([image1_resized, image2_resized])
    return combined_image

