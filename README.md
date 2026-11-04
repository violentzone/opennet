# Generate Valid Slot Reel Configuration

## Generate any valid Slot Game reel configuration that meets the following requirements

### Rules

1. The RTP (Return to Player) must be 0.95.  
   (Assume a total bet amount of 100 units; the expected return for the user per 100 units bet should be 95 units.)
2. The user’s win rate must not be lower than 55%.
3. The slot game display consists of 3 columns × 3 rows.
4. There are five winning patterns, as shown below (the blocks (■) must all be the same symbol to trigger a win):

  
```
4.1 Uper left 2×2     4.2 Upper right 2×2     4.3 buttom left 2×2     4.4 buttom right 2×2     4.5 full 3×3
■ ■ .                     . ■ ■                       . . .                 . . .                  ■ ■ ■
■ ■ .                     . ■ ■                       ■ ■ .                 . ■ ■                  ■ ■ ■
. . .                     . . .                       ■ ■ .                 . ■ ■                  ■ ■ ■


```
   #### Winning Patterns ####
     
5. For the first four patterns, the payout is: **bet amount × symbol multiplier**.  
   For the fifth pattern, the payout is: **bet amount × symbol multiplier × 5**.
6. There are **5 types of symbols**. Their keys and multipliers are as follows:  
   `{0: 0.25, 1: 0.55, 2: 1, 3: 3, 4: 5}`
7. The reels do **not** need to be of equal length, nor is there any limit on their lengths.  
   You can imagine them as being placed on large, possibly uneven, rotating drums.

### Assumptions

- Three reels stop event is independent
- Reels stops randomly
- Reels are head-tail connected ban structure, with length of L1, L2 and L3
- When getting full 3x3, odds will NOT contain other 2x2
- RTP 0.95, multiplier {0: 0.25, 1: 0.55, 2: 1, 3: 3, 4: 5}, and win rate > 0.55 will encounter "floating point precision error" → Convert them into integers(20x)
   - N(all situations) = L1 x L2 x L3
   - RTP = 0.95 → pay 20 for a spin, expect to get 19 back → pay_sum = 19 x N (all situations)
- There shall be at least of one 3 x3 combination of each symbol, and count of symbol 2 > count of symbol 3 > count of symbol 4 → reels start building from [0] x 6 + [1] x 6 + [2] x 5 + [3] x 4 + [4] x 3

### Solution
1. Build method that calculates reward amount from display panel [payout_calc.py](calculations.py)
2. Build method that generate all three symbol on display panel of simgle reel [get_all_reel_display](calculations.py)
3. After first calculation(reels with init state [0] x 7 + [1] x 6 + [2] x 5 + [3] x 4 + [4] x 3):
    ```
    r1 = r2 = r3 = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4]
    pay_sum, N, win_rate = get_parameters_from_reels(r1, r2, r3)
    print('pay_sum: ', pay_sum, 'N: ', N, 'win_rate: ', win_rate, 'calculate: ', pay_sum / (N * 19))
    ```
    - N: 13824
    - pay_sum: 161504
    - pay_sum / (N x 19) = 0.6149
    - win_ratio: 34.8%
4. By testing, adding symbol 2 increase RTP too rapid, therefore the goal here is to add symbol 1 and symbol 0 to reels, strategy here is making reel 1 and reel 2 identical for simplicity, then search through reel 3 to get answer
5. 