import numpy as np
import matplotlib.pyplot as plt
from FilePlotting import FileMaker


class PhasePlotter(object):

    def __init__(self, a, b, fun, axis, description):
        self.a = a
        self.b = b
        self.fun = fun
        self.axis = axis
        self.fhandle = FileMaker('phase_figs_' + description)

    def PhaseField1D(self):
        dx = 1e-2
        nvals = np.int((self.b-self.a)/dx)
        xvals = np.linspace(self.a, self.b, nvals + 1)
        fvals = self.fun(xvals)

        ipos = fvals >= 0.
        ineg = fvals < 0.

        xpos = xvals[ipos]
        xneg = xvals[ineg]
        npos = np.size(xpos)
        nneg = np.size(xneg)
        pjmps = xpos[1:] - xpos[:npos-1]
        pizrs = pjmps > 2.*dx

        if np.mod(np.sum(pizrs), 2) > 0:
            zrsl = xpos[:npos-1][pizrs]
            zrsr = xpos[1:][pizrs]
        else:
            pjmps = xneg[1:] - xneg[:nneg - 1]
            pizrs = pjmps > 2. * dx
            zrsl = xneg[:nneg - 1][pizrs]
            zrsr = xneg[1:][pizrs]

        zrs = np.concatenate((zrsl, zrsr), 0)
        zrs = np.sort(zrs)

        if xvals[0] < zrs[0]:
            zrs = np.concatenate((np.array([xvals[0]]), zrs), 0)
        if xvals[-1] > zrs[-1]:
            zrs = np.concatenate((zrs, np.array([xvals[-1]])), 0)

        nzrs = np.size(zrs)
        mds = (zrs[1:] + zrs[:nzrs-1])/2.
        fmds = self.fun(mds)
        fpos = np.zeros(np.size(xvals), dtype=np.float64)
        fneg = np.zeros(np.size(xvals), dtype=np.float64)
        fpos[ipos] = fvals[ipos]
        fneg[ineg] = fvals[ineg]
        plt.plot(xvals, fpos, color='b')
        plt.plot(xvals, fneg, color='r')
        plt.plot(xvals, np.zeros(np.size(xvals)), color='k')
        head_size = .1*(np.max(fvals)-np.min(fvals))
        dx_arrow = .025*(self.b-self.a)
        for jj in range(nzrs-1):
            if fmds[jj] > 0.:
                plt.arrow(mds[jj], 0., dx_arrow, 0., shape='full', length_includes_head=True, head_width=head_size)
            else:
                plt.arrow(mds[jj], 0., -1.*dx_arrow, 0., shape='full', length_includes_head=True, head_width=head_size)

        for jj in range(1, nzrs-1):
            if fmds[jj-1] > 0. and fmds[jj] < 0.:
                plt.plot(zrs[jj], 0., color='k', marker='o', markersize=10, fillstyle='full')
            elif fmds[jj-1] < 0. and fmds[jj] > 0.:
                plt.plot(zrs[jj], 0., color='k', marker='o', markersize=10, fillstyle='none')
            else:
                plt.plot(zrs[jj], 0., color='k', marker='o', markersize=10, fillstyle='right')

        plt.xlabel(self.axis)
        plt.ylabel('f('+self.axis+')')
        plt.title('Phase Plot')
        plt.savefig(self.fhandle + 'One_Dimensional_Phase_Plot' + '.png', format='png')

