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

## Solution

### Assumptions

- Three reels stop event is independent
- Reels stops randomly
- Reels are head-tail connected ban structure, with length of L1, L2 and L3
- When getting full 3x3, odds will NOT contain other 2x2
- RTP 0.95, multiplier {0: 0.25, 1: 0.55, 2: 1, 3: 3, 4: 5}, and win rate > 0.55 will encounter "floating point precision error" → Convert them into integers(20x)
   - N(all situations) = L1 x L2 x L3
   - RTP = 0.95 → pay 20 for a spin, expect to get 19 back → pay_sum = 19 x N (all situations)
   - Win rate: hits/N > 55/100 → 100 x hits > 55 x N
- There shall be at least of one 3 x3 combination of each symbol → reels start building from [0] x 3 + [1] x3 + [2] x 3 + [3] x 3 + [4] x 3
- In order to get RTP of 0.95, adding symbol 0 and symbol 1 (multiply < 1) to get RTP to 0.95 and win rate 0.55.
- To simplify calculate, 

### Build method that calculates payout of display area by distinct column
[payout_calc.py](payout_calc.py)

### Build method iterate through possibilities
1. Strategy:
    - Simbol 0 & 1 build fundamental reel, other symbol exceeds RTA 0.95
    - Fix reel 1 and reel 2, then calculate reel 3 
    - 