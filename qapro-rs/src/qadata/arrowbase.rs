use arrow::array;
use datafusion::prelude::*;
use datafusion::error::Result;
use crate::qaprotocol::mifi::market::{
    BAR, StockDay,StockMin, FutureDay,FutureMin
};


