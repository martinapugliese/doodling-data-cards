import numpy as np
from scipy import optimize


def fit_powlaw(x, y, start=0, x0=[1, 1]):

    """
    Fit a powerlaw in log-log scale (fit the logs) with optimize.leastsq, given x and y and the (defaults to index 0) starting point for them
    so to exclude an initial part. Uses log in base 10.
    x0 is the starting value of the estimation params (defaults to [1, 1]).
    """

    x = x[start:]
    y = y[start:]

    log_x = np.log10(x)
    log_y = np.log10(y)

    fitfunc = lambda p, x: p[0] + p[1] * x           # fitting function
    errfunc = lambda p, x, y: (y - fitfunc(p, x))    # error

    olsfit = optimize.leastsq(errfunc, x0, args=(log_x, log_y))

    p_fit = olsfit[0]
    covar_fit = olsfit[1]

    return p_fit, covar_fit
