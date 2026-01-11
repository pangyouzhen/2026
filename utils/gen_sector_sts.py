import pandas as pd

# 生成从 2026-01-01 到 2026-12-31 的日期范围
date_range = pd.date_range(start='2026-01-01', end='2026-12-31', freq='D')

# 创建 DataFrame，包含日期列和5个空板块列
df = pd.DataFrame({
    '日期': date_range,
    '板块1': '',
    '板块2': '',
    '板块3': '',
    '板块4': '',
    '板块5': ''
})

# 将日期列格式化为 YYYY-MM-DD 字符串（可选，避免写入带时间的格式）
df['日期'] = df['日期'].dt.strftime('%Y-%m-%d')

# 保存为 CSV 文件
df.to_csv('sector_sts.csv', index=False, encoding='utf-8-sig')

print("sector_sts.csv")