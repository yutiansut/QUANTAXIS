## QAPRO-RS QUANTAXIS & Rust

[如果需要 simd 的加速支持, 请使用 nightly 版本的 rust]
> cargo +nightly run --color=always --package qapro-rs  --release example.toml

具体内容可以参见http://www.quantaxis.tech:3000/topic/61c33e858481913fcb6113d5

使用方式:

首先拉起4个api服务 

- clickhouse
- redis
- mongodb
- rabbitmq

如果你本地没有这几个服务 可以使用docker-compose 拉起

> docker-compose -f database.yaml up -d

如果你有部分的服务, 可以修改并删除database.yaml里的代码块


编译方式: [支持windows/ mac/ linux]

cargo build --release


运行方式

cargo run --release example.toml

cargo run --example api --release example.toml [开启的服务在example.toml中配置 默认5000端口]




@yutiansut

2021-12-22