import numpy as np


def return_plottable_hist(my_list, bins=100):
    """Helper to return histogram in directly plottable format.

    Args:
        - list of numerical values to histogram
        - num bins desired (defaults to 100)

    Returns:
        tuple bin_mids, bin_counts

    """

    hist = np.histogram(my_list, bins=bins)
    mids = [float(hist[1][i] + hist[1][i+1])/2 for i in range(len(hist[1])-1)]

    return mids, hist[0]
