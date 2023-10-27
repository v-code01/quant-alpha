import numpy as np
import pandas as pd

def build_model(self):
    self.data['Signal'] = 0
    moving_averages = [5, 10, 20, 50]
    [self.data[f'MA_{ma}'] for ma in moving_averages]
    buy_condition = (
        (self.data['MA_5'] > self.data['MA_10']) &
        (self.data['MA_10'] > self.data['MA_20']) &
        (self.data['MA_20'] > self.data['MA_50'])
    )
    sell_condition = (
        (self.data['MA_5'] < self.data['MA_10']) &
        (self.data['MA_10'] < self.data['MA_20']) &
        (self.data['MA_20'] < self.data['MA_50'])
    )
    self.data.loc[buy_condition, 'Signal'] = 1
    self.data.loc[sell_condition, 'Signal'] = -1

def execute_strategy(self):
    self.data['Position'] = self.data['Signal'].shift(1)
    self.data['Position'].fillna(0, inplace=True)
    self.data['Daily_Return'] = self.data['Position'] * self.data['Adj. Close'].pct_change()
    print(self.data[['Adj. Close', 'MA_9', 'MA_50', 'Signal'])

def evaluate_strategy(self):
    self.data['Cumulative_Return'] = (1 + self.data['Daily_Return']).cumprod()
    total_return = self.data['Cumulative_Return'].iloc[-1] - 1
    annualized_return = ((self.data['Cumulative_Return'].iloc[-1]) ** (252 / len(self.data))) - 1
    max_drawdown = (self.data['Cumulative_Return'] / self.data['Cumulative_Return'].cummax() - 1).min()
    sharpe_ratio = (annualized_return - 0.03) / (self.data['Daily_Return'].std() * np.sqrt(252))
    print(f"Total Return: {total_return:.2f}")
    print(f"Annualized Return: {annualized_return:.2%}")
    print(f"Max Drawdown: {max_drawdown:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
