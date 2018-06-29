import logging
import threading

import PyCTP


class CTPMarketSpi(PyCTP.CThostFtdcMdSpi):
    TIME_OUT = 5
    SUB_LIMIT = 500

    def __init__(
            self, _con_path: bytes,
            _front_addr: bytes,
            _broker_id: bytes,
            _user_id: bytes,
            _passwd: bytes,
            _callback
    ):
        super().__init__()

        if not _con_path.endswith(b'/'):
            _con_path += b'/'
        self.con_path = _con_path
        self.front_addr = _front_addr
        self.broker_id = _broker_id
        self.user_id = _user_id
        self.passwd = _passwd
        self.callback = _callback

        self.request_id = 1

        self.event = threading.Event()
        self.ret_data = None

        self.api: PyCTP.CThostFtdcMdApi = \
            PyCTP.CThostFtdcMdApi.CreateFtdcMdApi(
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
            logging.info('login {} DONE!'.format(
                _rsp_info.ErrorMsg.decode('gb2312')
            ))
            self.eventSet()

    def SubscribeMarketData(self, _instrument_list):
        assert len(_instrument_list) <= self.SUB_LIMIT
        self.eventClear()
        self.ret_data = set()
        logging.info('subscribe({}) TRY!'.format(
            len(_instrument_list))
        )
        if self.api.SubscribeMarketData(_instrument_list):
            logging.error('subscribe FAILED!')
            return False

        ret = self.eventWait(self.TIME_OUT)
        if ret is False:
            return ret
        return self.ret_data

    def OnRspSubMarketData(
            self,
            _spec_instrument: PyCTP.CThostFtdcSpecificInstrumentField,
            _rsp_info: PyCTP.CThostFtdcRspInfoField,
            _request_id: int, _is_last: bool
    ):
        logging.debug('subscribe {}'.format(
            _spec_instrument.InstrumentID
        ))
        self.ret_data.add(
            _spec_instrument.InstrumentID.decode('gb2312')
        )
        if _is_last:
            logging.info('subscribe({}) DONE!'.format(len(self.ret_data)))
            self.eventSet()

    def OnRtnDepthMarketData(
            self,
            _depth_market_data: PyCTP.CThostFtdcDepthMarketDataField,
    ):
        self.callback(_depth_market_data)