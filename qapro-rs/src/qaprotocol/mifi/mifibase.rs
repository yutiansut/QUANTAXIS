use serde::{Deserialize, Serialize};

pub trait Handler {
    fn to_json(&self) -> String
    where
        Self: Serialize,
    {
        serde_json::to_string(&self).unwrap()
    }
    fn get_datetime(&self) -> String;
    fn get_code(&self) -> String;
    fn get_date(&self) -> String;
    fn get_open(&self) -> f64;
    fn get_close(&self) -> f64;
    fn get_high(&self) -> f64;
    fn get_low(&self) -> f64;
    fn get_vol(&self) -> f64;
    fn get_amount(&self) -> f64;

    fn set_datetime(&mut self, datetime: String) {}
    fn set_code(&mut self, code: String) {}
    fn set_date(&mut self, date: String) {}
    fn set_open(&mut self, open: f64) {}
    fn set_close(&mut self, close: f64) {}
    fn set_high(&mut self, high: f64) {}
    fn set_low(&mut self, low: f64) {}
    fn set_vol(&mut self, vol: f64) {}
    fn set_amount(&mut self, amount: f64) {}
}
