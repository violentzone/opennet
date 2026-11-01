"""步驟 3：怎麼算 RTP 與中獎率？——完整列舉每一種結果。

RTP   = 所有結果的賠付加總 / (N x 下注)
中獎率 = 賠付 > 0 的結果數 / N

用一組很短的滾輪（N = 3 x 4 x 4 = 48），把 48 種結果全部印出來，
可以用手算驗證加總。
"""
from itertools import product

from slot_core import (MIN_HIT_PCT, TARGET_PAY, evaluate, hit_rate, is_valid,
                       payout_points, rtp, windows)

r1 = (0, 0, 1)
r2 = (0, 0, 1, 1)
r3 = (0, 1, 1, 2)
print(f"reel1 = {list(r1)}, reel2 = {list(r2)}, reel3 = {list(r3)}")
print()
print("p1 p2 p3 | 欄1        欄2        欄3        | 點數")
for (p1, c1), (p2, c2), (p3, c3) in product(enumerate(windows(r1)),
                                            enumerate(windows(r2)),
                                            enumerate(windows(r3))):
    pts = payout_points((c1, c2, c3))
    mark = "  <- 中獎" if pts else ""
    print(f"{p1}  {p2}  {p3} | {c1} {c2} {c3} | {pts:3d}{mark}")

pay_sum, hits, n = evaluate(r1, r2, r3)
print()
print(f"N        = {len(r1)} x {len(r2)} x {len(r3)} = {n}")
print(f"pay_sum  = {pay_sum} 點      （把上面的點數欄全部加起來）")
print(f"hits     = {hits}            （點數 > 0 的列數）")
print()
print("RTP = pay_sum / (20 x N)      因為 20 點 = 1 倍")
print(f"    = {pay_sum} / (20 x {n}) = {rtp(pay_sum, n)} = {float(rtp(pay_sum, n)):.4f}")
print(f"中獎率 = hits / N = {hits} / {n} = {hit_rate(hits, n)} = {float(hit_rate(hits, n)):.4f}")
print()
print("---- 把兩個條件改寫成整數比較 ----")
print(f"RTP == 19/20   <=>  pay_sum == {TARGET_PAY} x N = {TARGET_PAY * n}      目前 pay_sum = {pay_sum}")
print(f"中獎率 >= 55%   <=>  100 x hits >= {MIN_HIT_PCT} x N  即 {100 * hits} >= {MIN_HIT_PCT * n}")
print(f"合法？ {is_valid(pay_sum, hits, n)}")
print()
print("目前 pay_sum 和 19N 差多少？這個「差距」就是後面要調到 0 的目標。")
print(f"差距 = pay_sum - 19N = {pay_sum - TARGET_PAY * n} 點")
