use actix::Addr;
use actix_redis::{Command, RedisActor};
use actix_web::{web, Error as AWError};
use chrono::Local;
use futures::future::join_all;
use log::{error, info};
use redis_async::{resp::RespValue, resp_array};
use std::str::from_utf8;

pub fn select_db(redis: Addr<RedisActor>, db: u32) {
    let db = db.to_string();
    let fut1 = redis.do_send(Command(resp_array!["select", db]));
}

pub fn flushall(redis: Addr<RedisActor>) {
    let fut1 = redis.do_send(Command(resp_array!["flushall"]));
}

pub fn set_bar(redis: Addr<RedisActor>, key: &str, data: String) {
    info!("write data to redis");
    let fut1 = redis.do_send(Command(resp_array!["set", key, data]));
}

pub async fn set_bar_async(redis: Addr<RedisActor>, key: String, data: String) {
    let keys = key.as_str();
    // info!("async write data to redis");
    redis.send(Command(resp_array!["set", keys, data])).await;
}

pub async fn get_bar(redis: Addr<RedisActor>, key: &str) -> Vec<String> {
    query(redis, Command(resp_array!["get", key])).await
}

pub fn pop_bar(redis: Addr<RedisActor>, key: &str) {
    let fut1 = redis.do_send(Command(resp_array!["RPOP", key]));
}

pub fn put_bar(redis: Addr<RedisActor>, key: &str, data: String) {
    let fut1 = redis.do_send(Command(resp_array!["RPUSH", key, data]));
}

pub async fn query(redis: Addr<RedisActor>, cmd: Command) -> Vec<String> {
    let fut1 = redis.send(cmd).await.unwrap();
    let mut res = Vec::new();
    match fut1 {
        Ok(rv) => match rv {
            RespValue::Array(bs) => {
                let _ = bs
                    .iter()
                    .map(|x| {
                        if let RespValue::BulkString(values) = x {
                            match from_utf8(values.as_ref()) {
                                Ok(x) => res.push(x.to_owned()),
                                _ => {}
                            }
                        }
                    })
                    .collect::<()>();
            }
            RespValue::BulkString(bs) => match from_utf8(bs.as_ref()) {
                Ok(x) => res.push(x.to_owned()),
                _ => {}
            },
            _ => {}
        },
        Err(e) => {
            error!("{:?}", e);
        }
    }
    res
}

pub async fn get_realtime_bar(redis: Addr<RedisActor>, key: String) -> Vec<String> {
    query(redis, Command(resp_array!["LRANGE", key, "0", "-1"])).await
}

pub async fn get_last_bar(redis: Addr<RedisActor>, key: String) -> Vec<String> {
    query(redis, Command(resp_array!["LINDEX", key, "-1"])).await
}

pub async fn get_all_keys(redis: Addr<RedisActor>) -> Vec<String> {
    query(redis, Command(resp_array!["keys", "*"])).await
}
