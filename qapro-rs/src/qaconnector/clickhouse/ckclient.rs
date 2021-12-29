use chrono::prelude::*;
use chrono_tz::Tz;

use std::io;
use std::io::Error;

use async_trait::async_trait;
use chrono;
use clickhouse_rs::Pool;

use crate::qadatastruct::factorstruct::QADataStruct_Factor;
use crate::qadatastruct::stockadj::QADataStruct_StockAdj;
use crate::qadatastruct::stockday::QADataStruct_StockDay;

use crate::qadatastruct::stocklist::QADataStruct_StockList;
use crate::qaenv::localenv::CONFIG;

use crate::qaprotocol::mifi::qafastkline::QAColumnBar;

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
    async fn get_stocklist(&self) -> Result<Vec<String>, io::Error>;
    async fn get_stocklist_adv(&self) -> Result<QADataStruct_StockList, io::Error>;
    async fn get_stock(
        &self,
        codelist: Vec<&str>,
        start: &str,
        end: &str,
        freq: &str,
    ) -> Result<QAColumnBar, io::Error>;
    async fn get_stock_adv(
        &self,
        codelist: Vec<&str>,
        start: &str,
        end: &str,
        freq: &str,
    ) -> Result<QADataStruct_StockDay, io::Error>;

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
    ) -> Result<QADataStruct_StockAdj, io::Error>;

    async fn get_factor(
        &self,
        factorname: &str,
        start: &str,
        end: &str,
    ) -> Result<QADataStruct_Factor, io::Error>;
}

#[async_trait]
impl DataConnector for QACKClient {
    async fn get_stocklist(&self) -> Result<Vec<String>, Error> {
        let mut cursor = self.pool.get_handle().await?;
        let sqlx = format!("SELECT * FROM quantaxis.stock_cn_codelist where status=='Active'");
        let mut result = cursor.query(sqlx).fetch_all().await?;

        let codevec: Vec<_> = result
            .get_column("order_book_id")?
            .iter::<&[u8]>()?
            .collect();
        let codev: Vec<String> = codevec
            .iter()
            .map(|x| String::from_utf8(x.to_vec()).unwrap())
            .collect();
        Ok(codev)
    }

    async fn get_stocklist_adv(&self) -> Result<QADataStruct_StockList, Error> {
        let mut cursor = self.pool.get_handle().await?;
        let sqlx = format!("SELECT * FROM quantaxis.stock_cn_codelist where status=='Active'");
        let mut result = cursor.query(sqlx).fetch_all().await?;

        let codevec: Vec<_> = result
            .get_column("order_book_id")?
            .iter::<&[u8]>()?
            .collect();
        let codev: Vec<String> = codevec
            .iter()
            .map(|x| String::from_utf8(x.to_vec()).unwrap())
            .collect();
        let symbol: Vec<_> = result.get_column("symbol")?.iter::<&[u8]>()?.collect();
        let symbolvec: Vec<String> = symbol
            .iter()
            .map(|x| String::from_utf8(x.to_vec()).unwrap())
            .collect();

        let listed_date: Vec<_> = result.get_column("listed_date")?.iter::<&[u8]>()?.collect();
        let listed_datevec: Vec<String> = listed_date
            .iter()
            .map(|x| String::from_utf8(x.to_vec()).unwrap())
            .collect();

        let delist_date: Vec<_> = result.get_column("delist_date")?.iter::<&[u8]>()?.collect();
        let delist_datevec: Vec<String> = delist_date
            .iter()
            .map(|x| String::from_utf8(x.to_vec()).unwrap())
            .collect();
        Ok(QADataStruct_StockList::new_from_vec(
            codev,
            listed_datevec,
            delist_datevec,
            symbolvec,
        ))
    }

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
        let result = cursor.query(sqlx).fetch_all().await?;

        let res: QAColumnBar;
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

        Ok(res)
    }
    async fn get_stock_adv(
        &self,
        codelist: Vec<&str>,
        start: &str,
        end: &str,
        freq: &str,
    ) -> Result<QADataStruct_StockDay, io::Error> {
        let mut cursor = self.pool.get_handle().await?;
        let codevar = codelist.join("','");
        let dt = if freq == "1min" { "datetime" } else { "date" };
        let sqlx = format!("SELECT * FROM quantaxis.stock_cn_{} where order_book_id in ['{}'] AND {} BETWEEN '{}' AND '{}' ",freq, codevar,dt, start, end);

        println!("{:#?}", sqlx);
        let result = cursor.query(sqlx).fetch_all().await?;

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
        };
        let limitupvec: Vec<_> = result
            .get_column("limit_up")?
            .iter::<f32>()?
            .copied()
            .collect();
        let limitdownvec: Vec<_> = result
            .get_column("limit_down")?
            .iter::<f32>()?
            .copied()
            .collect();
        let numtradesvec: Vec<_> = result
            .get_column("num_trades")?
            .iter::<f32>()?
            .copied()
            .collect();

        let res = QADataStruct_StockDay::new_from_vec(
            ttimevec,
            codev,
            openvec,
            highvec,
            lowvec,
            closevec,
            limitupvec,
            limitdownvec,
            numtradesvec,
            volumevec,
            amountvec,
        );
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
    ) -> Result<QADataStruct_StockAdj, Error> {
        let mut cursor = self.pool.get_handle().await?;
        let codevar = codelist.join("','");
        let sqlx = format!("SELECT * FROM quantaxis.stock_adj where order_book_id in ['{}'] AND date BETWEEN '{}' AND '{}' ", codevar, start, end);
        println!("{:#?}", sqlx);
        let mut result = cursor.query(sqlx).fetch_all().await?;
        let timevec: Vec<_> = result.get_column("date")?.iter::<Date<Tz>>()?.collect();

        let ttimevec = timevec
            .iter()
            .map(|x| x.to_string()[0..10].parse().unwrap())
            .collect();
        let codevec: Vec<_> = result
            .get_column("order_book_id")?
            .iter::<&[u8]>()?
            .collect();
        let codev: Vec<String> = codevec
            .iter()
            .map(|x| String::from_utf8(x.to_vec()).unwrap())
            .collect();
        let adj: Vec<_> = result.get_column("adj")?.iter::<f32>()?.copied().collect();
        let res = QADataStruct_StockAdj::new_from_vec(ttimevec, codev, adj);
        Ok(res)
    }

    async fn get_factor(
        &self,
        factorname: &str,
        start: &str,
        end: &str,
    ) -> Result<QADataStruct_Factor, Error> {
        let mut cursor = self.pool.get_handle().await?;
        let sqlx = format!(
            "SELECT * FROM factor.{} where date BETWEEN '{}' AND '{}' ",
            factorname, start, end
        );

        let mut result = cursor.query(sqlx).fetch_all().await?;
        let factorvec: Vec<_> = result
            .get_column("factor")?
            .iter::<f32>()?
            .copied()
            .collect();
        let mut ttimevec: Vec<String> = vec![];
        let timevec: Vec<_> = result.get_column("date")?.iter::<Date<Tz>>()?.collect();
        ttimevec = timevec
            .iter()
            .map(|x| x.to_string()[0..10].parse().unwrap())
            .collect();
        let codevec: Vec<_> = result.get_column("code")?.iter::<&[u8]>()?.collect();
        let codev: Vec<String> = codevec
            .iter()
            .map(|x| String::from_utf8(x.to_vec()).unwrap())
            .collect();
        let res =
            QADataStruct_Factor::new_from_vec(ttimevec, codev, factorvec, factorname.to_string());
        Ok(res)
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
                .get_stock(Vec::from(codelist), "2021-01-10", "2021-01-01")
                .await?;
            //assert_eq!(expected, actual);
        }

        task::block_on(execute()).unwrap();
        assert_eq!('1', '1');
    }

    use actix_rt;
    #[actix_rt::test]
    async fn execute() {
        let c = QACKClient::init();

        let codelist = vec!["000001.XSHE", "000002.XSHE"];
        let b = c
            .get_stock_adv(codelist, "2021-01-10", "2021-01-21", "day")
            .await
            .unwrap();

        println!("{:#?}", b.data);
    }
}
