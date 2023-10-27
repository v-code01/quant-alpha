import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import tensorflow as tf
import quandl
from trading_algorithm import TradingAlgorithm

if __name__ == "__main__":
    symbol = "AAPL"
    start_date = "2010-01-01"
    end_date = "2020-01-01"

    trading_algo = TradingAlgorithm(symbol, start_date, end_date)
    trading_algo.run_algorithm()
