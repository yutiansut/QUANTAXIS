use actix_rt;
use chrono::Local;
use qapro_rs::qaconnector::clickhouse::ckclient;
use qapro_rs::qaconnector::clickhouse::ckclient::DataConnector;
use qapro_rs::qaenv::localenv::CONFIG;
use qapro_rs::qalog::log4::init_log4;
use qapro_rs::qaprotocol::mifi::qafastkline::QAKlineBase;
use qapro_rs::qautil::tradedate::get_n_day_before_date9;
use serde_json::Value;
use std::collections::HashMap;
#[actix_rt::main]
async fn main() {
    let c = ckclient::QACKClient::init();

    let codelist = ["600010.XSHG", "300002.XSHE"];
    let hisdata = c
        .get_stock(Vec::from(codelist), "2021-07-11", "2021-12-22", "day")
        .await
        .unwrap();

    println!(
        "QARUNTIME Start: {}",
        Local::now().format("%Y-%m-%d %H:%M:%S").to_string()
    );

    init_log4(&CONFIG.cli.log_path);
    let names: Vec<String> = CONFIG.cli.name.clone();
    let codes: Vec<String> = CONFIG.cli.codes.clone();
    let frequences: Vec<String> = CONFIG.cli.freqs.clone();
    let json: Value = serde_json::from_str(&format!(r#"{}"#, CONFIG.cli.params.clone()))
        .unwrap_or(Value::String("{\"\":\"\"}".to_owned()));

    let count = names.len() * codes.len() * frequences.len();
    // 初始化 MarketMQ 管理

    let mut cash_map: HashMap<String, f64> =
        serde_json::from_str(&format!(r#"{}"#, CONFIG.accsetup.cash_map)).unwrap();
    let backtest_start = get_n_day_before_date9(20);

    let mut all_hisdata: HashMap<String, Vec<QAKlineBase>> = HashMap::new();
    for code in codes.iter() {
        for frequence in frequences.iter() {
            all_hisdata.insert(format!("mongo_{}_{}", code, frequence), hisdata.to_kline());
            all_hisdata.insert(format!("redis_{}_{}", code, frequence), vec![]);
        }
    }
}
