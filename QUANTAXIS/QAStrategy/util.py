import pandas as pd

def QA_data_futuremin_resample(min_data,  type_='5min'):
    """期货分钟线采样成大周期
    分钟线采样成子级别的分钟线
    future:
    vol ==> trade
    amount X
    """

    min_data.tradeime = pd.to_datetime(min_data.tradetime)

    CONVERSION = {'code': 'first', 'open': 'first', 'high': 'max', 'low': 'min',
                  'close': 'last', 'trade': 'sum', 'tradetime': 'last', 'date': 'last'}
    resx = min_data.resample(type_, closed='right',
                             loffset=type_).apply(CONVERSION)
    return resx.dropna().reset_index().set_index(['datetime', 'code'])