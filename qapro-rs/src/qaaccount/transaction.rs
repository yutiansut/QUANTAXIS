use chrono::{TimeZone, Utc};

use crate::qaprotocol::qifi::account::Trade;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct QATransaction {
    pub code: String,
    pub amount: f64,
    pub price: f64,
    pub datetime: String,
    pub order_id: String,
    pub trade_id: String,
    pub realorder_id: String,
    pub account_cookie: String,
    pub commission: f64,
    pub tax: f64,
    pub message: String,
    pub frozen: f64,
    pub direction: i32,
}

impl QATransaction {
    pub fn to_json(&self) -> String {
        let jdata = serde_json::to_string(&self).unwrap();
        jdata
    }
    pub fn get_direction_or_offset(&mut self, towards: i32) -> (String, String) {
        let rt = match towards {
            1 => (String::from("BUY"), String::from("OPEN")),
            2 => (String::from("BUY"), String::from("OPEN")),
            3 => (String::from("BUY"), String::from("CLOSE")),
            4 => (String::from("BUY"), String::from("CLOSETODAY")),
            -1 => (String::from("SELL"), String::from("CLOSE")),
            -2 => (String::from("SELL"), String::from("OPEN")),
            -3 => (String::from("SELL"), String::from("CLOSE")),
            -4 => (String::from("SELL"), String::from("CLOSETODAY")),
            _ => (String::from(""), String::from("")),
        };
        rt
    }

    pub fn to_qifitrade(&mut self) -> Trade {
        let (direction, offset) = self.get_direction_or_offset(self.direction);
        let td = Utc
            .datetime_from_str(self.datetime.as_ref(), "%Y-%m-%d %H:%M:%S")
            .unwrap()
            .timestamp_nanos()
            - 28800000000000;

        Trade {
            seqno: 0,
            user_id: self.account_cookie.clone(),
            trade_id: self.trade_id.clone(),
            exchange_id: "".to_string(),
            instrument_id: self.code.clone(),
            order_id: self.order_id.clone(),
            exchange_trade_id: self.realorder_id.clone(),
            direction,
            offset,
            volume: self.amount.clone(),
            price: self.price.clone(),
            trade_date_time: td,
            commission: self.commission.clone(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_to_qifi() {
        let mut transaction = QATransaction {
            code: "".to_string(),
            amount: 0.0,
            price: 0.0,
            datetime: "2020-01-02 00:00:00".to_string(),
            order_id: "".to_string(),
            trade_id: "".to_string(),
            realorder_id: "".to_string(),
            account_cookie: "".to_string(),
            commission: 0.0,
            tax: 0.0,
            message: "".to_string(),
            frozen: 0.0,
            direction: 0,
        };
        transaction.to_qifitrade();
    }
}
