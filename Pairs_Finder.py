import pandas as pd
import numpy as np
from itertools import combinations
import math


def euclidean(ticker1, ticker2, beta_dict):
    beta_market_1 = beta_dict[ticker1][0]
    beta_market_2 = beta_dict[ticker2][0]
    beta_oil_1 = beta_dict[ticker1][1]
    beta_oil_2 = beta_dict[ticker2][1]
    euclidean_distance = math.sqrt(
        (beta_market_1 - beta_market_2)**2 + (beta_oil_1 - beta_oil_2)**2)
    return euclidean_distance


def pairs_finder(data, beta_dict, max_distance=0.15, n=20):
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
    top_pairs_by_euclidean = []
    for ticker1, ticker2, _ in top_pairs:
        euclidean_distance = euclidean(ticker1, ticker2, beta_dict)
        if euclidean_distance <= max_distance:
            top_pairs_by_euclidean.append(
                (ticker1, ticker2, euclidean_distance))

    print(f"Top {n} pairs found:")
    for i, (a, b, d) in enumerate(top_pairs_by_euclidean, 1):
        print(f"  {i}. {a} / {b}")

    return top_pairs_by_euclidean
