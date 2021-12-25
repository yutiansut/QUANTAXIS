use actix::prelude::*;
use actix::{Actor, Addr, AsyncContext, Context, Handler, Recipient, Supervised};

extern crate serde_json;

use crate::qaruntime::qacontext::MOrder;

use crate::qaaccount::order::QAOrder;
use crate::qaprotocol::mifi::qafastkline::QAKlineBase;
use crate::qaprotocol::qifi::account::QIFI;
use crate::qapubsub::market_mq::MarketMQ;
use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Debug, Message, Clone, Deserialize, Serialize)]
#[rtype(result = "()")]
pub struct Instruct {
    pub id: String,
    pub topic: String,
    pub target: Vec<String>,
    pub body: String,
}

#[derive(Debug, Message, Clone, Deserialize, Serialize)]
#[rtype(result = "()")]
pub struct Ack {
    pub id: String,
    pub status: i32,
    pub ack: String,
    pub answerer: String,
}

#[derive(Debug, Message, Clone, Deserialize, Serialize)]
#[rtype(result = "()")]
pub struct Order {
    pub direction: String,
    pub offset: String,
    pub volume: f64,
    pub price: f64,
}

#[derive(Debug, Message)]
#[rtype(result = "()")]
pub struct AddMonitor {
    pub account_cookie: String,
    pub rec: Recipient<Instruct>,
}

#[derive(Debug, Message)]
#[rtype(result = "()")]
pub struct ShowAllMonitor;

#[derive(Message)]
#[rtype(result = "()")]
pub struct MQAddr {
    pub key: String,
    pub addr: Addr<MarketMQ>,
}

#[derive(Debug, Message)]
#[rtype(result = "()")]
pub struct ShowAllMQ;

#[derive(Debug, Message)]
#[rtype(result = "()")]
pub struct StartAllMQ;

#[derive(Debug, Message)]
#[rtype(result = "()")]
pub struct MarketSubscribe {
    pub key: String,
    pub rec: Recipient<QAKline>,
}

#[derive(Debug, Message)]
#[rtype(result = "()")]
pub struct QifiRsp {
    pub t: i32,
    pub data: QIFI,
}

#[derive(Debug, Message)]
#[rtype(result = "()")]
pub struct QAOrderRsp {
    pub data: Vec<MOrder>,
}

#[derive(Debug, Message)]
#[rtype(result = "()")]
pub struct QAKline {
    pub data: QAKlineBase,
}
