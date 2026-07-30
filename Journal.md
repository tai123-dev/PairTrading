## Purpose for this Journal is for Tai to learn and understand everything in this project
## This Journal is a little bit late since Tai is too stupid to realize that he needs a Journal

- Jul 21:
    - Do:
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

    - Learn:
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
    - Do: 
    + Fix the compute_factor_loadings, downloaded Oil from FRED as "DCOILWTICO" 
    + Create a dictionary to store the market return, oil return and stock return because each factor has different date of data, and the reason for dictionary is to turn the dictionary into DataFrame using pd.DataFrame()
    + Then create data_pack where it store alpha, market and oil into a list, numpy.ones(len of the market (follow market dates))
    + Use column stack to put it as column, three columns (alpha, market, oil)
    + Then use numpy.linalg.lstsq to handle two inputs, one outputs only
    + The beta_dict will have the ticker as key, and each key will have two betas, market and oil as value
    - Question raise: What is the use of betas, the market and oil beta
    + Similar betas -> systematic shocks cancel out in the spread -> what is left in the spread is mostly ε (noise term) -> ε mean reverts -> so the spread mean reverts -> tradeable signal