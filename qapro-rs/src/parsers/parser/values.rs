use nom::character::complete::multispace0;
use nom::{
    character::complete::{char, digit1},
    combinator::cut,
    error::context,
    multi::separated_list0,
    sequence::{preceded, terminated},
    IResult,
};

pub fn array<'a>(input: &'a str) -> IResult<&'a str, Vec<u64>> {
    let (input, res) = context(
        "array",
        preceded(
            char('['),
            preceded(
                multispace0,
                cut(terminated(
                    separated_list0(char(','), preceded(multispace0, digit1)),
                    preceded(multispace0, char(']')),
                )),
            ),
        ),
    )(input)?;

    let r = res
        .iter()
        .map(|s| s.parse::<u64>().unwrap())
        .collect::<Vec<_>>();

    Ok((input, r))
}
