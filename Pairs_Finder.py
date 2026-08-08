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


def pairs_finder(data, beta_dict, n=20, n_std=1):
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
    top_pairs_by_euclidean = {}
    for ticker1, ticker2, _ in top_pairs:
        euclidean_distance = euclidean(ticker1, ticker2, beta_dict)
        top_pairs_by_euclidean[(ticker1, ticker2)] = euclidean_distance

    mean = np.array(list(top_pairs_by_euclidean.values())).mean()
    std = np.array(list(top_pairs_by_euclidean.values())).std()
    threshold = mean - n_std * std
    qualify_pairs = {}
    for ticker in top_pairs_by_euclidean:
        distance = top_pairs_by_euclidean.get(ticker)
        if distance < threshold:
            qualify_pairs[ticker] = distance

    print(f"Top {len(qualify_pairs)} pairs found:")
    for i, (a, b) in enumerate(qualify_pairs.keys(), 1):
        print(f"  {i}. {a} / {b}")

    return list(qualify_pairs.keys())
