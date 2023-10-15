use polars::prelude::{
    ChunkCompare, CsvReader, DataFrame, DataType, Field, NamedFrom, ParquetCompression,
    ParquetReader, ParquetWriter, Result as PolarResult, RollingOptions, Schema, SerReader, Series,
};

use polars::series::ops::NullBehavior;
use rayon::prelude::{IntoParallelIterator, ParallelIterator};
use std::fs::{ File};
use std::sync::Arc;

use crate::qaenv::localenv::CONFIG;
const FILES_IN_PARALLEL: usize = 2;

pub struct QADataStruct_StockDay {
    pub data: DataFrame,
}

fn QADataStruct_StockDay_schema() -> Schema {
    Schema::new(vec![
        Field::new("date", DataType::Utf8),
        Field::new("code", DataType::Utf8),
        Field::new("order_book_id", DataType::Utf8),
        Field::new("num_trades", DataType::Float32),
        Field::new("limit_up", DataType::Float32),
        Field::new("limit_down", DataType::Float32),
        Field::new("open", DataType::Float32),
        Field::new("high", DataType::Float32),
        Field::new("low", DataType::Float32),
        Field::new("close", DataType::Float32),
        Field::new("volume", DataType::Float32),
        Field::new("total_turnover", DataType::Float32),
        Field::new("amount", DataType::Float32),
    ])
}
impl QADataStruct_StockDay {
    pub fn new_from_csv(path: &str) -> Self {
        let schema = QADataStruct_StockDay_schema();
        let file = File::open(path).expect("Cannot open file.");
        let df = CsvReader::new(file)
            .with_schema(&Arc::new(schema))
            .has_header(true)
            .finish()
            .unwrap();
        Self { data: df }
    }
    fn new_from_path() -> Self {
        todo!()
    }
    pub fn new_from_vec(
        date: Vec<String>,
        code: Vec<String>,
        open: Vec<f32>,
        high: Vec<f32>,
        low: Vec<f32>,
        close: Vec<f32>,
        limit_up: Vec<f32>,
        limit_down: Vec<f32>,
        num_trades: Vec<f32>,
        volume: Vec<f32>,
        total_turnover: Vec<f32>,
    ) -> Self {
        let dateS = Series::new("date", &date);
        let codeS = Series::new("code", &code);
        let order_book_idS = Series::new("order_book_id", &code);
        let num_tradesS = Series::new("num_trades", &num_trades);
        let limit_upS = Series::new("limit_up", &limit_up);
        let limit_downS = Series::new("limit_down", &limit_down);
        let openS = Series::new("open", &open);
        let highS = Series::new("high", &high);
        let lowS = Series::new("low", &low);
        let closeS = Series::new("close", &close);
        let volumeS = Series::new("volume", &volume);
        let total_turnoverS = Series::new("total_turnover", &total_turnover);
        let amountS = Series::new("amount", &total_turnover);

        let df = DataFrame::new(vec![
            dateS,
            codeS,
            order_book_idS,
            num_tradesS,
            limit_upS,
            limit_downS,
            openS,
            highS,
            lowS,
            closeS,
            volumeS,
            total_turnoverS,
            amountS,
        ])
        .unwrap();
        Self {
            data: df
                .sort(&["date", "order_book_id"], vec![false, false])
                .unwrap(),
        }
    }
    pub fn new_from_parquet(path: &str) -> Self {
        let file = File::open(path).expect("Cannot open file.");
        let df = ParquetReader::new(file).finish().unwrap();
        Self { data: df }
    }

    pub fn query_code(&mut self, order_book_id: &str) -> DataFrame {
        let value = self.data.column("order_book_id").unwrap();
        let mask = value.equal(order_book_id);
        let selectdf = &self.data.filter(&mask).unwrap();
        selectdf.to_owned()
    }
    pub fn query_date(&mut self, date: &str) -> DataFrame {
        let value = self.data.column("date").unwrap();
        let mask = value.equal(date);
        let selectdf = &self.data.filter(&mask).unwrap();
        selectdf.to_owned()
    }
    pub fn high(&mut self) -> &Series {
        &self.data["high"]
    }

    pub fn low(&mut self) -> &Series {
        &self.data["low"]
    }
    pub fn close(&mut self) -> &Series {
        &self.data["close"]
    }

    pub fn save_cache(&mut self) {
        let cache = &CONFIG.DataPath.cache;
        let cachepath = format!("{}stockday.parquet", &CONFIG.DataPath.cache);
        let file = File::create(cachepath).expect("could not create file");
        ParquetWriter::new(file).finish(&self.data);
    }

    pub fn save_selfdefined_cache(&mut self, path: &str) {
        //let cache = &CONFIG.DataPath.cache;
        // let cachepath = format!("{}stockday.parquet", &CONFIG.DataPath.cache);
        let file = File::create(path).expect("could not create file");
        ParquetWriter::new(file).finish(&self.data);
    }
}
#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_QADataStruct_StockDay() {
        let mut sd = QADataStruct_StockDay::new_from_csv("testdata.csv");

        println!("Final DataFrame:\n{}", sd.data);
        let high = &sd.data["high"];
        let low = &sd.data["low"];

        let calc = high - low;
        println!("Final Series high - low :\n{}", calc);

        println!("High diff:\n{}", high.diff(2, NullBehavior::Drop));

        println!(
            "High rollingstd:\n{}",
            high.rolling_std(RollingOptions {
                window_size: 3,
                min_periods: 1,
                weights: None,
                center: false
            })
            .unwrap()
        );
    }

    #[test]
    fn test_QADataStruct_StockDay_fromvec() {
        let testds = QADataStruct_StockDay::new_from_vec(
            vec!["2021-01-01".to_string(), "2021-01-02".to_string()],
            vec!["000001.XSHE".to_string(), "000001.XSHE".to_string()],
            vec![20.1, 20.2],
            vec![22.1, 21.1],
            vec![19.2, 19.8],
            vec![21.0, 20.4],
            vec![22.0, 23.0],
            vec![19.0, 19.5],
            vec![99.2, 99.2],
            vec![880.2, 990.2],
            vec![8880.2, 8890.2],
        );
        println!("{:#?}", testds.data);
    }
    #[test]
    fn test_QADataStruct_StockDay_save() {
        let mut testds = QADataStruct_StockDay::new_from_vec(
            vec!["2021-01-01".to_string(), "2021-01-02".to_string()],
            vec!["000001.XSHE".to_string(), "000001.XSHE".to_string()],
            vec![20.1, 20.2],
            vec![22.1, 21.1],
            vec![19.2, 19.8],
            vec![21.0, 20.4],
            vec![22.0, 23.0],
            vec![19.0, 19.5],
            vec![99.2, 99.2],
            vec![880.2, 990.2],
            vec![8880.2, 8890.2],
        );
        println!("{:#?}", testds.data);

        testds.save_cache();
    }
}
