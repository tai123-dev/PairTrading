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


def pairs_finder(data, stock_info, beta_dict, ssd_band=40, euclidean_std=1):

    same_company = set()
    for ticker1, ticker2 in combinations(data.columns.tolist(), 2):
        if stock_info[ticker1] == stock_info[ticker2]:
            same_company.add((ticker1, ticker2))
    normalized = data / data.iloc[0]
    tickers = normalized.columns.tolist()

    matrix = normalized.values
    difference = matrix[:, :, None] - matrix[:, None, :]
    sq = (difference**2).sum(axis=0)

    pairs_extract = np.triu_indices(sq.shape[1], k=1)

    stock_diff = sq[pairs_extract[0], pairs_extract[1]]

    lower_bound = np.percentile(stock_diff, ssd_band)
    upper_bound = np.percentile(stock_diff, 100 - ssd_band)
    qualify_over_bound = []
    print(f"Pairs passing SSD band filter: {len(qualify_over_bound)}")
    print(f"lower: {lower_bound}, upper: {upper_bound}")
    print(f"Sample SSDs: {stock_diff[:5]}")

    for k, distance in enumerate(stock_diff):
        if (tickers[pairs_extract[0][k]], tickers[pairs_extract[1][k]]) in same_company:
            continue
        if distance > lower_bound and distance < upper_bound:
            qualify_over_bound.append(((tickers[pairs_extract[0][k]],
                                        tickers[pairs_extract[1][k]]), distance))

    print(f"Pairs passing SSD band filter: {len(qualify_over_bound)}")

    # Sort and return top n pairs

    top_pairs_by_euclidean = {}
    for (ticker1, ticker2), distance in qualify_over_bound:
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
