use polars::prelude::{
    CsvReader, DataFrame, DataType, Field, NamedFrom, ParquetReader, Result as PolarResult,
    RollingOptions, Schema, SerReader, Series,
};

fn QADataStruct_StockAdj_schema() -> Schema {
    Schema::new(vec![
        Field::new("date", DataType::Utf8),
        Field::new("order_book_id", DataType::Utf8),
        Field::new("adj", DataType::Float32),
    ])
}
pub struct QADataStruct_StockAdj {
    data: DataFrame,
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
        }
    }
}
