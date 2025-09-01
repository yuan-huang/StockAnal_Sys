# -*- coding: utf-8 -*-
"""
智能分析系统（股票） - 股票市场数据分析系统
修改：熊猫大侠
版本：v2.1.0
"""
# web_server.py

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import os
from flask_cors import CORS
import sys
from flask_swagger_ui import get_swaggerui_blueprint
from app.web.api import api_blueprint
from app.web.page_router import page_blueprint
import logging
from dotenv import load_dotenv, find_dotenv
from app.analysis.news_fetcher import start_news_scheduler

# 将 tradingagents 目录添加到系统路径
# 这允许应用从 tradingagents 代码库中导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tradingagents')))

# 加载环境变量
load_dotenv(find_dotenv())

# 导入依赖注入容器
from app.analysis._analysis_container import AnalysisContainer

# 创建并配置依赖注入容器
analysis_container = AnalysisContainer()
# 将依赖注入容器连接到所有相关模块
analysis_container.wire(modules=[
    __name__,  # 主模块
    'app.web.api',  # API模块
    'app.web.api.tasks',  # 任务模块
    'app.web.api.stock_analysis',  # 股票分析模块
    'app.web.api.data',  # 数据模块
    'app.web.api.analysis',  # 分析模块
    'app.web.api.us_stocks',  # 美股模块
    'app.web.api.capital_flow',  # 资金流模块
    'app.web.api.system',  # 系统模块
    'app.web.api.news',  # 新闻模块
    'app.web.api.qa',  # 智能问答模块
])

# 定义日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 配置Swagger
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "股票智能分析系统 API文档"
    }
)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key_for_development')

# 初始化依赖注入容器
app.container = analysis_container

# 注册Swagger蓝图
app.register_blueprint(swaggerui_blueprint)

# 启用CORS
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/docs')
def get_docs():
    """提供Swagger UI文档页面"""
    return redirect(SWAGGER_URL)


# 添加在web_server.py主代码中
@app.errorhandler(404)
def not_found(error):
    """处理404错误"""
    if request.path.startswith('/api/'):
        # 为API请求返回JSON格式的错误
        return jsonify({
            'error': '找不到请求的API端点',
            'path': request.path,
            'method': request.method
        }), 404
    # 为网页请求返回HTML错误页
    return render_template('error.html', error_code=404, message="找不到请求的页面"), 404


@app.errorhandler(500)
def server_error(error):
    """处理500错误"""
    app.logger.error(f"服务器错误: {str(error)}")
    if request.path.startswith('/api/'):
        # 为API请求返回JSON格式的错误
        return jsonify({
            'error': '服务器内部错误',
            'message': str(error)
        }), 500
    # 为网页请求返回HTML错误页
    return render_template('error.html', error_code=500, message="服务器内部错误"), 500


# 注册API和页面蓝图
app.register_blueprint(api_blueprint)
app.register_blueprint(page_blueprint)

# --- 初始化应用 ---
# 使用应用上下文来确保在正确的时机执行初始化
with app.app_context():
    # 初始化日志输出
    print("="*50)
    print("应用启动")
    print("="*50)
    print(f"依赖注入容器状态: {analysis_container}")
    start_news_scheduler()  

