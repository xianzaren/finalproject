import numpy as np
import matplotlib.pyplot as plt
import os
import random


# 生成标量场图像，仅显示 AB 点标记
def generate_scalar_field_image(noise, colormap, ab_positions, output_filepath):
    ax, ay, bx, by = ab_positions

    # 动态设置标记点的颜色
    if colormap == "hot":
        color = 'green'
    elif colormap == "rainbow":
        color = 'black'
    elif colormap == "gray":
        color = 'red'  # 默认红色

    # 创建标量场图像
    plt.figure(figsize=(6, 6))
    plt.imshow(noise, cmap=colormap, origin='upper')
    plt.axis('off')
    plt.scatter(ax, ay, color=color, label='A', s=20, zorder=5)  # 标记点 A
    plt.scatter(bx, by, color=color, label='B', s=20, zorder=5)  # 标记点 B
    plt.text(ax, ay - 10, 'A', color=color, fontsize=12, ha='center', va='bottom')  # A 的文字标签上移
    plt.text(bx, by - 10, 'B', color=color, fontsize=12, ha='center', va='bottom')  # B 的文字标签上移
    plt.tight_layout()
    plt.savefig(output_filepath, dpi=150, bbox_inches='tight', pad_inches=0)
    plt.close()


# 生成包含剖面曲线的组合图像
def generate_profiles_image(noise, colormap, ab_positions, all_profiles, output_filepath):
    ax, ay, bx, by = ab_positions
    # 动态设置标记点的颜色
    if colormap == "hot":
        color = 'green'
    elif colormap == "rainbow":
        color = 'black'
    elif colormap == "gray":
        color = 'red'  # 默认红色
    # 创建合并图像：标量场图像 + 六个独立的高程剖面图
    fig = plt.figure(figsize=(12, 6))
    # 绘制主图像
    ax_main = fig.add_subplot(1, 2, 1)
    ax_main.imshow(noise, cmap=colormap, origin='upper')
    ax_main.axis('off')
    ax_main.scatter(ax, ay, color=color, label='A', s=20, zorder=5)
    ax_main.scatter(bx, by, color=color, label='B', s=20, zorder=5)
    ax_main.text(ax, ay - 10, 'A', color=color, fontsize=12, ha='center', va='bottom')
    ax_main.text(bx, by - 10, 'B', color=color, fontsize=12, ha='center', va='bottom')

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

        # 在剖面图上标注 A 和 B
        ax_profile.text(2, profile[0], 'A', color='red', fontsize=10, ha='center', va='bottom')
        ax_profile.text(len(profile) - 1, profile[-1], 'B', color='blue', fontsize=10, ha='center', va='bottom')

        # 标记这是第几张曲线
        ax_profile.text(0.5, 1.05, f"Curve {i + 1}", transform=ax_profile.transAxes, fontsize=10, ha='center',
                        va='bottom', color='black')

    plt.subplots_adjust(wspace=0.1, hspace=0.5)
    plt.tight_layout()
    plt.savefig(output_filepath, dpi=150, bbox_inches='tight', pad_inches=0)
    plt.close()


# 主函数
def main():
    csv_dir = r"E:\桌面\Final project\data\uncolor"  # 存储 CSV 的目录
    colromap_list = ['gray', 'hot', 'rainbow']
    for colormap in colromap_list:
        output_dir = f"E:\桌面\Final project\color\exp3\{colormap}"  # 输出图像文件夹
        os.makedirs(output_dir, exist_ok=True)
        result_file_path = os.path.join(output_dir, "result.txt")
        with open(result_file_path, "w") as result_file:
            for i in range(1, 4):
                for csv_filename in os.listdir(csv_dir):
                    if csv_filename.endswith(".csv"):
                        csv_filepath = os.path.join(csv_dir, csv_filename)
                        print(f"正在读取 CSV 文件: {csv_filepath}")
                        noise = np.loadtxt(csv_filepath, delimiter=",", skiprows=1)
                        noise = (noise - noise.min()) / (noise.max() - noise.min())

                        # 随机生成 A 和 B 的位置
                        ax = random.randint(30, noise.shape[1] - 351 - 30)
                        ay = random.randint(30, noise.shape[0] - 30)
                        bx, by = ax + 350, ay
                        ab_positions = (ax, ay, bx, by)

                        # 生成真实剖面和伪造剖面
                        real_profile = noise[ay, ax:bx + 1]
                        fake_profiles = []
                        for _ in range(5):
                            while True:
                                fake_ax = random.randint(30, noise.shape[1] - 351 - 30)
                                fake_ay = random.randint(30, noise.shape[0] - 30)
                                fake_bx, fake_by = fake_ax + 350, fake_ay
                                if (fake_ax, fake_ay) != (ax, ay):
                                    break
                            fake_profiles.append((fake_ax, fake_ay, fake_bx, fake_by, noise[fake_ay, fake_ax:fake_bx + 1]))
                        all_profiles = [(ax, ay, bx, by, real_profile)] + fake_profiles
                        random.shuffle(all_profiles)
                        real_index = all_profiles.index((ax, ay, bx, by, real_profile))

                        # 输出标量场图像
                        scalar_field_filepath = os.path.join(output_dir,
                                                             f"ScalarField_{os.path.splitext(csv_filename)[0]}_{colormap}_{i}.png")
                        generate_scalar_field_image(noise, colormap, ab_positions, scalar_field_filepath)

                        # 输出剖面曲线图像
                        profiles_filepath = os.path.join(output_dir,
                                                         f"Profiles_{os.path.splitext(csv_filename)[0]}_{colormap}_{i}.png")
                        generate_profiles_image(noise, colormap, ab_positions, all_profiles, profiles_filepath)

                        # 修改后的代码段
                        result_file.write(f"{os.path.basename(profiles_filepath)} + 真实曲线是第 {real_index + 1} 条\n")
                        print(f"{os.path.basename(profiles_filepath)} + 真实曲线是第 {real_index + 1} 条")

if __name__ == "__main__":
    main()
