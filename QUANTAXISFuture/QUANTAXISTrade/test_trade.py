#coding:utf-8
from QA_trade_stock import QA_Stock


st = QA_Stock()
st.get_config()
client = st.QA_trade_stock_login()
st.QA_trade_stock_get_cash(client)
st.QA_trade_stock_get_stock(client)
st.QA_trade_stock_get_orders(client)
holder=st.QA_trade_stock_get_holder(client)
st.QA_trade_stock_get_quotes(client,['000001','601988'])