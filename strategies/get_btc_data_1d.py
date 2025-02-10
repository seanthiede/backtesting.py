import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf # Bibliothek für Candlestick charts

# Bitcoin daten abrufen
btc = yf.download("BTC-USD", start="2021-01-01", end="2024-01-01", interval="1d")

#CVS einlesen
df = pd.read_csv("btc_data_1d_21_to_24.csv", skiprows=2, index_col=0, parse_dates=True)

# daten anzeigen
#print(btc.head())

#Spalten umbennenen
df.columns = ["Open", "High", "Low", "Close", "Volume"]

"""
# Dataframe für mplfinance vorbereiten
df_mpf = df.copy()
df_mpf.index.name = "Date" # Sicherstellen, dass das Datum als Index gesetzt ist

# Candlestick-Chart zeichnen
mpf.plot(df_mpf, type="candle", style="charles", volume=True, title="Bitcoin Candlestick Chart (2021-2023)")
"""



#daten überprüfen
#print(df.head()) #zeigt die ersten 5 Zeilen
#print(df.tail()) #zeigt die letzten 5 Zeilen
#print(df.info())
#print(df.isnull().sum()) # auf fehlende Werte überprüfen
#print(df.index) # überprüft die Indizes
#print(df.index.min(), df.index.max()) #Zeigt das früheste und das späteste Datum
#print(df.shape)
#print(df.describe())

# Prüfen, ob es fehlende Tage gibt
#date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq="D")
#missing_dates = date_range.difference(df.index)

#print("Fehlende Tage:", missing_dates)

# Plot des Bitcoin Preises
"""
plt.figure(figsize=(12, 6)) # Grösse des Plots
plt.plot(df.index, df["Close"], label="Bitcoin Closing Price", color="blue")

# Titel und Achsenbeschriftungen
plt.title("Bitcoin Closing Price (2021-2023)")
plt.xlabel("Datum")
plt.ylabel("Preis in USD")
plt.legend()
plt.grid()

# Plot anzeigen
plt.show()
"""

"""
plt.figure(figsize=(12, 6))
plt.bar(df.index, df["Volume"], color="gray", alpha=0.6)

plt.title("Bitcoin Handelsvolumen (2021-2023)")
plt.xlabel("Datum")
plt.ylabel("Volumen (USD)")
plt.grid()
plt.show()
"""


# Gleitende Durchschnitte berechnen
df["SMA_50"] = df["Close"].rolling(window=50).mean()
df["SMA_200"] = df["Close"].rolling(window=200).mean()

"""
# Preis und Durchschnitte ploten
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Close"], label="BTC-Preis", color="blue", alpha=0.5)
plt.plot(df.index, df["Close"], label="50-Tage SMA", color="red")
plt.plot(df.index, df["Close"], label="200-Tage SMA", color="green")

plt.title("Bitcoin Preis mit 50-Tage & 200-Tage SMA (2021-2023)")
plt.xlabel("Datum")
plt.ylabel("Preis in USD")
plt.legend()
plt.grid()
plt.show()
"""


# daily returns berechnen
df["Daily Return"] = df["Close"].pct_change() # Prozentuale Änderung
df["Log Return"] = np.log(df["Close"] / df["Close"].shift(1)) # Logarithmische Rendite

"""
# daily returns visualisieren
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Daily Return"], label="Einfache Rendite", alpha=0.6)
plt.plot(df.index, df["Log Return"], label="Logarithmische Rendite", alpha=0.6)
plt.axhline(y=0, color="black", linestyle="--", linewidth=0.8)

# Titel und Achsenbeschriftungen
plt.title("Tägliche Renditen von Bitcoin")
plt.xlabel("Datum")
plt.ylabel("Rendite")
plt.legend()
plt.grid()
plt.show()
"""

"""
# Gleitende Durchschnitte berechnen
df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean() # 50-Tage EMA
df["EMA_200"] = df["Close"].ewm(span=200, adjust=False).mean() # 200-Tage EMA

# Preis und Durchschnitte visualisieren
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Close"], label="BTC-Preis", color="blue", alpha=0.5)
plt.plot(df.index, df["SMA_50"], label="50-Tage SMA", color="red")
plt.plot(df.index, df["SMA_200"], label="200-Tage SMA", color="green")
plt.plot(df.index, df["EMA_50"], label="50-Tage EMA", color="orange", linestyle="dashed")
plt.plot(df.index, df["EMA_200"], label="200-Tage EMA", color="purple", linestyle="dashed")

# Titel und Achsenbeschriftungen
plt.title("Bitcoin Preis mit SMA & EMA (2021-2023)")
plt.xlabel("Datum")
plt.ylabel("Preis in USD")
plt.legend()
plt.grid()
plt.show()
"""

"""
# RSI berechnen
window_length = 14 # Standardwert für RSI

# Gewinne und Verluste berechnen
delta = df["Close"].diff()
gain = np.where(delta > 0, delta, 0)
loss = np.where(delta < 0, -delta, 0)

# Durchschnittliche Gewinne & Verluste berechnen (glattender Durchschnitt)
avg_gain = pd.Series(gain).rolling(window=window_length, min_periods=1).mean()
avg_loss = pd.Series(loss).rolling(window=window_length, min_periods=1).mean()

# Durchschnittliche Verluste anpassen, um Division durch 0 zu verhindern
avg_loss = avg_loss.replace(0, 1e-10) # Ersetze 0 durch einen kleinen Wert

# Relative Stärke (RS) berechnen
rs = avg_gain / avg_loss

# RSI berechnen
df["RSI"] = 100 -(100 / (1 + rs))

# RSI visualisieren
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["RSI"], label="RSI", color="purple")
plt.axhline(70, linestyle="--", color="red", label="Überkauft (70)")
plt.axhline(30, linestyle="--", color="blue", label="Unterkauft (30)")

# Titel und Achsenbeschriftungen
plt.title("Bitcoin RSI (14 Tage)")
plt.xlabel("Datum")
plt.ylabel("RSI-Wert")
plt.legend()
plt.grid()
plt.show()

#print(df["RSI"].dropna().head(20)) # Zeigt die ersten 20 nicht-leeren Werte des RSI

# Gewinne und Verluste überprüfen
#print(delta.head(20)) # Zeigt die Preisänderung (delta)
#print(gain[:20])
#print(loss[:20])

# Durchschnittliche Gewinne und Verluste überprüfen
#print(avg_gain.head(20))
#print(avg_loss.head(20))

# RS überprüfen
#print(rs.head(20))

# WICHTIG: RSI wurde noch nicht angezeigt auf dem Graphen. Fehler selbst noch beheben!!
"""

# Bollinger Bänder berechnen
window = 20 # Fenstergrösse für den SMA 
df["Middle Band"] = df["Close"].rolling(window=window).mean()
df["Upper Band"] = df["Middle Band"] + 2 * df["Close"].rolling(window=window).std()
df["Lower Band"] = df["Middle Band"] - 2 *df["Close"].rolling(window=window).std()

# Bollinger Bänder visualisieren
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Close"], label="BTC-Preis", color="blue", alpha=0.5)
plt.plot(df.index, df["Middle Band"], label="Mittleres Band", color="green", linestyle="--")
plt.plot(df.index, df["Upper Band"], label="Oberes Band", color="red", linestyle="--")
plt.plot(df.index, df["Lower Band"], label="Unteres Band", color="purple", linestyle="--")

# Titel und Achsenbeschriftungen
plt.title("Bitcoin Bollinger Bände (20 Tage)")
plt.xlabel("Datum")
plt.ylabel("Preis in USD")
plt.legend()
plt.grid()
plt.show()


# CSV speichern
#btc.to_csv("btc_data_1d_21_to_24.csv")