use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub struct Atom {
    data: u64,
}

impl From<u64> for Atom {
    fn from(v: u64) -> Self {
        Self { data: v }
    }
}

impl fmt::Display for Atom {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        writeln!(f, "{{");
        writeln!(f, "  '_1': {},", self.data);
        writeln!(f, "}}");
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Array {
    data: Vec<Atom>,
}

impl From<&[u64]> for Array {
    fn from(v: &[u64]) -> Self {
        Self {
            data: v.to_vec().into_iter().map(Atom::from).collect::<Vec<_>>(),
        }
    }
}

impl fmt::Display for Array {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        writeln!(f, "<<");
        for atom in self.data.iter() {
            writeln!(f, "  {},", atom);
        }
        writeln!(f, ">>")?;
        Ok(())
    }
}
