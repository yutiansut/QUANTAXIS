use crate::qaprotocol::mifi::qafastkline::QAKlineBase;
use crate::qaruntime::base::{MQAddr, QAKline};
use crate::qaruntime::qamanagers::mq_manager::MQManager;
use actix::prelude::*;
use actix::{Actor, Addr, Context, Handler, Recipient};
use amiquip::{
    Channel, Connection, ConsumerMessage, ConsumerOptions, Exchange, ExchangeDeclareOptions,
    ExchangeType, FieldTable, Publish, QueueDeclareOptions, Result,
};
use log::{error, info, warn};
use serde_json::Value;

trait Attach {
    fn init_data(&mut self, data: Value);
    fn update(&mut self, data: Value);
}

impl Attach for QAKlineBase {
    fn init_data(&mut self, data: Value) {
        self.datetime = data["datetime"].as_str().unwrap().parse().unwrap();
        self.updatetime = data["datetime"].as_str().unwrap().parse().unwrap();
        self.code = data["symbol"].as_str().unwrap().parse().unwrap();
        self.open = data["last_price"].as_f64().unwrap();
        self.high = data["last_price"].as_f64().unwrap();
        self.low = data["last_price"].as_f64().unwrap();
        self.close = data["last_price"].as_f64().unwrap();
        self.volume = data["volume"].as_f64().unwrap();
    }

    fn update(&mut self, data: Value) {
        if self.open == 0.0 {
            self.init_data(data.clone());
        }
        let new_price = data["last_price"].as_f64().unwrap();
        if self.high < new_price {
            self.high = new_price;
        }
        if self.low > new_price {
            self.low = new_price;
        }
        self.close = new_price;
        let cur_datetime: String = data["datetime"].as_str().unwrap().parse().unwrap();
        self.updatetime = cur_datetime.clone();
    }
}

// 订阅结构体
#[derive(Debug, Message)]
#[rtype(result = "()")]
pub struct Subscribe(pub Recipient<QAKline>);

#[derive(Debug, Message)]
#[rtype(result = "()")]
pub struct Start;

// MarketMQ 行情订阅与分发
pub struct MarketMQ {
    pub amqp: String,
    pub exchange: String,
    pub model: String,
    pub routing_key: String,
    // connection:
    pub subscribers: Vec<Recipient<QAKline>>,
    pub mqm: Addr<MQManager>,
}

impl MarketMQ {
    pub fn new(
        amqp: String,
        exchange: String,
        model: String,
        routing_key: String,
        mqm: Addr<MQManager>,
    ) -> Self {
        Self {
            amqp,
            exchange,
            model,
            routing_key,
            subscribers: Vec::new(),
            mqm,
        }
    }
    pub fn notify(&self, bar: QAKlineBase) {
        for subscr in &self.subscribers {
            match subscr.try_send(QAKline { data: bar.clone() }) {
                Err(e) => error!("[{}] notify fail {}", self.routing_key, e.to_string()),
                _ => {}
            }
        }
    }
    pub fn consume_direct(&self) -> Result<()> {
        let mut connection = Connection::insecure_open(&self.amqp)?;
        let channel = connection.open_channel(None)?;
        let exchange = channel.exchange_declare(
            ExchangeType::Direct,
            &self.exchange,
            ExchangeDeclareOptions {
                durable: false,
                auto_delete: false,
                internal: false,
                arguments: Default::default(),
            },
        )?;
        let queue = channel.queue_declare(
            "",
            QueueDeclareOptions {
                exclusive: true,
                ..QueueDeclareOptions::default()
            },
        )?;
        info!("[{}] Receiving...", self.routing_key);

        queue.bind(&exchange, self.routing_key.clone(), FieldTable::new())?;

        let consumer = queue.consume(ConsumerOptions {
            no_ack: true,
            ..ConsumerOptions::default()
        })?;

        for (_i, message) in consumer.receiver().iter().enumerate() {
            match message {
                ConsumerMessage::Delivery(delivery) => {
                    let msg = delivery.body.clone();
                    let foo = String::from_utf8(msg).unwrap();
                    let data = foo.to_string();
                    let kdata: Value = serde_json::from_str(&data).unwrap();
                    let mut kbar = QAKlineBase::init();
                    kbar.init_data(kdata);
                    // 未重采样Bar
                    self.notify(kbar.clone());
                }
                other => {
                    warn!("Consumer ended: {:?}", other);
                    break;
                }
            }
        }
        connection.close()
    }
}

impl Actor for MarketMQ {
    type Context = Context<Self>;
    fn started(&mut self, ctx: &mut Self::Context) {
        ctx.set_mailbox_capacity(1000); // 设置邮箱容量
        match self.mqm.try_send(MQAddr {
            key: self.routing_key.clone(),
            addr: ctx.address().clone(),
        }) {
            Err(e) => error!("[{}] register fail {}", self.routing_key, e.to_string()),
            _ => {}
        }
    }
}

impl Handler<Subscribe> for MarketMQ {
    type Result = ();

    fn handle(&mut self, msg: Subscribe, _: &mut Self::Context) {
        self.subscribers.push(msg.0);
    }
}

impl Handler<Start> for MarketMQ {
    type Result = ();
    fn handle(&mut self, msg: Start, ctx: &mut Self::Context) -> Self::Result {
        self.consume_direct();
    }
}
