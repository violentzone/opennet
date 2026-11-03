""" Iterate through possibilities to get valid reels"""

INIT_REEL = [0] * 3 + [1] * 3 + [2] * 3 + [3] * 3 + [4] * 3

def get_all_reel_display(reel_list):
    """
    Gets all displays of a reel's symbols
    Args:
        reel_list: The reel's symbol list

    Returns:
        All symbols conformation in display panel
    """
    length = len(reel_list)
    all_stop = [[reel_list[i], reel_list[(i + 1) % length], reel_list[(i + 2) % length]] for i in range(length)]
    return all_stop

def get_first_correct_reels():
    """

    Returns:

    """

if __name__ == '__main__':
    get_all_reel_display(INIT_REEL)
    # print(INIT_REEL)