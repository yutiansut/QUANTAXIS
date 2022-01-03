use std::ops::{Add, Div, Mul, Neg, Rem, Sub};

use rayon::prelude::*;

use crate::parsers::value::PqlValue;

#[derive(Debug, Default, Clone, PartialEq)]
pub struct PqlVector(pub Vec<PqlValue>);

impl From<PqlVector> for PqlValue {
    fn from(v: PqlVector) -> Self {
        Self::Array(v.0)
    }
}

impl Neg for PqlVector {
    type Output = Self;
    fn neg(self) -> Self::Output {
        let v = self.0.into_iter().map(|value| -value).collect::<Vec<_>>();
        Self(v)
    }
}

impl Add for PqlVector {
    type Output = Self;
    fn add(self, other: Self) -> Self::Output {
        let v = self
            .0
            .into_iter()
            .zip(other.0.into_iter())
            .map(|(a, b)| a + b)
            .collect::<Vec<PqlValue>>();
        Self(v)
    }
}

impl Sub for PqlVector {
    type Output = Self;
    fn sub(self, other: Self) -> Self::Output {
        let v = self
            .0
            .into_iter()
            .zip(other.0.into_iter())
            .map(|(a, b)| a - b)
            .collect::<Vec<PqlValue>>();
        Self(v)
    }
}

impl Mul for PqlVector {
    type Output = Self;
    fn mul(self, other: Self) -> Self::Output {
        let v = self
            .0
            .into_iter()
            .zip(other.0.into_iter())
            .map(|(a, b)| a * b)
            .collect::<Vec<PqlValue>>();
        Self(v)
    }
}

impl Div for PqlVector {
    type Output = Self;
    fn div(self, other: Self) -> Self::Output {
        let v = self
            .0
            .into_iter()
            .zip(other.0.into_iter())
            .map(|(a, b)| a / b)
            .collect::<Vec<PqlValue>>();
        Self(v)
    }
}

impl Rem for PqlVector {
    type Output = Self;
    fn rem(self, other: Self) -> Self::Output {
        let v = self
            .0
            .into_iter()
            .zip(other.0.into_iter())
            .map(|(a, b)| a % b)
            .collect::<Vec<PqlValue>>();
        Self(v)
    }
}
