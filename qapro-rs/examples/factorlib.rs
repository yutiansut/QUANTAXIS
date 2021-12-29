use qapro_rs::qaconnector::clickhouse::ckclient;
use qapro_rs::qaconnector::clickhouse::ckclient::DataConnector;

#[actix_rt::main]
async fn main() {
    let c = ckclient::QACKClient::init();

    let codelist = ["600010.XSHG", "300002.XSHE"];
    let hisdata = c
        .get_stock(Vec::from(codelist), "2021-07-11", "2021-12-22", "1min")
        .await
        .unwrap();
    println!("{:#?}", hisdata.to_kline());
}
