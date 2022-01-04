use nom::character::complete::multispace0;
use nom::{
    branch::alt,
    combinator::opt,
    sequence::{preceded, tuple},
    IResult,
};

use crate::parsers::parser::clauses;

use crate::parsers::sql::Sql;

pub fn from_str(input: &str) -> anyhow::Result<Sql> {
    match parse_planner_sql(input) {
        Ok((_, sql)) => Ok(sql),
        Err(nom::Err::Incomplete(_needed)) => {
            anyhow::bail!("needed")
        }
        Err(nom::Err::Error(err)) => {
            dbg!(&err);
            eprintln!("{}", err);
            anyhow::bail!("parser error")
        }
        Err(nom::Err::Failure(err)) => {
            dbg!(&err);
            eprintln!("{}", err);
            anyhow::bail!("parse failed")
        }
    }
}

pub fn parse_planner_sql(input: &str) -> IResult<&str, Sql> {
    alt((parse_sql21, parse_sql22))(input)
}

pub fn parse_sql21(input: &str) -> IResult<&str, Sql> {
    let (
        input,
        (
            opt_select_clause,
            opt_calc_clause,
            opt_from_clause,
            opt_left_join_clause,
            opt_where_clause,
            opt_order_by,
            opt_limit,
        ),
    ) = tuple((
        opt(preceded(multispace0, clauses::select)),
        opt(preceded(multispace0, clauses::calc)),
        opt(preceded(multispace0, clauses::from)),
        opt(preceded(multispace0, clauses::left_join)),
        opt(preceded(multispace0, clauses::parse_where)),
        opt(preceded(multispace0, clauses::orderby)),
        opt(preceded(multispace0, clauses::limit)),
    ))(input)?;

    let sql = Sql {
        select_clause: opt_select_clause.unwrap_or_default(),
        calc_clause: opt_calc_clause.unwrap_or_default(),
        from_clause: opt_from_clause.unwrap_or_default(),
        left_join_clause: opt_left_join_clause.unwrap_or_default(),
        where_clause: opt_where_clause.map(Box::new),
        orderby: opt_order_by,
        limit: opt_limit,
    };
    Ok((input, sql))
}

pub fn parse_sql22(input: &str) -> IResult<&str, Sql> {
    let (
        input,
        (
            opt_from_clause,
            opt_left_join_clause,
            opt_where_clause,
            opt_select_clause,
            opt_calc_clause,
            opt_order_by,
            opt_limit,
        ),
    ) = tuple((
        opt(preceded(multispace0, clauses::from)),
        opt(preceded(multispace0, clauses::left_join)),
        opt(preceded(multispace0, clauses::parse_where)),
        opt(preceded(multispace0, clauses::select)),
        opt(preceded(multispace0, clauses::calc)),
        opt(preceded(multispace0, clauses::orderby)),
        opt(preceded(multispace0, clauses::limit)),
    ))(input)?;

    let sql = Sql {
        select_clause: opt_select_clause.unwrap_or_default(),
        calc_clause: opt_calc_clause.unwrap_or_default(),
        from_clause: opt_from_clause.unwrap_or_default(),
        left_join_clause: opt_left_join_clause.unwrap_or_default(),
        where_clause: opt_where_clause.map(Box::new),
        orderby: opt_order_by,
        limit: opt_limit,
    };
    Ok((input, sql))
}
