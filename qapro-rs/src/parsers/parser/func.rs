use nom::branch::alt;
use nom::bytes::complete::{ tag_no_case};
use nom::character::complete::char;
use nom::combinator::cut;
use nom::sequence::{preceded, terminated, tuple};
use nom::IResult;

use crate::parsers::sql::Expr;
use crate::parsers::sql::Func;

use crate::parsers::parser::{parse_expr, whitespace};

pub fn function(input: &str) -> IResult<&str, Expr> {
    let (input, (funcname, _, expr)) = tuple((
        preceded(
            whitespace,
            alt((
                tag_no_case("count"),
                tag_no_case("upper"),
                tag_no_case("lower"),
                tag_no_case("ceil"),
                tag_no_case("floor"),
                tag_no_case("round"),
            )),
        ),
        char('('),
        cut(terminated(
            preceded(whitespace, parse_expr),
            preceded(whitespace, char(')')),
        )),
    ))(input)?;

    let func = match funcname.to_lowercase().as_str() {
        "count" => Func::Count(expr),
        "upper" => Func::Upper(expr),
        _ => todo!(),
    };

    let res = Expr::Func(Box::new(func));

    Ok((input, res))
}
