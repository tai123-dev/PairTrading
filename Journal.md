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