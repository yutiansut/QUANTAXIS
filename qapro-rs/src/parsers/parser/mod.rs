pub mod clauses;
pub mod elements;
pub mod expressions;
pub mod func;
pub mod keywords;
pub mod math;
pub mod select_statement;
pub mod values;

use nom::branch::alt;
use nom::combinator::map;
use nom::number::complete::double;
use nom::IResult;
use ordered_float::OrderedFloat;

use crate::parsers::value::PqlValue;
pub use elements::{float_number, string_allowed_in_field, whitespace};
pub use expressions::parse_expr;
pub use expressions::parse_field;
pub use expressions::parse_path_as_expr;

pub fn parse_value(input: &str) -> IResult<&str, PqlValue> {
    alt((
        map(elements::string, |s| PqlValue::Str(s.to_string())),
        map(double, |f| PqlValue::Float(OrderedFloat(f as f64))),
    ))(input)
}
