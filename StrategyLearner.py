"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""
import datetime
import pandas as pd
import numpy as np
import util as ut
import random
import BagLearner as bl
import RTLearner as rt
from marketsimcode import compute_portvals
from indicators import exponential_mov_avg, simple_mov_avg, bollinger_bands

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.N = 10
        self.window_size = 20
        self.bag = 10
        self.feature_size = 5 
        self.leaf_size = 5

        self.learner = bl.BagLearner(learner=rt.RTLearner,
                                     bags=self.bag,
                                     kwargs={"leaf_size":self.leaf_size})

    def addEvidence(self, symbol = "IBM", \
        sd=datetime.datetime(2008,1,1), \
        ed=datetime.datetime(2009,1,1), \
        sv = 10000):
        
        BASE_THRESHOLD = 0.03

        # Load up the relevant price data form the csv
        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        prices = prices[symbol]

        # Calculate the Bollinger, the Simple Moving Average and the
        # Exponetial Moving Average for the prices found.
        bol_band = bollinger_bands(prices,
                                   symbol = symbol,
                                   chart = True,
                                   days = self.window_size)
        sma = simple_mov_avg(prices,
                             symbol = symbol, 
                             chart = False,
                             days = self.window_size)
        ema = exponential_mov_avg(prices,
                                  symbol = symbol,
                                  chart = False, 
                                  days = self.window_size)

        # Data and training structures
        X = []
        Y = []
        
        # threshold to determine whether it's a buy signal or a sell signal or nothing
        if BASE_THRESHOLD > 2 * self.impact:
            threshold = 0.03
        else:
            threshold = 2 * self.impact
       
        # Go through all of the prices within the window
        for i in range(self.window_size + self.feature_size + 1, 
                       len(prices) - self.N):

            X.append( np.concatenate((sma[i - self.feature_size : i],
                                      bol_band[i - self.feature_size : i],
                                      ema[i - self.feature_size : i])))

            # ret = (price[t+N]/price[t]) - 1.0
            ret = (prices.values[i + self.N] - prices.values[i]) / \
                   prices.values[i]

            # From document:
            # classify that return as LONG, SHORT or CASH. You're 
            # trying to predict a relative change that you can use 
            # to invest with.
            # +1: LONG
            # 0: CASH
            # -1: SHORT
            if ret > threshold:
                Y.append(1)
            elif ret < -threshold:
                Y.append(-1)
            else:
                Y.append(0)

        X = np.array(X)
        Y = np.array(Y)
        self.learner.addEvidence(X, Y)

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=datetime.datetime(2009,1,1), \
        ed=datetime.datetime(2010,1,1), \
        sv = 10000):

        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        trades = prices_all[[symbol,]].copy(deep=True)  # only portfolio symbols
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later

        # Get the price data from csv files
        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        prices = prices[symbol]
        curr_hold = 0

        # Calculate the Bollinger, the Simple Moving Average and the
        # Exponetial Moving Average for the prices found.
        bol_band = bollinger_bands(prices,
                                   symbol = symbol, 
                                   chart = True,
                                   days = self.window_size)
        sma = simple_mov_avg(prices,
                             symbol = symbol, 
                             chart = False,
                             days = self.window_size)
        ema = exponential_mov_avg(prices,
                                  symbol = symbol, 
                                  chart = False, 
                                  days = self.window_size)

        trades.values[:, :] = 0
        Xtest = []

        for i in range(self.window_size + self.feature_size + 1,
                       len(prices) - 1):
            data = np.concatenate((sma[i - self.feature_size : i], \
                                  bol_band[i - self.feature_size : i], \
                                  ema[i - self.feature_size : i]))
            Xtest.append(data)

        res = self.learner.query(np.array(Xtest))

        for i, r in enumerate(res):
            # These are for buys...
            if r > 0:
                trades.values[i + self.window_size \
                                + self.feature_size + 1, : ] \
                                = 1000 - curr_hold

                curr_hold = 1000
            #... or sells
            else:
                trades.values[i + self.window_size \
                                + self.feature_size + 1, :] \
                                = - 1000 - curr_hold
                curr_hold = -1000

        if self.verbose: print type(trades) 
        if self.verbose: print trades
        if self.verbose: print prices_all

        return trades

    def author():
        return 'plivesey3'

if __name__=="__main__":
    print "Hoff"
