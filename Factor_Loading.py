from fredapi import Fred
import yfinance as yf
import numpy
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")
fred = Fred(api_key)


def compute_factor_loadings(tickers, start, end):
    oil_ticker = ["DCOILWTICO"]
    spy_ticker = ["SPY"]
    spy_data = yf.download(spy_ticker, start, end)["Close"]
    spy_data = spy_data["SPY"].pct_change().dropna()
    oil_data = fred.get_series("DCOILWTICO", start, end)
    oil_data = oil_data.pct_change().dropna()
    print(oil_data.head(5))
    data = yf.download(tickers, start,
                       end)["Close"]
    data = data.pct_change().dropna()

    beta_dict = {}
    for ticker in tickers:
        stock_return = data[ticker]
        aligned_dict = {"Market": spy_data,
                        "Oil": oil_data, "Stock": stock_return}
        df = pd.DataFrame(aligned_dict).dropna()
        data_pack = [numpy.ones(len(df["Market"])), df["Market"], df["Oil"]]
        x = numpy.column_stack(data_pack)
        beta = numpy.linalg.lstsq(x, df["Stock"], rcond=None)
        beta_dict[ticker] = [beta[0][1], beta[0][2]]
        print(beta_dict)
    return beta_dict


if __name__ == "__main__":
    compute_factor_loadings(["AAPL"], start="2024-01-01", end="2024-06-01")
