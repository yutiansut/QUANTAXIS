use crate::parsers::planner::drain::Drain;
use crate::parsers::planner::filter::Filter;
use crate::parsers::planner::project::Projection;
use crate::parsers::sql::clause::Limit;
use crate::parsers::sql::clause::OrderBy;
use crate::parsers::sql::Env;

use crate::parsers::sql::Sql;
use crate::parsers::value::BPqlValue;
use crate::parsers::value::PqlValue;

#[derive(Debug, Default)]
pub struct LogicalPlan {
    pub drains: Vec<Drain>,
    pub filter: Filter,
    pub project: Projection,
    pub order_by: Option<OrderBy>,
    pub limit: Option<Limit>,
}

impl From<Sql> for LogicalPlan {
    fn from(sql: Sql) -> Self {
        Self {
            drains: vec![Drain(sql.from_clause), Drain(sql.left_join_clause)],
            filter: Filter(sql.where_clause),
            project: Projection(sql.select_clause),
            order_by: sql.orderby,
            limit: sql.limit,
        }
    }
}

impl LogicalPlan {
    pub fn execute(self, env: &mut Env) -> PqlValue {
        for drain in self.drains {
            drain.execute(env);
        }

        self.filter.execute(env);

        let mut list = self.project.execute(&env);

        if let Some(orderby) = &self.order_by {
            let mut list_with_key = list
                .into_iter()
                .filter_map(|record| {
                    record
                        .to_owned()
                        .get(&orderby.label)
                        .map(|value| (BPqlValue::from(value), record))
                })
                .collect::<Vec<_>>();
            list_with_key.sort_by(|x, y| {
                if orderby.is_asc {
                    x.0.partial_cmp(&y.0).unwrap()
                } else {
                    y.0.partial_cmp(&x.0).unwrap()
                }
            });
            list = list_with_key
                .into_iter()
                .map(|(_k, v)| v)
                .collect::<Vec<_>>();
        }

        if let Some(limit_clause) = &self.limit {
            let (_, values) = list.split_at(limit_clause.offset as usize);
            let (values, _) = values.split_at(limit_clause.limit as usize);
            list = values.to_owned();
        }

        PqlValue::Array(list)
    }
}
