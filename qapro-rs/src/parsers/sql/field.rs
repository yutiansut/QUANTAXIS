use std::str::FromStr;

use crate::parsers::parser;
use crate::parsers::sql::Env;
use crate::parsers::sql::Expr;
use crate::parsers::value::PqlValue;

#[derive(Debug, Default, Clone, PartialEq)]
pub struct Field {
    pub expr: Expr,
    pub alias: Option<String>,
}

impl FromStr for Field {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> anyhow::Result<Self> {
        match parser::expressions::parse_field(s) {
            Ok((_, field)) => Ok(field),
            Err(nom::Err::Error(err)) => {
                eprint!("{:#?}", err);
                anyhow::bail!("failed")
            }
            _ => todo!(),
        }
    }
}

impl Field {
    pub fn expand_fullpath(&self, env: &Env) -> Self {
        Self {
            expr: self.expr.expand_fullpath(&env),
            alias: self.alias.to_owned(),
        }
    }

    pub fn evaluate(self, env: &Env) -> PqlValue {
        let value = self.expr.eval(&env);
        value
    }

    pub fn rename(self) -> (String, Expr) {
        if let Some(alias) = self.alias {
            (alias, self.expr)
        } else {
            let alias = match &self.expr {
                Expr::Selector(selector) => selector.to_vec().last().unwrap().to_string(),
                _ => todo!(),
            };
            (alias, self.expr)
        }
    }
}
