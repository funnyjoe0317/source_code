import cv2

# 두 이미지 파일 이름
image_name1 = "004201_resize.png"
image_name2 = "004201_SR_resize.png"
image_name3 = "004201_vsr_resize.png"

# 이미지를 불러옵니다.
image1 = cv2.imread(image_name1)
image2 = cv2.imread(image_name2)
image3 = cv2.imread(image_name3)

# 관심 영역(ROI)을 정의합니다. 예시: (x 시작점, y 시작점, 너비, 높이)
roi = (1088, 0, 500, 300) # 실제 사용할 ROI를 여기에 맞게 조절하세요.

# 각 이미지에서 동일한 ROI를 추출합니다.
roi_image1 = image1[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
roi_image2 = image2[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
roi_image3 = image3[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]

# 확대할 배율을 설정합니다.
scale_factor = 5  # 배율을 조절하세요.

# ROI를 확대합니다.
zoomed_roi_image1 = cv2.resize(roi_image1, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
zoomed_roi_image2 = cv2.resize(roi_image2, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
zoomed_roi_image3 = cv2.resize(roi_image3, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

# 확대된 이미지를 파일로 저장합니다.
cv2.imwrite("zoomed_roi_image1.jpg", zoomed_roi_image1)
cv2.imwrite("zoomed_roi_image2.jpg", zoomed_roi_image2)
cv2.imwrite("zoomed_roi_image3.jpg", zoomed_roi_image3)
