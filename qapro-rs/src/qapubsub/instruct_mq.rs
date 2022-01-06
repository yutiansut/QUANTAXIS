use crate::qaruntime::base::Instruct;
use crate::qaruntime::qamanagers::monitor_manager::MonitorManager;


use actix::{Actor, Addr, Context};
use amiquip::{
    Channel, Connection, ConsumerMessage, ConsumerOptions, Exchange, ExchangeDeclareOptions,
    ExchangeType, FieldTable, Publish, QueueDeclareOptions, Result,
};
use log::{error, info, warn};

// 指令接收

pub struct InstructMQ {
    pub amqp: String,
    pub exchange: String,
    pub model: String,
    pub routing_key: String,
    // connection:
    pub morm: Addr<MonitorManager>,
}

impl InstructMQ {
    fn consume_direct(&self) -> Result<()> {
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
        info!("[InstructMQ] Start at <{}> ", self.routing_key);

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
                    match serde_json::from_str(&data) {
                        Ok(v) => match self.morm.try_send::<Instruct>(v) {
                            Ok(_) => {}
                            Err(e) => {
                                error!("[Monitor Manager] send instruct fail {}", e.to_string())
                            }
                        },
                        Err(e) => error!("[Monitor Manager] Instruct parse fail {}", e.to_string()),
                    }
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

impl Actor for InstructMQ {
    type Context = Context<Self>;
    fn started(&mut self, ctx: &mut Self::Context) {
        ctx.set_mailbox_capacity(1000); // 设置邮箱容量
        self.consume_direct();
    }
}
