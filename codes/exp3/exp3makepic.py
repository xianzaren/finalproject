import numpy as np
import matplotlib.pyplot as plt
import os
import random

# 从 CSV 数据生成标量场图像，并标记两个点 A 和 B

def generate_scalar_field_image_with_points(noise, colormap, output_filepath, profile_output_filepath):
    height, width = noise.shape

    # 根据 colormap 动态设置标记点的颜色
    if colormap == "hot":
        color = 'green'
    elif colormap == "rainbow":
        color = 'white'
    elif colormap == "gray":
        color = 'red'  # 默认红色

    # 随机选择点 A 的坐标，确保点 B 水平相隔 350 个像素且不越界
    while True:
        ax = random.randint(0, width - 351)  # 确保 B 点不会超出边界
        ay = random.randint(0, height - 1)  # A 点的纵坐标可以是任意值
        bx = ax + 350  # 点 B 的横坐标
        by = ay        # 点 B 的纵坐标与 A 相同
        if 0 <= bx < width:  # 验证点 B 的坐标合法性
            break

    # 提取 A 和 B 之间的所有数据（水平剖面）
    profile_data = noise[ay, ax:bx+1]

    # 绘制高程剖面曲线
    plt.figure(figsize=(10, 5))
    plt.plot(profile_data, label='Elevation Profile', color='black')
    plt.title('Elevation Profile Between Points A and B')
    plt.xlabel('Pixel Index')
    plt.ylabel('Elevation Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(profile_output_filepath, dpi=150, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"高程剖面图已保存: {profile_output_filepath}")

    # 绘制图像
    plt.figure(figsize=(8, 6))
    plt.imshow(noise, cmap=colormap, origin='upper')  # 使用指定的 colormap
    plt.axis('off')  # 关闭坐标轴
    plt.gca().set_axis_off()  # 确保没有轴信息
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)  # 调整布局
    plt.margins(0, 0)

    # 在图像上标记点 A 和点 B
    plt.scatter(ax, ay, color=color, label='A', s=50, zorder=5)  # 标记点 A
    plt.scatter(bx, by, color=color, label='B', s=50, zorder=5)  # 标记点 B
    plt.text(ax, ay, 'A', color=color, fontsize=12, ha='center', va='bottom')  # A 的文字标签
    plt.text(bx, by, 'B', color=color, fontsize=12, ha='center', va='bottom')  # B 的文字标签

    # 保存图像
    plt.savefig(output_filepath, dpi=150, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"标量场图像已保存: {output_filepath}")

# 主函数
def main():
    csv_dir = r"E:\桌面\Final project\data\uncolor"  # 存储 CSV 的目录
    colormap = 'hot'  # 使用的 colormap
    output_dir = f"E:\桌面\Final project\color\exp3\{colormap}"  # 输出图像文件夹

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

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
            image_filename = f"ScalarField_WithPoints_{os.path.splitext(csv_filename)[0]}_{colormap}.png"
            profile_filename = f"ElevationProfile_{os.path.splitext(csv_filename)[0]}_{colormap}.png"
            output_filepath = os.path.join(output_dir, image_filename)
            profile_output_filepath = os.path.join(output_dir, profile_filename)
            # 生成标量场图像并标记点 A 和点 B，同时生成高程剖面
            generate_scalar_field_image_with_points(noise, colormap, output_filepath, profile_output_filepath)

if __name__ == "__main__":
    main()