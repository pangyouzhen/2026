from collections import Counter
from pathlib import Path

import pandas as pd
import typer

p = Path("../sentiment/strong/")
csvs = [i for i in p.glob("*.csv")]
csvs.sort()
# print(csvs)

app = typer.Typer()
  
@app.command()
def get_strong(k:int=30):
    # K 数量
    dfs = []
    bankuai = []
    for i in csvs[-k:]:
        df = pd.read_csv(i.absolute())
        df = df[df["入选理由"]!="近期多次涨停"]
        # 过滤科创板股票
        df["代码"] = df["代码"].astype(str)
        df = df[~df["代码"].str.startswith('688')]
        dfs.append(df)

    all_df = pd.concat(dfs)
    c = Counter(all_df["名称"].tolist())

    res = pd.DataFrame(c.most_common(k),columns=['name','num'])
    res.to_csv("strong.txt",index=False)

if __name__ == "__main__":
    app()