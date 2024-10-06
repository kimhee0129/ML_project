import cv2
import os

def convert_to_grayscale(image_dir, output_dir):
    # ��� ���丮�� ������ ����
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # ���丮 �� ��� ���� Ž��
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):  # �̹��� ���� Ȯ���� ���͸�
                image_path = os.path.join(root, file)
                
                # �̹����� ������� ��ȯ �� ���� ��� ����
                rel_path = os.path.relpath(image_path, image_dir)  # ��� ��� ���
                save_path = os.path.join(output_dir, os.path.splitext(rel_path)[0] + ".png")  # ���� ��� (PNG Ȯ���ڷ� ����)
                
                # ������ ������ ������ ����
                save_dir = os.path.dirname(save_path)
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                # �̹��� �б� �� ��� ��ȯ �� ����
                image = cv2.imread(image_path)
                if image is None:
                    print(f"Image not found: {image_path}")
                    continue
                
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(save_path, gray_image)
                print(f"Grayscale image saved to {save_path}")


# ����ڰ� ��δ� ���� �������־�� ��.
# �̹��� ���丮�� ������ ���丮 ��� ����
image_directory = "D:/test_data_set"
output_directory = "D:/output_grayscale_images"

convert_to_grayscale(image_directory, output_directory)
