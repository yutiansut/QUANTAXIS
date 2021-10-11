
create database qifi;

create table IF NOT EXISTS qifi.accounts
(
    user_id           String,
    currency          String,
    qifi_id           String,
    pre_balance       Float64,
    deposit           Float64,
    withdraw          Float64,
    WithdrawQuota     Float64,
    close_profit      Float64,
    commission        Float64,
    premium           Float64,
    static_balance    Float64,
    position_profit   Float64,
    float_profit      Float64,
    balance           Float64,
    margin            Float64,
    frozen_margin     Float64,
    frozen_commission Float64,
    frozen_premium    Float64,
    available         Float64,
    risk_ratio        Float64
)
engine = ReplacingMergeTree
ORDER BY qifi_id
SETTINGS index_granularity = 8192;



create table IF NOT EXISTS qifi.banks
(

    id     String,
    qifi_id          String,
    name         String,
    bank_account String,
    fetch_amount Float64,
    qry_count    Int64
)
    engine = ReplacingMergeTree
        ORDER BY qifi_id
        SETTINGS index_granularity = 8192;


create table IF NOT EXISTS qifi.qifi
(
    account_cookie   String,
    bank_password   String,
    qifi_id          String,
    bankid           String,
    bankname         String,
    broker_name      String,
    capital_password String,
    eventmq_ip       String,
    investor_name    String,
    money            Float64,
    password         String,
    ping_gap         Int32,
    portfolio        String,
    pub_host         String,
    taskid           String,
    trade_host       String,
    updatetime       String,
    wsuri            String,
    trading_day      String,
    status           Int32,
    databaseip       String
)
    engine = ReplacingMergeTree ORDER BY (account_cookie, trading_day)
        SETTINGS index_granularity = 8192;


create table IF NOT EXISTS qifi.orders
(
    qifi_id          String,
    seqno             Int32,
    account_cookie    String,
    user_id           String,
    order_id          String,
    price            Float32,
    volume            Int32,
    towards           Int32,
    exchange_id       String,
    instrument_id     String,
    direction         String,
    offset            String,
    volume_orign      Float64,
    price_type        String,
    limit_price       Float64,
    time_condition    String,
    volume_condition  String,
    insert_date_time  Int64,
    order_time        String,
    exchange_order_id String,
    status            String,
    volume_left       Float64,
    last_msg          String
)
    engine = ReplacingMergeTree ORDER BY qifi_id
        SETTINGS index_granularity = 8192;
create table IF NOT EXISTS qifi.positions
(
    code                      String,
    qifi_id                   String,
    user_id                   String,
    portfolio_cookie          String,
    account_cookie   String,
    username   String,
    exchange_id               String,
    instrument_id             String,
    position_id String,
    market_type String,
    volume_long_today         Float64,
    volume_long_his           Float64,
    volume_long               Float64,
    volume_long_frozen_today  Float64,
    volume_long_frozen_his    Float64,
    volume_long_frozen        Float64,
    volume_short_today        Float64,
    volume_short              Float64,
    volume_short_frozen_today Float64,
    volume_short_frozen_his   Float64,
    volume_short_frozen       Float64,
    volume_long_yd            Float64,
    volume_short_yd           Float64,
    pos_long_his              Float64,
    pos_long_today            Float64,
    pos_short_his             Float64,
    pos_short_today           Float64,
    open_price_long           Float64,
    open_price_short          Float64,
    open_cost_short           Float64,
    open_cost_long            Float64,
    position_price_long       Float64,
    position_price_short      Float64,
    position_cost_long        Float64,
    position_cost_short       Float64,
    last_price                Float64,
    float_profit_long         Float64,
    float_profit_short        Float64,
    float_profit              Float64,
    position_profit_long      Float64,
    position_profit_short     Float64,
    position_profit           Float64,
    margin_long               Float64,
    margin_short              Float64,
    margin                    Float64
)
    engine = ReplacingMergeTree ORDER BY qifi_id
        SETTINGS index_granularity = 8192;


create table IF NOT EXISTS qifi.trades
(
    seqno             Int32,
    qifi_id           String,
    user_id           String,
    trade_id          String,
    exchange_id       String,
    instrument_id     String,
    order_id          String,
    exchange_trade_id String,
    direction         String,
    offset            String,
    volume            Float64,
    price             Float64,
    trade_date_time   Int64,
    commission        Float64
)
    engine = ReplacingMergeTree
        ORDER BY qifi_id
        SETTINGS index_granularity = 8192;
