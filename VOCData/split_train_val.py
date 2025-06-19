# coding:utf-8

import os
import random
import argparse

parser = argparse.ArgumentParser()
# 输出txt文件的保存路径，默认为 ImageSets/Main
parser.add_argument('--txt_path', default='ImageSets/Main', type=str, help='output txt label path')
opt = parser.parse_args()

# 数据划分比例
trainval_percent = 1.0  # 所有 train 数据中划分为 train + val（这里不使用 test）
train_percent = 0.9     # 其中 90% 用作 train，10% 用作 val
txtsavepath = opt.txt_path

# 图像和标签路径设置（只处理 train 目录中的图像）
image_dir = 'images/train'  # 修改为你自己的 train 图像路径
label_dir = 'labels/train'  # 修改为你自己的 train 标签路径

# 获取所有训练图像文件名（去除扩展名）
image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
image_files = [os.path.splitext(f)[0] for f in image_files]

if not os.path.exists(txtsavepath):
    os.makedirs(txtsavepath)

num = len(image_files)
list_index = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list_index, tv)
train = random.sample(trainval, tr)

# 创建并写入列表文件
file_trainval = open(os.path.join(txtsavepath, 'trainval.txt'), 'w')
file_test = open(os.path.join(txtsavepath, 'test.txt'), 'w')
file_train = open(os.path.join(txtsavepath, 'train.txt'), 'w')
file_val = open(os.path.join(txtsavepath, 'val.txt'), 'w')

for i in list_index:
    name = image_files[i] + '\n'
    if i in trainval:
        file_trainval.write(name)
        if i in train:
            file_train.write(name)
        else:
            file_val.write(name)
    else:
        file_test.write(name)

file_trainval.close()
file_train.close()
file_val.close()
file_test.close()

print(f"共 {num} 张训练图像")
print(f"已生成 trainval.txt, train.txt, val.txt 到 {txtsavepath}")
