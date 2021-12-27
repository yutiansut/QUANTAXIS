use actix_rt;

use qapro_rs::qaconnector::clickhouse::ckclient;
use qapro_rs::qaconnector::clickhouse::ckclient::DataConnector;
use qapro_rs::qadatastruct::stockday::QADataStruct_StockDay;
use qapro_rs::qaenv::localenv::CONFIG;
use qapro_rs::qalog::log4::init_log4;
use qapro_rs::qaprotocol::mifi::qafastkline::QAKlineBase;

use polars::frame::DataFrame;
use polars::prelude::*;
use polars::series::ops::NullBehavior;
use qapro_rs::qadatastruct::stockadj::QADataStruct_StockAdj;
use qapro_rs::qahandlers::realtime::RoomType::Factor;
use rayon::join;
use std::fmt::format;
use std::fs::File;

extern crate stopwatch;

#[actix_rt::main]
async fn main() {
    ///
    /// this example is load cache from cachedir which defined in config.toml/example.toml
    ///
    ///
    /// cachedir/stockday.parquet
    ///
    let c = ckclient::QACKClient::init();

    let stocklist = c.get_stocklist().await.unwrap();

    let cache_file = format!("{}stockdayqfq.parquet", &CONFIG.DataPath.cache);
    let mut sw = stopwatch::Stopwatch::new();
    sw.start();
    let mut qfq = QADataStruct_StockDay::new_from_parquet(cache_file.as_str());
    println!("load cache 2year fullmarket stockdata {:#?}", sw.elapsed());

    let cache_file = format!("{}stockadj.parquet", &CONFIG.DataPath.cache);

    // load factor
    let factor = c
        .get_factor("Asset_LR_Gr", "2019-01-01", "2021-12-25")
        .await
        .unwrap();

    sw.restart();
    let data_with_factor = qfq
        .data
        .join(
            &factor.data,
            &["date", "order_book_id"],
            &["date", "order_book_id"],
            JoinType::Inner,
            None,
        )
        .unwrap();
    println!("join factor_data time {:#?}", sw.elapsed());
    println!("data_with_factor  {:#?}", data_with_factor);

    let rank = data_with_factor
        .groupby("date")
        .unwrap()
        .apply(|x| Ok(x.sort("factor", true).unwrap().head(Some(10))))
        .unwrap()
        .sort(&["date", "order_book_id"], false)
        .unwrap();

    fn write_result(data:DataFrame, path: &str){
        let file = File::create(path).expect("could not create file");

        ParquetWriter::new(file).finish(&data);
    }

    write_result(rank, "./cache/rankres.parquet");

}
