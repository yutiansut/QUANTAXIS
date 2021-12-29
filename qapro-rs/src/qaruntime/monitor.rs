extern crate redis;
use actix::prelude::*;
use actix::{Actor, Addr, AsyncContext, Context, Handler, Recipient, Supervised};
use chrono::{Local, TimeZone};
use log::{error, info, warn};
use redis::Commands;
use serde_json::Value;
use std::fmt::Debug;
use std::time::Duration;
use uuid::Version::Mac;

use crate::qaaccount::account::QA_Account;
use crate::qaaccount::marketpreset::MarketPreset;
use crate::qaaccount::order::QAOrder;
use crate::qaconnector::mongo::mongoclient::QAMongoClient;
use crate::qadata::resample::{resample_db, QARealtimeResampler};
use crate::qaenv::localenv::CONFIG;
use crate::qaprotocol::mifi::qafastkline::QAKlineBase;
use crate::qaprotocol::qifi::account::QIFI;
use crate::qaruntime::base::{Ack, AddMonitor, Instruct, Order, QAKline, QAOrderRsp, QifiRsp};
use crate::qaruntime::qacontext::{QAContext, StrategyFunc};
use crate::qaruntime::qamanagers::monitor_manager::MonitorManager;
use crate::qautil::tradedate::QATradeDate;

enum StateCode {}

pub struct Monitor<T> {
    pub qactx: QAContext,
    pub stg: T,
    pub mor_manger: Addr<MonitorManager>,
    pub qarere: QARealtimeResampler,
    ur: bool,
    td: QATradeDate,

    settle_ts: i64,
    qifi_ts: i64,
}

impl<T: 'static> Monitor<T>
where
    T: StrategyFunc + Debug,
{
    pub fn new(qactx: QAContext, stg: T, mor_manger: Addr<MonitorManager>) -> Self {
        let f = qactx.frequence.clone();
        let freq = f[0..f.len() - 3].parse::<i64>().unwrap();
        let qarere = QARealtimeResampler::new(freq);
        let u = Self {
            qactx,
            stg,
            mor_manger,
            qarere,
            ur: true,
            td: QATradeDate::new(),
            settle_ts: 0,
            qifi_ts: 0,
        };
        u
    }

    pub fn backtest(&mut self, mongo_data: &Vec<QAKlineBase>, redis_data: &Vec<QAKlineBase>) {
        //---------
        // mongo_ 回测
        //----------
        info!("[{}] backtest mongo...", self.qactx.account_cookie);
        for (realtimebar, is_last) in mongo_data
            .into_iter()
            .map(|data| (data.clone().to_bar(), data.is_last))
        {
            println!("{:#?}", realtimebar);
            if !self
                .qactx
                .acc
                .get_tradingday()
                .eq(&self.td.get_trade_day(realtimebar.datetime.clone()))
            {
                self.qactx.acc.settle();
                self.settle_ts = Local::now().timestamp();
            }

            if is_last {
                self.ur = true;

                self.qactx.update(realtimebar.clone(), &mut self.stg);
                self.qactx.switch(realtimebar);
            } else {
                if self.ur {
                    self.qactx.next(realtimebar, &mut self.stg);
                    self.ur = false;
                } else {
                    self.qactx.update(realtimebar, &mut self.stg);
                }
            }
        }
        self.qactx.acc.settle();
        self.settle_ts = Local::now().timestamp();
        info!("[{}] backtest mongo end", self.qactx.account_cookie);
        //---------
        // redis 实时数据回测
        //----------
        info!("[{}] backtest redis...", self.qactx.account_cookie);
        for (realtimebar, is_last) in redis_data
            .into_iter()
            .map(|data| (data.clone().to_bar(), data.is_last))
        {
            if !self
                .qactx
                .acc
                .get_tradingday()
                .eq(&self.td.get_trade_day(realtimebar.datetime.clone()))
            {
                self.qactx.acc.settle();
                self.settle_ts = Local::now().timestamp();
            }
            if is_last {
                self.ur = true;
                self.qactx.update(realtimebar.clone(), &mut self.stg);
                self.qactx.switch(realtimebar);
            } else {
                if self.ur {
                    self.qactx.next(realtimebar, &mut self.stg);
                    self.ur = false;
                } else {
                    self.qactx.update(realtimebar, &mut self.stg);
                }
            }
        }
        info!("[{}] backtest redis end", self.qactx.account_cookie);
        // 回测的订单不发出

        self.qactx
            .acc
            .to_csv(format!("{}.csv", self.qactx.account_cookie));
        self.qactx.order_que.clear();
    }

    pub fn inner_handle(&mut self, msg: QAKlineBase) {
        let bar = self.qarere.next(msg.to_bar());
        let (is_last, data) = (bar.is_last, bar.to_bar());
        if is_last {
            self.ur = true;
            self.qactx.update(data.clone(), &mut self.stg);
            self.qactx.switch(data);
        } else {
            if self.ur {
                self.qactx.next(data, &mut self.stg);
                self.ur = false;
            } else {
                self.qactx.update(data, &mut self.stg);
            }
        }
        //---------
        // 订单pub
        //---------
        match self.mor_manger.try_send(QAOrderRsp {
            data: self.qactx.order_que.clone(),
        }) {
            Err(e) => {
                let m = format!("pub orders fail {:?}", e.to_string());
            }
            _ => {}
        }
        //---------
        // 清空订单列表
        //---------
        self.qactx.order_que.clear();
        //---------
        // qifi save
        //---------
        match self.mor_manger.try_send(QifiRsp {
            t: 0,
            data: self.qactx.acc.get_qifi_slice(),
        }) {
            Err(e) => {
                let m = format!("qifi save fail {:?}", e.to_string());
            }
            _ => {
                self.qifi_ts = Local::now().timestamp();
            }
        }
    }

    pub fn manual_settle(&mut self, instruct: Instruct) {
        let ts = Local::now().timestamp();
        if instruct.body.eq("--force") || ts - self.settle_ts > 60 * 60 * 24 {
            match self.mor_manger.try_send(QifiRsp {
                t: 1,
                data: self.qactx.acc.get_qifi_slice(),
            }) {
                Ok(_) => {
                    self.settle_ts = ts;
                    self.qactx.acc.settle();
                    //------
                    // flow
                    //-------
                    let m = "settle success".to_owned();
                    self.ack(instruct, 200, m);
                }
                Err(e) => {
                    let m = format!("save qifi_his fail{:?}", e.to_string());

                    self.ack(instruct, 500, m);
                }
            }
        } else {
            let m = "last time settle < 24h, or use [--force]".to_owned();

            self.ack(instruct, 400, m);
        }
    }

    pub fn manual_send_order(&mut self, instruct: Instruct) {
        match serde_json::from_str(&instruct.body) {
            Ok(o) => {
                let time = Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
                let code = self.qactx.code.clone();
                let order: Order = o;
                if order.direction.eq("BUY") && order.offset.eq("OPEN") {
                    self.qactx.buy_open(&code, order.volume, &time, order.price)
                } else if order.direction.eq("BUY") && order.offset.eq("CLOSE") {
                    self.qactx
                        .buy_close(&code, order.volume, &time, order.price)
                } else if order.direction.eq("SELL") && order.offset.eq("OPEN") {
                    self.qactx
                        .sell_open(&code, order.volume, &time, order.price)
                } else if order.direction.eq("SELL") && order.offset.eq("CLOSE") {
                    self.qactx
                        .sell_close(&code, order.volume, &time, order.price)
                } else {
                    let m = "send_order fail".to_owned();

                    self.ack(instruct, 400, m);
                    return;
                }
                let m = "send_order success".to_owned();
                self.ack(instruct, 200, m);
            }
            Err(e) => {
                let m = format!("Instruct order parse fail {}", e.to_string());
                self.ack(instruct, 400, m);
            }
        }
    }

    pub fn get_clock(&mut self, instruct: Instruct) {
        match instruct.body.as_str() {
            "stg_status" => println!("{:#?}", &self.stg),
            _ => {}
        }
        self.ack(instruct, 200, self.qactx.clock.clone());
    }

    pub fn ack(&mut self, instruct: Instruct, status: i32, ack: String) {
        match self.mor_manger.try_send(Ack {
            id: instruct.id.clone(),
            status,
            ack,
            answerer: self.qactx.account_cookie.clone(),
        }) {
            Err(e) => {
                let s = format!("[{}] ack fail {}", self.qactx.account_cookie, e.to_string());
                println!("{:#?}", &s);
            }
            _ => {}
        };
    }
}

impl<T: 'static> Actor for Monitor<T>
where
    T: StrategyFunc + Debug,
{
    type Context = Context<Self>;
    fn started(&mut self, ctx: &mut Self::Context) {
        ctx.set_mailbox_capacity(10000); // 设置邮箱容量
                                         //---------
                                         // register monitor
                                         //---------
        match self.mor_manger.try_send(AddMonitor {
            account_cookie: self.qactx.account_cookie.clone(),
            rec: ctx.address().recipient().clone(),
        }) {
            Err(e) => error!("monitor register fail {:?}", e.to_string()),
            _ => {}
        }
        ctx.run_interval(Duration::from_secs(30), |mor, ctx| {
            //---------
            // save qifi
            //---------
            let t = Local::now().timestamp();
            if t - mor.qifi_ts > 30 {
                match mor.mor_manger.try_send(QifiRsp {
                    t: 0,
                    data: mor.qactx.acc.get_qifi_slice(),
                }) {
                    Err(e) => error!("heartbeat save qifi fail {:?}", e.to_string()),
                    _ => {}
                }
            }
        });
    }
}

impl<T: 'static> Handler<QAKline> for Monitor<T>
where
    T: StrategyFunc + Debug,
{
    type Result = ();
    fn handle(&mut self, msg: QAKline, ctx: &mut Context<Self>) -> Self::Result {
        self.inner_handle(msg.data);
    }
}

impl<T: 'static> Handler<Instruct> for Monitor<T>
where
    T: StrategyFunc + Debug,
{
    type Result = ();
    fn handle(&mut self, msg: Instruct, ctx: &mut Context<Self>) -> Self::Result {
        // println!("{:?}", msg);
        match msg.topic.as_str() {
            "settle" => {
                self.manual_settle(msg);
            }
            "send_order" => {
                self.manual_send_order(msg);
            }
            "clock" => {
                self.get_clock(msg);
            }
            _ => {}
        }
    }
}

impl<T: 'static> Unpin for Monitor<T> where T: StrategyFunc + Debug {}

impl<T: 'static> Supervised for Monitor<T>
where
    T: StrategyFunc + Debug,
{
    fn restarting(&mut self, _: &mut actix::Context<Self>) {
        warn!("[{}] Restarting!!!", self.qactx.account_cookie);
    }
}
