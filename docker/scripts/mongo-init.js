// 创建应用数据库用户
db = db.getSiblingDB('tradingagents');

// 创建应用用户（读写权限）
db.createUser({
  user: "app_user",
  pwd: "tradingagents123",
  roles: [
    {
      role: "readWrite",
      db: "tradingagents"
    }
  ]
});

// 创建示例集合和索引
db.users.createIndex({ "email": 1 }, { unique: true });
db.trades.createIndex({ "timestamp": -1 });
db.stocks.createIndex({ "symbol": 1 }, { unique: true });

print("MongoDB initialization completed successfully!");