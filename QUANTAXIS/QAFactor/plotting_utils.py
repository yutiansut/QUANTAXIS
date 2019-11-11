import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union
import pandas as pd
from IPython.display import display
from functools import wraps


class GridFigure:
    """
    使用网格视图
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.fig = plt.figure(figsize=(14, rows * 7))
        self.gs = gridspec.GridSpec(rows, cols, wspace=0.4, hspace=0.3)
        self.curr_row = 0
        self.curr_col = 0

    def next_row(self):
        if self.curr_col != 0:
            self.curr_row += 1
            self.curr_col = 0
        subplt = plt.subplot(self.gs[self.curr_row, :])
        self.curr_row += 1

    def next_cell(self):
        if self.curr_col >= self.cols:
            self.curr_row += 1
            self.curr_col = 0
        subplt = plt.subplot(self.gs[self.curr_row, self.curr_col])
        self.curr_col += 1
        return subplt

    def close(self):
        plt.close(self.fig)
        self.fig = None
        self.gs = None


def customize(func):
    """
    修饰器，设置输出图像内容与风格
    """

    @wraps(func)
    def call_w_context(*args, **kwargs):
        set_context = kwargs.pop("set_context", True)
        if set_context:
            color_palette = sns.color_palette("colorblind")
            with plotting_context(), axes_style(), color_palette:
                sns.despine(left=True)
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return call_w_context


def plotting_context(
    context: str = "notebook", font_scale: float = 1.5, rc: dict = None
):
    """
    创建默认画图板样式

    参数
    ---
    :param context: seaborn 样式
    :param font_scale: 设置字体大小
    :param rc: 配置标签
    """
    if rc is None:
        rc = {}

    rc_default = {"lines.linewidth": 1.5}

    # 如果没有默认设置，增加默认设置
    for name, val in rc_default.items():
        rc.setdefault(name, val)

    return sns.plotting_context(context=context, font_scale=font_scale, rc=rc)


def axes_style(style: str = "darkgrid", rc: dict = None):
    """
    创建默认轴域风格

    参数
    ---
    :param style: seaborn 样式
    :param rc: dict 配置标签
    """
    if rc is None:
        rc = {}

    rc_default = {}

    for name, val in rc_default.items():
        rc.set_default(name, val)

    return sns.axes_style(style=style, rc=rc)


def print_table(
    table: Union[pd.Series, pd.DataFrame], name: str = None, fmt: str = None
):
    """
    设置输出的 pandas DataFrame 格式

    参数
    ---
    :param table: 输入表格
    :param name: 表格列名设置
    :param fmt: 设置表格元素展示格式，譬如设置 '{0:.2f}%'，那么 100 展示出来就是 '100.00%'
    """
    if isinstance(table, pd.Series):
        table = pd.DataFrame(table)

    if isinstance(table, pd.DataFrame):
        table.columns.name = name

    prev_option = pd.get_option("display.float_format")
    if fmt is not None:
        pd.set_option("display.float_format", lambda x: fmt.format(x))

    display(table)

    # from alphalens, seems useless
    # if fmt is not None:
    #     pd.set_option("display.float_format", prev_option)
