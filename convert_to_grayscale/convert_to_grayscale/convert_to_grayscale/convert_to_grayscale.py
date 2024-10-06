import cv2
import os

def convert_to_grayscale(image_dir, output_dir):
    # 출력 디렉토리가 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 디렉토리 내 모든 파일 탐색
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):  # 이미지 파일 확장자 필터링
                image_path = os.path.join(root, file)
                
                # 이미지를 흑백으로 변환 및 저장 경로 생성
                rel_path = os.path.relpath(image_path, image_dir)  # 상대 경로 계산
                save_path = os.path.join(output_dir, os.path.splitext(rel_path)[0] + ".png")  # 저장 경로 (PNG 확장자로 변경)
                
                # 저장할 폴더가 없으면 생성
                save_dir = os.path.dirname(save_path)
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                # 이미지 읽기 및 흑백 변환 후 저장
                image = cv2.imread(image_path)
                if image is None:
                    print(f"Image not found: {image_path}")
                    continue
                
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(save_path, gray_image)
                print(f"Grayscale image saved to {save_path}")


# 사용자가 경로는 직접 지정해주어야 함.
# 이미지 디렉토리와 저장할 디렉토리 경로 설정
image_directory = "D:/test_data_set"
output_directory = "D:/output_grayscale_images"

convert_to_grayscale(image_directory, output_directory)
