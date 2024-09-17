# calculate summary metrics


# from run_sim.py
# demand_data.to_csv('demand_data_sim1.csv')

# remove first month of data ?

########### calculate metrics


'''
# aggregations
total_units_delivered = sum(delivery),
fill_rate_pct_met_demand_qty = sum(unmet_demand),
fill_rate_pct_met_demand_days = sum(unmet_demand > 0)
daily_il_mean = mean(on_hand_il),
daily_il_max = max(on_hand_il),
daily_il_min = min(on_hand_il),
daily_demand_mean = mean(new_daily_demand),
deliveries = total_units_delivered/reorder_qty,
days_of_supply_mean = daily_il_mean / daily_demand_mean,
days_of_supply_max = daily_il_max / daily_demand_mean,
days_of_supply_min = daily_il_min / daily_demand_mean,
'''

grouped_df = demand_data.groupby(['dc', 'item_num']).agg({
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
grouped_df['total_deliveries'] = grouped_df['total_units_delivered'] / 80000
grouped_df['days_of_supply_mean'] = grouped_df['daily_il_mean']/grouped_df['daily_demand_mean']
grouped_df['days_of_supply_max'] = grouped_df['daily_il_max']/grouped_df['daily_demand_mean']
grouped_df['days_of_supply_min'] = grouped_df['daily_il_min']/grouped_df['daily_demand_mean']

# alternative to the above
'''
columns_to_divide = ['daily_il_mean', 'daily_il_max']
grouped_df[["days_of_supply_mean", "days_of_supply_max"]] = grouped_df[columns_to_divide].div(
    grouped_df['daily_demand_mean'], axis=0)
    '''

# transpose table
results = grouped_df.round(0).transpose()