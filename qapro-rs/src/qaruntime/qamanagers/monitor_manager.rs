use crate::qaconnector::mongo::mongoclient::QAMongoClient;
use crate::qaenv::localenv::CONFIG;
use crate::qaruntime::base::{Ack, AddMonitor, Instruct, QAOrderRsp, QifiRsp, ShowAllMonitor};
use actix::prelude::*;
use actix::{Actor, Addr, Context, Handler, Recipient};
use amiquip::{
    Channel, Connection, ConsumerMessage, ConsumerOptions, Exchange, ExchangeDeclareOptions,
    ExchangeType, FieldTable, Publish, QueueDeclareOptions, Result,
};
use log::{error, info, warn};
use serde_json::Value;
use std::collections::HashMap;
use std::thread;

//订单推送
pub struct MQPublish {
    pub conn: Connection,
    pub channel: Channel,
}

impl MQPublish {
    pub fn new(amqp: &str) -> Self {
        let mut connection = Connection::insecure_open(amqp).unwrap();
        let channel = connection.open_channel(None).unwrap();
        Self {
            conn: connection,
            channel,
        }
    }
    pub fn publish_topic(&mut self, exchange_name: &str, context: String, routing_key: &str) {
        let exchange = self
            .channel
            .exchange_declare(
                ExchangeType::Topic,
                exchange_name,
                ExchangeDeclareOptions::default(),
            )
            .unwrap();
        exchange
            .publish(Publish::new(context.as_bytes(), routing_key))
            .unwrap();
        //connection.close();
    }
}

// Monitor 管理
// 账户处理 \ 订单管理 \ 指令集 \ 应答反馈
pub struct MonitorManager {
    pub monitor_num: usize,
    pub monitor_pool: HashMap<String, Recipient<Instruct>>,
    pub acc_handler: QAMongoClient,
    pub order_handler: MQPublish,
    pub ack_handler: MQPublish,
}

impl MonitorManager {
    pub async fn new(monitor_num: usize) -> Self {
        let acc_handler = QAMongoClient::new(CONFIG.account.uri.as_str()).await;
        let order_handler = MQPublish::new(CONFIG.order.uri.as_str());
        let ack_handler = MQPublish::new(CONFIG.ack.uri.as_str());
        Self {
            monitor_num,
            monitor_pool: HashMap::new(),
            acc_handler,
            order_handler,
            ack_handler,
        }
    }
}

impl Actor for MonitorManager {
    type Context = Context<Self>;
    fn started(&mut self, ctx: &mut Self::Context) {
        ctx.set_mailbox_capacity(10000); // 设置邮箱容量
        info!("[Monitor Manager] started.");
    }
}

impl Handler<QifiRsp> for MonitorManager {
    type Result = ();
    fn handle(&mut self, msg: QifiRsp, ctx: &mut Context<Self>) -> Self::Result {
        if msg.t == 0 {
            let acc = self.acc_handler.clone();
            ctx.spawn(
                (async move { acc.save_qifi_slice(msg.data.clone()).await }).into_actor(self),
            );
        } else if msg.t == 1 {
            let acc = self.acc_handler.clone();
            ctx.spawn(
                (async move { acc.save_his_qifi_slice(msg.data.clone()).await }).into_actor(self),
            );
        }
    }
}

impl Handler<QAOrderRsp> for MonitorManager {
    type Result = ();
    fn handle(&mut self, msg: QAOrderRsp, ctx: &mut Context<Self>) -> Self::Result {
        for m in msg.data.iter() {
            let key = m.order.account_cookie.clone();
            let data = serde_json::to_string(&m.to_mt()).unwrap();
            self.order_handler
                .publish_topic(CONFIG.order.exchange.as_str(), data, &key);
        }
    }
}

impl Handler<AddMonitor> for MonitorManager {
    type Result = ();
    fn handle(&mut self, msg: AddMonitor, ctx: &mut Context<Self>) -> Self::Result {
        self.monitor_num -= 1;
        info!(
            "[{}] register; {} not yet",
            msg.account_cookie, self.monitor_num
        );
        self.monitor_pool.insert(msg.account_cookie, msg.rec);
    }
}

impl Handler<Instruct> for MonitorManager {
    type Result = ();
    fn handle(&mut self, msg: Instruct, ctx: &mut Context<Self>) -> Self::Result {
        for (k, r) in &self.monitor_pool {
            if msg.target.contains(k) {
                match r.try_send(msg.clone()) {
                    Ok(_) => {}
                    Err(e) => error!(
                        "[Monitor Manager] pub [{}] instruct fail {}",
                        k,
                        e.to_string()
                    ),
                }
            }
        }
    }
}

impl Handler<Ack> for MonitorManager {
    type Result = ();
    fn handle(&mut self, msg: Ack, ctx: &mut Context<Self>) -> Self::Result {
        match serde_json::to_string(&msg) {
            Ok(data) => {
                self.ack_handler
                    .publish_topic(CONFIG.ack.exchange.as_str(), data, &msg.answerer);
            }
            Err(e) => {
                error!("[Monitor Manager] ack Serialize fail {}", e.to_string())
            }
        }
    }
}

impl Handler<ShowAllMonitor> for MonitorManager {
    type Result = ();
    fn handle(&mut self, msg: ShowAllMonitor, ctx: &mut Self::Context) -> Self::Result {
        info!("Monitors: {:#?}", self.monitor_pool.keys());
    }
}
