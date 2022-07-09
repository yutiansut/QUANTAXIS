use crate::qaaccount::account::QA_Account;
use crate::qaaccount::order::QAOrder;
use crate::qaconnector::mongo::mongoclient::QAMongoClient;
use crate::qaenv::localenv::CONFIG;
use async_trait::async_trait;
use std::collections::HashMap;
pub struct QAOMS {
    pub accountmap: HashMap<String, QA_Account>,
    pub account_db: QAMongoClient,
    pub ordermap: HashMap<String, QAOrder>,
}

trait OrderCheck {
    fn add_main_account(&self, account_cookie: &str);
    fn add_sub_account(&self, sub_account_cookie: &str);
}
#[async_trait]
trait Reload {
    async fn init() -> Self;
    async fn reload_account(&mut self, account: &str) {}
}

impl OrderCheck for QAOMS {
    fn add_main_account(&self, account_cookie: &str) {
        todo!()
    }

    fn add_sub_account(&self, account_cookie: &str) {
        todo!()
    }
}
#[async_trait]
impl Reload for QAOMS {
    async fn init() -> Self {
        Self {
            accountmap: HashMap::new(),
            account_db: QAMongoClient::new(&*CONFIG.account.uri).await,
            ordermap: Default::default(),
        }
    }
    async fn reload_account(&mut self, account_cookie: &str) {
        let account = self
            .account_db
            .get_account(account_cookie.parse().unwrap())
            .await;
        self.accountmap.insert(account_cookie.to_string(), account);
    }
}
