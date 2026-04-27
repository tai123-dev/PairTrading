import pandas as pd
import numpy as np
from itertools import combinations


def pairs_finder(data):
    normalized = data / data.iloc[0]
    # print(normalized)
    results = []
    for stock_a, stock_b in combinations(normalized.columns, 2):
        diff = normalized[stock_a] - normalized[stock_b]
        distance = np.sum(diff ** 2)
        results.append((stock_a, stock_b, distance))
    results.sort(key=lambda x: x[2])
    results_df = pd.DataFrame(
        results, columns=["Stock_A", "Stock_B", "Distance"])
    results_df = results_df.sort_values("Distance")
    best_pair = results_df.iloc[0]
    print(best_pair)
    return best_pair["Stock_A"], best_pair["Stock_B"]
