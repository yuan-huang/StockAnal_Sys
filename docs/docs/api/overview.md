# API 接口概览

## 概述

本文档提供了系统 API 接口的完整概览，包括接口规范、认证方式、错误处理等核心信息。

## API 基本信息

- **基础 URL**：`https://api.your-project.com`
- **API 版本**：v1
- **数据格式**：JSON
- **字符编码**：UTF-8
- **请求方法**：GET, POST, PUT, DELETE, PATCH

## 接口规范

### 请求格式

#### HTTP 头部
```
Content-Type: application/json
Authorization: Bearer <access_token>
Accept: application/json
User-Agent: YourApp/1.0
```

#### 请求体示例
```json
{
  "name": "示例名称",
  "description": "示例描述",
  "tags": ["标签1", "标签2"]
}
```

### 响应格式

#### 成功响应
```json
{
  "success": true,
  "data": {
    "id": 123,
    "name": "示例名称",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "message": "操作成功"
}
```

#### 错误响应
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "验证失败",
    "details": [
      {
        "field": "name",
        "message": "名称不能为空"
      }
    ]
  }
}
```

## 认证授权

### JWT Token 认证

系统使用 JWT (JSON Web Token) 进行身份认证：

1. **获取 Token**
   ```
   POST /auth/login
   ```

2. **使用 Token**
   ```
   Authorization: Bearer <your_jwt_token>
   ```

3. **刷新 Token**
   ```
   POST /auth/refresh
   ```

### 权限控制

系统采用 RBAC (基于角色的访问控制) 模型：

- **角色**：管理员、普通用户、访客
- **权限**：读取、创建、更新、删除
- **资源**：用户、数据、配置等

## 接口分类

### 1. 认证接口
- `POST /auth/login` - 用户登录

### 2. 大盘分析页接口
- `GET /api/market/indices` - 获取指数行情数据
- `GET /api/market/fund-flow` - 获取资金流数据
- `GET /api/market/sector-fund-flow` - 获取板块资金流数据
- `GET /api/market/sentiment` - 获取市场情绪数据
- `GET /api/market/kline` - 获取K线图数据
- `GET /api/market/technical-indicators` - 获取技术指标数据
- `POST /api/market/export-report` - 导出分析报告
- `WS /api/market/realtime` - 实时数据推送

详细接口文档请参考：[大盘分析页API文档](./market-overview.md)
- `POST /auth/register` - 用户注册
- `POST /auth/logout` - 用户登出
- `POST /auth/refresh` - 刷新令牌
- `POST /auth/forgot-password` - 忘记密码
- `POST /auth/reset-password` - 重置密码

### 2. 用户管理接口
- `GET /users` - 获取用户列表
- `GET /users/{id}` - 获取用户详情
- `POST /users` - 创建用户
- `PUT /users/{id}` - 更新用户
- `DELETE /users/{id}` - 删除用户
- `PUT /users/{id}/profile` - 更新用户资料

### 3. 数据管理接口
- `GET /data` - 获取数据列表
- `GET /data/{id}` - 获取数据详情
- `POST /data` - 创建数据
- `PUT /data/{id}` - 更新数据
- `DELETE /data/{id}` - 删除数据
- `GET /data/search` - 搜索数据

### 4. 系统管理接口
- `GET /system/status` - 系统状态
- `GET /system/config` - 系统配置
- `PUT /system/config` - 更新配置
- `GET /system/logs` - 系统日志
- `POST /system/backup` - 系统备份

## 错误码说明

### HTTP 状态码

- `200` - 请求成功
- `201` - 创建成功
- `400` - 请求参数错误
- `401` - 未授权
- `403` - 禁止访问
- `404` - 资源不存在
- `422` - 验证失败
- `500` - 服务器内部错误

### 业务错误码

| 错误码 | 说明 | HTTP 状态码 |
|--------|------|-------------|
| `AUTH_FAILED` | 认证失败 | 401 |
| `INSUFFICIENT_PERMISSIONS` | 权限不足 | 403 |
| `RESOURCE_NOT_FOUND` | 资源不存在 | 404 |
| `VALIDATION_ERROR` | 验证失败 | 422 |
| `RATE_LIMIT_EXCEEDED` | 请求频率超限 | 429 |
| `INTERNAL_ERROR` | 内部错误 | 500 |

## 限流策略

### 请求限制

- **普通用户**：100 请求/小时
- **高级用户**：1000 请求/小时
- **管理员**：无限制

### 限流响应

当请求超过限制时，API 将返回：

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "请求频率超限，请稍后重试",
    "retry_after": 3600
  }
}
```

## 版本控制

### 版本策略

- **主版本**：不兼容的 API 变更
- **次版本**：向后兼容的功能新增
- **修订版本**：向后兼容的问题修复

### 版本兼容性

- 支持同时运行多个 API 版本
- 新版本默认向后兼容
- 废弃的接口会提前通知并保留一段时间

## 测试接口

### 沙箱环境

- **测试 URL**：`https://sandbox-api.your-project.com`
- **测试数据**：独立的测试数据库
- **限制**：仅支持基本功能测试

### 测试工具

推荐使用以下工具进行 API 测试：

- **Postman**：功能强大的 API 测试工具
- **Insomnia**：轻量级 API 客户端
- **curl**：命令行工具
- **Swagger UI**：在线 API 文档和测试

## 下一步

- [认证授权](./authentication.md) - 详细认证说明
- [接口端点](./endpoints/) - 具体接口文档
- [数据模型](./schemas.md) - 数据结构定义
- [错误码说明](./error-codes.md) - 完整错误码列表

## 获取帮助

- **API 文档**：查看详细接口说明
- **技术支持**：联系开发团队
- **社区讨论**：参与开发者社区
- **问题反馈**：提交 GitHub Issues
