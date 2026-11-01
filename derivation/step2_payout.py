"""步驟 2：一個 3x3 盤面賠多少？

先把倍率換成整數「點數」（1 倍 = 20 點），再逐一檢查五個圖案。
先用紙筆判斷每個盤面哪些圖案成立、賠多少，再跟程式對照。
"""
from slot_core import MULT, SCALE, STACK_3X3, pattern_hits, payout_points

print("倍率 -> 點數（x20）：", {k: f"{v / SCALE} 倍 = {v} 點" for k, v in MULT.items()})
print()
print("為什麼要換成點數？因為 float 存不準小數：")
print(f"  0.55 * 3 == 1.65 ?  {0.55 * 3 == 1.65}   (實際算出 {0.55 * 3})")
print(f"  sum([0.05]*19) == 0.95 ?  {sum([0.05] * 19) == 0.95}   (實際算出 {sum([0.05] * 19)})")
print("  這叫浮點數精度誤差。改用整數點數後 11 * 3 == 33 永遠成立。")
print()


def show(name, grid):
    """grid 用 [欄][列] 存，印出時轉成人看的 列 x 欄。"""
    print(f"--- {name} ---")
    for r in range(3):
        print("   ", " ".join(str(grid[c][r]) for c in range(3)))
    for pname, sym in pattern_hits(grid):
        print(f"    成立：{pname}，符號 {sym}，{MULT[sym]} 點")
    total = payout_points(grid)
    if any(name == "全滿 3x3" for name, _ in pattern_hits(grid)) and not STACK_3X3:
        print("    （全滿成立時只賠 5 x 倍率，四個 2x2 不另計）")
    print(f"    總賠付 = {total} 點 = {total / SCALE} 倍 = 下注 100 賠 {total / SCALE * 100:.0f}")
    print()


# 每個盤面以三「欄」給定：grid[欄] = (上, 中, 下)
show("什麼都沒中",             ((0, 1, 2), (1, 2, 0), (2, 0, 1)))
show("只中左上 2x2 (符號 1)",  ((1, 1, 0), (1, 1, 2), (0, 3, 4)))
show("左上與右下同時成立 (都是 1)", ((1, 1, 2), (1, 1, 1), (3, 1, 1)))
show("左右兩個 2x2 都是 0",     ((0, 0, 3), (0, 0, 4), (0, 0, 2)))
show("全滿 3x3 (符號 1)",       ((1, 1, 1), (1, 1, 1), (1, 1, 1)))
print(f"STACK_3X3 = {STACK_3X3}：全滿時", "有" if STACK_3X3 else "沒有", "加上四個 2x2。")
print("這是題目沒說清楚的地方，報告裡要明寫你的假設。")
