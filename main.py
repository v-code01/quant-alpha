import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import tensorflow as tf
import quandl  # Import the Quandl library

# Define the AI-Driven Trading Algorithm
from sklearn.preprocessing import MinMaxScaler

class TradingAlgorithm:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.model = None
        self.portfolio = None
        self.normalize_and_scale = True  # Set to True to normalize and scale the data

    def fetch_data(self):
        try:
            # Fetch historical stock price data using Quandl
            # Replace 'YOUR_API_KEY' with your actual Quandl API key
            quandl.ApiConfig.api_key = 'YOUR_API_KEY'
            self.data = quandl.get('WIKI/'+self.symbol, start_date=self.start_date, end_date=self.end_date)
            # Check if data was successfully retrieved
            if self.data is not None and not self.data.empty:
                # Print the first few rows of the data frame to verify data retrieval
                pass
            else:
                print("No data retrieved. Check your dataset code and date range.")
        #BASIC ERROR HANDLING
        except Exception as e:
            print(f"An error occurred while fetching data: {str(e)}")

    def preprocess_data(self):
        # Perform data preprocessing, including feature engineering and cleaning
        if self.data is None or self.data.isnull().values.any():
            print("NO DATA")
        # Adding technical indicators (Moving Averages)
        self.data['MA_9'] = self.data['Adj. Close'].rolling(window=9).mean()
        self.data['MA_50'] = self.data['Adj. Close'].rolling(window=50).mean()
        self.data['MA_200'] = self.data['Adj. Close'].rolling(window=200).mean()

        # Normalize and scale the data
        if self.normalize_and_scale:
            scaler = MinMaxScaler()
            self.data[['Adj. Close', 'MA_9', 'MA_50', 'MA_200']] = scaler.fit_transform(
                self.data[['Adj. Close', 'MA_9', 'MA_50', 'MA_200']])


    def build_model(self):
        self.data['Signal'] = 0  # Initialize the signal column

        # Generate signals based on moving average crossovers
        # Using additional short-term moving averages for more setups
        self.data['MA_5'] = self.data['Adj. Close'].rolling(window=5).mean()
        self.data['MA_10'] = self.data['Adj. Close'].rolling(window=10).mean()
        self.data['MA_20'] = self.data['Adj. Close'].rolling(window=20).mean()
        self.data['MA_50'] = self.data['Adj. Close'].rolling(window=50).mean()

        # Buy signal conditions (confirmation-based)
        buy_condition = (
                (self.data['MA_5'] > self.data['MA_10']) &
                (self.data['MA_10'] > self.data['MA_20']) &
                (self.data['MA_20'] > self.data['MA_50'])
        )

        # Sell signal conditions (confirmation-based)
        sell_condition = (
                (self.data['MA_5'] < self.data['MA_10']) &
                (self.data['MA_10'] < self.data['MA_20']) &
                (self.data['MA_20'] < self.data['MA_50'])
        )

        # Assign signals based on conditions
        self.data.loc[buy_condition, 'Signal'] = 1  # Buy signal
        self.data.loc[sell_condition, 'Signal'] = -1  # Sell signal


    def execute_strategy(self):
        # Implement the trading strategy using the generated signals
        self.data['Position'] = self.data['Signal'].shift(1)  # Shift signals by one day to avoid look-ahead bias
        self.data['Position'].fillna(0, inplace=True)

        # Calculate daily returns based on position changes and actual daily returns
        self.data['Daily_Return'] = self.data['Position'] * self.data['Adj. Close'].pct_change()

        # Print out the buy/sell signals
        print(self.data[['Adj. Close', 'MA_9', 'MA_50', 'Signal']])

    def evaluate_strategy(self):
        self.data['Cumulative_Return'] = (1 + self.data['Daily_Return']).cumprod()
        total_return = self.data['Cumulative_Return'].iloc[-1] - 1
        annualized_return = ((self.data['Cumulative_Return'].iloc[-1]) ** (252 / len(self.data))) - 1
        max_drawdown = (self.data['Cumulative_Return'] / self.data['Cumulative_Return'].cummax() - 1).min()
        sharpe_ratio = (annualized_return - 0.03) / (self.data['Daily_Return'].std() * np.sqrt(252))

        # Print out the performance metrics
        print(f"Total Return: {total_return:.2f}")
        print(f"Annualized Return: {annualized_return:.2%}")
        print(f"Max Drawdown: {max_drawdown:.2%}")
        print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

    def run_algorithm(self):
        # Execute the entire trading algorithm
        self.fetch_data()
        self.preprocess_data()
        self.build_model()
        self.execute_strategy()
        self.evaluate_strategy()

if __name__ == "__main__":
    # Define the parameters for the trading algorithm
    symbol = "AAPL"#only use TOP 500 COMPANIES FOR HIGH PROBABILITY CONDITIONS
    start_date = "2010-01-01"
    end_date = "2020-01-01"

    # Create an instance of the TradingAlgorithm
    trading_algo = TradingAlgorithm(symbol, start_date, end_date)

    # Run the trading algorithm
    trading_algo.run_algorithm()
