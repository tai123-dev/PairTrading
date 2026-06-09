import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def spread_diff(stock_a, stock_b):
    # csv_path = ("data/KO_PEP_aligned.csv")
    data = yf.download([stock_a, stock_b], start="2025-01-01",
                       end="2025-06-01")["Close"]
    table = data
    table["Spread_Diff"] = table[stock_a]-table[stock_b]
    table.to_csv(f"PairsTrading/data/{stock_a}_{stock_b}_spread.csv")
    average = table["Spread_Diff"].rolling(window=30).mean()
    deviation = table["Spread_Diff"].rolling(window=30).std()
    table["Z"] = (table["Spread_Diff"] - average) / deviation
    signal = []
    position = "Flat"
    for i in table["Z"]:
        if position == "Flat":
            if i > 2:
                signal.append(f"ENTER: Short {stock_a} / Long {stock_b}")
                position = "Shortspread"
            elif i < -2:
                signal.append(f"ENTER: Long {stock_a} / Short {stock_b}")
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
    table.to_csv(
        f"PairsTrading/data/{stock_a}_{stock_b}_spread.csv", index=True)
    trade_log.to_csv(
        f"PairsTrading/data/{stock_a}_{stock_b}_trades.csv", index=True)

    # BackTesting
    trade_status = False
    direction = None
    trade_list = []
    Entry_Date = None
    Exit_Date = None
    stock_a_Entry = None
    stock_a_Exit = None
    stock_b_Entry = None
    stock_b_Exit = None
    stock_a_PnL = None
    stock_b_PnL = None
    Total_PnL_Each_Trade = None
    Total_Trade_PnL = 0
    win_Trade = 0
    best_Trade = None
    worst_Trade = None
    best_Trade_PnL = None
    worst_Trade_PnL = None
    for date, row in trade_log.iterrows():
        signal_today = row["Signal"]
        stock_a_today = row[stock_a]
        stock_b_today = row[stock_b]
        if (trade_status == False and signal_today == f"ENTER: Long {stock_a} / Short {stock_b}"):
            Entry_Date = date
            stock_a_Entry = stock_a_today
            stock_b_Entry = stock_b_today
            # print("Trade Open 1")
            trade_status = True
            direction = f"Long {stock_a} / Short {stock_b}"
        elif (trade_status == False and signal_today == f"ENTER: Short {stock_a} / Long {stock_b}"):
            Entry_Date = date
            stock_a_Entry = stock_a_today
            stock_b_Entry = stock_b_today
            # print("Trade Open 2")
            trade_status = True
            direction = f"Short {stock_a} / Long {stock_b}"
        elif (trade_status == True and signal_today == "Exit"):
            Exit_Date = date
            stock_a_Exit = stock_a_today
            stock_b_Exit = stock_b_today
            # print("Trade Close")
            trade_status = False
            if (direction == f"Long {stock_a} / Short {stock_b}"):
                stock_a_PnL = (stock_a_Exit - stock_a_Entry) / stock_a_Entry
                stock_b_PnL = (stock_b_Entry - stock_b_Exit) / stock_b_Entry
                Total_PnL_Each_Trade = stock_a_PnL + stock_b_PnL - 0.004 # Minus transaction cost
            else:
                stock_a_PnL = (stock_a_Entry - stock_a_Exit) / stock_a_Entry
                stock_b_PnL = (stock_b_Exit - stock_b_Entry) / stock_b_Entry
                Total_PnL_Each_Trade = stock_a_PnL + stock_b_PnL - 0.004
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
                f"{stock_a} Entry": stock_a_Entry,
                f"{stock_a} Exit": stock_a_Exit,
                f"{stock_b} Entry": stock_b_Entry,
                f"{stock_b} Exit": stock_b_Exit,
                f"{stock_a} PnL": stock_a_PnL,
                f"{stock_b} PnL": stock_b_PnL,
                "Total_PnL_Each_Trade": Total_PnL_Each_Trade
            }
            if (Total_PnL_Each_Trade > 0):
                win_Trade += 1
            Total_Trade_PnL += Total_PnL_Each_Trade
            trade_list.append(trade)
            direction = None
            Entry_Date = None
            Exit_Date = None
            stock_a_Entry = None
            stock_a_Exit = None
            stock_b_Entry = None
            stock_b_Exit = None
            stock_a_PnL = None
            stock_b_PnL = None
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
        # Sharpe ratio: How much extra return do I get for each unit of risk I take
        # Sharpe ratio can be calculate by take the return from the portifolio - risk-free return and
        # divide by the standard deviation of porfolio return
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
    plt.title(f"Equity Curve - {stock_a}/{stock_b} Pairs Trading Strategy")
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
    return win_rate, average_PnL, Total_Trade_PnL, sharpe_ratio, max_drawdown
