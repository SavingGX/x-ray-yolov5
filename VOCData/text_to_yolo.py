# -*- coding: utf-8 -*-
import os

# 数据集划分（train, val, test）
sets = ['train', 'val', 'test']

# 获取当前工作目录（确保脚本在 yolo_dataset 目录下运行）
wd = os.getcwd()
print(f"当前工作目录：{wd}")

# 创建输出文件夹
output_dir = 'dataSet_path'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ImageSets/Main 路径（包含 train.txt, val.txt, test.txt）
image_sets_dir = 'ImageSets/Main'

# 图像根目录（images/train 和 images/test）
images_train_dir = 'images/train'
images_test_dir = 'images/test'  # 如果 test 集有 test 子文件夹

for image_set in sets:
    # 打开对应的 txt 文件（如 ImageSets/Main/train.txt）
    list_file_path = os.path.join(image_sets_dir, f'{image_set}.txt')
    if not os.path.exists(list_file_path):
        print(f"警告: 文件 {list_file_path} 不存在，跳过处理")
        continue

    with open(list_file_path, encoding='utf-8') as f:
        image_ids = f.read().strip().split()

    # 写入 dataSet_path/train.txt 等文件
    output_file = os.path.join(output_dir, f'{image_set}.txt')
    with open(output_file, 'w', encoding='utf-8') as list_file:
        for image_id in image_ids:
            # 判断属于 train 还是 test（假设 val 属于 train）
            if image_set in ['train', 'val']:
                img_path = os.path.join(wd, 'images', 'train', f'{image_id}.jpg')
            elif image_set == 'test':
                img_path = os.path.join(wd, 'images', 'test', f'{image_id}.jpg')
            else:
                continue

            # 检查图像是否存在（可选）
            if not os.path.exists(img_path):
                print(f"警告: 图像文件 {img_path} 不存在")

            # 写入图像路径
            list_file.write(f'{img_path}\n')

    print(f"已生成 {output_file}")
