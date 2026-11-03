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
        # Up check
        if col2[0] != check_value:
            return 0
        else:
            if col1[0] == check_value and col1[1] == check_value:
                return MULTIPLIER[display_panel[1][1]]

        # Down check
        if col2[2] != check_value:
            return 0
        else:
            if col1[1] == check_value and col1[2] == check_value:
                return MULTIPLIER[display_panel[1][1]]
            else:
                return 0

if __name__ == '__main__':
    print([0] * 3 + [1] * 3)