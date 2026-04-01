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
trade_list = []
Entry_Date = None
Exit_Date = None
KO_Entry = None
KO_Exit = None
PEP_Entry = None
PEP_Exit = None
KO_PnL = None
PEP_PnL = None
Total_PnL = None
for date, row in trade_log.iterrows():
    signal_today = row["Signal"]
    ko_today = row["KO"]
    pep_today = row["PEP"]
    if (trade_status == False and row["Signal"] == "ENTER: Long KO / Short PEP"):
        Entry_Date = date
        KO_Entry = ko_today
        PEP_Entry = pep_today
        print("Trade Open")
        trade_status = True
        direction = "Long KO / Short PEP"
    elif (trade_status == False and row["Signal"] == "ENTER: Short KO / Long PEP"):
        Entry_Date = date
        KO_Entry = ko_today
        PEP_Entry = pep_today
        print("Trade Open")
        trade_status = True
        direction = "Short KO / Long PEP"
    elif (trade_status == True and row["Signal"] == "Exit"):
        Exit_Date = date
        KO_Exit = ko_today
        PEP_Exit = pep_today
        print("Trade Close")
        trade_status = False
        if (direction == "Long KO / Short PEP"):
            KO_PnL = KO_Exit - KO_Entry
            PEP_PnL = PEP_Entry - PEP_Exit
            Total_PnL = KO_PnL+PEP_PnL
        else:
            KO_PnL = KO_Entry-KO_Exit
            PEP_PnL = PEP_Exit-PEP_Entry
            Total_PnL = KO_PnL+PEP_PnL
        trade = {
            "Entry_Date": Entry_Date,
            "Exit_Date": Exit_Date,
            "Direction": direction,
            "KO_Entry": KO_Entry,
            "KO_Exit": KO_Exit,
            "PEP_Entry": PEP_Entry,
            "PEP_Exit": PEP_Exit,
            "KO_PnL": KO_PnL,
            "PEP_PnL": PEP_PnL,
            "Total_PnL": Total_PnL
        }
        trade_list.append(trade)
        trade_status = False
        direction = None
        Entry_Date = None
        Exit_Date = None
        KO_Entry = None
        KO_Exit = None
        PEP_Entry = None
        PEP_Exit = None
        KO_PnL = None
        PEP_PnL = None
        Total_PnL = None
trade_table = pd.DataFrame(trade_list)
print(trade_table)
