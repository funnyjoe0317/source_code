import cv2

# 이미지 이름을 입력받습니다.
image_name = "000_00000079.png"  # 이 부분을 원하는 이미지 파일 이름으로 변경하세요.
new_width = 2560  # 새로운 너비를 지정하세요.
new_height = 1440  # 새로운 높이를 지정하세요.

# 이미지를 불러옵니다.
image = cv2.imread(image_name)

# 이미지를 새로운 크기로 변경합니다.
resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

# 변경된 이미지를 보여줍니다.
# cv2.imshow("000001_resize", resized_image)

# 변경된 이미지를 저장하고 싶다면 다음 줄의 주석을 해제하세요.
cv2.imwrite("resized_ori" + image_name, resized_image)

# 사용자가 키를 누를 때까지 창을 열어둡니다.
cv2.waitKey(0)
cv2.destroyAllWindows()
