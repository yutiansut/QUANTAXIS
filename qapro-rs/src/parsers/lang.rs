use std::str::FromStr;

use parse_display::{Display, FromStr};




use polars::prelude::*;

use crate::parsers::value::{BPqlValue, PqlValue, TomlValue};

#[derive(Display, FromStr, PartialEq, Clone, Debug)]
#[display(style = "snake_case")]
pub enum LangType {
    Json,
    Yaml,
    Toml,
    Xml,
    // Csv,
}

impl Default for LangType {
    fn default() -> Self {
        Self::Json
    }
}

#[derive(Debug, Default, Clone, PartialEq)]
pub struct Lang {
    pub data: PqlValue,
    pub text: String,
    pub from: LangType,
    pub to: LangType,
    pub colnames: Vec<String>,
}

impl FromStr for Lang {
    type Err = anyhow::Error;

    fn from_str(input: &str) -> anyhow::Result<Self> {
        if let Ok(this) = Self::from_as_json(input) {
            Ok(this)
        } else if let Ok(this) = Self::from_as_toml(input) {
            Ok(this)
        } else if let Ok(this) = Self::from_as_xml(input) {
            Ok(this)
        } else if let Ok(this) = Self::from_as_xml(input) {
            Ok(this)
        } else {
            anyhow::bail!("not supported")
        }
    }
}

impl Lang {
    pub fn from_as(input: &str, lnag_type: LangType) -> anyhow::Result<Self> {
        match lnag_type {

            // LangType::Csv => Self::from_as_csv(input),
            LangType::Json => Self::from_as_json(input),
            LangType::Toml => Self::from_as_toml(input),
            LangType::Yaml => Self::from_as_yaml(input),
            LangType::Xml => Self::from_as_xml(input),
        }
    }

    
    // pub fn from_as_csv(input: &str) -> anyhow::Result<Self> {
    //     if let Ok(data) = csvstr_to_pqlv(input) {
    //         Ok(Self {
    //             data,
    //             text: input.to_string(),
    //             from: LangType::Csv,
    //             to: LangType::Csv,
    //             colnames: Vec::default(),
    //         })
    //     } else {
    //         anyhow::bail!("fail to parse input as csv");
    //     }
    // }

    pub fn from_as_json(input: &str) -> anyhow::Result<Self> {
        if let Ok(data) = serde_json::from_str::<serde_json::value::Value>(input) {
            // Json does not distinguish between Float and Int. For this reason, it it parsed once with serde_json::value::Value, not crate::value::PqlValue.
            Ok(Self {
                data: crate::parsers::value::json_value::to_pqlvalue(data),
                text: input.to_string(),
                from: LangType::Json,
                to: LangType::Json,
                colnames: Vec::default(),
            })
        } else {
            anyhow::bail!("fail to parse input as json");
        }
    }

    pub fn from_as_toml(input: &str) -> anyhow::Result<Self> {
        if let Ok(data) = toml::from_str::<PqlValue>(input) {
            Ok(Self {
                data,
                text: input.to_string(),
                from: LangType::Toml,
                to: LangType::Toml,
                colnames: Vec::default(),
            })
        } else {
            anyhow::bail!("fail to parse input as toml");
        }
    }

    pub fn from_as_xml(input: &str) -> anyhow::Result<Self> {
        if let Ok(data) = quick_xml::de::from_str::<PqlValue>(input) {
            Ok(Self {
                data,
                text: input.to_string(),
                from: LangType::Xml,
                to: LangType::Xml,
                colnames: Vec::default(),
            })
        } else {
            anyhow::bail!("fail to parse input as xml");
        }
    }

    pub fn from_as_yaml(input: &str) -> anyhow::Result<Self> {
        if let Ok(data) = serde_yaml::from_str::<PqlValue>(input) {
            Ok(Self {
                data,
                text: input.to_string(),
                from: LangType::Yaml,
                to: LangType::Yaml,
                colnames: Vec::default(),
            })
        } else {
            anyhow::bail!("fail to parse input as yaml");
        }
    }

    pub fn sort_keys(&mut self) {
        let json = serde_json::to_string(&self.data).unwrap();
        let bdata = serde_json::from_str::<BPqlValue>(&json).unwrap();
        let bjson = serde_json::to_string(&bdata).unwrap();
        let data = serde_json::from_str::<PqlValue>(&bjson).unwrap();
        self.data = data;
    }

    pub fn to_string(&self, compact: bool) -> anyhow::Result<String> {
        let output = match (&self.to, &self.from == &self.to) {

            // (LangType::Csv, _) => {
            //     // To pad missing values with null, serialize them to json, deserialize them with polars, and write them to csv from there.
            //     let sss = match &self.data {
            //         PqlValue::Array(array) => array
            //             .iter()
            //             .map(|v| serde_json::to_string(&v).unwrap())
            //             .collect::<Vec<String>>()
            //             .join("\n"),
            //         _ => anyhow::bail!("must array"),
            //     };
            //     let c = std::io::Cursor::new(&sss);
            //     let mut df = CsvReader::new(c).infer_schema(Some(100)).finish()?;
            //
            //     let mut v = Vec::new();
            //     CsvWriter::new(&mut v)
            //         .has_header(true)
            //         .with_delimiter(b',')
            //         .finish(&mut df)?;
            //     let s = String::from_utf8(v)?;
            //     s
            // }
            (LangType::Json, _) if compact => serde_json::to_string(&self.data).unwrap(),
            (LangType::Json, _) => serde_json::to_string_pretty(&self.data).unwrap(),
            (_, true) => self.text.to_owned(),
            (LangType::Toml, _) => {
                let v = TomlValue::from(self.data.to_owned());
                toml::to_string_pretty(&v).unwrap()
            }
            (LangType::Yaml, _) => serde_yaml::to_string(&self.data)
                .unwrap()
                .trim_start_matches("---\n")
                .to_string(),
            (LangType::Xml, _) => quick_xml::se::to_string(&self.data).unwrap(),
        };

        Ok(output)
    }


    pub fn print(&self, compact: bool) -> anyhow::Result<()> {
        let output = self.to_string(compact)?;

        if atty::is(atty::Stream::Stdout) {
            let bytes = output.as_bytes().to_vec();
            let lang_type = self.to.to_string();

            // PrettyPrinter::new()
            //     .language(&lang_type)
            //     .input(bat::Input::from_bytes(&bytes))
            //     .print()
            //     .unwrap();
        } else {
            println!("{}", &output);
        }
        Ok(())
    }
}


// fn csvstr_to_pqlv(input: &str) -> anyhow::Result<PqlValue> {
//     let c = std::io::Cursor::new(input.to_owned());
//     let df = CsvReader::new(c).infer_schema(Some(100)).finish()?;
//     Ok(PqlValue::from(df))
// }
