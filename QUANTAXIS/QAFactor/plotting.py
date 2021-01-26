"""
画图模块
"""

import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api
from matplotlib.ticker import ScalarFormatter
from scipy import stats

from QUANTAXIS.QAFactor import performance as perf
from QUANTAXIS.QAFactor import plotting_utils
from QUANTAXIS.QAFactor import utils
from QUANTAXIS.QAFactor.parameters import DECIMAL_TO_BPS
from QUANTAXIS.QAFactor.plotting_utils import GridFigure, customize


@customize
def create_summary_tear_sheet(
        factor_data: pd.DataFrame,
        long_short: bool = True,
        group_neutral: bool = False
):
    """

    """
    # Return Analysis
    mean_quant_ret, std_quantiles = perf.mean_return_by_quantile(
        factor_data,
        by_group=False,
        demeaned=long_short,
        group_adjust=group_neutral)

    mean_quant_rateret = mean_quant_ret.apply(
        utils.rate_of_return,
        axis=0,
        base_period=mean_quant_ret.columns[0]
    )

    mean_quant_ret_bydatetime, std_quant_bydatetime = perf.mean_return_by_quantile(
        factor_data,
        by_datetime=True,
        by_group=False,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    mean_quant_rateret_bydatetime = mean_quant_ret_bydatetime.apply(
        utils.rate_of_return,
        axis=0,
        base_period=mean_quant_ret_bydatetime.columns[0]
    )
    std_quant_bydatetime = std_quant_bydatetime.apply(
        utils.std_conversion,
        axis=0,
        base_period=std_quant_bydatetime.columns[0]
    )
    alpha_beta = perf.factor_alpha_beta(
        factor_data,
        demeaned=long_short,
        group_adjust=group_neutral
    )
    mean_ret_spread_quant, std_spread_quant = perf.mean_returns_spread(
        mean_quant_rateret_bydatetime,
        factor_data["factor_quantile"].max(),
        factor_data["factor_quantile"].min(),
        std_err=std_quant_bydatetime,
    )

    periods = utils.get_forward_returns_columns(factor_data.columns)

    fr_cols = len(periods)
    vertical_sections = 2 + fr_cols * 3
    gr = GridFigure(rows=vertical_sections, cols=1)

    plot_quantile_statistics_table(factor_data)
    plot_quantile_returns_bar(
        mean_quant_rateret,
        by_group=False,
        ylim_percentiles=None,
        ax=gf.next_row()
    )


def plot_returns_table(alpha_beta, mean_ret_quantile, mean_ret_spread_quantile):
    """
    打印因子收益表, 需要输入因子的 alpha, beta, 分位收益情况
    """
    returns_table = pd.DataFrame()
    returns_table = returns_table.append(alpha_beta)
    returns_table.loc["Mean Period Wise Return Top Quantile (bps)"] = (
        mean_ret_quantile.iloc[-1] * DECIMAL_TO_BPS
    )
    returns_table.loc["Mean Period Wise Return Bottom Quantile (bps)"] = (
        mean_ret_quantile.iloc[0] * DECIMAL_TO_BPS
    )
    returns_table.loc["Mean Period Wise Spread (bps)"] = (
        mean_ret_spread_quantile.mean() * DECIMAL_TO_BPS
    )

    print("Returns Analysis")
    plotting_utils.print_table(returns_table.apply(lambda x: x.round(3)))


def plot_quantile_returns_bar(
        mean_ret_by_q,
        by_group: bool = False,
        ylim_percentiles=None,
        ax=None
):
    mean_ret_by_q = mean_ret_by_q

    if ylim_percentiles is not None:
        ymin = np.nanpercentile(
            mean_ret_by_q.values,
            ylim_percentiles[0] * DECIMAL_TO_BPS
        )
        ymax = np.nanpercentile(
            mean_ret_by_q.values,
            ylim_percentiles[1] * DECIMAL_TO_BPS
        )
    else:
        ymin = None
        ymax = None

    if by_group:
        num_groups = len(mean_ret_by_q.index.get_level_values("group").unique())

        if ax is None:
            v_spaces = ((num_groups - 1) // 2) + 1
            f, ax = plt.subplots(v_spaces,
                                 2,
                                 sharex=False,
                                 sharey=True,
                                 figsize=(18, 6 * v_spaces))
            ax = ax.flatten()

        for a, (sc, cor) in zip(ax, mean_ret_by_q.groupby(level="group")):
            (
                cor.xs(sc,
                       level="group").multiply(DECIMAL_TO_BPS).plot(
                           kind="bar",
                           title=sc,
                           ax=a
                       )
            )

            a.set(xlabel="", ylabel="Mean Return (bps)", ylim=(ymin, ymax))

        if num_groups < len(ax):
            ax[-1].set_visible(False)

        return ax
    else:
        if ax is None:
            f, ax = plt.subplots(1, 1, figsize=(18, 6))

        (
            mean_ret_by_q.multiply(DECIMAL_TO_BPS).plot(
                kind="bar",
                title="Mean Period Wise Return By Factor Quantiles",
                ax=ax
            )
        )
        ax.set(xlabel="", ylabel="Mean Return (bps)", ylim=(ymin, ymax))

        return ax


def plot_quantile_statistics_table(
        factor_data: pd.DataFrame,
        by_group: bool = False
):
    """
    分位统计量
    """
    grouper = ["factor_quantile"]
    if by_group:
        grouper.append("group")
    quantile_stats = factor_data.groupby(grouper).agg(
        ["min",
         "max",
         "mean",
         "std",
         "count"]
    )["factor"]
    quantile_stats["count %"] = (
        quantile_stats["count"] / quantile_stats["count"].sum() * 100
    )

    print("Quantiles Statistics")
    plotting_utils.print_table(quantile_stats)


def plot_information_table(ic_data):
    """
    IC 统计量
    """
    ic_summary_table = pd.DataFrame()
    ic_summary_table["IC Mean"] = ic_data.mean()
    ic_summary_table["IC std."] = ic_data.std()
    ic_summary_table["Risk-Adjusted IC (IR)"] = ic_data.mean() / ic_data.std()
    t_stat, p_value = stats.ttest_1samp(ic_data, 0)
    ic_summary_table["t-stat (IC)"] = t_stat
    ic_summary_table["p-value (IC)"] = p_value
    ic_summary_table["IC Skew"] = stats.skew(ic_data)
    ic_summary_table["IC Kurtosis"] = stats.kurtosis(ic_data)

    print("Information Analysis")
    plotting_utils.print_table(ic_summary_table.apply(lambda x: x.round(3)).T)


def plot_turnover_table(autocorrelation_data, quantile_turnover):
    turnover_table = pd.DataFrame()
    for period in sorted(quantile_turnover.keys()):
        for quantile, p_data in quantile_turnover[period].iteritems():
            turnover_table.loc[f"Quantile {quantile} Mean Turnover",
                               f"{period}"] = p_data.mean()

    auto_corr = pd.DataFrame()
    for period, p_data in autocorrelation_data.iteritems():
        auto_corr.loc["Mean Factor Rank Autocorrelation",
                      f"{period}"] = p_data.mean()

    print("Turnover Analysis")
    plotting_utils.print_table(turnover_table.apply(lambda x: x.round(3)))
    plotting_utils.print_table(auto_corr.apply(lambda x: x.round(3)))


def plot_quantile_returns_violin(return_by_q, ylim_percentiles=None, ax=None):
    return_by_q = return_by_q.copy()

    if ylim_percentiles is not None:
        ymin = (
            np.nanpercentile(return_by_q.values,
                             ylim_percentiles[0]) * DECIMAL_TO_BPS
        )
        ymax = (
            np.nanpercentile(return_by_q.values,
                             ylim_percentiles[1]) * DECIMAL_TO_BPS
        )
    else:
        ymin = None
        ymax = None

    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))

    unstacked_dr = return_by_q.multiply(DECIMAL_TO_BPS)
    unstacked_dr.columns = unstacked_dr.columns.set_names("forward_periods")
    unstacked_dr = unstacked_dr.stack()
    unstacked_dr.name = "return"
    unstacked_dr = unstacked_dr.reset_index()

    sns.violinplot(
        data=unstacked_dr,
        x="factor_quantile",
        hue="forward_periods",
        y="return",
        orient="v",
        cut=0,
        inner="quartile",
        ax=ax,
    )
    ax.set(
        xlabel="",
        ylabel="Return (bps)",
        title="Period Wise Return By Factor Quantile",
        ylim=(ymin,
              ymax),
    )

    ax.axhline(0.0, linestyle="-", color="black", lw=0.7, alpha=0.6)

    return ax


def plot_cumulative_returns(
        factor_returns: pd.DataFrame,
        period,
        freq,
        title=None,
        ax=None
):
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(18, 6))

    factor_returns = perf.cumulative_returns(
        returns=factor_returns,
        period=period,
    )
    pass
