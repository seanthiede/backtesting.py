import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

# absolute path to file
file_path = "/Users/seanthiede/Desktop/Programmieren/backtesting/data/btc_data_1d.csv"

# load data
df = pd.read_csv(file_path, skiprows=2)

# format data (Backtesting.py wants OHLCV)
df.columns = ["Date", "Close", "High", "Low", "Open", "Volume"]
df.set_index("Date", inplace=True)
df.index = pd.to_datetime(df.index)

# define market cycles
timeframes = {
    "2014-2017": df.loc["2014-01-01":"2017-12-31"],
    "2017-2020": df.loc["2017-01-01":"2020-12-31"],
    "2020-2024": df.loc["2020-01-01":"2024-12-31"]
}

# define strategy
class SmaCross(Strategy):
    short_window = 10 # short term sma
    long_window = 20 # long term sma

    def init(self):
        self.short_sma = self.I(SMA, self.data.Close, self.short_window)
        self.long_sma = self.I(SMA, self.data.Close, self.long_window)

    def next(self):
        if crossover(self.short_sma, self.long_sma):
            self.buy()
        elif crossover(self.long_sma, self.short_sma):
            self.sell()

    @classmethod
    def optimize(cls, short_window=range(5, 50, 5), long_window=range(10, 100, 10)):
        return super().optimize(short_window=short_window, long_window=long_window)

# backtest for every timeframe
for label, df_subset in timeframes.items():
     print(f"\n🚀 Backtest für Zeitraum: {label}")


# start backtest
bt = Backtest(df, SmaCross, cash=1_000_000, commission=0.003)

# automatic optimization of the smas
optimized_result = bt.optimize(
    short_window = range(5, 50, 5),
    long_window = range(10, 100, 10), 
    maximize="Return [%]" # maximizes return
)

# print best sma values
print("Optimierte Parameter:", optimized_result._strategy.short_window, optimized_result._strategy.long_window)

# run optimated strategy
result = bt.run()

# print results and visualize performance
print(result)   
bt.plot()