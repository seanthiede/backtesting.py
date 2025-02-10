import pandas as pd

# Absoluter Pfad zur Datei
file_path = "/Users/seanthiede/Desktop/Programmieren/backtesting/data/btc_data_1d.csv"

# 📌 Überspringe die ersten **zwei Zeilen**, um zu den echten Daten zu gelangen
df = pd.read_csv(file_path, skiprows=2)
# 📌 Spalten manuell setzen (da sie anscheinend nicht korrekt erkannt werden)
df.columns = ["Date", "Close", "High", "Low", "Open", "Volume"]
# 📌 Setze das Datum als Index
df.set_index("Date", inplace=True)
# 📌 Stelle sicher, dass das Datum als Timestamp erkannt wird
df.index = pd.to_datetime(df.index)

# Debug: Zeige die ersten Zeilen
print(df.head())  
print(df.columns)  
print(df.index)  # Prüfe, ob das Datum jetzt korrekt als Index gesetzt ist
