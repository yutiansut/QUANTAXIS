use crate::qapubsub::market_mq::{MarketMQ, Start, Subscribe};
use crate::qaruntime::base::{MQAddr, MarketSubscribe, ShowAllMQ};
use actix::prelude::*;
use actix::{Actor, Addr, Context, Handler, Recipient};
use log::{error, info, warn};
use std::collections::HashMap;

// 作为mq与策略之间的中间件
pub struct MQManager {
    pub mq_pool: HashMap<String, Addr<MarketMQ>>,
    pub connect_num: usize,
}

impl MQManager {
    pub fn new(connect_num: usize) -> Self {
        Self {
            mq_pool: HashMap::new(),
            connect_num,
        }
    }
}

impl Actor for MQManager {
    type Context = Context<Self>;
    fn started(&mut self, ctx: &mut Self::Context) {
        ctx.set_mailbox_capacity(1000); // 设置邮箱容量
        info!("[MarketMQ Manager] started.");
    }
}

// mq启动后将自己的addr发送至MQM
impl Handler<MQAddr> for MQManager {
    type Result = ();
    fn handle(&mut self, msg: MQAddr, ctx: &mut Self::Context) -> Self::Result {
        self.mq_pool.insert(msg.key, msg.addr);
    }
}

impl Handler<ShowAllMQ> for MQManager {
    type Result = ();
    fn handle(&mut self, msg: ShowAllMQ, ctx: &mut Self::Context) -> Self::Result {
        info!("MarketMQ routing_key: {:#?}", self.mq_pool.keys());
    }
}

// 策略订阅某行情
impl Handler<MarketSubscribe> for MQManager {
    type Result = ();
    fn handle(&mut self, msg: MarketSubscribe, ctx: &mut Self::Context) -> Self::Result {
        match self.mq_pool.get(msg.key.as_str()) {
            Some(mq) => match mq.try_send(Subscribe(msg.rec)) {
                Ok(_) => {
                    self.connect_num -= 1;
                    info!(
                        "[{}] add new Subscriber; {} not yet",
                        msg.key, self.connect_num
                    );
                    if self.connect_num == 0 {
                        info!("MarketMQ routing_key: {:#?}", self.mq_pool.keys());
                        for (k, mq) in self.mq_pool.iter() {
                            match mq.try_send(Start) {
                                Err(e) => error!("[{}] start fail {:?}", k, e.to_string()),
                                _ => {}
                            }
                        }
                    }
                }
                Err(e) => error!("[{}] subscribe fail {}", msg.key, e.to_string()),
            },
            None => {}
        }
    }
}
