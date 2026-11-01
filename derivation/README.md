# 解題推導腳本（按順序執行）

每一步只做一件事，印出中間結果讓人可以手算對照。執行方式：

```powershell
cd derivation
python step1_windows.py
python step2_payout.py
python step3_rtp_winrate.py
python step4_experiments.py
python step5_tuning.py     # 改檔案頂端的 reel1/2/3，反覆執行直到「合法？ True」
python step6_verify.py     # 填入最終配置，產生報告用的數字
```

| 檔案 | 回答的問題 |
|---|---|
| slot_core.py | 共用函式：視窗、賠付、完整列舉、整數判定 |
| step1_windows.py | 一條滾輪有幾種畫面？環狀繞回怎麼算？N 是什麼？ |
| step2_payout.py | 一個 3x3 盤面賠多少？為什麼倍率要乘 20 變整數？ |
| step3_rtp_winrate.py | RTP 與中獎率怎麼算？為什麼變成 pay_sum == 19N 和 100·hits >= 55N？ |
| step4_experiments.py | 哪些東西會動 RTP／中獎率？段長、符號比例、樞紐欄 |
| step5_tuning.py | 固定前兩輪後，第三輪每加一格會改變多少？用紙筆解出該加幾格 |
| step6_verify.py | 精確驗證、貢獻表、蒙地卡羅交叉確認 |

`slot_core.py` 裡的 `STACK_3X3` 控制 3x3 全滿是否同時加上四個 2x2，預設 `False`（只賠 5 倍），與專案 README 的假設一致。
