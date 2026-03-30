import pandas as pd
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
# print(table.head())
# print(table[table["Signal"] != ""][["Z", "Signal"]])
# print(table["Z"].min(), table["Z"].max())

# BackTesting
trade_status = False
direction = None
for date, row in trade_log.iterrows():
    print(date)
    print(row["Signal"])
    print(row["KO"])
    print(row["PEP"])
    if (trade_status == False and row["Signal"] == "ENTER: Long KO / Short PEP"):
        print("Trade Open")
        trade_status = True
        direction = "Long KO / Short PEP"
    elif (trade_status == False and row["Signal"] == "ENTER: Short KO / Long PEP"):
        print("Trade open")
        trade_status = True
        direction = "Short KO / Long PEP"
    elif (trade_status == True and row["Signal"] == "Exit"):
        print("Trade close")
        trade_status = False
        direction = None
