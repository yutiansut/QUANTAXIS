
from QUANTAXIS_CRAWLY.jrj_simulation_web import get_financial_report_date

def QA_fetch_get_financial_calendar(report_date):
    data = get_financial_report_date(report_date)
    return(data)
