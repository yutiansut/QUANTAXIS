// 此库提供好用的API以提供数据转换功能
use bson::{from_bson, Bson, Document};
use serde::de::DeserializeOwned;
use serde_json::{Error, Value};
// use mongodb::Cursor;
use serde::Serialize;

/// 此处为了描述如何从bson数据载入为可用的结构体,传入一个bson以使用它
pub fn from_bson_(data: Bson) -> Option<Bson> {
    from_bson(data).unwrap()
}

/// 将Value值转换成已经实现了Deserialized的struct
/// Examples
/// ```
/// use qifi_rs::{QIFI, from_string, from_serde_value};
/// use serde_json::Value;
/// let qifi_string = r#"{"account_cookie": "T01B2_IF2004_1min", "password": "T01B2_IF2004_1min", "accounts": {"user_id": "T01B2_IF2004_1min", "currency": "CNY", "pre_balance": 1000000, "deposit": 0, "withdraw": 0, "WithdrawQuota": 0, "close_profit": 0, "commission": 0, "premium": 1330, "static_balance": 1000000, "position_profit": 0, "float_profit": 0, "balance": 1000000, "margin": 0, "frozen_margin": 0, "frozen_commission": 0.0, "frozen_premium": 0.0, "available": 1000000, "risk_ratio": 0.0}, "bank_password": "", "bankid": "QASIM", "bankname": "QASIMBank", "banks": {"QASIM": {"id": "QASIM", "name": "QASIMBank", "bank_account": "", "fetch_amount": 0.0, "qry_count": 0}}, "broker_name": "QAPaperTrading", "capital_password": "", "databaseip": "", "events": {}, "frozen": {}, "investor_name": "", "model": "SIM", "money": 1000000, "orders": {}, "ping_gap": 5, "portfolio": "QAPaperTrade", "positions": {}, "pub_host": "", "settlement": {}, "sourceid": "QIFI_Account", "status": 200, "taskid": "", "trade_host": "", "trades": {}, "trading_day": "2020-03-26", "transfers": {}, "updatetime": "", "wsuri": "ws://www.yutiansut.com:7988"}"#;
/// let string = String::from(qifi_string);
/// let qifi: Value = from_string(string).unwrap();
/// let qifi_struct: QIFI = from_serde_value(qifi).unwrap();
/// let _deserialize = serde_json::to_string(&qifi_struct).expect("呀 反序列化失败,请检查你的字符串格式");
/// ```
///
pub fn from_serde_value<T>(value: Value) -> Result<T, Error>
where
    T: DeserializeOwned,
{
    T::deserialize(value)
}

/// 2020-3-27 14:01 @somewheve
/// 将String转换为Value类型的数据 你需要合理的处理这个问题
/// 出于你可能想对自己的数据格式进行修改考虑，我在此仅仅返回了Option<Value>，方便你进行自己的处理
/// 你仍然可以使用我们提供的from_serde_value或者serde_json::from_value来进行转换成struct.
/// ps: 他们是一样，取决于你想不想再导入serde_json
/// Examples
/// ```
/// use qifi_rs::from_string;
/// use serde_json::Value;
/// let qifi_string = r#"{"account_cookie": "T01B2_IF2004_1min", "password": "T01B2_IF2004_1min", "accounts": {"user_id": "T01B2_IF2004_1min", "currency": "CNY", "pre_balance": 1000000, "deposit": 0, "withdraw": 0, "WithdrawQuota": 0, "close_profit": 0, "commission": 0, "premium": 1330, "static_balance": 1000000, "position_profit": 0, "float_profit": 0, "balance": 1000000, "margin": 0, "frozen_margin": 0, "frozen_commission": 0.0, "frozen_premium": 0.0, "available": 1000000, "risk_ratio": 0.0}, "bank_password": "", "bankid": "QASIM", "bankname": "QASIMBank", "banks": {"QASIM": {"id": "QASIM", "name": "QASIMBank", "bank_account": "", "fetch_amount": 0.0, "qry_count": 0}}, "broker_name": "QAPaperTrading", "capital_password": "", "databaseip": "", "event": {}, "frozen": {}, "investor_name": "", "model": "SIM", "money": 1000000, "orders": {}, "ping_gap": 5, "portfolio": "QAPaperTrade", "positions": {}, "pub_host": "", "settlement": {}, "sourceid": "QIFI_Account", "status": 200, "taskid": "", "trade_host": "", "trades": {}, "trading_day": "2020-03-26", "transfers": {}, "updatetime": "", "wsuri": "ws://www.yutiansut.com:7988"}"#;
/// let string = String::from(qifi_string);
/// let qifi: Value = from_string(string).unwrap();
/// let _deserialize = serde_json::to_string(&qifi).expect("呀 反序列化失败,请检查你的字符串格式");
///```
pub fn from_string(data: String) -> Option<Value> {
    let solve = data.replace("null", "\"qifi_default\"");
    // println!("{:#?}", solve);
    match serde_json::from_str(&solve) {
        Ok(_t) => _t,
        Err(_e) => None,
    }
}

/// 2020-3-27 14:16 @somewheve
/// 将&str转换为Value类型的数据, 在出现错误的时候返回一个None, 你需要合理的处理这个问题
/// 出于你可能想对自己的数据格式进行修改考虑，我在此仅仅返回了Option<Value>，方便你进行自己的处理
/// 你仍然可以使用我们提供的from_serde_value或者serde_json::from_value来进行转换成struct.
/// ps: 他们是一样，取决于你想不想再导入serde_json户
/// Examples
/// ```
/// use qifi_rs::from_str;
/// use serde_json::Value;
/// let qifi_string = r#"{"account_cookie": "T01B2_IF2004_1min", "password": "T01B2_IF2004_1min", "accounts": {"user_id": "T01B2_IF2004_1min", "currency": "CNY", "pre_balance": 1000000, "deposit": 0, "withdraw": 0, "WithdrawQuota": 0, "close_profit": 0, "commission": 0, "premium": 1330, "static_balance": 1000000, "position_profit": 0, "float_profit": 0, "balance": 1000000, "margin": 0, "frozen_margin": 0, "frozen_commission": 0.0, "frozen_premium": 0.0, "available": 1000000, "risk_ratio": 0.0}, "bank_password": "", "bankid": "QASIM", "bankname": "QASIMBank", "banks": {"QASIM": {"id": "QASIM", "name": "QASIMBank", "bank_account": "", "fetch_amount": 0.0, "qry_count": 0}}, "broker_name": "QAPaperTrading", "capital_password": "", "databaseip": "", "event": {}, "frozen": {}, "investor_name": "", "model": "SIM", "money": 1000000, "orders": {}, "ping_gap": 5, "portfolio": "QAPaperTrade", "positions": {}, "pub_host": "", "settlement": {}, "sourceid": "QIFI_Account", "status": 200, "taskid": "", "trade_host": "", "trades": {}, "trading_day": "2020-03-26", "transfers": {}, "updatetime": "", "wsuri": "ws://www.yutiansut.com:7988"}"#;
/// let qifi: Value = from_str(qifi_string).unwrap();
/// let _deserialize = serde_json::to_string(&qifi).expect("呀 反序列化失败,请检查你的字符串格式");
/// ```
pub fn from_str(data: &str) -> Option<Value> {
    let solve = data.replace("null", "\"qifi_default\"");
    match serde_json::from_str(&solve) {
        Ok(_t) => _t,
        Err(_e) => None,
    }
}

// /// 此API用于快速将读取出来的数据转换为json字符串,注意是单个
// pub fn covert_cursors_to_json(cursor: Cursor) -> String {
//     let docs: Vec<_> = cursor.map(|doc| doc.unwrap()).collect();
//     serde_json::to_string(&docs).unwrap()
// }
//
// /// 转换单条数据,
// pub fn covert_cursor_to_json(cursor: Cursor) -> String {
//     let docs: Vec<_> = cursor.map(|doc| doc.unwrap()).collect()[0];
//     serde_json::to_string(&docs).unwrap()
// }

/// 将结构体转换可以直接插入的doc参数
///     Note: 注意你的数据类型中尽量不要使用 **u8等数据类型**,他会导致bson无法解析结构体. 参见 https://github.com/mongodb/bson-rust/issues/89
/// Examples
/// ```
/// use qifi_rs::to_doc;
/// use serde::{Deserialize, Serialize};
/// #[derive(Serialize, Clone, Deserialize, Debug)]
/// struct Name {
///     hello:String
/// }
/// let x  = to_doc(Name{ hello:"somewheve".to_string()});
/// println!("{:?}", x)
///
/// ```
pub fn to_doc<T>(value: T) -> Document
where
    T: Serialize + std::fmt::Debug,
{
    // println!("{:?}", value);
    let serialized = bson::to_bson(&value).unwrap(); // Serialize
    let x = serialized.as_document().expect("期望一个合法的document");
    x.to_owned()
}
