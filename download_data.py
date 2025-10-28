import yfinance as yf
import pandas as pd
import os
# Download and save stock data
# tickers = ["AAPL", "MSFT"]
# data = yf.download(tickers, start="2020-01-01", end="2025-01-01")["Close"]
# os.makedirs("data", exist_ok=True)
# for ticker in tickers:
#     data[[ticker]].to_csv(f"data/{ticker}_daily.csv")
# # Clean and align data
# print(data.head())
# aligned = data.dropna()
# aligned.to_csv("data/AAPL_MSFT_aligned.csv")
# print("Saved: data/AAPL_MSFT_aligned.csv")
# print(aligned.head())

tickers = ["KO", "PEP"]
data = yf.download(tickers, start="2020-01-01", end="2025-01-01")["Close"]
os.makedirs("data", exist_ok=True)
for ticker in tickers:
    data[[ticker]].to_csv(f"data/{ticker}_daily.csv")
print(data.head())
aligned = data.dropna()
aligned.to_csv("data/KO_PEP_aligned.csv")
print(aligned.head())
