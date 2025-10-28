import pandas as pd
# csv_path = "data/AAPL_MSFT_aligned.csv"
# table = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")
# table["Spread_Diff"] = table["AAPL"]-table["MSFT"]
# table.to_csv("data/AAPL_MSFT_spread.csv", index=False)
# average = table["Spread_Diff"].dropna().mean()
# deviation = table["Spread_Diff"].dropna().std()
# table["Z"] = (table["Spread_Diff"] - average) / deviation
# signal = []
# position = "Flat"
# for i in table["Z"]:
#     if position == "Flat":
#         if i > 2:
#             signal.append("ENTER: Short AAPL / Long MSFT")
#             position = "Shortspread"
#         elif i < -2:
#             signal.append("ENTER: Long AAPL / Short MSFT")
#             position = "Longspread"
#         else:
#             signal.append("")
#     elif position == "ENTER: Shortspread":
#         if -0.5 <= i <= 0.5:
#             signal.append("Exit")
#             position = "Flat"
#         else:
#             signal.append("")
#     elif position == "Longspread":
#         if -0.5 <= i <= 0.5:
#             signal.append("Exit")
#             position = "Flat"
#         else:
#             signal.append("")

# table["Signal"] = signal
# print(table.head())
# table.to_csv("data/AAPL_MSFT_spread_signal.csv")


csv_path = ("data/KO_PEP_aligned.csv")
table = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")
table["Spread_Diff"] = table["KO"]-table["PEP"]
table.to_csv("data/KO_PEP_spread.csv", index=False)
average = table["Spread_Diff"].dropna().mean()
deviation = table["Spread_Diff"].dropna().std()
table["Z"] = (table["Spread_Diff"] - average) / deviation
signal = []
position = "Flat"
for i in table["Z"]:
    if position == "Flat":
        if i > 2:
            signal.append("ENTER: Short KO / Long PEP")
            position = "Shortspread"
        elif i < -2:
            signal.append("ENTER: Long KO / Short PEP")
            position = "Longspread"
        else:
            signal.append("")
    elif position == "Shortspread":
        if -0.5 <= i <= 0.5:
            signal.append("Exit")
            position = "Flat"
        else:
            signal.append("")
    elif position == "Longspread":
        if -0.5 <= i <= 0.5:
            signal.append("Exit")
            position = "Flat"
        else:
            signal.append("")

table["Signal"] = signal
trade_log = table[(table["Signal"].notna()) & (table["Signal"] != "")]
table.to_csv("data/KO_PEP_spread_signal.csv", index=True)
trade_log.to_csv("data/KO_PEP_trades.csv", index=True)
print(table.head())
print(table[table["Signal"] != ""][["Z", "Signal"]])
print(table["Z"].min(), table["Z"].max())
