use actix::prelude::*;
use actix_redis::RedisActor;
use chrono::{Local, Timelike};
use log::{error, info, warn};
use rand::StdRng;
use reqwest;
use std::collections::{HashMap, HashSet};

use crate::account::account_handler::{AccountHandler, QIFISub, QIFIUnSub};
use crate::db::redis::flushall;
use crate::future::future_handler::FutureHandler;
use crate::helper::state::WSRsp;
use crate::stock::stock_handler::StockHandler;
use crate::ws::ws_handler::{WSMessage, WebsocketHandler};
use std::time::Duration;

#[derive(Message)]
#[rtype(result = "()")]
pub struct Connect {
    pub id: String,
    pub addr: Addr<WebsocketHandler>,
}

/// 断开连接
#[derive(Message)]
#[rtype(result = "()")]
pub struct Disconnect {
    pub id: String,
}

#[derive(Debug)]
pub enum RoomType {
    Account,
    Future,
    Stock,
}

/// 加入房间 如果room不存在那么创建一个新的.
#[derive(Message)]
#[rtype(result = "bool")]
pub struct Join {
    ///客户端id
    pub id: String,
    /// 房间名字
    pub room: String,
    pub room_type: RoomType,
}

/// 离开房间请求
#[derive(Message, Debug)]
#[rtype(result = "bool")]
pub struct Leave {
    ///客户端id
    pub id: String,
    /// 房间名字
    pub room: String,
    pub room_type: RoomType,
}

/// 发送信息到房间
#[derive(Message, Debug)]
#[rtype(result = "()")]
pub struct RoomMessage {
    pub msg: String,
    pub room: String,
}

#[derive(Message)]
#[rtype(result = "Vec<String>")]
pub struct ListRooms;

#[derive(Message)]
#[rtype(result = "()")]
pub struct RegisterAccount(pub Addr<AccountHandler>);

#[derive(Message)]
#[rtype(result = "()")]
pub struct RegisterFuture(pub Addr<FutureHandler>);

#[derive(Message)]
#[rtype(result = "()")]
pub struct RegisterStock(pub Addr<StockHandler>);

pub struct Realtime {
    // 房间名 对应 id
    rooms: HashMap<String, HashSet<String>>,
    // id 对应 ws
    sessions: HashMap<String, Addr<WebsocketHandler>>,
    rng: StdRng,
    redis_addr: Addr<RedisActor>,
    account_handler: Option<Addr<AccountHandler>>,
    stock_handler: Option<Addr<StockHandler>>,
    future_handler: Option<Addr<FutureHandler>>,
    //
    flushall_ts: i64,
}

impl Realtime {
    pub fn new(redis_addr: Addr<RedisActor>) -> Self {
        let rooms = HashMap::new();
        Self {
            rooms,
            redis_addr,
            sessions: HashMap::new(),
            rng: rand::StdRng::new().unwrap(),
            account_handler: None,
            stock_handler: None,
            future_handler: None,
            flushall_ts: 0,
        }
    }

    /// Send message to all users in the stock/future message
    fn send_message(&self, room: &str, message: String, ctx: &mut Context<Self>) -> bool {
        if let Some(sessions) = self.rooms.get(room) {
            let _ = sessions
                .iter()
                .map(|x| {
                    if let Some(addr) = self.sessions.get(x) {
                        let fut = addr.send(WSMessage(message.to_owned()));
                        ctx.spawn(
                            (async {
                                let _ = fut.await;
                            })
                                .into_actor(self),
                        );
                    }
                })
                .collect::<()>();
            return true;
        }
        false
    }

    fn add_room(&mut self, room_name: String) {
        self.rooms.insert(room_name.clone(), Default::default());
    }

    fn flushall(&mut self) {
        let now = Local::now();
        let hour = now.hour();
        let minute = now.minute();
        if now.timestamp() - self.flushall_ts > 600 && hour == 20 && (minute == 50 || minute == 51)
        {
            flushall(self.redis_addr.clone());
            self.flushall_ts = now.timestamp();
            info!("FLUSHALL");
        }
    }
}

impl Actor for Realtime {
    type Context = Context<Self>;

    fn started(&mut self, ctx: &mut Self::Context) {
        ctx.run_interval(Duration::from_secs(60), |act, ctx| {
            act.flushall();
        });
    }
}

impl Handler<RegisterAccount> for Realtime {
    type Result = ();
    fn handle(&mut self, msg: RegisterAccount, _: &mut Context<Self>) -> Self::Result {
        self.account_handler = Some(msg.0);
    }
}

impl Handler<RegisterFuture> for Realtime {
    type Result = ();
    fn handle(&mut self, msg: RegisterFuture, _: &mut Context<Self>) -> Self::Result {
        self.future_handler = Some(msg.0);
    }
}

impl Handler<RegisterStock> for Realtime {
    type Result = ();
    fn handle(&mut self, msg: RegisterStock, _: &mut Context<Self>) -> Self::Result {
        self.stock_handler = Some(msg.0);
    }
}

/// 处理客户端信息
impl Handler<RoomMessage> for Realtime {
    type Result = ();
    fn handle(&mut self, msg: RoomMessage, ctx: &mut Context<Self>) {
        let ro = msg.room.to_uppercase();
        if !self.send_message(&ro, msg.msg, ctx) {
            self.add_room(ro)
        }
    }
}

/// 为新的连接添加一个新的session并注册id
impl Handler<Connect> for Realtime {
    type Result = ();
    fn handle(&mut self, msg: Connect, _: &mut Context<Self>) -> Self::Result {
        self.sessions.insert(msg.id, msg.addr);
    }
}

/// Handler for Disconnect message.
impl Handler<Disconnect> for Realtime {
    type Result = ();
    fn handle(&mut self, msg: Disconnect, _: &mut Context<Self>) {
        for (_, sessions) in &mut self.rooms {
            sessions.remove(&msg.id);
        }
        self.sessions.remove(&msg.id);
    }
}

impl Handler<Join> for Realtime {
    type Result = bool;
    fn handle(&mut self, msg: Join, ctx: &mut Context<Self>) -> Self::Result {
        let Join {
            id,
            room,
            room_type,
        } = msg;
        let addr = match self.sessions.get(&id) {
            Some(addr) => addr,
            None => {
                warn!("非法sid {:?}", id);
                return false;
            }
        };
        let nt = room.replace('"', "").to_uppercase();
        if let Some(r) = self.rooms.get_mut(&nt) {
            r.insert(id.clone());
        } else {
            let mut r = HashSet::new();
            r.insert(id.clone());
            self.rooms.insert(nt.clone(), r);
        }
        match room_type {
            RoomType::Account => self.account_handler.as_ref().unwrap().do_send(QIFISub {
                account_cookie: nt.clone(),
            }),
            _ => {}
        }
        true
    }
}

/// Handler for Disconnect message.
impl Handler<Leave> for Realtime {
    type Result = bool;
    fn handle(&mut self, msg: Leave, _: &mut Context<Self>) -> Self::Result {
        // 将该地址从房间中移除
        let Leave {
            id,
            room,
            room_type,
        } = msg;
        let nt = room.replace('"', "").to_uppercase();
        if let Some(r) = self.rooms.get_mut(&nt) {
            r.remove(&id);
        }
        match room_type {
            RoomType::Account => self.account_handler.as_ref().unwrap().do_send(QIFIUnSub {
                account_cookie: nt.clone(),
            }),
            _ => {}
        }
        true
    }
}

impl Handler<ListRooms> for Realtime {
    type Result = MessageResult<ListRooms>;
    fn handle(&mut self, _: ListRooms, _: &mut Context<Self>) -> Self::Result {
        let mut rooms = Vec::new();
        for key in self.rooms.keys() {
            rooms.push(key.to_owned())
        }
        MessageResult(rooms)
    }
}
