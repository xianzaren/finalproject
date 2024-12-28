import os
import random

def generate_random_groups_and_save(output_file, group_count=20, group_size=4, value_range=(1, 8)):
    """
    随机生成 1 到 8 内的四个数字为一组，生成指定数量的组并保存到文件。
    参数：
    - output_file: 保存结果的文件路径。
    - group_count: 要生成的组数（默认为 20）。
    - group_size: 每组包含的数字个数（默认为 4）。
    - value_range: 随机数范围（默认为 1 到 8）。
    """
    # 确保文件夹存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # 打开文件写入随机组数据
    with open(output_file, "w") as file:
        for group_id in range(1, group_count + 1):  # 遍历每组
            # 从范围内随机选择 group_size 个不重复数字
            random_group = random.sample(range(value_range[0], value_range[1] + 1), group_size)
            # 写入组号和随机数据
            file.write(f"Group {group_id}: {random_group}\n")
    print(f"随机组数据已保存到 {output_file}")

def main():
    # 输出文件路径
    output_file = r"E:\桌面\Final project\result\exp2\分组.txt"
    # 调用函数生成随机组并保存
    generate_random_groups_and_save(output_file, group_count=20, group_size=4, value_range=(1, 8))

if __name__ == "__main__":
    main()
