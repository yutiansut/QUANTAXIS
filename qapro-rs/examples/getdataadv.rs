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
        .get_stock_adv(Vec::from(codelist), "2021-07-11", "2021-12-22", "day")
        .await
        .unwrap();

    println!(
        "qadatastruct {}",
       hisdata.data
    );


}
