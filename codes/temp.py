import numpy as np
import matplotlib.pyplot as plt
import os
import random

# 生成图像并添加随机红蓝方框，同时比较方框内平均值
def generate_image_with_boxes_and_compare(noise, colormap, output_filepath, result_filepath, box_count=8):
    height, width = noise.shape

    # 打开结果文件
    with open(result_filepath, "a") as result_file:  # "a" 模式为追加写入
        # 随机选择两个不重叠的 100x100 区域
        def random_box():
            x = random.randint(30, width - 130)  # 确保距离边界至少 30 格
            y = random.randint(30, height - 130)
            return x, y

        for i in range(box_count):
            # 确保两个区域不重叠
            while True:
                x1, y1 = random_box()
                x2, y2 = random_box()
                if not (x1 < x2 + 100 and x1 + 100 > x2 and y1 < y2 + 100 and y1 + 100 > y2):
                    break

            # 从噪声矩阵中提取红蓝方框内的值
            red_box_values = noise[y1:y1 + 100, x1:x1 + 100]
            blue_box_values = noise[y2:y2 + 100, x2:x2 + 100]
            # 计算两个方框内的平均值
            red_box_avg = np.mean(red_box_values)
            blue_box_avg = np.mean(blue_box_values)

            # 动态设置方框颜色和文字描述
            if colormap == "hot":
                red_color = 'purple'  # 红框修改为紫色
                blue_color = 'green'  # 蓝框修改为绿色
                red_text = "Purple Box Avg"  # 输出文字对应方框颜色
                blue_text = "Green Box Avg"  # 输出文字对应方框颜色
            elif colormap == "rainbow":
                red_color = 'black'  # 红框修改为黑色
                blue_color = 'white'  # 蓝框修改为白色
                red_text = "Black Box Avg"  # 输出文字对应方框颜色
                blue_text = "White Box Avg"  # 输出文字对应方框颜色
            else:
                red_color = 'red'  # 默认红色
                blue_color = 'blue'  # 默认蓝色
                red_text = "Red Box Avg"  # 输出文字对应方框颜色
                blue_text = "Blue Box Avg"  # 输出文字对应方框颜色

            # 比较两个平均值并记录
            larger_box_color = blue_color if blue_box_avg > red_box_avg else red_color

            # 写入结果文件（包括具体的方框位置）
            image_basename = os.path.basename(output_filepath).replace("ScalarField_WithBoxes_Noise_", "").replace(
                ".png", f"_{i + 1}")
            result_file.write(
                f"{image_basename}, {red_text}: {red_box_avg:.4f}, {blue_text}: {blue_box_avg:.4f}, "
                f"Larger Box: {larger_box_color}\n"
            )

            # 打印输出
            print(
                f"第 {i + 1} 个图像 - {red_text}: {red_box_avg:.4f}, {blue_text}: {blue_box_avg:.4f}, "
                f"较大方框: {larger_box_color.capitalize()}"
            )

            # 绘制图像并添加方框
            plt.figure(figsize=(8, 6))
            plt.imshow(noise, cmap=colormap, origin='upper')
            plt.axis('off')  # 关闭所有坐标轴
            plt.gca().set_axis_off()  # 确保没有任何轴信息
            plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)  # 调整布局
            plt.margins(0, 0)

            # 绘制红色方框（区域 1）
            rect1 = plt.Rectangle((x1, y1), 100, 100, edgecolor=red_color, facecolor='none', linewidth=2)
            plt.gca().add_patch(rect1)

            # 绘制蓝色方框（区域 2）
            rect2 = plt.Rectangle((x2, y2), 100, 100, edgecolor=blue_color, facecolor='none', linewidth=2)
            plt.gca().add_patch(rect2)

            # 保存图像
            output_filepath_with_index = output_filepath.replace(".png", f"_{i + 1}.png")
            plt.savefig(output_filepath_with_index, dpi=150, bbox_inches='tight', pad_inches=0)
            plt.close()
            print(f"第 {i + 1} 个带方框的图像已保存: {output_filepath_with_index}")


# 主函数
def main():
    csv_dir = r"E:\桌面\Final project\data\uncolor"  # 存储 CSV 的目录
    colormap = 'rainbow'  # 使用的 colormap
    output_dir = f"E:\桌面\Final project\color\\newexp2\{colormap}"  # 输出图像文件夹
    result_filepath = os.path.join(output_dir, "result.txt")  # 结果文件路径
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    # 清空结果文件（如果已存在）
    with open(result_filepath, "w") as result_file:
        result_file.write("")
    # 遍历所有 CSV 文件
    for csv_filename in os.listdir(csv_dir):
        if csv_filename.endswith(".csv"):
            csv_filepath = os.path.join(csv_dir, csv_filename)
            # 加载 CSV 数据
            print(f"正在读取 CSV 文件: {csv_filepath}")
            noise = np.loadtxt(csv_filepath, delimiter=",", skiprows=1)  # 跳过 header 行
            # 归一化到 [0,1] 区间（如果之前保存时未归一化，则需要此步骤）
            noise = (noise - noise.min()) / (noise.max() - noise.min())
            # 构造输出文件名
            image_filename = f"ScalarField_WithBoxes_{os.path.splitext(csv_filename)[0]}_{colormap}.png"
            output_filepath = os.path.join(output_dir, image_filename)
            # 生成 8 个图像并添加不同的随机方框，比较方框平均值
            generate_image_with_boxes_and_compare(noise, colormap, output_filepath, result_filepath, box_count=8)


if __name__ == "__main__":
    main()
