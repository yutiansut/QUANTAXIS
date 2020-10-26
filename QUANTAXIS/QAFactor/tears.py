import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
from typing import Union, Tuple, List

from QUANTAXIS.QAFactor import plotting
from QUANTAXIS.QAFactor import performance as perf
from QUANTAXIS.QAFactor import utils
from QUANTAXIS.QAFactor.plotting_utils import GridFigure, customize
from QUANTAXIS.QAFactor.process import get_clean_factor_and_forward_returns


@customize
def create_summary_tear_sheet(
        factor_data: pd.DataFrame,
        by_datetime: bool = True,  # 按日期计算
        by_group: bool = False,  # 按分组计算
        long_short: bool = True,  # 多空组合
        group_neutral: bool = False,  # 分组中性
        periods: Union[int, Tuple[int], List[int]] = 1,
        frequence: str = '1d'):
    """
    创建一个小型的汇总表格，包括因子的收益率分析，IC 值，换手率等分析

    参数
    ---
    :param factor_data: 因子数据
    :param long_short: 是否构建多空组合，在该组合上进行进行分析。
    :param group_neutral: 是否进行行业中性
    """
    if isinstance(periods, int):
        periods = [
            periods,
        ]
    # 收益分析
    mean_quant_ret, std_quant = perf.mean_return_by_quantile(
        factor_data,
        by_group=by_group,
        demeaned=long_short,
        group_adjust=group_neutral)
    mean_quant_rateret = mean_quant_ret.apply(
        utils.rate_of_return,
        axis=0,
        base_period=mean_quant_ret.columns[0]
    )
    std_quant_rate = std_quant.apply(
        utils.std_conversion,
        axis=0,
        base_period=std_quant.columns[0]
    )

    mean_quant_ret_bydatetime, std_quant_bydatetime = perf.mean_return_by_quantile(
        factor_data,
        by_datetime=by_datetime,
        by_group=by_group,
        demeaned=long_short,
        group_adjust=group_neutral)

    mean_quant_rateret_bydatetime = mean_quant_ret_bydatetime.apply(
        utils.rate_of_return,
        axis=0,
        base_period=mean_quant_ret_bydatetime.columns[0]
    )
    std_quant_rate_bydatetime = std_quant_bydatetime.apply(
        utils.std_conversion,
        axis=0,
        base_period=std_quant_bydatetime.columns[0]
    )

    alpha_beta = perf.factor_alpha_beta(
        factor_data=factor_data,
        demeaned=long_short,
        group_adjust=group_neutral
    )

    mean_ret_spread_quant, std_spread_quant = perf.mean_returns_spread(
        mean_quant_rateret,
        upper_quant=factor_data.factor_quantile.max(),
        lower_quant=factor_data.factor_quantile.min(),
        std_err=std_quant_rate)

    fr_cols = utils.get_forward_returns_columns(factor_data.columns)

    vertical_sections = 2 + len(fr_cols) * 3
    gf = GridFigure(rows=vertical_sections, cols=1)

    plotting.plot_quantile_statistics_table(factor_data)
    plotting.plot_returns_table(
        alpha_beta,
        mean_quant_rateret,
        mean_ret_spread_quant
    )
    plotting.plot_quantile_returns_bar(
        mean_quant_rateret,
        by_group=by_group,
        ylim_percentiles=None,
        ax=gf.next_row()
    )

    # Information Analysis
    ic = perf.factor_information_coefficient(factor_data)
    plotting.plot_information_table(ic)

    # Turnover Analysis
    # FIXME: 股票是 T+1，意味着频率只能是 Day 及以上频率
    quantile_factor = factor_data["factor_quantile"]
    quantile_turnover = {
        p: pd.concat(
            [
                perf.quantile_turnover(quantile_factor,
                                       q,
                                       p)
                for q in range(1,
                               int(quantile_factor.max()) + 1)
            ],
            axis=1,
        )
        for p in periods
    }
    autocorrelation = pd.concat(
        [
            perf.factor_rank_autocorrelation(factor_data,
                                             period) for period in periods
        ],
        axis=1,
    )

    plotting.plot_turnover_table(autocorrelation, quantile_turnover)

    plt.show()
    gf.close()
