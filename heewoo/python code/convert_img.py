import cv2
import glob
import os
import sys
import numpy as np

# 이미지 개수 맞추기 및 정렬 저장 경로
RAW_PATH = 'E:\\AI_data\\test_set\\'
TRAINING_PATH = 'E:\\AI_data\\test_set\\test_set\\'
OBJECTS = ['cat', 'fish'] # ['bird', 'car', 'cat', 'dog', 'fish']

min_n = 0

def object_s(ob):
    """객체 이름에 복수형 접미사 추가"""
    return ob

def num(filepath):
    """주어진 경로의 이미지 개수 반환"""
    return len(glob.glob(filepath + '\\*.jpg'))

def initialize_objects():
    """객체 목록 초기화 및 이미지 경로 생성"""
    objects_s = [object_s(obj) for obj in OBJECTS]
    objects_p_raw_old = [RAW_PATH + obj_s for obj_s in objects_s]
    print(objects_p_raw_old)
    objects_n_raw = [num(old_path) for old_path in objects_p_raw_old]
    objects_p_raw_new = [RAW_PATH + obj for obj in OBJECTS]
    return objects_s, objects_p_raw_old, objects_n_raw, objects_p_raw_new

def create_new_folder(filepath_new):
    """새 폴더 생성"""
    if not os.path.exists(filepath_new):
        os.makedirs(filepath_new)
        print(f"{filepath_new} 폴더 생성완료")
    else:
        print(f"{filepath_new} 폴더가 이미 존재합니다.")

def array_in_new_folder(ob_n, filepath_old, filepath_new, filename):
    """새 파일 만들어 파일 번호 붙여 재정렬"""
    create_new_folder(filepath_new)
    files = glob.glob(filepath_old + '/*.jpg')

    if len(files) < ob_n:
        print(f"{filename}의 이미지 개수가 부족합니다. {len(files)}개만 사용합니다.")
        ob_n = len(files)  # 실제 파일 수에 맞추기

    for i in range(ob_n):
        img = cv2.imread(files[i])
        if img is not None:
            output_path = f'{filepath_new}/{filename}{i + 1}.jpg'
            success = cv2.imwrite(output_path, img)
            if success:
                print(f"{output_path} 저장완료")
            else:
                print(f"{output_path} 저장실패")
        else:
            print(f"{files[i]}를 읽는 데 실패했습니다.")

def remove_files(ob_n, filepath, filename, min_n):
    """파일 삭제"""
    for i in range(ob_n - min_n):
        try:
            os.remove(f'{filepath}/{filename}{i + 1}.jpg')
            print(f"{filename}{i + 1}.jpg 삭제완료")
        except FileNotFoundError:
            print(f"파일 {filename}{i + 1}.jpg를 찾을 수 없습니다.")
    if len(glob.glob(filepath + '/*')) == min_n:
        print(f"{filename} 삭제완")

def crop_and_gray(filepath_old, filepath_new, filename):
    """흑백 변환 및 크롭"""
    create_new_folder(filepath_new)
    img_files = glob.glob(f'{filepath_old}\\*.jpg')

    if not img_files:
        print("이미지 없음")
        sys.exit()

    for i in range(min_n):
        img = cv2.imread(img_files[i])
        if img is None:
            print("이미지를 불러오는 데 실패했습니다.")
            continue

        percent = 128 / max(img.shape[:2])
        img = cv2.resize(img, dsize=(0, 0), fx=percent, fy=percent, interpolation=cv2.INTER_LINEAR)

        h, w = img.shape[:2]
        w_x = max((128 - w) // 2, 0)
        h_y = max((128 - h) // 2, 0)

        M = np.float32([[1, 0, w_x], [0, 1, h_y]])
        crop_image = cv2.warpAffine(img, M, (128, 128))

        if crop_image.shape == (128, 128, 3):
            print("변형성공")

        output_path = f'{filepath_new}\\{filename}{i + 1}.jpg'
        success = cv2.imwrite(output_path, crop_image)
        if success:
            print(f"{output_path} 저장완료")
        else:
            print(f"{output_path} 저장실패")

# 메인 실행 부분
objects_s, objects_p_raw_old, objects_n_raw, objects_p_raw_new = initialize_objects()
min_n = min(objects_n_raw)
print(min_n)

for i in range(len(OBJECTS)):
    array_in_new_folder(objects_n_raw[i], objects_p_raw_old[i], objects_p_raw_new[i], OBJECTS[i])
    remove_files(objects_n_raw[i], objects_p_raw_new[i], OBJECTS[i], min_n)
    objects_n_raw[i] = num(objects_p_raw_new[i])  # 사진 개수 갱신

print(objects_n_raw)

for i in range(len(OBJECTS)):
    crop_and_gray(objects_p_raw_new[i], TRAINING_PATH + OBJECTS[i], OBJECTS[i])