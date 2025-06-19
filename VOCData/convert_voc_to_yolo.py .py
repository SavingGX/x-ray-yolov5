import os

# 类别映射（根据你的实际类别修改）
class_mapping = {
    'Mobile_Phone': 1,
    'Laptop': 2,
    'Portable_Charger_2': 3,
    'Portable_Charger_1': 4,
    'Tablet': 5,
    'Cosmetic': 6,
    'Water': 7,
    'Nonmetallic_Lighter': 0,
}

def convert_bbox(img_w, img_h, x_min, y_min, x_max, y_max):
    """
    将左上角+右下角坐标转换为YOLOv5所需的中心点+宽高（归一化）
    """
    xc = (x_min + x_max) / 2.0 / img_w
    yc = (y_min + y_max) / 2.0 / img_h
    w = (x_max - x_min) / img_w
    h = (y_max - y_min) / img_h
    return [xc, yc, w, h]

def convert_label_file(input_path, output_path, img_w=640, img_h=640):
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            parts = line.strip().split()
            if len(parts) != 6:
                continue  # 忽略不合法行
            _, class_name, xmin, ymin, xmax, ymax = parts
            class_id = class_mapping.get(class_name)
            if class_id is None:
                print(f"警告: 类别 {class_name} 未在映射表中定义")
                continue
            try:
                xmin = int(xmin)
                ymin = int(ymin)
                xmax = int(xmax)
                ymax = int(ymax)
            except ValueError:
                print(f"警告: 坐标不是整数: {line}")
                continue

            bbox = convert_bbox(img_w, img_h, xmin, ymin, xmax, ymax)
            line_out = f"{class_id} {' '.join(map(str, bbox))}\n"
            outfile.write(line_out)

def batch_convert_labels(input_dir, output_dir, img_size=(640, 640)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            convert_label_file(input_path, output_path, *img_size)

if __name__ == "__main__":
    # 修改为你自己的路径
    train_label_dir = "labels/train"
    test_label_dir = "labels/test"
    output_train_dir = "labels/train_yolo"
    output_test_dir = "labels/test_yolo"

    # 转换训练集标签
    batch_convert_labels(train_label_dir, output_train_dir)

    # 转换测试集标签
    batch_convert_labels(test_label_dir, output_test_dir)

    print("✅ 标签转换完成！")
