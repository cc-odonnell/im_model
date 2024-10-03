# Scale the simulation across multiple items and locations
# Use the "groupby" function

import pandas as pd
import numpy as np
import calculate_metrics
import prep_demand_data_for_sim

def sim_il_metrics(demand_data, rq_inputs):
    # create empty dataframe
    all_results = pd.DataFrame()

    # loop through r and q values
    for j in range(0, len(rq_inputs)):
        mean_daily_demand = demand_data['new_daily_demand'].mean()
        r = rq_inputs.loc[rq_inputs.index[j], 'reorder_pt']
        q = rq_inputs.loc[rq_inputs.index[j], 'reorder_qty']
        lead_time = rq_inputs.loc[rq_inputs.index[j], 'lead_time']
        reorder_pt = r * mean_daily_demand
        reorder_qty = q * mean_daily_demand

        # set starting values
        demand_data = prep_demand_data_for_sim.prep_data(demand_data, reorder_pt)

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
        results['iteration'] = f"lt = {lead_time}, r = {r}, q = {q}"
        # append
        all_results = pd.concat(objs=[all_results, results], ignore_index=True)

    return all_results


# test the sim

# set my rq inputs (use just 1 row for testing)
### CHANGE THIS TO DAYS OF SUPPLY !!!
rq = {"lead_time": [10], "reorder_pt": [10], "reorder_qty": [1]}
rq_inputs = pd.DataFrame(rq)

# get data from 'generate_data.py'
df = pd.read_pickle('demand_data.pkl')

# subset to 1 SKU and 1 location
demand_data = df[(df['item_num'] == 10000) & (df['dc'] == "A")]

# subset to 1 SKU, but all DC locations (A,B,C)
# demand_data = df[(df['item_num'] == 10000)]

results = sim_il(demand_data, rq_inputs)

''' now run over many item locations

grouped = demand_data.groupby(['item', 'location'])

# define a list to store results
results = []


# iterating over grouped object
for (itemName, locationName), groupData in grouped:
    # filter the rq_inputs for the specific item and location
    rq_inputs_specific = rq_inputs[(rq_inputs['item'] == itemName) & (rq_inputs['location'] == locationName)]

    result = sim_il(groupData, rq_inputs_specific, itemName, locationName)
    results.append(result)

# concatenate results into a final DataFrame
final_results = pd.concat(results)
