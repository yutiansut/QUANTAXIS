#[macro_export]
macro_rules! launchstrategy{
    ($name:expr;$code:expr;$json:expr;$ctx:expr;$morm_addr:expr;$mqm_addr:expr;$mdata:expr; $rdata:expr; $($m: ident),*) => {
        match $name {
            $(

                stringify!($m) => {
                    // 初始化策略和上下文
                    println!("{:#?}",$code);
                    let params = match $json{
                        Some(x) => match serde_json::from_value(x.clone()) {
                            Ok(p) => p,
                            Err(_) => $m::Params::default(),
                        },
                        None => $m::Params::default(),
                    };
                    let p = serde_json::to_string(&params).unwrap();
                    let t = $m::QAStrategy::new(params);
                    // 创建监视器
                    let mut mor = Monitor::new($ctx, t, $morm_addr);

                    mor.backtest($mdata, $rdata);
                    let addr = mor.start();
                    $mqm_addr.do_send(MarketSubscribe {
                        key: $code.to_string(),
                        rec: addr.recipient().clone(),
                    });
                }
            )*
            _ => {}
        }
    }
}

#[macro_export]
macro_rules! mapjobs{
    ($name:expr;$code:expr; $($m: ident),*) => {
         match $name {
             $(
                stringify!($m) => {

                    println!("{}", $code);

                })*
            _ => {}
         }
     }
}
