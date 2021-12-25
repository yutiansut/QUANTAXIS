use std::collections::{BTreeMap, HashMap};
use std::error::Error;

use crate::qaprotocol::qifi::account::{Account, Order, Position, Trade, QIFI};
use chrono::{Local, TimeZone, Utc};
use csv;
use serde::{Deserialize, Serialize};

use crate::qaaccount::marketpreset::MarketPreset;
use crate::qaaccount::order::QAOrder;
use crate::qaaccount::position::{QA_Frozen, QA_Postions};
use crate::qaaccount::transaction;
use crate::qaaccount::transaction::QATransaction;
use crate::qautil::tradedate::QATradeDate;
use log::{error, info, warn};
use uuid::v1::{Context, Timestamp};
use uuid::Uuid;

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct QAAccountSlice {
    pub datetime: String,
    pub cash: f64,
    pub accounts: account,
    pub positions: HashMap<String, QA_Postions>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct QAMOMSlice {
    pub datetime: String,
    pub user_id: String,
    // 用户号 兼容diff协议, ==> 实盘则为具体账户号
    pub pre_balance: f64,
    // 上一个交易日的结算权益
    pub close_profit: f64,
    // 平仓盈亏
    pub commission: f64,
    pub position_profit: f64,
    // 持仓盈亏
    pub float_profit: f64,
    // 浮动盈亏
    pub balance: f64,
    // 当前权益
    pub margin: f64,
    // 保证金
    // 冻结附加费用
    pub available: f64,
    // 可用资金
    pub risk_ratio: f64, // 风险度
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct account_info {
    pub datetime: String,
    pub balance: f64,
    pub account_cookie: String,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct account {
    pub user_id: String,
    // 用户号 兼容diff协议, ==> 实盘则为具体账户号
    pub currency: String,
    // 货币属性 兼容diff协议
    pub pre_balance: f64,
    // 上一个交易日的结算权益
    pub deposit: f64,
    // 今日转入资金
    pub withdraw: f64,
    // 今日转出资金
    pub WithdrawQuota: f64,
    // 当前可取字段(QIFI 独有)
    pub close_profit: f64,
    // 平仓盈亏
    pub commission: f64,
    // 手续费
    pub premium: f64,
    // 附加费
    pub static_balance: f64,
    // 静态权益(一般= pre_balance)
    pub position_profit: f64,
    // 持仓盈亏
    pub float_profit: f64,
    // 浮动盈亏
    pub balance: f64,
    // 当前权益
    pub margin: f64,
    // 保证金
    pub frozen_margin: f64,
    // 冻结保证金
    pub frozen_commission: f64,
    // 冻结手续费
    pub frozen_premium: f64,
    // 冻结附加费用
    pub available: f64,
    // 可用资金
    pub risk_ratio: f64, // 风险度
}

#[allow(non_camel_case_types)]
#[derive(Debug, Clone)]
pub struct QA_Account {
    init_cash: f64,
    init_hold: HashMap<String, QA_Postions>,

    allow_t0: bool,
    allow_sellopen: bool,
    allow_margin: bool,

    auto_reload: bool,
    market_preset: MarketPreset,
    time: String,
    pub events: HashMap<String, String>,
    pub accounts: account,
    pub cash: Vec<f64>,
    pub money: f64,
    pub trades: HashMap<String, QATransaction>,
    pub hold: HashMap<String, QA_Postions>,
    pub frozen: HashMap<String, QA_Frozen>,
    pub dailyassets: HashMap<String, QAAccountSlice>,
    pub history: Vec<transaction::QATransaction>,
    pub account_cookie: String,
    pub portfolio_cookie: String,
    pub user_cookie: String,
    pub dailytrades: BTreeMap<String, Trade>,
    pub dailyorders: BTreeMap<String, Order>,
    environment: String,
    event_id: i32,
    commission_ratio: f64,
    // 手续费率
    tax_ratio: f64, // tax for qaaccount
}

impl QA_Account {
    pub fn new(
        account_cookie: &str,
        portfolio_cookie: &str,
        user_cookie: &str,
        init_cash: f64,
        auto_reload: bool,
        environment: &str,
    ) -> Self {
        let mut acc = Self {
            init_cash,
            init_hold: HashMap::new(),
            allow_t0: false,
            allow_sellopen: false,
            allow_margin: false,
            market_preset: MarketPreset::new(),
            auto_reload,
            time: Local::now().format("%Y-%m-%d %H:%M:%S").to_string(),
            events: HashMap::new(),
            accounts: account {
                user_id: account_cookie.to_string(),
                currency: "CNY".to_string(),
                pre_balance: init_cash.clone(),
                deposit: 0.0,
                withdraw: 0.0,
                WithdrawQuota: init_cash.clone(),
                close_profit: 0.0,
                commission: 0.0,
                premium: 0.0,
                static_balance: init_cash.clone(),
                position_profit: 0.0,
                float_profit: 0.0,
                balance: init_cash.clone(),
                margin: 0.0,
                frozen_margin: 0.0,
                frozen_commission: 0.0,
                frozen_premium: 0.0,
                available: init_cash.clone(),
                risk_ratio: 0.0,
            },
            cash: vec![init_cash],
            money: init_cash,
            hold: HashMap::new(),
            trades: HashMap::new(),
            frozen: HashMap::new(),
            history: vec![],
            account_cookie: account_cookie.parse().unwrap(),
            portfolio_cookie: portfolio_cookie.parse().unwrap(),
            user_cookie: user_cookie.parse().unwrap(),
            environment: environment.to_string(),
            dailyorders: Default::default(),
            dailytrades: Default::default(),
            dailyassets: HashMap::new(),
            event_id: 0,
            commission_ratio: 0.00025,
            tax_ratio: 0.001, // only in stock model
        };

        if auto_reload {
            acc.reload()
        }
        acc
    }
    pub fn set_portfoliocookie(&mut self, portfolio: String) {
        self.portfolio_cookie = portfolio;
    }

    pub fn new_from_qifi(message: QIFI) -> Self {
        let mut pos = message.positions;
        let mut accpos: HashMap<String, QA_Postions> = HashMap::new();

        for pos_i in pos.values_mut() {
            accpos.insert(
                pos_i.instrument_id.to_string(),
                QA_Postions::new_with_inithold(
                    pos_i.instrument_id.to_string(),
                    pos_i.user_id.to_string(),
                    message.account_cookie.to_string().clone(),
                    message.account_cookie.to_string().clone(),
                    message.account_cookie.to_string(),
                    pos_i.volume_long_today,
                    pos_i.volume_long_his,
                    pos_i.volume_short_today,
                    pos_i.volume_short_his,
                    pos_i.open_price_long,
                    pos_i.open_price_short,
                ),
            );
        }

        let mut acc = Self {
            init_cash: message.accounts.available,
            init_hold: HashMap::new(),
            allow_t0: false,
            allow_sellopen: false,
            allow_margin: false,
            market_preset: MarketPreset::new(),
            auto_reload: false,
            time: message.updatetime.clone(),
            events: HashMap::new(),
            accounts: account {
                user_id: message.accounts.user_id.clone(),
                currency: "CNY".to_string(),
                pre_balance: message.accounts.pre_balance.clone(),
                deposit: message.accounts.deposit.clone(),
                withdraw: message.accounts.withdraw.clone(),
                WithdrawQuota: message.accounts.WithdrawQuota.clone(),
                close_profit: message.accounts.close_profit.clone(),
                commission: message.accounts.commission.clone() as f64,
                premium: message.accounts.premium.clone() as f64,
                static_balance: message.accounts.static_balance.clone(),
                position_profit: message.accounts.position_profit.clone(),
                float_profit: message.accounts.float_profit.clone(),
                balance: message.accounts.balance.clone(),
                margin: message.accounts.margin.clone(),
                frozen_margin: message.accounts.frozen_margin.clone(),
                frozen_commission: message.accounts.frozen_commission.clone(),
                frozen_premium: message.accounts.frozen_premium.clone(),
                available: message.accounts.available.clone(),
                risk_ratio: message.accounts.risk_ratio.clone(),
            },
            cash: vec![message.accounts.available],
            money: message.money.clone(),
            hold: accpos,
            trades: HashMap::new(),
            frozen: HashMap::new(),
            history: vec![],
            account_cookie: message.account_cookie.clone(),
            portfolio_cookie: message.portfolio.clone(),
            user_cookie: message.account_cookie.clone(),
            environment: "real".to_string(),
            dailyorders: message.orders.clone(),
            dailytrades: message.trades.clone(),
            dailyassets: HashMap::new(),
            event_id: 0,
            commission_ratio: 0.00025,
            tax_ratio: 0.001, // only in stock model
        };
        acc
    }

    pub fn init_h(&mut self, code: &str) {
        let code: String = code.parse().unwrap();
        self.hold.insert(
            code.clone(),
            QA_Postions::new(
                code.clone(),
                self.account_cookie.clone(),
                self.account_cookie.clone(),
                self.account_cookie.clone(),
                self.portfolio_cookie.clone(),
            ),
        );
    }

    pub fn reload(&mut self) {}

    pub fn get_cash(&mut self) -> f64 {
        self.cash.last().unwrap().to_owned()
    }
    pub fn get_riskratio(&mut self) -> f64 {
        0.0
    }

    pub fn get_mom_slice(&mut self) -> QAMOMSlice {
        QAMOMSlice {
            datetime: self.time.clone(),
            user_id: self.account_cookie.clone(),
            pre_balance: self.accounts.pre_balance,
            close_profit: self.accounts.close_profit,
            commission: self.accounts.commission,
            position_profit: self.get_positionprofit(),
            float_profit: self.get_floatprofit(),
            balance: self.get_balance(),
            margin: self.get_margin(),
            available: self.money,
            risk_ratio: self.get_riskratio(),
        }
    }

    /// 创建QIFI的账户切片， 注意他是一个结构体
    pub fn get_qifi_slice(&mut self) -> QIFI {
        let mut pos: HashMap<String, Position> = HashMap::new();
        for posx in self.hold.values_mut() {
            pos.insert(posx.instrument_id.clone(), posx.get_qifi_position());
        }

        QIFI {
            account_cookie: self.account_cookie.clone(),
            portfolio: self.portfolio_cookie.clone(),
            broker_name: "QASIM".to_string(),
            money: self.money.clone(),
            updatetime: self.time.clone(),
            bankname: "QASIM".to_string(),
            trading_day: self.get_tradingday(),
            status: 200,
            accounts: self.get_accountmessage(),
            orders: self.dailyorders.clone(),
            positions: pos,
            trades: self.dailytrades.clone(),
            ..QIFI::default()
        }
    }

    pub fn get_accountmessage(&mut self) -> Account {
        Account {
            user_id: self.account_cookie.clone(),
            currency: "CNY".to_string(),
            pre_balance: self.accounts.pre_balance,
            deposit: self.accounts.deposit,
            withdraw: self.accounts.withdraw,
            WithdrawQuota: self.accounts.WithdrawQuota,
            close_profit: self.accounts.close_profit,
            commission: self.accounts.commission,
            premium: self.accounts.premium,
            static_balance: self.accounts.static_balance,
            position_profit: self.get_positionprofit(),
            float_profit: self.get_floatprofit(),
            balance: self.get_balance(),
            margin: self.get_margin(),
            frozen_margin: 0.0,
            frozen_commission: 0.0,
            frozen_premium: 0.0,
            available: self.money,
            risk_ratio: self.get_riskratio(),
        }
    }
    /// positions about
    ///
    /// a fast way to get the realtime price/cost/volume/history
    pub fn get_position(&mut self, code: &str) -> Option<&mut QA_Postions> {
        let pos = self.hold.get_mut(code);
        pos
    }

    pub fn get_volume_long(&mut self, code: &str) -> f64 {
        if self.hold.contains_key(code) {
            let pos = self.get_position(code).unwrap();
            pos.volume_long()
        } else {
            0.0
        }
    }
    pub fn get_volume_short(&mut self, code: &str) -> f64 {
        if self.hold.contains_key(code) {
            let pos = self.get_position(code).unwrap();
            pos.volume_short()
        } else {
            0.0
        }
    }
    pub fn get_open_price_long(&mut self, code: &str) -> f64 {
        self.get_position(code).unwrap().open_price_long
    }
    pub fn get_open_price_short(&mut self, code: &str) -> f64 {
        self.get_position(code).unwrap().open_price_short
    }

    /// frozen & margin
    pub fn get_frozen(&mut self, code: &str) -> f64 {
        self.get_position(code).unwrap().frozen
    }
    pub fn get_margin(&mut self) -> f64 {
        let mut margin = 0.0;
        for pos in self.hold.values_mut() {
            margin += pos.margin();
        }
        margin
    }

    /// profit
    pub fn get_floatprofit(&mut self) -> f64 {
        let mut fp = 0.0;
        for pos in self.hold.values_mut() {
            fp += pos.float_profit();
        }
        fp
    }
    pub fn get_positionprofit(&mut self) -> f64 {
        let mut pp = 0.0;
        for pos in self.hold.values_mut() {
            pp += pos.float_profit();
        }
        pp
    }

    /// balance
    pub fn get_balance(&mut self) -> f64 {
        let fp = self.get_floatprofit();
        //info!("{} {} {} {} {}", self.accounts.static_balance, self.accounts.deposit, self.accounts.withdraw, fp, self.accounts.close_profit);
        self.accounts.static_balance + self.accounts.deposit - self.accounts.withdraw
            + fp
            + self.accounts.close_profit
    }

    pub async fn settle_async(&mut self) {
        self.settle();
    }

    pub fn settle(&mut self) {
        self.dailyassets.insert(
            self.time.clone(),
            QAAccountSlice {
                datetime: self.time.clone(),
                cash: self.money.clone(),
                accounts: self.accounts.clone(),
                //events: self.events.clone(),
                positions: self.hold.clone(),
                //frozen: self.frozen.clone(),
                //trades: self.trades.clone(),
            },
        );
        self.trades = HashMap::new();
        self.dailyorders = BTreeMap::new();
        self.dailytrades = BTreeMap::new();
        self.events = HashMap::new();
        self.event_id = 0;

        for pos in self.hold.values_mut() {
            pos.settle();
        }
        // init the next day cash
        let balance_settle =
            self.accounts.pre_balance + self.accounts.close_profit - self.accounts.commission;
        self.accounts = account {
            user_id: self.account_cookie.to_string(),
            currency: "CNY".to_string(),
            pre_balance: balance_settle.clone(),
            deposit: 0.0,
            withdraw: 0.0,
            WithdrawQuota: balance_settle.clone(),
            close_profit: 0.0,
            commission: 0.0,
            premium: 0.0,
            static_balance: balance_settle.clone(),
            position_profit: 0.0,
            float_profit: 0.0,
            balance: balance_settle.clone(),
            margin: self.accounts.margin,
            frozen_margin: 0.0,
            frozen_commission: 0.0,
            frozen_premium: 0.0,
            available: balance_settle.clone(),
            risk_ratio: self.get_riskratio(),
        }
    }

    pub fn get_codeSubscribed(&mut self) -> Vec<String> {
        // if a QAAccount trades a packages, then it need the get_codeSubscribed to update the price
        // some examples like below
        // let codes = account.get_codeSubscribed();
        // for code in codes.iter():
        //     acc.on_price_change(code, price.get(code), datetime)
        let mut codeSub = vec![];
        for key in self.hold.keys() {
            codeSub.push(key.to_string())
        }
        codeSub
    }

    pub fn get_slice(&mut self) -> QAAccountSlice {
        // get a realtime slice of account
        // this can be save to database

        QAAccountSlice {
            datetime: self.time.clone(),
            cash: self.money.clone(),
            accounts: self.accounts.clone(),
            positions: self.hold.clone(),
        }
    }

    pub fn get_account_info(&mut self) -> account_info {
        account_info {
            datetime: self.time.clone(),
            balance: self.get_balance(),
            account_cookie: self.account_cookie.clone(),
        }
    }

    pub fn get_latest_info(&mut self) -> String {
        let info = self.get_account_info();

        serde_json::to_string(&info).unwrap()
    }

    /// history about

    pub fn history_table(&self) {
        for item in self.history.iter() {
            info!("{:?}", transaction::QATransaction::to_json(item));
        }
    }

    pub fn to_csv(&self, string: String) -> Result<(), Box<dyn Error>> {
        let mut wtr = csv::Writer::from_path(format!("{}.csv", self.account_cookie)).unwrap();
        for item in self.history.iter() {
            wtr.serialize(item)?;
            wtr.flush()?;
        }
        Ok(())
    }

    /// order about
    /// buy| sell| buy_open| sell_open| buy_close| sell_close|
    /// send_order
    pub fn buy(&mut self, code: &str, amount: f64, time: &str, price: f64) -> Result<QAOrder, ()> {
        self.send_order(code, amount, time, 1, price, "BUY")
    }
    pub fn sell(&mut self, code: &str, amount: f64, time: &str, price: f64) -> Result<QAOrder, ()> {
        self.send_order(code, amount, time, -1, price, "SELL")
    }
    pub fn buy_open(
        &mut self,
        code: &str,
        amount: f64,
        time: &str,
        price: f64,
    ) -> Result<QAOrder, ()> {
        self.send_order(code, amount, time, 2, price, "BUY_OPEN")
    }
    pub fn sell_open(
        &mut self,
        code: &str,
        amount: f64,
        time: &str,
        price: f64,
    ) -> Result<QAOrder, ()> {
        self.send_order(code, amount, time, -2, price, "SELL_OPEN")
    }
    pub fn buy_close(
        &mut self,
        code: &str,
        amount: f64,
        time: &str,
        price: f64,
    ) -> Result<QAOrder, ()> {
        self.send_order(code, amount, time, 3, price, "BUY_CLOSE")
    }
    pub fn sell_close(
        &mut self,
        code: &str,
        amount: f64,
        time: &str,
        price: f64,
    ) -> Result<QAOrder, ()> {
        self.send_order(code, amount, time, -3, price, "SELL_CLOSE")
    }
    pub fn buy_closetoday(
        &mut self,
        code: &str,
        amount: f64,
        time: &str,
        price: f64,
    ) -> Result<QAOrder, ()> {
        self.send_order(code, amount, time, 4, price, "BUY_CLOSETODAY")
    }
    pub fn sell_closetoday(
        &mut self,
        code: &str,
        amount: f64,
        time: &str,
        price: f64,
    ) -> Result<QAOrder, ()> {
        self.send_order(code, amount, time, -4, price, "SELL_CLOSETODAY")
    }
    pub fn get_tradingday(&mut self) -> String {
        let mut u = QATradeDate::new();
        u.get_trade_day(self.time.clone())
    }

    fn order_check(
        &mut self,
        code: &str,
        amount: f64,
        price: f64,
        towards: i32,
        order_id: String,
    ) -> bool {
        let mut res = false;
        if self.hold.contains_key(code) {
        } else {
            self.init_h(code);
        }
        let qapos = self.get_position(code).unwrap();

        match towards {
            3 => {
                if (qapos.volume_short() - qapos.volume_short_frozen()) >= amount {
                    qapos.volume_short_frozen_today += amount;
                    qapos.volume_short_today -= amount;
                    res = true;
                } else {
                    warn!("仓位不足");
                }
            }
            4 => {
                if (qapos.volume_short_today - qapos.volume_short_frozen_today) >= amount {
                    qapos.volume_short_frozen_today += amount;
                    qapos.volume_short_today -= amount;
                    res = true;
                } else {
                    warn!("今日仓位不足");
                }
            }

            -1 => {
                if (qapos.volume_long_his - qapos.volume_long_frozen()) >= amount {
                    qapos.volume_long_frozen_today += amount;
                    qapos.volume_long_today -= amount;
                    res = true;
                } else {
                    warn!("SELL CLOSE 仓位不足");
                }
            }

            -3 => {
                if (qapos.volume_long() - qapos.volume_long_frozen()) >= amount {
                    qapos.volume_long_frozen_today += amount;
                    qapos.volume_long_today -= amount;
                    res = true;
                } else {
                    warn!("SELL CLOSE 仓位不足");
                }
            }

            -4 => {
                if (qapos.volume_long_today - qapos.volume_short_frozen_today) >= amount {
                    qapos.volume_long_frozen_today += amount;
                    qapos.volume_long_today -= amount;
                    res = true;
                } else {
                    warn!("SELL CLOSETODAY 仓位不足");
                }
            }

            1 | 2 | -2 => {
                let coeff = qapos.preset.calc_coeff() * price;

                let frozen = coeff * amount;
                //                println!("OPEN FROZEN{:#?}", frozen);
                //                println!("ORDER ID {:#?}", order_id);

                if self.money > frozen {
                    self.money -= frozen;

                    self.frozen.insert(
                        order_id,
                        QA_Frozen {
                            amount,
                            coeff,
                            money: frozen,
                        },
                    );

                    res = true
                } else {
                    warn!(
                        "余额不足,当前可用money {:#?}, 需要冻结 {:#?}",
                        self.money, frozen
                    );
                }
            }
            _ => {}
        }
        res
    }

    pub async fn send_order_async(
        &mut self,
        code: &str,
        amount: f64,
        time: &str,
        towards: i32,
        price: f64,
        order_id: &str,
    ) -> Option<QAOrder> {
        let order = self.send_order(code, amount, time, towards, price, order_id);
        let result = if order.is_ok() {
            Some(order.unwrap())
        } else {
            None
        };
        result
    }
    pub fn send_order(
        &mut self,
        code: &str,
        amount: f64,
        time: &str,
        towards: i32,
        price: f64,
        order_id: &str,
    ) -> Result<QAOrder, ()> {
        self.event_id += 1;
        let datetimer = if time.len() == 10 {
            format!("{} 00:00:00", time.to_string())
        } else {
            time.to_string()
        };
        let datetime = datetimer.as_str();

        let context = Context::new(self.event_id as u16);
        let ts = Timestamp::from_unix(&context, 1497624119, 1234);
        let uuid = Uuid::new_v1(ts, &[1, 2, 3, 4, 5, 6]).expect("failed to generate UUID");

        let order_id: String = uuid.to_string();

        if self.order_check(code, amount, price, towards, order_id.clone()) {
            let order = QAOrder::new(
                self.account_cookie.clone(),
                code.clone().to_string(),
                towards,
                "".to_string(),
                datetime.to_string(),
                amount,
                price,
                order_id.clone(),
            );
            match self.environment.as_ref() {
                "backtest" => {
                    self.receive_deal(
                        code.parse().unwrap(),
                        amount,
                        price,
                        datetime.parse().unwrap(),
                        order_id.clone(),
                        order_id.clone(),
                        order_id.clone(),
                        towards,
                    );
                }
                "real" => {
                    let (direction, offset) = self.get_direction_or_offset(towards);
                    self.dailyorders.insert(
                        order_id.clone(),
                        Order {
                            seqno: self.event_id.clone(),
                            user_id: self.account_cookie.clone(),
                            order_id: order_id.clone(),
                            exchange_id: "".to_string(),
                            instrument_id: code.clone().to_string(),
                            direction,
                            offset,
                            volume_orign: amount,
                            price_type: "LIMIT".to_string(),
                            limit_price: price,
                            time_condition: "AND".to_string(),
                            volume_condition: "GFD".to_string(),
                            insert_date_time: Utc
                                .datetime_from_str(datetime, "%Y-%m-%d %H:%M:%S")
                                .unwrap()
                                .timestamp_nanos()
                                - 28800000000000,
                            exchange_order_id: Uuid::new_v4().to_string(),
                            status: "FINISHED".to_string(),
                            volume_left: 0.0,
                            last_msg: "".to_string(),
                        },
                    );

                    self.receive_deal_real(
                        code.parse().unwrap(),
                        amount,
                        price,
                        datetime.parse().unwrap(),
                        order_id.clone(),
                        order_id.clone(),
                        order_id.clone(),
                        towards,
                        self.event_id.clone(),
                    )
                    // self.events.insert(self.datetime.clone(), "order insert".to_string());
                }
                _ => {
                    self.events
                        .insert(self.time.clone(), "order insert".to_string());
                }
            }
            Ok(order.clone())
        } else {
            Err(())
        }
    }

    pub fn on_price_change(&mut self, code: String, price: f64, datetime: String) {
        // 当行情变化时候 要更新计算持仓

        if self.hold.contains_key(&code) {
            let pos = self.get_position(code.as_ref()).unwrap();
            pos.on_price_change(price, datetime.clone());
            self.change_datetime(datetime);
        }
    }

    pub fn change_datetime(&mut self, datetime: String) {
        // 用于切换时间
        self.time = datetime;
    }

    pub fn set_init_cash(&mut self, cash: f64) {
        self.init_cash = cash;
    }

    /// 获取成交单方向信息的API， 支持股票与期货
    pub fn get_direction_or_offset(&mut self, towards: i32) -> (String, String) {
        let rt = match towards {
            1 => (String::from("BUY"), String::from("OPEN")),
            2 => (String::from("BUY"), String::from("OPEN")),
            3 => (String::from("BUY"), String::from("CLOSE")),
            4 => (String::from("BUY"), String::from("CLOSETODAY")),
            -1 => (String::from("SELL"), String::from("CLOSE")),
            -2 => (String::from("SELL"), String::from("OPEN")),
            -3 => (String::from("SELL"), String::from("CLOSE")),
            -4 => (String::from("SELL"), String::from("CLOSETODAY")),
            _ => (String::from(""), String::from("")),
        };
        rt
    }
    fn receive_deal_real(
        &mut self,
        code: String,
        amount: f64,
        price: f64,
        datetime: String,
        order_id: String,
        trade_id: String,
        realorder_id: String,
        towards: i32,
        event_id: i32,
    ) {
        self.time = datetime.clone();
        if self.frozen.contains_key(&order_id) {
            let frozen = self.frozen.get_mut(&order_id).unwrap();
            self.money += frozen.money;
            self.frozen.remove(&order_id);
        } else {
            if towards == -1 | 1 | 2 | -2 {
                error!("NOT IN DAY ORDER {}", order_id)
            }
        }
        let qapos = self.get_position(code.as_ref()).unwrap();

        let commission = qapos
            .clone()
            .preset
            .calc_commission(price.clone(), amount.clone());
        let tax = qapos
            .clone()
            .preset
            .calc_tax(price.clone(), amount.clone(), towards.clone());
        qapos.on_price_change(price.clone(), datetime.clone());
        let (margin, close_profit) = qapos.update_pos(price, amount, towards);
        let (direction, offset) = self.get_direction_or_offset(towards);
        // add calc tax/coeff
        //        qapos.preset.commission_coeff_pervol

        self.money -= (margin - close_profit + commission + tax);
        self.accounts.close_profit += close_profit;
        self.cash.push(self.money);
        self.accounts.commission += commission + tax;

        // println!("{:?} {:?} {:?} {:?}", datetime,code,direction,offset);

        let td = Utc
            .datetime_from_str(datetime.as_ref(), "%Y-%m-%d %H:%M:%S")
            .unwrap()
            .timestamp_nanos()
            - 28800000000000;
        let trade = Trade {
            seqno: event_id,
            user_id: self.account_cookie.clone(),
            price,
            order_id,
            trade_id: trade_id.clone(),
            exchange_id: "".to_string(),
            commission: commission + tax,
            direction,
            offset,
            instrument_id: code,
            exchange_trade_id: "".to_string(),
            volume: amount,
            trade_date_time: td,
        };
        self.dailytrades.insert(trade_id, trade.clone());
    }

    fn receive_deal(
        &mut self,
        code: String,
        amount: f64,
        price: f64,
        datetime: String,
        order_id: String,
        trade_id: String,
        realorder_id: String,
        towards: i32,
    ) {
        self.time = datetime.clone();
        if self.frozen.contains_key(&order_id) {
            let frozen = self.frozen.get_mut(&order_id).unwrap();
            self.money += frozen.money;
            self.frozen.remove(&order_id);

            // self.frozen.insert(order_id.clone(), QA_Frozen {
            //     amount: 0.0,
            //     coeff: 0.0,
            //     money: 0.0,
            // });
        } else {
            if towards == -1 | 1 | 2 | -2 {
                error!("ERROR NO THAT ORDER {}", order_id)
            }
        }

        let qapos = self.get_position(code.as_ref()).unwrap();
        let commission = qapos
            .clone()
            .preset
            .calc_commission(price.clone(), amount.clone());
        let tax = qapos
            .clone()
            .preset
            .calc_tax(price.clone(), amount.clone(), towards.clone());
        qapos.on_price_change(price.clone(), datetime.clone());

        let (margin, close_profit) = qapos.update_pos(price, amount, towards);

        //println!("MARGIN RELEASE {:#?}", margin.clone());
        //println!("CLOSE PROFIT RELEASE {:#?}", close_profit.clone());
        self.money -= (margin - close_profit + commission + tax);
        self.accounts.close_profit += close_profit;
        self.cash.push(self.money);
        self.accounts.commission += commission + tax;
        let transaction = transaction::QATransaction {
            code,
            amount,
            price,
            datetime,
            order_id,
            trade_id: trade_id.clone(),
            realorder_id,
            account_cookie: self.account_cookie.clone(),
            commission,
            tax,
            message: "".to_string(),
            frozen: 0.0,
            direction: towards,
        };
        self.trades.insert(trade_id, transaction.clone());
        self.history.push(transaction);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new() {
        // create a new account
        // 可以正确的创建一个账户
        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );
        acc.history_table();

        let mut acc = QA_Account::new("RustT01B2_RBL8", "test", "admin", 100000.0, false, "real");
    }

    #[test]
    fn test_pos() {
        // test get position function
        // 可以正确初始化一个/多个持仓
        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );
        acc.init_h("RB2005");
        acc.get_position("RB2005");

        acc.init_h("000001");

        println!("{:#?}", acc.get_codeSubscribed());
    }

    #[test]
    fn test_init_h() {
        // test init a position function
        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );
        acc.init_h("RB2005");
        println!("{:#?}", acc.get_position("RB2005").unwrap().message());
    }

    #[test]
    fn test_buy_open() {
        println!("test buy open");
        let code = "RB2005";
        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            1000000.0,
            false,
            "backtest",
        );

        acc.buy_open(code, 10.0, "2020-01-20", 3500.0);
        println!("MONEY LEFT{:#?}", acc.money);
        assert_eq!(acc.get_volume_long(code), 10.0);
        acc.history_table();
    }

    #[test]
    fn test_buy_open_for_stock() {
        println!("test buy open");
        let code = "000001";
        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            1000000.0,
            false,
            "backtest",
        );

        acc.buy_open(code, 1000.0, "2020-01-20", 35.0);
        println!("MONEY LEFT{:#?}", acc.money);
        assert_eq!(acc.get_volume_long(code), 1000.0);
        acc.history_table();
    }

    #[test]
    fn test_realaccountmodel_for_stock() {
        println!("test buy open");
        let code = "000001";
        let mut acc = QA_Account::new("RustT01B2_RBL8", "test", "admin", 1000000.0, false, "real");

        acc.buy_open(code, 1000.0, "2020-01-20", 35.0);
        println!("MONEY LEFT{:#?}", acc.money);
        assert_eq!(acc.get_volume_long(code), 1000.0);
        println!("QIFI {:#?}", acc.get_qifi_slice());
        //acc.history_table();
    }

    #[test]
    fn test_sell_open() {
        println!("test sell open");
        let code = "RB2005";
        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );
        acc.sell_open(code, 10.0, "2020-01-20", 3500.0);
        assert_eq!(acc.get_volume_short(code), 10.0);
        acc.history_table();
    }

    #[test]
    fn test_buy_close() {
        println!("test buy close");
        let code = "RB2005";
        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );
        acc.init_h(code);
        acc.sell_open(code, 10.0, "2020-01-20", 3500.0);
        assert_eq!(acc.get_volume_short(code), 10.0);
        acc.buy_close(code, 10.0, "2020-01-20", 3600.0);
        assert_eq!(acc.get_volume_short(code), 0.0);
        println!("LATEST MONEY {:#?}", acc.money);
        println!("CLOSE PROFIT {:#?}", acc.accounts.close_profit);
        acc.history_table();
    }

    #[test]
    fn test_sell_close() {
        println!("test sell close");
        let code = "RB2005";
        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );
        acc.init_h(code);
        acc.buy_open(code, 10.0, "2020-01-20", 3500.0);
        assert_eq!(acc.get_volume_long(code), 10.0);
        acc.sell_close(code, 10.0, "2020-01-20", 3600.0);
        assert_eq!(acc.get_volume_long(code), 0.0);
        println!("LATEST MONEY {:#?}", acc.money);
        println!("CLOSE PROFIT {:#?}", acc.accounts.close_profit);
        acc.history_table();
    }

    #[test]
    fn test_sellclose_for_stock_rzrq() {
        println!("test buy open");
        let code = "000001";
        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            1000000.0,
            false,
            "backtest",
        );

        acc.buy_open(code, 1000.0, "2020-01-20", 35.0);
        println!("MONEY LEFT{:#?}", acc.money);
        assert_eq!(acc.get_volume_long(code), 1000.0);

        acc.sell_close(code, 1000.0, "2020-01-20", 36.0);
        acc.history_table();
    }

    #[test]
    fn test_stock_buy() {
        println!("test account slice");
        let code = "000001";
        let mut acc = QA_Account::new(
            "rust_test_stock",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );

        acc.buy(code, 10.0, "2020-01-20 22:10:00", 3500.0);
        assert_eq!(acc.get_volume_long(code), 10.0);
        println!("{:#?}", acc.trades)
    }

    #[test]
    fn test_stocksell() {
        println!("test account slice");
        let code = "000001";
        let mut acc = QA_Account::new("rust_test_stock", "test", "admin", 100000.0, false, "real");
        acc.init_h(code);
        acc.buy(code, 10.0, "2020-01-20 22:10:00", 3500.0);
        assert_eq!(acc.get_volume_long(code), 10.0);

        acc.settle();
        acc.sell(code, 10.0, "2020-01-22 22:10:00", 3600.0);
        println!("{:#?}", acc.dailytrades);
    }

    #[test]
    fn test_stocksell_with_settle() {
        println!("test account slice");
        let code = "000001";
        let mut acc = QA_Account::new("rust_test_stock", "test", "admin", 100000.0, false, "real");
        acc.init_h(code);
        acc.buy(code, 10.0, "2020-01-20 22:10:00", 3500.0);
        assert_eq!(acc.get_volume_long(code), 10.0);
        acc.settle();
        acc.sell(code, 10.0, "2020-01-20 22:10:00", 3600.0);
        println!("{:#?}", acc.dailytrades);
    }

    #[test]
    fn test_accountSlice() {
        println!("test account slice");
        let code = "RB2005";

        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );
        acc.init_h(code);
        acc.buy_open(code, 10.0, "2020-01-20", 3500.0);
        let slice = acc.get_slice();
        println!("account Slice  {:#?}", slice);
        assert_eq!(acc.get_volume_long(code), 10.0);
        acc.sell_close(code, 10.0, "2020-01-20", 3600.0);
        assert_eq!(acc.get_volume_long(code), 0.0);
        println!("LATEST MONEY {:#?}", acc.money);
        println!("CLOSE PROFIT {:#?}", acc.accounts.close_profit);
        let slice = acc.get_slice();
        println!("account Slice  {:#?}", slice);
        acc.history_table();
    }

    #[test]
    fn test_accountSlice_for_qifi() {
        println!("test account slice");
        let code = "RB2005";
        let mut acc = QA_Account::new("RustT01B2_RBL8", "test", "admin", 100000.0, false, "real");
        acc.init_h(code);
        acc.buy_open(code, 10.0, "2020-01-20 22:10:00", 3500.0);
        let slice = acc.get_qifi_slice();
        println!("account Slice  {:#?}", slice);
        assert_eq!(acc.get_volume_long(code), 10.0);
        acc.sell_close(code, 10.0, "2020-01-20 22:10:00", 3600.0);
        assert_eq!(acc.get_volume_long(code), 0.0);
        println!("LATEST MONEY {:#?}", acc.money);
        println!("CLOSE PROFIT {:#?}", acc.accounts.close_profit);
        let slice = acc.get_qifi_slice();
        let slicestr = serde_json::to_string(&slice).unwrap();
        println!("{:#?}", slicestr);
    }

    #[test]
    fn test_qifi_reload() {
        println!("test account slice");
        let code = "RB2005";
        let mut acc = QA_Account::new("RustT01B2_RBL8", "test", "admin", 100000.0, false, "real");
        acc.buy_open(code, 10.0, "2020-01-20 22:10:00", 3500.0);
        let slice = acc.get_qifi_slice();
        assert_eq!(acc.get_volume_long(code), 10.0);
        let slice = acc.get_qifi_slice();
        let mut new_acc = QA_Account::new_from_qifi(slice);
        assert_eq!(new_acc.get_volume_long(code), 10.0);
        new_acc.sell_close(code, 10.0, "2020-01-20 22:10:00", 3600.0);

        println!("{:#?}", new_acc.trades);

        println!("{:#?}", new_acc.dailytrades);
    }

    #[test]
    fn test_stock_qifi_reload() {
        println!("test account slice");
        let code = "000001";
        let mut acc = QA_Account::new("rust_test_stock", "test", "admin", 100000.0, false, "real");
        acc.init_h(code);
        acc.buy_open(code, 10.0, "2020-01-20 22:10:00", 3500.0);
        let slice = acc.get_qifi_slice();
        assert_eq!(acc.get_volume_long(code), 10.0);
        let slice = acc.get_qifi_slice();
        let mut new_acc = QA_Account::new_from_qifi(slice);
        assert_eq!(new_acc.get_volume_long(code), 10.0);
        new_acc.sell_close(code, 10.0, "2020-01-20 22:10:00", 3600.0);
        println!("{:#?}", new_acc.trades);
        println!("{:#?}", new_acc.dailytrades);
    }

    #[test]
    fn test_getaccountmessage() {
        println!("test account slice");
        let code = "RB2005";
        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );
        acc.init_h(code);
        acc.buy_open(code, 10.0, "2020-01-20", 3500.0);
        let slice = acc.get_accountmessage();
        println!("account Slice  {:#?}", slice);
        assert_eq!(acc.get_volume_long(code), 10.0);
        acc.sell_close(code, 10.0, "2020-01-20", 3600.0);
        assert_eq!(acc.get_volume_long(code), 0.0);
        println!("LATEST MONEY {:#?}", acc.money);
        println!("CLOSE PROFIT {:#?}", acc.accounts.close_profit);
        let slice = acc.get_accountmessage();
        println!("account Slice  {:#?}", slice);
        acc.history_table();
    }

    #[test]
    fn test_settle() {
        println!("test account slice");
        let code = "RB2005";

        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );
        acc.init_h(code);
        acc.buy_open(code, 10.0, "2020-01-20", 3500.0);

        let slice = acc.get_accountmessage();
        println!("before settle");
        println!("account Slice  {:#?}", slice);
        assert_eq!(acc.get_volume_long(code), 10.0);

        acc.sell_close(code, 10.0, "2020-01-20", 3600.0);

        assert_eq!(acc.get_volume_long(code), 0.0);
        //println!("{:#?}", )
        println!("LATEST MONEY {:#?}", acc.money);
        println!("CLOSE PROFIT {:#?}", acc.accounts.close_profit);

        let slice = acc.get_accountmessage();

        println!("account Slice  {:#?}", slice);

        acc.settle();
        println!("after settle");

        let slice = acc.get_accountmessage();
        println!("account Slice  {:#?}", slice);

        acc.buy_open(code, 10.0, "2020-01-22", 3500.0);

        acc.on_price_change(code.to_string(), 3523.0, "2020-01-22".to_string());
        let slice = acc.get_accountmessage();
        println!("before settle");
        println!("account Slice  {:#?}", slice);
        acc.settle();
        println!("after settle");

        let slice = acc.get_accountmessage();
        println!("account Slice  {:#?}", slice);

        acc.history_table();
    }

    #[test]
    fn test_on_pricechange() {
        println!("test on price change");
        let code = "RB2005";

        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );
        acc.init_h(code);
        acc.buy_open(code, 10.0, "2020-01-20", 3500.0);
        assert_eq!(acc.get_volume_long(code), 10.0);

        acc.on_price_change(code.to_string(), 3520.0, "2020-01-20".to_string());
        assert_eq!(2000.0, acc.get_floatprofit());

        acc.sell_close(code, 10.0, "2020-01-20", 3600.0);

        assert_eq!(acc.get_volume_long(code), 0.0);
        //println!("{:#?}", )
        println!("LATEST MONEY {:#?}", acc.money);
        println!("CLOSE PROFIT {:#?}", acc.accounts.close_profit);

        acc.history_table();
    }

    #[test]
    fn test_to_csv() {
        println!("test sell close");
        let code = "RB2005";

        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );
        acc.init_h(code);
        acc.buy_open(code, 10.0, "2020-01-20", 3500.0);
        assert_eq!(acc.get_volume_long(code), 10.0);
        acc.sell_close(code, 10.0, "2020-01-20", 3600.0);

        assert_eq!(acc.get_volume_long(code), 0.0);
        //println!("{:#?}", )
        println!("{:#?}", acc.money);
        acc.to_csv("".to_string());
        //acc.history_table();
    }

    #[test]
    fn test_get_info() {
        let mut acc = QA_Account::new(
            "RustT01B2_RBL8",
            "test",
            "admin",
            100000.0,
            false,
            "backtest",
        );
        acc.buy_open("rb2005", 10.0, "2020-01-20", 3500.0);
        let r = acc.get_latest_info();
        println!("{:#?}", r);
        assert_eq!(100000.0, acc.get_balance());
        acc.on_price_change("rb2005".to_string(), 3600.0, "2020-01-21".to_string());
        let r = acc.get_latest_info();
        println!("{:#?}", r);
        assert_eq!(110000.0, acc.get_balance());
    }
}
