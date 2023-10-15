#![allow(dead_code)]

use serde::{Deserialize, Serialize};

use std::collections::{BTreeMap, HashMap};

use crate::qaprotocol::qifi::default::{default_i32, default_string};

// 注意当前设置的数据大小 是否可能会出现溢出情况  这需要我们进行考虑
#[allow(dead_code, non_snake_case)]
#[derive(Serialize, Clone, Deserialize, Debug, Default)]
pub struct Account {
    pub user_id: String,
    pub currency: String,
    pub pre_balance: f64,
    pub deposit: f64,
    pub withdraw: f64,
    pub WithdrawQuota: f64,
    pub close_profit: f64,
    pub commission: f64,
    pub premium: f64,
    pub static_balance: f64,
    pub position_profit: f64,
    pub float_profit: f64,
    pub balance: f64,
    pub margin: f64,
    pub frozen_margin: f64,
    pub frozen_commission: f64,
    pub frozen_premium: f64,
    pub available: f64,
    pub risk_ratio: f64,
}

#[allow(dead_code)]
#[derive(Serialize, Clone, Deserialize, Debug, Default)]
pub struct BankDetail {
    pub id: String,
    pub name: String,
    pub bank_account: String,
    pub fetch_amount: f64,
    pub qry_count: i64,
}

#[allow(dead_code)]
#[derive(Serialize, Clone, Deserialize, Debug, Default)]
pub struct Order {
    pub seqno: i32,
    pub user_id: String,
    pub order_id: String,
    pub exchange_id: String,
    pub instrument_id: String,
    pub direction: String,
    pub offset: String,
    pub volume_orign: f64,
    pub price_type: String,
    pub limit_price: f64,
    pub time_condition: String,
    pub volume_condition: String,
    pub insert_date_time: i64,
    pub exchange_order_id: String,
    pub status: String,
    pub volume_left: f64,
    pub last_msg: String,
}

#[allow(dead_code)]
#[derive(Serialize, Clone, Deserialize, Debug, Default)]
pub struct Position {
    pub user_id: String,
    pub exchange_id: String,
    pub instrument_id: String,
    pub volume_long_today: f64,
    pub volume_long_his: f64,
    pub volume_long: f64,
    pub volume_long_frozen_today: f64,
    pub volume_long_frozen_his: f64,
    pub volume_long_frozen: f64,
    pub volume_short_today: f64,
    pub volume_short_his: f64,
    pub volume_short: f64,
    pub volume_short_frozen_today: f64,
    pub volume_short_frozen_his: f64,
    pub volume_short_frozen: f64,
    pub volume_long_yd: f64,
    pub volume_short_yd: f64,
    pub pos_long_his: f64,
    pub pos_long_today: f64,
    pub pos_short_his: f64,
    pub pos_short_today: f64,
    pub open_price_long: f64,
    pub open_price_short: f64,
    pub open_cost_long: f64,
    pub open_cost_short: f64,
    pub position_price_long: f64,
    pub position_price_short: f64,
    pub position_cost_long: f64,
    pub position_cost_short: f64,
    pub last_price: f64,
    pub float_profit_long: f64,
    pub float_profit_short: f64,
    pub float_profit: f64,
    pub position_profit_long: f64,
    pub position_profit_short: f64,
    pub position_profit: f64,
    pub margin_long: f64,
    pub margin_short: f64,
    pub margin: f64,
}

#[allow(dead_code)]
#[derive(Serialize, Clone, Deserialize, Debug, Default)]
pub struct Trade {
    pub seqno: i32,
    pub user_id: String,
    pub trade_id: String,
    pub exchange_id: String,
    pub instrument_id: String,
    pub order_id: String,
    pub exchange_trade_id: String,
    pub direction: String,
    pub offset: String,
    pub volume: f64,
    pub price: f64,
    pub trade_date_time: i64,
    pub commission: f64,
}

#[allow(dead_code)]
#[derive(Serialize, Clone, Deserialize, Debug, Default)]
pub struct Transfer {
    pub datetime: i64,
    pub currency: String,
    pub amount: f64,
    pub error_id: i32,
    pub error_msg: String,
}

/// QIFI账户数据结构
/// Examples
/// ```
///
/// ```
#[allow(dead_code)]
#[derive(Serialize, Clone, Deserialize, Debug, Default)]
pub struct QIFI {
    #[serde(default = "default_string")]
    pub databaseip: String,
    pub account_cookie: String,
    pub password: String,
    pub portfolio: String,
    pub broker_name: String,
    pub capital_password: String,
    pub bank_password: String,
    pub bankid: String,
    pub investor_name: String,
    pub money: f64,
    pub pub_host: String,
    pub settlement: HashMap<String, String>,
    // 是一个字典是否考虑反序列化
    // #[serde(default="default_i32")]
    pub taskid: String,
    pub trade_host: String,
    pub updatetime: String,
    pub wsuri: String,
    pub bankname: String,
    pub trading_day: String,
    pub status: i32,
    pub accounts: Account,
    // 注意下面都是不确定的
    pub banks: HashMap<String, BankDetail>,
    #[serde(default = "Default::default")]
    pub event: HashMap<String, String>,
    pub orders: BTreeMap<String, Order>,
    pub positions: HashMap<String, Position>,
    pub trades: BTreeMap<String, Trade>,
    pub transfers: BTreeMap<String, Transfer>,
    #[serde(default = "default_i32")]
    pub ping_gap: i32,
    pub eventmq_ip: String,
}
