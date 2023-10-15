use collect_mac::collect;
use indexmap::IndexMap as Map;
use nom::branch::alt;
use nom::bytes::complete::{tag, tag_no_case};
use nom::character::complete::alphanumeric1;
use nom::character::complete::char;
use nom::character::complete::multispace0;
use nom::combinator::map;
use nom::combinator::opt;
use nom::multi::separated_list1;
use nom::sequence::delimited;
use nom::sequence::preceded;
use nom::sequence::tuple;
use nom::IResult;

pub use crate::parsers::parser;
pub use crate::parsers::parser::elements;
pub use crate::parsers::parser::elements::string_allowed_in_field;
pub use crate::parsers::parser::whitespace;
use crate::parsers::pqlir_parser;
pub use crate::parsers::sql::clause;
use crate::parsers::sql::Expr;
use crate::parsers::sql::Field;
use crate::parsers::sql::Selector;
use crate::parsers::sql::SelectorNode;
use crate::parsers::value::PqlValue;

pub fn pqlvalue_as_field(input: &str) -> IResult<&str, Field> {
    let (input, (value, alias)) = tuple((
        pqlir_parser::root,
        opt(preceded(
            opt(preceded(multispace0, tag_no_case("AS"))),
            preceded(multispace0, alphanumeric1),
        )),
    ))(input)?;

    let field = Field {
        expr: Expr::Value(value),
        alias: alias.map(String::from),
    };
    Ok((input, field))
}

pub fn parse_field(input: &str) -> IResult<&str, Field> {
    alt((expr_as_field, pqlvalue_as_field, selector_as_field))(input)
}

/// ```
/// use std::str::FromStr;
/// use piqel::parser;
/// use piqel::value::PqlValue;
/// fn main() -> anyhow::Result<()> {
///   let value = parser::expressions::pqlvalue_with_alias_to_pql_value(r#"[1,2,3] AS arr"#)?.1;
///   let expected = PqlValue::from_str(r#"{ "arr" : [1,2,3] }"#)?;
///   assert_eq!(value, expected);
///   Ok(())
/// }
/// ```
pub fn pqlvalue_with_alias_to_pql_value(input: &str) -> IResult<&str, PqlValue> {
    let (input, field) = pqlvalue_as_field(input)?;
    let value = match field {
        Field {
            expr: Expr::Value(value),
            alias: Some(alias),
        } => PqlValue::Object(collect! {
            as Map::<String , PqlValue>:
            alias.to_string() => value
        }),
        _ => todo!(),
    };
    Ok((input, value))
}

pub fn selector_as_field(input: &str) -> IResult<&str, Field> {
    let (input, (selector, alias)) = tuple((
        parse_selector,
        opt(preceded(
            opt(preceded(multispace0, tag_no_case("AS"))),
            preceded(multispace0, alphanumeric1),
        )),
    ))(input)?;

    let field = Field {
        expr: Expr::Selector(selector),
        alias: alias.map(String::from),
    };
    Ok((input, field))
}

pub fn projection(input: &str) -> IResult<&str, (Selector, Option<String>)> {
    let (input, (selector, opt_alias)) = tuple((
        parse_selector,
        opt(preceded(
            opt(preceded(multispace0, tag_no_case("AS"))),
            preceded(multispace0, alphanumeric1),
        )),
    ))(input)?;
    Ok((input, (selector, opt_alias.map(String::from))))
}

pub fn expr_as_field(input: &str) -> IResult<&str, Field> {
    // The math::parse must be placed after the parse_path_as_expr to prevent the inf keyword from being parsed.
    let (input, (expr, alias)) = tuple((
        parse_expr,
        opt(preceded(
            opt(preceded(multispace0, tag_no_case("AS"))),
            preceded(multispace0, alphanumeric1),
        )),
    ))(input)?;

    let field = Field {
        expr,
        alias: alias.map(String::from),
    };
    Ok((input, field))
}

pub fn parse_expr(input: &str) -> IResult<&str, Expr> {
    // The math::parse must be placed after the parse_path_as_expr to prevent the inf keyword from being parsed.
    alt((
        parse_star_as_expr,
        parser::math::parse,
        parser::elements::float_number,
        parser::func::function,
    ))(input)
}

pub fn parse_star_as_expr(input: &str) -> IResult<&str, Expr> {
    map(tag("*"), |_| Expr::Star)(input)
}

pub fn parse_sql_as_expr(_input: &str) -> IResult<&str, Expr> {
    todo!()
    // map(parse_field, |sql| Expr::Sql(sql))(input)
}

pub fn parse_alias_in_from_clause(input: &str) -> IResult<&str, String> {
    let (input, (_, alias)) = tuple((
        opt(preceded(whitespace, tag_no_case("AS"))),
        preceded(whitespace, string_allowed_in_field),
    ))(input)?;
    Ok((input, alias))
}

pub fn parse_selector(input: &str) -> IResult<&str, Selector> {
    pub fn selecotrnode_with_index<'a>(input: &str) -> IResult<&str, Vec<SelectorNode>> {
        let (input, (s, opt_i)) = tuple((
            string_allowed_in_field,
            opt(delimited(char('['), elements::integer, char(']'))),
        ))(input)?;

        let mut nodes = vec![];
        nodes.push(SelectorNode::String(s));
        if let Some(i) = opt_i {
            nodes.push(SelectorNode::Number(i as i64));
        };

        Ok((input, nodes))
    }

    let (input, (opt_dot, vec_nodes)) = tuple((
        opt(char('.')),
        separated_list1(char('.'), selecotrnode_with_index),
    ))(input)?;

    let mut nodes = vec![];
    if let Some(_dot) = opt_dot {
        nodes.push(SelectorNode::default())
    }
    let mut nodes2 = vec_nodes.into_iter().flatten().collect::<Vec<_>>();
    nodes.append(&mut nodes2);
    let res = Selector::from(nodes.as_slice());
    Ok((input, res))
}

pub fn parse_path_as_expr<'a>(input: &'a str) -> IResult<&'a str, Expr> {
    map(parse_selector, |selector| Expr::Selector(selector))(input)
}

#[cfg(test)]
mod tests {
    use super::parse_selector;
    use crate::parsers::parser;
    use crate::parsers::sql::Selector;
    use crate::parsers::sql::SelectorNode;
    use crate::parsers::value::PqlValue;
    use std::str::FromStr;

    #[test]
    fn selector_xyz() -> anyhow::Result<()> {
        let (_, selector) = parse_selector("x.y.z")?;

        let expected = Selector::from(
            vec![
                SelectorNode::from("x"),
                SelectorNode::from("y"),
                SelectorNode::from("z"),
            ]
            .as_slice(),
        );

        assert_eq!(selector, expected);
        Ok(())
    }

    #[test]
    fn selector_xy2z() -> anyhow::Result<()> {
        let (_, selector) = parse_selector("x.y[2].z")?;

        let expected = Selector::from(
            vec![
                SelectorNode::from("x"),
                SelectorNode::from("y"),
                SelectorNode::from(2),
                SelectorNode::from("z"),
            ]
            .as_slice(),
        );

        assert_eq!(selector, expected);
        Ok(())
    }

    #[test]
    fn alias_pql_vlaue_to_pql_value() -> anyhow::Result<()> {
        let value = parser::expressions::pqlvalue_with_alias_to_pql_value(r#"[1,2,3] AS arr"#)?.1;
        let expected = PqlValue::from_str(r#"{ "arr" : [1,2,3] }"#)?;
        assert_eq!(value, expected);
        Ok(())
    }
}
