use actix::Actor;

use actix_redis::RedisActor;
use actix_rt::Arbiter;

use actix_web::{web, App, HttpServer};
use qapro_rs::qaenv::localenv::CONFIG;
use qapro_rs::qahandlers::factorhandler::FactorHandler;
use qapro_rs::qahandlers::realtime::Realtime;
use qapro_rs::qahandlers::subunsub::{realtime_sub, realtime_unsub};
use qapro_rs::qahandlers::websocket::websocket_router;

use qapro_rs::qalog::log4::init_log4;

#[actix_rt::main]
async fn main() -> std::io::Result<()> {
    init_log4("log/qarealtimepro_rs.log");
    println!("{:#?}", &CONFIG.common.addr);
    let redis_addr = RedisActor::start(&CONFIG.redis.uri);
    let realtime_addr = Realtime::new(redis_addr.clone()).start();
    let factor_addr = FactorHandler::new(realtime_addr.clone()).start();
    HttpServer::new(move || {
        App::new()
            .data(realtime_addr.clone())
            .data(factor_addr.clone())
            //.service(web::scope("/ws").route("/", web::get().to(index)))
            .route("/ws/", web::get().to(websocket_router))
            .route("/realtime_sub", web::post().to(realtime_sub))
            .route("/realtime_unsub", web::post().to(realtime_unsub))
    })
    .bind(&CONFIG.common.addr)?
    .run()
    .await
}
