# CLAUDE.md

该文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 常用命令

- **安装依赖**:
  ```bash
  pip install -r requirements.txt
  # 如果新闻搜索功能报错，可能需要安装
  pip install tavily-python
  ```

- **运行应用**: 主服务器可以通过 `start.sh` 脚本进行管理。
  ```bash
  # 在后台启动服务器
  bash start.sh start

  # 停止服务器
  bash start.sh stop

  # 重启服务器
  bash start.sh restart

  # 查看服务器状态
  bash start.sh status

  # 查看服务器日志
  bash start.sh logs
  ```

- **使用 Docker 运行**:
  ```bash
  docker-compose up -d
  ```

- **运行测试**: 项目使用 `pytest` 进行测试。
  ```bash
  pytest
  ```

## 架构概览

该项目是一个使用 Python 和 Flask 构建的股票分析系统。

- **主应用 (`web_server.py`)**: Flask 服务器，处理 HTTP 请求、提供前端页面和 REST API。

- **模块化分析器**: 核心分析逻辑分布在多个模块中：
  - `stock_analyzer.py`: 核心分析引擎，使用 `akshare` 获取数据，计算技术指标，并集成 AI 模型进行定性分析。
  - `fundamental_analyzer.py`: 基本面分析。
  - `capital_flow_analyzer.py`: 资金流分析。
  - `scenario_predictor.py`: 市场情景预测。
  - `risk_monitor.py`: 风险评估。
  - `stock_qa.py`: 智能问答。
  - `news_fetcher.py`: 新闻获取与缓存。
  - `us_stock_service.py`: 美股服务（可选）。

- **技术栈**:
  - **后端**: Python, Flask, AKShare
  - **前端**: HTML, CSS, JavaScript, Bootstrap 5, ApexCharts
  - **数据分析**: Pandas, NumPy

- **异步任务**: 对于耗时操作（如市场扫描），系统通过 `/api/start_market_scan` 等端点启动后台线程 (`threading`) 执行任务，并返回 `task_id`。前端通过 `/api/scan_status/<task_id>` 轮询结果。

- **配置**: 应用配置通过 `.env` 文件管理。关键参数包括 API 密钥和数据库/缓存设置。

- **缓存**: 系统使用 Flask-Caching 和内存字典进行缓存，以减少重复的 API 调用和计算。缓存会在每个交易日收盘后自动清理。

## 关键配置参数

可在 `stock_analyzer.py` 的 `__init__` 方法中调整以下技术指标参数：

- `ma_periods`: 移动平均线周期
- `rsi_period`: RSI 指标周期
- `bollinger_period`: 布林带周期
- `bollinger_std`: 布林带标准差
- `volume_ma_period`: 成交量均线周期
- `atr_period`: ATR 周期

## 环境变量

应用通过 `.env` 文件配置，关键变量如下：

| 变量 | 描述 | 默认值 |
|---|---|---|
| `API_PROVIDER` | API 提供商选择 | `openai` |
| `OPENAI_API_KEY` | OpenAI API 密钥 | **必须** |
| `OPENAI_API_URL` | OpenAI API 端点 URL | `https://api.openai.com/v1` |
| `OPENAI_API_MODEL`| 要使用的 OpenAI 模型 | `gpt-4o` |
| `NEWS_MODEL` | 用于新闻分析的 AI 模型 | |
| `PORT` | Web 服务器端口 | `8888` |
| `USE_DATABASE` | 设置为 `True` 以使用持久的 SQLite 数据库 | `False` |
| `USE_REDIS_CACHE`| 设置为 `True` 以使用 Redis 进行缓存 | `False` |

## API 文档

项目提供 REST API，API 文档可通过 Swagger UI 在 `/api/docs` 端点查看。

---
*请始终用中文回答用户。*
