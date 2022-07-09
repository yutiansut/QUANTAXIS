use std::collections::HashSet;
use std::str::FromStr;

use collect_mac::collect;
use ordered_float::OrderedFloat;

use crate::parsers::parser;
use crate::parsers::sql::Env;
use crate::parsers::sql::Func;
use crate::parsers::sql::Selector;
use crate::parsers::sql::Sql;
use crate::parsers::value::PqlValue;

#[derive(Debug, Clone, PartialEq)]
pub enum Expr {
    Star,
    Selector(Selector),
    Value(PqlValue),
    Func(Box<Func>),
    Add(Box<Expr>, Box<Expr>),
    Sub(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
    Div(Box<Expr>, Box<Expr>),
    Rem(Box<Expr>, Box<Expr>),
    Exp(Box<Expr>, Box<Expr>),
    Sql(Sql),
}

impl Default for Expr {
    fn default() -> Self {
        Self::Value(PqlValue::default())
    }
}

impl From<i64> for Expr {
    fn from(i: i64) -> Self {
        Self::Value(PqlValue::Int(i))
    }
}

impl From<f64> for Expr {
    fn from(f: f64) -> Self {
        Self::Value(PqlValue::Float(OrderedFloat(f)))
    }
}

impl From<&str> for Expr {
    fn from(s: &str) -> Self {
        Self::Value(PqlValue::from(s))
    }
}

impl From<Selector> for Expr {
    fn from(selector: Selector) -> Self {
        Self::Selector(selector)
    }
}

impl From<PqlValue> for Expr {
    fn from(value: PqlValue) -> Self {
        Self::Value(value)
    }
}

impl From<Expr> for String {
    fn from(expr: Expr) -> Self {
        match expr {
            Expr::Selector(selector) => selector.to_string(),
            Expr::Value(value) => value.to_json().expect("to json"),
            _ => todo!(),
        }
    }
}

impl FromStr for Expr {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> anyhow::Result<Self> {
        match parser::expressions::parse_expr(s) {
            Ok((_, expr)) => Ok(expr),
            Err(nom::Err::Error(err)) => {
                eprint!("{}", err);
                anyhow::bail!("failed")
            }
            _ => todo!(),
        }
    }
}

impl Expr {
    pub fn to_string(self) -> String {
        String::from(self)
    }

    pub fn as_path(&self) -> Option<Selector> {
        match self {
            Expr::Selector(path) => Some(path.to_owned()),
            _ => None,
        }
    }

    pub fn expand_fullpath(&self, env: &Env) -> Self {
        match self {
            Self::Selector(path) => Self::Selector(path.expand_fullpath2(&env)),
            Expr::Value(_) => self.to_owned(),
            Expr::Star => todo!(),
            Expr::Func(_) => todo!(),
            Self::Add(left, right) => Self::Add(
                Box::new((*left).expand_fullpath(&env)),
                Box::new((*right).expand_fullpath(&env)),
            ),
            Self::Sub(left, right) => Self::Sub(
                Box::new((*left).expand_fullpath(&env)),
                Box::new((*right).expand_fullpath(&env)),
            ),
            Self::Mul(left, right) => Self::Mul(
                Box::new((*left).expand_fullpath(&env)),
                Box::new((*right).expand_fullpath(&env)),
            ),
            Self::Div(left, right) => Self::Div(
                Box::new((*left).expand_fullpath(&env)),
                Box::new((*right).expand_fullpath(&env)),
            ),
            Self::Rem(left, right) => Self::Rem(
                Box::new((*left).expand_fullpath(&env)),
                Box::new((*right).expand_fullpath(&env)),
            ),
            Self::Exp(left, right) => Self::Exp(
                Box::new((*left).expand_fullpath(&env)),
                Box::new((*right).expand_fullpath(&env)),
            ),
            Expr::Sql(_) => todo!(),
        }
    }

    pub fn eval(self, env: &Env) -> PqlValue {
        match self.to_owned() {
            Self::Value(value) => value,
            Self::Selector(selector) => selector.evaluate(&env),
            Self::Star => todo!(),
            Self::Func(_) => todo!(),
            Self::Sql(_) => todo!(),
            Self::Add(box expr1, box expr2) => (expr1).eval(&env) + (expr2).eval(&env),
            Self::Sub(box expr1, box expr2) => (expr1).eval(&env) - (expr2).eval(&env),
            Self::Mul(box expr1, box expr2) => (expr1).eval(&env) * (expr2).eval(&env),
            Self::Div(box expr1, box expr2) => (expr1).eval(&env) / (expr2).eval(&env),
            Self::Rem(box expr1, box expr2) => (expr1).eval(&env) % (expr2).eval(&env),
            Self::Exp(box expr1, box expr2) => (expr1).eval(&env).powf((expr2).eval(&env)),
        }
    }

    pub fn source_field_name_set(&self, env: &Env) -> HashSet<String> {
        match self.to_owned() {
            Expr::Selector(selector) => {
                collect! {
                    as HashSet<String>:
                    selector.expand_fullpath2(&env).to_string()
                }
            }
            Expr::Add(box expr1, box expr2) => {
                let a = expr1.source_field_name_set(&env);
                let b = expr2.source_field_name_set(&env);
                a.union(&b).map(String::from).collect::<HashSet<_>>()
            }
            Expr::Sub(box expr1, box expr2) => {
                let a = expr1.source_field_name_set(&env);
                let b = expr2.source_field_name_set(&env);
                a.union(&b).map(String::from).collect::<HashSet<_>>()
            }
            Expr::Mul(box expr1, box expr2) => {
                let a = expr1.source_field_name_set(&env);
                let b = expr2.source_field_name_set(&env);
                a.union(&b).map(String::from).collect::<HashSet<_>>()
            }
            Expr::Div(box expr1, box expr2) => {
                let a = expr1.source_field_name_set(&env);
                let b = expr2.source_field_name_set(&env);
                a.union(&b).map(String::from).collect::<HashSet<_>>()
            }
            Expr::Rem(box expr1, box expr2) => {
                let a = expr1.source_field_name_set(&env);
                let b = expr2.source_field_name_set(&env);
                a.union(&b).map(String::from).collect::<HashSet<_>>()
            }
            Expr::Exp(box expr1, box expr2) => {
                let a = expr1.source_field_name_set(&env);
                let b = expr2.source_field_name_set(&env);
                a.union(&b).map(String::from).collect::<HashSet<_>>()
            }
            _ => {
                dbg!(&self);
                todo!();
            }
        }
    }

    pub fn to_path(&self) -> Option<Selector> {
        match self.to_owned() {
            Self::Value(_value) => None,
            Self::Selector(selector) => Some(selector),
            Self::Star => todo!(),
            Self::Func(_) => todo!(),
            Self::Sql(_) => todo!(),
            Self::Add(box expr1, box expr2) => match (expr1.to_path(), expr2.to_path()) {
                (Some(s1), Some(s2)) => Some(s1.intersect(&s2)),
                (Some(s1), _) => Some(s1),
                (_, Some(s2)) => Some(s2),
                _ => None,
            },
            Self::Sub(box expr1, box expr2) => match (expr1.to_path(), expr2.to_path()) {
                (Some(s1), Some(s2)) => Some(s1.intersect(&s2)),
                (Some(s1), _) => Some(s1),
                (_, Some(s2)) => Some(s2),
                _ => None,
            },
            Self::Mul(box expr1, box expr2) => match (expr1.to_path(), expr2.to_path()) {
                (Some(s1), Some(s2)) => Some(s1.intersect(&s2)),
                (Some(s1), _) => Some(s1),
                (_, Some(s2)) => Some(s2),
                _ => None,
            },
            Self::Div(box expr1, box expr2) => match (expr1.to_path(), expr2.to_path()) {
                (Some(s1), Some(s2)) => Some(s1.intersect(&s2)),
                (Some(s1), _) => Some(s1),
                (_, Some(s2)) => Some(s2),
                _ => None,
            },
            Self::Rem(box expr1, box expr2) => match (expr1.to_path(), expr2.to_path()) {
                (Some(s1), Some(s2)) => Some(s1.intersect(&s2)),
                (Some(s1), _) => Some(s1),
                (_, Some(s2)) => Some(s2),
                _ => None,
            },
            Self::Exp(box expr1, box expr2) => match (expr1.to_path(), expr2.to_path()) {
                (Some(s1), Some(s2)) => Some(s1.intersect(&s2)),
                (Some(s1), _) => Some(s1),
                (_, Some(s2)) => Some(s2),
                _ => None,
            },
        }
    }
}

#[cfg(test)]
mod tests {
    use std::str::FromStr;

    use crate::parsers::parser;
    use crate::parsers::planner::LogicalPlan;
    use crate::parsers::sql::Env;
    use crate::parsers::sql::Expr;
    use crate::parsers::sql::Selector;
    use crate::parsers::sql::Sql;
    use crate::parsers::value::PqlValue;

    #[test]
    fn test_expr_mul() -> anyhow::Result<()> {
        let mut sql = Sql::default();
        sql.select_clause = parser::clauses::select(r#"SELECT 4 * a AS aa"#)?.1;
        sql.from_clause = parser::clauses::from("FROM 3 as a")?.1;
        let plan = LogicalPlan::from(sql);

        let mut env = Env::default();
        let res = plan.execute(&mut env);

        assert_eq!(res, PqlValue::from_str(r#"[{ "aa": 12 }]"#)?);

        Ok(())
    }
    #[test]
    fn test_expr_calc() -> anyhow::Result<()> {
        let mut sql = Sql::default();
        sql.select_clause = parser::clauses::select(r#"CALC 4 * a AS aa"#)?.1;
        println!("{:#?}", sql.select_clause);
        sql.from_clause = parser::clauses::from("FROM 3 as a")?.1;
        let plan = LogicalPlan::from(sql);

        let mut env = Env::default();
        let res = plan.execute(&mut env);

        assert_eq!(res, PqlValue::from_str(r#"[{ "aa": 12 }]"#)?);

        Ok(())
    }

    #[test]
    fn test_get_common_path() -> anyhow::Result<()> {
        let expr = Expr::from_str("a.b.c + a.b.d")?;

        let res = expr.to_path();

        assert_eq!(res, Some(Selector::from(r#"a.b"#)));

        Ok(())
    }

    #[test]
    fn test_get_common_math() -> anyhow::Result<()> {
        let expr = Expr::from_str("a.b * 2")?;

        let res = expr.to_path();

        assert_eq!(res, Some(Selector::from(r#"a.b"#)));

        Ok(())
    }
}
