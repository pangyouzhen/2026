#!/data/project/2024/venv/bin/python
from pathlib import Path

import natsort  # 用于自然排序
import pandas as pd
from pypinyin import (  # Import pinyin and Style for Chinese character to pinyin conversion
    Style, pinyin)

p = Path('../sentiment/weekly/')

# 获取所有 Excel 文件，并按自然排序
files = sorted(p.glob('*.xlsx'), key=lambda x: natsort.natsort_key(str(x)))

dfs = []
for file in files:
    df = pd.read_excel(file)
    print(file)
    if '类别' in df.columns:
        df.set_index('类别', inplace=True)
        if not df.index.duplicated().any():
            dfs.append(df)
        else:
            print(f"Warning: Duplicate indices found in {file}. Skipping this file.")
    else:
        print(f"Warning: '类别' column not found in {file}. Skipping this file.")

# 合并数据
if dfs:
    merged_df = dfs[0]
    for i in range(1, len(dfs)):
        merged_df = pd.merge(merged_df, dfs[i], how='outer', on='类别')
    
 # --- Sort the '类别' index by pinyin ---
    # The 'TypeError: sequence item 0: expected str instance, list found'
    # happened because `pinyin(str(x))` returns a list of lists (e.g., [['li'], ['ming']]).
    # We need to flatten this list of lists into a single string for sorting.
    # The `sum([], [])` trick effectively flattens a list of lists.

    # Ensure the index is string type before attempting pinyin conversion
    merged_df.index = merged_df.index.astype(str)

    # Sort the index directly using the pinyin conversion as the key
    sorted_index = sorted(
        merged_df.index,
        key=lambda x: ''.join(sum(pinyin(x, style=Style.NORMAL), []))
    )

    # Reindex the DataFrame with the sorted index
    merged_df = merged_df.reindex(sorted_index)
    # ----------------------------------------

    # 保存合并结果
    print('\n')
    print(list(merged_df.index))
    print('\n')
    merged_df.to_excel('../workday_data/merge_all.xlsx')
    merged_df.to_csv('../workday_data/merge_all.csv')

    print("Merged file saved as 'merge_all.xlsx'")
else:
    print("No valid Excel files found to merge.")
