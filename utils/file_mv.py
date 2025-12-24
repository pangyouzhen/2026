#! /usr/bin/env pythond
import subprocess
import sys
from pathlib import Path

import pandas as pd


def main():
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)
    
    # 获取文件名
    file_path = sys.argv[1]
    print(file_path)
    excel_file = Path(f"{file_path}")
    filename = excel_file.stem
    csv_file = f"{filename}.csv"
    
    # 读取 Excel 文件
    try:
        df = pd.read_excel(excel_file)
        if '类别' not in df.columns:
            raise KeyError("Column '类别' not found in the Excel file.")

        duplicated_mask = df['类别'].duplicated(keep=False)
        if duplicated_mask.any():
            duplicate_rows = df[duplicated_mask]
            duplicate_categories = duplicate_rows['类别'].unique()
            print("重复的类别有:", duplicate_categories)
            print("\n重复的行号（Excel 从 1 开始计数）:")
            for category in duplicate_categories:
                indices = df.index[df['类别'] == category].tolist()
                # +2 是因为 Excel 行号从 1 开始，且 pandas 默认第一行是表头
                excel_rows = [i + 2 for i in indices]
                print(f"类别 '{category}' 出现在行号: {excel_rows}")
            raise ValueError("存在重复类别，请检查。")
        
        # 将数据保存为 CSV 文件
        csv_file = f'../sentiment/weekly/{filename}.csv'
        df.to_csv(csv_file, index=False)
        subprocess.run(f"mv ../workday_data/{filename}.xlsx ../sentiment/weekly/{filename}.xlsx", shell=True)

    except FileNotFoundError:
        print(f"File {excel_file} not found.")
    except KeyError as e:
        print(str(e))


if __name__ == '__main__':
    main()
