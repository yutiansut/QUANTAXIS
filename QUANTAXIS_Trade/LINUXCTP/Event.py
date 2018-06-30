import typing
from datetime import datetime

from DataStruct import DataStruct


class EventType:
    MARKET = 1
    SIGNAL = 2
    ORDER = 3
    FILL = 4
    SETTLEMENT = 5

    @staticmethod
    def toStr(_value: int) -> str:
        if _value == EventType.MARKET:
            return 'MARKET'
        elif _value == EventType.SIGNAL:
            return 'SIGNAL'
        elif _value == EventType.ORDER:
            return 'ORDER'
        elif _value == EventType.FILL:
            return 'FILL'
        elif _value == EventType.SETTLEMENT:
            return 'SETTLEMENT'
        else:
            raise Exception('unknown event type')


class SignalType:
    LONG = 1
    SHORT = 2
    EMPTY = 3

    @staticmethod
    def toStr(_value: int) -> str:
        if _value == SignalType.LONG:
            return 'LONG'
        elif _value == SignalType.SHORT:
            return 'SHORT'
        elif _value == SignalType.EMPTY:
            return 'EMPTY'
        else:
            raise Exception('unknown signal type')

    @staticmethod
    def fromStr(_value: str) -> int:
        if _value == 'LONG':
            return SignalType.LONG
        elif _value == 'SHORT':
            return SignalType.SHORT
        elif _value == 'EMPTY':
            return SignalType.EMPTY
        else:
            raise Exception('unknown signal type')


class OrderType:
    MARKET = 1
    LIMIT = 2

    @staticmethod
    def toStr(_value: int) -> str:
        if _value == OrderType.MARKET:
            return 'MARKET'
        elif _value == OrderType.LIMIT:
            return 'LIMIT'
        else:
            raise Exception()

    @staticmethod
    def fromStr(_value: str) -> int:
        if _value == 'MARKET':
            return OrderType.MARKET
        elif _value == 'LIMIT':
            return OrderType.LIMIT
        else:
            raise Exception()


class ActionType:
    OPEN = 1
    CLOSE = 2

    @staticmethod
    def toStr(_value: int) -> str:
        if _value == ActionType.OPEN:
            return 'OPEN'
        elif _value == ActionType.CLOSE:
            return 'CLOSE'
        else:
            raise Exception()

    @staticmethod
    def fromStr(_value: str) -> int:
        if _value == 'OPEN':
            return ActionType.OPEN
        elif _value == 'CLOSE':
            return ActionType.CLOSE
        else:
            raise Exception()


class DirectionType:
    BUY = 1
    SELL = 2

    @staticmethod
    def toStr(_value: int) -> str:
        if _value == DirectionType.BUY:
            return 'BUY'
        elif _value == DirectionType.SELL:
            return 'SELL'
        else:
            raise Exception()

    @staticmethod
    def fromStr(_value: str) -> int:
        if _value == 'BUY':
            return DirectionType.BUY
        elif _value == 'SELL':
            return DirectionType.SELL
        else:
            raise Exception()


class EventAbstract:
    def __init__(self):
        self.type = None

    def toDict(self) -> dict:
        raise NotImplementedError('toDict not implemented')


class MarketEvent(EventAbstract):
    def __init__(
            self,
            _market_register_key: str,
            _strategy: str,
            _symbol: str,
            _data: typing.Union[None, DataStruct] = None
    ):
        super().__init__()
        self.type = EventType.MARKET
        self.market_register_key = _market_register_key
        self.strategy = _strategy
        self.symbol = _symbol
        self.data = _data

    def toDict(self) -> dict:
        return {
            'type': self.type,
            'market_register_key': self.market_register_key,
            'strategy': self.strategy,
            'symbol': self.symbol,
        }

    @staticmethod
    def fromDict(_dict: dict) -> 'MarketEvent':
        return MarketEvent(
            _market_register_key=_dict['market_register_key'],
            _strategy=_dict['strategy'],
            _symbol=_dict['symbol'],
            _data=None
        )

    def __repr__(self):
        tmp = 'MARKET:\n' \
              '\tkey: {}\n' \
              '\tstrategy: {}\n' \
              '\tsymbol: {}'
        return tmp.format(
            self.market_register_key,
            self.strategy, self.symbol
        )


class SignalEvent(EventAbstract):
    def __init__(
            self,
            _symbol: str,
            _strategy: str,
            _signal_type: int,
            _tradingday: str,
            _datetime: typing.Union[str, datetime],
            _strength: typing.Any = None
    ):
        super().__init__()
        self.type = EventType.SIGNAL
        self.symbol = _symbol
        self.strategy = _strategy
        self.signal_type = _signal_type
        self.tradingday = _tradingday
        self.datetime = _datetime
        self.strength = _strength

    def toDict(self) -> dict:
        return {
            'type': self.type,
            'symbol': self.symbol,
            'strategy': self.strategy,
            'signal_type': self.signal_type,
            'tradingday': self.tradingday,
            'datetime': self.datetime,
            'strength': self.strength
        }

    @staticmethod
    def fromDict(_dict: dict) -> 'SignalEvent':
        return SignalEvent(
            _symbol=_dict['symbol'],
            _strategy=_dict['strategy'],
            _signal_type=_dict['signal_type'],
            _tradingday=_dict['tradingday'],
            _datetime=_dict['datetime'],
            _strength=_dict['strength'])

    def __repr__(self):
        tmp = 'SIGNAL:\n' \
              '\tsymbol: {}\n' \
              '\tstrategy: {}\n' \
              '\tsignal: {}\n' \
              '\ttradingday: {}\n' \
              '\tdatetime: {}\n' \
              '\tstrength: {}'
        return tmp.format(
            self.symbol, self.strategy,
            SignalType.toStr(self.signal_type),
            self.tradingday, self.datetime,
            self.strength
        )


class OrderEvent(EventAbstract):
    def __init__(
            self,
            _index: int,
            _symbol: str,
            _tradingday: str,
            _datetime: typing.Union[str, datetime],
            _order_type: int = None,
            _action: int = None,
            _direction: int = None,
            _quantity: int = 1,
            _price: float = None
    ):
        super().__init__()
        self.type = EventType.ORDER
        self.index = _index
        self.symbol = _symbol
        self.tradingday = _tradingday
        self.datetime = _datetime
        self.order_type = _order_type
        self.action = _action
        self.direction = _direction
        self.quantity = _quantity
        self.price = _price

    def toDict(self) -> dict:
        return {
            'type': self.type,
            'index': self.index,
            'symbol': self.symbol,
            'tradingday': self.tradingday,
            'datetime': self.datetime,
            'order_type': self.order_type,
            'action': self.action,
            'direction': self.direction,
            'quantity': self.quantity,
            'price': self.price,
        }

    @staticmethod
    def fromDict(_dict: dict) -> 'OrderEvent':
        return OrderEvent(
            _index=_dict['index'],
            _symbol=_dict['symbol'],
            _tradingday=_dict['tradingday'],
            _datetime=_dict['datetime'],
            _order_type=_dict['order_type'],
            _action=_dict['action'],
            _direction=_dict['direction'],
            _quantity=_dict['quantity'],
            _price=_dict['price'], )

    def __repr__(self):
        tmp = 'ORDER:\n' \
              '\tindex: {}\n' \
              '\tsymbol: {}\n' \
              '\ttradingday: {}\n' \
              '\tdatetime: {}\n' \
              '\ttype: {}\n' \
              '\taction: {}\n' \
              '\tdirection: {}\n' \
              '\tquantity: {}\n' \
              '\tprice: {}\n'
        return tmp.format(
            self.index, self.symbol,
            self.tradingday, self.datetime,
            OrderType.toStr(self.order_type),
            ActionType.toStr(self.action),
            DirectionType.toStr(self.direction),
            self.quantity, self.price
        )


class FillEvent(EventAbstract):
    def __init__(
            self,
            _index: int,
            _symbol: str,
            _tradingday: str,
            _datetime: typing.Union[str, datetime],
            _quantity: int,
            _action: int,
            _direction: int,
            _price: float,
            _commission: float
    ):
        super().__init__()
        self.type = EventType.FILL
        self.index = _index
        self.symbol = _symbol
        self.tradingday = _tradingday
        self.datetime = _datetime
        self.quantity = _quantity
        self.action = _action
        self.direction = _direction
        self.price = _price
        self.commission = _commission

    def toDict(self) -> dict:
        return {
            'type': self.type,
            'index': self.index,
            'symbol': self.symbol,
            'tradingday': self.tradingday,
            'datetime': self.datetime,
            'quantity': self.quantity,
            'action': self.action,
            'direction': self.direction,
            'price': self.price,
            'commission': self.commission,
        }

    @staticmethod
    def fromDict(_dict: dict) -> 'FillEvent':
        return FillEvent(
            _index=_dict['index'],
            _symbol=_dict['symbol'],
            _tradingday=_dict['tradingday'],
            _datetime=_dict['datetime'],
            _quantity=_dict['quantity'],
            _action=_dict['action'],
            _direction=_dict['direction'],
            _price=_dict['price'],
            _commission=_dict['commission'], )

    def __repr__(self):
        tmp = 'FILL:\n' \
              '\tindex: {}\n' \
              '\tsymbol: {}\n' \
              '\ttradingday: {}\n' \
              '\tdatetime: {}\n' \
              '\tquantity: {}\n' \
              '\taction: {}\n' \
              '\tdirection: {}\n' \
              '\tprice: {}\n' \
              '\tcommission: {}'
        return tmp.format(
            self.index, self.symbol,
            self.tradingday, self.datetime,
            self.quantity, ActionType.toStr(self.action),
            DirectionType.toStr(self.direction),
            self.price, self.commission
        )


class SettlementEvent(EventAbstract):
    def __init__(
            self,
            _tradingday: str,
    ):
        super().__init__()
        self.type = EventType.SETTLEMENT
        self.tradingday = _tradingday

    def toDict(self) -> dict:
        return {
            'type': self.type,
            'tradingday': self.tradingday,
        }

    @staticmethod
    def fromDict(_dict: dict) -> 'SettlementEvent':
        return SettlementEvent(
            _tradingday=_dict['tradingday'],
        )

    def __repr__(self):
        tmp = "SETTLEMENT:\n" \
              "\ttradingday: {}\n"
        return tmp.format(
            self.tradingday
        )