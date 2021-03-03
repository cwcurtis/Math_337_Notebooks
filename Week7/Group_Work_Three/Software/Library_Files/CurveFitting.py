import numpy as np
from scipy.optimize import minimize


def least_squares_vbfit(params, *indata):
    data = np.array(indata)
    dim = np.int(np.size(data)/2)
    data = data.reshape((dim, 2))
    return np.sum((data[:, 1] - params[0]*(1. - np.exp(-params[1]*data[:, 0])))**2.)


def vonbertalfit(data):
    params = np.array([100., .1])
    pfin = minimize(least_squares_vbfit, params, args=tuple(data.flatten()))
    return pfin.x


def allometricfit(data):
    rhs = [np.sum(data[:, 1]), np.sum(data[:, 0]*data[:, 1])]
    n = np.size(data[:, 0])
    g1 = np.sum(data[:, 0])
    g2 = np.sum(data[:, 0]**2.)
    det = n*g2 - g1**2.
    lhs0 = (g2*rhs[0] - g1*rhs[1])/det
    lhs1 = (-g1*rhs[0] + n*rhs[1])/det
    return [lhs0, lhs1]


def choose_fun(lval, k):
    return np.math.factorial(k)/(np.math.factorial(lval)*np.math.factorial(k-lval))


def gfun(time, Lstar, b, a, k):
    rhs = b*time
    wstar = a * Lstar**k
    etrm = np.exp(-b * time)
    fac = -1.
    for ll in range(1, np.int(k)+1):
        rhs += fac * (1.-etrm)/ll * choose_fun(ll, np.int(k))
        etrm *= etrm
        fac *= -1
    return wstar*rhs/b


def wfun(time, Lstar, b, a, k):
    wstar = a * Lstar ** k
    etrm = np.exp(-b * time)
    return wstar*(1.-etrm)**k


def mercuryfit(data, Lstar, b, a, k):
    gvals = gfun(data[:, 0], Lstar, b, a, k)
    wvals = wfun(data[:, 0], Lstar, b, a, k)
    return [np.sum(gvals*data[:, 1]*wvals)/np.sum(gvals**2.), gvals]