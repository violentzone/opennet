from payout_calc import payout_calc
from get_solusion import get_all_reel_display

# Test three identical reels of [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4] payout
reel1 = reel2 = reel3 = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]

n = len(reel1) * len(reel2) * len(reel3)
payout = payout_calc(reel1, reel2, reel3)
print(payout)