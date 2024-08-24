import os

# 기존 번호와 새로운 번호의 매핑을 정의합니다.
# mapping = {
#     1: 0, 4: 1, 5: 2, 10: 3, 15: 4, 17: 5, 20: 6, 22: 7, 24: 8, 26: 9,
#     27: 10, 29: 11, 36: 12, 40: 13, 41: 14, 43: 15, 44: 16, 46: 17,
#     79: 18, 80: 19, 81: 20, 95: 21, 96: 22, 97: 23, 98: 24, 100: 25,
#     101: 26, 103: 27, 128: 28, 129: 29, 130: 30, 137: 31, 140: 32,
#     150: 33, 157: 34, 159: 35, 162: 36, 172: 37, 93: 38
# }

# 남해
# mapping = {
#     9: 0,
#     12: 1,
#     19: 2,
#     24: 3,
#     33: 4,
#     39: 5,
#     41: 6,
#     42: 7,
#     43: 8,
#     78: 9,
#     94: 10,
#     96: 11,
#     97: 12,
#     98: 13,
#     100: 14,
#     118: 15,
#     141: 16,
#     150: 17,
#     157: 18,
#     158: 19,
#     159: 20,
#     160: 21
# }

# 동해
# mapping = {
#     20: 0,
#     22: 1,
#     24: 2,
#     26: 3,
#     29: 4,
#     40: 5,
#     41: 6,
#     80: 7,
#     94: 8,
#     95: 9,
#     96: 10,
#     97: 11,
#     98: 12,
#     100: 13,
#     103: 14,
#     129: 15,
#     140: 16,
#     157: 17,
#     159: 18,
#     162: 19
# }

# 서해
# mapping = {
#     6: 0,
#     157: 1
# }

# 필리핀
mapping = {
    41: 0,
    42: 1,
    44: 2,
    60: 3,
    66: 4,
    80: 5,
    83: 6,
    93: 7,
    94: 8,
    95: 9,
    96: 10,
    97: 11,
    104: 12,
    117: 13,
    137: 14,
    145: 15,
    157: 16,
    160: 17,
    162: 18,
    172: 19
}


# 소스 디렉토리를 정의합니다.
source_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels\\pillpines'

# # 소스 디렉토리 내의 모든 파일을 순회합니다.
# for filename in os.listdir(source_dir):
#     if filename.endswith(".txt"):
#         file_path = os.path.join(source_dir, filename)
        
#         # 파일 내용을 읽습니다.
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
        
#         # 파일 내용을 수정합니다.
#         with open(file_path, 'w') as file:
#             for line in lines:
#                 parts = line.split()
#                 if int(parts[0]) in mapping:
#                     parts[0] = str(mapping[int(parts[0])])
#                 modified_line = ' '.join(parts)
#                 file.write(modified_line + '\n')

# print("모든 파일에서 번호를 변경했습니다.")
# 소스 디렉토리 내의 모든 파일을 순회합니다.
for filename in os.listdir(source_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(source_dir, filename)
        
        # 파일 내용을 읽습니다.
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # 파일 내용을 수정합니다.
        with open(file_path, 'w') as file:
            for line in lines:
                parts = line.split()
                if len(parts) > 0 and int(parts[0]) in mapping:
                    old_value = parts[0]
                    parts[0] = str(mapping[int(parts[0])])
                    print(f"Mapping {old_value} to {parts[0]} in file {filename}")
                    modified_line = ' '.join(parts)
                    file.write(modified_line + '\n')
                else:
                    print(f"Skipping line with {parts[0]} in file {filename}")
                    # 매핑되지 않은 숫자는 파일에 기록되지 않음

print("모든 파일에서 번호를 변경했습니다.")