//----------------------
//   T
//---------------------
use std::f64::INFINITY;

use chrono::prelude::Utc;

use crate::qaaccount::{account::QA_Account, order::QAOrder, transaction::QATransaction};

use serde::{Deserialize, Serialize};

use crate::qadata::datafunc::{dhhv, dllv, max, min, vec_bigger, vec_smaller, Que};
use crate::qaprotocol::mifi::market::BAR;
use crate::qaruntime::qacontext::{QAContext, StrategyFunc};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Params {}

// impl Params {
//     pub fn default() -> Params {
//         Params {
//
//         }
//     }
// }

#[derive(Debug, Clone)]
pub struct QAStrategy {
    pub params: Params,
}

// impl StrategyFunc for QAStrategy {
//     fn on_bar_next(&mut self, data: &BAR, context: &mut QAContext) {
//         let bar = data;
//         let hour = bar.datetime[11..13].parse::<i32>().unwrap();
//         let minute = bar.datetime[14..16].parse::<i32>().unwrap();
//         let now = Utc::now();
//         let code = bar.code.as_ref();
//         let long_pos = context.acc.get_volume_long(code);
//         let short_pos = context.acc.get_volume_short(code);
// //-----------------Strategy---Content-------------------------
//     }
//
//     fn on_bar_update(&mut self, data: &BAR, context: &mut QAContext) {
//         let bar = data;
//         let hour = bar.datetime[11..13].parse::<i32>().unwrap();
//         let minute = bar.datetime[14..16].parse::<i32>().unwrap();
//         let now = Utc::now();
//         let code = bar.code.as_ref();
//         let long_pos = context.acc.get_volume_long(code);
//         let short_pos = context.acc.get_volume_short(code);
// //-----------------Strategy---Content-------------------------
//     }
// }
