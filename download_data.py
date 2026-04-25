import yfinance as yf
import pandas as pd
import os

tickers = ["KO", "PEP"]
data = yf.download(tickers, start="2020-01-01", end="2025-01-01")["Close"]
os.makedirs("data", exist_ok=True)
for ticker in tickers:
    data[[ticker]].to_csv(f"data/{ticker}_daily.csv")
print(data.head())
aligned = data.dropna()
aligned.to_csv("data/KO_PEP_aligned.csv")
print(aligned.head())


tickers = [
    "NEE", "DUK", "SO", "AEP", "EXC",
    "SRE", "PEG", "ED", "XEL", "ES",
    "WEC", "ETR", "FE", "PPL", "CMS",
    "NI", "ATO", "LNT", "EVRG", "PNW",
    "OGE", "NWE", "AVA", "IDA", "SR",
    "UTL", "AWK", "SWX", "NWN", "UGI"
]
data = yf. download(tickers, start="2024-01-01", end="2025-01-01")["Close"]
os.makedirs("PairsTrading/data", exist_ok=True)
for ticker in tickers:
    data[[ticker]].to_csv(f"PairsTrading/data/{ticker}_daily.csv")
print(data.head())
aligned = data.dropna(axis=1)
aligned.to_csv("data/30_Utility_Stock.csv")
print(aligned.head())
print(aligned.shape)
