
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

def process_images_before(start, end, folder_path, gamma=2.2):
    # 이미지 로드 및 평균
    images = []
    for i in range(start, end):
        img_path = os.path.join(folder_path, f"{i:05d}.png")
        img =cv2.imread(img_path)
        if img is not None:
            images.append(img)
        else:
            print(f"image {img_path} not found")
            
    if not images:
        print("No images were loaded")
        return
    
    # 평균 이미지 계산
    average_image = np.mean(images, axis=0).astype(np.uint8)
    
    # 감마 보정
    # blurred_images = gamma_correction(average_image, gamma)
    
    # recovered_image = inverse_gamma_correction(blurred_images, gamma)
        
    # 결과 이미지 저장
    output_path = os.path.join(folder_path, f"average_{start:05d}_to_{end:05d}.png")
    
    cv2.imwrite(output_path, average_image)
    # cv2.imwrite(output_path, average_image)
    print(f"Blurred image saved to {output_path}")
    
def process_images(start, end, folder_path, gamma=2.2):
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
    if not os.path.exists(image_out):
        os.makedirs(image_out)
        print(f"Directory {image_out} was created.")
    # output_path = os.path.join(folder_path, f"recovered_{start:05d}_to_{end:05d}.png")
    output_path = os.path.join(image_out, f"recovered_{start:05d}_to_{end:05d}.png")
    cv2.imwrite(output_path, recovered_image)
    print(f"Recovered image saved to {output_path}")
    
# 사용 예
folder_path = './gopro_film/GX013503_cam_shake_4k_120fps'  # 이미지가 저장된 폴더 경로
image_out = './gopro_film/output_g_a_g_7_GX013503_cam_shake_4k_120fps'
total_images = 560
batch_size = 7

for start in range(1, total_images + 1, batch_size):
    end = min(start + batch_size - 1, total_images)
    process_images(start, end, folder_path)

# import cv2
# import numpy as np
# import os

# def gamma_correction(image, gamma=2.2):
#     # 감마 보정을 위한 룩업 테이블 생성
#     invGamma = 1.0 / gamma
#     table = np.array([((i / 255.0) ** invGamma) * 255 for i in range(256)]).astype("uint8")
#     # 보정 적용
#     return cv2.LUT(image, table)

# def process_images(start, end, folder_path, gamma=2.2):
#     # 이미지 로드 및 평균 계산
#     images = []
#     for i in range(start, end):
#         img_path = os.path.join(folder_path, f"{i:05d}.png")  # 파일명 포맷 맞춤
#         img = cv2.imread(img_path)
#         if img is not None:
#             images.append(img)
#         else:
#             print(f"Image {img_path} not found.")
    
#     if not images:
#         print("No images were loaded.")
#         return
    
#     # 평균 이미지 계산
#     average_image = np.mean(images, axis=0).astype(np.uint8)
    
#     # 감마 보정 적용
#     blurred_image = gamma_correction(average_image, gamma)
    
#     # 결과 이미지 저장
#     output_path = os.path.join(folder_path, f"blurred_{start:05d}_to_{end:05d}.png")
#     cv2.imwrite(output_path, blurred_image)
#     print(f"Blurred image saved to {output_path}")

# # 사용 예
# folder_path = '/path/to/images'  # 이미지가 저장된 폴더 경로
# total_images = 999
# batch_size = 7

# for start in range(1, total_images + 1, batch_size):
#     end = min(start + batch_size - 1, total_images)
#     process_images(start, end, folder_path)
