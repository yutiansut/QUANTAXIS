use nom::branch::alt;
use nom::bytes::complete::escaped;
use nom::bytes::complete::tag;
use nom::bytes::complete::take_while;
use nom::character::complete::alphanumeric1;
use nom::character::complete::char;
use nom::character::complete::digit1;
use nom::character::complete::multispace0;
use nom::character::complete::one_of;
use nom::character::complete::space1;
use nom::combinator::cut;
use nom::error::{ErrorKind, ParseError};
use nom::multi::many1;
use nom::number::complete::recognize_float;
use nom::sequence::delimited;
use nom::sequence::{preceded, terminated};
use nom::{IResult, InputLength};

use crate::parsers::sql::Expr;

pub fn eof<I: Copy + InputLength, E: ParseError<I>>(input: I) -> IResult<I, I, E> {
    if input.input_len() == 0 {
        Ok((input, input))
    } else {
        Err(nom::Err::Error(E::from_error_kind(input, ErrorKind::Eof)))
    }
}

pub fn comma(input: &str) -> IResult<&str, &str> {
    delimited(multispace0, tag(","), multispace0)(input)
}

pub fn whitespace<'a, E: ParseError<&'a str>>(input: &'a str) -> IResult<&'a str, &'a str, E> {
    let chars = " \t\r\n";
    take_while(move |c| chars.contains(c))(input)
}

pub fn string_allowed_in_field<'a>(input: &'a str) -> IResult<&'a str, String> {
    let (input, ss) = many1(alt((alphanumeric1, tag("_"))))(input)?;

    Ok((input, ss.into_iter().collect::<String>()))
}

pub fn integer<'a>(input: &'a str) -> IResult<&'a str, u64> {
    let (input, s) = digit1(input)?;
    match s.parse::<u64>() {
        Ok(i) => Ok((input, i)),
        Err(_) => Err(nom::Err::Error(ParseError::from_error_kind(
            input,
            ErrorKind::Float,
        ))),
    }
}

// Unlike nom::complete::{float, double}, this function does not parse `inf` keyword
pub fn float_number<'a>(input: &'a str) -> IResult<&'a str, Expr> {
    let (input, s) = recognize_float(input)?;
    match s.parse::<f64>() {
        Ok(f) => Ok((input, Expr::from(f))),
        Err(_) => Err(nom::Err::Error(ParseError::from_error_kind(
            input,
            ErrorKind::Float,
        ))),
    }
}

pub fn string<'a>(input: &'a str) -> IResult<&'a str, &'a str> {
    alt((
        preceded(char('"'), cut(terminated(parse_str, char('"')))),
        preceded(char('\''), cut(terminated(parse_str, char('\'')))),
    ))(input)
}

fn parse_str<'a, E: ParseError<&'a str>>(i: &'a str) -> IResult<&'a str, &'a str, E> {
    escaped(
        alt((alphanumeric1, space1, tag("%"))),
        '\\',
        one_of("\"n\\"),
    )(i)
}

#[cfg(test)]
mod tests {
    use super::float_number;
    use crate::parsers::sql::Expr;
    use crate::parsers::value::PqlValue;

    fn float(input: &str) -> anyhow::Result<Expr> {
        match float_number(input) {
            Ok((_, f)) => Ok(f),
            Err(_err) => anyhow::bail!("fail"),
        }
    }

    #[test]
    fn parse_float_number() -> anyhow::Result<()> {
        assert_eq!(float("3.4E3")?, Expr::Value(PqlValue::from(3.4e3)));

        Ok(())
    }
}
