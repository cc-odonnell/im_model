import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calculate_metrics

# set my rq inputs
# cross join for every combination of r and q
lt = 10
r = np.arange(10,15,1)
q = np.arange(1,5,1)
rq = [(lt, y, z) for y in r for z in q]
rq_inputs = pd.DataFrame(rq, columns=['lead_time', 'reorder_pt', 'reorder_qty'])

# subset for testing the simulation
rq1 = rq_inputs.iloc[[0]]

# get data from 'generate_data.py'
#df.to_pickle('demand_data.pkl')
df = pd.read_pickle('demand_data.pkl')

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
# so order triggered on day 2
starting_value = rq_inputs.loc[rq_inputs.index[0], 'reorder_pt'] + demand_data.loc[demand_data.index[0], 'new_daily_demand'] + 10
demand_data.loc[demand_data.index[0], 'on_hand_il'] = starting_value


def sim_il(demand_data, rq_inputs):
    # create empty dataframe
    all_results = pd.DataFrame()

    # loop through r and q values
    for j in range(0, len(rq_inputs)):
        lead_time = rq_inputs.loc[rq_inputs.index[j], 'lead_time']
        reorder_pt = rq_inputs.loc[rq_inputs.index[j],'reorder_pt']
        reorder_qty = rq_inputs.loc[rq_inputs.index[j],'reorder_qty']

    # run through the inventory sim
    # NOTE: index starts at 0, so 1 is the second row
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

        demand_data['unmet_demand'] = (demand_data['new_daily_demand'] - demand_data['on_hand_il']).clip(lower=0)
        # calculate summary statistics
        results = calculate_metrics.calc_metrics(demand_data, reorder_qty)
        results['iteration'] = f"lt = {lead_time}, r = {reorder_pt}, q = {reorder_qty}"
        # append
        all_results = pd.concat(objs=[all_results, results], ignore_index=True)
    return all_results


# run the sim
results = sim_il(demand_data, rq_inputs)
