# %%
# %%
from datetime import datetime

import pandas as pd

# %%
today = datetime.today()

# %%
today
 
# %%
str(today)

# %%
from datetime import timedelta

# %%
weeks = []
year_week = []
for i in range(5):
    d = today + timedelta(days=i)
    year_week.append(str(d).split(" ")[0].replace("-",""))
    d = str(d).split(" ")[0]
    d = d.replace("-","")
    d = d[-4:]
    weeks.append(d)
weeks

# %%
file_name = year_week[0] +"-"+ year_week[-1]

# %%
week_ch = ["周一","周二","周三","周四","周五"]

t = []
for i,v in zip(weeks,week_ch):
    t.append(v+i)
t

# %%
index = ["市场焦点股"]

# %%
df = pd.DataFrame(index=index,columns=t)

# %%
df

# %%


# %%
df.to_excel("/mnt/d/pro/wps_sync/%s.xlsx"%file_name)

# %%



