extern crate stopwatch;

use std::fs::File;

use actix_rt;
use polars::frame::DataFrame;
use polars::prelude::*;
use polars::series::ops::NullBehavior;

use itertools::izip;
use qapro_rs::qaaccount::account::QA_Account;
use qapro_rs::qaconnector::clickhouse::ckclient;
use qapro_rs::qaconnector::clickhouse::ckclient::DataConnector;
use qapro_rs::qadatastruct::stockday::QADataStruct_StockDay;
use qapro_rs::qaenv::localenv::CONFIG;

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
    println!("data  {:#?}", qfq.data.get_row(1).0);
    // println!("data  {:#?}", qfq.data.transpose());

    let cache_file = format!("{}stockadj.parquet", &CONFIG.DataPath.cache);

    // trait qatrans {
    //     fn transform_qadatastruct(data:DataFrame) -> Vec<QAKlineBase>;
    // }
    // impl  qatrans for DataFrame{
    //     fn transform_qadatastruct(data:DataFrame) -> Vec<QAKlineBase>{
    //         data.get_row(0)
    //     }
    // }

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
        .groupby(["date"])
        .unwrap()
        .apply(|x| Ok(x.sort(["factor"], true).unwrap().head(Some(40))))
        .unwrap()
        .sort(["date", "order_book_id"], false)
        .unwrap();

    println!("analysis factor_data time {:#?}", sw.elapsed());
    fn write_result(data: DataFrame, path: &str) {
        let file = File::create(path).expect("could not create file");

        ParquetWriter::new(file).finish(&data);
    }

    sw.restart();

    let rank4 = rank
        .sort(["date"], false)
        .unwrap()
        .lazy()
        .groupby([col("order_book_id")])
        .agg([
            col("close").pct_change(1).alias("pct"),
            col("date"),
            col("close"),
            col("open"),
            col("limit_up"),
            col("limit_down"),
            col("factor"),
        ])
        .select([
            col("order_book_id"),
            col("date"),
            col("close"),
            col("factor"),
            col("open"),
            col("limit_up"),
            col("limit_down"),
            col("pct"),
        ])
        .explode(vec![
            col("date"),
            col("close"),
            col("factor"),
            col("open"),
            col("limit_up"),
            col("limit_down"),
            col("pct"),
        ])
        .sort("date", false)
        .collect()
        .unwrap();

    println!("calc lazy time {:#?}", sw.elapsed());
    println!("lazy res {:#?}", rank4);

    let closes = rank4["close"].f32().unwrap();
    let codes = rank4["order_book_id"].utf8().unwrap();
    let dates = rank4["date"].utf8().unwrap();
    sw.restart();

    let mut acc = QA_Account::new("test2", "test", "test", 1000000000.0, false, "backtest");
    let mut curdate = "";
    for (code, date, close) in izip!(codes, dates, closes) {
        let code2: &str = code.unwrap();
        let date2: &str = date.unwrap();
        let close2: f32 = close.unwrap();
        if curdate != date2 {
            acc.settle();
            curdate = date2;
        } else {
            let posx = acc.get_position(code2);
            match posx {
                Some(pos) => {
                    if pos.volume_long_his > 0.0 {
                        acc.sell(code2, 100.0, date2, close2 as f64);
                    } else {
                        if rand::random() {
                            acc.buy(code2, 100.0, date2, close2 as f64);
                        }
                    }
                }
                _ => {
                    acc.init_h(code2);
                }
            }
        }
    }

    println!("calc get row time {:#?}", sw.elapsed());
    let _  = acc.to_csv("vv".to_string()).unwrap();
}
