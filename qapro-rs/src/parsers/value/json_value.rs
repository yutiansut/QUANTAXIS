use std::collections::{BTreeMap, BTreeSet};

use indexmap::IndexMap as Map;
use ordered_float::OrderedFloat;
use serde_derive::{Deserialize, Serialize};

use crate::parsers::value::PqlValue;

#[derive(Debug, Clone, Eq, PartialEq, Ord, PartialOrd, Serialize, Deserialize)]
#[serde(untagged)]
pub enum BJsonValue {
    Null,
    Str(String),
    Boolean(bool),
    Num(OrderedFloat<f64>),
    Array(BTreeSet<BJsonValue>),
    Object(BTreeMap<String, BJsonValue>),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum JsonValue {
    Null,
    Str(String),
    Boolean(bool),
    Num(OrderedFloat<f64>),
    Array(Vec<JsonValue>),
    Object(Map<String, JsonValue>),
}

impl From<JsonValue> for PqlValue {
    fn from(json: JsonValue) -> Self {
        match json {
            JsonValue::Null => Self::Null,
            JsonValue::Str(string) => Self::Str(string),
            JsonValue::Boolean(boolean) => Self::Boolean(boolean),
            JsonValue::Num(number) => Self::Float(number),
            JsonValue::Array(array) => Self::Array(
                array
                    .into_iter()
                    .filter_map(|v| match v {
                        JsonValue::Null => None,
                        _ => Some(Self::from(v)),
                    })
                    .collect::<Vec<_>>(),
            ),
            JsonValue::Object(map) => Self::Object(
                map.into_iter()
                    .filter_map(|(k, v)| match v {
                        JsonValue::Null => None,
                        _ => Some((k, Self::from(v))),
                    })
                    .collect::<Map<_, _>>(),
            ),
        }
    }
}

impl From<PqlValue> for JsonValue {
    fn from(pqlv: PqlValue) -> Self {
        match pqlv {
            PqlValue::Missing => unreachable!(),
            PqlValue::Null => Self::Null,
            PqlValue::Str(string) => Self::Str(string),
            PqlValue::Boolean(boolean) => Self::Boolean(boolean),
            PqlValue::Float(float) => Self::Num(float),
            PqlValue::Int(int) => Self::Num(OrderedFloat(int as f64)),
            PqlValue::DateTime(datetime) => Self::Str(datetime.to_rfc3339()),
            PqlValue::Array(array) => {
                Self::Array(array.into_iter().map(Self::from).collect::<Vec<_>>())
            }
            PqlValue::Object(map) => Self::Object(
                map.into_iter()
                    .map(|(k, v)| (k, Self::from(v)))
                    .collect::<Map<_, _>>(),
            ),
        }
    }
}

pub fn to_pqlvalue(json: serde_json::value::Value) -> PqlValue {
    match json {
        serde_json::value::Value::Null => PqlValue::Null,
        serde_json::value::Value::String(string) => PqlValue::Str(string),
        serde_json::value::Value::Bool(boolean) => PqlValue::Boolean(boolean),
        serde_json::value::Value::Number(number) if number.is_f64() => {
            PqlValue::Float(OrderedFloat(number.as_f64().unwrap()))
        }
        serde_json::value::Value::Number(number) => PqlValue::Int(number.as_i64().unwrap()),
        serde_json::value::Value::Array(array) => {
            PqlValue::Array(array.into_iter().map(to_pqlvalue).collect::<Vec<_>>())
        }
        serde_json::value::Value::Object(map) => PqlValue::Object(
            map.into_iter()
                .map(|(k, v)| (k, to_pqlvalue(v)))
                .collect::<Map<_, _>>(),
        ),
    }
}
