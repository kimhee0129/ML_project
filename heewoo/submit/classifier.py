import torch
from torchvision.models import resnet18, ResNet18_Weights
from torch import nn
import numpy as np
import os, cv2

inputFile_path = os.path.join(os.getcwd(), "images") ## 변경 필요 ##

label2str = { 0 : "새",
              1 : "자동차",
              2 : "고양이",
              3 : "개",
              4 : "물고기" }

class Res18Net(nn.Module):
    def __init__(self):
        super(Res18Net, self).__init__()
        self.model = resnet18(weights=ResNet18_Weights.DEFAULT)
        self.model.conv1 = nn.Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 5)

    def forward(self, x):
        x = self.model(x)
        return x


def main():
    data_x = path2tensor(inputFile_path)

    data_x = np.array(data_x)
    data_x = torch.tensor(data_x, dtype=torch.float32)

    device = torch.device('cpu')
    model = Res18Net()
    model.load_state_dict(torch.load("model.wgt", map_location=device))

    pred_data = []

    model.eval()

    with torch.no_grad():
        inputs = data_x.to(device)
        outputs = model(inputs)

        _, predicted = torch.max(outputs, 1)
        pred_data.extend(predicted.cpu().numpy())
    
    save_data(pred_data)
    print("예측 파일을 성공적으로 생성했습니다.")

def path2tensor(path):
    data_x = []
    
    for i in range(1, 101):
        f = os.path.join(path, f"{i:03}.jpg")
        img = cv2.imread(f).astype(np.float32) / 255
        img = np.transpose(img, (2, 0, 1))
        data_x.append(img)

    return data_x

def save_data(pred_data):
    with open("res_0반_0팀.txt", 'w') as f:
        for i in range(1, 101):
            f.write(f"{i:03} : {label2str[pred_data[i-1]]}\n")

if __name__ == "__main__":
    main()