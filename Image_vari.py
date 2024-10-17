import cv2
import glob
import sys
import random

## 함수 총 3개 (반전, 회전, 밝기조절) ##
## 원본 이미지를 받으면 변형한 이미지가 담긴 리스트를 반환
## 1개 이미지를 10개로 늘려줌

# 1. 반전 (3개)
# 좌우반전, 상하반전, 상하좌우 반전
def flip_img(img) :
    f_images = []
    for i in [-1, 0, 1] :
        f_images.append(cv2.flip(img, i))
    return f_images

# 2. 회전 (3개)
# 90도, 180도, 270도 회전
def rotate_img(img) :
    r_images = []
    r_images.append(cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE))
    r_images.append(cv2.rotate(img, cv2.ROTATE_180))
    r_images.append(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
    return r_images

# 3. 밝기 조절 (4개)
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