## Purpose for this Journal is for Tai to learn and understand everything in this project
## This Journal is a little bit late since Tai is too stupid to realize that he needs a Journal

- Jul 21:
    - Did:
    + Create clean_data.py where pull S&P 500 stock from Wikipedia, download 2024 data then clean it
    + Clean data here mean just take the name of the stocks from Wikipedia, then drop all the stocks that
    missing more than 10% of data, 10% because we still need data to have pairs to do some trades, no more 
    than 10% because there will some noise pairs which can fuck up the process
    + Add a half_life function where it calculate how fast the stock gonna go back to normal, this function using
    y as daily change, x as the spread, then do a process call linear regression (finding the slope that best fits X vs Y) where it returns a slope which can 
    use for the half-life formula, ln(2)/thete where theta is absolute value of the slope
    + Add entry threshold function to determine the enter for trading, the formula we are using right now is 
    constant * ln(half_life), the reason for using ln(half_life) is because natural log will grow slow with larger input.
    We are still doing test on the formula (to be continue)
    + Add a exit rule, exit a trade after the day_counter (a count for how many days did we enter this trade) is 
    bigger than half-life/2 or z-score is nearly equal to zero

    - Learned:
    + Statistic: - More trades means less luck, trying constant on the whole data file including 2024-2025 will give you luck
                    not your strategy
                 - So split the data in half, 2024 for building strategy, 2025 for testing that strategy
                 - Overfitting - finding a constant that works on history does not mean it works on future data
    + Math:      - Ornstein-Uhlenbeck process: how spread mean-revert with a pulling force
                 - Theta: the speed of mean reversion, estimated frrom the slope of a linear regression
                 - Half-life formula:  ln(2)/theta
    + Strategy:  - Fixed threshold fail because there are fast and slow pairs, we have to calculate different enter and exit threshold
    design       - Entry threshold logic is that slow pairs need higher z-score threshold, opposite with fast pairs, need lower threshold
                 - Exit logic is that z-score returning to nearly zero or stop if hit deadline
                 - ONE CONSTANT DOES NOT WORK ACROSS ALL PAIRS, NEXT THING TOMORROW

- Jul 25: 
    - Do:
    + Rebuilt entry_threshold() from 0.5 * ln(half_life) to 2.0 * sqrt(ln(half_life)) since the first version cannot make the output small enough
    + Fixed spread_diff.py - moved sharper ratio, max_drawdown, trade printes all insde if total_trades > 0 block
    + Fixed else block to return (0,0,0,0,0) matching the 5-value return signature
    + Add print(table["Z"].abs().max()) and print(["Z"].std()) to diagnose PNC/RF
    - Learn:
    + Working backwards from a desired threshold of 2.0 proved the formula c * ln(half_life) collapses — ln cancels and you just get the constant back. The formula was adding fake complexity.
    + 2.0 is the literature baseline for pairs trading entry — don't invent numbers, borrow from validated research
    + Slow pairs need higher thresholds because longer exposure = more things can go wrong = you need bigger initial edge
    + sqrt controls growth so thresholds don't explode for very slow pairs
    + SSD finds pairs that co-move perfectly — but perfect co-movement means external shocks hit both stocks equally, spread stays flat, no trades generated
    + 2025 was volatile but PNC/RF spread barely moved (max Z = 2.83, std = 1.345) — the problem is the pairs, not the year
    + Fundamental tension: more correlated = tighter spread = fewer trades

## Next problem will be what information beyound price history tells you two stocks have a reason to sometimes diverge?

-  Jul 27:
    - Identify, SSD (Square Sum Different) finds pairs by price history but is blind to whether the relationships is structural. We add factor loading to improve pairs selection. We use a fundamental factors model where we choose the factors ourselves, because it's interpretable (can be explain) and defensible. PCA finds factors automatically but produces uninterpretable components

    - Decision made:
        + Two-stage filtering pipeline for pair selection — SSD first as coarse filter, factor loading distance second as fine filter.

## Open question for next session: 500 stocks means 500 regressions to compute factor loadings. Should you run them one by one or is there a smarter way?

- Jul 27:
    - We choose to trade on noise term (ε) because the factor on market and loading all affect on others systematic factors have persistent trends, but the noise term is random, spikes up and down, but it has no persistent trend, it revert back to zero
    - The sharpe ratio that we are calculating is using 3-month Treasury bill
    - Do:
    + Created a function called compute_factor_loading, where it download S&P500 (SPY) from yfiance, download the start day is 2024-06-01 and end day is 2024-12-01
    + Download all the stock with the same date as SPY, then convert price series into percentage return using pct_change(), then use dropna() to drop the row with NaN so that scipy.linregress() does not raise an error. All price must be CLOSE. Then return the function with a dictionary where it will contain the ticker and it beta value

- Jul 29:
    - Did: 
    + Fix the compute_factor_loadings, downloaded Oil from FRED as "DCOILWTICO" 
    + Create a dictionary to store the market return, oil return and stock return because each factor has different date of data, and the reason for dictionary is to turn the dictionary into DataFrame using pd.DataFrame()
    + Then create data_pack where it store alpha, market and oil into a list, numpy.ones(len of the market (follow market dates))
    + Use column stack to put it as column, three columns (alpha, market, oil)
    + Then use numpy.linalg.lstsq to handle two inputs, one outputs only
    + The beta_dict will have the ticker as key, and each key will have two betas, market and oil as value
    - Question raise: What is the use of betas, the market and oil beta
    + Similar betas -> systematic shocks cancel out in the spread -> what is left in the spread is mostly ε (noise term) -> ε mean reverts -> so the spread mean reverts -> tradeable signal

- Aug 2:
    - Did: 
    + Move the compute_factor_loading to a new file where every file can access it without running into circular import.
    + Write a function that calculate the distance call euclidean that compute the distance of a pair using the two betas of each ticker, oil and market
    + Problem with oil and  yfinace is that yfinace does not have a ticker call "DCOILWTICO", so I have to get API keys from FRED, download freadpi and downloaded the oil data
    + The main problem we are having right now is that the threshold for the distance is not making any sense right now since we only set it bceause the smaller the distance, the better the pair, so the thinking we should do right now is that how to come up with a threshold that make sense with all the pairs, that can give use tradeable signal
    + I thought of using the average for the distance but it did not make sense it will eliminate half of the data, the average is about at the middle of data
    
- Aug 8:
    - Did:
    + Ran into a problem that max_distance is not working, does not adapt to the actual distribution of pairswise Euclidean distance
    + Came up with a solution that to make a 2 pass, first pass will compute all Euclidean distance for top 20 pairs that pass the first filter(SDD), then store it in dictionary
    + Then compute mean and std of those distance, set "threshold = mean - n_std * std", filter pairs below threshold
    + Another problem came up, it is that there are none trade execute across all pairs, z-scores never reach entry threshold
    + The root of the problem is that they are too similar, from the same company share classes or near-identical utilities. So spread barely move
    + So I has to came up with a solution is that put another filter, so there are three filter, this filter will block pairs from the same company using ticker.info['website'] from yfinance
    + Implement this itno clean_data.py  as a loop saving stock_info.csv

- Aug 14:
    - Did: 
    + SSD band filter redesign. Replaced the top-N smallest SSd approach with a percentile band [ssd_band , 100 - sdd_band]. The reason for this is because mean plus minus std was broken because the SSD distribution is heavily righ skewed - a few extreme outlier pairs were dragging the mean and std so high that the boundaries were meaningless. Percentile bands are robuse to outliers beacuse they only care about rank, not magnitufe. ssd_nband = 40 gives the middle 20% pairs.
    + Hedge ratio added: Replaced the raw price difference spread (stock_a - stock_b) with a beta adjusted spread (stock_a - beta * stock_b). Beta is etimated using scipy.stats.linregress on 2024 in-sample prices, then applied to 2025 out-of-sample prices. This is to make sure that we notice that the stock is move up and down together or just one stock move and the other does not. This ensures systematic co-movement cancels out of the spread, leaving only idiosyncratic noise to trade.
    + Half-life threshold where only choose pairs with half-life below 25 days, since more than 25 days can carry unnotice risk and too long to hold for a trading window.
    + Need to be finish. ADF test, Half-life ranking for concentration control, same-company filter, matrix optimization

- Aug 21:
    - Did:
    + Realized that the pairs generates 0 or 1 trades per pair. Because the standard deviation is to high which base on the normal distribution, it just take about 0.7% in one tail, which give close to 1 day, that mean that the Z-score exceed that standard deviation is very rare, like 1 days in a 102 days window of trading
    + The entry threshold is not trigger 

- Aug 24:
    - Did:
    + Delete the entry_threshold function because it does not make any sense and I don't rememeber derive it, instead of that function, we will use the paper threshold 2.0
- Aug 25:
    - Did: 
    + Added the same_company filter where it will eliminate the pair that come from the same company like FOX and FOXA. 
    + The mechanism behind this filter is that from clean_data.py, it will cleaning data and loop through every single one of the stock and find the website of that stock, it will not download and clean dstock that does not have date. Then save it into stock_info.csv
    + Pairs_Finder will loop through the stock_info.csv file and and create possible pair, if the two stocks are the same, it will add to same_company set, then if the pair show up in the normalized price, it will skip that pair
    + 

- Aug 31:
    - Did:
    + Implement concentration control, receive half-life calculation from spread_diff.py and ranking them