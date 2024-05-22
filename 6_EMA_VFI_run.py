import cv2
import torch
import os
import numpy as np
import argparse
from benchmark.utils.pytorch_msssim import ssim_matlab
from Trainer import Model
import config as cfg
import warnings
from tqdm import tqdm
import re
import shutil

warnings.filterwarnings('ignore')
torch.set_grad_enabled(False)

def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='ours', type=str, help='Model type')
    parser.add_argument('--path', type=str, required=True, help='Path to images')
    parser.add_argument('--newpath', type=str, required=True, help='Path to interpolatied images')
    return parser.parse_args()

def load_and_prepare_image(image_path):
    image = cv2.imread(image_path)
    return (torch.tensor(image.transpose(2, 0, 1)).cuda() / 255.).unsqueeze(0)

def interpolate_and_save_images(folder_path, output_path):
    images = sorted([img for img in os.listdir(folder_path) if img.endswith('.png')])
    model = setup_model(args.model)
    temp_output_path = os.path.join(folder_path, "temp")

    if not os.path.exists(temp_output_path):
        os.makedirs(temp_output_path)

    for i in range(len(images) - 1):
        I0 = load_and_prepare_image(os.path.join(folder_path, images[i]))
        I2 = load_and_prepare_image(os.path.join(folder_path, images[i + 1]))

        mid = model.inference(I0, I2, TTA=True, fast_TTA=True)[0]
        mid = mid.detach().cpu().numpy().transpose(1, 2, 0)
        mid = np.clip(mid, 0, 1)

        # output_filename = f'{int(images[i][:-4]) + 0.5:.1f}.png'
        output_filename = f'{i * 2 + 1:05d}.png'
        cv2.imwrite(os.path.join(temp_output_path, output_filename), (mid * 255).astype(np.uint8))
        # print(f"image interpolation : {output_filename}")

    # Optional: Move files from temp to final output, renaming as needed
    organize_interpolated_frames(temp_output_path, output_path, folder_path)

def setup_model(model_name):
    cfg.MODEL_CONFIG['LOGNAME'] = model_name
    cfg.MODEL_CONFIG['MODEL_ARCH'] = cfg.init_model_config(F=32, depth=[2, 2, 2, 4, 4])
    model = Model(-1)
    model.load_model()
    model.eval()
    model.device()
    return model

def is_numeric(s):
    """ 파일 이름의 시작 부분이 숫자인지 확인 """
    return s.split('.')[0].isdigit()

def organize_interpolated_frames(temp_path, final_path, folder_path):
    print(f"Final path: {final_path}")
    print(f"Absolute final path: {os.path.abspath(final_path)}")    
    if not os.path.exists(final_path):
        os.makedirs(final_path) 

    # 파일 목록 불러오기 및 정렬
    temp_files = sorted([f for f in os.listdir(temp_path) if f.endswith('.png')], key=lambda x: int(x.split('.')[0]))
    original_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')], key=lambda x: int(x.split('.')[0]))

    # 새로운 파일 목록 생성
    new_file_list = [''] * (2 * len(original_files) - 1)

    # 원본 파일 이름 변경 및 짝수 인덱스에 할당
    for i, orig_file in enumerate(original_files):
        new_index = 2 * i
        new_file_list[new_index] = f"{new_index:05d}.png"

    # 보간된 파일을 홀수 인덱스에 할당
    for i, temp_file in enumerate(temp_files):
        new_index = 2 * i + 1
        if new_index < len(new_file_list):
            new_file_list[new_index] = f"{new_index:05d}.png"

    # 파일을 새로운 이름으로 이동
    for i, file_name in enumerate(new_file_list):
        if file_name == '':  # 빈 슬롯은 건너뛰기
            continue
        source_folder = temp_path if i % 2 == 1 else folder_path
        old_name = temp_files[i//2] if i % 2 == 1 else original_files[i//2]
        source_path = os.path.join(source_folder, old_name)
        new_path = os.path.join(final_path, file_name)

        if not os.path.exists(source_path):
            print(f"File not found: {source_path}")
            continue
        
        shutil.move(source_path, new_path)
        # print(f"Moved {old_name} from {source_path} to {new_path}")     

    # 임시 폴더가 비어있으면 삭제
    if not os.listdir(temp_path):
        os.rmdir(temp_path)

def clear_folder(folder_path):
    """Clear all files in the specified folder."""
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            # print(f"Deleted file {item} from {folder_path}")
        elif os.path.isdir(item_path):
            print(f"Skipping directory {item} in {folder_path}")

def relocate_images(final_path, original_folder_path):
    """Relocate images from the final directory back to the original directory after clearing it."""
    print("Clearing the original folder...")
    clear_folder(original_folder_path)  # Clear the original folder first

    print("Relocating images back to the original folder...")
    files = os.listdir(final_path)
    for file in files:
        source_path = os.path.join(final_path, file)
        destination_path = os.path.join(original_folder_path, file)
        shutil.move(source_path, destination_path)
        # print(f"Moved {file} from {source_path} to {destination_path}")

    # Check if final_path is now empty and remove if it is
    if not os.listdir(final_path):
        os.rmdir(final_path)
        print(f"Cleaned up the final directory: {final_path}")

def clear_temporary_files(temp_path):
    print("Cleaning up temporary files...")
    files = os.listdir(temp_path)
    for file in files:
        file_path = os.path.join(temp_path, file)
        os.remove(file_path)
        print(f"Deleted temporary file: {file_path}")

    # Remove the temp directory if empty
    if not os.listdir(temp_path):
        os.rmdir(temp_path)
        print(f"Removed empty temporary directory: {temp_path}")

def count_files_in_directory(directory_path):
    """Count only files in the given directory."""
    return sum(1 for item in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, item)))

if __name__ == "__main__":
    args = setup_parser()
    temp_path = os.path.join(args.path, "temp") 

    # 첫 번째 로그: 초기 이미지 파일 개수
    initial_count = count_files_in_directory(args.path)
    print(f"Initial number of image files: {initial_count}")    
    for i in range(1):# 3번 해야함
        print("------------------ start interpolation-------------------")
        interpolate_and_save_images(args.path, args.newpath)
        # organize_interpolated_frames('./test_frames/temp','./test_frames')
        print("------------------ good job!-------------------")

        print("------------------ relocate images --------------------")
        relocate_images(args.newpath, args.path)
        # clear_temporary_files(temp_path)
        print("------------------ clean-up done ----------------------")  
        
        count = count_files_in_directory(args.path)
        print(f"Number of image files after third iteration: {count}")

    print("All processes completed.")

# shell 예시
# import subprocess
# import time
# # 기본 경로 및 범위 설정
# base_path = '../datasets/reds_upscale_120fps/part3/'
# start = 45
# end = 59

# # 반복 실행
# for i in range(start, end + 1):
#     input_path = f"{base_path}{i:03d}"
#     output_path = f"{input_path}/new"
    
#     command = f"python benchmark/gopro.py --path {input_path} --newpath {output_path}"
#     print(f"Executing: {command}")
    
#     try:
#         # subprocess를 사용하여 명령어 실행
#         result = subprocess.run(command, shell=True, check=True)
        
#         # 성공적으로 실행되었는지 확인
#         if result.returncode == 0:
#             print(f"Successfully executed for: {input_path}")
#         else:
#             print(f"Failed to execute for: {input_path}")
    
#     except subprocess.CalledProcessError as e:
#         print(f"Error occurred while processing {input_path}: {e}")

#     # 각 명령어 실행 후 잠시 대기
#     time.sleep(1)     