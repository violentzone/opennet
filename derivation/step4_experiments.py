"""步驟 4：哪些東西會動 RTP 和中獎率？——做實驗建立直覺。

先猜，再跑。每一組實驗只改一個變數。
"""
from slot_core import evaluate, hit_rate, rtp, runs


def row(label, r1, r2, r3):
    pay_sum, hits, n = evaluate(r1, r2, r3)
    print(f"{label:<32} N={n:>6}  RTP={float(rtp(pay_sum, n)):.3f}  中獎率={float(hit_rate(hits, n)):.3f}")


def same(r):
    return (r, r, r)


print("實驗一：三輪相同，只用符號 0 和 1。改「段長」與「總長度」")
print("先猜：長度加倍，RTP 會變嗎？")
print()
row("0,1 交錯 (段長 1)  L=20",  *same(runs(*[(0, 1), (1, 1)] * 10)))
row("[0x2,1x2] x5       L=20",  *same(runs(*[(0, 2), (1, 2)] * 5)))
row("[0x5,1x5]          L=10",  *same(runs((0, 5), (1, 5))))
row("[0x5,1x5] x2       L=20",  *same(runs(*[(0, 5), (1, 5)] * 2)))
row("[0x5,1x5] x3       L=30",  *same(runs(*[(0, 5), (1, 5)] * 3)))
row("[0x10,1x10]        L=20",  *same(runs((0, 10), (1, 10))))
row("[0x12,1x12]        L=24",  *same(runs((0, 12), (1, 12))))
row("[0x7,1x3] x2       L=20",  *same(runs(*[(0, 7), (1, 3)] * 2)))
row("全部 0             L=20",  *same(runs((0, 20))))
print()
print("觀察：")
print(" - 同一圖樣重複 2 次、3 次，數字完全一樣 → 滾輪長度本身不是旋鈕。")
print(" - 段長 2 → 5 → 10，RTP 與中獎率都上升 → 段長是第一個旋鈕。")
print(" - 0 多 1 少時中獎率略高、RTP 略低（0 比較便宜）→ 符號比例是第二個旋鈕。")
print(" - 全部同一符號 RTP 爆掉，所以至少要混兩種符號來稀釋配對。")
print()

print("實驗二：第 2 欄是樞紐（四個 2x2 都包含第 2 欄）")
side = runs((0, 8), (1, 8))
row("樞紐 = [0x8,1x8]",                side, runs((0, 8), (1, 8)), side)
row("樞紐全是段長 1 (0,1 交錯)",       side, runs(*[(0, 1), (1, 1)] * 8), side)
row("側欄加一段 4x2，樞紐沒有 4",      side + (4, 4), runs((0, 8), (1, 8)), side + (4, 4))
row("側欄與樞紐都加一段 4x2",          side + (4, 4), runs((0, 8), (1, 8), (4, 2)), side + (4, 4))
print()
print("觀察：")
print(" - 樞紐沒有任何配對時，不管側欄怎麼排都不會中。")
print(" - 側欄有的符號，樞紐也要有，否則那個符號貢獻 0，只會稀釋中獎率。")
print()

print("實驗三：中獎率的下限壓住了平均賠付")
print(" RTP = 中獎率 x 平均每次中獎賠付")
print(" 0.95 / 0.55 ≈ 1.73 → 平均每次中獎最多約 1.73 倍")
print(" 單一 2x2：0 賠 0.25、1 賠 0.55、2 賠 1、3 賠 3、4 賠 5")
print(" 所以大多數中獎必須是符號 0、1 的 2x2，高倍率符號只能是少數。")
print()
print("結論：用低倍率符號的長段堆中獎率，再用少量高倍率符號或死格把 RTP 修到 0.95。")
