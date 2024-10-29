import cv2, glob, os, sys, random
import numpy as np
min_n = 0;

def num(filepath):
    return len(glob.glob(filepath + '/*'))

def array_in_new_folder(ob_n, filepath_old, filepath_new, filename): 
    file = glob.glob(filepath_old + '/*.jpg')
    os.mkdir(filepath_new)
    for i in range(ob_n):
        img = cv2.imread(file[i])
        cv2.imwrite(f'{filepath_new}/{filename}{i+1}.jpg', img)
    print("정렬완") 

def removefiles(ob_n, filepath, filename):
    for i in range(ob_n - min_n):
        os.remove(f'{filepath}/{filename}{i+1}.jpg')
    if len(glob.glob(filepath + '/*')) == min_n:
        print("삭제완") #

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
            pass
            #print("변형성공") #

        cv2.imwrite(f'{filepath_new}/{filename}{str(i+1).zfill(len(str(min_n)))}_0.jpg', crop_image)

def flip_img(img) :
    f_images = []
    for i in [-1, 0, 1] :
        f_images.append(cv2.flip(img, i))
    return f_images

def rotate_img(img) :
    r_images = []
    r_images.append(cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE))
    r_images.append(cv2.rotate(img, cv2.ROTATE_180))
    r_images.append(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
    return r_images

def bright_img(img) :
    b_images = []
    i = 0
    for _ in range(2):
        val = random.randrange(10, 101)         # 무작위로 밝기 설정
        b_images.append(cv2.subtract(img, val)) # 어두워진 이미지 추가
        b_images.append(cv2.add(img, val))      # 밝아진 이미지 추가
    return b_images

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

source_path = "E:\AI_data\ques\strange_test"
new_path = "E:\AI_data\stra_test_set"

def main():
    global min_n
    classes = ["bird", "car", "cat", "dog", "fish"]
    n_classes = [0 for i in range(5)]
    for i in range(5):
        n_classes[i] = num(os.path.join(source_path, classes[i]))
    min_n = min(n_classes)
    print(n_classes)

    for c in classes:
        sp = os.path.join(source_path, c)
        np = os.path.join(new_path, c)
        crop(sp, np, c)
        #save(np, c)

main()
print("successfully completed!")