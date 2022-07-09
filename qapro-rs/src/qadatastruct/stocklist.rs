use polars::prelude::{
    CsvReader, DataFrame, DataType, Field, NamedFrom, ParquetReader, Result as PolarResult,
    RollingOptions, Schema, SerReader, Series,
};

///┌─order_book_id─┬─industry_code─┬─market_tplus─┬─symbol─┬─special_type─┬─exchange─┬─status─┬─type─┬─de_listed_date─┬─listed_date─┬─sector_code_name─┬─abbrev_symbol─┬─sector_code─┬─round_lot─┬─trading_hours───────────┬─board_type─┬─industry_name────────┬─issue_price─┬─trading_code─┬─purchasedate─┐

fn QADataStruct_StockAdj_schema() -> Schema {
    Schema::new(vec![
        Field::new("order_book_id", DataType::Utf8),
        Field::new("listed_date", DataType::Utf8),
        Field::new("de_listed_date", DataType::Utf8),
        Field::new("symbol", DataType::Utf8),
    ])
}
pub struct QADataStruct_StockList {
    pub data: DataFrame,
    name: String,
}

impl QADataStruct_StockList {
    pub fn new_from_vec(
        order_book_id: Vec<String>,
        listed_date: Vec<String>,
        delist_date: Vec<String>,
        symbol: Vec<String>,
    ) -> Self {
        let order_book_id_S = Series::new("order_book_id", order_book_id);
        let listed_date_S = Series::new("listed_date", listed_date);
        let delist_date_S = Series::new("delist_date", delist_date);

        let symbol_S = Series::new("symbol", symbol);
        let df = DataFrame::new(vec![
            order_book_id_S,
            listed_date_S,
            delist_date_S,
            symbol_S,
        ])
        .unwrap();

        QADataStruct_StockList {
            data: df,
            name: "stocklist".to_string(),
        }
    }
}
