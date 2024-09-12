# generate dummy data for project
# remember command + return to run a line of code
# or you can use Option + Shift + e

import pandas as pd
import numpy as np
import string
import matplotlib.pyplot as plt
import seaborn as sns

############ DEMAND #################

# generate list of item numbers
item_num = np.arange(10000,10004, 1)

# generate list of letters to represent locations
# distribution center (DC)
dc = list((string.ascii_uppercase)[0:3])

# dates in date range
order_date = pd.date_range(start='2023/01/01', end='2023/12/31', freq='d').tolist()

# cross join for every combination of date, item, and location
c = [(x, y, z) for x in order_date for y in dc for z in item_num]
df = pd.DataFrame(c, columns=['order_date', 'dc', 'item_num'])

# randomly generate demand values from normal distribution
np.random.seed(1)
df["daily_demand"] = np.random.normal(8000, 2000, size=4380)

# customize demand
# make 1 location have higher demand
df["new_daily_demand"] = np.where(df.dc == "A", df.daily_demand *1.2, df.daily_demand)

# data check
df.groupby("dc")["new_daily_demand"].mean()
plt.plot(df.order_date, df.daily_demand, label="Daily Demand")
plt.plot(df.order_date, df.new_daily_demand, label="New Daily Demand")
plt.show()

# show weekly average demand instead of straight daily demand
df_weekly = df.set_index('order_date')
# down sample from day to week
df_weekly = df_weekly.groupby(['dc', 'item_num']).resample('W').agg({'daily_demand': 'mean', 'new_daily_demand':'mean'}).reset_index()
# create a plot of new vs old demand by location
grid_plot = sns.FacetGrid(df_weekly, col= 'dc', row= 'item_num')
grid_plot.map(plt.plot, 'order_date', 'daily_demand', color='blue')
grid_plot.map(plt.plot, 'order_date', 'new_daily_demand', color='red')
plt.show()

# add seasonal demand for 1 item
condition1 = df["order_date"] > '2023/10/01'
condition2 = df["order_date"] < '2023/04/01'
condition3 = df["item_num"] == 10000
df["new_daily_demand"] = np.where((condition1 | condition2) & condition3,
                                  df.new_daily_demand *0.9, df.new_daily_demand)

# data check
by_date = df.groupby([df['order_date'].dt.month, "item_num"])["new_daily_demand"].mean().reset_index()

# make 1 item in 1 region have higher demand in summer
condition1a = df["order_date"] >= '2023/06/01'
condition1b = df["order_date"] < '2023/09/01'
condition2 = df["item_num"] == 10001
condition3 = df["dc"] == "B"

df["new_daily_demand"] = np.where(condition1a & condition1b & condition2 & condition3,
                                  df.new_daily_demand *1.3, df.new_daily_demand)

# data check
df_weekly = df.set_index('order_date')
# down sample from day to week
df_weekly = df_weekly.groupby(['dc', 'item_num']).resample('W').agg({'daily_demand': 'mean', 'new_daily_demand':'mean'}).reset_index()
# create a plot of new vs old demand by location
grid_plot = sns.FacetGrid(df_weekly, row= 'dc', col= 'item_num')
grid_plot.map(plt.plot, 'order_date', 'daily_demand', color='blue')
grid_plot.map(plt.plot, 'order_date', 'new_daily_demand', color='red')
plt.show()

# add a title
# add labels to Top and Right (DC and item_num)
# adjust dates at the bottom so they aren't squished
# add Bottom and Left labels (Order Date, Average Daily Units)
# add a legend for red and blue (red = new, blue = old)

# add some outliers

# set new_daily_demand to zero on these dates (2023-07-04, 2023-12-25)
dates_to_zero = pd.to_datetime(['2023/07/04', '2023/12/25'])

for date in dates_to_zero:
    df.loc[df['order_date'] == date, 'new_daily_demand'] = 0

# round demand values to integers
df[['daily_demand', 'new_daily_demand']] = df[['daily_demand', 'new_daily_demand']].round(0)

# save dataset
df.to_csv('demand_data.csv')
df.to_pickle('demand_data.pkl')

############ LEAD TIME #################

# from above
# item_num = np.arange(10000,10004, 1)
# dc = list((string.ascii_uppercase)[0:3])

# create new vendor list
vendor = ['VendorW','VendorX', 'VendorY', 'VendorZ']
# create a 1:1 relationship between vendor and SKU
vendor_item = pd.DataFrame(list(zip(vendor, item_num)), columns=['vendor', 'item_num'])

# create lead time data frame
dfs = []

for i in dc:
    df1 = vendor_item.copy()
    df1['dc'] = i
    dfs.append(df1)

lt = pd.concat(dfs)

# now add mean and std lead times
# Let's say that W and X are closer to A (West Coast),
# # Y is closer to B (Central), and
# # Z is closer to C (East Coast)
[10, 20, 30,
 10, 20, 30,
 20, 5, 20,
 30, 20, 10]

# Vendor X has very little variability
# Vendor Z has lots of variability
[3,3,3,
 1,1,1,
 3,3,3,
 4,4,4,]

lt['mean_lead_time'] = [10, 10, 20, 30, 20, 20, 5, 20, 30, 30, 30, 10]
lt['std_lead_time'] = [3, 1, 3, 4, 3, 1, 3, 4, 3, 1, 3, 4]

# save dataset

