import cv2
import glob
import os
import sys
import numpy as np
import random

#뒤에 '#'표시만 있는 코드: 실행 확인용

#1. 이미지 개수 맞추기
#2. 이미지 증식 함수
#3. 이미지 변환 함수
#4. 이미지 정렬해 저장

##1. 이미지 개수 맞추기##
raw_path = 'E:\AI_data\ques\ordinary_test'

def object_s(ob):
    return ob

#폴더 속 이미지 개수 세기
def num(filepath):
    return len(glob.glob(filepath + '/*'))

objects = ['bird', 'car', 'cat', 'dog', 'fish']
objects_s = [] #ex) 'birds'
objects_p_raw_old = [] #변형전, 삭제전 사진 경로
objects_n_raw = [] #변형전, 삭제전 사진 개수
objects_p_raw_new = [] #변형전, 삭제후 사진 경로(재정렬에 필요)
for i in range(5):
    objects_s.append(object_s(objects[i]))
    objects_p_raw_old.append(raw_path + "\\" + objects_s[i])
    #ex)'raw_images/birds'폴더
    objects_n_raw.append(num(objects_p_raw_old[i]))
    objects_p_raw_new.append(raw_path + "\\" + objects[i])
    #ex)'raw_images/bird'폴더(임시로 정렬)
    
min_n = min(objects_n_raw) #개수비교, 최소 구하기

for i in range(5):
    print(objects_n_raw[i])

#새 폴더 생성 후 파일 번호 붙여 재정렬
def array_in_new_folder(ob_n, filepath_old, filepath_new, filename): 
    file = glob.glob(filepath_old + '/*.jpg')
    os.mkdir(filepath_new)
    for i in range(ob_n):
        img = cv2.imread(file[i])
        cv2.imwrite(f'{filepath_new}/{filename}{i+1}.jpg', img)
    print("정렬완") #

#파일 삭제
def removefiles(ob_n, filepath, filename):
    for i in range(ob_n - min_n):
        os.remove(f'{filepath}/{filename}{i+1}.jpg')
    if len(glob.glob(filepath + '/*')) == min_n:
        print("삭제완") #
        
for i in range(5):
    array_in_new_folder(objects_n_raw[i], objects_p_raw_old[i],
                        objects_p_raw_new[i], objects[i])
    removefiles(objects_n_raw[i], objects_p_raw_new[i], objects[i])
    objects_n_raw[i] = num(objects_p_raw_new[i]) #사진개수 갱신

print(objects_n_raw[0], objects_n_raw[1], objects_n_raw[2],
      objects_n_raw[3], objects_n_raw[4]) #

##2. 이미지 변환 후 정렬해 저장##
training_path = 'E:\AI_data\ord_test_set'

objects_p_train = [] #변환후 사진 경로

for i in range(5):
    objects_p_train.append(training_path + "\\" + objects[i])
    #ex)'training_set/bird'

def crop(filepath_old, filepath_new, filename):
    os.mkdir(filepath_new)
    
    img_files = glob.glob(f'{filepath_old}/*.jpg')
    
    if not img_files:
        print("이미지 없음")
        sys.exit()

    for i in range(min_n):
        img = cv2.imread(img_files[i])
        if img is None:
            print("이미지를 불러오는 데 실패했습니다.")

        #이미지의 x, y가 128이 넘을 경우 작게해주기
        percent = 1
        if(img.shape[1] > img.shape[0]):
            percent = 128/img.shape[1]
        else:
            percent = 128/img.shape[0]

        img = cv2.resize(img, dsize=(0, 0), fx=percent, fy=percent,
                         interpolation=cv2.INTER_LINEAR)

        #이미지 범위 지정
        y, x, h, w = (0, 0, img.shape[0], img.shape[1])

        #그림 주변에 검은색으로 칠하기
        w_x = (128-(w-x))/2
        h_y = (128-(h-y))/2

        if(w_x < 0):
            w_x = 0
        elif(h_y < 0):
            h_y = 0

        M = np.float32([[1, 0, w_x], [0, 1, h_y]]) #(2*3 이차원 행렬)
        crop_image = cv2.warpAffine(img, M, (128, 128))
        if crop_image.shape[0] == 128 and crop_image.shape[1] == 128:
            print("변형성공") #

        cv2.imwrite(f'{filepath_new}/{filename}{str(i+1).zfill(len(str(min_n)))}.jpg', crop_image)

for i in range(5):
    crop(objects_p_raw_new[i], objects_p_train[i], objects[i])

##3. 이미지 증식, 저장##
# 함수 총 3개 (반전, 회전, 밝기조절)
# 원본 이미지를 받으면 변형한 이미지가 담긴 리스트를 반환
# 1개 이미지를 10개로 늘려줌

# 3-1. 반전 (3개)
# 좌우반전, 상하반전, 상하좌우 반전
def flip_img(img) :
    f_images = []
    for i in [-1, 0, 1] :
        f_images.append(cv2.flip(img, i))
    return f_images

# 3-2. 회전 (3개)
# 90도, 180도, 270도 회전
def rotate_img(img) :
    r_images = []
    r_images.append(cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE))
    r_images.append(cv2.rotate(img, cv2.ROTATE_180))
    r_images.append(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
    return r_images

# 3-3. 밝기 조절 (4개)
# 무작위로 밝기 설정
# 어두운 이미지 2개, 밝은 이미지 2개 저장
def bright_img(img) :
    b_images = []
    i = 0
    for _ in range(2):
        val = random.randrange(10, 101)         # 무작위로 밝기 설정
        b_images.append(cv2.subtract(img, val)) # 어두워진 이미지 추가
        b_images.append(cv2.add(img, val))      # 밝아진 이미지 추가
    return b_images

#모든 변형된 이미지 취합 후 저장
def save(filepath, filename):
    img_files = glob.glob(f'{filepath}/*.jpg')
    
    if not img_files:
        print("이미지 없음")
        sys.exit()

    for i in range(min_n):
        img = cv2.imread(img_files[i])
        if img is None:
            print("이미지를 불러오는 데 실패했습니다.")
    
        imgs = flip_img(img) + rotate_img(img) + bright_img(img)
        for j in range(10):
            cv2.imwrite(f'{filepath}/{filename}{str(i+1).zfill(len(str(min_n)))}_{j+1}.jpg', imgs[j])

for i in range(5):
    save(objects_p_train[i], objects[i])

#crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY) 흑백변환이었으나 빼버림



