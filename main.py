import pandas as pd
from Pairs_Finder import pairs_finder
from spread_diff import spread_diff
# load data
data = pd.read_csv("data/30_Utility_Stock.csv", index_col=0)

# find best pair
stock_a, stock_b = pairs_finder(data)
print(f"Best pair found: {stock_a} and {stock_b}")

# run trading strategy
spread_diff(stock_a, stock_b)
