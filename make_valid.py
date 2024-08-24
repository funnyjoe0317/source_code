import os
import shutil
import random

# 디렉토리 경로 정의
source_label_dir = r'\\?\C:\Users\cho\Desktop\uwi_DB_2408\labels\pillpines\train'
source_image_dir = r'\\?\C:\Users\cho\Desktop\uwi_DB_2408\images\pillpines\train'
valid_label_dir = r'\\?\C:\Users\cho\Desktop\uwi_DB_2408\labels\pillpines\valid'
valid_image_dir = r'\\?\C:\Users\cho\Desktop\uwi_DB_2408\images\pillpines\valid'

# 유효성 폴더 생성 (존재하지 않으면)
os.makedirs(valid_label_dir, exist_ok=True)
os.makedirs(valid_image_dir, exist_ok=True)

# 클래스별 파일 목록 저장
class_files = {}

# 라벨 디렉토리 내 모든 파일 순회
for filename in os.listdir(source_label_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(source_label_dir, filename)
        
        # 라벨 파일 읽기
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # 라벨 파일에 특정 클래스가 포함되어 있는지 확인
        for line in lines:
            class_id = line.split()[0]
            
            if class_id not in class_files:
                class_files[class_id] = []
            
            # 클래스 ID별로 파일 경로와 이름을 저장
            class_files[class_id].append((file_path, filename))

# 각 클래스에서 20개의 파일을 선택하여 valid 폴더로 이동
for class_id, files in class_files.items():
    random.shuffle(files)  # 파일 리스트를 무작위로 섞기
    selected_files = files[:20]  # 각 클래스에서 20개의 파일 선택
    
    for file_path, filename in selected_files:
        try:
            # 라벨 파일 valid/labels 폴더로 이동
            shutil.move(file_path, os.path.join(valid_label_dir, filename))
        except FileNotFoundError:
            print(f"Error: Label file {file_path} not found. Skipping this file.")
            continue
        
        # 동일한 이름의 이미지 파일을 valid/images 폴더로 이동
        image_filename = filename.replace('.txt', '.jpg')
        image_path = os.path.join(source_image_dir, image_filename)
        if os.path.exists(image_path):
            try:
                shutil.move(image_path, os.path.join(valid_image_dir, image_filename))
                print(f'Moved {filename} and {image_filename} to valid folders.')
            except FileNotFoundError:
                print(f"Error: Image file {image_path} not found during move. Skipping this file.")
        else:
            print(f'Warning: Image file {image_filename} not found for label {filename}.')

print("지정된 클래스의 라벨 및 이미지를 valid 폴더로 이동 완료.")
