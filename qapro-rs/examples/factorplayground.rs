use actix_rt;

use qapro_rs::qaconnector::clickhouse::ckclient;
use qapro_rs::qaconnector::clickhouse::ckclient::DataConnector;
use qapro_rs::qadatastruct::stockday::QADataStruct_StockDay;
use qapro_rs::qaenv::localenv::CONFIG;

use polars::frame::DataFrame;
use polars::prelude::*;

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
    // let rank3 = rank
    //     .lazy()
    //     //.drop_duplicates(false, Some(vec!["date".to_string(),  "order_book_id".to_string()]))
    //     .sort("date", false)
    //     .groupby([col("order_book_id")])
    //     .agg([
    //         (col("close") / col("close").shift(1))
    //             .list()
    //             .alias("pctchange"),
    //         col("date").list(),
    //         col("close"),
    //         col("factor")
    //     ])
    //     .collect()
    //     .unwrap();

    let rank4 = rank
        .lazy()
        .groupby([col("date")])
        .agg([
            (col("close") / col("high")).list().alias("ch"),
            (col("close") / col("high").shift(1)).list().alias("cpreh"),
            col("order_book_id"),
            col("date").list().alias("datetime"),
            col("close"),
            col("factor"),
        ])
        .sort("date", false)
        .select([
            col("order_book_id"),
            col("datetime"),
            col("close"),
            col("factor"),
        ])
        .collect()
        .unwrap();

    println!("calc lazy time {:#?}", sw.elapsed());
    println!("lazy res {:#?}", rank4);
    // println!(
    //     "rank {}",
    //     rank2.select(&["date", "order_book_id", "close"]).unwrap()
    // );
    //
    //
    let s1 = rank4
        .explode(&["order_book_id", "datetime", "close", "factor"])
        .unwrap();
    println!("res idx1 {:#?}", s1);
    //write_result(rank, "./cache/rankres.parquet");
}
