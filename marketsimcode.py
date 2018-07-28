import pandas as pd
import numpy as np
import datetime as dt

def compute_portvals(orders_df, prices, start_val=100000, commission = 0, impact = 0):
    """ Compute portvals recreated as other was broken.
    """

    hold_df = pd.DataFrame(np.ones(len(prices)) * 0, 
                           prices.index, 
                           ['val'])

    cash_df = pd.DataFrame(np.ones(len(prices)) * start_val, 
                           prices.index, 
                           ['val'])

    test = 0
    for cnt in range(0, len(prices.index)):
        cash_diff = 0

        if orders_df.values[cnt][0] != 0:
            if orders_df.values[cnt][0] > 0:
                cash_diff =(1 + impact) * \
                             abs(orders_df.values[cnt][0]) * \
                             prices.values[cnt]
            else:
                cash_diff = (-1 + impact) * \
                              abs(orders_df.values[cnt][0]) * \
                              prices.values[cnt]

            cash_diff += commission

        if cnt == 0:
            cash_df['val'].iloc[cnt] -= cash_diff
            hold_df['val'].iloc[cnt] += orders_df.values[cnt][0]
        else:
            cash_df['val'].iloc[cnt] = cash_df['val'].iloc[cnt - 1] - cash_diff
            hold_df['val'].iloc[cnt] = hold_df['val'].iloc[cnt - 1] + orders_df.values[cnt][0]
        
        test += 1
        
    shares_df = hold_df.val * prices
    portvals = shares_df + cash_df.val

    return portvals

def author():
    return 'plivesey3'

if __name__ == "__main__":
    print "Go Baby!!!"
