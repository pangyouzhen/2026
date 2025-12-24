import argparse
from datetime import datetime, timedelta

import pandas as pd

# 设置命令行参数解析
parser = argparse.ArgumentParser(description="生成 Excel 和 CSV 文件")
parser.add_argument('--date', type=str, default=datetime.today().strftime('%Y-%m-%d'), 
                    help="本周一的日期，格式: YYYY-MM-DD，默认是今天的日期")

args = parser.parse_args()
start_date_str = args.date

# 解析输入的日期
start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

# 计算周五的日期
end_date = start_date + timedelta(days=4)

# 生成文件名
file_name = f"{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}"

# 生成日期和列标签
days_of_week = ["周一", "周二", "周三", "周四", "周五"]
dates = [start_date + timedelta(days=i) for i in range(5)]
columns = [f"{day}{date.strftime('%m%d')}" for day, date in zip(days_of_week, dates)]

# 创建 DataFrame
df = pd.DataFrame(columns=["类别"] + columns)
df.loc[0] = ["类别"] + columns
df.loc[1] = ["市场焦点股"] + [""] * len(columns)

# 保存到 Excel 文件
df.to_excel(f"../workday_data/{file_name}.xlsx", index=False, header=False)
