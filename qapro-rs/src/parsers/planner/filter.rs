use crate::parsers::sql::re_from_str;
use crate::parsers::sql::Env;
use crate::parsers::sql::Expr;

use crate::parsers::sql::WhereCond;
use crate::parsers::value::PqlValue;

#[derive(Debug, Default, Clone)]
pub struct Filter(pub Option<Box<WhereCond>>);

impl Filter {
    pub fn execute(self, env: &mut Env) {
        if let Some(cond) = self.0 {
            let cond = &cond.to_owned().expand_fullpath(&env);
            if let Some(expr) = env.get("") {
                let data = match expr {
                    Expr::Value(value) => {
                        let restricted = value.restrict3(&cond, 0).expect("restricted value");
                        Expr::from(restricted)
                    }
                    _ => todo!(),
                };
                env.insert("", &data);
            };
        }
    }

    pub fn expand_fullpath(self, env: &Env) -> Self {
        match self.0 {
            Some(box cond) => Self(Some(Box::new(cond.expand_fullpath(env)))),
            None => Self(None),
        }
    }
}

impl PqlValue {
    fn restrict3(self, cond: &WhereCond, depth: usize) -> Option<Self> {
        match &self {
            PqlValue::Array(array) => {
                let arr = array
                    .into_iter()
                    .filter_map(|child| {
                        let vv = child.to_owned().restrict3(&cond, depth);
                        vv
                    })
                    .collect::<Vec<_>>();
                (!arr.is_empty()).then(|| PqlValue::from(arr))
            }
            PqlValue::Object(object) => {
                let obj = match cond.to_path().map(|selector| selector.get(depth)) {
                    Some(Some(head)) => {
                        if let Some(src) = object.get(head.to_string().as_str()) {
                            if let Some(dist) = src.to_owned().restrict3(cond, depth + 1) {
                                let mut restricted = object.to_owned();
                                restricted.insert(head.to_string(), dist);
                                let m = Some(PqlValue::from(restricted));
                                m
                            } else {
                                None
                            }
                        } else {
                            // MISSING
                            // Some(PqlValue::Null)
                            None
                        }
                    }
                    Some(None) => {
                        todo!()
                    }
                    _ => None,
                };
                obj
            }
            value => match cond.to_owned() {
                WhereCond::Eq { expr, right } => {
                    if expr.eval(&Env::from(value.to_owned())) == right {
                        Some(value.to_owned())
                    } else {
                        None
                    }
                }
                WhereCond::Neq { expr, right } => {
                    if expr.eval(&Env::from(value.to_owned())) != right {
                        Some(value.to_owned())
                    } else {
                        None
                    }
                }
                WhereCond::Like { expr: _, right } => {
                    if let PqlValue::Str(string) = &value {
                        if re_from_str(&right).is_match(&string) {
                            Some(value.to_owned())
                        } else {
                            None
                        }
                    } else {
                        todo!()
                    }
                }
            },
        }
    }
}

#[cfg(test)]
mod tests {
    use std::str::FromStr;

    use crate::parsers::pqlir_parser;

    use crate::parsers::sql::Expr;

    use crate::parsers::sql::Selector;

    use crate::parsers::sql::WhereCond;
    use crate::parsers::value::PqlValue;

    #[test]
    fn missing() -> anyhow::Result<()> {
        let value = PqlValue::from_str(
            "
    {
        'top': <<
            {'a': 1, 'b': true, 'c': 'alpha'},
            {'a': 2, 'b': null, 'c': 'beta'},
            {'a': 3, 'c': 'gamma'}
        >>
    }
       ",
        )?;
        let cond = WhereCond::Eq {
            expr: Expr::from(Selector::from("top.b")),
            right: PqlValue::from(true),
        };
        let expected = pqlir_parser::pql_value(
            "
    {
        'top': <<
            {'a': 1, 'b': true, 'c': 'alpha'}
        >>
    }
       ",
        )?;
        let res = value.restrict3(&cond, 0);
        assert_eq!(res, Some(expected));

        Ok(())
    }

    #[test]
    fn test_filter_scalar() -> anyhow::Result<()> {
        let value = PqlValue::from_str(
            "
<<
    {
        'id': 3,
        'name': 'Bob Smith',
        'title': null,
        'projects': [
            { 'name': 'AWS Redshift Spectrum querying' },
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
   ",
        )?;
        let cond = WhereCond::Eq {
            expr: Expr::from(Selector::from("id")),
            right: PqlValue::from(6.),
        };
        let res = value.restrict3(&cond, 0);
        let expected = pqlir_parser::pql_value(
            "
[
    {
        'id': 6,
        'name': 'Jane Smith',
        'title': 'Software Eng 2',
        'projects': [ { 'name': 'AWS Redshift security' } ]
    }
]
   ",
        )?;
        assert_eq!(res, Some(expected));
        Ok(())
    }

    #[test]
    fn test_filter_objects() -> anyhow::Result<()> {
        let value = PqlValue::from_str(
            "
<<
    {
        'id': 3,
        'name': 'Bob Smith',
        'title': null,
        'projects': [
            { 'name': 'AWS Redshift Spectrum querying' },
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
   ",
        )?;
        let cond = WhereCond::Like {
            expr: Expr::from(Selector::from("projects.name")),
            right: "%security%".to_owned(),
        };
        let res = value.restrict3(&cond, 0);
        let expected = pqlir_parser::pql_value(
            "
[
    {
        'id': 3,
        'name': 'Bob Smith',
        'title': null,
        'projects': [
            { 'name': 'AWS Redshift security' },
            { 'name': 'AWS Aurora security' }
        ]
    },
    {
        'id': 6,
        'name': 'Jane Smith',
        'title': 'Software Eng 2',
        'projects': [ { 'name': 'AWS Redshift security' } ]
    }
]
   ",
        )?;
        assert_eq!(res, Some(expected));
        Ok(())
    }

    #[test]
    fn test_filter_like() -> anyhow::Result<()> {
        let value = PqlValue::from_str(
            "
<<
    {
        'id': 3,
        'name': 'Bob Smith',
        'title': null,
        'projects': [
            'AWS Redshift Spectrum querying',
            'AWS Redshift security',
            'AWS Aurora security'
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
        'projects': [ 'AWS Redshift security' ]
    }
>>
       ",
        )?;
        let cond = WhereCond::Like {
            expr: Expr::from(Selector::from("projects")),
            right: "%security%".to_owned(),
        };
        let res = value.restrict3(&cond, 0);
        let expected = pqlir_parser::pql_value(
            "
[
    {
        'id': 3,
        'name': 'Bob Smith',
        'title': null,
        'projects': [
            'AWS Redshift security',
            'AWS Aurora security'
        ]
    },
    {
        'id': 6,
        'name': 'Jane Smith',
        'title': 'Software Eng 2',
        'projects': [ 'AWS Redshift security' ]
    }
]
           ",
        )?;
        assert_eq!(res, Some(expected));
        Ok(())
    }

    #[test]
    fn test_filter_even() -> anyhow::Result<()> {
        let value = PqlValue::from_str(
            "
[
    { 'n': 0 },
    { 'n': 1 },
    { 'n': 2 },
    { 'n': 3 }
]
       ",
        )?;

        // let env = Env::from(value.to_owned());
        let cond = WhereCond::Eq {
            expr: Expr::from_str("n%2")?,
            right: PqlValue::from(0.),
        };
        let res = value.restrict3(&cond, 0);
        let expected = pqlir_parser::pql_value(
            "
[
    { 'n': 0 },
    { 'n': 2 }
]
                   ",
        )?;
        assert_eq!(res, Some(expected));
        Ok(())
    }
}
