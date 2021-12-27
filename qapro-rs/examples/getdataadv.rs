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

    let codelist = ["600010.XSHG", "300002.XSHE"];
    let mut hisdata = c
        .get_stock_adv(Vec::from(codelist), "2021-07-11", "2021-12-22", "day")
        .await
        .unwrap();

    println!("qadatastruct {}", hisdata.data);
    hisdata.save_cache();

    let cache_file = format!("{}stockday.parquet", &CONFIG.DataPath.cache);

    let mut data = QADataStruct_StockDay::new_from_parquet(cache_file.as_str());

    println!("load cache file {:#?}", data.data);

    println!(
        "groupby test {:#?}",
        data.data.groupby("date").unwrap().select("close").mean()
    );
    println!(
        "groupby test {:#?}",
        data.data
            .groupby("order_book_id")
            .unwrap()
            .select("close")
            .mean()
    );

    println!(
        "diff test {:#?}",
        data.data["high"].diff(1, NullBehavior::Drop)
    );

    let selectdf = data.query_code("300002.XSHE");
    println!("select df {:#?}", selectdf);
    let close = &selectdf["close"];
    let lastclose = close.diff(1, NullBehavior::Ignore);
    println!("pct test {:#?}", close / &lastclose);

    let ma20 = close
        .rolling_mean(RollingOptions {
            window_size: 5,
            min_periods: 1,
            weights: None,
            center: false,
        })
        .unwrap();
    println!("rolling mean test {:#?}", ma20);
}
