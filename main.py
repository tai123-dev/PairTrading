import pandas as pd
from Pairs_Finder import pairs_finder
from spread_diff import spread_diff
# load data
data = pd.read_csv("data/Tech_Stock.csv",
                   index_col=0, parse_dates=True)
# find best pair
top_5 = pairs_finder(data, n=5)
top_20 = pairs_finder(data, n=20)
print(f"Best top 5 pairs and top 20 pairs found: {top_5} and {top_20}")

# run trading strategy
spread_diff(top_5[0][0], top_5[0][1])
