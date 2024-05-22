
import cv2
import numpy as np
import os

def gamma_correction(image, gamma=2.2):
    invGamma = 1.0 / gamma
    table = np.array([(( i / 255.0) ** invGamma) * 255 for i in range(256)]).astype("uint8")
    
    return cv2.LUT(image, table)

def inverse_gamma_correction(image, gamma):
    table = np.array([((i / 255.0) ** gamma) * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(image, table)

  
def process_images(start, end, folder_path,blur_out, gamma=2.2):
    global image_index 
    images = []
    for i in range(start, end):
        img_path = os.path.join(folder_path, f"{i:05d}.png")
        img = cv2.imread(img_path)
        if img is not None:
            corrected_img = gamma_correction(img, gamma)  # 먼저 감마 보정 적용
            images.append(corrected_img)
        else:
            print(f"Image {img_path} not found.")
    
    if not images:
        print("No images were loaded.")
        return
    
    # 평균 이미지 계산
    average_image = np.mean(images, axis=0).astype(np.uint8)
    
    # 평균된 이미지에서 감마 보정 해제
    recovered_image = inverse_gamma_correction(average_image, gamma)
    
    # 결과 이미지 저장
    # if not os.path.exists(image_out):
    #     os.makedirs(image_out)
    #     print(f"Directory {image_out} was created.")
    
    # output_path = os.path.join(image_out, f"recovered_{start:05d}_to_{end:05d}.png")
    output_path = os.path.join(blur_out, f"{image_index:05d}.png")
    cv2.imwrite(output_path, recovered_image)
    print(f"Recovered image saved to {output_path}")
    image_index +=1
    

# 사용 예
folder_path = '/vfi/datasets/reds_upscale_120fps/part1/'  # 이미지가 저장된 폴더 경로
# folder_path = '/vfi/datasets/GX013496_4k_120fps_test'  # 이미지가 저장된 폴더 경로
image_out = '/vfi/datasets/reds_upscale_blur/part1/'
# image_out = '/vfi/datasets/test/deblur'
total_images = 3993
# total_images = 100
batch_size = 40

cnt = 18
cnt_end = 29



for i in range(cnt, cnt_end+1):
    src_input_path = f"{folder_path}{i:03}"
    blur_out = f"{image_out}{i:03}/blur"
    if not os.path.exists(blur_out):
        os.makedirs(blur_out)
        print(f"Directory {blur_out} was created.")
        image_index = 0  

    for start in range(0, total_images + 1, batch_size):
        end = min(start + batch_size - 1, total_images)
        process_images(start, end, src_input_path, blur_out)

def copy_middle_images(src_folder, dst_folder, group_size=40):
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
        print(f"Directory {dst_folder} created.")

    # 이미지 파일의 색인을 시작
    idx = 0
    total_images = len([name for name in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, name))])

    # 각 그룹에서 중간 프레임을 찾아서 복사
    for group_start in range(0, total_images, group_size):
        middle_frame_index = group_start + 19  # 0 기반 인덱스이므로 19가 중간 프레임
        if middle_frame_index < total_images:  # 전체 이미지 수를 넘지 않는지 확인
            src_path = os.path.join(src_folder, f"{middle_frame_index:05d}.png")
            dst_path = os.path.join(dst_folder, f"{idx:05d}.png")
            if os.path.exists(src_path):
                img = cv2.imread(src_path)
                cv2.imwrite(dst_path, img)
                print(f"Image {src_path} copied to {dst_path}")
                idx += 1
            else:
                print(f"Image {src_path} not found.")

# 사용 예
src_folder = '/vfi/datasets/reds_upscale_120fps/part1/'  # 원본 이미지가 저장된 폴더 경로
# src_folder = '/vfi/datasets/GX013496_4k_120fps_test'  # 원본 이미지가 저장된 폴더 경로
dst_folder = '/vfi/datasets/reds_upscale_blur/part1/'  # 저장될 새 폴더 경로
# dst_folder = '/vfi/datasets/test/sharp' # 저장될 새 폴더 경로

# copy_middle_images(src_folder, dst_folder)

# base_path = '/vfi/datasets/reds_upscale_blur'

start = 17
end = 29

for i in range(start, end+1):

    src_input = f"{src_folder}{i:03d}"
    blur_output = f"{dst_folder}{i:03d}/sharp/"

    if not os.path.exists(blur_output):
        os.makedirs(blur_output)
        print(f"Directory {blur_output} created.")

    copy_middle_images(src_input, blur_output)