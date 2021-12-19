//! Provide storage statistics for parquet files
extern crate parquet;
use parquet::{
    file::reader::{FileReader, SerializedFileReader},
    record::{RecordWriter, Row},
    schema,
};

use std::fs::File;
use std::path::Path;

pub struct QAParquetClient {
    filepath: String,
}

impl QAParquetClient {
    pub fn new(filepath: String) -> QAParquetClient {
        QAParquetClient { filepath }
    }
    pub fn get_data(&self) -> Vec<Row> {
        let mut data: Vec<Row> = vec![];
        let file = File::open(&Path::new(&self.filepath)).unwrap();
        let reader = SerializedFileReader::new(file).unwrap();
        let mut iter = reader.get_row_iter(None).unwrap();
        while let Some(record) = iter.next() {
            data.push(record);
        }
        data
    }
}
