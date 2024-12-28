import os
import re
import pandas as pd


def clean_zero_width_spaces(text):
    """清除零宽字符"""
    return re.sub(r'[\u200B\u200C\u200D\uFEFF]', '', text)


def process_coordinates(txt_file, csv_mapping, output_txt, log_file):
    """
    处理坐标文件，生成结果并记录异常日志。
    x为行，y为列
    """
    # 读取文本文件 (坐标信息)
    if not os.path.exists(txt_file):
        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(f"Error: Coordinate file not found - {txt_file}\n")
        print(f"❌ Error: Coordinate file not found - {txt_file}")
        return

    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    all_results = []  # 保存处理后的结果
    current_image = None  # 当前 Image 编号

    for line in lines:
        line = clean_zero_width_spaces(line)
        line_stripped = line.strip()

        # 匹配 "Image 1", "Image 2" 等
        match_img = re.match(r'^Image\s+(\d+):?$', line_stripped)
        if match_img:
            current_image = match_img.group(1)
            continue

        # 匹配坐标行，例如 "1.0: (596, 372)"
        match_coord = re.match(r'^([\d\.]+):\s*\((\d+)\s*,\s*(\d+)\)$', line_stripped)
        if match_coord:
            float_value, x_str, y_str = match_coord.groups()
            x, y = int(x_str), int(y_str)

            if not current_image or current_image not in csv_mapping:
                # 如果没有匹配到对应的 CSV 文件
                result_line = f"{float_value}: ({x}, {y}) - No CSV mapping for Image {current_image}"
                all_results.append(result_line)
                continue

            csv_path = csv_mapping[current_image]

            if not os.path.exists(csv_path):
                # 如果 CSV 文件不存在
                result_line = f"{float_value}: ({x}, {y}) - CSV Not Found: {csv_path}"
                all_results.append(result_line)
                with open(log_file, 'a', encoding='utf-8') as log:
                    log.write(f"Error: CSV file not found - {csv_path}\n")
                continue

            try:
                # 加载 CSV 文件 (跳过第一行)
                df = pd.read_csv(csv_path, header=None, skiprows=1)
            except Exception as e:
                result_line = f"{float_value}: ({x}, {y}) - Fail to load CSV: {str(e)}"
                all_results.append(result_line)
                with open(log_file, 'a', encoding='utf-8') as log:
                    log.write(f"Error: Fail to load CSV - {csv_path} | {e}\n")
                continue

            # 判断坐标是否越界
            if x < 0 or x >= len(df) or y < 0 or y >= len(df.columns):
                result_line = f"{float_value}: ({x}, {y}) - OutOfRange"
                print(f"⚠️ Warning: OutOfRange at ({x}, {y}) in Image {current_image}")
            else:
                # 读取对应位置的值
                value_at_coord = df.iloc[x, y]
                result_line = f"{float_value}: ({x}, {y}) - {value_at_coord}"

            all_results.append(result_line)

    # 将结果写入输出文件
    with open(output_txt, 'w', encoding='utf-8') as f:
        for line_out in all_results:
            f.write(line_out + "\n")

    print(f"✅ Processed {txt_file}, results saved to {output_txt}")


def check_and_write_empty_message(output_txt):
    """
    检查指定的输出文件是否为空，若为空则提示。
    """
    if os.path.exists(output_txt) and os.path.getsize(output_txt) == 0:
        print(f"⚠️ Warning: Output file is empty - {output_txt}")


def main():
    # 定义 CSV 文件的路径
    csv_mapping = {
        '1': r"../../data\uncolor\Noise_(630, 820)_(1, 1)_5.csv",
        '2': r"../../data\uncolor\Noise_(630, 820)_(3, 3)_5.csv",
        '3': r"../../data\uncolor\Noise_(630, 820)_(5, 5)_5.csv",
        '4': r"../../data\uncolor\Noise_(630, 820)_(7, 7)_5.csv",
        '5': r"../../data\uncolor\Noise_(630, 820)_(9, 9)_5.csv",
    }

    # 日志文件路径
    log_file = r"../../error_log.txt"
    with open(log_file, 'w', encoding='utf-8') as log:
        log.write("Error Log\n")

    # 处理多个坐标文件
    for i in range(4, 5):
        base_dir = f"../..//result//{i}"
        gray_txt = os.path.join(base_dir, "gray.txt")
        hot_txt = os.path.join(base_dir, "hot.txt")
        rainbow_txt = os.path.join(base_dir, "rainbow.txt")

        gray_result = os.path.join(base_dir, "gray_result.txt")
        hot_result = os.path.join(base_dir, "hot_result.txt")
        rainbow_result = os.path.join(base_dir, "rainbow_result.txt")

        # 分别处理文件并记录日志
        process_coordinates(gray_txt, csv_mapping, gray_result, log_file)
        check_and_write_empty_message(gray_result)

        process_coordinates(hot_txt, csv_mapping, hot_result, log_file)
        check_and_write_empty_message(hot_result)

        process_coordinates(rainbow_txt, csv_mapping, rainbow_result, log_file)
        check_and_write_empty_message(rainbow_result)


if __name__ == "__main__":
    main()
