extern crate stopwatch;

use std::fs::File;

use actix_rt;
use polars::frame::DataFrame;
use polars::prelude::*;

use itertools::izip;
use rand::prelude::*;

use qapro_rs::qaaccount::account::QA_Account;
use qapro_rs::qadatastruct::stockday::QADataStruct_StockDay;
use qapro_rs::qaenv::localenv::CONFIG;

#[actix_rt::main]
async fn main() {
    let cache_file = format!("{}stockdayqfq.parquet", &CONFIG.DataPath.cache);
    let mut sw = stopwatch::Stopwatch::new();
    sw.start();
    let mut qfq = QADataStruct_StockDay::new_from_parquet(cache_file.as_str());
    println!("load cache 2year fullmarket stockdata {:#?}", sw.elapsed());
    println!("data  {:#?}", qfq.data.get_row(1).0);

    // load factor
    sw.restart();
    let rank4 = qfq
        .data
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
        ])
        .select([
            col("order_book_id"),
            col("date"),
            col("close"),
            col("open"),
            col("limit_up"),
            col("limit_down"),
            col("pct"),
        ])
        .explode(vec![
            col("date"),
            col("close"),
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

    let mut acc = QA_Account::new("test", "test", "test", 1000000000.0, false, "backtest");
    let mut curdate = "";
    sw.restart();

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
    acc.to_csv("".to_string());

    println!("calc get row time {:#?}", sw.elapsed());
}
