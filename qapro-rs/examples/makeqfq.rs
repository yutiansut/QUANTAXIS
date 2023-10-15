use actix_rt;

use qapro_rs::qaconnector::clickhouse::ckclient;
use qapro_rs::qaconnector::clickhouse::ckclient::DataConnector;
use qapro_rs::qadatastruct::stockday::QADataStruct_StockDay;
use qapro_rs::qaenv::localenv::CONFIG;

use polars::frame::DataFrame;
use polars::prelude::{col, ChunkCompare, IntoLazy, JoinType, RollingOptions};
use polars::series::ops::NullBehavior;
use qapro_rs::qadatastruct::stockadj::QADataStruct_StockAdj;

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

    let cache_file = format!("{}stockday.parquet", &CONFIG.DataPath.cache);
    let mut sw = stopwatch::Stopwatch::new();
    sw.start();
    let mut data = QADataStruct_StockDay::new_from_parquet(cache_file.as_str());
    println!("load cache 2year fullmarket stockdata {:#?}", sw.elapsed());

    let cache_file = format!("{}stockadj.parquet", &CONFIG.DataPath.cache);
    let mut adj = QADataStruct_StockAdj::new_from_parquet(cache_file.as_str());

    /// join data
    ///
    ///
    ///
    let mut sw = stopwatch::Stopwatch::new();
    sw.start();
    let joindata = data
        .data
        .join(
            &adj.data,
            &["date", "order_book_id"],
            &["date", "order_book_id"],
            JoinType::Inner,
            None,
        )
        .unwrap();
    //println!("join data {:#?}", joindata);

    let qfq = joindata
        .lazy()
        .with_columns(vec![
            col("open") * col("adj"),
            col("high") * col("adj"),
            col("low") * col("adj"),
            col("close") * col("adj"),
            col("limit_up") * col("adj"),
            col("limit_down") * col("adj"),
        ])
        .drop_duplicates(
            false,
            Some(vec!["date".to_string(), "order_book_id".to_string()]),
        )
        .collect()
        .unwrap();
    println!("run qfq calc {:#?}", sw.elapsed());
    println!("qfq data {:#?}", qfq);

    let mut qfqstruct = QADataStruct_StockDay { data: qfq };
    qfqstruct
        .save_selfdefined_cache(format!("{}stockdayqfq.parquet", CONFIG.DataPath.cache).as_str());
}
