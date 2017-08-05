# coding


# TODO
# 集成funcat
import numpy as np
import six
# ATR


def ATR(security_list, timeperiod=14):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 ATR
    atr = {}
    for stock in security_list:
        security_data = attribute_history(
            stock, timeperiod * 2, '1d', ['close', 'high', 'low'], df=False)
        nan_count = list(np.isnan(security_data['close'])).count(True)
        if nan_count == len(security_data['close']):

            atr[stock] = np.array([np.nan])
        else:
            close_ATR = security_data['close']
            high_ATR = security_data['high']
            low_ATR = security_data['low']
            atr[stock] = talib.ATR(high_ATR, low_ATR, close_ATR, timeperiod)
    return atr


def df_to_sarray(df):
    """
    Convert a pandas DataFrame object to a numpy structured array.
    This is functionally equivalent to but more efficient than
    np.array(df.to_array())

    :param df: the data frame to convert
    :return: a numpy structured array representation of df
    """

    v = df.values
    cols = df.columns

    if six.PY2:  # python 2 needs .encode() but 3 does not
        types = [(cols[i].encode(), df[k].dtype.type)
                 for (i, k) in enumerate(cols)]
    else:
        types = [(cols[i], df[k].dtype.type) for (i, k) in enumerate(cols)]
    dtype = np.dtype(types)
    z = np.zeros(v.shape[0], dtype)
    for (i, k) in enumerate(z.dtype.names):
        z[k] = v[:, i]
    return z


def RSI_CN(close, timeperiod):
    '''
    依赖库：
        import talib as tl
    参数：
        close: 股票收盘价list
    范例：
        rsiValue = RSI_CN(close, 13) 
    '''
    diff = map(lambda x, y: x - y, close[1:], close[:-1])
    diffGt0 = map(lambda x: 0 if x < 0 else x, diff)
    diffABS = map(lambda x: abs(x), diff)
    diff = np.array(diff)
    diffGt0 = np.array(diffGt0)
    diffABS = np.array(diffABS)
    diff = np.append(diff[0], diff)
    diffGt0 = np.append(diffGt0[0], diffGt0)
    diffABS = np.append(diffABS[0], diffABS)
    rsi = map(lambda x: SMA_CN(diffGt0[:x], timeperiod) / SMA_CN(
        diffABS[:x], timeperiod) * 100, range(1, len(diffGt0) + 1))

    return np.array(rsi)


def MTM(security_list, timeperiod=13):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 MFI
    mtm = {}
    for stock in security_list:
        security_data = attribute_history(
            stock, timeperiod, '1d', ['close'], df=False)
        nan_count = list(np.isnan(security_data['close'])).count(True)
        if nan_count == len(security_data['close']):
            
            mtm[stock] = np.array([np.nan])
        else:
            close_MTM = security_data['close']
            mtm[stock] = close_MTM[-1] - close_MTM[-timeperiod]
    return mtm
