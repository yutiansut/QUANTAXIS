use nom::branch::alt;
use nom::bytes::complete::{tag, tag_no_case};
use nom::character::complete::{multispace0, multispace1};
use nom::combinator::opt;
use nom::error::context;
use nom::multi::separated_list1;
use nom::sequence::{preceded, tuple};
use nom::IResult;

pub use crate::parsers::parser::elements;
pub use crate::parsers::parser::elements::comma;
pub use crate::parsers::parser::expressions;
pub use crate::parsers::parser::keywords;
pub use crate::parsers::parser::parse_expr;
pub use crate::parsers::parser::parse_value;
pub use crate::parsers::parser::string_allowed_in_field;
pub use crate::parsers::sql::clause;
use crate::parsers::sql::Field;
use crate::parsers::sql::WhereCond;

pub fn select(input: &str) -> IResult<&str, Vec<Field>> {
    let (input, vec) = context(
        "select claues",
        preceded(
            tag_no_case("SELECT"),
            preceded(
                multispace0,
                separated_list1(comma, expressions::parse_field),
            ),
        ),
    )(input)?;
    Ok((input, vec))
}
pub fn calc(input: &str) -> IResult<&str, Vec<Field>> {
    let (input, vec) = context(
        "calc claues",
        preceded(
            tag_no_case("CALC"),
            preceded(
                multispace0,
                separated_list1(comma, expressions::parse_field),
            ),
        ),
    )(input)?;
    Ok((input, vec))
}
pub fn from<'a>(input: &'a str) -> IResult<&'a str, Vec<Field>> {
    let (input, fields) = context(
        "from clause",
        preceded(
            tag_no_case("FROM"),
            preceded(
                multispace0,
                preceded(
                    multispace0,
                    separated_list1(comma, expressions::parse_field),
                ),
            ),
        ),
    )(input)?;
    Ok((input, fields))
}

pub fn left_join<'a>(input: &'a str) -> IResult<&'a str, Vec<Field>> {
    let (input, fields) = context(
        "left join clause",
        preceded(
            tuple((tag_no_case("LEFT"), multispace1, tag_no_case("JOIN"))),
            preceded(
                multispace0,
                preceded(
                    multispace0,
                    separated_list1(comma, expressions::parse_field),
                ),
            ),
        ),
    )(input)?;
    Ok((input, fields))
}

pub fn parse_where(input: &str) -> IResult<&str, WhereCond> {
    preceded(
        tag_no_case("WHERE"),
        alt((parse_where_eq, parse_where_like)),
    )(input)
}

pub fn parse_where_eq(input: &str) -> IResult<&str, WhereCond> {
    let (input, (expr, _, right)) = preceded(
        multispace0,
        tuple((
            parse_expr,
            preceded(multispace0, tag("=")),
            preceded(multispace0, parse_value),
        )),
    )(input)?;
    let res = WhereCond::Eq { expr, right };
    Ok((input, res))
}

pub fn parse_where_like(input: &str) -> IResult<&str, WhereCond> {
    let (input, (expr, _, s)) = preceded(
        multispace0,
        tuple((
            parse_expr,
            preceded(multispace0, tag_no_case("LIKE")),
            preceded(multispace0, elements::string),
        )),
    )(input)?;
    let res = WhereCond::Like {
        expr,
        right: s.to_string(),
    };
    Ok((input, res))
}

pub fn orderby(input: &str) -> IResult<&str, clause::OrderBy> {
    let (input, (_, field_name, opt_asc_or_desc)) = tuple((
        tag_no_case("ORDER BY"),
        preceded(multispace0, string_allowed_in_field),
        preceded(
            multispace0,
            opt(alt((tag_no_case("ASC"), tag_no_case("DESC")))),
        ),
    ))(input)?;

    let is_asc = opt_asc_or_desc
        .map(|asc_or_desc| asc_or_desc.to_lowercase() == "asc")
        .unwrap_or(true);
    Ok((
        input,
        clause::OrderBy {
            label: field_name,
            is_asc,
        },
    ))
}

pub fn limit(input: &str) -> IResult<&str, clause::Limit> {
    let (input, (_, limit, opt_offset)) = tuple((
        tag_no_case("LIMIT"),
        preceded(multispace0, elements::integer),
        opt(preceded(multispace0, offset)),
    ))(input)?;

    let offset = opt_offset.unwrap_or(0);
    Ok((input, clause::Limit { limit, offset }))
}

pub fn offset(input: &str) -> IResult<&str, u64> {
    preceded(
        tag_no_case("OFFSET"),
        preceded(multispace0, elements::integer),
    )(input)
}

#[cfg(test)]
mod tests {
    use std::str::FromStr;

    use super::from;
    use crate::parsers::sql::Field;

    #[test]
    fn parse_from() -> anyhow::Result<()> {
        assert_eq!(from("FROM [1,2,3]")?.1, vec![Field::from_str("[1,2,3]")?],);
        assert_eq!(
            from("FROM [1,2,3] AS arr")?.1,
            vec![Field::from_str("[1,2,3] AS arr")?],
        );
        assert_eq!(
            from("FROM x.y.z AS xyz")?.1,
            vec![Field::from_str("x.y.z AS xyz")?],
        );

        Ok(())
    }
}
