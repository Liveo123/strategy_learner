import pandas as pd
import numpy as np
import datetime as dt

def compute_portvals(orders_df, prices, start_val=100000, commission = 0, impact = 0):
    """ Compute portvals
    """

    hold_df = pd.DataFrame(np.ones(len(prices)) * 0, 
                           prices.index, 
                           ['val'])

    cash_df = pd.DataFrame(np.ones(len(prices)) * start_val, 
                           prices.index, 
                           ['val'])
    cnt = 0

    for cnt in range(len(prices.index)):
        cash_change = 0

        if orders_df.values[cnt][0] != 0:
            if orders_df.values[cnt][0] > 0:
                cash_change =(1 + impact) * \
                             abs(orders_df.values[cnt][0]) * \
                             prices.values[cnt]
            else:
                cash_change = (-1 + impact) * \
                              abs(orders_df.values[cnt][0]) * \
                              prices.values[cnt]

            cash_change += commission

        if cnt == 0:
            cash_df['val'].iloc[cnt] -= cash_change
            hold_df['val'].iloc[cnt] += orders_df.values[cnt][0]
            continue

        cash_df['val'].iloc[cnt] = cash_df['val'].iloc[cnt - 1] - cash_change
        hold_df['val'].iloc[cnt] = hold_df['val'].iloc[cnt - 1] + orders_df.values[cnt][0]

    shares_df = hold_df.val * prices
    portvals = shares_df + cash_df.val

    return portvals

def author():
    return 'plivesey3'

if __name__ == "__main__":
    print "Go Baby!!!"
