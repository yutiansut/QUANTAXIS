
use indexmap::IndexMap as Map;

use crate::parsers::sql::Expr;
use crate::parsers::sql::Selector;
use crate::parsers::sql::SelectorNode;
use crate::parsers::value::PqlValue;

#[derive(Debug, Default, Clone)]
pub struct Env {
    data: Map<String, Expr>,
}

impl From<PqlValue> for Env {
    fn from(value: PqlValue) -> Self {
        let mut env = Self::default();
        env.insert("", &Expr::from(value));
        env
    }
}

impl Env {
    pub fn insert(&mut self, alias: &str, expr: &Expr) -> Option<Expr> {
        self.data.insert(alias.to_string(), expr.to_owned())
    }

    pub fn insert_from_selector(&mut self, alias: &str, selector: &Selector) -> Option<Expr> {
        let value = Expr::Selector(selector.to_owned());
        self.insert(alias, &value)
    }

    pub fn insert_from_pqlval(&mut self, alias: &str, value: &PqlValue) -> Option<Expr> {
        let value = Expr::Value(value.to_owned());
        self.insert(alias, &value)
    }

    pub fn get(&self, key: &str) -> Option<Expr> {
        self.data.get(key).map(|e| e.to_owned())
    }

    pub fn get_mut(&mut self, key: &str) -> Option<&mut Expr> {
        self.data.get_mut(key)
    }

    pub fn get_by_selector(&self, selector: &Selector) -> PqlValue {
        if let Some((head, tail)) = selector.split_first() {
            if let Some(expr) = self.get(head.to_string().as_str()) {
                match expr {
                    Expr::Value(value) => {
                        let v = if tail.data.len() > 0 {
                            value.select_by_selector(&tail)
                        } else {
                            value
                        };
                        v
                    }
                    _ => todo!(),
                }
            } else {
                todo!()
            }
        } else {
            unreachable!()
        }
    }

    pub fn get_as_selector(&self, key: &str) -> Option<Selector> {
        match self.get(key) {
            Some(Expr::Selector(selector)) => Some(selector),
            _ => None,
        }
    }
}

#[cfg(test)]
mod tests {
    use std::str::FromStr;

    use super::Env;
    use crate::parsers::planner::Drain;
    use crate::parsers::sql::Expr;
    use crate::parsers::sql::Field;
    use crate::parsers::sql::Sql;

    #[test]
    fn get_full_path() -> anyhow::Result<()> {
        let sql = Sql::from_str(
            r#"
SELECT
  e.name AS employeeName, p.name AS projectName
FROM
  hr.employeesNest AS e, e.projects AS p
        "#,
        )?;

        let mut env = Env::default();
        Drain(sql.from_clause).execute(&mut env);

        assert_eq!(
            Field::from_str("e.name AS employeeName")?
                .expr
                .expand_fullpath(&env)
                .to_string(),
            "hr.employeesNest.name",
        );

        assert_eq!(
            Field::from_str("p.name AS projectName")?
                .expr
                .expand_fullpath(&env)
                .to_string(),
            "hr.employeesNest.projects.name",
        );

        Ok(())
    }

    #[test]
    fn test_update_env() -> anyhow::Result<()> {
        let mut env = Env::default();
        env.insert("name", &Expr::from("Alice"));

        if let Some(name) = env.get_mut("name") {
            *name = Expr::from("Bob");
        }

        assert_eq!(env.get("name"), Some(Expr::from("Bob")));

        Ok(())
    }
}
