use crate::qaenv::localenv::CONFIG;

use polars::prelude::{
    CsvReader, DataFrame, DataType, Field, NamedFrom, ParquetReader, ParquetWriter,
    Result as PolarResult, RollingOptions, Schema, SerReader, Series,
};
use std::fs::File;

fn QADataStruct_StockAdj_schema() -> Schema {
    Schema::new(vec![
        Field::new("date", DataType::Utf8),
        Field::new("order_book_id", DataType::Utf8),
        Field::new("adj", DataType::Float32),
    ])
}
pub struct QADataStruct_StockAdj {
    pub data: DataFrame,
    name: String,
}

impl QADataStruct_StockAdj {
    pub fn new_from_vec(date: Vec<String>, order_book_id: Vec<String>, adj: Vec<f32>) -> Self {
        let dateS = Series::new("date", &date);

        let order_book_idS = Series::new("order_book_id", &order_book_id);
        let adjS = Series::new("adj", &adj);
        let df = DataFrame::new(vec![dateS, order_book_idS, adjS]).unwrap();
        Self {
            data: df
                .sort(&["date", "order_book_id"], vec![false, false])
                .unwrap(),
            name: "stockadj".to_string(),
        }
    }
    pub fn new_from_parquet(path: &str) -> Self {
        let file = File::open(path).expect("Cannot open file.");
        let df = ParquetReader::new(file).finish().unwrap();
        Self {
            data: df,
            name: "stockadj".to_string(),
        }
    }

    pub fn save_cache(&mut self) {
        let cachepath = format!("{}stockadj.parquet", &CONFIG.DataPath.cache);
        let file = File::create(cachepath).expect("could not create file");

        ParquetWriter::new(file).finish(&self.data);
    }
}
