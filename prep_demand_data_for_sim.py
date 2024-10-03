# Turn this into a function and put this function inside sim_il

def prep_data(demand_data, reorder_pt):

    # make sure date is set as index
    demand_data = demand_data.reset_index(drop=True)

    # add new placeholder columns
    demand_data['on_hand_il'] = 0
    demand_data['in_transit_il'] = 0
    demand_data['total_il'] = 0
    demand_data['delivery'] = 0

    # set the first day of inventory
    # so order triggered on day 2
    starting_value = demand_data.loc[demand_data.index[0], 'new_daily_demand'] + reorder_pt + 10
    demand_data.loc[demand_data.index[0], 'on_hand_il'] = starting_value

    return demand_data

''' # test function
df = pd.read_pickle('demand_data.pkl')
test_demand_data = df[(df['item_num'] == 10000) & (df['dc'] == 'A')]
test_reorder_pt = 10
test_results = prep_data(test_demand_data, test_reorder_pt)
'''