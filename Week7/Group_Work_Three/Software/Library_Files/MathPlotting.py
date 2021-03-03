import numpy as np
import matplotlib.pyplot as plt


class MathPlotting(object):

    def __init__(self, a, b, sz, var):
        self.left_side = a
        self.right_side = b
        self.window_size = sz
        self.axis_label = var

        dx = 1e-2
        self.xaxis = np.linspace(a, b, np.int((b-a)/dx)+1)

    def resize(self, rsz):
        self.window_size = rsz

    def fun_plot(self, dims, *funs):

        num_funs = len(funs)
        if num_funs == 0:
            print("Need to please provide functions to plot.")
            return
        if len(dims) == 0:
            print("Need to please provide subplot dimensions.")
            return
        else:
            num_axes = dims[1] * dims[0]

        if num_funs < num_axes:
            print("Please do not ask for empty graphs.")
            return
        else:
            wsize = self.window_size
            fig, axes = plt.subplots(ncols=dims[1], nrows=dims[0], figsize=(wsize, wsize))
            cnt = 0
            if num_axes == 1:
                for fun in funs:
                    fvals = fun(self.xaxis)
                    sstr = '$f_{%d}(' % cnt
                    labels = sstr + self.axis_label + ')$'
                    axes.plot(self.xaxis, fvals, label=labels)
                    axes.set_xlabel('$' + self.axis_label + '$', fontsize=24)
                    cnt += 1
                plt.legend(loc='best', fontsize=12)

            elif num_funs == num_axes:
                ax = axes.flatten()
                cmap = ['r', 'k', 'b', 'g', 'v']
                if num_funs > 5:
                    cmap = cmap + list(np.random.rand(num_funs-5, 3))
                for fun in funs:
                    fvals = fun(self.xaxis)
                    sstr = '$f_{%d}(' % cnt
                    labels = sstr + self.axis_label + ')$'
                    ax[cnt].plot(self.xaxis, fvals, color = cmap[cnt], label=labels)
                    ax[cnt].set_xlabel('$' + self.axis_label + '$', fontsize=24)
                    ax[cnt].legend(loc='best', fontsize=12)
                    cnt += 1

            elif num_funs > num_axes:
                ax = axes.flatten()
                axcnt = 0
                for fun in funs:
                    fvals = fun(self.xaxis)
                    sstr = '$f_{%d}(' % cnt
                    labels = sstr + self.axis_label + ')$'
                    ax[axcnt].plot(self.xaxis, fvals, label=labels)
                    ax[axcnt].set_xlabel('$' + self.axis_label + '$', fontsize=24)
                    ax[axcnt].legend(loc='best', fontsize=12)
                    cnt += 1
                    axcnt += 1
                    if axcnt == num_axes:
                        axcnt = 0

            plt.tight_layout()
            plt.show()
            return
