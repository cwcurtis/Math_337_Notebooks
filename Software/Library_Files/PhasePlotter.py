import numpy as np
import scipy.optimize as spo
import matplotlib.pyplot as plt


class PhasePlotter(object):

    def __init__(self, a, b, fun):
        self.a = a
        self.b = b
        self.fun = fun

    def PhaseField1D(self):
        dx = 1e-4
        nvals = np.int((self.b-self.a)/dx)
        xvals = np.linspace(self.a, self.b, nvals + 1)
        fvals = self.fun(xvals)
        ipos = fvals >= 0.
        ineg = fvals < 0.
        xpos = xvals[ipos]
        xneg = xvals[ineg]

        npos = np.size(xpos)
        pjmps = xpos[1:] - xpos[:npos-1]
        pizrs = pjmps > 2.*dx
        zrsl = xpos[:npos-1][pizrs]
        zrsr = xpos[1:][pizrs]

        zrs = np.concatenate((zrsl, zrsr), 0)
        zrs = np.sort(zrs)

        if xvals[0] < zrs[0]:
            zrs = np.concatenate((np.array([xvals[0]]), zrs), 0)
        if xvals[-1] > zrs[-1]:
            zrs = np.concatenate((zrs, np.array([xvals[-1]])), 0)

        nzrs = np.size(zrs)
        mds = (zrs[1:] + zrs[:nzrs-1])/2.
        fmds = self.fun(mds)

        plt.plot(xpos, fvals[ipos], color='b')
        plt.plot(xneg, fvals[ineg], color='r')
        plt.plot(xvals, np.zeros(np.size(xvals)), color='k')

        for jj in range(nzrs-1):
            if fmds[jj] > 0.:
                plt.arrow(mds[jj], 0., .1, 0., shape='full', length_includes_head=True, head_width=.1)
            else:
                plt.arrow(mds[jj], 0., -.1, 0., shape='full', length_includes_head=True, head_width=.1)

        for jj in range(1, nzrs-1):
            if fmds[jj-1] > 0. and fmds[jj] < 0.:
                plt.plot(zrs[jj], 0., color='k', marker='o', markersize=10, fillstyle='full')
            elif fmds[jj-1] < 0. and fmds[jj] > 0.:
                plt.plot(zrs[jj], 0., color='k', marker='o', markersize=10, fillstyle='none')
            else:
                plt.plot(zrs[jj], 0., color='k', marker='o', markersize=10, fillstyle='right')

        plt.xlabel('$y$')
        plt.ylabel('$f(y)$')
        plt.title('Phase Plot')
