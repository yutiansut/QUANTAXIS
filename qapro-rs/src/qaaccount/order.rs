use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone)]
pub struct QAOrder {
    pub account_cookie: String,
    pub user_id: String,
    pub instrument_id: String,
    pub towards: i32,
    pub exchange_id: String,
    pub order_time: String,
    pub volume: f64,
    pub price: f64,
    pub order_id: String,
    pub seqno: String,
    pub direction: String,
    pub offset: String,
    pub volume_orign: f64,
    pub price_type: String,
    pub limit_price: f64,
    pub time_condition: String,
    pub volume_condition: String,
    pub insert_date_time: String,
    pub exchange_order_id: String,
    pub status: i32,
    pub volume_left: f64,
    pub last_msg: String,
}

impl QAOrder {
    pub fn new(
        account: String,
        code: String,
        towards: i32,
        exchange_id: String,
        order_time: String,
        volume: f64,
        price: f64,
        order_id: String,
    ) -> Self {
        let mut direction = "BUY".to_string();
        let mut offset = "OPEN".to_string();

        match towards {
            1 | 2 => {}
            -1 => {
                direction = "SELL".to_string();
            }
            -2 => {
                direction = "SELL".to_string();
            }
            3 => {
                offset = "CLOSE".to_string();
            }
            -3 => {
                direction = "SELL".to_string();
                offset = "CLOSE".to_string();
            }
            _ => {}
        }

        Self {
            account_cookie: account.clone(),
            user_id: account.clone(),
            instrument_id: code.clone(),
            towards,
            exchange_id,
            order_time,
            volume,
            price,
            order_id,
            seqno: "".to_string(),
            direction,
            offset,
            volume_orign: 0.0,
            price_type: "LIMIT".to_string(),
            limit_price: price,
            time_condition: "AND".to_string(),
            volume_condition: "GFD".to_string(),
            insert_date_time: "".to_string(),
            exchange_order_id: Uuid::new_v4().to_string(),
            status: 100,
            volume_left: volume,
            last_msg: "".to_string(),
        }
    }

    pub fn to_trade_order(&self) -> TradeOrder {
        TradeOrder {
            aid: "insert_order".to_string(),
            user_id: self.account_cookie.clone(),
            order_id: self.order_id.clone(),
            exchange_id: self.exchange_id.clone(),
            instrument_id: self.instrument_id.clone(),
            direction: self.direction.clone(),
            offset: self.offset.clone(),
            volume: self.volume as i64,
            price_type: self.price_type.clone(),
            limit_price: self.price,
            volume_condition: self.volume_condition.clone(),
            time_condition: self.time_condition.clone(),
        }
    }
}

#[derive(Serialize, Deserialize, Debug)]
pub struct TradeOrder {
    pub aid: String,
    pub user_id: String,
    pub order_id: String,
    pub exchange_id: String,
    pub instrument_id: String,
    pub direction: String,
    pub offset: String,
    pub volume: i64,
    pub price_type: String,
    pub limit_price: f64,
    pub volume_condition: String,
    pub time_condition: String,
}
