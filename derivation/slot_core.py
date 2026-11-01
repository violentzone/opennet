"""共用的基礎函式：視窗、賠付、完整列舉。

這個檔案刻意只用最直白的寫法（直接在 3x3 盤面上比對圖案），
目的是讓人可以逐行讀懂，也能用紙筆對照結果。
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product

sys.stdout.reconfigure(encoding="utf-8")

# ---- 題目常數 ----------------------------------------------------------------
# 倍率乘以 20 後的整數「點數」。1 倍 = 20 點。
# 0.25 -> 5, 0.55 -> 11, 1 -> 20, 3 -> 60, 5 -> 100
MULT = {0: 5, 1: 11, 2: 20, 3: 60, 4: 100}
SCALE = 20                 # 點數 / 倍率
TARGET_PAY = 19            # RTP 0.95 = 19/20，也就是平均每轉拿回 19 點
MIN_HIT_PCT = 55           # 中獎率 >= 55%

# 3x3 全滿時要不要同時加上四個 2x2？
#   False: 只賠 5 x 倍率          （README 採用的假設）
#   True : 四個 2x2 + 5 x 倍率 = 9 x 倍率
STACK_3X3 = False

# 五個圖案各自覆蓋哪些格子，座標是 (欄, 列)，從 0 開始
PATTERNS = {
    "左上 2x2": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "右上 2x2": [(1, 0), (2, 0), (1, 1), (2, 1)],
    "左下 2x2": [(0, 1), (1, 1), (0, 2), (1, 2)],
    "右下 2x2": [(1, 1), (2, 1), (1, 2), (2, 2)],
    "全滿 3x3": [(c, r) for c in range(3) for r in range(3)],
}


# ---- 第 1 層：滾輪 -> 視窗 -----------------------------------------------------
def windows(reel):
    """滾輪每個停點 p 顯示的三格 (reel[p], reel[p+1], reel[p+2])，尾端繞回開頭。"""
    n = len(reel)
    return [(reel[i], reel[(i + 1) % n], reel[(i + 2) % n]) for i in range(n)]


# ---- 第 2 層：盤面 -> 賠付 -----------------------------------------------------
def pattern_hits(grid):
    """回傳成立的圖案清單 [(圖案名, 符號)]。grid[欄][列]。"""
    hits = []
    for name, cells in PATTERNS.items():
        symbols = {grid[c][r] for c, r in cells}
        if len(symbols) == 1:
            hits.append((name, symbols.pop()))
    return hits


def payout_points(grid):
    """一個盤面的總賠付（點數，整數）。"""
    hits = pattern_hits(grid)
    full = [s for name, s in hits if name == "全滿 3x3"]
    if full:
        sym = full[0]
        return 5 * MULT[sym] + (4 * MULT[sym] if STACK_3X3 else 0)
    return sum(MULT[s] for _, s in hits)


# ---- 第 3 層：三條滾輪 -> RTP 與中獎率 ------------------------------------------
def evaluate(reel1, reel2, reel3):
    """完整列舉 N = L1*L2*L3 種結果，回傳 (pay_sum, hits, N)。全部是整數。"""
    pay_sum = hits = 0
    for c1, c2, c3 in product(windows(reel1), windows(reel2), windows(reel3)):
        p = payout_points((c1, c2, c3))
        pay_sum += p
        hits += p > 0
    n = len(reel1) * len(reel2) * len(reel3)
    return pay_sum, hits, n


def rtp(pay_sum, n):
    return Fraction(pay_sum, SCALE * n)


def hit_rate(hits, n):
    return Fraction(hits, n)


def is_valid(pay_sum, hits, n):
    """兩個條件都用整數比較。"""
    return pay_sum == TARGET_PAY * n and 100 * hits >= MIN_HIT_PCT * n


def describe(reel):
    """把 [0,0,0,1,1] 這種序列壓成 '0x3 1x2' 方便閱讀。"""
    out, i = [], 0
    while i < len(reel):
        j = i
        while j < len(reel) and reel[j] == reel[i]:
            j += 1
        out.append(f"{reel[i]}x{j - i}")
        i = j
    return " ".join(out)


def runs(*pairs):
    """runs((0, 3), (1, 2)) -> (0, 0, 0, 1, 1)。用「段」描述滾輪。"""
    return tuple(s for s, k in pairs for _ in range(k))
