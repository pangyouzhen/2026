import argparse
import subprocess
from pathlib import Path

import pandas as pd


def get_latest_file_path():
    p = Path("/mnt/d/pro/wps_sync/")
    file_path = [i for i in p.glob("20*xlsx")][-1]
    return str(file_path)

# 输入一个excel文件将其转为csv文件并移动到指定位置


def excel_to_csv(file_path, destination_path):
    df = pd.read_excel(file_path, header=None)
    df.to_csv(destination_path + '/' + file_path.split('/')
              [-1].split('.')[0] + '.csv', index=False, header=False)
    # 使用mv命令移动文件及其所在目录到指定位置
    subprocess.run(['cp', file_path, destination_path])


if __name__ == "__main__":
    # 创建一个ArgumentParser对象
    parser = argparse.ArgumentParser(
        description='Convert an Excel file to a CSV file and move it to a specified location.')

    # 添加命令行参数
    file_path = get_latest_file_path()
    parser.add_argument(
        '--file_path', help='Path to the Excel file', default=file_path)
    parser.add_argument('--destination_path', help='Path to the destination folder',
                        nargs="?",
                        default="/data/project/2024/sentiment/weekly/")

    # 解析命令行参数
    args = parser.parse_args()
    print(args)
    # 调用excel_to_csv函数
    excel_to_csv(args.file_path, args.destination_path)
