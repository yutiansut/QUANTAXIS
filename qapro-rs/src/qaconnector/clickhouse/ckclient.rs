use chrono::prelude::*;
use chrono_tz::Tz;
use std::convert::TryInto;
use std::io;
use std::io::Error;
use std::sync::atomic::AtomicBool;
use std::sync::{Arc, Mutex};

use async_trait::async_trait;
use chrono;
use clickhouse_rs::{Block, Pool};
use serde::Deserialize;
use serde_json::Value;

use self::chrono::Utc;
use crate::qaenv::localenv::CONFIG;
use crate::qaprotocol::mifi::market::{StockDay, StockMin};
use crate::qaprotocol::mifi::qafastkline::{QAColumnBar, QAKlineBase};
use clickhouse_rs::types::Column;
use std::ops::Deref;

type ServerDate = chrono::Date<Tz>;
type ServerDateTime = chrono::DateTime<Tz>;

macro_rules! get {
    ($row: ident, $i: expr, $err: ident) => {
        $row.value($i)?.ok_or_else($err)?;
    };
}

#[derive(Debug)]
pub struct RqBar {
    pub order_book_id: String,
    pub date: ServerDate,
    pub datetime: ServerDate,
    pub open: f32,
    pub high: f32,
    pub low: f32,
    pub close: f32,
    pub num_trades: f32,
    pub limit_up: f32,
    pub limit_down: f32,
    pub volume: f32,
    pub total_turnover: f32,
}

pub struct QACKClient {
    pool: Pool,
}

struct query_ck {
    order_book_id: String,
    start: String,
    end: String,
}

impl QACKClient {
    pub fn init() -> Self {
        let pool = Pool::new(CONFIG.clickhouse.uri.clone());
        Self { pool }
    }
}

#[async_trait]
pub trait DataConnector {
    async fn get_stock(
        &self,
        codelist: Vec<&str>,
        start: &str,
        end: &str,
        freq: &str,
    ) -> Result<QAColumnBar, io::Error>;

    async fn get_future(
        &self,
        codelist: Vec<&str>,
        start: &str,
        end: &str,
        freq: &str,
    ) -> Result<QAColumnBar, io::Error>;

    async fn get_stock_adj(
        &self,
        codelist: Vec<&str>,
        start: &str,
        end: &str,
    ) -> Result<QAColumnBar, io::Error>;
}

#[async_trait]
impl DataConnector for QACKClient {
    async fn get_stock(
        &self,
        codelist: Vec<&str>,
        start: &str,
        end: &str,
        freq: &str,
    ) -> Result<QAColumnBar, io::Error> {
        let mut cursor = self.pool.get_handle().await?;
        let codevar = codelist.join("','");
        let dt = if freq == "1min" { "datetime" } else { "date" };
        let sqlx = format!("SELECT * FROM quantaxis.stock_cn_{} where order_book_id in ['{}'] AND {} BETWEEN '{}' AND '{}' order by {}",freq, codevar,dt, start, end, dt);

        println!("{:#?}", sqlx);
        let mut result = cursor.query(sqlx).fetch_all().await?;

        let mut res: QAColumnBar;
        let openvec: Vec<_> = result.get_column("open")?.iter::<f32>()?.copied().collect();
        let highvec: Vec<_> = result.get_column("high")?.iter::<f32>()?.copied().collect();
        let lowvec: Vec<_> = result.get_column("low")?.iter::<f32>()?.copied().collect();
        let closevec: Vec<_> = result
            .get_column("close")?
            .iter::<f32>()?
            .copied()
            .collect();
        let volumevec: Vec<_> = result
            .get_column("volume")?
            .iter::<f32>()?
            .copied()
            .collect();

        let codevec: Vec<_> = result
            .get_column("order_book_id")?
            .iter::<&[u8]>()?
            .collect();
        let codev: Vec<String> = codevec
            .iter()
            .map(|x| String::from_utf8(x.to_vec()).unwrap())
            .collect();

        let amountvec: Vec<_> = result
            .get_column("total_turnover")?
            .iter::<f32>()?
            .copied()
            .collect();

        let mut ttimevec: Vec<String> = vec![];
        if freq == "day" {
            let timevec: Vec<_> = result.get_column("date")?.iter::<Date<Tz>>()?.collect();

            ttimevec = timevec
                .iter()
                .map(|x| x.to_string()[0..10].parse().unwrap())
                .collect();
        } else {
            let timevec: Vec<_> = result
                .get_column("datetime")?
                .iter::<DateTime<Tz>>()?
                .collect();

            ttimevec = timevec
                .iter()
                .map(|x| x.to_string()[0..19].parse().unwrap())
                .collect();
        }

        res = QAColumnBar {
            datetime: ttimevec,
            code: codev,
            open: openvec.iter().map(|x| *x as f64).collect(),
            high: highvec.iter().map(|x| *x as f64).collect(),
            low: lowvec.iter().map(|x| *x as f64).collect(),
            close: closevec.iter().map(|x| *x as f64).collect(),
            volume: volumevec.iter().map(|x| *x as f64).collect(),
            amount: amountvec.iter().map(|x| *x as f64).collect(),
            frequence: "".to_string(),
            currentidx: 0,
        };
        // for i in range(0..openvec.len()){
        //
        // }
        // let datestr: String = datestr.to_string();
        // let data = QAKlineBase {
        //     datetime: datestr.clone(),
        //     updatetime: datestr.clone(),
        //     code,
        //     open: open as f64,
        //     high: high as f64,
        //     low: low as f64,
        //     close: close as f64,
        //     volume: volume as f64,
        //     amount: amount as f64,
        //     frequence: freq.to_string(),
        //     pctchange: 0.0,
        //     startstamp: 0,
        //     is_last: false,
        // };

        //
        // for row in result.rows() {
        //     let mut datestr:String= String::new();
        //
        //     let code: String = row.get("order_book_id")?;
        //     let open: f32 = row.get("open")?;
        //     let high: f32 = row.get("high")?;
        //     let low: f32 = row.get("low")?;
        //     let close: f32 = row.get("close")?;
        //     let volume: f32 = row.get("volume")?;
        //     let amount: f32 = row.get("total_turnover")?;
        //     println!("{}",amount);
        //     println!("{:?}", row.sql_type(dt));
        //     if freq =="day"{
        //         let date:Option<Date<Tz>> = row.get(dt)?;
        //         let dt= date.unwrap();
        //         datestr =dt.to_string()[0..10].parse().unwrap();
        //
        //     }else{
        //         let date:Option<DateTime<Tz>> = row.get(dt)?;
        //         println!("{:#?}",date);
        //         let dt = "sssssss";
        //         println!("{:#?}",dt);
        //
        //         datestr =dt.to_string()[0..19].parse().unwrap();
        //     }
        //
        //
        //
        //
        //     //println!("{:#?}", date);
        //
        //     res.push(data);
        // }

        Ok(res)
    }

    async fn get_future(
        &self,
        codelist: Vec<&str>,
        start: &str,
        end: &str,
        freq: &str,
    ) -> Result<QAColumnBar, Error> {
        todo!()
    }

    async fn get_stock_adj(
        &self,
        codelist: Vec<&str>,
        start: &str,
        end: &str,
    ) -> Result<QAColumnBar, Error> {
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[cfg(feature = "async_std")]
    #[test]
    fn test_simple() {
        use async_std::task;
        println!("{:#?}", CONFIG.clickhouse.uri);
        async fn execute() -> Result<(), Error> {
            let c = QACKClient::init();

            let codelist = ["000001.XSHE", "000002.XSHE"];
            let b = c
                .exectue(Vec::from(codelist), "2021-01-10", "2021-01-01")
                .await?;
            //assert_eq!(expected, actual);
        }

        task::block_on(execute()).unwrap();
        assert_eq!('1', '1');
    }
}
