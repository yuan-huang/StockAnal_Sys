# Trading Agents 数据库服务部署

本目录包含 Trading Agents 项目的数据库服务 Docker 部署配置。

## 目录结构

```
docker/
├── .env                    # 环境变量配置文件
├── docker-compose.yml      # Docker Compose 配置
├── scripts/                # 初始化脚本目录
│   ├── mongo-init.js      # MongoDB 初始化脚本
│   └── postgres-init.sql  # PostgreSQL 初始化脚本
└── README.md              # 本说明文档
```

## 服务清单

- **MongoDB 4.4**: 文档数据库 (端口: 27017)
- **PostgreSQL 15**: 关系型数据库 (端口: 5432)  
- **Redis**: 缓存服务 (端口: 6379)
- **Mongo Express**: MongoDB 管理界面 (端口: 8082) - 可选
- **pgAdmin**: PostgreSQL 管理界面 (端口: 8083) - 可选
- **Redis Commander**: Redis 管理界面 (端口: 8081)

## 部署步骤

### 1. 环境准备

确保已安装 Docker 和 Docker Compose。

### 2. 配置检查

检查 `.env` 文件中的配置是否符合要求，特别是密码配置。

### 3. 启动服务

**启动基础服务 (MongoDB, PostgreSQL, Redis, Redis Commander):**
```bash
cd docker
docker-compose up -d
```

**启动所有服务 (包括管理界面):**
```bash
cd docker  
docker-compose --profile management up -d
```

**检查服务状态:**
```bash
docker-compose ps
docker-compose logs [service_name]
```

### 4. 服务访问

| 服务 | 地址 | 用户名 | 密码 |
|------|------|--------|------|
| MongoDB | localhost:27017 | admin | tradingagents123 |
| PostgreSQL | localhost:5432 | admin | tradingagents123 |
| Redis | localhost:6379 | - | tradingagents123 |
| Redis Commander | http://localhost:8081 | - | - |
| Mongo Express | http://localhost:8082 | admin | tradingagents123 |
| pgAdmin | http://localhost:8083 | admin@tradingagents.com | tradingagents123 |

### 5. 数据持久化

所有数据库数据都会持久化到 Docker 卷中：
- `mongodb_data`: MongoDB 数据
- `postgresql_data`: PostgreSQL 数据  
- `redis_data`: Redis 数据
- `pgadmin_data`: pgAdmin 配置

## 常用命令

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷 (注意：会丢失所有数据)
docker-compose down -v

# 查看日志
docker-compose logs -f [service_name]

# 重启特定服务
docker-compose restart [service_name]

# 进入容器
docker-compose exec [service_name] bash

# 备份数据库
docker-compose exec mongodb mongodump --uri="mongodb://admin:tradingagents123@localhost:27017/tradingagents" --out=/data/backup
docker-compose exec postgresql pg_dump -U admin -h localhost tradingagents > backup.sql
```

## 安全说明

- 生产环境请修改 `.env` 文件中的默认密码
- 考虑使用更强的密码策略
- 生产环境建议关闭不必要的管理界面端口
- 定期备份重要数据
