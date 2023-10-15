use actix_rt;

use qapro_rs::qaconnector::clickhouse::ckclient;
use qapro_rs::qaconnector::clickhouse::ckclient::DataConnector;
use qapro_rs::qadatastruct::stockday::QADataStruct_StockDay;
use qapro_rs::qaenv::localenv::CONFIG;
use qapro_rs::qalog::log4::init_log4;
use qapro_rs::qaprotocol::mifi::qafastkline::QAKlineBase;

use polars::prelude::{ChunkCompare, RollingOptions};
use polars::series::ops::NullBehavior;
use std::fmt::format;

#[actix_rt::main]
async fn main() {
    let c = ckclient::QACKClient::init();
    let factor = c
        .get_factor("Asset_LR_Gr", "2021-01-01", "2021-10-01")
        .await
        .unwrap();
    println!("{:#?}", factor.data);
}
