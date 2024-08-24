import os
import random
import shutil

# 소스 디렉토리와 대상 디렉토리를 정의합니다.
source_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels\\pillpines'
valid_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels\\pillpines'

# 소스 디렉토리 내의 모든 이미지 파일을 가져옵니다.
image_files = [f for f in os.listdir(source_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]

# 이미지 파일 리스트를 랜덤으로 섞습니다.
random.shuffle(image_files)

# 최대 20개의 파일을 선택합니다.
num_files = len(image_files)
num_valid = min(20, num_files)  # 20개 또는 이미지 파일의 총 개수 중 작은 값을 사용
valid_files = image_files[:num_valid]

# 대상 디렉토리가 존재하지 않으면 생성합니다.
if not os.path.exists(valid_dir):
    os.makedirs(valid_dir)

# 선택된 파일들을 valid 디렉토리로 이동합니다.
for file in valid_files:
    source_path = os.path.join(source_dir, file)
    dest_path = os.path.join(valid_dir, file)
    shutil.move(source_path, dest_path)

print(f"{num_valid} files moved to {valid_dir}")
