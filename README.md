# strategy_learner

For this part of the project you should develop a learner that can learn a trading policy using your learner. You should be able to use your Q-Learner or RTLearner from the earlier project directly, with no changes. If you want to use the optimization approach, you will need to create new code or that. You will need to write code in StrategyLearner.py to "wrap" your learner appropriately to frame the trading problem for it. Utilize the template provided in StrategyLearner.py.

Your StrategyLearner should implement the following API:

import StrategyLearner as sl
learner = sl.StrategyLearner(verbose = False, impact = 0.000) # constructor
learner.addEvidence(symbol = "AAPL", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000) # training phase
df_trades = learner.testPolicy(symbol = "AAPL", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000) # testing phase

The input parameters are:

    verbose: if False do not generate any output
    impact: The market impact of each transaction.
    symbol: the stock symbol to train on
    sd: A datetime object that represents the start date
    ed: A datetime object that represents the end date
    sv: Start value of the portfolio

The output result is:

    df_trades: A data frame whose values represent trades for each day. Legal values are +1000.0 indicating a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING. Values of +2000 and -2000 for trades are also legal when switching from long to short or short to long so long as net holdings are constrained to -1000, 0, and 1000.
    
    
Write a report describing your system. The centerpiece of your report should be the description of how you utilized your learner to determine trades:

    Describe the steps you took to frame the trading problem as a learning problem for your learner. What are your indicators? Did you adjust the data in any way (dicretization, standardization)? Why or why not?

    NEW Describe at least 3 and at most 5 technical indicators that you used. You may find our lecture on time series processing to be helpful. For each indicator you should create a single, compelling chart that illustrates the indicator. As an example, you might create a chart that shows the price history of the stock, along with "helper data" (such as upper and lower bollinger bands) and the value of the indicator itself. Another example: If you were using price/SMA as an indicator you would want to create a chart with 3 lines: Price, SMA, Price/SMA. In order to facilitate visualization of the indicator you might normalize the data to 1.0 at the start of the date range (i.e. divide price[t] by price[0]). Your report description of each indicator should enable someone to reproduce it just by reading the description. We want a written description here, not code, however, it is OK to augment your written description with a pseudocode figure. At least one of the indicators you use should be completely different from the ones presented in our lectures. (i.e. something other than SMA, Bollinger Bands, RSI).

* Experiment 1: Using exactly the same indicators that you used in manual_strategy, compare your manual strategy with your learning strategy in sample.

    Experiment 1: Using the benchmark described above, plot the performance of the benchmark versus your strategy in sample. Trade only the symbol JPM for this evaluation. The code that implements this experiment and generates the relevant charts and data should be submitted as experiment1.py
        Describe your experiment in detail: Assumptions, parameter values and so on.
        Describe the outcome of your experiment.
        Would you expect this relative result every time with in-sample data? Explain why or why not.
    Experiment 2: Provide an hypothesis regarding how changing the value of impact should affect in sample trading behavior and results (provide at least two metrics). Conduct an experiment with JPM on the in sample period to test that hypothesis. Provide charts, graphs or tables that illustrate the results of your experiment. The code that implements this experiment and generates the relevant charts and data should be submitted as experiment2.py

In situations other than Experiment 1, you may choose to use other indicators than the ones you used in manual strategy. If this is the case, be sure to indicate that in your report. Your descriptions should be stated clearly enough that an informed reader could reproduce the results you report.

The report can be up to 2500 words long and contain up to NEW 9 figures (charts and/or tables). 
