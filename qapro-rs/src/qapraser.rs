use evalexpr::*;

use serde::{Deserialize, Serialize};

/// Defines a string constant for a single keyword: `kw_def!(SELECT);`
/// expands to `pub const SELECT = "SELECT";`
macro_rules! kw_def {
    ($ident:ident = $string_keyword:expr) => {
        pub const $ident: &'static str = $string_keyword;
    };
    ($ident:ident) => {
        kw_def!($ident = stringify!($ident));
    };
}

macro_rules! define_keywords {
    ($(
        $ident:ident $(= $string_keyword:expr)?
    ),*) => {
        #[derive(Debug, Clone, Copy, PartialEq, PartialOrd, Eq, Ord, Hash)]
        #[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
        #[allow(non_camel_case_types)]
        pub enum Keyword {
            NoKeyword,
            $($ident),*
        }

        pub const ALL_KEYWORDS_INDEX: &[Keyword] = &[
            $(Keyword::$ident),*
        ];

        $(kw_def!($ident $(= $string_keyword)?);)*
        pub const ALL_KEYWORDS: &[&str] = &[
            $($ident),*
        ];
    };
}


define_keywords!(
    SELECT,
    AVG,
    ABS);
#[cfg(test)]
mod test {
    use crate::qapraser;
    use super::*;

    #[test]
    fn test_keywords(){
        println!("{:#?}", qapraser::Keyword::ABS);
    }




    #[test]
    fn test() {
        let context = context_map! {

        "five" => 5,
        "twelve" => 12,
        "f" => Function::new(|argument| {
            if let Ok(int) = argument.as_int() {
                Ok(Value::Int(int / 2))
            } else if let Ok(float) = argument.as_float() {
                Ok(Value::Float(float / 2.0))
            } else {
                Err(EvalexprError::expected_number(argument.clone()))
            }
        }),
        "avg" => Function::new(|argument| {
            let arguments = argument.as_tuple()?;

            if let (Value::Int(a), Value::Int(b)) = (&arguments[0], &arguments[1]) {
                Ok(Value::Int((a + b) / 2))
            } else {
                Ok(Value::Float((arguments[0].as_number()? + arguments[1].as_number()?) / 2.0))
            }
        })
        }
        .unwrap(); // Do proper error handling here

        assert_eq!(
            eval_with_context("five + 8 > f(twelve)", &context),
            Ok(Value::from(true))
        );
        // `eval_with_context` returns a variant of the `Value` enum,
        // while `eval_[type]_with_context` returns the respective type directly.
        // Both can be used interchangeably.
        assert_eq!(
            eval_boolean_with_context("five + 8 > f(twelve)", &context),
            Ok(true)
        );
        assert_eq!(
            eval_with_context("avg(2, 4) == 3", &context),
            Ok(Value::from(true))
        );
    }
}
