use actix::prelude::*;

use actix_web::{web, Error, HttpRequest, HttpResponse};
use actix_web_actors::ws;
use log::{error, info, warn};

use serde_json::value::Value;


use uuid::Uuid;

use crate::qaenv::localenv::CONFIG;
use crate::qahandlers::realtime::{Connect, Disconnect, Join, Leave, Realtime, RoomType};
use crate::qahandlers::state::WSRsp;

#[derive(Message)]
#[rtype(result = "()")]
pub struct WSMessage(pub String);

/// 开始心跳处理 同时开始使用actor
pub async fn websocket_router(
    r: HttpRequest,
    stream: web::Payload,
    addr: web::Data<Addr<Realtime>>,
) -> Result<HttpResponse, Error> {
    let res = ws::start(WebsocketHandler::new(addr.get_ref().clone()), &r, stream);
    match res {
        Ok(t) => Ok(t),
        Err(e) => {
            error!("启动ws连接失败{:?}", e);
            Err(e)
        }
    }
}

pub struct WebsocketHandler {
    id: String,
    auth: bool,
    realtime_addr: Addr<Realtime>,
}

impl WebsocketHandler {
    fn new(addr: Addr<Realtime>) -> Self {
        let id = Uuid::new_v4().to_string();
        Self {
            id,
            auth: false,
            realtime_addr: addr,
        }
    }
}

impl Actor for WebsocketHandler {
    type Context = ws::WebsocketContext<Self>;
    fn started(&mut self, ctx: &mut Self::Context) {
        self.realtime_addr.do_send(Connect {
            id: self.id.clone(),
            addr: ctx.address().clone(),
        });
    }
    fn stopped(&mut self, _: &mut Self::Context) {
        warn!("该连接已经退出,{}", self.id);
        self.realtime_addr.do_send(Disconnect {
            id: self.id.clone(),
        });
    }
}

impl Handler<WSMessage> for WebsocketHandler {
    type Result = ();
    fn handle(&mut self, msg: WSMessage, ctx: &mut Self::Context) {
        ctx.text(msg.0);
    }
}

impl StreamHandler<Result<ws::Message, ws::ProtocolError>> for WebsocketHandler {
    fn handle(&mut self, msg: Result<ws::Message, ws::ProtocolError>, ctx: &mut Self::Context) {
        //处理websocket信息
        match msg {
            Ok(ws::Message::Close(_)) => {
                warn!("WS收到断开连接请求, 即将断开连接");
                ctx.stop();
            }
            Ok(ws::Message::Ping(msg)) => {
                info!("Ping> {:?}", msg);
                ctx.pong(&msg);
            }
            Ok(ws::Message::Pong(_)) => {}
            Ok(ws::Message::Text(text)) => {
                info!("Text> {}", text);

                let request: Value = match serde_json::from_str(text.to_string().as_str()) {
                    Ok(x) => x,
                    Err(e) => {
                        error!("{:?}", e.to_string());
                        return ctx.text(e.to_string());
                    }
                };
                if let Some(topic) = request["topic"].as_str() {
                    match topic {
                        //{"topic":"auth","key":"000000000"}
                        "auth" => {
                            let key = request["key"].as_str().unwrap_or("");
                            if CONFIG.common.key.eq(key) {
                                self.auth = true;
                                ctx.text(WSRsp::ok(self.id.clone(), "auth_result").to_string());
                            }
                        }
                        "realtime_sub" => {
                            let room = request["room"].to_string().replace('"', "");
                            self.realtime_addr.do_send(Join {
                                id: self.id.clone(),
                                room,
                                room_type: RoomType::Factor,
                            });
                            ctx.text(
                                WSRsp::ok("success".to_string(), "realtime_sub_result").to_string(),
                            );
                        }
                        // 处理取消订阅行情{"topic":"realtime_unsub","room":"stock_SZ_000001$*$1min"}
                        "realtime_unsub" => {
                            let room = request["room"].to_string().replace('"', "");
                            self.realtime_addr.do_send(Leave {
                                id: self.id.clone(),
                                room,
                                room_type: RoomType::Factor,
                            });
                            ctx.text(
                                WSRsp::ok("success".to_string(), "realtime_unsub_result")
                                    .to_string(),
                            );
                        }
                        _ => {}
                    }
                }
            }
            Err(e) => {
                warn!("连接出现错误,原因: {:?}", e);
                ctx.stop()
            }
            _ => {
                warn!("WS消息未匹配,即将断开连接");
                ctx.stop()
            }
        }
    }
}
