

def sim_il_data(demand_data, rq_inputs):
    # create empty dataframe
    all_results = pd.DataFrame()

    # loop through r and q values
    for j in range(0, len(rq_inputs)):
        mean_daily_demand = int(round(demand_data['new_daily_demand'].mean()))
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

    return demand_data


data_results = sim_il_data(demand_data, rq_inputs)
