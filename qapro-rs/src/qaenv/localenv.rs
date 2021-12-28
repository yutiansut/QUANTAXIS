use lazy_static::lazy_static;
use log::debug;
use std::path::Path;
use std::{env, fs};

use serde_derive::*;
use toml;

pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Defines and parses CLI argument for this server.
pub fn parse_cli_args<'a>() -> clap::ArgMatches<'a> {
    clap::App::new("qaruntime-rs")
        .version(VERSION)
        .arg(
            clap::Arg::with_name("config")
                .required(false)
                .help("Path to configuration file")
                .index(1),
        )
        .get_matches()
}

/// Parses CLI arguments, finds location of config file, and parses config file into a struct.
pub fn parse_config_from_cli_args(matches: &clap::ArgMatches) -> Config {
    let conf = match matches.value_of("config") {
        Some(config_path) => match Config::from_file(config_path) {
            Ok(config) => config,
            Err(msg) => {
                eprintln!("Failed to parse config file {}: {}", config_path, msg);
                std::process::exit(1);
            }
        },
        None => {
            eprintln!("No config file specified, append toml file");
            std::process::exit(1);
        }
    };
    conf
}

#[derive(Clone, Debug, Default, Deserialize)]
pub struct Config {
    pub clickhouse: ClickhouseConfig,

    pub account: MongoConfig,
    pub hisdata: MongoConfig,
    pub order: MQConfig,
    pub realtime: MQConfig,
    pub redis: RedisConfig,
    pub accsetup: AccountConfig,
    pub cli: Cli,
    pub backtest: Backtest,
    pub instruct: MQConfig,
    pub ack: MQConfig,
    pub common: Common,
    pub DataPath: DataPath,
}

impl Config {
    /// Read configuration from a file into a new Config struct.
    pub fn from_file<P: AsRef<Path>>(path: P) -> Result<Self, String> {
        let path = path.as_ref();
        debug!("Reading configuration from {}", path.display());

        let data = match fs::read_to_string(path) {
            Ok(data) => data,
            Err(err) => return Err(err.to_string()),
        };

        let conf: Config = match toml::from_str(&data) {
            Ok(conf) => conf,
            Err(err) => return Err(err.to_string()),
        };

        Ok(conf)
    }
}

#[derive(Clone, Debug, Deserialize)]
#[serde(default)]
pub struct MongoConfig {
    pub uri: String,
    pub db: String,
}

impl Default for MongoConfig {
    fn default() -> Self {
        Self {
            uri: "mongodb://localhost:27017".to_owned(),
            db: "quantaxis".to_owned(),
        }
    }
}

#[derive(Clone, Debug, Deserialize)]
#[serde(default)]
pub struct MQConfig {
    pub uri: String,
    pub exchange: String,
    pub routing_key: String,
}

impl Default for MQConfig {
    fn default() -> Self {
        Self {
            uri: "amqp://admin:admin@localhost:5672/".to_owned(),
            exchange: "".to_owned(),
            routing_key: "default".to_owned(),
        }
    }
}

#[derive(Clone, Debug, Deserialize)]
#[serde(default)]
pub struct RedisConfig {
    pub uri: String,
}

impl Default for RedisConfig {
    fn default() -> Self {
        Self {
            uri: "redis://localhost:6379/0".to_owned(),
        }
    }
}

#[derive(Clone, Debug, Deserialize)]
#[serde(default)]
pub struct ClickhouseConfig {
    pub uri: String,
}

impl Default for ClickhouseConfig {
    fn default() -> Self {
        Self {
            uri: "tcp://default@192.168.2.126:9000?compression=lz4&ping_timeout=42ms".to_owned(),
        }
    }
}

#[derive(Clone, Debug, Deserialize)]
#[serde(default)]
pub struct Common {
    pub addr: String,
    pub log_level: String,
    pub key: String,
    pub qifi_gap: u64,
}

impl Default for Common {
    fn default() -> Self {
        Self {
            addr: "0.0.0.0:5000".to_string(),
            log_level: "info".to_string(),
            key: "quantaxis".to_string(),
            qifi_gap: 5,
        }
    }
}

#[derive(Clone, Debug, Deserialize)]
#[serde(default)]
pub struct AccountConfig {
    pub cash_map: String,
    pub multiply: f64,
    pub default: f64,
    pub symbol: String,
}

impl Default for AccountConfig {
    fn default() -> Self {
        Self {
            cash_map: "{}".to_owned(),
            multiply: 2.0,
            default: 50000.0,
            symbol: "KTKS".to_owned(),
        }
    }
}

#[derive(Clone, Debug, Deserialize)]
#[serde(default)]
pub struct Cli {
    pub name: Vec<String>,
    pub codes: Vec<String>,
    pub freqs: Vec<String>,
    pub params: String,
    pub log_path: String,
}

impl Default for Cli {
    fn default() -> Self {
        Self {
            name: vec!["t00".to_owned()],
            codes: vec!["rb2010".to_owned()],
            freqs: vec!["1min".to_owned()],
            params: "{\"\":\"\"}".to_owned(),
            log_path: "log/qaruntime.log".to_owned(),
        }
    }
}

#[derive(Clone, Debug, Deserialize)]
#[serde(default)]
pub struct Backtest {
    pub start: String,
    pub end: String,
}

impl Default for Backtest {
    fn default() -> Self {
        Self {
            start: "2020-01-01 09:00:00".to_owned(),
            end: "2021-12-01 09:00:00".to_owned(),
        }
    }
}
#[derive(Clone, Debug, Deserialize)]
#[serde(default)]
pub struct DataPath {
    pub cache: String,
    pub cachestart: String,
    pub cacheend: String,
}

impl Default for DataPath {
    fn default() -> Self {
        Self {
            cache: "/data/".to_owned(),
            cachestart: "".to_string(),
            cacheend: "".to_string(),
        }
    }
}
pub fn new_config() -> Config {
    let _args: Vec<String> = env::args().collect();

    let cfg: Config = parse_config_from_cli_args(&parse_cli_args());
    cfg
}

lazy_static! {
    pub static ref CONFIG: Config = new_config();
}
