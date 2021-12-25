use actix::prelude::*;

use crate::qaenv::localenv::CONFIG;
use crate::qahandlers::realtime::{Realtime, RegisterFactor, RoomMessage};
use crate::qahandlers::state::WSRsp;
use actix_redis::RedisActor;
use std::collections::HashMap;
use std::time::Duration;

pub struct FactorHandler {
    pub realtime_addr: Addr<Realtime>,
}

impl FactorHandler {
    pub fn new(realtime_addr: Addr<Realtime>) -> Self {
        Self { realtime_addr }
    }

    pub fn run_int(&mut self) {
        let sock = WSRsp::ok("xxxxtest", "realtime_pub").to_string();
        self.realtime_addr.do_send(RoomMessage {
            room: "factorx".to_string(),
            msg: sock,
        });
    }
}

impl Actor for FactorHandler {
    type Context = Context<Self>;

    fn started(&mut self, ctx: &mut Self::Context) {
        self.realtime_addr
            .do_send(RegisterFactor(ctx.address().clone()));

        ctx.run_interval(Duration::from_secs(CONFIG.common.qifi_gap), |act, ctx| {
            println!("account_polling query");
            act.run_int();
        });
    }
}
