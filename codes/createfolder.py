import os

# 指定父目录路径
base_path = r"../result\exp3"  # 替换为你实际的目录路径

# 创建 1 到 20 的文件夹
for i in range(1, 21):
    folder_name = os.path.join(base_path, str(i))  # 合成文件夹的完整路径

    # 如果文件夹不存在则创建
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)  # 创建多级目录
        print(f"文件夹 {folder_name} 创建成功")
    else:
        print(f"文件夹 {folder_name} 已存在")
