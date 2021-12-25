extern crate arrow;
use arrow::{
    csv,
    datatypes::{DataType, Field, Schema, SchemaRef},
    record_batch::RecordBatch,
    tensor::Tensor,
    util::pretty::print_batches,
};
use std::{any::Any, collections::BTreeSet, fs::File, sync::Arc};

use datafusion::{
    datasource::TableProvider,
    error::{DataFusionError, Result},
    logical_plan::Expr,
    physical_plan::{
        ColumnStatistics, DisplayFormatType, ExecutionPlan, Partitioning,
        SendableRecordBatchStream, Statistics,
    },
    prelude::ExecutionContext,
    scalar::ScalarValue,
};

fn read_csv() {
    let file = File::open("C:\\QUANT\\quantaxis\\qapro-rs\\testdata.csv").unwrap();
    let builder = csv::ReaderBuilder::new()
        .has_header(true)
        .infer_schema(Some(100));
    let mut csv = builder.build(file).unwrap();
    let batch = csv.next().unwrap().unwrap();
    let data = batch.column(3).max();
    println!("{:#?}", data);

    //print_batches(&[batch]).unwrap();
}

#[cfg(test)]
mod tests {
    use super::*;
    use arrow::util::pretty::print_batches;
    use futures_util::StreamExt;

    #[test]
    fn t() {
        read_csv()
    }
}
