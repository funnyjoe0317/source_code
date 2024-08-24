import os
import shutil

# 경로 설정
valid_image_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels\\pillpines'
source_label_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels\\pillpines'
valid_label_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels\\pillpines'

# valid 디렉토리의 모든 이미지 파일 이름을 가져옵니다.
valid_image_files = [f for f in os.listdir(valid_image_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]

# 대상 디렉토리가 존재하지 않으면 생성합니다.
if not os.path.exists(valid_label_dir):
    os.makedirs(valid_label_dir)

# 이미지 파일 이름을 기반으로 라벨 파일을 이동합니다.
for image_file in valid_image_files:
    label_file = os.path.splitext(image_file)[0] + '.txt'  # 이미지 파일의 확장자를 .txt로 변경
    source_label_path = os.path.join(source_label_dir, label_file)
    dest_label_path = os.path.join(valid_label_dir, label_file)
    
    # 라벨 파일이 존재하는 경우에만 이동
    if os.path.exists(source_label_path):
        shutil.move(source_label_path, dest_label_path)
        print(f"Moved: {source_label_path} to {dest_label_path}")
    else:
        print(f"Label file not found: {source_label_path}")

print("Label files moved based on valid images.")
