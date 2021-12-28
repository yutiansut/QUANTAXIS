use actix_rt;

use qapro_rs::qaconnector::clickhouse::ckclient;
use qapro_rs::qaconnector::clickhouse::ckclient::DataConnector;
use qapro_rs::qadatastruct::stockday::QADataStruct_StockDay;
use qapro_rs::qaenv::localenv::CONFIG;
use qapro_rs::qalog::log4::init_log4;
use qapro_rs::qaprotocol::mifi::qafastkline::QAKlineBase;

use polars::frame::DataFrame;
use polars::prelude::*;

use actix::fut::ok;
use polars::series::ops::NullBehavior;
use qapro_rs::qadatastruct::stockadj::QADataStruct_StockAdj;
use qapro_rs::qahandlers::realtime::RoomType::Factor;
use rayon::join;
use redis::Value::Data;
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

    //let stocklist = c.get_stocklist().await.unwrap();
    //let stocklist = c.get_stocklist().await.unwrap();

    let cache_file = format!("{}stockdayqfq.parquet", &CONFIG.DataPath.cache);
    let mut sw = stopwatch::Stopwatch::new();
    sw.start();
    let mut qfq = QADataStruct_StockDay::new_from_parquet(cache_file.as_str());
    println!("load cache 2year fullmarket stockdata {:#?}", sw.elapsed());
    println!("data  {:#?}", qfq.data);
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
        .unwrap()
        .drop_duplicates(
            false,
            Some(&["date".to_string(), "order_book_id".to_string()]),
        )
        .unwrap();
    println!("join factor_data time {:#?}", sw.elapsed());
    println!("data_with_factor  {:#?}", data_with_factor);

    sw.restart();
    let rank = data_with_factor
        .groupby("date")
        .unwrap()
        .apply(|x| Ok(x.sort("factor", true).unwrap().head(Some(40))))
        .unwrap()
        .sort(&["date", "order_book_id"], false)
        .unwrap();
    println!("analysis factor_data time {:#?}", sw.elapsed());
    fn write_result(data: DataFrame, path: &str) {
        let file = File::create(path).expect("could not create file");

        ParquetWriter::new(file).finish(&data);
    }

    trait pct {
        fn pctchange(&self, n: usize) -> Series;
    }
    impl pct for Series {
        fn pctchange(&self, n: usize) -> Series {
            self / &self.shift(n as i64)
        }
    }

    fn closepctchange(close: &Series) -> Series {
        close.pctchange(1)
    }
    sw.restart();
    let rank2 = rank
        .groupby("order_book_id")
        .unwrap()
        .apply(|mut x| {
            let res = x
                .sort("date", false)
                .unwrap()
                .apply("close", closepctchange)
                .unwrap()
                .clone();
            //println!("rank {}", rank["close"]);
            Ok(res)
        })
        .unwrap()
        .sort("date", false)
        .unwrap()
        .drop_nulls(Some(&["close".to_string()]))
        .unwrap();
    println!("calc time {:#?}", sw.elapsed());
    sw.restart();
    let rank3 = rank
        .lazy()
        //.drop_duplicates(false, Some(vec!["date".to_string(),  "order_book_id".to_string()]))
        .sort("date", false)
        .groupby([col("order_book_id")])
        .agg([(col("close") / col("close").shift(1)).list().alias("pctchange"), col("date").list()])
        .collect()
        .unwrap();
    println!("calc lazy time {:#?}", sw.elapsed());
    println!(
        "rank {}",
        rank2.select(&["date", "order_book_id", "close"]).unwrap()
    );

    println!(
        "rank lazy {}",
        rank3
    );
    //write_result(rank, "./cache/rankres.parquet");
}
