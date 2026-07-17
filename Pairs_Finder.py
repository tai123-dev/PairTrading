import pandas as pd
import numpy as np
from itertools import combinations


def pairs_finder(data, n=20):
    normalized = data / data.iloc[0]
    # print(normalized)

    # Convert to a NumPy matrix (days x stocks)
    matrix = normalized.values  # (num_days, num_stocks)
    tickers = normalized.columns.tolist()
    num_stocks = len(tickers)
    # Compute all pairwise distances at once
    results = []
    for i in range(num_stocks):
        for j in range(i+1, num_stocks):
            diff = matrix[:, i] - matrix[:, j]
            distance = np.dot(diff, diff)
            results.append((tickers[i], tickers[j], distance))

    # Sort and return top n pairs
    results.sort(key=lambda x: x[2])
    top_pairs = [(a, b, d) for a, b, d in results[:n]]

    print(f"Top {n} pairs found:")
    for i, (a, b, d) in enumerate(top_pairs, 1):
        print(f"  {i}. {a} / {b}")

    return top_pairs
