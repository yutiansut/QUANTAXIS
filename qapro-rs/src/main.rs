extern crate chrono_tz;

use std::collections::HashMap;

use actix::Actor;
use actix_rt;
use actix_rt::Arbiter;
use chrono::Local;

use serde_json::Value;

use qapro_rs::launchstrategy;

use qapro_rs::qaconnector::clickhouse::ckclient;
use qapro_rs::qaconnector::clickhouse::ckclient::DataConnector;
use qapro_rs::qaenv::localenv::CONFIG;
use qapro_rs::qalog::log4::init_log4;
use qapro_rs::qaprotocol::mifi::qafastkline::QAKlineBase;
use qapro_rs::qapubsub::{instruct_mq::InstructMQ, market_mq::MarketMQ};
use qapro_rs::qaruntime::{
    base::MarketSubscribe,
    monitor::Monitor,
    qacontext::QAContext,
    qamanagers::{monitor_manager::MonitorManager, mq_manager::MQManager},
};
use qapro_rs::qastrategy::t00;

use qapro_rs::qautil::tradedate::get_n_day_before_date9;

#[actix_rt::main]
async fn main() {
    let c = ckclient::QACKClient::init();

    let codelist = ["600010.XSHG", "300002.XSHE"];
    let hisdata = c
        .get_stock(Vec::from(codelist), "2021-07-11", "2021-12-22", "day")
        .await
        .unwrap();
    //println!("{:#?}",hisdata.to_kline());

    println!(
        "QARUNTIME Start: {}",
        Local::now().format("%Y-%m-%d %H:%M:%S").to_string()
    );
    // let system = System::new("awesome");
    init_log4(&CONFIG.cli.log_path);
    let names: Vec<String> = CONFIG.cli.name.clone();
    let codes: Vec<String> = CONFIG.cli.codes.clone();
    let frequences: Vec<String> = CONFIG.cli.freqs.clone();
    let json: Value = serde_json::from_str(&format!(r#"{}"#, CONFIG.cli.params.clone()))
        .unwrap_or(Value::String("{\"\":\"\"}".to_owned()));

    let count = names.len() * codes.len() * frequences.len();
    // 初始化 MarketMQ 管理
    let mqm_addr = MQManager::new(count).start();
    // 初始化 Monitor管理
    let morm_addr = MonitorManager::new(count).await.start();

    let cash_map: HashMap<String, f64> =
        serde_json::from_str(&format!(r#"{}"#, CONFIG.accsetup.cash_map)).unwrap();
    let _backtest_start = get_n_day_before_date9(20);

    let mut all_hisdata: HashMap<String, Vec<QAKlineBase>> = HashMap::new();
    for code in codes.iter() {
        for frequence in frequences.iter() {
            all_hisdata.insert(format!("mongo_{}_{}", code, frequence), hisdata.to_kline());
            all_hisdata.insert(format!("redis_{}_{}", code, frequence), vec![]);
        }
    }

    let morm = morm_addr.clone();
    let arb = Arbiter::new();

    InstructMQ::start_in_arbiter(&arb.handle(), move |_| InstructMQ {
        amqp: CONFIG.instruct.uri.clone(),
        exchange: CONFIG.instruct.exchange.clone(),
        routing_key: CONFIG.instruct.routing_key.clone(),
        model: "direct".to_string(),
        morm,
    });
    for code in codes.iter() {
        // 初始化mq
        let mqm = mqm_addr.clone();
        let mc = code.clone();
        let arc = Arbiter::new();

        MarketMQ::start_in_arbiter(&arc.handle(), move |_| {
            MarketMQ::new(
                CONFIG.realtime.uri.clone(),
                CONFIG.realtime.exchange.clone(),
                "direct".to_string(),
                mc.to_string(),
                mqm,
            )
        });
    }
    for name in names.iter() {
        println!("names: {:#?}", name);
        for code in codes.iter() {
            for frequence in frequences.iter() {
                let mkey = format!("mongo_{}_{}", code, frequence);
                let rkey = format!("redis_{}_{}", code, frequence);
                let cookie = format!(
                    "{}_{}_{}_{}",
                    CONFIG.accsetup.symbol.as_str(),
                    name,
                    code,
                    frequence
                );
                let mut ctx = QAContext::new(cookie.as_ref(), frequence, code, "real".to_string());
                let initcash = cash_map.get(code).unwrap_or(&CONFIG.accsetup.default)
                    * CONFIG.accsetup.multiply;
                ctx.acc.set_init_cash(initcash);
                println!("mkey: {:#?}", mkey);
                launchstrategy!(name.as_str();
                code;
                json.get(&name);
                ctx;
                morm_addr.clone();
                mqm_addr.clone();
                all_hisdata.get(&mkey).unwrap();
                all_hisdata.get(&rkey).unwrap();
                 t00
                 );
            }
        }
    }
    //
    all_hisdata.clear();
    println!("all histdata is cleaned");
    // system.run();

    let (_tx, rx) = futures::channel::oneshot::channel::<()>();
    rx.await.unwrap();
}
