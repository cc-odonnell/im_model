# generate dummy data for project

import pandas as pd
import numpy as np
import string

# generate list of item numbers
item_num = np.arange(10000,10010, 1)

# generate list of letters to represent locations
# distribution center (DC)
dc = list((string.ascii_uppercase)[0:3])

# dates in date range
order_date = pd.date_range(start='2023/01/01', end='2023/12/31', freq='d').tolist()

# cross join for every combination of date, item, and location
c = [(x, y, z) for x in order_date for y in dc for z in item_num]
df = pd.DataFrame(c, columns=['order_date', 'dc', 'item_num'])

# randomly generate numbers from normal distribution
np.random.seed(1)
df["daily_demand"] = np.random.normal(8000, 2000, size=10950)

# customize demand
# make 1 location have higher demand
df["new_daily_demand"] = np.where(df.dc == "A", df.daily_demand *1.2, df.daily_demand)

# data check
df.groupby("dc")["new_daily_demand"].mean()

# add seasonal demand for 1 item
condition1 = df["order_date"] > '2023/10/01'
condition2 = df["order_date"] < '2023/04/01'
condition3 = df["item_num"] == 10000
df["new_daily_demand"] = np.where((condition1 | condition2) & condition3,
                                  df.new_daily_demand *0.9, df.new_daily_demand)

# data check
by_date = df.groupby([df['order_date'].dt.month, "item_num"])[
    "new_daily_demand"].mean().reset_index()
by_date[(by_date["item_num"] == 10000)]

# make 1 item in 1 region have higher demand in summer
condition1 = df["order_date"] >= '2023/06/01' & < '2023/09/01'
condition2 = df["item_num"] == 10009
condition3 = df["dc"] == "A"

# data check
by_date = df.groupby([df['order_date'].dt.month, "item_num", "dc"])[
    "new_daily_demand"].mean().reset_index()
by_date[(by_date["item_num"]== 10001) & (by_date["dc"]=="A")]


# add some outliers (zero demand and peak demands at holidays)

del [a,b,c]



#############
# alternatives

# copy and paste from Excel
# reads it from the computer's clipboard function !!
df = pd.read_clipboard()

# enter manually
from io import StringIO
F = """
Name,Score,Section
W,26,A
M,62,A
Q,69,A
"""
df =pd.read_csv(StringIO(F))


