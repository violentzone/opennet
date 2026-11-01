"""步驟 5：手動調參工具。改頂端三條滾輪，看差距，再改。

這個檔案不會給你答案，它會告訴你：
  1. 目前 pay_sum 離 19N 差幾點、hits 離 55N 差多少。
  2. 固定前兩輪時，在第三輪「多加一格」會改變多少點。
有了 2，就可以用紙筆算出該加幾格什麼東西，讓差距剛好變 0。

方法：先用步驟 4 的直覺把前兩輪定下來（例如 0 與 1 各一段長段），
再只動第三輪。因為每個停點獨立計分，第三輪每一格的「貢獻」可以分開算。
"""
from itertools import product

from slot_core import (MIN_HIT_PCT, TARGET_PAY, describe, evaluate, hit_rate,
                       is_valid, payout_points, rtp, runs, windows)

# ======== 在這裡改你的配置 ===================================================
reel1 = runs((0, 8), (1, 12))
reel2 = runs((0, 8), (1, 12))
reel3 = runs((0, 8), (1, 12))
# ===========================================================================

pay_sum, hits, n = evaluate(reel1, reel2, reel3)
print(f"reel1 (L={len(reel1)}): {describe(reel1)}")
print(f"reel2 (L={len(reel2)}): {describe(reel2)}")
print(f"reel3 (L={len(reel3)}): {describe(reel3)}")
print()
print(f"N = {n}")
print(f"pay_sum  = {pay_sum:>8} 點   目標 19N = {TARGET_PAY * n:>8}   差距 = {pay_sum - TARGET_PAY * n:+d} 點")
print(f"100*hits = {100 * hits:>8}     目標 55N = {MIN_HIT_PCT * n:>8}   餘裕 = {100 * hits - MIN_HIT_PCT * n:+d}")
print(f"RTP = {rtp(pay_sum, n)} ≈ {float(rtp(pay_sum, n)):.4f},  中獎率 ≈ {float(hit_rate(hits, n)):.4f}")
print(f"合法？ {is_valid(pay_sum, hits, n)}")
print()

# ---- 固定前兩輪，第三輪每一種「視窗」的單格貢獻 ------------------------------
# 第三輪多一個停點，N 會多 L1*L2，所以目標 19N 也多 19*L1*L2。
# 一個視窗的「淨賠付分數」= 它對所有 (p1,p2) 的賠付總和 - 19*L1*L2。
# 第三輪所有停點的淨分數相加 == 0  就是 RTP 恰好 19/20。
base = len(reel1) * len(reel2)
print(f"---- 第三輪每種視窗的單格貢獻（前兩輪固定，L1*L2 = {base}）----")
print(f"第三輪每多一個停點：目標 19N 多 {TARGET_PAY * base} 點、55N 多 {MIN_HIT_PCT * base}")
print()
print(f"{'視窗型態':<12} {'(上,中,下)':<12} {'賠付總和':>8} {'淨賠付分數':>10} {'淨中獎分數':>10}")


def window_score(win):
    pay = hit = 0
    for c1, c2 in product(windows(reel1), windows(reel2)):
        p = payout_points((c1, c2, win))
        pay += p
        hit += p > 0
    return pay, pay - TARGET_PAY * base, 100 * hit - MIN_HIT_PCT * base


candidates = [
    ("三連 0", (0, 0, 0)), ("三連 1", (1, 1, 1)), ("三連 2", (2, 2, 2)),
    ("三連 3", (3, 3, 3)), ("三連 4", (4, 4, 4)),
    ("只有上對 0", (0, 0, 2)), ("只有下對 0", (2, 0, 0)),
    ("只有上對 1", (1, 1, 2)), ("只有下對 1", (2, 1, 1)),
    ("只有上對 4", (4, 4, 2)), ("只有下對 4", (2, 4, 4)),
    ("死格 (無配對)", (2, 3, 2)),
]
for name, win in candidates:
    pay, s_pay, s_hit = window_score(win)
    print(f"{name:<12} {str(win):<12} {pay:>8} {s_pay:>+10} {s_hit:>+10}")
print()
print("怎麼用這張表：")
print(" - 第三輪「一段長 k 的符號 x」= 1 個上對 + 1 個下對 + (k-2) 個三連，與段的排列順序無關。")
print("   所以第三輪整條的淨賠付分數 = 各格淨分數相加。")
print(" - 目標：淨賠付分數總和 = 0，淨中獎分數總和 >= 0。")
print(" - 淨分數為正的格子（例如三連 1）把 RTP 往上推，為負的（死格、三連 0）往下拉。")
print(" - 用紙筆列線性方程：a x (三連 1) + b x (三連 0) + d x (死格) + 各段頭尾的上對下對 = 0，")
print("   找非負整數解 (a, b, d)。把 reel3 改成對應的段，重新執行本檔驗證。")
print(" - 死格：放在兩段之間（或尾端）、與左右都不同且彼此交錯的符號（如 2,3,2,3）。")
print("   它只增加 N、不增加任何配對，是「只拉低 RTP」的細調旋鈕。")
print(" - 若怎麼湊都除不盡，換一組前兩輪（改 0 與 1 的段長）再試，分數會跟著變。")
