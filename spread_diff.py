import pandas as pd
import matplotlib.pyplot as plt
csv_path = ("data/KO_PEP_aligned.csv")
table = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")
table["Spread_Diff"] = table["KO"]-table["PEP"]
table.to_csv("data/KO_PEP_spread.csv", index=False)
average = table["Spread_Diff"].rolling(window=30).mean()
deviation = table["Spread_Diff"].rolling(window=30).std()
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
        if -0.25 <= i <= 0.25:
            signal.append("Exit")
            position = "Flat"
        else:
            signal.append("")
    elif position == "Longspread":
        if -0.25 <= i <= 0.25:
            signal.append("Exit")
            position = "Flat"
        else:
            signal.append("")

table["Signal"] = signal
trade_log = table[(table["Signal"].notna()) & (table["Signal"] != "")]
table.to_csv("data/KO_PEP_spread_signal.csv", index=True)
trade_log.to_csv("data/KO_PEP_trades.csv", index=True)


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
Total_PnL_Each_Trade = None
Total_Trade_PnL = 0
win_Trade = 0
best_Trade = None
worst_Trade = None
best_Trade_PnL = None
worst_Trade_PnL = None
for date, row in trade_log.iterrows():
    signal_today = row["Signal"]
    ko_today = row["KO"]
    pep_today = row["PEP"]
    if (trade_status == False and signal_today == "ENTER: Long KO / Short PEP"):
        Entry_Date = date
        KO_Entry = ko_today
        PEP_Entry = pep_today
        # print("Trade Open 1")
        trade_status = True
        direction = "Long KO / Short PEP"
    elif (trade_status == False and signal_today == "ENTER: Short KO / Long PEP"):
        Entry_Date = date
        KO_Entry = ko_today
        PEP_Entry = pep_today
        # print("Trade Open 2")
        trade_status = True
        direction = "Short KO / Long PEP"
    elif (trade_status == True and signal_today == "Exit"):
        Exit_Date = date
        KO_Exit = ko_today
        PEP_Exit = pep_today
        # print("Trade Close")
        trade_status = False
        if (direction == "Long KO / Short PEP"):
            KO_PnL = (KO_Exit - KO_Entry) / KO_Entry
            PEP_PnL = (PEP_Entry - PEP_Exit) / PEP_Entry
            Total_PnL_Each_Trade = KO_PnL + PEP_PnL - 0.004
        else:
            KO_PnL = (KO_Entry - KO_Exit) / KO_Entry
            PEP_PnL = (PEP_Exit - PEP_Entry) / PEP_Entry
            Total_PnL_Each_Trade = KO_PnL + PEP_PnL - 0.004
        if (best_Trade_PnL == None or Total_PnL_Each_Trade >= best_Trade_PnL):
            best_Trade_PnL = Total_PnL_Each_Trade
            best_Trade = Exit_Date
        if (worst_Trade_PnL == None or Total_PnL_Each_Trade < worst_Trade_PnL):
            worst_Trade_PnL = Total_PnL_Each_Trade
            worst_Trade = Exit_Date
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
            "Total_PnL_Each_Trade": Total_PnL_Each_Trade
        }
        if (Total_PnL_Each_Trade > 0):
            win_Trade += 1
        Total_Trade_PnL += Total_PnL_Each_Trade
        trade_list.append(trade)
        direction = None
        Entry_Date = None
        Exit_Date = None
        KO_Entry = None
        KO_Exit = None
        PEP_Entry = None
        PEP_Exit = None
        KO_PnL = None
        PEP_PnL = None
        Total_PnL_Each_Trade = None
trade_table = pd.DataFrame(trade_list)
if not trade_table.empty:
    trade_table["Cumulative_PnL"] = trade_table["Total_PnL_Each_Trade"].cumsum()
total_trade = len(trade_table)
if (total_trade > 0):
    average_PnL = Total_Trade_PnL/total_trade
    win_rate = (win_Trade/total_trade)
    # Choosing T-bills because this model do a shor period of time, compare with T-bills make more sense
    risk_free_rate = 0.04/252
    trade_table["Excess_return"] = trade_table["Total_PnL_Each_Trade"] - risk_free_rate
    sharpe_ratio = (
        trade_table["Excess_return"].mean() / trade_table["Excess_return"].std()) * (252**0.5)
    peak = trade_table["Cumulative_PnL"].cummax()
    drawdown = trade_table["Cumulative_PnL"] - peak
    max_drawdown = drawdown.min()
    print(f"Win Rate: {win_rate * 100:.2f}%")
    print(f"Average PnL: {average_PnL*100:.2f}%")
    print(f"Total Trade PnL: {Total_Trade_PnL*100:.2f}%")
    print(trade_table.groupby(trade_table["Entry_Date"].dt.year)[
          "Total_PnL_Each_Trade"].sum())
else:
    print("No completed Trades")

plt.figure(figsize=(8, 5))
plt.hist(trade_table["Total_PnL_Each_Trade"])
plt.title("Distribution of Trade PnL")
plt.xlabel("Trade PnL")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
plt.figure(figsize=(12, 6))
plt.plot(trade_table["Exit_Date"],
         trade_table["Cumulative_PnL"], color="blue", linewidth=2)
plt.axhline(y=0, color="red", linestyle="--", linewidth=1)
plt.title("Equity Curve - KO/PEP Pairs Trading Strategy")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.tight_layout()
plt.show()
print(f"Worst trade date: {worst_Trade}")
print(f"Wosrt trade PnL:{worst_Trade_PnL}")
print(f"Best trade date:{best_Trade}")
print(f"Best trade PnL:{best_Trade_PnL}")
print(f"Sharpe ratio: {sharpe_ratio}")
print(f"Max Drawdown: {max_drawdown * 100:.2f}%")
print(trade_table[["Entry_Date", "Exit_Date", "Direction",
      "Total_PnL_Each_Trade", "Cumulative_PnL", "Excess_return"]])
