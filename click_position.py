import cv2

# 클릭 이벤트가 발생했을 때 실행될 콜백 함수
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 마우스 버튼이 클릭되면
        print(f"X: {x}, Y: {y}")  # 클릭된 위치의 픽셀 좌표를 출력
        cv2.circle(img, (x, y), 5, (255, 0, 0), -1)  # 클릭된 위치에 원을 그림
        cv2.imshow('image', img)

# 이미지를 불러오고 'image'라는 이름의 윈도우에 표시
img = cv2.imread('004201_resize.png')  # 'your_image.jpg'를 이미지 파일 이름으로 변경
cv2.imshow('image', img)

# 마우스 클릭 이벤트와 위에서 정의한 콜백 함수를 연결
cv2.setMouseCallback('image', click_event)

# 키보드의 아무 키나 누를 때까지 대기
cv2.waitKey(0)
cv2.destroyAllWindows()
