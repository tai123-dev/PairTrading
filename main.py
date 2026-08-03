import pandas as pd
from Pairs_Finder import pairs_finder
from spread_diff import spread_diff
from Factor_Loading import compute_factor_loadings
# load data
data = pd.read_csv("data/clean_data.csv",
                   index_col=0, parse_dates=True)
factor_loading = compute_factor_loadings(
    data.columns.tolist(), start="2024-01-01", end="2024-06-01")
# find best pair
top_5 = pairs_finder(data, factor_loading, n=5)
top_20 = pairs_finder(data, factor_loading, n=20)
print(f"Best top 5 pairs and top 20 pairs found: {top_5} and {top_20}")

# run trading strategy
for i in range(len(top_20)):
    spread_diff(top_5[i][0], top_5[i][1])
