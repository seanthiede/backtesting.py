import pandas as pd
import matplotlib.pyplot as plt

# Gespeicherte BTC-Daten laden (1d)
btc = pd.read_csv("btc_data_1d.csv", index_col=0, parse_dates=True, skiprows=2, header=None)

# Spaltennamen manuell einsetzen
btc.columns = ["Close", "High", "Low", "Open", "Volume"]

# Spalten in nummerische Werte umwandeln
btc = btc.apply(pd.to_numeric, errors="coerce")

# Überprüfen, ob fehlende Werte vorhanden sind
btc = btc.dropna() # Entfernt Zeilen mit NaN

# Berechnung der SMAs
btc["SMA 50"] = btc["Close"].rolling(window=50).mean()
btc["SMA 200"] = btc["Close"].rolling(window=200).mean()

# Kauf- und Verkaufssignale generieren
btc["Signal"] = 0
btc.loc[btc["SMA 50"] > btc["SMA 200"], "Signal"] = 1 # Kaufen
btc.loc[btc["SMA 50"] <= btc["SMA 200"], "Signal"] = -1 # Verkaufen

# Kapital simulieren
def backtest_strategy(data, initial_capital=1000000):
    capital = initial_capital
    position = 0 # Aktuelle Position: 0 = keine, >0 = long
    capital_history = []
    
    for i in range(len(data)):
        signal = data["Signal"].iloc[i]
        price = data["Close"].iloc[i]

        if signal == 1 and position == 0: # Kaufen
            position = capital / price
            capital = 0
        elif signal == -1 and position > 0: # Verkaufen
            capital = position * price
            position = 0

        capital_history.append(capital + (position * price if position > 0 else 0))

    data["Capital"] = capital_history
    
    return data

btc = backtest_strategy(btc)

# Visualisierung der Strategie
plt.figure(figsize=(12, 6))
plt.plot(btc.index, btc["Close"], label="Portfolio Value", color="green")
plt.legend()
plt.title("Portfolio Performance")
plt.xlabel("Date")
plt.ylabel("Portfolio Value")
plt.show()


