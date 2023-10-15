use chrono::prelude::*;
use serde::{Deserialize, Serialize};
use std::clone::Clone;

use crate::qaprotocol::mifi::mifibase::Handler;

#[derive(Serialize, Deserialize, Debug)]
pub struct FullData {
    pub amount: f64,
    pub close: f64,
    pub code: String,
    pub high: f64,
    pub low: f64,
    pub market: String,
    pub open: f64,
    pub productid: f64,
    pub tickcount: f64,
    pub time: String,
    pub vol: f64,
    pub BuyPrices: Vec<f64>,
    pub BuyVols: Vec<f64>,
    pub SellPrices: Vec<f64>,
    pub SellVols: Vec<f64>,
}

impl Handler for FullData {
    fn get_datetime(&self) -> String {
        return self.time.clone();
    }

    fn get_code(&self) -> String {
        self.code.clone()
    }

    fn get_date(&self) -> String {
        unimplemented!()
    }

    fn get_open(&self) -> f64 {
        self.open.clone()
    }

    fn get_close(&self) -> f64 {
        self.close.clone()
    }

    fn get_high(&self) -> f64 {
        self.high.clone()
    }

    fn get_low(&self) -> f64 {
        self.low.clone()
    }

    fn get_vol(&self) -> f64 {
        self.vol.clone()
    }

    fn get_amount(&self) -> f64 {
        self.amount.clone()
    }

    fn set_datetime(&mut self, datetime: String) {
        self.time = datetime;
    }
    fn set_open(&mut self, open: f64) {
        self.open = open;
    }

    fn set_high(&mut self, high: f64) {
        self.high = high;
    }

    fn set_low(&mut self, low: f64) {
        self.low = low;
    }
    fn set_close(&mut self, close: f64) {
        self.close = close
    }
    fn set_vol(&mut self, vol: f64) {
        self.vol = vol;
    }

    fn set_amount(&mut self, amount: f64) {
        self.amount = amount
    }
}

impl Clone for FullData {
    fn clone(&self) -> Self {
        FullData {
            amount: self.amount.clone(),
            close: self.close.clone(),
            code: self.code.clone(),
            high: self.high.clone(),
            low: self.low.clone(),
            market: self.market.clone(),
            open: self.open.clone(),
            productid: self.productid.clone(),
            tickcount: self.tickcount.clone(),
            time: self.time.clone(),
            vol: self.vol.clone(),
            BuyPrices: self.BuyPrices.clone(),
            BuyVols: self.BuyVols.clone(),
            SellPrices: self.SellPrices.clone(),
            SellVols: self.SellVols.clone(),
        }
    }
}

impl Default for FullData {
    fn default() -> Self {
        FullData {
            amount: 0.0,
            close: 0.0,
            code: "".to_string(),
            high: 0.0,
            low: 0.0,
            market: "".to_string(),
            open: 0.0,
            productid: 0.0,
            tickcount: 0.0,
            time: "1900-01-01 00:00:00".to_string(),
            vol: 0.0,
            BuyPrices: vec![],
            BuyVols: vec![],
            SellPrices: vec![],
            SellVols: vec![],
        }
    }
}

#[derive(Serialize, Clone, Deserialize, Debug)]
pub struct Full {
    pub MarketFullName: String,
    pub products: Vec<FullData>,
}

/// ctpx提供的数据源
#[derive(Serialize, Clone, Deserialize, Debug)]
pub struct CtpPro {
    pub ask_price_1: f64,
    pub ask_price_2: f64,
    pub ask_price_3: f64,
    pub ask_price_4: f64,
    pub ask_price_5: f64,
    pub ask_volume_1: f64,
    pub ask_volume_2: f64,
    pub ask_volume_3: f64,
    pub ask_volume_4: f64,
    pub ask_volume_5: f64,
    pub average_price: f64,
    pub bid_price_1: f64,
    pub bid_price_2: f64,
    pub bid_price_3: f64,
    pub bid_price_4: f64,
    pub bid_price_5: f64,
    pub bid_volume_1: f64,
    pub bid_volume_2: f64,
    pub bid_volume_3: f64,
    pub bid_volume_4: f64,
    pub bid_volume_5: f64,
    pub datetime: String,
    pub exchange: String,
    pub gateway_name: String,
    pub high_price: f64,
    pub last_price: f64,
    pub last_volume: f64,
    pub limit_down: f64,
    pub limit_up: f64,
    pub local_symbol: String,
    pub low_price: f64,
    pub name: String,
    pub open_interest: f64,
    pub open_price: f64,
    pub preSettlementPrice: f64,
    pub pre_close: f64,
    pub symbol: String,
    pub volume: f64,
}

impl Handler for CtpPro {
    fn get_datetime(&self) -> String {
        return self.datetime.clone();
    }

    fn get_code(&self) -> String {
        self.symbol.clone().to_string()
    }

    fn get_date(&self) -> String {
        self.datetime[0..9].parse().unwrap()
    }

    fn get_open(&self) -> f64 {
        unimplemented!()
    }

    fn get_close(&self) -> f64 {
        self.last_price.clone()
    }

    fn get_high(&self) -> f64 {
        unimplemented!()
    }

    fn get_low(&self) -> f64 {
        unimplemented!()
    }

    fn get_vol(&self) -> f64 {
        self.volume.clone()
    }

    fn get_amount(&self) -> f64 {
        0 as f64
    }
}

impl Default for CtpPro {
    fn default() -> Self {
        CtpPro {
            ask_price_1: 0.0,
            ask_price_2: 0.0,
            ask_price_3: 0.0,
            ask_price_4: 0.0,
            ask_price_5: 0.0,
            ask_volume_1: 0.0,
            ask_volume_2: 0.0,
            ask_volume_3: 0.0,
            ask_volume_4: 0.0,
            ask_volume_5: 0.0,
            average_price: 0.0,
            bid_price_1: 0.0,
            bid_price_2: 0.0,
            bid_price_3: 0.0,
            bid_price_4: 0.0,
            bid_price_5: 0.0,
            bid_volume_1: 0.0,
            bid_volume_2: 0.0,
            bid_volume_3: 0.0,
            bid_volume_4: 0.0,
            bid_volume_5: 0.0,
            datetime: "1900-01-01 00:00:00.10000".to_string(),
            exchange: "".to_string(),
            gateway_name: "".to_string(),
            high_price: 0.0,
            last_price: 0.0,
            last_volume: 0.0,
            limit_down: 0.0,
            limit_up: 0.0,
            local_symbol: "".to_string(),
            low_price: 0.0,
            name: "".to_string(),
            open_interest: 0.0,
            open_price: 0.0,
            preSettlementPrice: 0.0,
            pre_close: 0.0,
            symbol: "".to_string(),
            volume: 0.0,
        }
    }
}

impl CtpPro {
    pub fn to_diff(&self) -> Diff {
        Diff {
            instrument_id: self.local_symbol.clone(),
            volume_multiple: 0,
            price_tick: 0.0,
            price_decs: 0,
            max_market_order_volume: 0,
            min_market_order_volume: 0,
            max_limit_order_volume: 0,
            min_limit_order_volume: 0,
            margin: 0.0,
            commission: 0.0,
            datetime: "1900-01-01 00:00:00".to_string(),
            ask_price1: 0.0,
            ask_volume1: 0,
            bid_price1: 0.0,
            bid_volume1: 0,
            last_price: 0.0,
            highest: 0.0,
            lowest: 0.0,
            amount: 0.0,
            volume: 0,
            open_interest: 0,
            pre_open_interest: 0,
            pre_close: self.pre_close,
            open: self.open_price.clone(),
            close: 0.0,
            lower_limit: 0.0,
            upper_limit: 0.0,
            average: 0.0,
            pre_settlement: 0.0,
            settlement: 0.0,
        }
    }
}

/// ---------------------------------------------------------------- StockDay------------------------------------------------------------------------
#[derive(Serialize, Clone, Deserialize, Debug)]
pub struct StockDay {
    pub open: f64,
    pub close: f64,
    pub high: f64,
    pub low: f64,
    #[serde(rename = "vol")]
    pub volume: f64,
    pub amount: f64,
    pub date: String,
    pub code: String,
    //    date_stamp : f64
}

impl Default for StockDay {
    fn default() -> Self {
        StockDay {
            open: 0.0,
            close: 0.0,
            high: 0.0,
            low: 0.0,
            volume: 0.0,
            amount: 0.0,
            date: "1900-01-01".to_string(),
            code: "".to_string(),
        }
    }
}

impl Handler for StockDay {
    fn get_datetime(&self) -> String {
        unimplemented!()
    }

    fn get_code(&self) -> String {
        self.code.clone()
    }

    fn get_date(&self) -> String {
        self.date.clone()
    }

    fn get_open(&self) -> f64 {
        self.open.clone()
    }

    fn get_close(&self) -> f64 {
        self.close.clone()
    }

    fn get_high(&self) -> f64 {
        self.high.clone()
    }

    fn get_low(&self) -> f64 {
        self.low.clone()
    }

    fn get_vol(&self) -> f64 {
        self.volume.clone()
    }

    fn get_amount(&self) -> f64 {
        self.amount.clone()
    }

    fn set_code(&mut self, code: String) {
        self.code = code;
    }

    fn set_date(&mut self, date: String) {
        self.date = date;
    }

    fn set_open(&mut self, open: f64) {
        self.open = open
    }

    fn set_close(&mut self, close: f64) {
        self.close = close;
    }

    fn set_high(&mut self, high: f64) {
        self.high = high;
    }

    fn set_low(&mut self, low: f64) {
        self.low = low;
    }

    fn set_vol(&mut self, vol: f64) {
        self.volume = vol;
    }

    fn set_amount(&mut self, amount: f64) {
        self.amount = amount
    }
}

/// ---------------------------------------------------------------- FutureDay------------------------------------------------------------------------
#[derive(Serialize, Clone, Deserialize, Debug)]
pub struct FutureDay {
    pub open: f64,
    pub close: f64,
    pub high: f64,
    pub low: f64,
    #[serde(rename = "trade")]
    pub volume: f64,
    pub date: String,
    pub code: String,
}

impl Default for FutureDay {
    fn default() -> Self {
        FutureDay {
            open: 0.0,
            close: 0.0,
            high: 0.0,
            low: 0.0,
            volume: 0.0,
            date: "1900-01-01".to_string(),
            code: "".to_string(),
        }
    }
}

impl Handler for FutureDay {
    fn get_datetime(&self) -> String {
        unimplemented!()
    }

    fn get_code(&self) -> String {
        self.code.clone()
    }

    fn get_date(&self) -> String {
        self.date.clone()
    }

    fn get_open(&self) -> f64 {
        self.open.clone()
    }

    fn get_close(&self) -> f64 {
        self.close.clone()
    }

    fn get_high(&self) -> f64 {
        self.high.clone()
    }

    fn get_low(&self) -> f64 {
        self.low.clone()
    }

    fn get_vol(&self) -> f64 {
        self.volume.clone()
    }

    fn get_amount(&self) -> f64 {
        unimplemented!()
    }

    fn set_code(&mut self, code: String) {
        self.code = code;
    }

    fn set_date(&mut self, date: String) {
        self.date = date;
    }

    fn set_open(&mut self, open: f64) {
        self.open = open
    }

    fn set_close(&mut self, close: f64) {
        self.close = close;
    }

    fn set_high(&mut self, high: f64) {
        self.high = high;
    }

    fn set_low(&mut self, low: f64) {
        self.low = low;
    }

    fn set_vol(&mut self, vol: f64) {
        self.volume = vol;
    }

    fn set_amount(&mut self, amount: f64) {
        unimplemented!()
    }
}

/// -------------------------------------------------------------------FutureMin ----------------------------------------------------------------------
#[derive(Serialize, Clone, Deserialize, Debug)]
pub struct FutureMin {
    pub open: f64,
    pub close: f64,
    pub high: f64,
    pub low: f64,
    #[serde(rename = "trade")]
    pub volume: f64,
    pub date: String,
    pub datetime: String,
    pub code: String,
    #[serde(rename = "type")]
    pub frequence: String,
    pub position: f64,
    pub amount: f64,
    pub tradetime: String,
}

impl Default for FutureMin {
    fn default() -> Self {
        FutureMin {
            open: 0.0,
            close: 0.0,
            high: 0.0,
            low: 0.0,
            volume: 0.0,
            date: "".to_string(),
            datetime: "1900-01-01 00:00:00".to_string(),
            code: "".to_string(),
            frequence: "".to_string(),
            position: 0.0,
            amount: 0.0,
            tradetime: "".to_string(),
        }
    }
}

impl Handler for FutureMin {
    fn get_datetime(&self) -> String {
        self.datetime.clone()
    }

    fn get_code(&self) -> String {
        self.code.clone()
    }

    fn get_date(&self) -> String {
        self.date.clone()
    }

    fn get_open(&self) -> f64 {
        self.open.clone()
    }

    fn get_close(&self) -> f64 {
        self.close.clone()
    }

    fn get_high(&self) -> f64 {
        self.high.clone()
    }

    fn get_low(&self) -> f64 {
        self.low.clone()
    }

    fn get_vol(&self) -> f64 {
        self.volume.clone()
    }

    fn get_amount(&self) -> f64 {
        self.amount.clone()
    }
}

#[derive(Serialize, Clone, Deserialize, Debug)]
pub struct StockMin {
    pub open: f64,
    pub close: f64,
    pub high: f64,
    pub low: f64,
    #[serde(rename = "vol")]
    pub volume: f64,
    pub amount: f64,
    pub date: String,
    pub datetime: String,
    pub code: String,
    //    date_stamp : f64,
    //    time_stamp : f64,
    #[serde(rename = "type")]
    pub frequence: String,
}

impl Default for StockMin {
    fn default() -> Self {
        StockMin {
            open: 0.0,
            close: 0.0,
            high: 0.0,
            low: 0.0,
            volume: 0.0,
            amount: 0.0,
            date: "".to_string(),
            datetime: "".to_string(),
            code: "".to_string(),
            frequence: "".to_string(),
        }
    }
}

impl Handler for StockMin {
    fn get_datetime(&self) -> String {
        self.datetime.clone()
    }

    fn get_code(&self) -> String {
        self.code.clone()
    }

    fn get_date(&self) -> String {
        unimplemented!()
    }

    fn get_open(&self) -> f64 {
        self.open.clone()
    }

    fn get_close(&self) -> f64 {
        self.close.clone()
    }

    fn get_high(&self) -> f64 {
        self.high.clone()
    }

    fn get_low(&self) -> f64 {
        self.low.clone()
    }

    fn get_vol(&self) -> f64 {
        self.volume.clone()
    }

    fn get_amount(&self) -> f64 {
        self.amount.clone()
    }
}

/// ------------------------------------------------------------ Diff --------------------------------------------------------------------
#[derive(Serialize, Clone, Deserialize, Debug)]
pub struct Diff {
    instrument_id: String,
    //合约代码
    volume_multiple: i64,
    //合约乘数
    price_tick: f64,
    //合约价格单位
    price_decs: i64,
    //合约价格小数位数
    max_market_order_volume: i64,
    //市价单最大下单手数
    min_market_order_volume: i64,
    //市价单最小下单手数
    max_limit_order_volume: i64,
    //限价单最大下单手数
    min_limit_order_volume: i64,
    //限价单最小下单手数
    margin: f64,
    //每手保证金
    commission: f64,
    //每手手续费
    datetime: String,
    //时间
    ask_price1: f64,
    //卖价
    ask_volume1: i64,
    //卖量
    bid_price1: f64,
    //买价
    bid_volume1: i64,
    //买量
    last_price: f64,
    //最新价
    highest: f64,
    //最高价
    lowest: f64,
    //最低价
    amount: f64,
    //成交额
    volume: i64,
    //成交量
    open_interest: i64,
    //持仓量
    pre_open_interest: i64,
    //昨持
    pre_close: f64,
    //昨收
    open: f64,
    //今开
    close: f64,
    //收盘
    lower_limit: f64,
    //跌停
    upper_limit: f64,
    //涨停
    average: f64,
    //均价
    pre_settlement: f64,
    //昨结
    settlement: f64, //结算价
}

impl Default for Diff {
    fn default() -> Self {
        Diff {
            instrument_id: "".to_string(),
            volume_multiple: 0,
            price_tick: 0.0,
            price_decs: 0,
            max_market_order_volume: 0,
            min_market_order_volume: 0,
            max_limit_order_volume: 0,
            min_limit_order_volume: 0,
            margin: 0.0,
            commission: 0.0,
            datetime: "1900-01-01 00:00:00.10000".to_string(),
            ask_price1: 0.0,
            ask_volume1: 0,
            bid_price1: 0.0,
            bid_volume1: 0,
            last_price: 0.0,
            highest: 0.0,
            lowest: 0.0,
            amount: 0.0,
            volume: 0,
            open_interest: 0,
            pre_open_interest: 0,
            pre_close: 0.0,
            open: 0.0,
            close: 0.0,
            lower_limit: 0.0,
            upper_limit: 0.0,
            average: 0.0,
            pre_settlement: 0.0,
            settlement: 0.0,
        }
    }
}

#[derive(Serialize, Deserialize, Debug)]
pub struct L2xHis {
    pub time: String,
    pub price: f64,
    pub vol: f64,
    pub buyorsell: f64,
    pub date: String,
    pub datetime: String,
    pub code: String,
    pub date_stamp: f64,
    pub time_stamp: f64,
    #[serde(rename(serialize = "type", deserialize = "type"))]
    //type字段 实现与数据库中读取不进行冲突
    pub type_: String,
    pub order: f64,
}

impl Default for L2xHis {
    fn default() -> Self {
        L2xHis {
            time: "25:00".to_string(),
            price: 0.0,
            vol: 0.0,
            buyorsell: 0.0,
            date: "1900-01-01".to_string(),
            datetime: "1900-01-01 00:00:00".to_string(),
            code: "".to_string(),
            date_stamp: 0.0,
            time_stamp: 0.0,
            type_: "tick".to_string(),
            order: 0.0,
        }
    }
}

impl Clone for L2xHis {
    fn clone(&self) -> Self {
        L2xHis {
            time: self.time.clone(),
            price: self.price.clone(),
            vol: self.vol.clone(),
            buyorsell: self.buyorsell.clone(),
            date: self.date.clone(),
            datetime: self.datetime.clone(),
            code: self.code.clone(),
            date_stamp: self.date_stamp.clone(),
            time_stamp: self.time_stamp.clone(),
            type_: self.type_.clone(),
            order: self.order.clone(),
        }
    }
}

impl Handler for L2xHis {
    fn get_datetime(&self) -> String {
        self.datetime.clone()
    }

    fn get_code(&self) -> String {
        self.code.clone()
    }

    fn get_date(&self) -> String {
        self.date.clone()
    }

    fn get_open(&self) -> f64 {
        unimplemented!()
    }

    fn get_close(&self) -> f64 {
        self.price.clone()
    }

    fn get_high(&self) -> f64 {
        unimplemented!()
    }

    fn get_low(&self) -> f64 {
        unimplemented!()
    }

    fn get_vol(&self) -> f64 {
        self.vol.clone()
    }

    fn get_amount(&self) -> f64 {
        unimplemented!()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BAR {
    pub code: String,
    pub datetime: String,
    pub open: f64,
    pub high: f64,
    pub low: f64,
    pub close: f64,
    pub volume: f64,
    pub amount: f64,
}

//┌───────date─┬─order_book_id─┬─num_trades─┬─limit_up─┬─limit_down─┬──open─┬──high─┬───low─┬─close─┬───volume─┬─total_turnover─┐
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RqBar {
    pub order_book_id: String,
    pub date: String,
    pub datetime: String,
    pub open: f32,
    pub high: f32,
    pub low: f32,
    pub close: f32,
    pub num_trades: f32,
    pub limit_up: f32,
    pub limit_down: f32,
    pub volume: f32,
    pub total_turnover: f32,
}

//datetime─┬─trading_date─┬─order_book_id─┬─open─┬──last─┬─high─┬─low─┬─prev_close─┬─volume─┬─total_turnover─┬─limit_up─┬─limit_down─┬
// ───a1─┬─a2─┬─a3─┬─a4─┬─a5─┬───b1─┬─b2─┬─b3─┬─b4─┬─b5─┬──a1_v─┬──a2_v─┬─a3_v─┬─a4_v─┬─a5_v─┬──b1_v─┬─b2_v─┬─b3_v─┬─b4_v─┬─b5_v─┬─change_rate─┐
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RqTick {
    pub order_book_id: String,
    pub trading_date: String,
    pub datetime: String,
    pub prev_close: f32,
    pub open: f32,
    pub high: f32,
    pub low: f32,
    pub last: f32,
    pub num_trades: f32,
    pub limit_up: f32,
    pub limit_down: f32,
    pub volume: f32,
    pub total_turnover: f32,
    pub a1: f32,
    pub a1_v: f32,
    pub a2: f32,
    pub a2_v: f32,
    pub a3: f32,
    pub a3_v: f32,
    pub a4: f32,
    pub a4_v: f32,
    pub a5: f32,
    pub a5_v: f32,
    pub b1: f32,
    pub b1_v: f32,
    pub b2: f32,
    pub b2_v: f32,
    pub b3: f32,
    pub b3_v: f32,
    pub b4: f32,
    pub b4_v: f32,
    pub b5: f32,
    pub b5_v: f32,
    pub change_rate: f32,
}
