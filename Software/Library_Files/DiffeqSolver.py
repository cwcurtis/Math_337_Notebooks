import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class DiffeqSolver(object):

    def __init__(self, dt, t0, tf, y0, fun):
        self.dt = dt
        self.t0 = t0
        self.tf = tf
        self.y0 = y0
        self.fun = fun
        nstep = np.int((tf - t0) / dt)
        self.nstep = nstep
        self.tvals = np.linspace(t0, tf, nstep+1)
        self.ysols = np.zeros((nstep + 1, 3), dtype=np.float64)
        self.track = [0, 0, 0]

    def PlotSol(self, ysol, tag):
        plt.plot(self.tvals, ysol, color='k')
        plt.xlabel("$t$")
        plt.ylabel("$y(t)$")
        plt.title("Solution generated via " + tag + " method")

    def PlotCompare(self, fact):
        yact = fact(self.tvals)
        plt.plot(self.tvals, yact, color='k', label="True")
        colors = ['r', 'b', 'g']
        labels = ['Euler', 'Huen', 'RK']
        for jj in range(3):
            if self.track[jj] == 1:
                plt.plot(self.tvals, self.ysols[:, jj], color=colors[jj], label=labels[jj])
        plt.xlabel("$t$")
        plt.ylabel("$y(t)$")
        plt.title("Comparison of Numerical Solutions to True Solution")
        plt.legend()

    def TableCompare(self, fact):
        yact = fact(self.tvals)
        dloc = {'Time': self.tvals,
                'True': yact}
        if self.track[0] == 1:
            dloc['Euler'] = self.ysols[:, 0]
        if self.track[1] == 1:
            dloc['Heun'] = self.ysols[:, 1]
        if self.track[2] == 1:
            dloc['RK4'] = self.ysols[:, 2]
        dfsol = pd.DataFrame(dloc)
        print(dfsol.to_markdown(showindex=False))

    def ExplicitEuler(self):
        ysol = np.zeros(self.nstep+1, dtype=np.float64)
        ysol[0] = self.y0
        dtl = self.dt
        for jj in range(1, self.nstep+1):
            ysol[jj] = ysol[jj-1] + dtl*self.fun(self.tvals[jj-1], ysol[jj-1])
        self.ysols[:, 0] = ysol
        self.track[0] = 1
        self.PlotSol(ysol, 'Explicit Euler')

    def HeunMethod(self):
        ysol = np.zeros(self.nstep + 1, dtype=np.float64)
        ysol[0] = self.y0
        dtl = self.dt

        for jj in range(1, self.nstep + 1):
            tl = self.tvals[jj-1]
            yl = ysol[jj-1]
            k1 = dtl * self.fun(tl, yl)
            k2 = dtl * self.fun(tl+dtl, yl+k1)
            ysol[jj] = ysol[jj - 1] + .5*(k1+k2)
        self.ysols[:, 1] = ysol
        self.track[1] = 1
        self.PlotSol(ysol, 'Heun Method')

    def RungeKutta4(self):
        ysol = np.zeros(self.nstep + 1, dtype=np.float64)
        ysol[0] = self.y0
        dtl = self.dt

        for jj in range(1, self.nstep + 1):
            tl = self.tvals[jj - 1]
            yl = ysol[jj - 1]
            k1 = dtl * self.fun(tl, yl)
            k2 = dtl * self.fun(tl+dtl/2., yl + k1/2.)
            k3 = dtl * self.fun(tl+dtl/2., yl + k2/2.)
            k4 = dtl * self.fun(tl+dtl, yl + k3)
            ysol[jj] = ysol[jj - 1] + (k1 + 2.*k2 + 2.*k3 + k4)/6.
        self.ysols[:, 2] = ysol
        self.track[2] = 1
        self.PlotSol(ysol, 'Runge Kutta 4')
