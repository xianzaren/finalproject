import numpy as np
import matplotlib.pyplot as plt
import os
import random

# 从 CSV 数据生成标量场图像，并标记两个点 A 和 B，同时生成真实和伪造的高程剖面

def generate_scalar_field_image_with_profiles(noise, colormap, output_filepath, result_file):
    height, width = noise.shape

    # 根据 colormap 动态设置标记点的颜色
    if colormap == "hot":
        color = 'green'
    elif colormap == "rainbow":
        color = 'black'
    elif colormap == "gray":
        color = 'red'  # 默认红色

    # 随机选择点 A 的坐标，确保点 B 水平相隔 350 个像素且不越界，并距离边缘至少 30 个像素
    while True:
        ax = random.randint(30, width - 351 - 30)  # 确保 A 点和 B 点距离左右边界至少 30 像素
        ay = random.randint(30, height - 30)  # 确保 A 点距离上下边界至少 30 像素
        bx = ax + 350  # 点 B 的横坐标
        by = ay  # 点 B 的纵坐标与 A 相同
        if 30 <= bx < width - 30:  # 验证点 B 的坐标合法性
            break

    # 提取 A 和 B 之间的所有数据（真实高程剖面）
    real_profile = noise[ay, ax:bx + 1]
    real_data = (ax, ay, bx, by, real_profile)

    # 生成伪造的剖面图（通过随机选择新的点对生成）
    fake_profiles = []
    for _ in range(5):
        while True:
            fake_ax = random.randint(30, width - 351 - 30)
            fake_ay = random.randint(30, height - 30)
            fake_bx = fake_ax + 350
            fake_by = fake_ay
            if 30 <= fake_bx < width - 30 and (fake_ax != ax or fake_ay != ay):  # 确保伪造点不同于真实点
                break
        fake_profile = noise[fake_ay, fake_ax:fake_bx + 1]
        fake_profiles.append((fake_ax, fake_ay, fake_bx, fake_by, fake_profile))

    # 将真实剖面图插入伪造剖面图列表
    all_profiles = [real_data] + fake_profiles
    random.shuffle(all_profiles)  # 随机排列

    # 找到真实剖面图在随机排列中的索引
    real_index = all_profiles.index(real_data)

    # 创建合并图像：标量场图像 + 六个独立的高程剖面图
    fig = plt.figure(figsize=(12, 6))

    # 绘制主图像
    ax_main = fig.add_subplot(1, 2, 1)
    ax_main.imshow(noise, cmap=colormap, origin='upper')
    ax_main.axis('off')
    ax_main.scatter(ax, ay, color=color, label='A', s=100, zorder=5)  # 标记点 A
    ax_main.scatter(bx, by, color=color, label='B', s=100, zorder=5)  # 标记点 B
    ax_main.text(ax, ay - 10, 'A', color=color, fontsize=12, ha='center', va='bottom')  # A 的文字标签上移
    ax_main.text(bx, by - 10, 'B', color=color, fontsize=12, ha='center', va='bottom')  # B 的文字标签上移

    # 绘制六个独立的高程剖面图
    for i, (_, _, _, _, profile) in enumerate(all_profiles):
        ax_profile = fig.add_subplot(6, 2, 2 * i + 2)
        ax_profile.plot(profile, color='black')
        ax_profile.set_xlim(0, len(profile))
        ax_profile.set_ylim(0, 1)
        ax_profile.axis('on')
        ax_profile.set_xticks([])
        ax_profile.set_yticks([])
        ax_profile.spines['top'].set_visible(True)
        ax_profile.spines['right'].set_visible(True)
        ax_profile.spines['left'].set_visible(True)
        ax_profile.spines['bottom'].set_visible(True)
        ax_profile.text(2, profile[0], 'A', color='red', fontsize=10, ha='center', va='bottom')
        ax_profile.text(len(profile) - 1, profile[-1], 'B', color='blue', fontsize=10, ha='center', va='bottom')
    # 调整子图布局，使剖面图更贴合标量场图的宽度
    plt.subplots_adjust(wspace=0.1, hspace=0.5)

    # 保存合并图像
    plt.tight_layout()
    plt.savefig(output_filepath, dpi=150, bbox_inches='tight', pad_inches=0)
    plt.close()

    # 输出真实曲线的索引
    result_file.write(f"{output_filepath}: 真实曲线是第 {real_index + 1} 条\n")
    print(f"真实曲线是第 {real_index + 1} 条")

# 主函数
def main():
    csv_dir = r"E:\桌面\Final project\data\uncolor"  # 存储 CSV 的目录
    colromap_list = ['gray','hot','rainbow']
    for colormap in colromap_list:
        output_dir = f"E:\桌面\Final project\color\exp3\{colormap}"  # 输出图像文件夹
        print(f"正在输出{colormap}的图像")
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        # 结果文件路径
        result_file_path = os.path.join(output_dir, "result.txt")
        # 打开结果文件进行写入
        with open(result_file_path, "w") as result_file:
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
                    output_filepath = os.path.join(output_dir, f"ScalarField_{os.path.splitext(csv_filename)[0]}_{colormap}.png")
                    # 生成标量场图像并附加剖面图
                    generate_scalar_field_image_with_profiles(noise, colormap, output_filepath, result_file)

if __name__ == "__main__":
    main()
