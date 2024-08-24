import os

# 소스 디렉토리를 정의합니다.
# source_dir = "../datasets/labels/train"
# source_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels\\Korea_east'

# # 모든 파일에서 찾은 첫 번째 숫자를 저장할 세트를 정의합니다.
# first_numbers = set()

# # 소스 디렉토리 내의 모든 파일을 순회합니다.
# for filename in os.listdir(source_dir):
#     if filename.endswith(".txt"):
#         file_path = os.path.join(source_dir, filename)
        
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
        
#         # 파일에서 첫 번째 숫자만 저장합니다.
#         for line in lines:
#             parts = line.split()
#             if len(parts) > 0:
#                 try:
#                     number = int(parts[0])
#                     first_numbers.add(number)
#                 except ValueError:
#                     print(f"파일 {file_path}에서 숫자로 변환할 수 없는 값 발견: {parts[0]}")

# # 결과 출력
# print("모든 파일의 첫 번째 숫자들(중복 제거):")
# print(sorted(first_numbers))


import os
from collections import Counter

# 소스 디렉토리를 정의합니다.
# source_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels\\pillpines'
# source_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels\\Korea_east\\train'
source_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels\\pillpines\\valid'
# source_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels\\Korea_east\\class_0'

# 모든 파일에서 찾은 첫 번째 숫자를 저장할 카운터를 정의합니다.
first_numbers_counter = Counter()

# 소스 디렉토리 내의 모든 파일을 순회합니다.
for filename in os.listdir(source_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(source_dir, filename)
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # 파일에서 첫 번째 숫자를 카운터에 추가합니다.
        for line in lines:
            parts = line.split()
            if len(parts) > 0:
                try:
                    number = int(parts[0])
                    first_numbers_counter[number] += 1
                except ValueError:
                    print(f"파일 {file_path}에서 숫자로 변환할 수 없는 값 발견: {parts[0]}")

# 결과 출력
print("모든 파일의 첫 번째 숫자들 및 그 빈도수:")
for number, count in sorted(first_numbers_counter.items()):
    print(f"숫자 {number}: {count}번")