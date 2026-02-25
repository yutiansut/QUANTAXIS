// QUANTAXIS 2.1.0 MongoDB 初始化脚本
// 创建数据库和用户,设置权限
//
// 作者: @yutiansut @quantaxis
// 版本: 2.1.0-alpha2

// 切换到admin数据库
db = db.getSiblingDB('admin');

// 创建QUANTAXIS用户
db.createUser({
  user: 'quantaxis',
  pwd: process.env.MONGO_PASSWORD || 'quantaxis',
  roles: [
    {
      role: 'readWrite',
      db: 'quantaxis'
    },
    {
      role: 'dbAdmin',
      db: 'quantaxis'
    }
  ]
});

// 切换到quantaxis数据库
db = db.getSiblingDB('quantaxis');

// 创建集合和索引
print('创建stock_day集合和索引...');
db.createCollection('stock_day');
db.stock_day.createIndex({ code: 1, date: 1 }, { unique: true });
db.stock_day.createIndex({ date: 1 });

print('创建stock_min集合和索引...');
db.createCollection('stock_min');
db.stock_min.createIndex({ code: 1, datetime: 1 }, { unique: true });
db.stock_min.createIndex({ datetime: 1 });

print('创建future_day集合和索引...');
db.createCollection('future_day');
db.future_day.createIndex({ code: 1, date: 1 }, { unique: true });
db.future_day.createIndex({ date: 1 });

print('创建future_min集合和索引...');
db.createCollection('future_min');
db.future_min.createIndex({ code: 1, datetime: 1 }, { unique: true });
db.future_min.createIndex({ datetime: 1 });

print('创建stock_list集合和索引...');
db.createCollection('stock_list');
db.stock_list.createIndex({ code: 1 }, { unique: true });

print('创建future_list集合和索引...');
db.createCollection('future_list');
db.future_list.createIndex({ code: 1 }, { unique: true });

// QIFI账户相关集合
print('创建account集合和索引...');
db.createCollection('account');
db.account.createIndex({ account_cookie: 1 }, { unique: true });
db.account.createIndex({ portfolio: 1 });
db.account.createIndex({ user_id: 1 });

print('创建order集合和索引...');
db.createCollection('order');
db.order.createIndex({ order_id: 1 }, { unique: true });
db.order.createIndex({ account_cookie: 1 });
db.order.createIndex({ datetime: 1 });

print('创建position集合和索引...');
db.createCollection('position');
db.position.createIndex({ account_cookie: 1, code: 1 }, { unique: true });

print('创建trade集合和索引...');
db.createCollection('trade');
db.trade.createIndex({ trade_id: 1 }, { unique: true });
db.trade.createIndex({ account_cookie: 1 });
db.trade.createIndex({ datetime: 1 });

// 资源管理器配置集合
print('创建resource_config集合...');
db.createCollection('resource_config');
db.resource_config.createIndex({ resource_type: 1, resource_name: 1 }, { unique: true });

// 系统日志集合
print('创建system_log集合和索引...');
db.createCollection('system_log', { capped: true, size: 104857600, max: 100000 });
db.system_log.createIndex({ timestamp: 1 });
db.system_log.createIndex({ level: 1 });

print('MongoDB初始化完成!');
