import os
import shutil
import sys


# log_file_path = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\output_log.txt'
# sys.stdout = open(log_file_path, 'w', encoding='utf-8')
# 원본 데이터 경로
# image_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\data\\test'
# label_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\yolo\\test'


image_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\data\\obj_train_data'
label_dir = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\yolo\\obj_train_data'

# 새로운 저장 경로
dest_image_base = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\images'
dest_label_base = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\labels'
# dest_image_base = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\test\\images'
# dest_label_base = 'C:\\Users\\cho\\Desktop\\uwi_DB_2408\\test\\labels'

# 새로운 데이터 경로 (지역별 폴더 이름 매핑)
dest_dirs = {
    "동해": "Korea_east",
    "남해": "Korea_south",
    "서해": "Korea_west",
    "필리핀": "pillpines",
    "unsorted": "unsorted"  # 처리되지 않은 파일을 위한 폴더
}

# 새로운 폴더 생성 (이미지 및 라벨용)
for key, folder_name in dest_dirs.items():
    os.makedirs(os.path.join(dest_image_base, folder_name), exist_ok=True)
    os.makedirs(os.path.join(dest_label_base, folder_name), exist_ok=True)

# 특정 디렉토리 내 이미지 파일 개수를 계산하는 함수
def count_image_files(directory, extensions=['.jpg', '.png', '.jpeg']):
    image_files = []
    for root, dirs, files in os.walk(directory):
        image_files.extend([file for file in files if file.lower().endswith(tuple(extensions))])
    return len(image_files)

# 폴더별로 이미지 파일을 이동 및 이름 변경
def move_and_rename_files(label_path, lines, dest_dir, img_filename, file_count, processed_images):
    if img_filename in processed_images:
        return  # 이미 처리된 이미지 파일은 건너뜁니다.

    # 데이터 값 추출 (클래스 정보 포함)
    # data = " ".join(line.split()[:5])
    
    # 새로운 파일 이름 생성 (000001부터 시작하여 오름차순)
    new_base_name = f"{dest_dir}_{file_count:06d}"
    
    new_img_filename = f"{new_base_name}.jpg"
    new_txt_filename = f"{new_base_name}.txt"
    
    # 파일 이동 및 이름 변경
    new_img_path = os.path.join(dest_image_base, dest_dir, new_img_filename)
    new_txt_path = os.path.join(dest_label_base, dest_dir, new_txt_filename)

    # 이미지 파일 복사
    if os.path.exists(img_filename):  # 이미지 파일이 존재할 때만 복사
        shutil.copyfile(img_filename, new_img_path)
        # print(f"Copied {img_filename} to {new_img_path}")

    # 라벨 파일 저장 (모든 라인 한 번에 저장)
    with open(new_txt_path, 'w') as new_txt_file:
        for line in lines:
            data = " ".join(line.split()[:5])
            new_txt_file.write(data + '\n')

    processed_images.add(img_filename)  # 처리된 이미지 파일로 추가

    return new_img_path, new_txt_path

# 디버깅용 출력 함수
def debug_print(folder_name, img_count, label_count, saved_img_count, saved_label_count, dest_dir):
    print(f"폴더: {folder_name}")
    # print(f"  기존 이미지 파일 개수: {img_count}")
    # print(f"  기존 라벨 파일 개수: {label_count}")
    # print(f"  새로 저장된 이미지 파일 개수: {saved_img_count}")
    # print(f"  새로 저장된 라벨 파일 개수: {saved_label_count}")
    
    # dest_dir 내 실제 파일 개수 확인
    final_img_count = count_image_files(os.path.join(dest_image_base, dest_dir))
    final_label_count = len([name for name in os.listdir(os.path.join(dest_label_base, dest_dir)) if name.endswith('.txt')])
    
    print(f"  대상 폴더 내 최종 이미지 파일 개수: {final_img_count}")
    print(f"  대상 폴더 내 최종 라벨 파일 개수: {final_label_count}")
    print("-" * 40)

# 각 지역별 폴더의 기존 파일 개수를 저장하는 딕셔너리
existing_img_files = {}
existing_label_files = {}

for region, dir_name in dest_dirs.items():
    existing_img_files[dir_name] = count_image_files(os.path.join(dest_image_base, dir_name))
    existing_label_files[dir_name] = len([name for name in os.listdir(os.path.join(dest_label_base, dir_name)) if name.endswith('.txt')])

# 폴더별로 이미지와 라벨을 처리
for root, dirs, files in os.walk(label_dir):
    processed_files = {
        "Korea_east": 0,
        "Korea_south": 0,
        "Korea_west": 0,
        "pillpines": 0,
        "unsorted": 0
    }
    
    processed_images = set()  # 처리된 이미지 파일을 저장할 집합

    for file in files:
        if file.endswith('.txt'):
            label_path = os.path.join(root, file)
            with open(label_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if "동해" in line:
                        dest_dir = dest_dirs["동해"]
                    elif "남해" in line:
                        dest_dir = dest_dirs["남해"]
                    elif "서해" in line:
                        dest_dir = dest_dirs["서해"]
                    elif "필리핀" in line:
                        dest_dir = dest_dirs["필리핀"]
                    else:
                        dest_dir = dest_dirs["unsorted"]
                    
                    # 이미지 파일 경로 확인
                    img_filename = label_path.replace(label_dir, image_dir).replace('.txt', '.jpg')
                    if os.path.exists(img_filename):
                        # 파일 개수 관리: 기존 파일 + 이번 폴더에서 새로 추가된 파일 수
                        file_count = existing_img_files[dest_dir] + processed_files[dest_dir] + 1
                        
                        # 파일 이동 및 이름 변경
                        move_and_rename_files(label_path, lines, dest_dir, img_filename, file_count, processed_images)
                        processed_files[dest_dir] += 1
    
    # 폴더 내 작업이 끝나면 디버깅 출력
    for region, dir_name in dest_dirs.items():
        if processed_files[dir_name] > 0:
            debug_print(root, existing_img_files[dir_name], existing_label_files[dir_name], processed_files[dir_name], processed_files[dir_name], dir_name)
            # 작업이 완료된 후, 폴더 내 이미지 및 라벨 파일 개수를 업데이트
            existing_img_files[dir_name] += processed_files[dir_name]
            existing_label_files[dir_name] += processed_files[dir_name]

print("파일 분류 및 이동이 완료되었습니다.")

# 로그 파일 스트림을 닫습니다.
# sys.stdout.close()