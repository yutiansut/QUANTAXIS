pub use crate::parsers::planner::LogicalPlan;
pub use crate::parsers::sql::clause::Limit;
pub use crate::parsers::sql::clause::OrderBy;
use crate::parsers::sql::Env;
use crate::parsers::sql::Expr;
use crate::parsers::sql::Sql;
use crate::parsers::value::PqlValue;

pub fn evaluate<'a>(sql: Sql, data: PqlValue) -> PqlValue {
    let mut env = Env::default();
    env.insert("", &Expr::from(data));
    let plan = LogicalPlan::from(sql);
    let result = plan.execute(&mut env);
    result
}

#[cfg(test)]
mod tests {
    use std::str::FromStr;

    use crate::parsers::planner::LogicalPlan;
    use crate::parsers::sql::Env;
    use crate::parsers::sql::Sql;
    use crate::parsers::value::PqlValue;

    #[test]
    fn test_rename() -> anyhow::Result<()> {
        let sql = Sql::from_str(
            r#"
SELECT e.id,
       e.name AS employeeName,
       e.title AS title
FROM
    {
        'employees': <<
            { 'id': 3, 'name': 'Bob Smith',   'title': null },
            { 'id': 4, 'name': 'Susan Smith', 'title': 'Dev Mgr' },
            { 'id': 6, 'name': 'Jane Smith',  'title': 'Software Eng 2'}
        >>
    } AS hr,
    hr.employees e
LIMIT 2
        "#,
        )?;

        let plan = LogicalPlan::from(sql);
        let mut env = Env::default();
        let res = plan.execute(&mut env);

        assert_eq!(
            res,
            PqlValue::from_str(
                r#"
        [
            { 'id': 3, 'employeeName': 'Bob Smith',   'title': null },
            { 'id': 4, 'employeeName': 'Susan Smith', 'title': 'Dev Mgr' }
        ]
            "#
            )?
        );

        Ok(())
    }
}
