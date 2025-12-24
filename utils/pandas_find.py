#!/usr/bin/env python3
import argparse
from pathlib import Path

import pandas as pd

parser = argparse.ArgumentParser(
    description="在指定目录下所有 CSV 文件中搜索关键字，并打印包含该关键字的行及匹配列。"
)
parser.add_argument("keyword", type=str, required=True, help="要搜索的关键字（支持子字符串匹配）。")
parser.add_argument("--show-cols-only", action="store_true", help="仅打印匹配列及其值，不显示整行数据。")
args = parser.parse_args()

# 目标路径
p = Path("/data/project/2025/sentiment/weekly")
target_keyword = args.keyword
show_cols_only = args.show_cols_only

print(f"开始在路径 {p} 下搜索包含关键字 '{target_keyword}' 的 CSV 文件...")
print("-" * 70)

# -------------------------------------------------------------------
# 关键修改：获取文件列表后，使用 sorted() 进行排序
# 假设文件名（例如 '2024-01-01_data.csv'）已经是按日期可排序的字符串格式
file_list = sorted(p.glob("*.csv")) 
# -------------------------------------------------------------------

for file_path in file_list: # 使用排序后的列表进行迭代
    try:
        # 1. 文件读取
        df = pd.read_csv(file_path, low_memory=False)
        
        # 2. 创建布尔掩码 (mask) 进行子字符串搜索
        # applymap 逐元素应用函数
        mask = df.applymap(
            lambda x: isinstance(x, str) and target_keyword.lower() in x.lower()
            if pd.notna(x) else False
        )
        row_mask = mask.any(axis=1)

        if row_mask.any():
            # 3. 筛选匹配的行和掩码
            matching_rows_df = df.loc[row_mask]
            matching_mask = mask.loc[row_mask]

            print(f"✅ 文件: {file_path.name} 包含关键字。匹配行数: {len(matching_rows_df)}")
            print(f"----- 匹配数据详情 -----")

            # 4. 逐行迭代并打印
            # iterrows() 返回 (索引, Series) 对
            for idx, row in matching_rows_df.iterrows():
                # 获取该行中匹配为 True 的列名列表
                # matching_mask.loc[idx] 获得该匹配行对应的布尔 Series
                matched_cols = matching_mask.columns[matching_mask.loc[idx]].tolist()
                
                # 打印行号（即行标签）和匹配列名
                print(f"行标签/索引 {idx} 匹配列: ############# {', '.join(matched_cols)}")

                if show_cols_only:
                    # 仅显示匹配列和对应值
                    for col in matched_cols:
                        # row[col] 是获取 Series 中列值的高效方式
                        print(f"  {col}: {row[col]}")
                else:
                    # 显示整行
                    # row 是一个 Series，使用 to_string() 确保完整打印
                    print(row.to_string())

                print("-" * 50) # 行分隔线

            print("/" * 100) # 文件分隔线

    except pd.errors.EmptyDataError:
        print(f"⚠️ 文件: {file_path.name} 是空文件，跳过。")
        print("-" * 70)
    except Exception as e:
        print(f"❌ 读取或处理文件 {file_path.name} 时发生错误: {e}")
        print("-" * 70)

print("搜索完成。")
