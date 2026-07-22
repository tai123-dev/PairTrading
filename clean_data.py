import pandas as pd
import yfinance as yf


def clean_data():

    wikipedia_read = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", storage_options={"User-Agent": "Mozilla/5.0"})

    s_and_p_500 = wikipedia_read[0]

    s_and_p_500_name = s_and_p_500["Symbol"].tolist()
    data = yf.download(s_and_p_500_name, start="2024-01-01",
                       end="2025-01-01")["Close"]
    day_of_trade = len(data)
    missing_day = data.isnull().sum()
    data = data.loc[:, missing_day <= day_of_trade*10/100]
    data = data.ffill()
    data.to_csv("data/clean_data.csv")


if __name__ == "__main__":
    clean_data()
