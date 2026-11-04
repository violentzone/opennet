from itertools import product

from calculations import get_all_reel_display, payout_calc

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
    r1 = r2 = r3 = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4]
    pay_sum, N, win_rate = get_parameters_from_reels(r1, r2, r3)
    print('pay_sum: ', pay_sum, 'N: ', N, 'win_rate: ', win_rate, 'calculate: ', pay_sum / (N * 19))