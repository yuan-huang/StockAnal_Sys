# -*- coding: utf-8 -*-
"""
智能分析系统（股票） - 股票市场数据分析系统
修改：熊猫大侠
版本：v2.1.0
"""
# web_server.py
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from flask_api import FlaskAPI
import os
import logging
from app.api import api_blueprint
# 加载环境变量

# 导入依赖注入容器
from app.analysis._analysis_container import AnalysisContainer

# 创建并配置依赖注入容器
analysis_container = AnalysisContainer()
# 将依赖注入容器连接到所有相关模块
analysis_container.wire(modules=[
    __name__,  # 主模块
    'app.api',  # API模块
    'app.api.tasks',  # 任务模块
    'app.api.stock_analysis',  # 股票分析模块
    'app.api.data',  # 数据模块
    'app.api.analysis',  # 分析模块
    'app.api.us_stocks',  # 美股模块
    'app.api.capital_flow',  # 资金流模块
    'app.api.system',  # 系统模块
    'app.api.news',  # 新闻模块
    'app.api.qa',  # 智能问答模块
    'app.api.agent_analysis',  # 智能体分析模块
])

# 定义日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


app = Flask(__name__)
app.container = analysis_container
app.register_blueprint(api_blueprint)

# --- 初始化应用 ---
# 使用应用上下文来确保在正确的时机执行初始化
with app.app_context():
    # 初始化日志输出
    print("="*50)
    print("应用启动")
    print(f"依赖注入容器状态: {analysis_container}")
    print(f"Debug 模式: {app.debug}")
    if app.debug:
        print("Swagger 文档已启用: /api/docs")
    print("="*50)

