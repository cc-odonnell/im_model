import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# get data from 'generate_data.py'
# subset to 1 SKU-DC combo
demand_data = df[(df['item_num'] == 10000) & (df['dc'] == 'A')]

# make sure date is set as index
demand_data = demand_data.reset_index(drop=True)

# add new placeholder columns
demand_data['on_hand_il'] = 0
demand_data['in_transit_il'] = 0
demand_data['total_il'] = 0
demand_data['delivery'] = 0

# set the first day of inventory
demand_data.loc[demand_data.index[0], 'on_hand_il'] = 11111

lead_time = 10
reorder_pt = 8000 * 10
reorder_qty = 8000 * 5


# Pandas-style version of function with .at method
def proj_inv_in_transitv2(demand_data):
    lead_time = lead_time
    reorder_pt = reorder_pt
    reorder_qty = reorder_qty

    # index starts at 0, so 1 is the second row
    for i in range(1, len(demand_data)):

        # calculate on-hand inventory, min floor inventory level to 0
        demand_data.at[i, 'on_hand_il'] = max(0,
                                              demand_data.at[i, 'delivery'] + demand_data.at[i - 1, 'on_hand_il'] -
                                              demand_data.at[i, 'daily_demand'])

        # calculate total inventory (on hand and in transit)
        demand_data.at[i, 'total_il'] = demand_data.at[i, 'on_hand_il'] + demand_data.at[i, 'in_transit_il']

        # trigger order if total inventory <= reorder point
        if demand_data.at[i, 'total_il'] <= reorder_pt:

            # supply arrives lead time days later (if within simulation time period)
            if (i + lead_time < len(demand_data)):
                # add supply
                demand_data.at[i + lead_time, 'delivery'] = demand_data.at[i + lead_time, 'delivery'] + reorder_qty

                # add in_transit inventory to each day (i+1) through (i + LT - 1)
                demand_data.loc[i + 1: i + lead_time, 'in_transit_il'] = demand_data.loc[i + 1: i + lead_time,
                                                                         'in_transit_il'] + reorder_qty

    return demand_data


demand_data = proj_inv_in_transitv2(demand_data)
# new column
demand_data['unmet_demand'] = (demand_data['new_daily_demand'] - demand_data['on_hand_il']).clip(lower=0)
# save data
demand_data.to_csv('demand_data_sim1.csv')

# later version should incorporate a rq_data dataframe

# generate diagnostic plots

plt.figure(figsize=(10, 6))

# Plot 'on_hand_il' with red color
plt.plot(demand_data['order_date'], demand_data['on_hand_il'], color='red', label='on_hand_il')

# Plot 'new_daily_demand' with blue color
plt.plot(demand_data['order_date'], demand_data['new_daily_demand'], color='blue', label='new_daily_demand')

plt.title('R = 10, Q = 5')
plt.legend()
plt.show()


