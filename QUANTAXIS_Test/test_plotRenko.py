import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from matplotlib.patches import Rectangle

import QUANTAXIS as QA


def plot_renko(ax, bricks):

    ymax = max(bricks) 
    ymin = min(np.absolute(bricks))
    width = 1.0 / len(bricks)
    prev_height = 0
    for index, brick in enumerate(bricks):
        facecolor = 'red' if brick > 0 else 'green'
        ypos = (abs(brick) - ymin) / (ymax - ymin)
        if index == len(bricks)-1:
            pass
        elif bricks[index] == bricks[index+1]:
            height = prev_height
        else:
            aux1 = (abs(bricks[index+1]) - ymin) / (ymax - ymin)
            height = abs(aux1 - ypos)
            prev_height = height
        rect = Rectangle((index * width, ypos), width, height,
                         facecolor=facecolor, alpha=0.5)
        ax.add_patch(rect)
    pass


if __name__ == "__main__":
    data = QA.QA_fetch_stock_day_adv('000001', '2019-01-01', '2019-11-01')
    bricks_fixed = QA.RENKOP(data.close, N=0.05).tolist()

    print(bricks_fixed)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plot_renko(ax, bricks_fixed)
    plt.title('RENKO {}'.format('600010'))
    plt.show()
