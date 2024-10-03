# calculate summary metrics
import pandas as pd


def calc_metrics(demand_data, reorder_qty):

    # remove first month of data
    grouped_df = demand_data[demand_data['order_date'] > '2023-01-31']

    # calculate metrics
    # grouping by dc and item_num to preserve sku-loc names in resulting df
    grouped_df = grouped_df.groupby(['dc', 'item_num']).agg({
        'delivery': 'sum',
        'unmet_demand': ['sum', lambda x: (x > 0).sum()],
        'on_hand_il': ['mean', 'max', 'min'],
        'new_daily_demand': ['sum', 'mean'],
        'order_date': 'count'
    })

    # rename the columns
    grouped_df.columns = ['units_delivered_total', \
                          'unmet_demand_qty', \
                          'unmet_demand_days', \
                          'daily_il_mean', 'daily_il_max', 'daily_il_min', \
                          'demand_total', 'daily_demand_mean', \
                          'days_of_sim'
                          ]

    # reset index
    grouped_df = grouped_df.reset_index()

    # calculate subsequent variables
    grouped_df['deliveries_total'] = grouped_df['units_delivered_total'] / reorder_qty
    grouped_df['days_of_supply_mean'] = grouped_df['daily_il_mean']/grouped_df['daily_demand_mean']
    grouped_df['days_of_supply_max'] = grouped_df['daily_il_max']/grouped_df['daily_demand_mean']
    grouped_df['days_of_supply_min'] = grouped_df['daily_il_min']/grouped_df['daily_demand_mean']
    grouped_df['fill_rate_days'] = grouped_df['unmet_demand_days']/grouped_df['days_of_sim']
    grouped_df['fill_rate_qty'] = grouped_df['unmet_demand_qty']/grouped_df['demand_total']

    return grouped_df


# test function
sim_demand_data = pd.read_csv('demand_data_sim1.csv')
reorder_qty = rq_inputs.loc[rq_inputs.index[0], 'reorder_qty']
test_results = calc_metrics(sim_demand_data, reorder_qty)
'''
