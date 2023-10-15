use std::cmp::PartialOrd;
use std::collections::{BTreeMap, BTreeSet};
use std::convert::TryFrom;
use std::ops::{Add, Div, Mul, Neg, Rem, Sub};
use std::str::FromStr;

use chrono::prelude::*;
use chrono::serde::ts_seconds;
use indexmap::IndexMap as Map;
use ordered_float::OrderedFloat;
use rayon::prelude::*;
use serde_derive::{Deserialize, Serialize};

use crate::parsers::sql::Selector;
use crate::parsers::sql::SelectorNode;
use crate::parsers::value::PqlVector;

#[derive(Debug, Clone, Eq, PartialEq, Ord, PartialOrd, Serialize, Deserialize)]
#[serde(untagged)]
pub enum BPqlValue {
    #[serde(skip_serializing)]
    Missing,
    Null,
    Str(String),
    Boolean(bool),
    Float(OrderedFloat<f64>),
    Int(i64),
    #[serde(with = "ts_seconds")]
    DateTime(DateTime<Utc>),
    Array(BTreeSet<Self>),
    Object(BTreeMap<String, Self>),
}

impl From<PqlValue> for BPqlValue {
    fn from(pqlv: PqlValue) -> Self {
        match pqlv {
            PqlValue::Missing => Self::Missing,
            PqlValue::Null => Self::Null,
            PqlValue::Str(s) => Self::Str(s),
            PqlValue::Boolean(b) => Self::Boolean(b),
            PqlValue::Int(i) => Self::Int(i),
            PqlValue::Float(f) => Self::Float(f),
            PqlValue::DateTime(t) => Self::DateTime(t),
            PqlValue::Array(_) => todo!(),
            PqlValue::Object(_) => todo!(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum PqlValue {
    #[serde(skip_serializing)]
    Missing,
    Null,
    Str(String),
    Boolean(bool),
    Int(i64),
    Float(OrderedFloat<f64>),
    #[serde(with = "ts_seconds")]
    DateTime(DateTime<Utc>),
    Array(Vec<Self>),
    Object(Map<String, Self>),
}

impl Default for PqlValue {
    fn default() -> Self {
        Self::Null
    }
}

impl FromStr for PqlValue {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> anyhow::Result<Self> {
        crate::parsers::pqlir_parser::from_str(s)
    }
}

impl From<&str> for PqlValue {
    fn from(s: &str) -> Self {
        Self::Str(s.to_owned())
    }
}

impl From<bool> for PqlValue {
    fn from(b: bool) -> Self {
        Self::Boolean(b)
    }
}

impl From<i64> for PqlValue {
    fn from(i: i64) -> Self {
        Self::Int(i)
    }
}

impl From<f64> for PqlValue {
    fn from(f: f64) -> Self {
        Self::Float(OrderedFloat(f))
    }
}

impl From<Vec<PqlValue>> for PqlValue {
    fn from(v: Vec<PqlValue>) -> Self {
        Self::Array(v)
    }
}

impl From<Map<String, PqlValue>> for PqlValue {
    fn from(obj: Map<String, PqlValue>) -> Self {
        Self::Object(obj)
    }
}

impl From<PqlValue> for Vec<PqlValue> {
    fn from(value: PqlValue) -> Self {
        match value {
            PqlValue::Array(array) => array,
            _ => vec![value],
        }
    }
}

impl PqlValue {
    pub fn get(self, key: &str) -> Option<Self> {
        match self {
            Self::Object(map) => map.get(key).map(|v| v.to_owned()),
            _ => None,
        }
    }

    pub fn get_path(self, path: &[&str]) -> Option<Self> {
        if let Some((key, path)) = path.split_first() {
            if let Some(obj) = self.get(key) {
                if path.is_empty() {
                    Some(obj)
                } else {
                    obj.get_path(path)
                }
            } else {
                None
            }
        } else {
            unreachable!();
        }
    }

    pub fn select_by_key(&self, key: &SelectorNode) -> Option<Self> {
        match (self, key.to_owned()) {
            (Self::Object(map), SelectorNode::String(key_s)) => {
                map.get(&key_s).map(|v| v.to_owned())
            }
            _ => None,
        }
    }

    pub fn get_mut_by_selectornode(&mut self, node: &SelectorNode) -> Option<&mut Self> {
        match (self, node.to_owned()) {
            (Self::Object(map), SelectorNode::String(key_s)) => map.get_mut(&key_s),
            _ => None,
        }
    }

    pub fn select_by_selector(&self, selector: &Selector) -> Self {
        match self {
            Self::Object(_map) => {
                if let Some((key, tail)) = selector.split_first() {
                    if let Some(obj) = self.select_by_key(&key) {
                        obj.select_by_selector(&tail)
                    } else {
                        PqlValue::Missing
                    }
                } else {
                    self.to_owned()
                }
            }
            Self::Array(array) => {
                if let Some((key, tail)) = selector.split_first() {
                    match key {
                        SelectorNode::Number(key_i) => {
                            if key_i < 0 {
                                todo!()
                            } else {
                                let key_u = key_i as usize;
                                array
                                    .get(key_u)
                                    .map(|value| value.select_by_selector(&tail))
                                    .unwrap_or(Self::Missing)
                            }
                        }
                        _ => {
                            let new_array = array
                                .into_iter()
                                .map(|value| value.select_by_selector(&selector))
                                .collect::<Vec<_>>();
                            Self::Array(new_array)
                        }
                    }
                } else {
                    let new_array = array
                        .into_iter()
                        .map(|value| value.select_by_selector(&selector))
                        .collect::<Vec<_>>();
                    Self::Array(new_array)
                }
            }
            _ => self.to_owned(),
        }
    }

    pub fn get_mut_by_selector(&mut self, selector: &Selector) -> Option<&mut Self> {
        match self {
            Self::Object(_map) => {
                if let Some((key, tail)) = selector.split_first() {
                    if let Some(obj) = self.get_mut_by_selectornode(&key) {
                        obj.get_mut_by_selector(&tail)
                    } else {
                        None
                    }
                } else {
                    Some(self)
                }
            }
            Self::Array(array) => {
                if let Some((key, _tail)) = selector.split_first() {
                    match key {
                        SelectorNode::Number(key_i) => {
                            if key_i < 0 {
                                todo!()
                            } else {
                                let key_u = key_i as usize;
                                array.get_mut(key_u)
                            }
                        }
                        _ => {
                            todo!()
                        }
                    }
                } else {
                    todo!()
                }
            }
            _ => Some(self),
        }
    }

    pub fn then_if_not_missing(self) -> Option<Self> {
        match self {
            Self::Missing => None,
            _ => Some(self),
        }
    }

    pub fn print(&self) -> anyhow::Result<()> {
        println!("{}", self.to_json()?);
        Ok(())
    }

    pub fn to_json(&self) -> serde_json::Result<String> {
        self.to_jsonp()
    }

    pub fn to_jsonp(&self) -> serde_json::Result<String> {
        serde_json::to_string_pretty(self)
    }

    pub fn to_jsonc(&self) -> serde_json::Result<String> {
        serde_json::to_string(self)
    }

    pub fn into_array(self) -> Self {
        let v: Vec<PqlValue> = self.into();
        PqlValue::Array(v)
    }

    pub fn flatten(self) -> Self {
        match self {
            PqlValue::Array(array) => {
                let flatten_array = array
                    .into_iter()
                    .map(|elem| {
                        let v: Vec<PqlValue> = elem.into();
                        v
                    })
                    .flatten()
                    .collect::<Vec<_>>();
                PqlValue::Array(flatten_array)
            }
            _ => self,
        }
    }
}

impl Neg for PqlValue {
    type Output = Self;
    fn neg(self) -> Self::Output {
        match self {
            Self::Int(a) => Self::Int(-a),
            Self::Float(a) => Self::Float(-a),
            _ => todo!(),
        }
    }
}

impl Add for PqlValue {
    type Output = Self;
    fn add(self, other: Self) -> Self::Output {
        match (self, other) {
            (Self::Int(a), Self::Int(b)) => Self::Int(a + b),
            (Self::Int(a), Self::Float(b)) => Self::Float(OrderedFloat(a as f64) + b),
            (Self::Float(a), Self::Int(b)) => Self::Float(a + OrderedFloat(b as f64)),
            (Self::Float(a), Self::Float(b)) => Self::Float(a + b),
            (Self::Array(array_a), Self::Array(array_b)) => {
                let (vec_a, vec_b) = (PqlVector(array_a), PqlVector(array_b));
                PqlValue::from(vec_a + vec_b)
            }
            (Self::Array(array), val) => {
                let n = array.len();
                let (vec_a, vec_b) = (PqlVector(array), PqlVector(vec![val; n]));
                PqlValue::from(vec_a + vec_b)
            }
            (val, Self::Array(array)) => {
                let n = array.len();
                let (vec_a, vec_b) = (PqlVector(vec![val; n]), PqlVector(array));
                PqlValue::from(vec_a + vec_b)
            }
            _ => todo!(),
        }
    }
}

impl Sub for PqlValue {
    type Output = Self;
    fn sub(self, other: Self) -> Self::Output {
        match (self, other) {
            (Self::Int(a), Self::Int(b)) => Self::Int(a - b),
            (Self::Int(a), Self::Float(b)) => Self::Float(OrderedFloat(a as f64) - b),
            (Self::Float(a), Self::Int(b)) => Self::Float(a - OrderedFloat(b as f64)),
            (Self::Float(a), Self::Float(b)) => Self::Float(a - b),
            (Self::Array(array_a), Self::Array(array_b)) => {
                let (vec_a, vec_b) = (PqlVector(array_a), PqlVector(array_b));
                PqlValue::from(vec_a - vec_b)
            }
            (Self::Array(array), val) => {
                let n = array.len();
                let (vec_a, vec_b) = (PqlVector(array), PqlVector(vec![val; n]));
                PqlValue::from(vec_a - vec_b)
            }
            (val, Self::Array(array)) => {
                let n = array.len();
                let (vec_a, vec_b) = (PqlVector(vec![val; n]), PqlVector(array));
                PqlValue::from(vec_a - vec_b)
            }
            _ => todo!(),
        }
    }
}

impl Mul for PqlValue {
    type Output = Self;
    fn mul(self, other: Self) -> Self::Output {
        match (self.to_owned(), other.to_owned()) {
            (Self::Int(a), Self::Int(b)) => Self::Int(a * b),
            (Self::Int(a), Self::Float(b)) => Self::Float(OrderedFloat(a as f64) * b),
            (Self::Float(a), Self::Int(b)) => Self::Float(a * OrderedFloat(b as f64)),
            (Self::Float(a), Self::Float(b)) => Self::Float(a * b),
            (Self::Array(array_a), Self::Array(array_b)) => {
                let (vec_a, vec_b) = (PqlVector(array_a), PqlVector(array_b));
                PqlValue::from(vec_a * vec_b)
            }
            (Self::Array(array), val) => {
                let n = array.len();
                let (vec_a, vec_b) = (PqlVector(array), PqlVector(vec![val; n]));
                PqlValue::from(vec_a * vec_b)
            }
            (val, Self::Array(array)) => {
                let n = array.len();
                let (vec_a, vec_b) = (PqlVector(vec![val; n]), PqlVector(array));
                PqlValue::from(vec_a * vec_b)
            }
            _ => todo!(),
        }
    }
}

impl Div for PqlValue {
    type Output = Self;
    fn div(self, other: Self) -> Self::Output {
        match (self, other) {
            (Self::Int(a), Self::Int(b)) => Self::Float(OrderedFloat(a as f64 / b as f64)),
            (Self::Int(a), Self::Float(b)) => Self::Float(OrderedFloat(a as f64) / b),
            (Self::Float(a), Self::Int(b)) => Self::Float(a / OrderedFloat(b as f64)),
            (Self::Float(a), Self::Float(b)) => Self::Float(a / b),
            (Self::Array(array_a), Self::Array(array_b)) => {
                let (vec_a, vec_b) = (PqlVector(array_a), PqlVector(array_b));
                PqlValue::from(vec_a / vec_b)
            }
            (Self::Array(array), val) => {
                let n = array.len();
                let (vec_a, vec_b) = (PqlVector(array), PqlVector(vec![val; n]));
                PqlValue::from(vec_a / vec_b)
            }
            (val, Self::Array(array)) => {
                let n = array.len();
                let (vec_a, vec_b) = (PqlVector(vec![val; n]), PqlVector(array));
                PqlValue::from(vec_a / vec_b)
            }
            _ => todo!(),
        }
    }
}

impl Rem for PqlValue {
    type Output = Self;
    fn rem(self, other: Self) -> Self::Output {
        match (self, other) {
            (Self::Int(a), Self::Int(b)) => Self::from(a % b),
            (Self::Int(a), Self::Float(OrderedFloat(b))) => Self::from(a as f64 % b),
            (Self::Float(OrderedFloat(a)), Self::Int(b)) => Self::from(a % b as f64),
            (Self::Float(OrderedFloat(a)), Self::Float(OrderedFloat(b))) => Self::from(a % b),
            (Self::Array(array_a), Self::Array(array_b)) => {
                let (vec_a, vec_b) = (PqlVector(array_a), PqlVector(array_b));
                PqlValue::from(vec_a % vec_b)
            }
            (Self::Array(array), val) => {
                let n = array.len();
                let (vec_a, vec_b) = (PqlVector(array), PqlVector(vec![val; n]));
                PqlValue::from(vec_a % vec_b)
            }
            (val, Self::Array(array)) => {
                let n = array.len();
                let (vec_a, vec_b) = (PqlVector(vec![val; n]), PqlVector(array));
                PqlValue::from(vec_a % vec_b)
            }
            _ => todo!(),
        }
    }
}

impl PqlValue {
    pub fn powf(self, other: Self) -> Self {
        let (a, b) = match (self, other) {
            (Self::Int(a), Self::Int(b)) => (a as f64, b as f64),
            (Self::Int(a), Self::Float(OrderedFloat(b))) => (a as f64, b),
            (Self::Float(OrderedFloat(a)), Self::Int(b)) => (a, b as f64),
            (Self::Float(OrderedFloat(a)), Self::Float(OrderedFloat(b))) => (a, b),
            _ => todo!(),
        };
        Self::from(a.powf(b))
    }
}

impl TryFrom<PqlValue> for i64 {
    type Error = anyhow::Error;
    fn try_from(value: PqlValue) -> anyhow::Result<Self> {
        match value {
            PqlValue::Int(int) => Ok(int),
            PqlValue::Float(OrderedFloat(f)) => Ok(f as i64),
            _ => anyhow::bail!("not numeric"),
        }
    }
}

impl PartialOrd for PqlValue {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        let v1 = BPqlValue::from(self.to_owned());
        let v2 = BPqlValue::from(other.to_owned());
        Some(v1.cmp(&v2))
    }
}

#[cfg(test)]
mod tests {
    use std::collections::VecDeque;
    use std::str::FromStr;

    use ordered_float::OrderedFloat;

    use crate::parsers::planner::LogicalPlan;
    use crate::parsers::pqlir_parser;
    use crate::parsers::sql::Env;
    use crate::parsers::sql::Expr;
    use crate::parsers::sql::Selector;
    use crate::parsers::sql::SelectorNode;
    use crate::parsers::sql::Sql;
    use crate::parsers::value::PqlValue;

    #[test]
    fn add_sub_mul_div() {
        assert_eq!(
            PqlValue::Float(OrderedFloat(1.)) + PqlValue::Float(OrderedFloat(2.)),
            PqlValue::Float(OrderedFloat(3.))
        );
        assert_eq!(
            PqlValue::Float(OrderedFloat(1.)) / PqlValue::Float(OrderedFloat(0.)),
            PqlValue::Float(OrderedFloat(f64::INFINITY))
        );
    }

    #[test]
    fn select_at_arr_1() -> anyhow::Result<()> {
        let value = PqlValue::from_str(r#"{ "arr" : [1,2,4] }"#)?;

        let selected_value = value.select_by_selector(&Selector {
            data: vec![
                SelectorNode::String(String::from("arr")),
                SelectorNode::Number(1),
            ]
            .into_iter()
            .collect::<VecDeque<SelectorNode>>(),
        });

        assert_eq!(selected_value, PqlValue::from_str("2")?);
        Ok(())
    }

    #[test]
    fn test_ord() {
        let i1 = PqlValue::from(1);
        let f2 = PqlValue::from(2.);
        let i3 = PqlValue::from(3);

        assert_eq!(i1 > f2, true);
        assert_eq!(f2 < i3, true);
    }

    #[test]
    fn test_update_value() -> anyhow::Result<()> {
        let mut value = PqlValue::from_str(r#"{ "arr" : [1,2,4] }"#)?;

        if let Some(partiql_value) = value.get_mut_by_selector(&Selector {
            data: vec![
                SelectorNode::String(String::from("arr")),
                SelectorNode::Number(1),
            ]
            .into_iter()
            .collect::<VecDeque<SelectorNode>>(),
        }) {
            *partiql_value = PqlValue::from(20.);
        };

        assert_eq!(value, PqlValue::from_str(r#"{ "arr": [1,20,4] }"#)?);
        Ok(())
    }

    #[test]
    fn test_add() -> anyhow::Result<()> {
        let data = PqlValue::from_str(
            r#"
{
    "dat": [
        { "n": 1 },
        { "n": 2 },
        { "n": 3 }
    ]
}
"#,
        )?;
        let mut env = Env::default();
        env.insert("", &Expr::from(data));

        let sql = Sql::from_str(
            r#"
SELECT
    dat.n + 3 AS n3,
    4 + dat.n  AS n4,
    dat.n + dat.n  AS nn,
    "#,
        )?;
        let plan = LogicalPlan::from(sql);

        let res = plan.execute(&mut env);

        assert_eq!(
            res,
            PqlValue::from_str(
                r#"
[
  {
    "n3": 4.0,
    "n4": 5.0,
    "nn": 2.0
  },
  {
    "n3": 5.0,
    "n4": 6.0,
    "nn": 4.0
  },
  {
    "n3": 6.0,
    "n4": 7.0,
    "nn": 6.0
  }
]
                "#
            )?
        );
        Ok(())
    }

    #[test]
    fn test_sub() -> anyhow::Result<()> {
        let data = PqlValue::from_str(
            r#"
{
    "dat": [
        { "n": 1 },
        { "n": 2 },
        { "n": 3 }
    ]
}
"#,
        )?;
        let mut env = Env::default();
        env.insert("", &Expr::from(data));

        let sql = Sql::from_str(
            r#"
SELECT
    dat.n - 3 AS n3,
    4 - dat.n  AS n4,
    dat.n - dat.n  AS nn,
    "#,
        )?;
        let plan = LogicalPlan::from(sql);

        let res = plan.execute(&mut env);
        res.print();

        assert_eq!(
            res,
            PqlValue::from_str(
                r#"
[
  {
    "n3": -2.0,
    "n4": 3.0,
    "nn": 0.0
  },
  {
    "n3": -1.0,
    "n4": 2.0,
    "nn": 0.0
  },
  {
    "n3": 0.0,
    "n4": 1.0,
    "nn": 0.0
  }
]
                "#
            )?
        );
        Ok(())
    }

    #[test]
    fn test_mul() -> anyhow::Result<()> {
        let data = PqlValue::from_str(
            r#"
{
    "dat": [
        { "n": 1 },
        { "n": 2 },
        { "n": 3 }
    ]
}
"#,
        )?;
        let mut env = Env::default();
        env.insert("", &Expr::from(data));

        let sql = Sql::from_str(
            r#"
SELECT
    dat.n * 3 AS n3,
    4* dat.n  AS n4,
    dat.n* dat.n  AS nn,
    "#,
        )?;
        let plan = LogicalPlan::from(sql);

        let res = plan.execute(&mut env);

        assert_eq!(
            res,
            PqlValue::from_str(
                r#"
[
  {
    "n3": 3.0,
    "n4": 4.0,
    "nn": 1.0
  },
  {
    "n3": 6.0,
    "n4": 8.0,
    "nn": 4.0
  },
  {
    "n3": 9.0,
    "n4": 12.0,
    "nn": 9.0
  }
]
                "#
            )?
        );
        Ok(())
    }

    #[test]
    fn test_div() -> anyhow::Result<()> {
        let data = PqlValue::from_str(
            r#"
{
    "dat": [
        { "n": 1 },
        { "n": 2 },
        { "n": 3 }
    ]
}
"#,
        )?;
        let mut env = Env::default();
        env.insert("", &Expr::from(data));

        let sql = Sql::from_str(
            r#"
SELECT
    dat.n / 3 AS n3,
    4 / dat.n  AS n4,
    dat.n / dat.n  AS nn,
    "#,
        )?;
        let plan = LogicalPlan::from(sql);

        let res = plan.execute(&mut env);
        res.print();

        assert_eq!(
            res,
            PqlValue::from_str(
                r#"
[
  {
    "n3": 0.3333333333333333,
    "n4": 4.0,
    "nn": 1.0
  },
  {
    "n3": 0.6666666666666666,
    "n4": 2.0,
    "nn": 1.0
  },
  {
    "n3": 1.0,
    "n4": 1.3333333333333333,
    "nn": 1.0
  }
]

                "#
            )?
        );
        Ok(())
    }

    #[test]
    fn test_calc_bmi() -> anyhow::Result<()> {
        let data = PqlValue::from_str(
            r#"
[
  { "no": 1, "height": 0.7, "weight": 6.9 },
  { "no": 2, "height": 1.0, "weight": 13.0 },
  { "no": 3, "height": 2.0, "weight": 100.0 },
  { "no": 4, "height": 0.6, "weight": 8.5 },
  { "no": 5, "height": 1.1, "weight": 19.0 },
  { "no": 6, "height": 1.7, "weight": 90.5 },
  { "no": 7, "height": 0.5, "weight": 9.0 },
  { "no": 8, "height": 1.0, "weight": 22.5 },
  { "no": 9, "height": 1.6, "weight": 85.5 },
  { "no": 10, "height": 0.3, "weight": 2.9 }
]
"#,
        )?;
        let mut env = Env::default();
        env.insert("", &Expr::from(data));

        let sql = Sql::from_str(
            r#"
SELECT
    no,
    weight/height/height AS bmi
ORDER BY bmi DESC
LIMIT 3
    "#,
        )?;
        let plan = LogicalPlan::from(sql);

        let res = plan.execute(&mut env);
        res.print();

        assert_eq!(
            res,
            PqlValue::from_str(
                r#"
[
  { "no": 7.0, "bmi": 36.0 },
  { "no": 9.0, "bmi": 33.3984375 },
  { "no": 10.0, "bmi": 32.22222222222222 }
]
        "#
            )?
        );

        Ok(())
    }

    #[test]
    fn test_flatten_array() -> anyhow::Result<()> {
        assert_eq!(
            PqlValue::from_str(
                r#"
[
  [ [2, 4], [6] ],
  [ [8] ]
]
     "#,
            )?
            .flatten(),
            PqlValue::from_str(
                r#"
[
  [ 2.0, 4.0 ],
  [ 6.0 ],
  [ 8.0 ]
]
        "#
            )?
        );

        Ok(())
    }
}
