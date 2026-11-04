""" Get window display and """

MULTIPLIER = {0: 5, 1: 11, 2: 20, 3: 60, 4: 100}  # 20x of original multiplier to avoid floating point precision error

def payout_calc(col1, col2, col3) -> int:
    """
    Calculate payout for each given column, col1, col2 and col3 are tuples of three integers
    Args:
        col1: Left column of reel
        col2: Middle column of reel
        col3: Right column of reel
    Returns:
        Coins (also 20x) host shall pay
    """
    display_panel = [col1, col2, col3]
    check_value = display_panel[1][1]
    # The center symbol is the most important, check the center symbol with 3x3 and 2x2 scenario
    # Check 3x3 condition and return first, not summing other 2x2 conditions if 3x3 hits
    if all(v == check_value for t in display_panel for v in t):
        return MULTIPLIER[display_panel[1][1]] * 5
    else:
        return_coins = 0
        # Up check and calculate
        if col2[0] == check_value:
            # Left 2 x 2
            if col1[0] == check_value and col1[1] == check_value:
                return_coins += MULTIPLIER[display_panel[1][1]]
            # Right 2 x 2
            if col3[0] == check_value and col3[1] == check_value:
                return_coins += MULTIPLIER[display_panel[1][1]]

        # Down check
        if col2[2] != check_value:
            return_coins += 0
        else:
            # Left 2 x 2
            if col1[1] == check_value and col1[2] == check_value:
                return_coins += MULTIPLIER[display_panel[1][1]]
            # Right 2 x 2
            if col3[1] == check_value and col3[2] == check_value:
                return_coins += MULTIPLIER[display_panel[1][1]]
            else:
                return_coins += 0
        return return_coins
if __name__ == '__main__':
    t = payout_calc((4, 4, 4), (4, 4, 4), (4, 4, 4))
    print(t)
