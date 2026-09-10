import pandas as pd
from Pairs_Finder import pairs_finder
from spread_diff import spread_diff
from Factor_Loading import compute_factor_loadings
# load data
data = pd.read_csv("data/clean_data.csv",
                   index_col=0, parse_dates=True)
factor_loading = compute_factor_loadings(data,
                                         data.columns.tolist(), start="2024-01-01", end="2024-06-01")

stock_info = pd.read_csv("data/stock_info.csv", index_col=0)["0"]
# find best pair
top_5 = pairs_finder(data, stock_info, factor_loading,
                     ssd_band=40, euclidean_std=1)
print(f"Best top 5 pairs and top 20 pairs found: {top_5}")

half_life_ranking = {}
full_result = {}

# run trading strategy
for i in range(len(top_5)):
    result = spread_diff(top_5[i][0], top_5[i][1], data)
    if result is not None:
        half_life_ranking[(top_5[i][0], top_5[i][1])] = result[5]
        full_result[(top_5[i][0], top_5[i][1])] = (result)

sorted_pairs = dict(sorted(half_life_ranking.items(), key=lambda x: x[1]))

stock_assign = set()
best_pair = {}
for key, value in sorted_pairs.items():
    if key[0] not in stock_assign and key[1] not in stock_assign:
        stock_assign.add(key[0])
        stock_assign.add(key[1])
        best_pair[(key[0], key[1])] = value

for key, value in best_pair.items():
    print(f"Best Pair: {key[0], key[1]} - Half-life value: {value}")
