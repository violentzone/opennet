"""步驟 6：驗證你的最終配置。

兩層驗證：
  1. 精確列舉：pay_sum == 19N、100*hits >= 55N（整數等式，零誤差）。
  2. 蒙地卡羅：隨機轉 20 萬次，結果應落在精確值附近（只用來交叉確認，不用來求解）。
另外印出每個符號、每種圖案的 RTP 貢獻，方便寫報告。
"""
import random
from collections import Counter
from fractions import Fraction
from itertools import product

from slot_core import (MULT, SCALE, evaluate, hit_rate, is_valid,
                       pattern_hits, payout_points, rtp, runs, windows)

# ======== 填入你在步驟 5 調好的配置 ============================================
reel1 = runs((0, 8), (1, 12))
reel2 = runs((0, 8), (1, 12))
reel3 = runs((0, 8), (1, 12))
# ===========================================================================

pay_sum, hits, n = evaluate(reel1, reel2, reel3)
print(f"reel1 (L={len(reel1)}): {list(reel1)}")
print(f"reel2 (L={len(reel2)}): {list(reel2)}")
print(f"reel3 (L={len(reel3)}): {list(reel3)}")
print()
print(f"N = {n}, pay_sum = {pay_sum}, 19N = {19 * n}, hits = {hits}")
print(f"RTP = {rtp(pay_sum, n)} = {float(rtp(pay_sum, n))}")
print(f"中獎率 = {hit_rate(hits, n)} = {float(hit_rate(hits, n)):.4f}")
print(f"合法？ {is_valid(pay_sum, hits, n)}")
print()

# ---- 貢獻表：每個符號、每種圖案貢獻多少 RTP -----------------------------------
contrib = Counter()
kinds = Counter()
for c1, c2, c3 in product(windows(reel1), windows(reel2), windows(reel3)):
    grid = (c1, c2, c3)
    pts = payout_points(grid)
    if not pts:
        continue
    hs = pattern_hits(grid)
    full = [s for name, s in hs if name == "全滿 3x3"]
    if full:
        contrib[(full[0], "3x3")] += pts
        kinds["3x3 全滿"] += 1
    else:
        for name, s in hs:
            contrib[(s, "2x2")] += MULT[s]
        kinds[f"{len(hs)} 個 2x2"] += 1
print("符號   2x2 貢獻   3x3 貢獻")
for s in MULT:
    two = Fraction(contrib[(s, "2x2")], SCALE * n)
    three = Fraction(contrib[(s, "3x3")], SCALE * n)
    print(f"  {s}     {float(two):.4f}     {float(three):.4f}")
print(f"合計 RTP = {Fraction(sum(contrib.values()), SCALE * n)}")
print()
print("中獎型態分布（佔全部轉動）")
for k, v in sorted(kinds.items()):
    print(f"  {k:<10} {float(Fraction(v, n)):.4f}")
print()

# ---- 蒙地卡羅 -----------------------------------------------------------------
rng = random.Random(0)
tables = [windows(reel1), windows(reel2), windows(reel3)]
spins = 200_000
mc_pay = mc_hit = 0
for _ in range(spins):
    p = payout_points(tuple(rng.choice(t) for t in tables))
    mc_pay += p
    mc_hit += p > 0
print(f"蒙地卡羅 {spins} 次：RTP ≈ {mc_pay / (SCALE * spins):.4f}，中獎率 ≈ {mc_hit / spins:.4f}")
print("模擬只會「接近」精確值，合法與否永遠以上面的整數等式為準。")
