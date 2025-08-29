# FinCore AI 股票分析系统 - 开发指导文档

本文档旨在为开发者提供 `FinCore AI` 股票分析系统的全面技术概览，帮助您快速理解项目架构、核心模块、API接口、大模型调用机制及关键系统设计。

## 目录

1.  [项目架构概览](#项目架构概览)
    *   [目录结构](#目录结构)
    *   [关键文件说明](#关键文件说明)
2.  [核心模块详解](#核心模块详解)
    *   [分析器模块 (`app/analysis`)](#分析器模块-appanalysis)
    *   [Web服务 (`app/web`)](#web服务-appweb)
3.  [API接口调用指南](#api接口调用指南)
    *   [API文档](#api文档)
    *   [API认证](#api认证)
    *   [主要端点](#主要端点)
    *   [调用示例](#调用示例)
4.  [大模型（LLM）调用机制](#大模型llm调用机制)
    *   [配置](#配置)
    *   [调用点](#调用点)
5.  [关键系统设计](#关键系统设计)
    *   [异步任务系统](#异步任务系统)
    *   [缓存机制](#缓存机制)
6.  [开发与部署](#开发与部署)
    *   [环境设置](#环境设置)
    *   [本地运行](#本地运行)
    *   [Docker部署](#docker部署)

---

## 1. 项目架构概览

本系统采用基于 Python 和 Flask 的模块化架构，旨在实现功能解耦和高可维护性。

### 目录结构

项目的核心代码位于 `app` 目录下，其结构如下：

-   `app/`: 应用主目录。
    -   `analysis/`: 包含所有核心数据分析逻辑的模块，每个文件负责一个特定的分析领域（如技术指标、基本面、资金流等）。
    -   `core/`: 存放应用的核心组件，如配置管理 (`config.py`)、数据库模型 (`database.py`) 和缓存管理 (`cache.py`)。
    -   `web/`: 处理所有与Web服务相关的功能。
        -   `api/`: 存放Flask蓝图，将API路由按功能（`analysis.py`, `tasks.py`, `data.py`）进行模块化组织。
        -   `static/`: 存放前端静态资源（CSS, JavaScript, 图像）。
        -   `templates/`: 存放Jinja2前端模板文件。
-   `data/`: 存放持久化数据，如SQLite数据库文件和日志。
-   `scripts/`: 包含用于管理应用的Shell脚本（如 `start.sh`）。
-   `tests/`: 存放单元测试和集成测试。
-   `tradingagents/`: AI智能体分析模块，包含独立的图结构和分析逻辑。

### 关键文件说明

-   `run.py`: 项目的入口文件，用于启动Flask Web服务器。
-   `web_server.py`: Flask应用的主文件，负责初始化应用、注册蓝图、配置全局中间件（如错误处理、日志）和加载分析器模块。
-   `app/core/config.py`: 集中管理应用的配置，从 `.env` 文件中加载环境变量。
-   `app/core/database.py`: 定义了所有与数据库交互相关的模型（使用SQLAlchemy ORM）和会话管理。
-   `app/core/cache.py`: 实现了应用的缓存逻辑，支持Redis和内存缓存两种模式，并包含自动清理策略。
-   `app/web/task_manager.py`: 提供了中央异步任务管理器 `TaskManager`，用于处理所有耗时操作。
-   `docker-compose.yml`: 用于通过Docker快速部署应用及其依赖（如Redis）。
-   `requirements.txt`: 列出了项目的所有Python依赖。
-   `.env-example`: `.env` 文件的模板，指导用户如何配置必要的环境变量。
-   `SECURITY.md`: 提供了关于如何安全配置应用的重要指南，特别是API密钥和数据库密码。

---

## 2. 核心模块详解

本系统的核心功能由分析器模块和Web服务模块共同完成。

### 分析器模块 (`app/analysis`)

该目录下的每个模块都是一个独立的分析单元，负责处理特定领域的数据获取与分析。

-   **`stock_analyzer.py`**:
    -   **职责**: 项目的核心分析引擎，负责获取股票的K线历史数据、计算各种技术指标（如MA, RSI, Bollinger Bands），并整合其他分析器的结果生成综合评分。
    -   **关键方法**:
        -   `get_stock_data`: 从 `akshare` 获取原始K线数据。
        -   `calculate_indicators`: 计算技术指标。
        -   `perform_enhanced_analysis`: 执行全面的单股分析，整合了技术、基本面、资金流和AI分析。
        -   `quick_analyze_stock`: 用于市场扫描的轻量级分析方法。

-   **`fundamental_analyzer.py`**: 负责获取和评估公司的基本面数据，如市盈率（PE）、市净率（PB）等，并计算基本面得分。

-   **`capital_flow_analyzer.py`**: 分析资金流向数据，包括概念板块资金流、个股资金流排行以及北向资金动向。

-   **`scenario_predictor.py`**: 利用大模型（LLM）对股票未来走势进行情景预测。

-   **`stock_qa.py`**: 实现了股票智能问答功能，能够基于上下文回答用户关于特定股票的具体问题。

-   **`risk_monitor.py`**: 评估个股及投资组合的风险，计算波动率、夏普比率等风险指标。

-   **`news_fetcher.py`**: 负责从多个来源（如财联社、新浪财经）获取新闻，并提供缓存功能以避免重复请求。

### Web服务 (`app/web`)

该目录负责处理所有HTTP请求、路由、前端渲染和API逻辑。

-   **`web_server.py`**:
    -   **职责**: 作为Flask应用的主入口，此文件负责：
        1.  初始化Flask应用实例。
        2.  加载应用配置，包括密钥、数据库URL等。
        3.  注册API蓝图 (`api_blueprint`)，将API路由与主应用分离。
        4.  定义全局的HTTP错误处理（如404, 500）。
        5.  初始化所有分析器模块的实例。
        6.  定义非API的页面路由（如主页、仪表盘等）。

-   **API蓝图 (`app/web/api`)**:
    -   **`__init__.py`**: 创建一个名为 `api` 的Flask `Blueprint`，并从其他模块导入路由以完成注册。
    -   **`analysis.py`**: 包含了所有同步的、直接返回分析结果的API端点，例如基本面分析 (`/api/fundamental_analysis`) 和风险分析 (`/api/risk_analysis`)。
    -   **`tasks.py`**: 管理所有异步任务的API端点。这包括启动长时间运行的任务（如 `/api/start_market_scan`）以及查询任务状态和结果的通用接口（`/api/tasks/<task_id>`）。
    -   **`data.py`**: 提供了所有与数据获取相关的API端点，如获取股票历史数据 (`/api/stock_data`) 和指数成分股 (`/api/index_stocks`)。

这种模块化的路由设计使得API逻辑清晰，易于扩展和维护。

---

## 3. API接口调用指南

本系统提供了一套完整的RESTful API，用于数据获取、分析任务启动和结果查询。

### API文档

最全面的API文档是通过Swagger UI提供的。在系统运行后，您可以访问以下URL查看所有端点、参数和响应模型的详细信息：

-   **Swagger UI**: `http://<your-server-address>/api/docs`

### API认证

部分敏感API（如系统管理类）通过基于会话的认证进行保护，需要管理员登录后才能访问。

### 主要端点

API端点根据功能被组织在不同的模块中：

#### 数据获取 (`app/web/api/data.py`)

-   `GET /api/stock_data`: 获取指定股票的历史K线数据和技术指标。
    -   **参数**: `stock_code`, `market_type`, `period`
-   `GET /api/index_stocks`: 获取指数的成分股列表。
    -   **参数**: `index_code`
-   `GET /api/latest_news`: 获取最新的财经新闻。
    -   **参数**: `limit`, `source`

#### 同步分析 (`app/web/api/analysis.py`)

-   `POST /api/fundamental_analysis`: 对单个股票进行基本面分析。
    -   **请求体**: `{"stock_code": "..."}`
-   `POST /api/risk_analysis`: 对单个股票或投资组合进行风险评估。
    -   **请求体**: `{"stock_code": "..."}` 或 `{"portfolio": [...]}`

#### 异步任务 (`app/web/api/tasks.py`)

对于耗时较长的分析，系统采用异步任务模型。客户端首先请求启动一个任务，获得一个 `task_id`，然后通过该ID轮询任务状态和结果。

-   `POST /api/start_stock_analysis`: 启动对单个股票的深度增强分析。
    -   **请求体**: `{"stock_code": "...", "market_type": "A"}`
    -   **成功响应**: `{"task_id": "..."}`
-   `POST /api/start_market_scan`: 启动对多个股票的市场扫描。
    -   **请求体**: `{"stock_list": ["...", "..."], "min_score": 60}`
    -   **成功响应**: `{"task_id": "..."}`
-   `GET /api/tasks/<task_id>`: 查询指定任务的状态和结果。
    -   **响应**: 包含任务状态（`PENDING`, `RUNNING`, `COMPLETED`, `FAILED`）、进度和结果的JSON对象。
-   `GET /api/tasks`: 获取所有任务的列表。

### 调用示例

使用 `curl` 调用异步股票分析的示例流程：

1.  **启动分析任务**:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"stock_code": "600519"}' http://127.0.0.1:8888/api/start_stock_analysis
    ```
    *响应*: `{"task_id":"some-unique-task-id"}`

2.  **查询任务状态**:
    ```bash
    curl http://127.0.0.1:8888/api/tasks/some-unique-task-id
    ```
    *响应*: `{"id": "...", "name": "...", "status": "COMPLETED", "result": {...}}`

---

## 4. 大模型（LLM）调用机制

本系统在多个分析模块中集成了大语言模型（LLM）以提供深入的定性分析、预测和问答能力。

### 配置

所有与LLM相关的配置都通过 `.env` 文件进行管理，并由 `app/core/config.py` 中的 `ConfigManager` 加载。关键配置项包括：

-   `OPENAI_API_URL`: API的基地址。
-   `OPENAI_API_KEY`: 用于认证的API密钥。
-   `OPENAI_API_MODEL`: 用于通用任务的默认模型（例如 `gpt-4o`）。
-   `NEWS_MODEL`: 专门用于新闻情感分析和摘要的模型。
-   `EMBEDDING_MODEL`: 用于文本向量化的模型。
-   `FUNCTION_CALL_MODEL`: 支持函数调用的模型。

### 调用点

LLM主要在以下几个核心分析模块中被调用：

1.  **`stock_analyzer.py`**:
    -   在 `perform_enhanced_analysis` 方法中，调用LLM对技术分析、基本面和资金流数据进行综合评估，生成一段自然语言格式的投资建议和市场情绪分析。

2.  **`scenario_predictor.py`**:
    -   `generate_scenarios` 方法是LLM的核心应用之一。它将股票的历史数据、关键技术指标和最新新闻作为上下文，要求LLM基于这些信息，预测在未来特定时间段内（如60天）可能出现的多种市场情景（乐观、悲观、中性），并给出相应的逻辑支撑。

3.  **`stock_qa.py`**:
    -   `answer_question` 方法构建一个包含股票实时数据和历史背景的上下文，然后将用户的问题与该上下文结合，让LLM提供精准的回答。这实现了基于实时数据的智能问答功能。

4.  **`news_fetcher.py`**:
    -   在获取到新闻列表后，可以调用LLM对新闻标题和内容进行情感分析，判断其对市场的潜在影响是积极、消极还是中性。

这种设计将LLM的调用封装在具体的业务模块中，使得LLM的应用与特定的分析任务紧密结合，提高了分析的深度和智能化水平。

---

## 5. 关键系统设计

为了确保系统的性能、可扩展性和可维护性，我们实现了一些关键的设计模式。

### 异步任务系统

对于可能耗时较长的操作，如深度股票分析和大规模市场扫描，系统采用了一套完整的异步任务处理机制。

-   **中央任务管理器 (`app/web/task_manager.py`)**:
    -   `TaskManager` 类是整个异步系统的核心。它负责创建、跟踪、更新和清理所有后台任务。
    -   任务的状态（如 `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`）和结果都存储在内存中，并通过API暴露给前端。
    -   管理器还包含一个后台清理线程，用于自动中止那些因意外（如服务器重启）而卡在“运行中”状态的僵尸任务。

-   **并发执行 (`ThreadPoolExecutor`)**:
    -   特别是在市场扫描功能中，为了显著提高处理效率，系统使用了 `concurrent.futures.ThreadPoolExecutor`。
    -   这使得对股票列表的分析可以并行执行，将原本需要数分钟的串行扫描任务缩短到几十秒内，极大地改善了用户体验。

-   **API流程**:
    1.  客户端通过 `POST /api/start_*` 端点请求一个新任务。
    2.  服务器立即创建一个任务记录，返回一个唯一的 `task_id`，HTTP状态码为 `202 Accepted`。
    3.  服务器在一个独立的后台线程中开始执行实际的分析逻辑。
    4.  客户端使用 `task_id` 定期轮询 `GET /api/tasks/<task_id>` 端点以获取最新状态和进度。
    5.  任务完成后，结果会附加到任务对象中，客户端在下一次轮询时即可获取。

### 缓存机制

为了减少对外部数据源（如 `akshare`）的重复请求和避免重复计算，系统实现了一个灵活的、多层次的缓存系统。

-   **中央缓存管理器 (`app/core/cache.py`)**:
    -   `CacheManager` 类提供了统一的缓存接口（`get`, `set`）。
    -   它支持两种后端存储：
        1.  **内存缓存**: 一个简单的Python字典，适用于开发和轻量级部署。
        2.  **Redis缓存**: 当在 `.env` 中配置了 `USE_REDIS_CACHE=True` 和 `REDIS_URL` 时，管理器会自动切换到Redis，提供更持久、可扩展的缓存能力。

-   **缓存应用点**:
    -   **数据获取**: 在各个分析器模块（如 `stock_analyzer.py`）中，从 `akshare` 获取的原始数据会被缓存，缓存键通常包含股票代码和日期，以确保数据的时效性。
    -   **计算结果**: 耗时的计算结果（如技术指标）也会被缓存，避免对相同数据进行重复计算。
    -   **API层缓存**: 使用 `Flask-Caching` 对某些不经常变动的API端点（如获取K线历史数据）的响应进行缓存。

-   **缓存失效**:
    -   缓存管理器包含一个自动清理机制，会在每个交易日结束后（例如，通过一个定时任务）清除当日的股票数据缓存，以确保第二天获取的是最新的数据。

---

## 6. 开发与部署

### 环境设置

1.  **克隆代码库**:
    ```bash
    git clone <repository-url>
    cd StockAnal_Sys
    ```

2.  **创建并激活虚拟环境**:
    ```bash
    python3 -m venv env
    source env/bin/activate  # on Windows: env\Scripts\activate
    ```

3.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **配置环境变量**:
    -   复制 `.env-example` 文件为 `.env`。
    -   编辑 `.env` 文件，至少填入您的 `OPENAI_API_KEY`。
    -   为了安全起见，强烈建议您按照 `SECURITY.md` 指南生成并配置您自己的 `SECRET_KEY`。

### 本地运行

-   使用 `start.sh` 脚本可以方便地管理应用：
    -   **启动服务**: `bash scripts/start.sh start`
    -   **查看状态**: `bash scripts/start.sh status`
    -   **查看日志**: `bash scripts/start.sh logs`
    -   **停止服务**: `bash scripts/start.sh stop`

-   服务启动后，默认监听 `http://0.0.0.0:8888`。

### Docker部署

项目提供了 `docker-compose.yml` 文件，用于一键部署应用及其所有依赖（如Redis）。

1.  **确保Docker和Docker Compose已安装**。

2.  **构建并启动容器**:
    ```bash
    docker-compose up --build -d
    ```
    -   `--build` 标志确保在启动前重新构建镜像。
    -   `-d` 标志让容器在后台运行。

3.  **管理服务**:
    -   **查看日志**: `docker-compose logs -f`
    -   **停止服务**: `docker-compose down`

通过Docker部署可以确保环境的一致性，并简化了依赖管理，是生产环境推荐的部署方式。
