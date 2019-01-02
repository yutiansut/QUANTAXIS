
from QUANTAXIS_CRAWLY.jrj_divyield_simulation_web import get_stock_divyield

def QA_fetch_get_stock_divyield(report_date):
    data = get_stock_divyield(report_date)
    return(data)
