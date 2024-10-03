# calculate summary metrics
import pandas as pd


def calc_metrics(demand_data, reorder_qty):

    # remove first month of data
    grouped_df = demand_data[demand_data['order_date'] > '2023-01-31']

    # calculate metrics
    grouped_df = grouped_df.groupby(['dc', 'item_num']).agg({
        'delivery': 'sum',
        'unmet_demand': ['sum', lambda x: (x > 0).sum()],
        'on_hand_il': ['mean', 'max', 'min'],
        'new_daily_demand': 'mean'
    })

    # rename the columns
    grouped_df.columns = ['total_units_delivered', \
                          'fill_rate_pct_met_demand_qty', \
                          'fill_rate_pct_met_demand_days', \
                          'daily_il_mean', 'daily_il_max', 'daily_il_min', \
                          'daily_demand_mean'
                          ]

    # reset index
    grouped_df = grouped_df.reset_index()

    # calculate subsequent variables
    grouped_df['total_deliveries'] = grouped_df['total_units_delivered'] / reorder_qty
    grouped_df['days_of_supply_mean'] = grouped_df['daily_il_mean']/grouped_df['daily_demand_mean']
    grouped_df['days_of_supply_max'] = grouped_df['daily_il_max']/grouped_df['daily_demand_mean']
    grouped_df['days_of_supply_min'] = grouped_df['daily_il_min']/grouped_df['daily_demand_mean']

    return grouped_df


'''# test function
sim_demand_data = pd.read_csv('demand_data_sim1.csv')
reorder_qty = rq_inputs.loc[rq_inputs.index[0], 'reorder_qty']
test_results = calc_metrics(sim_demand_data, reorder_qty)
'''
