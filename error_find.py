import os

# 소스 디렉토리를 정의합니다.
source_dir = "../datasets/labels/valid"

# 유효한 번호의 범위를 정의합니다.
valid_numbers = set(range(0, 39))

# 범위를 벗어나는 번호를 찾기 위한 리스트를 정의합니다.
invalid_files = []

# 소스 디렉토리 내의 모든 파일을 순회합니다.
for filename in os.listdir(source_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(source_dir, filename)
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        for line in lines:
            parts = line.split()
            if len(parts) > 0:
                try:
                    number = int(parts[0])
                    if number not in valid_numbers:
                        invalid_files.append((file_path, number))
                except ValueError:
                    print(f"파일 {file_path}에서 숫자로 변환할 수 없는 값 발견: {parts[0]}")

# 결과 출력
if invalid_files:
    print("범위를 벗어나는 번호를 포함한 파일 목록:")
    for file_path, number in invalid_files:
        print(f"파일: {file_path}, 번호: {number}")
else:
    print("모든 파일이 유효한 번호를 포함하고 있습니다.")
