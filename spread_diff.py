import pandas as pd
csv_path = "data/AAPL_MSFT_aligned.csv"
table = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")
table["Spread_Diff"] = table["AAPL"]-table["MSFT"]
table.to_csv("data/AAPL_MSFT_spread.csv", index=False)
table["Spread_Diff"].mean()
table["Spread_Diff"].std()

# print("First 5 rows")
# print(table.head())
