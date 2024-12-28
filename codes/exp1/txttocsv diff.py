import os
import csv
import re

# 设置文件夹路径（包含所有 TXT 文件的文件夹）
base_folder = r'../../result'  # 主文件夹路径
color = 'rainbow'

# 获取所有符合条件的文件路径（假设所有 txt 文件都在 result/1, result/2, ... result/20 文件夹下）
txt_files = []
for i in range(1, 21):  # 假设有 20 个文件夹，每个文件夹中有一个 gray_result.txt 文件
    folder_path = os.path.join(base_folder, str(i))
    txt_file_path = os.path.join(folder_path, f'{color}_result.txt')  # 每个文件夹中的 gray_result.txt 文件路径
    if os.path.exists(txt_file_path):  # 确保文件存在
        txt_files.append(txt_file_path)

# 创建一个空列表来存储每个 TXT 文件的计算结果
txt_data = []

# 正则表达式模式，用于提取行中的前后两个数字
pattern = re.compile(r'(-?\d*\.\d+):.*-?\s*(\d*\.\d+)')  # 提取前后两个浮动数字

# 读取每个 TXT 文件的内容
for txt_file in txt_files:
    with open(txt_file, 'r', encoding='utf-8') as file:
        content = file.readlines()  # 读取所有行
        # 提取每行中的前后两个数值，并计算它们的差值的绝对值
        extracted_values = []
        for line in content:
            match = pattern.search(line)  # 查找符合模式的数值
            if match:
                # 提取前后两个数值并计算它们的差值的绝对值
                first_value = float(match.group(1))  # 第一个数字
                second_value = float(match.group(2))  # 第二个数字
                absolute_diff = abs(first_value - second_value)  # 计算差值的绝对值
                extracted_values.append(absolute_diff)
            else:
                extracted_values.append('')  # 若没有匹配到，填充空值
        txt_data.append(extracted_values)

# 确保每个文件的数据的行数一致
max_length = max(len(column) for column in txt_data)
for column in txt_data:
    column.extend([''] * (max_length - len(column)))  # 填充不足的部分

# 将数据写入 CSV 文件
csv_filename = f'../../result\data\{color}_diff.csv'  # 输出的 CSV 文件路径
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    # 将计算结果写入 CSV 文件
    for row in zip(*txt_data):  # 使用 zip(*txt_data) 将每列内容组合成一行
        writer.writerow(row)

print(f"已将所有 TXT 文件的差值绝对值保存到 {csv_filename}")
