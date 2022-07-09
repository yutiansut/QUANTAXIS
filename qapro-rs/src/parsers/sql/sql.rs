use std::str::FromStr;

use crate::parsers::parser;
pub use crate::parsers::sql::clause::Limit;
pub use crate::parsers::sql::clause::OrderBy;
use crate::parsers::sql::Field;
pub use crate::parsers::sql::WhereCond;

#[derive(Debug, Default, Clone, PartialEq)]
pub struct Sql {
    pub select_clause: Vec<Field>,
    pub calc_clause: Vec<Field>,
    pub from_clause: Vec<Field>,
    pub left_join_clause: Vec<Field>,
    pub where_clause: Option<Box<WhereCond>>,
    pub orderby: Option<OrderBy>,
    pub limit: Option<Limit>,
}

impl FromStr for Sql {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> anyhow::Result<Self> {
        parser::select_statement::from_str(s)
    }
}
