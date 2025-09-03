# 大盘分析页 API 接口文档

## 概述
本文档描述大盘分析页（Market Overview）所需的所有后台API接口，包括核心数据接口、图表数据接口、数据导出接口和实时数据接口。

## 接口基础信息
- **基础URL**: `/api/market`
- **数据格式**: JSON
- **认证方式**: Bearer Token
- **请求频率限制**: 100次/分钟

## 核心数据接口

### 1. 指数行情接口

#### 获取主要指数实时行情
```
GET /api/market/indices
```

**请求参数**:
- `codes` (可选): 指数代码数组，如 `["000001", "000300", "399006"]`
- `fields` (可选): 返回字段，如 `["price", "change", "volume"]`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "code": "000001",
      "name": "上证指数",
      "current_price": 3150.25,
      "change": 37.45,
      "change_percent": 1.20,
      "volume": 2850000000,
      "turnover": 885000000000,
      "high": 3160.50,
      "low": 3120.80,
      "open": 3125.30,
      "prev_close": 3112.80
    }
  ],
  "timestamp": "2024-01-15T09:30:00Z"
}
```

### 2. 资金流数据接口

#### 获取市场资金流向数据
```
GET /api/market/fund-flow
```

**请求参数**:
- `start_date` (必需): 开始日期，格式：YYYY-MM-DD
- `end_date` (必需): 结束日期，格式：YYYY-MM-DD
- `flow_type` (可选): 资金类型，可选值：`super_large`, `large`, `medium`, `small`, `all`
- `period` (可选): 数据周期，可选值：`daily`, `weekly`, `monthly`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "summary": {
      "total_inflow": 125000000000,
      "total_outflow": 98000000000,
      "net_inflow": 27000000000
    },
    "daily_data": [
      {
        "date": "2024-01-15",
        "super_large": 45000000000,
        "large": 35000000000,
        "medium": 25000000000,
        "small": 20000000000,
        "net_inflow": 25000000000
      }
    ]
  }
}
```

### 3. 板块资金流接口

#### 获取行业/概念板块资金流数据
```
GET /api/market/sector-fund-flow
```

**请求参数**:
- `sector_type` (必需): 板块类型，可选值：`industry`, `concept`, `region`
- `start_date` (必需): 开始日期
- `end_date` (必需): 结束日期
- `sort_by` (可选): 排序字段，可选值：`inflow`, `change_percent`, `volume`
- `sort_order` (可选): 排序方向，可选值：`asc`, `desc`
- `limit` (可选): 返回数量限制，默认50

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "sector_code": "BK0001",
      "sector_name": "半导体",
      "inflow_5d": [12000000000, 15000000000, 18000000000, 16000000000, 14000000000],
      "consecutive_days": 5,
      "total_inflow": 75000000000,
      "trend_sparkline": [0.8, 1.2, 1.5, 1.3, 1.1]
    }
  ]
}
```

### 4. 市场情绪数据接口

#### 获取市场情绪指标
```
GET /api/market/sentiment
```

**请求参数**:
- `date` (可选): 查询日期，默认今日

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "volume_ratio_distribution": {
      "high": 1250,
      "medium": 1850,
      "low": 2100
    },
    "overbought_oversold": {
      "overbought": 320,
      "oversold": 180,
      "normal": 4500
    },
    "market_breadth": {
      "advance_decline_line": 0.65,
      "advance_count": 2389,
      "decline_count": 2015
    }
  }
}
```

## 图表数据接口

### 5. K线图数据接口

#### 获取指数K线数据
```
GET /api/market/kline
```

**请求参数**:
- `index_code` (必需): 指数代码
- `period` (必需): 时间周期，可选值：`1m`, `5m`, `15m`, `30m`, `1h`, `1d`, `1w`, `1M`
- `start_date` (必需): 开始时间
- `end_date` (必需): 结束时间
- `limit` (可选): 数据条数限制，默认1000

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "index_code": "000001",
    "period": "1d",
    "klines": [
      {
        "timestamp": "2024-01-15T00:00:00Z",
        "open": 3125.30,
        "high": 3160.50,
        "low": 3120.80,
        "close": 3150.25,
        "volume": 2850000000,
        "turnover": 885000000000
      }
    ]
  }
}
```

### 6. 技术指标接口

#### 获取技术指标数据
```
GET /api/market/technical-indicators
```

**请求参数**:
- `index_code` (必需): 指数代码
- `indicator_type` (必需): 指标类型，可选值：`MACD`, `RSI`, `KDJ`, `BOLL`
- `start_date` (必需): 开始时间
- `end_date` (必需): 结束时间
- `period` (可选): 计算周期，默认14

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "index_code": "000001",
    "indicator_type": "MACD",
    "period": 14,
    "values": [
      {
        "timestamp": "2024-01-15T00:00:00Z",
        "macd": 12.5,
        "signal": 8.2,
        "histogram": 4.3
      }
    ]
  }
}
```

## 数据导出接口

### 7. 报告导出接口

#### 导出市场分析报告
```
POST /api/market/export-report
```

**请求参数**:
```json
{
  "report_type": "market_overview",
  "time_range": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-15"
  },
  "format": "excel",
  "include_charts": true,
  "include_data": true
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "download_url": "https://api.example.com/download/report_20240115_123456.xlsx",
    "expires_at": "2024-01-16T12:00:00Z",
    "file_size": 2048576
  }
}
```

## 实时数据接口

### 8. WebSocket实时推送

#### 实时市场数据推送
```
WS /api/market/realtime
```

**连接参数**:
- `token`: 认证令牌
- `subscriptions`: 订阅的数据类型数组

**订阅数据类型**:
- `indices`: 指数实时数据
- `fund_flow`: 资金流实时数据
- `sentiment`: 市场情绪实时数据

**推送消息格式**:
```json
{
  "type": "indices_update",
  "timestamp": "2024-01-15T09:30:15Z",
  "data": {
    "index_code": "000001",
    "current_price": 3150.25,
    "change": 37.45,
    "change_percent": 1.20
  }
}
```

## 接口性能要求

### 响应时间
- **历史数据查询**: < 500ms
- **实时数据查询**: < 100ms
- **数据导出**: < 30秒

### 并发支持
- **支持用户数**: 1000+ 并发用户
- **单用户请求限制**: 100次/分钟

### 数据缓存
- **历史数据**: 24小时
- **实时数据**: 1分钟
- **技术指标**: 1小时

### 错误处理

#### 错误码定义
- `200`: 成功
- `400`: 请求参数错误
- `401`: 未授权
- `403`: 禁止访问
- `404`: 数据不存在
- `429`: 请求频率超限
- `500`: 服务器内部错误

#### 错误响应格式
```json
{
  "code": 400,
  "message": "Invalid parameter: start_date",
  "details": "start_date must be in YYYY-MM-DD format",
  "timestamp": "2024-01-15T09:30:00Z"
}
```

## 数据格式规范

### 时间格式
- 所有时间字段使用ISO 8601格式：`YYYY-MM-DDTHH:mm:ssZ`
- 日期字段使用：`YYYY-MM-DD`

### 数值格式
- 价格保留2位小数
- 金额使用整数（以分为单位）
- 百分比使用小数形式（如1.20表示1.20%）

### 分页格式
```json
{
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```
