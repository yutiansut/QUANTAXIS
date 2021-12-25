extern crate serde_json;

use serde::Serialize;

#[derive(Serialize)]
pub struct Rsp<T> {
    code: i32,
    data: T,
    msg: String,
}

impl<T: 'static> Rsp<T>
where
    T: Serialize,
{
    pub fn to_string(&self) -> String {
        serde_json::to_string(self).unwrap()
    }

    pub fn ok(data: T, msg: &str) -> Self {
        Self {
            code: 200,
            data,
            msg: msg.to_owned(),
        }
    }

    pub fn fail(data: T, msg: &str) -> Self {
        Self {
            code: 400,
            data,
            msg: msg.to_owned(),
        }
    }

    pub fn error(data: T, msg: &str) -> Self {
        Self {
            code: 500,
            data,
            msg: msg.to_owned(),
        }
    }

    pub fn not_found(data: T, msg: &str) -> Self {
        Self {
            code: 404,
            data,
            msg: msg.to_owned(),
        }
    }
}

#[derive(Serialize)]
pub struct WSRsp<T> {
    data: T,
    topic: String,
    code: i32,
}

impl<T: 'static> WSRsp<T>
where
    T: Serialize,
{
    pub fn ok(data: T, topic: &str) -> Self {
        Self {
            code: 200,
            data,
            topic: topic.to_owned(),
        }
    }

    pub fn fail(data: T, topic: &str) -> Self {
        Self {
            code: 400,
            data,
            topic: topic.to_owned(),
        }
    }

    pub fn error(data: T, topic: &str) -> Self {
        Self {
            code: 500,
            data,
            topic: topic.to_owned(),
        }
    }

    pub fn to_string(&self) -> String {
        serde_json::to_string(self).unwrap()
    }
}
