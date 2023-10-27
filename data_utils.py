import quandl
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from contextlib import contextmanager

def data_fetch_decorator(func):
    def wrapper(self):
        try:
            # Fetch historical stock price data using Quandl
            # Replace 'YOUR_API_KEY' with your actual Quandl API key
            quandl.ApiConfig.api_key = 'YOUR_API_KEY'
            self.data = quandl.get('WIKI/' + self.symbol, start_date=self.start_date, end_date=self.end_date)
            # Check if data was successfully retrieved
            if self.data is not None and not self.data.empty:
                # Print the first few rows of the data frame to verify data retrieval
                pass
            else:
                print("No data retrieved. Check your dataset code and date range.")
        except Exception as e:
            print(f"An error occurred while fetching data: {str(e)}")

    return wrapper

@data_fetch_decorator
def fetch_data(self):
    pass

@contextmanager
def data_preprocess_context(self):
    try:
        yield
    except Exception as e:
        print(f"Error during data preprocessing: {str(e)}")

def preprocess_data(self):
    with data_preprocess_context():
        if self.data is None or self.data.isnull().values.any():
            print("NO DATA")
        self.data['MA_9'] = self.data['Adj. Close'].rolling(window=9).mean()
        self.data['MA_50'] = self.data['Adj. Close'].rolling(window=50).mean()
        self.data['MA_200'] = self.data['Adj. Close'].rolling(window=200).mean()
        if self.normalize_and_scale:
            scaler = MinMaxScaler()
            self.data[['Adj. Close', 'MA_9', 'MA_50', 'MA_200']] = scaler.fit_transform(
                self.data[['Adj. Close', 'MA_9', 'MA_50', 'MA_200']])
