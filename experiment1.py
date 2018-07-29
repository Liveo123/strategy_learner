import datetime
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import util as ut
import BagLearner as bl
import DTLearner as dt
from indicators import exponential_mov_avg, simple_mov_avg, bollinger_bands
import StrategyLearner as sl
import ManualStrategy as ms
from marketsimcode import compute_portvals

if __name__ == '__main__':
   
    VERBOSE = True

    # Symbol and dates specified in rules
    SYMBOL_TO_CHECK = 'JPM'
    start_date = datetime.datetime(2008, 1, 1)
    end_date = datetime.datetime(2009, 12, 31)
    dates = pd.date_range(start_date, end_date)

    # Grab the Prices for SYMBOL_TO_CHECK from the file
    sym_prices = ut.get_data([SYMBOL_TO_CHECK], pd.date_range(start_date, end_date))
    if VERBOSE == True:
        print "sym_prices"
        print sym_prices.head(10)

    sym_prices = sym_prices[SYMBOL_TO_CHECK]

    if VERBOSE == True:
        print "sym_prices"
        print sym_prices.head(10)

    # Add SPY to the table
    every_price = ut.get_data([SYMBOL_TO_CHECK], dates) 
    if VERBOSE == True:
        print "every price"
        print every_price.head(10)
    benchmark_trades = every_price[[SYMBOL_TO_CHECK,]]
    if VERBOSE == True:
        print "benchmark trades"
        print benchmark_trades.head(10)
    benchmark_trades.values[:, :] = 0
    benchmark_trades.values[0, :] = 1000
    if VERBOSE == True:
        print "benchmark trades"
        print benchmark_trades.head(10)

    benchmark_values = compute_portvals(benchmark_trades, sym_prices)
    if VERBOSE == True:
        print "benchmark_values"
        print benchmark_values.head(10)

    # Create a learner
    learner = sl.StrategyLearner(verbose = False, impact = 0)
    # Train the learner
    learner.addEvidence(symbol = SYMBOL_TO_CHECK, 
                        sd=start_date, 
                        ed=end_date, 
                        sv = 100000)
    # Test the learner
    df_trades = learner.testPolicy(symbol = SYMBOL_TO_CHECK, 
                                   sd=start_date, 
                                   ed=end_date, 
                                   sv = 100000)

    classification_values = compute_portvals(df_trades, 
                                             sym_prices, 
                                             impact = 0)
    if VERBOSE == True:
        print "classification_values"
        print classification_values.head(10)

    benchmark_values = benchmark_values / benchmark_values[0]
    classification_values = classification_values / classification_values[0]

    # Create a graph of the results
    benchmark_chart, = plt.plot(benchmark_values, 
                                'b', 
                                label = "Benchmark Prices")
    classification_chart, = plt.plot(classification_values, 
                                     'r', 
                                     label = "Classification Prices")
    plt.title("Comparing Strategies")
    plt.legend(handles=[benchmark_chart, classification_chart], loc=2)
    plt.show()
    
    # Output the descriptive statistics of the results.
    print "      Benchmark Results"
    print " ----------------------------"
    print benchmark_values.describe()
    print "cumsum = %g" % benchmark_values[1].cumsum()

    print "      Classification Results"
    print " ----------------------------"
    print classification_values.describe()

def author():
    return 'plivesey'
