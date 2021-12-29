use chrono::prelude::Utc;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::ops::Deref;

use crate::qaaccount::account::QA_Account;
use crate::qaaccount::order::{QAOrder, TradeOrder};
use crate::qaprotocol::mifi::market::BAR;

use crate::qadata::datafunc::{dhhv, dllv, max, min, Que};

pub trait StrategyFunc {
    fn on_bar_next(&mut self, data: &BAR, context: &mut QAContext);
    fn on_bar_update(&mut self, data: &BAR, context: &mut QAContext);
}

#[derive(Debug, Clone)]
pub struct MOrder {
    pub model: String,
    pub time: String,
    pub order: QAOrder,
}

impl MOrder {
    pub fn to_mt(&self) -> MTrade {
        MTrade {
            time: self.time.clone(),
            model: self.model.clone(),
            trade: self.order.to_trade_order(),
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MTrade {
    pub model: String,
    pub time: String,
    pub trade: TradeOrder,
}

#[derive(Debug, Clone)]
pub struct QAContext {
    pub acc: QA_Account,
    pub account_cookie: String,
    pub frequence: String,
    pub bar_id: i32,
    pub lastbar: BAR,
    pub lasttradebar: i32,
    pub priceoffset: f64,
    pub high_que: Que<f64>,
    pub low_que: Que<f64>,
    pub open_que: Que<f64>,
    pub close_que: Que<f64>,
    pub code: String,
    pub order_que: Vec<MOrder>,
    pub clock: String,
    pub current_model: String,
}

impl QAContext {
    pub fn new(account_cookie: &str, frequence: &str, code: &str, environment: String) -> Self {
        let acc = QA_Account::new(
            account_cookie,
            "test",
            "admin",
            100000.0,
            false,
            &environment,
        );
        let mut ctx = Self {
            acc,
            account_cookie: account_cookie.to_string(),
            frequence: frequence.to_string(),
            bar_id: 0,
            lastbar: BAR {
                code: "".to_string(),
                datetime: "0000-00-00 00:00:00".to_string(),
                open: 0.0,
                high: 0.0,
                low: 0.0,
                close: 0.0,
                volume: 0.0,
                amount: 0.0,
            },
            lasttradebar: 0,
            priceoffset: 0.0,
            high_que: Que::new(300, 0.0),
            low_que: Que::new(300, 0.0),
            open_que: Que::new(300, 0.0),
            close_que: Que::new(300, 0.0),
            order_que: Vec::new(),
            code: code.to_string(),
            clock: String::new(),
            current_model: String::new(),
        };
        ctx.init(code);
        ctx
    }

    pub fn same_bar(&self) -> bool {
        if self.bar_id == self.lasttradebar && self.lasttradebar != 0 {
            return true;
        }
        false
    }

    pub fn account_reload(&mut self, acc: QA_Account) {
        self.acc = acc;
        self.init(self.code.clone().as_str());
    }

    pub fn init(&mut self, code: &str) {
        if !self.acc.hold.contains_key(code) {
            self.acc.init_h(code);
        }
        self.priceoffset = self.acc.get_position(code).unwrap().get_price_tick();
    }

    pub fn switch(&mut self, data: BAR) {
        self.lastbar = data;
        self.bar_id += 1;
    }

    pub fn next(&mut self, bar: BAR, stg_func: &mut impl StrategyFunc) {
        self.clock = bar.datetime.clone();
        //  包含当前最新bar
        self.high_que.push(bar.high);
        self.low_que.push(bar.low);
        self.close_que.push(bar.close);
        self.open_que.push(bar.open);
        //
        self.current_model = "next".to_owned();

        stg_func.on_bar_next(&bar, self);
        self.acc
            .on_price_change(bar.code.clone(), bar.close.clone(), bar.datetime.clone());
    }

    pub fn update(&mut self, bar: BAR, stg_func: &mut impl StrategyFunc) {
        self.clock = bar.datetime.clone();
        //  包含当前最新bar
        self.high_que.last_update(bar.high);
        self.low_que.last_update(bar.low);
        self.close_que.last_update(bar.close);
        self.open_que.last_update(bar.open);
        //
        self.current_model = "update".to_owned();

        stg_func.on_bar_update(&bar, self);
        self.acc
            .on_price_change(bar.code.clone(), bar.close.clone(), bar.datetime.clone());
    }

    /// order about
    /// buy| sell| buy_open| sell_open| buy_close| sell_close|
    /// send_order

    pub fn buy_open(&mut self, code: &str, amount: f64, time: &str, price: f64) {
        println!("buy open");
        match self.acc.buy_open(code, amount, time, price) {
            Ok(order) => {
                self.order_que.push(MOrder {
                    model: self.current_model.clone(),
                    time: time.to_owned(),
                    order,
                });
                self.lasttradebar = self.bar_id;
            }
            Err(e) => {}
        };
    }
    pub fn sell_open(&mut self, code: &str, amount: f64, time: &str, price: f64) {
        match self.acc.sell_open(code, amount, time, price) {
            Ok(order) => {
                self.order_que.push(MOrder {
                    model: self.current_model.clone(),
                    time: time.to_owned(),
                    order,
                });
                self.lasttradebar = self.bar_id;
            }
            Err(e) => {}
        };
    }
    pub fn buy_close(&mut self, code: &str, amount: f64, time: &str, price: f64) {
        match self.acc.buy_close(code, amount, time, price) {
            Ok(order) => {
                self.order_que.push(MOrder {
                    model: self.current_model.clone(),
                    time: time.to_owned(),
                    order,
                });
                self.lasttradebar = self.bar_id;
            }
            Err(e) => {}
        };
    }
    pub fn sell_close(&mut self, code: &str, amount: f64, time: &str, price: f64) {
        match self.acc.sell_close(code, amount, time, price) {
            Ok(order) => {
                self.order_que.push(MOrder {
                    model: self.current_model.clone(),
                    time: time.to_owned(),
                    order,
                });
                self.lasttradebar = self.bar_id;
            }
            Err(e) => {}
        };
    }
}
