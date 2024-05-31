import os  # 导入操作系统相关模块
import random  # 导入随机数生成模块
import argparse  # 导入命令行参数解析模块


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="划分数据集并生成训练、验证和测试集的文件列表")
    parser.add_argument('--xml_path', default=r'D:\Desktop\YOLOv9\data\Annotations', type=str, help='输入 XML 标签路径')
    parser.add_argument('--txt_path', default=r'D:\Desktop\YOLOv9\data\images', type=str, help='输出 TXT 标签路径')
    return parser.parse_args()  # 返回解析后的命令行参数


def create_dir_if_not_exists(path):
    """如果路径不存在，则创建它"""
    if not os.path.exists(path):  # 检查路径是否存在
        os.makedirs(path)  # 创建目录及其所有父目录


def write_to_file(file, filenames):
    """将文件名列表写入文件"""
    with open(file, 'w') as f:  # 以写模式打开文件
        for name in filenames:  # 遍历文件名列表
            f.write(name + '\n')  # 将文件名写入文件，并在末尾添加换行符


def main():
    # 解析命令行参数
    opt = parse_args()

    # 数据划分比例
    trainval_percent = 0.9  # 训练集和验证集的总比例
    train_percent = 0.8  # 训练集中训练数据的比例

    # 获取 XML 文件路径和输出 TXT 文件路径
    xmlfilepath = opt.xml_path
    txtsavepath = opt.txt_path

    # 获取 XML 文件夹下的所有文件名（不包括扩展名）
    total_xml = [f[:-4] for f in os.listdir(xmlfilepath) if f.endswith('.xml')]

    # 如果输出目录不存在，则创建该目录
    create_dir_if_not_exists(txtsavepath)

    # 总文件数量
    num = len(total_xml)  # 计算 XML 文件的总数量
    list_index = list(range(num))  # 生成文件索引列表

    # 计算训练+验证集数量和训练集数量
    tv = int(num * trainval_percent)  # 训练+验证集的数量
    tr = int(tv * train_percent)  # 训练集的数量

    # 随机抽取训练+验证集和训练集
    trainval = random.sample(list_index, tv)  # 随机选择 tv 个文件作为训练+验证集
    train = random.sample(trainval, tr)  # 从训练+验证集中随机选择 tr 个文件作为训练集

    # 分配文件名到对应的集合
    trainval_files = [total_xml[i] for i in trainval]  # 获取训练+验证集文件名
    test_files = [total_xml[i] for i in list_index if i not in trainval]  # 获取测试集文件名
    train_files = [total_xml[i] for i in train]  # 获取训练集文件名
    val_files = [total_xml[i] for i in trainval if i not in train]  # 获取验证集文件名

    # 定义文件路径
    trainval_path = os.path.join(txtsavepath, 'trainval.txt')  # 训练+验证集文件路径
    test_path = os.path.join(txtsavepath, 'test.txt')  # 测试集文件路径
    train_path = os.path.join(txtsavepath, 'train.txt')  # 训练集文件路径
    val_path = os.path.join(txtsavepath, 'val.txt')  # 验证集文件路径

    # 将文件名写入对应的 TXT 文件中
    write_to_file(trainval_path, trainval_files)  # 写入训练+验证集文件名
    write_to_file(test_path, test_files)  # 写入测试集文件名
    write_to_file(train_path, train_files)  # 写入训练集文件名
    write_to_file(val_path, val_files)  # 写入验证集文件名


if __name__ == "__main__":
    main()  # 运行主函数
