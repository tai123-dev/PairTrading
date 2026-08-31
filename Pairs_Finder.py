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


def pairs_finder(data, beta_dict, ssd_band=40, euclidean_std=1):
    stock_info = pd.read_csv("data/stock_info.csv",
                             index_col=0)["0"]
    same_company = set()
    for ticker1, ticker2 in combinations(data.columns.tolist(), 2):
        if stock_info[ticker1] == stock_info[ticker2]:
            same_company.add((ticker1, ticker2))
    normalized = data / data.iloc[0]
    # print(normalized)

    # Convert to a NumPy matrix (days x stocks)
    matrix = normalized.values  # (num_days, num_stocks)
    sq = (matrix**2).sum(axis=0)
    gram = np.dot(matrix.T, matrix)
    ssd_matrix = sq.reshape(-1, 1) + sq.reshape(1, -1) - 2 *gram
    tickers = normalized.columns.tolist()
    num_stocks = len(tickers)
    print(f"num_stocks: {num_stocks}")
    # Compute all pairwise distances at once
    results = []
    for i in range(num_stocks):
        for j in range(i+1, num_stocks):
            if (tickers[i], tickers[j]) in same_company:
                continue
            diff = matrix[:, i] - matrix[:, j]
            distance = np.dot(diff, diff)
            results.append((tickers[i], tickers[j], distance))
    ssd_list = []
    for i in range(len(results)):
        x, y, z = results[i]
        ssd_list.append(z)

    lower_bound = np.percentile(ssd_list, ssd_band)
    upper_bound = np.percentile(ssd_list, 100 - ssd_band)
    qualify_over_bound = []
    print(f"Pairs passing SSD band filter: {len(qualify_over_bound)}")
    print(f"lower: {lower_bound}, upper: {upper_bound}")
    print(f"Sample SSDs: {ssd_list[:5]}")

    for a, b, c in results:
        if c > lower_bound and c < upper_bound:
            qualify_over_bound.append((a, b, c))

    print(f"Pairs passing SSD band filter: {len(qualify_over_bound)}")

    # Sort and return top n pairs

    top_pairs_by_euclidean = {}
    for ticker1, ticker2, _ in qualify_over_bound:
        euclidean_distance = euclidean(ticker1, ticker2, beta_dict)
        top_pairs_by_euclidean[(ticker1, ticker2)] = euclidean_distance

    mean = np.array(list(top_pairs_by_euclidean.values())).mean()
    std = np.array(list(top_pairs_by_euclidean.values())).std()
    threshold = mean - euclidean_std * std
    qualify_pairs = {}
    for ticker in top_pairs_by_euclidean:
        distance = top_pairs_by_euclidean.get(ticker)
        if distance < threshold:
            qualify_pairs[ticker] = distance

    print(f"Top {len(qualify_pairs)} pairs found:")
    for i, (a, b) in enumerate(qualify_pairs.keys(), 1):
        print(f"  {i}. {a} / {b}")

    return list(qualify_pairs.keys())
