use crate::parsers::sql::Env;

use crate::parsers::sql::Field;

#[derive(Debug, Default, Clone)]
pub struct Drain(pub Vec<Field>);

impl Drain {
    pub fn execute(self, env: &mut Env) {
        for field in self.0 {
            if let Some(alias) = field.alias {
                env.insert(&alias, &field.expr);
            }
        }
    }
}
