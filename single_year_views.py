# Takes the one-year IL data and generates diagnostic plots

import matplotlib.pyplot as plt

# data saved from simulation
demand_data2.to_csv('demand_data_sim1.csv')

def year_plot(demand_data):
    plt.figure(figsize=(10, 6))

    # Plot 'on_hand_il' with red color
    plt.plot(demand_data['order_date'], demand_data['on_hand_il'], color='red', label='on_hand_il')

    # Plot 'new_daily_demand' with blue color
    plt.plot(demand_data['order_date'], demand_data['new_daily_demand'], color='blue', label='new_daily_demand')

    plt.title('R = 10, Q = 5')
    plt.legend()
    plt.show()

year_plot(data_results)