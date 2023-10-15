use crate::qaprotocol::mifi::market::BAR;
use crate::qaprotocol::mifi::qafastkline::QAKlineBase;
use crate::qaprotocol::qifi::account::QIFI;
use chrono::format::ParseError;
use chrono::{DateTime, FixedOffset, NaiveDate, NaiveDateTime, NaiveTime, TimeZone, Utc};
use serde::Serialize;

#[derive(Debug, Clone)]
pub struct QARealtimeResampler {
    bardata: QAKlineBase,
    pub frequence: String,
    pub frq: i64,
    pub last: QAKlineBase,
}

impl QARealtimeResampler {
    pub fn new(freq: i64) -> Self {
        Self {
            bardata: QAKlineBase::init(),
            frequence: format!("{}min", &freq),
            frq: freq * 60,
            last: QAKlineBase::init(),
        }
    }

    pub fn next(&mut self, bar: BAR) -> QAKlineBase {
        let cur_datetime: String = bar.datetime.clone();
        let curstamp = Utc
            .datetime_from_str(cur_datetime.as_ref(), "%Y-%m-%d %H:%M:%S")
            .unwrap()
            .timestamp();

        if self.bardata.startstamp == 0 {
            self.bardata = QAKlineBase::new_from_bar(
                bar.clone(),
                self.frequence.parse().unwrap(),
                cur_datetime.clone(),
                curstamp.clone(),
            );
        }

        let min_f = cur_datetime[14..16].parse::<i32>().unwrap();
        if self.bardata.startstamp + self.frq <= curstamp {
            let realstart: i64;
            let openstamp: i64;
            let dthour: i32 = cur_datetime[11..13].parse::<i32>().unwrap();
            // println!("dthour {:#?} / curdt {:#?}", dthour, cur_datetime);
            if dthour > 8 && dthour < 12 {
                // day
                if bar.code.starts_with("IF")
                    || bar.code.starts_with("IC")
                    || bar.code.starts_with("IH")
                    || bar.code.starts_with("TF")
                {
                    // starts with 9:00
                    let x = &cur_datetime[0..10];
                    openstamp = Utc
                        .datetime_from_str(format!("{} 09:30:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                        .unwrap()
                        .timestamp();

                    realstart = openstamp + ((curstamp - openstamp) / self.frq) * self.frq;
                } else {
                    let x = &cur_datetime[0..10];
                    openstamp = Utc
                        .datetime_from_str(format!("{} 09:00:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                        .unwrap()
                        .timestamp();
                    realstart = openstamp + ((curstamp - openstamp) / self.frq) * self.frq;
                }
            } else if dthour > 12 && dthour < 16 {
                // afternoon
                if bar.code.starts_with("IF")
                    || bar.code.starts_with("IC")
                    || bar.code.starts_with("IH")
                    || bar.code.starts_with("TF")
                {
                    // starts with 9:00

                    let x = &cur_datetime[0..10];
                    openstamp = Utc
                        .datetime_from_str(format!("{} 13:00:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                        .unwrap()
                        .timestamp();
                    realstart = openstamp + ((curstamp - openstamp) / self.frq) * self.frq;
                } else {
                    let x = &cur_datetime[0..10];
                    openstamp = Utc
                        .datetime_from_str(format!("{} 13:30:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                        .unwrap()
                        .timestamp();
                    realstart = openstamp + ((curstamp - openstamp) / self.frq) * self.frq;
                }
            } else if dthour < 9 {
                // night
                openstamp = Utc
                    .datetime_from_str("1970-01-01 21:00:00", "%Y-%m-%d %H:%M:%S")
                    .unwrap()
                    .timestamp();
                let x = &cur_datetime[10..19];
                let fake_stamp = Utc
                    .datetime_from_str(format!("1970-01-02 {}", x).as_str(), "%Y-%m-%d %H:%M:%S")
                    .unwrap()
                    .timestamp();
                realstart = curstamp - fake_stamp
                    + openstamp
                    + ((fake_stamp - openstamp) / self.frq) * self.frq;
            } else {
                // night
                let x = &cur_datetime[0..10];
                openstamp = Utc
                    .datetime_from_str(format!("{} 21:00:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                    .unwrap()
                    .timestamp();

                realstart = openstamp + ((curstamp - openstamp) / self.frq) * self.frq;
            }
            // println!("bar {:#?}", bar.datetime);
            let real_starttime = Utc.timestamp(realstart, 0).to_string();
            // println!("calc real {:#?}", real_starttime);
            self.bardata.is_last = true;
            self.last = self.bardata.clone();
            self.bardata = QAKlineBase::new_from_bar(
                bar.clone(),
                self.frequence.parse().unwrap(),
                real_starttime[0..19].to_string(),
                realstart,
            );
        } else {
            self.last = self.bardata.clone();
            self.bardata.update_from_bar(bar.clone());
        }
        self.last.clone()
    }
}

pub fn resample(code: String, raw_freq: i64, freq: i64, filepath: String) -> Vec<QAKlineBase> {
    //let filepath = "G:\\onedrive\\data\\TBDATA\\".to_string();
    let filepath = format!("{}TB_DATA_{}_{}MIN.csv", &filepath, &code, &raw_freq);
    println!("{:#?}", filepath);
    let mut rdr = csv::Reader::from_path(&filepath).unwrap();

    let mut bardata: QAKlineBase = QAKlineBase::init();
    let frequence: String = format!("{}min", &freq);
    let frq: i64 = freq * 60;
    let mut ures = vec![];
    for result in rdr.deserialize() {
        let bar: BAR = result.unwrap();
        let cur_datetime: String = bar.datetime.clone();
        let curstamp = Utc
            .datetime_from_str(cur_datetime.as_ref(), "%Y-%m-%d %H:%M:%S")
            .unwrap()
            .timestamp();

        if bardata.startstamp == 0 {
            bardata = QAKlineBase::new_from_bar(
                bar.clone(),
                frequence.parse().unwrap(),
                cur_datetime.clone(),
                curstamp.clone(),
            );
        }

        let min_f = cur_datetime[14..16].parse::<i32>().unwrap();
        if bardata.startstamp + frq <= curstamp {
            let realstart: i64;
            let openstamp: i64;
            let dthour: i32 = cur_datetime[11..13].parse::<i32>().unwrap();
            // println!("dthour {:#?} / curdt {:#?}", dthour, cur_datetime);
            if dthour > 8 && dthour < 12 {
                // day
                if bar.code.starts_with("IF")
                    || bar.code.starts_with("IC")
                    || bar.code.starts_with("IH")
                    || bar.code.starts_with("TF")
                {
                    // starts with 9:00
                    let x = &cur_datetime[0..10];
                    openstamp = Utc
                        .datetime_from_str(format!("{} 09:30:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                        .unwrap()
                        .timestamp();

                    realstart = openstamp + ((curstamp - openstamp) / frq) * frq;
                } else {
                    let x = &cur_datetime[0..10];
                    openstamp = Utc
                        .datetime_from_str(format!("{} 09:00:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                        .unwrap()
                        .timestamp();
                    realstart = openstamp + ((curstamp - openstamp) / frq) * frq;
                }
            } else if dthour > 12 && dthour < 16 {
                // afternoon
                if bar.code.starts_with("IF")
                    || bar.code.starts_with("IC")
                    || bar.code.starts_with("IH")
                    || bar.code.starts_with("TF")
                {
                    // starts with 9:00

                    let x = &cur_datetime[0..10];
                    openstamp = Utc
                        .datetime_from_str(format!("{} 13:00:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                        .unwrap()
                        .timestamp();
                    realstart = openstamp + ((curstamp - openstamp) / frq) * frq;
                } else {
                    let x = &cur_datetime[0..10];
                    openstamp = Utc
                        .datetime_from_str(format!("{} 13:30:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                        .unwrap()
                        .timestamp();
                    realstart = openstamp + ((curstamp - openstamp) / frq) * frq;
                }
            } else if dthour < 9 {
                // night
                openstamp = Utc
                    .datetime_from_str("1970-01-01 21:00:00", "%Y-%m-%d %H:%M:%S")
                    .unwrap()
                    .timestamp();
                let x = &cur_datetime[10..19];
                let fake_stamp = Utc
                    .datetime_from_str(format!("1970-01-02 {}", x).as_str(), "%Y-%m-%d %H:%M:%S")
                    .unwrap()
                    .timestamp();
                realstart =
                    curstamp - fake_stamp + openstamp + ((fake_stamp - openstamp) / frq) * frq;
            } else {
                // night
                let x = &cur_datetime[0..10];
                openstamp = Utc
                    .datetime_from_str(format!("{} 21:00:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                    .unwrap()
                    .timestamp();

                realstart = openstamp + ((curstamp - openstamp) / frq) * frq;
            }
            // println!("bar {:#?}", bar.datetime);
            let real_starttime = Utc.timestamp(realstart, 0).to_string();
            // println!("calc real {:#?}", real_starttime);
            bardata.is_last = true;
            ures.push(bardata.clone());
            bardata = QAKlineBase::new_from_bar(
                bar.clone(),
                frequence.parse().unwrap(),
                real_starttime[0..19].to_string(),
                realstart,
            );
        } else {
            ures.push(bardata.clone());
            bardata.update_from_bar(bar.clone());
        }
    }
    bardata.is_last = true;
    ures.push(bardata.clone());
    ures
}

pub fn resample_db(hisdata: Vec<BAR>, freq: i64) -> Vec<QAKlineBase> {
    let mut bardata: QAKlineBase = QAKlineBase::init();
    let frequence: String = format!("{}min", &freq);
    let frq: i64 = freq * 60;
    let mut ures = vec![];
    for bar in hisdata {
        let cur_datetime: String = bar.datetime.clone();
        let curstamp = Utc
            .datetime_from_str(cur_datetime.as_ref(), "%Y-%m-%d %H:%M:%S")
            .unwrap()
            .timestamp();

        if bardata.startstamp == 0 {
            bardata = QAKlineBase::new_from_bar(
                bar.clone(),
                frequence.parse().unwrap(),
                cur_datetime.clone(),
                curstamp.clone(),
            );
        }

        let min_f = cur_datetime[14..16].parse::<i32>().unwrap();
        if bardata.startstamp + frq <= curstamp {
            let realstart: i64;
            let openstamp: i64;
            let dthour: i32 = cur_datetime[11..13].parse::<i32>().unwrap();
            // println!("dthour {:#?} / curdt {:#?}", dthour, cur_datetime);
            if dthour > 8 && dthour < 12 {
                // day
                if bar.code.starts_with("IF")
                    || bar.code.starts_with("IC")
                    || bar.code.starts_with("IH")
                    || bar.code.starts_with("TF")
                {
                    // starts with 9:00
                    let x = &cur_datetime[0..10];
                    openstamp = Utc
                        .datetime_from_str(format!("{} 09:30:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                        .unwrap()
                        .timestamp();

                    realstart = openstamp + ((curstamp - openstamp) / frq) * frq;
                } else {
                    let x = &cur_datetime[0..10];
                    openstamp = Utc
                        .datetime_from_str(format!("{} 09:00:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                        .unwrap()
                        .timestamp();
                    realstart = openstamp + ((curstamp - openstamp) / frq) * frq;
                }
            } else if dthour > 12 && dthour < 16 {
                // afternoon
                if bar.code.starts_with("IF")
                    || bar.code.starts_with("IC")
                    || bar.code.starts_with("IH")
                    || bar.code.starts_with("TF")
                {
                    // starts with 9:00

                    let x = &cur_datetime[0..10];
                    openstamp = Utc
                        .datetime_from_str(format!("{} 13:00:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                        .unwrap()
                        .timestamp();
                    realstart = openstamp + ((curstamp - openstamp) / frq) * frq;
                } else {
                    let x = &cur_datetime[0..10];
                    openstamp = Utc
                        .datetime_from_str(format!("{} 13:30:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                        .unwrap()
                        .timestamp();
                    realstart = openstamp + ((curstamp - openstamp) / frq) * frq;
                }
            } else if dthour < 9 {
                // night
                openstamp = Utc
                    .datetime_from_str("1970-01-01 21:00:00", "%Y-%m-%d %H:%M:%S")
                    .unwrap()
                    .timestamp();
                let x = &cur_datetime[10..19];
                let fake_stamp = Utc
                    .datetime_from_str(format!("1970-01-02 {}", x).as_str(), "%Y-%m-%d %H:%M:%S")
                    .unwrap()
                    .timestamp();
                realstart =
                    curstamp - fake_stamp + openstamp + ((fake_stamp - openstamp) / frq) * frq;
            } else {
                // night
                let x = &cur_datetime[0..10];
                openstamp = Utc
                    .datetime_from_str(format!("{} 21:00:00", x).as_str(), "%Y-%m-%d %H:%M:%S")
                    .unwrap()
                    .timestamp();

                realstart = openstamp + ((curstamp - openstamp) / frq) * frq;
            }
            // println!("bar {:#?}", bar.datetime);
            let real_starttime = Utc.timestamp(realstart, 0).to_string();
            // println!("calc real {:#?}", real_starttime);
            bardata.is_last = true;
            ures.push(bardata.clone());
            bardata = QAKlineBase::new_from_bar(
                bar.clone(),
                frequence.parse().unwrap(),
                real_starttime[0..19].to_string(),
                realstart,
            );
        } else {
            ures.push(bardata.clone());
            bardata.update_from_bar(bar.clone());
        }
    }
    if ures.is_empty() {
        ures
    } else {
        bardata.is_last = true;
        ures.push(bardata.clone());
        ures
    }
}
