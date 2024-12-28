import os
import shutil

def save_images_to_group_folders(groups, frequencies, colormaps, base_output_dir):
    for group_id, group in enumerate(groups, start=1):  # 遍历每组
        # 创建对应的组文件夹
        group_folder = os.path.join(base_output_dir, str(group_id))
        os.makedirs(group_folder, exist_ok=True)
        # 记录该组的图像
        selected_images = []
        for number in group:  # 遍历组内的每个数字
            for frequency in frequencies:  # 遍历频率
                for colormap in colormaps:  # 遍历 colormap
                    # 根据规则生成图像名称
                    image_name = f"ScalarField_WithBoxes_Noise_(630, 820)_({frequency}, {frequency})_5_{colormap}_{number}.png"
                    selected_images.append(image_name)
        # 保存图像列表到组文件夹中的文件
        image_list_file = os.path.join(group_folder, "images.txt")
        with open(image_list_file, "w") as file:
            file.write("\n".join(selected_images))
        print(f"Group {group_id} 的图像列表已保存到 {image_list_file}")

def copy_images_based_on_txt(folder, source_base_dir):
    # 遍历目标文件夹中的所有子文件夹和文件
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file == "images.txt":  # 找到 images.txt 文件
                txt_path = os.path.join(root, file)  # 获取 images.txt 的完整路径
                target_folder = root  # images.txt 所在的文件夹
                # 读取 images.txt 中的文件名
                with open(txt_path, "r") as f:
                    image_names = f.read().splitlines()
                # 遍历每个文件名，将其从 source_base_dir 的子文件夹中拷贝到 target_folder
                for image_name in image_names:
                    # 根据 colormap 从对应的子文件夹中查找
                    colormap = image_name.split('_')[-2]  # 从文件名中提取 colormap
                    source_path = os.path.join(source_base_dir, colormap, image_name)
                    target_path = os.path.join(target_folder, image_name)

                    if os.path.exists(source_path):  # 检查源文件是否存在
                        shutil.copy2(source_path, target_path)  # 复制文件到目标文件夹
                        print(f"已拷贝文件：{source_path} -> {target_path}")
                    else:
                        print(f"未找到文件：{source_path}，跳过。")

def main():
    # 分组数据
    groups = [
        [1, 6, 8, 3],
        [4, 1, 7, 6],
        [7, 2, 6, 4],
        [7, 6, 5, 2],
        [5, 2, 3, 4],
        [7, 6, 1, 3],
        [5, 8, 2, 3],
        [7, 2, 3, 5],
        [5, 6, 1, 2],
        [5, 8, 4, 3],
        [2, 8, 5, 4],
        [4, 6, 5, 1],
        [3, 5, 7, 6],
        [2, 8, 4, 7],
        [2, 5, 4, 3],
        [5, 3, 2, 6],
        [2, 5, 3, 1],
        [7, 1, 3, 4],
        [6, 3, 8, 2],
        [7, 4, 3, 1]
    ]
    # 定义频率和 colormap
    frequencies = ['1', '3', '5', '7', '9']
    colormaps = ['gray', 'hot', 'rainbow']
    # 基础输出文件夹
    base_output_dir = r"../..\\result\\exp2"
    # 图片来源文件夹（包含 gray、hot、rainbow 子文件夹）
    source_base_dir = r"../..\\color\\exp2"
    # 调用函数保存图像列表到各组文件夹中
    save_images_to_group_folders(groups, frequencies, colormaps, base_output_dir)
    # 根据 images.txt 拷贝文件到对应文件夹
    copy_images_based_on_txt(base_output_dir, source_base_dir)

if __name__ == "__main__":
    main()
