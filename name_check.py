import os

# 디렉토리 경로 설정
image_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\images\\pillpines\\valid'
label_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels\\pillpines\\valid'

# 이미지와 라벨 파일의 이름을 저장할 세트
image_files = set()
label_files = set()

# 이미지 파일의 기본 이름(.jpg 제외)을 저장
for filename in os.listdir(image_dir):
    if filename.endswith(".jpg"):
        image_files.add(os.path.splitext(filename)[0])

# 라벨 파일의 기본 이름(.txt 제외)을 저장
for filename in os.listdir(label_dir):
    if filename.endswith(".txt"):
        label_files.add(os.path.splitext(filename)[0])

# 이미지 폴더에 있지만 라벨 폴더에 없는 파일 찾기
image_only = image_files - label_files
# 라벨 폴더에 있지만 이미지 폴더에 없는 파일 찾기
label_only = label_files - image_files

# 결과 출력
if image_only:
    print("이미지 폴더에만 존재하는 파일들:")
    for file in image_only:
        print(file + ".jpg")

if label_only:
    print("라벨 폴더에만 존재하는 파일들:")
    for file in label_only:
        print(file + ".txt")

if not image_only and not label_only:
    print("모든 파일이 매칭됩니다.")
