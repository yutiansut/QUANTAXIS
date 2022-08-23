use crate::qahandlers::realtime::{Join, Leave, Realtime, RoomType};
use crate::qahandlers::state::Rsp;
use actix::Addr;

use actix_web::{web, HttpRequest, HttpResponse};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Clone, Debug, Deserialize)]
pub struct SubscribeForm {
    pub sid: String,
    pub room: String,
}

#[derive(Serialize, Clone, Debug, Deserialize)]
pub struct UnSubscribeForm {
    pub sid: String,
    pub room: String,
}

pub async fn realtime_sub(
    r: HttpRequest,
    form: web::Json<UnSubscribeForm>,
    addr: web::Data<Addr<Realtime>>,
) -> HttpResponse {
    if let Ok(res) = addr
        .send(Join {
            id: form.sid.clone(),
            room: form.room.clone(),
            room_type: RoomType::Factor,
        })
        .await
    {
        if res {
            return HttpResponse::Ok().json(Rsp::ok("", "订阅成功"));
        }
    }
    HttpResponse::Ok().json(Rsp::fail("", "订阅失败"))
}

pub async fn realtime_unsub(
    r: HttpRequest,
    form: web::Json<UnSubscribeForm>,
    addr: web::Data<Addr<Realtime>>,
) -> HttpResponse {
    if let Ok(res) = addr
        .send(Leave {
            id: form.sid.clone(),
            room: form.room.clone(),
            room_type: RoomType::Factor,
        })
        .await
    {
        if res {
            return HttpResponse::Ok().json(Rsp::ok("", "取消订阅成功"));
        }
    }
    HttpResponse::Ok().json(Rsp::fail("", "取消订阅失败"))
}
