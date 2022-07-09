use rand::prelude::*;
use serde::{Deserialize, Serialize};

use crate::qaprotocol::mifi::market::BAR;
use crate::qaruntime::qacontext::{QAContext, StrategyFunc};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Params {}
impl Params {
    pub fn default() -> Params {
        Params {}
    }
}

#[derive(Debug, Clone)]
pub struct QAStrategy {
    pub params: Params,
}

impl QAStrategy {
    pub fn new(params: Params) -> QAStrategy {
        QAStrategy { params }
    }
}

impl StrategyFunc for QAStrategy {
    fn on_bar_next(&mut self, data: &BAR, context: &mut QAContext) {
        //println!("strategy receive --{:#?}", data);
        if rand::random() {
            println!("rand !! xxxx");
            let pos_long = context.acc.get_volume_long(data.code.as_str());
            let pos_short = context.acc.get_volume_short(data.code.as_str());
            if pos_long > 0.0 {
                if rand::random() {
                    context.sell_close(
                        data.code.clone().as_ref(),
                        pos_long,
                        data.datetime.clone().as_ref(),
                        data.close.clone(),
                    );
                }
            } else {
                if rand::random() {
                    context.buy_open(
                        data.code.clone().as_ref(),
                        1.0,
                        data.datetime.clone().as_ref(),
                        data.close.clone(),
                    );
                }
            }
            if pos_short > 0.0 {
                if rand::random() {
                    context.buy_close(
                        data.code.clone().as_ref(),
                        pos_long,
                        data.datetime.clone().as_ref(),
                        data.close.clone(),
                    );
                }
            } else {
                if rand::random() {
                    context.sell_open(
                        data.code.clone().as_ref(),
                        1.0,
                        data.datetime.clone().as_ref(),
                        data.close.clone(),
                    );
                }
            }
        }
    }

    fn on_bar_update(&mut self, data: &BAR, context: &mut QAContext) {
        //println!("strategy receive --{:#?}", data);
        if rand::random() {
            println!("rand !! yyy");
            let pos_long = context.acc.get_volume_long(data.code.as_str());
            let pos_short = context.acc.get_volume_short(data.code.as_str());
            if pos_long > 0.0 {
            } else {
                if rand::random() {
                    context.buy_open(
                        data.code.clone().as_ref(),
                        1.0,
                        data.datetime.clone().as_ref(),
                        data.close.clone(),
                    );
                }
            }
            if pos_short > 0.0 {
            } else {
                if rand::random() {
                    context.sell_open(
                        data.code.clone().as_ref(),
                        1.0,
                        data.datetime.clone().as_ref(),
                        data.close.clone(),
                    );
                }
            }
        }
    }
}
