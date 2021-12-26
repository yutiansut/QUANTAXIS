use polars::prelude::{
    CsvReader, DataFrame, DataType, Field, ParquetReader, Result as PolarResult, RollingOptions,
    Schema, SerReader, Series,
};

use polars::series::ops::NullBehavior;
use rayon::prelude::{IntoParallelIterator, ParallelIterator};
use std::error::Error;
use std::fs::{self, File};
use std::io::Result as IoResult;
use std::path::{Path, PathBuf};
use std::sync::Arc;

use crate::qaenv::localenv::CONFIG;
const FILES_IN_PARALLEL: usize = 2;

pub struct StockDay {
    pub data: DataFrame,
}

fn stockday_schema() -> Schema {
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
impl StockDay {
    fn new_from_csv(path: &str) -> Self {
        let schema = stockday_schema();
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
    fn new_from_vec() -> Self {
        todo!()
    }
    fn new_from_parquet(path: &str) -> Self {
        let file = File::open(path).expect("Cannot open file.");
        let df = ParquetReader::new(file).finish().unwrap();
        Self { data: df }
    }

    fn high(&mut self) -> &Series {
        &self.data["high"]
    }

    fn low(&mut self) -> &Series {
        &self.data["low"]
    }
    fn close(&mut self) -> &Series {
        &self.data["close"]
    }
}
#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_stockday() {
        let mut sd = StockDay::new_from_csv("testdata.csv");

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
}
