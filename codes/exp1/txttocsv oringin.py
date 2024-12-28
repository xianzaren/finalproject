import os
import openpyxl
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

# 创建一个空列表来存储每个 TXT 文件的内容（提取的数值）
txt_data = []

# 正则表达式模式，用于提取数值（最后一个数值）
pattern = re.compile(r'-?\d*\.\d+$')  # 匹配行末的浮动数字，支持负号

# 读取每个 TXT 文件的内容
for txt_file in txt_files:
    with open(txt_file, 'r', encoding='utf-8') as file:
        content = file.readlines()  # 读取所有行
        # 提取每行中的最后一个数值
        extracted_values = []
        for line in content:
            match = pattern.search(line)  # 查找符合模式的数值
            if match:
                extracted_values.append(match.group())  # 提取到的数值
            else:
                extracted_values.append('')  # 若没有匹配到，填充空值
        txt_data.append(extracted_values)

# 确保每个文件的数据的行数一致
max_length = max(len(column) for column in txt_data)
for column in txt_data:
    column.extend([''] * (max_length - len(column)))  # 填充不足的部分

# 创建 Excel 工作簿并保存数据
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "TXT Data"

# 将每个 TXT 文件的提取值写入不同的列
for col_idx, column in enumerate(txt_data, start=1):
    for row_idx, value in enumerate(column, start=1):
        ws.cell(row=row_idx, column=col_idx, value=value)

# 保存到 Excel 文件
excel_filename = f'../../result//data//{color}.xlsx'  # 输出的 Excel 文件路径
wb.save(excel_filename)

print(f"已将所有 TXT 文件的提取数值保存到 {excel_filename}")
