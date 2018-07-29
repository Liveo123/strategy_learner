"""
    Strategy Learner by Paul Livesey (c)
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import datetime as dt


def exponential_mov_avg(prices, symbol, days = 10, chart = True):
    """ Create exponential moving average of "days" days.
        Create a chart if chart is set.
    """
    
    normed_prices = prices /prices[0]
    price_values = np.array(normed_prices.values)

    # Create the ema.
    alp = float(2) / (days + 1)
    ema = np.zeros(len(price_values))
    ema[0] = price_values[0]
    for cnt in range(1, len(price_values)):
        ema[cnt] = ema[cnt - 1] * (1 - alp) + price_values[cnt] * alp
    ema_df = pd.DataFrame(data=ema, index=normed_prices.index, columns=['vals'])
    # Turn the numpy ema into a DataFrame.
    ema_df = pd.DataFrame(ema, 
                          normed_prices.index, 
                          ['val'])

    # Display a chart if needed.
    if chart == True:

        price_chart = plt.plot(normed_prices, 
                               'g',
                               label = 'Price($)')
        moving_avg_chart = plt.plot(ema_df, 
                                    'r',
                                    label = '%d-day Exp Moving Average' % days)
        plt.title("%s EMA Chart" % symbol)
        plt.legend(loc='best')
        plt.show()

    to_return = price_values / ema - 1

    return to_return

def bollinger_bands(prices, symbol, chart = True, days = 10):
    """ Create Bollinger Bands using SMA of "days" days.
        Create a chart if chart is set.
    """
    normed_prices = prices / prices[0]
    price_values = np.array(normed_prices.values)
    
    # Calculate basic moving averages
    total = np.cumsum(price_values) 
    total[days :] = total[days :] - total[: -days]
    mov_avg_calc =  total[days - 1 : -1] / days

    # Create an array of nans the same as the sma window size (days)
    nans = np.empty(days)
    nans[:] = np.nan
    
    # Create moving averages
    moving_avg = np.concatenate((nans, mov_avg_calc))

    # Create standard deviations
    moving_std = np.array([np.nan] * days + 
                          [price_values[start : start + days].std() 
                          for start in range(len(prices) - days)])

    # Convert the moving averages and standard deviations 
    # into DataFrames.
    mov_avg_df = pd.DataFrame(moving_avg, 
                              normed_prices.index, 
                              ['val'])

    mov_std_df = pd.DataFrame(moving_std, 
                              normed_prices.index, 
                              ['val'])
    
    # Display a chart if needed.
    if chart == True:
        # Create charts for the Bollinger line on the top...
        top_bol, = plt.plot(mov_avg_df + 2 * mov_std_df, 
                            'b', 
                            label = "Bollinger")

        # ... and on the bottom.
        bottom_bol, = plt.plot(mov_avg_df - 2 * mov_std_df, 
                               'b')

        price_chart, = plt.plot(normed_prices, 
                                'g', 
                                label = "Prices($)")

        moving_avg_chart, = plt.plot(mov_avg_df, 
                                     'r', 
                                     label = "%d-days Moving Average" % days)

        plt.title("%s Bollinger(c) Bands Chart" % symbol)
        plt.legend(loc='best')
        plt.show()

    bol_band = (price_values - moving_avg) / (moving_std * 2)

    return bol_band

def simple_mov_avg(prices, symbol, chart = True, days = 10):
    """ Create simple moving average of the last "days" days  of prices
        Create a chart of the prices against the sma.
        SMA calculated by creating a rolling average of the last "days"
        days i.e. divide the last "days" days prices by days and add 
        the results to the mov_avg data structure.
    """
    #_Calculate
    df_prices = prices.to_frame() 
    mov_avg_df = df_prices.rolling(days).mean()

    # Display a chart if needed.
    if chart == True:
        price_chart = plt.plot(prices,
                               'r', 
                               label = 'Price ($)')

        moving_avg_chart = plt.plot(mov_avg_df, 
                                    'b', 
                                    label = '%d-days SMA' % days)

        plt.title("%s SMA Chart" % symbol)
        plt.legend(loc='best')
        plt.show()

    # TODO: Sort later - problem with number of return values, so
    # creating sma different way.  May have problem with timings
    normed_prices = prices/prices[0]
    price_values = np.array(normed_prices.values)
    total = np.cumsum(price_values) 
    total[days :] = total[days :] - total[: -days]
    mov_avg_calc =  total[days - 1 : -1] / days
    
    # Create an array of nans the same as the sma window size (days)
    nans = np.empty(days)
    nans[:] = np.nan

    # Join 'em together
    moving_avg = np.concatenate((nans, mov_avg_calc )) 
    sma = price_values / moving_avg - 1

    return sma



def author():
    return 'plivesey3'

if __name__ == '__main__':
    print "Let's Rock!!!"
