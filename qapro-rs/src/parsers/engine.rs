use std::str::FromStr;

use crate::parsers::lang::{Lang, LangType};
use crate::parsers::planner;
use crate::parsers::sql::Sql;
use crate::parsers::value::PqlValue;

pub fn evaluate(sql: &str, input: &str, from: &str, to: &str) -> anyhow::Result<String> {
    let from_lang_type = LangType::from_str(&from)?;
    let to_lang_type = LangType::from_str(&to)?;
    let mut lang = Lang::from_as(&input, from_lang_type)?;

    let sql = Sql::from_str(&sql)?;

    let result = planner::evaluate(sql, lang.data);
    lang.to = to_lang_type;
    lang.data = result;
    let output = lang.to_string(true)?;

    Ok(output)
}

pub fn loads(input: &str, from: &str) -> anyhow::Result<PqlValue> {
    let from_lang_type = LangType::from_str(&from)?;
    let lang = Lang::from_as(&input, from_lang_type)?;
    let value = lang.data;
    Ok(value)
}

pub fn dumps(data: PqlValue, to: &str) -> anyhow::Result<String> {
    let to_lang_type = LangType::from_str(&to)?;
    let mut lang = Lang::default();
    lang.data = data;
    lang.to = to_lang_type;
    let output = lang.to_string(true)?;
    Ok(output)
}

pub fn query_evaluate(data: PqlValue, sql: &str) -> anyhow::Result<PqlValue> {
    let sql = Sql::from_str(&sql)?;
    let data = PqlValue::from(data);
    let value = planner::evaluate(sql, data);
    Ok(value)
}
