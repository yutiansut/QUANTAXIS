use std::collections::VecDeque;
use std::str::FromStr;

use crate::parsers::parser;
use crate::parsers::sql::Env;
use crate::parsers::sql::Expr;
use crate::parsers::value::PqlValue;

#[derive(Debug, Clone, PartialEq)]
pub enum SelectorNode {
    String(String),
    Number(i64),
}

impl Default for SelectorNode {
    fn default() -> Self {
        Self::String(String::default())
    }
}

impl From<&str> for SelectorNode {
    fn from(s: &str) -> Self {
        Self::String(s.to_string())
    }
}

impl From<i64> for SelectorNode {
    fn from(i: i64) -> Self {
        Self::Number(i)
    }
}

impl From<SelectorNode> for String {
    fn from(node: SelectorNode) -> Self {
        match node {
            SelectorNode::String(s) => s,
            SelectorNode::Number(i) => format!("{}", i),
        }
    }
}

impl SelectorNode {
    pub fn to_string(&self) -> String {
        String::from(self.to_owned())
    }
}

#[derive(Debug, Default, Clone, PartialEq)]
pub struct Selector {
    pub data: VecDeque<SelectorNode>,
}

impl FromStr for Selector {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> anyhow::Result<Self> {
        match parser::expressions::parse_selector(s) {
            Ok((_, r)) => Ok(r),
            Err(_err) => anyhow::bail!("failed"),
        }
    }
}

impl From<&[&str]> for Selector {
    fn from(ss: &[&str]) -> Self {
        let data = ss
            .iter()
            .map(|s| SelectorNode::String(s.to_string()))
            .collect::<VecDeque<_>>();
        Self { data }
    }
}

impl From<&[String]> for Selector {
    fn from(ss: &[String]) -> Self {
        let data = ss
            .iter()
            .map(|s| SelectorNode::String(s.to_string()))
            .collect::<VecDeque<_>>();
        Self { data }
    }
}

impl From<&str> for Selector {
    fn from(s: &str) -> Self {
        let data = s
            .to_string()
            .split(".")
            .map(|s| SelectorNode::String(s.to_string()))
            .collect::<VecDeque<_>>();
        Self { data }
    }
}

impl From<&SelectorNode> for Selector {
    fn from(node: &SelectorNode) -> Self {
        Self {
            data: vec![node]
                .into_iter()
                .map(|n| n.to_owned())
                .collect::<VecDeque<_>>(),
        }
    }
}
impl From<&[SelectorNode]> for Selector {
    fn from(nodes: &[SelectorNode]) -> Self {
        Self {
            data: nodes
                .into_iter()
                .map(|n| n.to_owned())
                .collect::<VecDeque<_>>(),
        }
    }
}

impl Selector {
    pub fn len(&self) -> usize {
        self.data.len()
    }

    pub fn get(&self, ith: usize) -> Option<SelectorNode> {
        self.data.get(ith).map(|e| e.to_owned())
    }

    pub fn last(&self) -> Option<String> {
        if let Some(last) = self.to_vec().last() {
            Some(last.to_string())
        } else {
            None
        }
    }

    pub fn split_first(&self) -> Option<(SelectorNode, Self)> {
        let mut data = self.data.to_owned();

        if let Some(first) = data.pop_front() {
            Some((first, Self { data }))
        } else {
            None
        }
    }

    pub fn split_last(&self) -> Option<(Self, SelectorNode)> {
        let mut data = self.data.to_owned();

        if let Some(last) = data.pop_back() {
            Some((Self { data }, last))
        } else {
            None
        }
    }

    pub fn to_string(&self) -> String {
        self.data
            .clone()
            .into_iter()
            .map(|node| node.to_string())
            .collect::<Vec<String>>()
            .join(".")
    }

    pub fn to_vec(&self) -> Vec<SelectorNode> {
        self.data.clone().into_iter().collect::<Vec<SelectorNode>>()
    }

    fn rec_get_full_path(&self, env: &Env, trace_path: &mut Selector) {
        if let Some((first, tail)) = self.split_first() {
            if let Some(alias_path) = env.get_as_selector(&first.to_string()) {
                alias_path.rec_get_full_path(env, trace_path)
            } else {
                (*trace_path).data.push_back(first);
            }
            if tail.data.len() > 0 {
                let tail_path = Selector::from(tail);
                let mut vec_path = tail_path.to_vec().into_iter().collect::<VecDeque<_>>();
                (*trace_path).data.append(&mut vec_path);
            }
        }
    }

    pub fn expand_fullpath2(&self, env: &Env) -> Self {
        let mut trace_path = Selector::default();
        self.rec_get_full_path(env, &mut trace_path);
        trace_path
    }

    pub fn expand_fullpath(&self, env: &Env) -> Self {
        if let Some((head, tail)) = self.split_first() {
            let mut selector = Selector::default();

            selector.data.append(
                &mut Selector::from(vec![head].as_slice())
                    .expand_fullpath2(&env)
                    .data,
            );
            selector.data.append(&mut tail.data.to_owned());
            selector
        } else {
            todo!()
        }
    }

    pub fn expand_abspath(&self, env: &Env) -> Self {
        if let Some((head, tail)) = self.split_first() {
            let mut selector = Selector::default();
            if head != SelectorNode::default() {
                selector.data.push_front(SelectorNode::default());
            }

            selector.data.append(
                &mut Selector::from(vec![head].as_slice())
                    .expand_fullpath2(env)
                    .data,
            );
            selector.data.append(&mut tail.data.to_owned());
            selector
        } else {
            todo!()
        }
    }

    pub fn evaluate(&self, env: &Env) -> PqlValue {
        if let Some((head, tail)) = self.expand_fullpath(&env).split_first() {
            if let Some(expr) = env.get(head.to_string().as_str()) {
                match expr {
                    Expr::Value(value) => {
                        let v = if tail.data.len() > 0 {
                            value.select_by_selector(&tail)
                        } else {
                            value
                        };
                        v
                    }
                    Expr::Selector(selector) => {
                        let s = selector.expand_fullpath2(&env);
                        s.evaluate(&env)
                    }
                    Expr::Star => todo!(),
                    Expr::Func(_) => todo!(),
                    Expr::Add(_, _) => todo!(),
                    Expr::Sub(_, _) => todo!(),
                    Expr::Mul(_, _) => todo!(),
                    Expr::Div(_, _) => todo!(),
                    Expr::Rem(_, _) => todo!(),
                    Expr::Exp(_, _) => todo!(),
                    Expr::Sql(_) => todo!(),
                }
            } else {
                self.expand_abspath(&env).evaluate(&env)
            }
        } else {
            unreachable!()
        }
    }

    pub fn intersect(&self, other: &Selector) -> Selector {
        let mut res = Selector::default();

        for (a, b) in self.data.iter().zip(other.data.iter()) {
            if a == b {
                res.data.push_back(a.to_owned())
            } else {
                break;
            }
        }

        res
    }
}

#[cfg(test)]
mod tests {
    use std::str::FromStr;

    use crate::parsers::planner::Drain;

    use crate::parsers::sql::Env;
    use crate::parsers::sql::Expr;
    use crate::parsers::sql::Field;
    use crate::parsers::sql::Selector;
    use crate::parsers::value::PqlValue;

    fn get_data() -> anyhow::Result<PqlValue> {
        PqlValue::from_str(
            r#"
{
  'hr': {
      'employeesNest': <<
         {
          'id': 3,
          'name': 'Bob Smith',
          'title': null,
          'projects': [ { 'name': 'AWS Redshift Spectrum querying' },
                        { 'name': 'AWS Redshift security' },
                        { 'name': 'AWS Aurora security' }
                      ]
          },
          {
              'id': 4,
              'name': 'Susan Smith',
              'title': 'Dev Mgr',
              'projects': []
          },
          {
              'id': 6,
              'name': 'Jane Smith',
              'title': 'Software Eng 2',
              'projects': [ { 'name': 'AWS Redshift security' } ]
          }
      >>
    }
}
    "#,
        )
    }

    #[test]
    fn test_eval_selector_fullpath() -> anyhow::Result<()> {
        let env = {
            let mut env = Env::default();
            let data = get_data()?;
            env.insert("", &Expr::Value(data));
            env
        };

        let selector = Selector::from_str(".hr.employeesNest.name")?;

        assert_eq!(
            selector.evaluate(&env),
            PqlValue::from_str(
                r#"
[
  "Bob Smith",
  "Susan Smith",
  "Jane Smith"
]
"#
            )?
        );
        Ok(())
    }

    #[test]
    fn test_eval_selector_aliaspath() -> anyhow::Result<()> {
        let env = {
            let mut env = Env::default();
            let data = get_data()?;
            env.insert("", &Expr::Value(data));
            let drain = Drain(vec![
                Field::from_str(r#"hr.employeesNest AS e"#)?,
                Field::from_str(r#"e.projects AS p"#)?,
            ]);
            drain.execute(&mut env);
            env
        };

        let selector = Selector::from_str("e.projects")?;
        assert_eq!(
            selector.evaluate(&env),
            PqlValue::from_str(
                r#"
[
  [
    {
      "name": "AWS Redshift Spectrum querying"
    },
    {
      "name": "AWS Redshift security"
    },
    {
      "name": "AWS Aurora security"
    }
  ],
  [],
  [
    {
      "name": "AWS Redshift security"
    }
  ]
]
"#
            )?
        );

        Ok(())
    }

    #[test]
    fn test_eval_selector_aliaspath2() -> anyhow::Result<()> {
        let env = {
            let mut env = Env::default();
            let data = get_data()?;
            env.insert("", &Expr::Value(data));
            let drain = Drain(vec![
                Field::from_str(r#"hr.employeesNest AS e"#)?,
                Field::from_str(r#"e.projects AS p"#)?,
            ]);
            drain.execute(&mut env);
            env
        };

        let selector = Selector::from_str("p")?;
        assert_eq!(
            selector.evaluate(&env),
            PqlValue::from_str(
                r#"
    [
      [
        {
          "name": "AWS Redshift Spectrum querying"
        },
        {
          "name": "AWS Redshift security"
        },
        {
          "name": "AWS Aurora security"
        }
      ],
      [],
      [
        {
          "name": "AWS Redshift security"
        }
      ]
    ]
    "#
            )?
        );
        Ok(())
    }

    #[test]
    fn test_eval_selector_num() -> anyhow::Result<()> {
        let env = {
            let mut env = Env::default();
            let data = get_data()?;
            env.insert("", &Expr::Value(data));
            let drain = Drain(vec![Field::from_str(r#"3 AS n"#)?]);
            drain.execute(&mut env);
            env
        };

        let selector = Selector::from_str("n")?;
        assert_eq!(selector.evaluate(&env), PqlValue::from_str("3")?);
        Ok(())
    }

    #[test]
    fn test_calculate_common_path() -> anyhow::Result<()> {
        let abc = Selector::from("a.b.c");
        let abd = Selector::from("a.b.d");

        let res = abc.intersect(&abd);

        assert_eq!(res, Selector::from("a.b"));

        Ok(())
    }

    #[test]
    fn test_eval_first_element() -> anyhow::Result<()> {
        let data = get_data()?;
        let env = Env::from(data);

        let selector = Selector::from_str("hr.employeesNest.projects[0]")?;
        assert_eq!(
            selector.evaluate(&env),
            PqlValue::from(vec![
                PqlValue::from_str(r#" { "name": "AWS Redshift Spectrum querying" } "#)?,
                PqlValue::Missing,
                PqlValue::from_str(r#" { "name": "AWS Redshift security" } "#)?
            ])
        );

        let selector = Selector::from_str("hr.employeesNest.projects[0].name")?;
        assert_eq!(
            selector.evaluate(&env),
            PqlValue::from(vec![
                PqlValue::from("AWS Redshift Spectrum querying"),
                PqlValue::Missing,
                PqlValue::from("AWS Redshift security")
            ])
        );
        Ok(())
    }
}
