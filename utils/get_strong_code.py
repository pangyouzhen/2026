import argparse

import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str,help="")
args = parser.parse_args()

df = pd.read_csv(args.input,dtype={"代码":str})

df["代码"].to_csv("code.txt",index=False,header=False)