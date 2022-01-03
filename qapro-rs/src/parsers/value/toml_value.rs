use chrono::prelude::*;
use chrono::serde::ts_seconds;
use indexmap::IndexMap as Map;
use serde_derive::{Deserialize, Serialize};

use crate::parsers::value::PqlValue;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum TomlValue {
    #[serde(skip_serializing)]
    Null,
    Str(String),
    Boolean(bool),
    Float(f64),
    Int(i64),
    #[serde(with = "ts_seconds")]
    DateTime(DateTime<Utc>),
    Array(Vec<Self>),
    Object(Map<String, Self>),
}

impl From<PqlValue> for TomlValue {
    fn from(pqlv: PqlValue) -> Self {
        match pqlv {
            PqlValue::Missing => unreachable!(),
            PqlValue::Null => Self::Null,
            PqlValue::Str(string) => Self::Str(string),
            PqlValue::Boolean(boolean) => Self::Boolean(boolean),
            PqlValue::Float(float) => Self::Float(float.into_inner()),
            PqlValue::Int(int) => Self::Int(int),
            PqlValue::DateTime(datetime) => Self::DateTime(datetime),
            PqlValue::Array(array) => Self::Array(
                array
                    .into_iter()
                    .filter_map(|v| match v {
                        PqlValue::Null => None,
                        PqlValue::Missing => None,
                        _ => Some(Self::from(v)),
                    })
                    .collect::<Vec<_>>(),
            ),
            PqlValue::Object(map) => Self::Object({
                let mut paris = vec![];
                let mut paris_for_map = vec![];
                for (k, v) in map.into_iter() {
                    match v {
                        PqlValue::Missing => {}
                        PqlValue::Null => {}
                        PqlValue::Object(_) => {
                            paris_for_map.push((k, Self::from(v)));
                        }
                        _ => {
                            paris.push((k, Self::from(v)));
                        }
                    }
                }
                paris.append(&mut paris_for_map);
                paris.into_iter().collect::<Map<_, _>>()
            }),
        }
    }
}
