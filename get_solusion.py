from itertools import product

from typing import Optional

from calculations import get_all_reel_display, pay_add, payout_calc

def get_parameters_from_reels(reel1: list[int], reel2: list[int], reel3: list[int]):
    """
    Gets payout_sum and total result count from three reels
    Args:
        reel1: Reel1 symbol list
        reel2: Reel2 symbol list
        reel3: Reel3 symbol list

    Returns:
        Pay sum(pay_sum), total results(n) and win rate(w_rate)
    """
    po1 = get_all_reel_display(reel1)
    po2 = get_all_reel_display(reel2)
    po3 = get_all_reel_display(reel3)
    n = len(reel1) * len(reel2) * len(reel3)
    pay_sum = 0
    w = 0
    for x, y, z in product(po1, po2, po3):
        pay = payout_calc(x, y, z)
        if pay > 0:
            w += 1
        pay_sum += pay
    w_rate = w / n
    return pay_sum, n, w_rate

def solve_reel3(score: int, diff_0: int, diff_1: int) -> Optional[tuple[int, int]]:
    """Find how many 0s and 1s to add to reel 3 so that pay_sum == 19N.

    Each added 0 moves (pay_sum - 19N) by diff_0, each added 1 by diff_1, so we need
    non-negative integers (x, y) with score + x*diff_0 + y*diff_1 == 0.

    Args:
        score: pay_sum - 19N with the current reel 3.
        diff_0: pay_add(reel1_2, 0) - threshold.
        diff_1: pay_add(reel1_2, 1) - threshold.

    Returns:
        (x, y) = numbers of 0s and 1s to add, or None if no solution in range.
    """
    for x in range(30):
        remain = -(score + x * diff_0)
        if remain == 0:
            return x, 0
        if diff_1 != 0 and remain % diff_1 == 0:
            return x, remain // diff_1
    return None


def grid_answer(init_reel_state: list[int], max_add: int = 30) -> Optional[tuple[list[int], list[int]]]:
    """Scan 0/1 counts of reels 1-2, then solve reel 3 exactly.

    For each (a, b) added to reels 1-2: threshold = L1 x L2 x 19 is what one extra
    reel-3 cell must pay; pay_add tells what it actually pays. Their difference per
    added 0 / 1 lets solve_reel3 close the gap pay_sum - 19N to exactly zero.

    Args:
        init_reel_state: The initial state of all reels.
        max_add: Exclusive upper bound for added 0s and 1s on every reel.

    Returns:
        Symbol lists of reel 1, reel 2 and reel 3, or None if nothing found.
    """
    for a in range(max_add):
        for b in range(max_add):
            reel1_2 = sorted(init_reel_state + [0] * a + [1] * b)
            threshold = len(reel1_2) ** 2 * 19
            diff_0 = pay_add(reel1_2, 0) - threshold
            diff_1 = pay_add(reel1_2, 1) - threshold
            pay_sum, n, _ = get_parameters_from_reels(reel1_2, reel1_2, init_reel_state)
            added = solve_reel3(pay_sum - 19 * n, diff_0, diff_1)
            if added is None:
                continue
            reel3 = sorted(init_reel_state + [0] * added[0] + [1] * added[1])
            pay_sum, n, w_rate = get_parameters_from_reels(reel1_2, reel1_2, reel3)
            if pay_sum == 19 * n and w_rate > 0.55:
                return reel1_2, reel3
    return None

# def brute_force_0(init_reel1: list[int], init_reel2: list[int], init_reel3: list[int]):
#     """
#     Add symbol 0 to every reel and check if any meets requirement of pay_sum == N x 19 and win rate > 0.55, only iterate 128 times cus if a reel exceed len of 128, it is too wild
#     Early break when
#     Args:
#         init_reel1: Init state of reel1
#         init_reel2: Init state of reel2
#         init_reel3: Init state of reel3
#
#     Returns:
#         The valid reels(hopefully)
#     """
#     for _ in range(0, 128):
#         init_reel1 = [0] + init_reel1
#         init_reel2 = [0] + init_reel2
#         init_reel3 = [0] + init_reel3
#         pay_sum, n, w_rate = get_parameters_from_reels(init_reel1, init_reel2, init_reel3)
#         print('current: ', init_reel3)
#         print('pay_sum: ', pay_sum,"N:", n,'win rate: ', w_rate)
#         print('calculate: ', pay_sum / (n * 19))
#         print('=' * 75)
#         if pay_sum  == n * 19 and w_rate > 0.55:
#             return init_reel1, init_reel2, init_reel3
#     print('No result')
#     return None
#
# def brute_force_2(init_reel1: list[int], init_reel2: list[int], init_reel3: list[int]):
#     for _ in range(0, 128):
#         init_reel1 += [2]
#         init_reel2 += [2]
#         init_reel3 += [2]
#         for reel in (init_reel1, init_reel2, init_reel3):
#             reel.sort()
#         pay_sum, n, w_rate = get_parameters_from_reels(init_reel1, init_reel2, init_reel3)
#         print('current: ', init_reel3)
#         print('pay_sum: ', pay_sum,"N:", n,'win rate: ', w_rate)
#         print('calculate: ', pay_sum / (n * 19))
#         print('=' * 75)
#         if pay_sum  == n * 19 and w_rate > 0.55:
#             return init_reel1, init_reel2, init_reel3
#
#     print('No result')
#     return None
# def tune_reel3(reel1: list[int], reel2: list[int], init_reel3: list[int]):
#     for _ in range(0, 128):
#         init_reel3 = [1] + init_reel3
#         init_reel3.sort()
#         pay_sum, n, w_rate = get_parameters_from_reels(reel1, reel2, init_reel3)
#         print('current: ', init_reel3)
#         print('pay_sum: ', pay_sum, "N:", n, 'win rate: ', w_rate)
#         print('calculate: ', pay_sum / (n * 19))
#         print('=' * 75)
#         if pay_sum  == n * 19 and w_rate > 0.55:
#             return reel1, reel2, init_reel3
#     print('No result')

if __name__ == '__main__':
    result = grid_answer([0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4])
    if result is None:
        print('No result')
    else:
        # print(result)
        reel1_2, reel3 = result
        pay_sum, n, w_rate = get_parameters_from_reels(reel1_2, reel1_2, reel3)
        print(f'reel1 = reel2 = {reel1_2}')
        print(f'reel3 = {reel3}')
        print(f'pay_sum: {pay_sum}  N: {n}  RTP: {pay_sum / (20 * n)}  win rate: {w_rate:.4f}')