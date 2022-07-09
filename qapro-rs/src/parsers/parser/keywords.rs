use nom::branch::alt;
use nom::bytes::complete::{tag, tag_no_case};

use nom::combinator::peek;

use nom::sequence::terminated;

use nom::IResult;

use crate::parsers::parser::elements::eof;

fn keyword_follow_char(input: &str) -> IResult<&str, &str> {
    peek(alt((
        tag(" "),
        tag("\n"),
        tag(";"),
        tag("("),
        tag(")"),
        tag("\t"),
        tag(","),
        tag("="),
        eof,
    )))(input)
}

pub fn sql_keyword(input: &str) -> IResult<&str, &str> {
    alt((
        terminated(tag_no_case("SELECT"), keyword_follow_char),
        terminated(tag_no_case("FROM"), keyword_follow_char),
        terminated(tag_no_case("WHERE"), keyword_follow_char),
        terminated(tag_no_case("ORDER"), keyword_follow_char),
        terminated(tag_no_case("BY"), keyword_follow_char),
        terminated(tag_no_case("ASC"), keyword_follow_char),
        terminated(tag_no_case("DESC"), keyword_follow_char),
        terminated(tag_no_case("LIMIT"), keyword_follow_char),
        terminated(tag_no_case("OFFSET"), keyword_follow_char),
    ))(input)
}

pub fn clause_delimiter(input: &str) -> IResult<&str, &str> {
    alt((sql_keyword, eof))(input)
}
