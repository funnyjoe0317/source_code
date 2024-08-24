import os
import shutil

# 디렉토리 경로 정의
source_label_dir = r'\\?\C:\Users\cho\Desktop\uwi_DB_2408\labels\Korea_east\valid'
target_label_dir = r'\\?\C:\Users\cho\Desktop\uwi_DB_2408\labels\Korea_east\class_0'

# 대상 폴더 생성 (존재하지 않으면)
os.makedirs(target_label_dir, exist_ok=True)

# 0번 클래스를 포함하는 라벨 파일 복사
for filename in os.listdir(source_label_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(source_label_dir, filename)
        
        # 라벨 파일 읽기
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # 라벨 파일에 0번 클래스가 포함되어 있는지 확인
        contains_class_0 = any(line.split()[0] == '0' for line in lines)
        
        if contains_class_0:
            # 0번 클래스가 포함된 라벨 파일을 타겟 폴더로 복사
            shutil.copy(file_path, os.path.join(target_label_dir, filename))
            print(f"Copied {filename} to {target_label_dir}")

print("0번 클래스를 포함하는 라벨 파일 복사 완료.")
