use crate::qaprotocol::mifi::market::BAR;
use crate::qaruntime::qacontext::{QAContext, StrategyFunc};
use std::fs::File;
use std::io::{BufRead, BufReader, Error, Write};

pub fn backtest(
    data: Vec<BAR>,
    name: String,
    code: String,
    frequence: i32,
    context: &mut QAContext,
    stg: &mut impl StrategyFunc,
    fs: &mut File,
) {
    for bar in data {
        context.next(bar.clone(), stg);
        context.switch(bar);
    }

    for o in context.order_que.chunks(2) {
        let x = match o[0].order.towards {
            2 => "多头",
            -2 => "空头",
            _ => "",
        };
        if o.len() == 2 {
            write!(
                fs,
                "{}",
                format!(
                    "{},{},{},{},{},{:.2},{},{},{:.2}\n",
                    name,
                    x,
                    code,
                    get_direction_or_offset(o[0].order.towards),
                    o[0].order.order_time,
                    o[0].order.price,
                    get_direction_or_offset(o[1].order.towards),
                    o[1].order.order_time,
                    o[1].order.price
                )
            )
            .unwrap();
        } else if o.len() == 1 {
            write!(
                fs,
                "{}",
                format!(
                    "{},{},{},{},{},{:.2},,,\n",
                    name,
                    x,
                    code,
                    get_direction_or_offset(o[0].order.towards),
                    o[0].order.order_time,
                    o[0].order.price
                )
            )
            .unwrap();
        }
    }
}

pub fn get_direction_or_offset(towards: i32) -> String {
    let rt = match towards {
        1 => (String::from("BUY_OPEN"), String::from("OPEN")),
        2 => (String::from("BUY"), String::from("OPEN")),
        3 => (String::from("BUY"), String::from("CLOSE")),
        4 => (String::from("BUY"), String::from("CLOSETODAY")),
        -1 => (String::from("SELL"), String::from("CLOSE")),
        -2 => (String::from("SELL"), String::from("OPEN")),
        -3 => (String::from("SELL"), String::from("CLOSE")),
        -4 => (String::from("SELL"), String::from("CLOSETODAY")),
        _ => (String::from(""), String::from("")),
    };
    format!("{}_{}", rt.0, rt.1)
}
