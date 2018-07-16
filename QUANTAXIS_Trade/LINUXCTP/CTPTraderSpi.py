import logging
import threading
import typing

import PyCTP

from Event import DirectionType, ActionType, SignalType
from DataStruct import DataStruct


class CTPTraderSpi(PyCTP.CThostFtdcTraderSpi):
    TIME_OUT = 5

    def __init__(
            self, _con_path: bytes,
            _front_addr: bytes,
            _broker_id: bytes,
            _user_id: bytes,
            _passwd: bytes,
    ):
        super().__init__()

        if not _con_path.endswith(b'/'):
            _con_path += b'/'
        self.con_path = _con_path
        self.front_addr = _front_addr
        self.broker_id = _broker_id
        self.user_id = _user_id
        self.passwd = _passwd

        self.front_id = None
        self.session_id = None

        self.request_id = 1
        self.order_id = 1

        self.event = threading.Event()  # lock for threading
        self.ret_data: typing.Any = None  # buf for return data

        self.api: PyCTP.CThostFtdcTraderApi = \
            PyCTP.CThostFtdcTraderApi.CreateFtdcTraderApi(
                self.con_path
            )
        self.api.RegisterSpi(self)

    def Release(self):
        self.api.RegisterSpi(None)
        self.api.Release()

    def incRequestID(self):
        tmp = self.request_id
        self.request_id += 1
        return tmp

    def getRequestID(self):
        return self.request_id

    def incOrderID(self):
        tmp = self.order_id
        self.order_id += 1
        return tmp

    def getOrderID(self):
        return self.order_id

    def eventClear(self):
        self.event.clear()

    def eventWait(self, _sec: int):
        if self.event.wait(_sec):
            return True
        else:
            logging.warning('{} sec TIMEOUT!'.format(_sec))
            return False

    def eventSet(self):
        self.event.set()

    def Connect(self) -> bool:
        self.eventClear()

        logging.info('connect front TRY!')
        self.api.RegisterFront(self.front_addr)
        self.api.Init()
        self.api.SubscribePrivateTopic(PyCTP.THOST_TERT_QUICK)
        self.api.SubscribePublicTopic(PyCTP.THOST_TERT_QUICK)

        return self.eventWait(self.TIME_OUT)

    def OnFrontConnected(self):
        logging.info('connect front DONE!')
        self.eventSet()

    def OnFrontDisconnected(self, _reason: int):
        logging.warning('disconnect front ({})'.format(_reason))

    def ReqUserLogin(self) -> bool:
        req = PyCTP.CThostFtdcReqUserLoginField()
        req.BrokerID = self.broker_id
        req.UserID = self.user_id
        req.Password = self.passwd

        self.eventClear()
        logging.info('login TRY!')
        if self.api.ReqUserLogin(req, self.incRequestID()):
            logging.error('login FAILED!')
            return False

        return self.eventWait(self.TIME_OUT)

    def OnRspUserLogin(
            self, _user_login: PyCTP.CThostFtdcRspUserLoginField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        if _is_last:
            self.front_id = _user_login.FrontID
            self.session_id = _user_login.SessionID
            try:
                self.order_id = int(_user_login.MaxOrderRef)
            except ValueError as e:
                logging.warning(e)
            logging.info('FrontID: {}, SessionID: {}, OrderID: {}'.format(
                self.front_id, self.session_id, self.order_id
            ))
            logging.info('login {} DONE!'.format(
                _rsp_info.ErrorMsg.decode('gb2312')
            ))
            self.eventSet()

    def GetTradingDay(self):
        return self.api.GetTradingDay()

    def ReqUserLogout(self) -> bool:
        req = PyCTP.CThostFtdcUserLogoutField()
        req.BrokerID = self.broker_id
        req.UserID = self.user_id

        self.eventClear()
        logging.info('logout TRY!')
        if self.api.ReqUserLogout(req, self.incRequestID()):
            logging.error('logout FAILED!')
            return False

        return self.eventWait(self.TIME_OUT)

    def OnRspUserLogout(
            self, _user_logout: PyCTP.CThostFtdcUserLogoutField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        if _is_last:
            logging.info('logout DONE!')
            self.eventSet()

    def ReqQryInstrument(self) -> typing.Union[bool, DataStruct]:
        qry = PyCTP.CThostFtdcQryInstrumentField()
        qry.ExchangeID = b''
        qry.InstrumentID = b''

        self.eventClear()
        self.ret_data = DataStruct([
            'InstrumentID', 'ProductID', 'VolumeMultiple', 'PriceTick',
            'DeliveryYear', 'DeliveryMonth'
        ], 'InstrumentID')
        logging.info('instrument TRY!')
        if self.api.ReqQryInstrument(qry, self.incRequestID()):
            logging.error('instrument FAILED!')
            return False

        ret = self.eventWait(self.TIME_OUT * 5)
        if ret is False:
            return False
        return self.ret_data

    def OnRspQryInstrument(
            self,
            _instrument: PyCTP.CThostFtdcInstrumentField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        symbol: str = _instrument.InstrumentID.decode('gb2312')
        if len(symbol) <= 6 and not symbol.endswith('efp'):
            self.ret_data.addDict({
                'InstrumentID': symbol,
                'ProductID': _instrument.ProductID.decode('gb2312'),
                'VolumeMultiple': _instrument.VolumeMultiple,
                'PriceTick': _instrument.PriceTick,
                'DeliveryYear': _instrument.DeliveryYear,
                'DeliveryMonth': _instrument.DeliveryMonth,
            })
        if _is_last:
            logging.info('instrument DONE! (total: {})'.format(
                len(self.ret_data)
            ))
            self.eventSet()

    def ReqQrySettlementInfo(
            self, _tradingday: bytes = b''
    ) -> typing.Union[bool, bytes]:
        req = PyCTP.CThostFtdcQrySettlementInfoField()
        req.BrokerID = self.broker_id
        req.InvestorID = self.user_id
        req.TradingDay = _tradingday

        self.eventClear()
        self.ret_data = b''
        logging.info('qry settlement info TRY!')
        if self.api.ReqQrySettlementInfo(req, self.incRequestID()):
            logging.info('qry settlement info FAILED!')
            return False

        ret = self.eventWait(self.TIME_OUT)
        if ret is False:
            return False
        return self.ret_data

    def OnRspQrySettlementInfo(
            self, _settlement_info: PyCTP.CThostFtdcSettlementInfoField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        self.ret_data += _settlement_info.Content
        if _is_last:
            logging.info('qry settlement info DONE!')
            self.eventSet()

    def ReqSettlementInfoConfirm(self) -> bool:
        req = PyCTP.CThostFtdcSettlementInfoConfirmField()
        req.BrokerID = self.broker_id
        req.InvestorID = self.user_id

        self.eventClear()
        logging.info('qry settlement info confirm TRY!')
        if self.api.ReqSettlementInfoConfirm(req, self.incRequestID()):
            logging.info('qry settlement info confirm FAILED!')
            return False

        return self.eventWait(self.TIME_OUT)

    def OnRspSettlementInfoConfirm(
            self,
            _confirm: PyCTP.CThostFtdcSettlementInfoConfirmField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        if _is_last:
            logging.info('qry settlement info confirm DONE!')
            self.eventSet()

    def ReqQryInvestorPosition(self) -> typing.Union[bool, DataStruct]:
        req = PyCTP.CThostFtdcQryInvestorPositionField()
        req.BrokerID = self.broker_id
        req.InvestorID = self.user_id

        self.eventClear()
        self.ret_data = DataStruct([
            'InstrumentID', 'Signal', 'Position',
            'PositionProfit', 'CloseProfit', 'Commission',
            'TradingDay'
        ], 'InstrumentID')
        logging.info('qry investor position TRY!')
        if self.api.ReqQryInvestorPosition(req, self.incRequestID()):
            logging.error('qry investor position FAILED!')
            return False

        ret = self.eventWait(self.TIME_OUT)
        if ret is False:
            return False
        return self.ret_data

    def OnRspQryInvestorPosition(
            self,
            _investor_position: PyCTP.CThostFtdcInvestorPositionField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        if _investor_position is not None:
            instrument = _investor_position.InstrumentID.decode('gb2312')
            signal = SignalType.EMPTY
            if _investor_position.PosiDirection == PyCTP.THOST_FTDC_PD_Long:
                signal = SignalType.LONG
            elif _investor_position.PosiDirection == PyCTP.THOST_FTDC_PD_Short:
                signal = SignalType.SHORT
            else:
                logging.error('Instrument:{}, PosiDirection: {}'.format(
                    instrument, _investor_position.PosiDirection,
                ))

            self.ret_data.addDict({
                'InstrumentID': instrument,
                'Signal': signal,
                'Position': _investor_position.Position,
                'PositionProfit': _investor_position.PositionProfit,
                'CloseProfit': _investor_position.CloseProfit,
                'Commission': _investor_position.Commission,
                'TradingDay': _investor_position.TradingDay.decode('gb2312'),
            })

        if _is_last:
            logging.info('qry investor position DONE! (total: {})'.format(
                len(self.ret_data)
            ))
            self.eventSet()

    def ReqQryDepthMarketData(self, _instrument_id: bytes):
        req = PyCTP.CThostFtdcQryDepthMarketDataField()
        req.InstrumentID = _instrument_id

        self.eventClear()
        self.ret_data = None
        logging.info('qry {} market TRY!'.format(_instrument_id))
        if self.api.ReqQryDepthMarketData(req, self.incRequestID()):
            logging.error('qry {} market FAILED!'.format(_instrument_id))
            return False

        ret = self.eventWait(self.TIME_OUT)
        if ret is False:
            return False
        return self.ret_data

    def OnRspQryDepthMarketData(
            self,
            _depth_market_data: PyCTP.CThostFtdcDepthMarketDataField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        self.ret_data = {
            'InstrumentID': _depth_market_data.InstrumentID.decode('gb2312'),
            'TradingDay': _depth_market_data.TradingDay.decode('gb2312'),
            'ActionDay': _depth_market_data.ActionDay.decode('gb2312'),
            'UpdateTime': _depth_market_data.UpdateTime.decode('gb2312'),
            'UpdateMillisec': _depth_market_data.UpdateMillisec,
            'LastPrice': _depth_market_data.LastPrice,
            'HighestPrice': _depth_market_data.HighestPrice,
            'LowestPrice': _depth_market_data.LowestPrice,
            'Volume': _depth_market_data.Volume,
            'Turnover': _depth_market_data.Turnover,
            'OpenInterest': _depth_market_data.OpenInterest,
            'AskPrice': _depth_market_data.AskPrice1,
            'AskVolume': _depth_market_data.AskVolume1,
            'BidPrice': _depth_market_data.BidPrice1,
            'BidVolume': _depth_market_data.BidVolume1,
        }

        if _is_last:
            logging.info('qry {} market DONE!'.format(
                _depth_market_data.InstrumentID
            ))
            self.eventSet()

    def ReqOrderInsert(
            self, _instrument: bytes, _direction: int,
            _action: int, _volume: int, _price: float,
            _today: bool = False
    ) -> typing.Union[bool, dict]:

        req = PyCTP.CThostFtdcInputOrderField()
        # trader info
        req.BrokerID = self.broker_id
        req.InvestorID = self.user_id
        # instrument and order ref
        req.InstrumentID = _instrument
        req.OrderRef = '{}'.format(self.incOrderID()).encode()
        # set direction
        if _direction == DirectionType.BUY:
            req.Direction = PyCTP.THOST_FTDC_D_Buy
        elif _direction == DirectionType.SELL:
            req.Direction = PyCTP.THOST_FTDC_D_Sell
        else:
            logging.error('unknown direction!')
            return False
        # set action
        if _action == ActionType.OPEN:
            req.CombOffsetFlag = PyCTP.THOST_FTDC_OF_Open
        elif _action == ActionType.CLOSE:
            if _today:
                req.CombOffsetFlag = PyCTP.THOST_FTDC_OF_CloseToday
            else:
                req.CombOffsetFlag = PyCTP.THOST_FTDC_OF_CloseYesterday
        else:
            logging.error('unknown action!')
            return False

        # common config
        req.CombHedgeFlag = PyCTP.THOST_FTDC_HF_Speculation
        req.ContingentCondition = PyCTP.THOST_FTDC_CC_Immediately
        req.ForceCloseReason = PyCTP.THOST_FTDC_FCC_NotForceClose
        req.IsAutoSuspend = 0
        req.UserForceClose = 0

        # limit, fill or kill
        req.VolumeTotalOriginal = _volume
        req.OrderPriceType = PyCTP.THOST_FTDC_OPT_LimitPrice
        req.LimitPrice = _price
        req.TimeCondition = PyCTP.THOST_FTDC_TC_IOC
        req.VolumeCondition = PyCTP.THOST_FTDC_VC_MV
        req.MinVolume = _volume

        self.eventClear()
        self.ret_data = False
        logging.info('order insert TRY!')
        if self.api.ReqOrderInsert(req, self.incRequestID()):
            logging.info('order insert FAILED!')
            return False

        ret = self.eventWait(self.TIME_OUT)
        if ret is False:
            return False
        return self.ret_data

    def OnRspOrderInsert(
            self,
            _input_order: PyCTP.CThostFtdcInputOrderField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        logging.info('ErrorID: {}, Msg: {}'.format(
            _rsp_info.ErrorID, _rsp_info.ErrorMsg.decode('gb2312')
        ))
        if _is_last:
            self.eventSet()

    def OnErrRtnOrderInsert(
            self,
            _input_order: PyCTP.CThostFtdcInputOrderField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
    ):
        logging.info('ErrorID: {}, Msg: {}'.format(
            _rsp_info.ErrorID, _rsp_info.ErrorMsg.decode('gb2312')
        ))
        self.eventSet()

    def OnRtnOrder(self, _order: PyCTP.CThostFtdcOrderField):
        if _order.SessionID != self.session_id:
            # skip order from session
            return
        status = _order.OrderStatus
        logging.info('OrderRef: {}, OrderStatus: {}, Msg: {}'.format(
            _order.OrderRef, status, _order.StatusMsg.decode('gb2312')
        ))
        if status == PyCTP.THOST_FTDC_OST_Canceled:
            self.ret_data = False
            self.eventSet()
        else:
            # keep waiting
            pass

    def OnRtnTrade(self, _trade: PyCTP.CThostFtdcTradeField):
        self.ret_data = {
            'TradingDay': _trade.TradingDay.decode('gb2312'),
            'TradeDate': _trade.TradeDate.decode('gb2312'),
            'TradeTime': _trade.TradeTime.decode('gb2312'),
            'OrderRef': int(_trade.OrderRef),
            'InstrumentID': _trade.InstrumentID.decode('gb2312'),
            'Direction': _trade.Direction,
            'Action': _trade.OffsetFlag,
            'Price': _trade.Price,
            'Volume': _trade.Volume,
        }
        logging.info('order insert DONE!')
        self.eventSet()

    def ReqQryOrder(self) -> typing.Union[bool, DataStruct]:
        req = PyCTP.CThostFtdcQryOrderField()
        req.BrokerID = self.broker_id
        req.InvestorID = self.user_id

        self.eventClear()
        self.ret_data = DataStruct([
            'OrderRef', 'OrderSysID', 'OrderStatus', 'InstrumentID',
            'Direction', 'Action', 'Price', 'Volume',
            'FrontID', 'SessionID',
            'TradingDay', 'InsertDate', 'InsertTime'
        ], 'OrderRef')
        logging.info('qry order TRY!')
        if self.api.ReqQryOrder(req, self.incRequestID()):
            logging.error('qry order FAILED!')
            return False

        ret = self.eventWait(self.TIME_OUT)
        if ret is False:
            return False
        return self.ret_data

    def OnRspQryOrder(
            self, _order: PyCTP.CThostFtdcOrderField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        if _order is not None:
            self.ret_data.addDict({
                'OrderRef': int(_order.OrderRef),
                'OrderSysID': _order.OrderSysID,
                'OrderStatus': _order.OrderStatus,
                'InstrumentID': _order.InstrumentID.decode('gb2312'),
                'Direction': _order.Direction,
                'Action': _order.CombOffsetFlag,
                'Price': _order.LimitPrice,
                'Volume': _order.VolumeTotalOriginal,
                'FrontID': _order.FrontID,
                'SessionID': _order.SessionID,
                'TradingDay': _order.TradingDay.decode('gb2312'),
                'InsertDate': _order.InsertDate.decode('gb2312'),
                'InsertTime': _order.InsertTime.decode('gb2312'),
            })

        if _is_last:
            logging.info('qry order DONE! (total: {})'.format(
                len(self.ret_data)
            ))
            self.eventSet()

    def ReqQryTrade(self) -> typing.Union[bool, DataStruct]:
        req = PyCTP.CThostFtdcQryTradeField()
        req.BrokerID = self.broker_id
        req.InvestorID = self.user_id

        self.eventClear()
        self.ret_data = DataStruct([
            'TradingDay', 'TradeDate', 'TradeTime',
            'OrderRef', 'InstrumentID',
            'Direction', 'Action', 'Price', 'Volume'
        ], 'OrderRef')
        logging.info('qry trade TRY!')
        if self.api.ReqQryTrade(req, self.incRequestID()):
            logging.error('qry trade FAILED!')
            return False

        ret = self.eventWait(self.TIME_OUT)
        if ret is False:
            return False
        return self.ret_data

    def OnRspQryTrade(
            self, _trade: PyCTP.CThostFtdcTradeField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        if _trade is not None:
            self.ret_data.addDict({
                'TradingDay': _trade.TradingDay.decode('gb2312'),
                'TradeDate': _trade.TradeDate.decode('gb2312'),
                'TradeTime': _trade.TradeTime.decode('gb2312'),
                'OrderRef': int(_trade.OrderRef),
                'InstrumentID': _trade.InstrumentID.decode('gb2312'),
                'Direction': _trade.Direction,
                'Action': _trade.OffsetFlag,
                'Price': _trade.Price,
                'Volume': _trade.Volume,
            })

        if _is_last:
            logging.info('qry trade DONE! (total: {})'.format(
                len(self.ret_data)
            ))
            self.eventSet()

    def ReqQryTradingAccount(self) -> typing.Union[bool, dict]:
        req = PyCTP.CThostFtdcQryTradingAccountField()
        req.BrokerID = self.broker_id
        req.InvestorID = self.user_id

        self.eventClear()
        logging.info('qry trading account TRY!')
        if self.api.ReqQryTradingAccount(req, self.incRequestID()):
            logging.error('qry trade FAILED!')
            return False

        ret = self.eventWait(self.TIME_OUT)
        if ret is False:
            return False
        return self.ret_data

    def OnRspQryTradingAccount(
            self,
            _trading_account: PyCTP.CThostFtdcTradingAccountField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        self.ret_data = {
            'TradingDay': _trading_account.TradingDay.decode('gb2312'),
            'PreBalance': _trading_account.PreBalance,
            'PreMargin': _trading_account.PreMargin,
            'CloseProfit': _trading_account.CloseProfit,
            'PositionProfit': _trading_account.PositionProfit,
            'Commission': _trading_account.Commission,
            'CurrMargin': _trading_account.CurrMargin,
            'Available': _trading_account.Available,

        }
        if _is_last:
            logging.info('qry trading account DONE!')
            self.eventSet()

    def ReqQryInstrumentCommissionRate(
            self, _instrument_id: bytes
    ) -> typing.Union[bool, dict]:
        req = PyCTP.CThostFtdcQryInstrumentCommissionRateField()
        req.BrokerID = self.broker_id
        req.InvestorID = self.user_id
        req.InstrumentID = _instrument_id

        self.eventClear()
        logging.info('qry commission rate({}) TRY!'.format(_instrument_id))
        if self.api.ReqQryInstrumentCommissionRate(req, self.incRequestID()):
            logging.error('qry commission rate FAILED!')
            return False

        ret = self.eventWait(self.TIME_OUT)
        if ret is False:
            return False
        return self.ret_data

    def OnRspQryInstrumentCommissionRate(
            self,
            _rate: PyCTP.CThostFtdcInstrumentCommissionRateField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        instrument = _rate.InstrumentID.decode('gb2312')
        self.ret_data = {
            'InstrumentID': instrument,
            'OpenRatioByMoney': _rate.OpenRatioByMoney,
            'OpenRatioByVolume': _rate.OpenRatioByVolume,
            'CloseRatioByMoney': _rate.CloseRatioByMoney,
            'CloseRatioByVolume': _rate.CloseRatioByVolume,
            'CloseTodayRatioByMoney': _rate.CloseTodayRatioByMoney,
            'CloseTodayRatioByVolume': _rate.CloseTodayRatioByVolume,
        }
        if _is_last:
            logging.info('qry commission rate({}) DONE'.format(instrument))
            self.eventSet()

    def ReqOrderAction(self, 
                        _instrument_id: bytes,
                        _orderref: bytes, 
                        _ordersysid:bytes,
                        _exchangeid:bytes ) -> typing.Union[bool, dict]:

        req = PyCTP.CThostFtdcInputOrderActionField()
        
        req.InstrumentID = _instrument_id
        req.OrderRef = _orderref
        req.OrderSysID = _ordersysid
        req.ExchangeID = _exchangeid
        
        req.BrokerID = self.broker_id
        req.InvestorID = self.user_id
        req.FrontID = self.front_id
        req.ActionFlag = PyCTP.THOST_FTDC_AF_Delete

        self.eventClear()
        self.ret_data = False
        logging.info('order cancel TRY!')
        if self.api.ReqOrderAction(req, self.incRequestID()):
            logging.info('order cancel FAILED!')
            return False

        ret = self.eventWait(self.TIME_OUT)
        if ret is False:
            return False
        return self.ret_data

    def OnRspOrderAction(self,_OrderAction: PyCTP.CThostFtdcOrderActionField,
                            _rsp_info: PyCTP.CThostFtdcRspInfoField,
                            _request_id: int, _is_last: bool
                            ):
        
        self.ret_data = {
                'OrderRef': int(_OrderAction.OrderRef),
                'OrderSysID': _OrderAction.OrderSysID,
                'InstrumentID': _OrderAction.InstrumentID.decode('gb2312'),
                'OrderActionRef': _OrderAction.OrderActionRef,
                'Action': _OrderAction.ActionFlag,
                'Price': _OrderAction.LimitPrice,
                'Volume': _OrderAction.VolumeChange,
                'FrontID': _OrderAction.FrontID,
                'SessionID': _OrderAction.SessionID,
                'ActionDate': _OrderAction.ActionDate.decode('gb2312'),
                'ActionTime': _OrderAction.ActionTime.decode('gb2312'),
        }
        if _is_last:
            logging.info('cancel order DONE!')
            self.eventSet()
