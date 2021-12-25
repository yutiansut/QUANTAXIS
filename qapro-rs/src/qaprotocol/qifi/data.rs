/*
此处描述了quantaxis-rs标准的期货/股票/数据结构
*/
use crate::qaprotocol::qifi::default::{
    default_bool, default_f64, default_i128, default_i32, default_i64, default_string,
};
use serde::{Deserialize, Serialize};

#[allow(dead_code)]
#[derive(Serialize, Clone, Deserialize, Debug)]
pub struct DataItem {
    #[serde(default = "default_f64")]
    pub open: f64,
    #[serde(default = "default_f64")]
    pub high: f64,
    #[serde(default = "default_f64")]
    pub low: f64,
    #[serde(default = "default_f64")]
    pub close: f64,
    #[serde(default = "default_i64")]
    pub volume: i64,
}

/// Bar格式的数据
///     high: 高
///     low: 低
///     close: 收
///     open: 开
///     volume: 成交量
///     amount: 成交金额
/// Examples
/// ```
/// use crate::qifi_rs::{Bar, from_str,from_serde_value};
/// use serde_json::Value;
/// let test_json_str = r#"{
///     "high":2900,
///     "low":2880,
///     "open": 2891,
///     "close": 2899,
///     "volume":100,
///     "amount": 51454131
/// }"#;
/// let val:Value = from_str(test_json_str).unwrap();
/// let bar:Bar = from_serde_value(val).unwrap();
/// println!("{:?}",  bar);
///
/// ```
#[allow(dead_code)]
#[derive(Serialize, Clone, Deserialize, Debug)]
pub struct Bar {
    #[serde(default = "default_f64")]
    pub high: f64,
    #[serde(default = "default_f64")]
    pub low: f64,
    #[serde(default = "default_f64")]
    pub close: f64,
    #[serde(default = "default_f64")]
    pub open: f64,
    #[serde(default = "default_i64")]
    pub volume: i64,
    #[serde(default = "default_f64")]
    pub amount: f64,
}

/// Tick格式的数据
///     price: 最新价
///     open_interest: 持仓量
///     high: 高
///     low: 低
///     close: 收
///     open: 开
///     volume: 成交量
///     amount: 成交金额
/// Examples
/// ```
///
/// ```
#[allow(dead_code)]
#[derive(Serialize, Clone, Deserialize, Debug)]
pub struct Tick {
    #[serde(default = "default_f64")]
    pub price: f64,
    #[serde(default = "default_i128")]
    pub open_interest: i128,
    #[serde(default = "default_f64")]
    pub high: f64,
    #[serde(default = "default_f64")]
    pub low: f64,
    #[serde(default = "default_f64")]
    pub close: f64,
    #[serde(default = "default_f64")]
    pub open: f64,
    #[serde(default = "default_i64")]
    pub volume: i64,
    #[serde(default = "default_f64")]
    pub amount: f64,
}

/// 获取当前code的代码以及限制数量
///     code: 代码名称
///     ip: ip地址
///     limit: 限制数量
#[derive(Serialize, Deserialize, Debug, Clone)]
struct Scode {
    pub code: String,
    pub ip: String,
    pub limit: i32,
}

/// L2行情数据， 注意我为此都添加大量的接口
///     index: 索引
///     time: 时间
///     price: 最新价格
///     isbuy:是否买
///     vol: 成交量
///     buyno:
///     sellno:
///     buyprice:
///     sellprice:
///     buyvol:
///     sellvol:
///     marketname: 市场名称
///     code:
#[derive(Serialize, Deserialize, Debug)]
pub struct L2X {
    #[serde(default = "default_i32")]
    pub index: i32,
    #[serde(default = " default_string")]
    pub time: String,
    #[serde(default = "default_f64")]
    pub price: f64,
    #[serde(default = "default_bool")]
    pub isbuy: bool,
    #[serde(default = "default_i32")]
    pub vol: i32,
    #[serde(default = "default_i32")]
    pub buyno: i32,
    #[serde(default = "default_i32")]
    pub sellno: i32,
    #[serde(default = "default_f64")]
    pub buyprice: f64,
    #[serde(default = "default_f64")]
    pub sellprice: f64,
    #[serde(default = "default_i32")]
    pub buyvol: i32,
    #[serde(default = "default_i32")]
    pub sellvol: i32,
    #[serde(default = " default_string")]
    pub marketname: String,
    #[serde(default = " default_string")]
    pub code: String,
}
