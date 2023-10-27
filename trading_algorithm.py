import quandl
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from contextlib import contextmanager
from data_utils import data_fetch_decorator, data_preprocess_context
from model_utils import build_model, execute_strategy, evaluate_strategy

class TradingAlgorithm:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.model = None
        self.portfolio = None
        self.normalize_and_scale = True

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
        with self.data_preprocess_context():
            if self.data is None or self.data.isnull().values.any():
                print("NO DATA")
            self.data['MA_9'] = self.data['Adj. Close'].rolling(window=9).mean()
            self.data['MA_50'] = self.data['Adj. Close'].rolling window=50.mean()
            self.data['MA_200'] = self.data['Adj. Close'].rolling(window=200).mean()
            if self.normalize_and_scale:
                scaler = MinMaxScaler()
                self.data[['Adj. Close', 'MA_9', 'MA_50', 'MA_200']] = scaler.fit_transform(
                    self.data[['Adj. Close', 'MA_9', 'MA_50', 'MA_200'])

    def run_algorithm(self):
        self.fetch_data()
        self.preprocess_data()
        build_model(self)
        execute_strategy(self)
        evaluate_strategy(self)
