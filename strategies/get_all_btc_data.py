import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# BTC Daten für verschiedene Zeitintervalle herunterladen
intervals = ["1d", "4h", "1h", "15m", "5m", "1m"]
btc_data = {}

for interval in intervals:
    btc_data[interval] = yf.download("BTC-USD", interval=interval, period="max")
    btc_data[interval].to_csv(f"btc_data_{interval}.csv") # Speichern der Daten