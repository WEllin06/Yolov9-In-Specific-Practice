# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from os import getcwd

# 数据集的子集
sets = ['train', 'val']
# 自定义类别
classes = ["fry"]
# 获取当前工作目录
abs_path = os.getcwd()
print(abs_path)


def convert(size, box):
    """
    将标注的边界框坐标转换为 YOLO 格式
    :param size: 图片的宽和高
    :param box: 边界框的坐标 (xmin, xmax, ymin, ymax)
    :return: 转换后的坐标 (x, y, w, h)
    """
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(image_id, in_dir, out_dir):
    """
    将单个 XML 文件转换为 YOLO 格式的 TXT 文件
    :param image_id: 图片的 ID
    :param in_dir: 输入 XML 文件的目录
    :param out_dir: 输出 TXT 文件的目录
    """
    in_file_path = os.path.join(in_dir, f'{image_id}.xml')
    out_file_path = os.path.join(out_dir, f'{image_id}.txt')

    try:
        in_file = open(in_file_path, encoding='UTF-8')
    except FileNotFoundError:
        print(f"文件 {in_file_path} 不存在，请检查路径和文件名。")
        return

    with open(out_file_path, 'w') as out_file:
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (
                float(xmlbox.find('xmin').text),
                float(xmlbox.find('xmax').text),
                float(xmlbox.find('ymin').text),
                float(xmlbox.find('ymax').text)
            )
            b1, b2, b3, b4 = b

            # 标注越界修正
            if b2 > w:
                b2 = w
            if b4 > h:
                b4 = h
            b = (b1, b2, b3, b4)

            bb = convert((w, h), b)
            out_file.write(f"{cls_id} {' '.join(map(str, bb))}\n")


def process_dataset(sets, in_dir, out_dir, img_dir):
    """
    处理整个数据集，将 XML 文件转换为 YOLO 格式
    :param sets: 数据集的子集列表
    :param in_dir: 输入 XML 文件的目录
    :param out_dir: 输出 TXT 文件的目录
    :param img_dir: 图像文件的目录
    """
    # 创建标签目录（如果不存在）
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for image_set in sets:
        image_ids_path = os.path.join(img_dir, f'{image_set}.txt')
        if not os.path.exists(image_ids_path):
            print(f"文件 {image_ids_path} 不存在，请检查路径和文件名。")
            continue

        with open(image_ids_path) as f:
            image_ids = f.read().strip().split()

        list_file_path = os.path.join(getcwd(), f'{image_set}.txt')

        with open(list_file_path, 'w') as list_file:
            for image_id in image_ids:
                list_file.write(f'{os.path.join(img_dir, image_id)}.jpg\n')
                convert_annotation(image_id, in_dir, out_dir)


# 设置目录路径
xml_dir = r'D:\Desktop\YOLOv9\data\Annotations'
labels_dir = r'D:\Desktop\YOLOv9\data\labels'
images_dir = r'D:\Desktop\YOLOv9\data\images'

# 处理数据集
process_dataset(sets, xml_dir, labels_dir, images_dir)
