"""步驟 1：滾輪是環狀的，每個停點顯示三格。

先搞清楚「一條滾輪有幾種可能畫面」。答案是：長度 L 的滾輪就有 L 種，
因為停點 p 可以是 0..L-1，每個停點顯示 p, p+1, p+2 三格，超出尾端就繞回開頭。

請用紙筆自己列一次，再跟程式輸出對照。
"""
from slot_core import windows

reel = (0, 0, 1, 1, 2)
print(f"滾輪: {list(reel)}  長度 L = {len(reel)}")
print()
print("停點 p   顯示的三格 (p, p+1, p+2)")
for p, w in enumerate(windows(reel)):
    print(f"  {p}       {w}")
print()
print(f"共 {len(windows(reel))} 種畫面，和長度一樣。")
print("注意最後兩個停點繞回了開頭：p=3 顯示 (1, 2, 0)，p=4 顯示 (2, 0, 0)。")
print()
print("三條滾輪獨立停下，所以總結果數 N = L1 x L2 x L3，每種結果等機率。")
for L in [(5, 5, 5), (20, 20, 20), (20, 20, 45)]:
    print(f"  長度 {L} -> N = {L[0] * L[1] * L[2]}")
