# -*- coding: utf-8 -*-
"""
智能分析系统（股票） - 股票市场数据分析系统
修改：熊猫大侠
版本：v2.1.0
"""
# web_server.py

import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import subprocess
import bcrypt
from functools import wraps
from app.analysis.stock_analyzer import StockAnalyzer
from app.analysis.us_stock_service import USStockService
import threading
import logging
from logging.handlers import RotatingFileHandler
from app.core.mongo_log_handler import MongoLogHandler
import traceback
import os
import json
from datetime import date, datetime, timedelta
from flask_cors import CORS
from pathlib import Path
import time
from flask_session import Session
import redis
from app.core.connections import REDIS_URL_SESSIONS
import threading
import sys
import re
from flask_swagger_ui import get_swaggerui_blueprint
from app.core.config import config_manager
from app.core.mongo_connector import get_mongo_db
from app.core.database import get_session, StockInfo, Portfolio, USE_DATABASE, User, init_db
from app.analysis.news_fetcher import news_fetcher, start_news_scheduler
from app.analysis.etf_analyzer import EtfAnalyzer
from app.web.task_manager import task_manager, TaskStatus
from app.web.api import api_blueprint
# Import analyzer instances from the central module
from app.analysis_instances import *
import akshare as ak

import sys
import os

# 将 tradingagents 目录添加到系统路径
# 这允许应用从 tradingagents 代码库中导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tradingagents')))


# 检查是否需要初始化数据库
if USE_DATABASE:
    init_db()

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

# Configure Server-Side Sessions using the centralized URL
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(REDIS_URL_SESSIONS)
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production' # Secure cookies in prod
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
server_session = Session(app)

CORS(app, resources={r"/*": {"origins": "*"}})
analyzer = StockAnalyzer()
us_stock_service = USStockService()

@app.route('/api/docs')
def get_docs():
    """提供Swagger UI文档页面"""
    return redirect(SWAGGER_URL)


def create_default_admin_user():
    """检查并创建默认的管理员用户 (如果不存在)"""
    if not USE_DATABASE:
        return

    session = get_session()
    try:
        # 检查是否已存在任何用户
        user_exists = session.query(User).first()
        if not user_exists:
            app.logger.info("系统中未找到用户，正在创建默认管理员...")
            
            # 哈希默认密码
            default_password = 'admin123'
            hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
            
            # 创建新用户
            new_admin = User(
                username='admin',
                password_hash=hashed_password.decode('utf-8'),
                password_change_required=True
            )
            session.add(new_admin)
            session.commit()
            app.logger.info("默认管理员 'admin' 创建成功。首次登录后需要修改密码。")
        else:
            app.logger.info("数据库中已存在用户，跳过创建默认管理员。")

    except Exception as e:
        app.logger.error(f"检查或创建默认管理员时出错: {e}")
        session.rollback()
    finally:
        session.close()

# --- 认证和会话管理 ---

def admin_required(f):
    """一个装饰器，用于验证用户是否已作为管理员登录"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            # 如果未登录，重定向到登录页面，并在URL中包含原始请求页面
            flash('此页面需要管理员权限，请先登录。', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    """处理用户登录请求"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        db_session = get_session()
        try:
            # 从数据库中查找用户
            user = db_session.query(User).filter_by(username=username).first()

            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                # 登录成功
                session['is_admin'] = True
                session['username'] = user.username
                session['password_change_required'] = user.password_change_required
                
                flash('登录成功!', 'success')
                
                # 如果需要修改密码，强制跳转
                if user.password_change_required:
                    flash('为了账户安全，请立即修改您的默认密码。', 'warning')
                    return redirect(url_for('change_password'))

                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                # 登录失败
                flash('用户名或密码错误。', 'danger')

        except Exception as e:
            app.logger.error(f"登录时发生数据库错误: {e}")
            flash('服务器内部错误，请稍后再试。', 'danger')
        finally:
            db_session.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    """处理用户登出请求"""
    session.pop('is_admin', None)
    session.pop('username', None)
    session.pop('password_change_required', None)
    flash('您已成功登出。', 'info')
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
@admin_required
def change_password():
    """处理强制密码修改请求"""
    # 再次检查是否真的需要修改密码，防止用户直接访问URL
    if not session.get('password_change_required', False):
        return redirect(url_for('index'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('两次输入的密码不匹配，请重试。', 'danger')
            return render_template('change_password.html')

        if len(new_password) < 8:
            flash('密码长度不能少于8位。', 'danger')
            return render_template('change_password.html')

        db_session = get_session()
        try:
            user = db_session.query(User).filter_by(username=session['username']).first()
            if user:
                # 哈希新密码并更新数据库
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user.password_hash = hashed_password.decode('utf-8')
                user.password_change_required = False
                db_session.commit()

                # 更新会话
                session['password_change_required'] = False
                
                flash('密码修改成功！', 'success')
                return redirect(url_for('index'))
        except Exception as e:
            app.logger.error(f"修改密码时发生数据库错误: {e}")
            flash('服务器内部错误，请稍后再试。', 'danger')
            db_session.rollback()
        finally:
            db_session.close()

    return render_template('change_password.html')


@app.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    """管理应用配置"""
    if request.method == 'POST':
        # 从表单中获取设置
        settings_to_save = {
            'OPENAI_API_URL': request.form.get('api_url'),
            'OPENAI_API_KEY': request.form.get('api_key'),
            'OPENAI_API_MODEL': request.form.get('api_model'),
            'NEWS_MODEL': request.form.get('news_model'),
            'EMBEDDING_MODEL': request.form.get('embedding_model'),
            'FUNCTION_CALL_MODEL': request.form.get('function_call_model')
        }
        
        # 过滤掉用户未输入的空值，但允许用户明确设置为空字符串
        # An empty API key might be a valid state for some configurations
        settings_to_save = {k: v for k, v in settings_to_save.items() if v is not None}

        config_manager.save(settings_to_save)
        
        flash('配置已成功保存。请注意，部分设置可能需要重启应用才能完全生效。', 'success')
        return redirect(url_for('settings'))

    current_settings = config_manager.get_all_configurable_settings()
    return render_template('settings.html', settings=current_settings)


@app.route('/api/restart_system', methods=['POST'])
@admin_required
def restart_system():
    """API endpoint to restart the application."""
    app.logger.info("接收到重启系统的API请求")
    try:
        # 查找 start.sh 脚本的路径
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'start.sh'))
        
        if not os.path.exists(script_path):
            app.logger.error(f"重启脚本未找到: {script_path}")
            return jsonify({'success': False, 'error': '重启脚本未找到'}), 500

        # 在后台启动重启命令
        subprocess.Popen(['bash', script_path, 'restart'])
        
        app.logger.info(f"成功执行重启脚本: {script_path} restart")
        return jsonify({'success': True, 'message': '重启指令已发送'})

    except Exception as e:
        app.logger.error(f"执行重启时发生异常: {traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)}), 500

# --- 认证和会话管理结束 ---


# 确保全局变量在重新加载时不会丢失
if 'analyzer' not in globals():
    try:
        from app.analysis.stock_analyzer import StockAnalyzer

        analyzer = StockAnalyzer()
        print("成功初始化全局StockAnalyzer实例")
    except Exception as e:
        print(f"初始化StockAnalyzer时出错: {e}", file=sys.stderr)
        raise

# Analyzer instances are now initialized in app.analysis_instances
# This avoids circular imports.


# 线程本地存储
thread_local = threading.local()


def get_analyzer():
    """获取线程本地的分析器实例"""
    # 如果线程本地存储中没有分析器实例，创建一个新的
    if not hasattr(thread_local, 'analyzer'):
        thread_local.analyzer = StockAnalyzer()
    return thread_local.analyzer


# 配置日志
# 从环境变量读取日志级别
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

# 创建日志格式化器
formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 配置根日志记录器
root_logger = logging.getLogger()
root_logger.setLevel(log_level)

# 清除所有现有的处理器
if root_logger.hasHandlers():
    root_logger.handlers.clear()

# 添加 MongoDB 处理器
mongo_handler = MongoLogHandler()
mongo_handler.setFormatter(formatter)
root_logger.addHandler(mongo_handler)

# 添加控制台处理器 (用于开发和调试)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

# 将Flask的默认处理器移除
from flask.logging import default_handler
app.logger.removeHandler(default_handler)
app.logger.propagate = True

# 将 werkzeug 日志记录器的级别也设置为 .env 中定义的级别
logging.getLogger('werkzeug').setLevel(log_level)

app.logger.info(f"日志系统已初始化，日志将发送到 MongoDB 和控制台。")


# Task management is now handled by app.web.task_manager


# 保持API兼容的路由
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        stock_codes = data.get('stock_codes', [])
        market_type = data.get('market_type', 'A')

        if not stock_codes:
            return jsonify({'error': '请输入代码'}), 400

        app.logger.info(f"分析股票请求: {stock_codes}, 市场类型: {market_type}")

        # 设置最大处理时间，每只股票10秒
        max_time_per_stock = 10  # 秒
        max_total_time = max(30, min(60, len(stock_codes) * max_time_per_stock))  # 至少30秒，最多60秒

        start_time = time.time()
        results = []

        for stock_code in stock_codes:
            try:
                # 检查是否已超时
                if time.time() - start_time > max_total_time:
                    app.logger.warning(f"分析股票请求已超过{max_total_time}秒，提前返回已处理的{len(results)}只股票")
                    break

                # 使用线程本地缓存的分析器实例
                current_analyzer = get_analyzer()
                result = current_analyzer.quick_analyze_stock(stock_code.strip(), market_type)

                app.logger.info(
                    f"分析结果: 股票={stock_code}, 名称={result.get('stock_name', '未知')}, 行业={result.get('industry', '未知')}")
                results.append(result)
            except Exception as e:
                app.logger.error(f"分析股票 {stock_code} 时出错: {str(e)}")
                results.append({
                    'stock_code': stock_code,
                    'error': str(e),
                    'stock_name': '分析失败',
                    'industry': '未知'
                })

        return jsonify({'results': results})
    except Exception as e:
        app.logger.error(f"分析股票时出错: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/north_flow_history', methods=['POST'])
def api_north_flow_history():
    try:
        data = request.json
        stock_code = data.get('stock_code')
        days = data.get('days', 10)  # 默认为10天，对应前端的默认选项

        # 计算 end_date 为当前时间
        end_date = datetime.now().strftime('%Y%m%d')

        # 计算 start_date 为 end_date 减去指定的天数
        start_date = (datetime.now() - timedelta(days=int(days))).strftime('%Y%m%d')

        if not stock_code:
            return jsonify({'error': '请提供股票代码'}), 400

        # 调用北向资金历史数据方法

        analyzer = CapitalFlowAnalyzer()
        result = analyzer.get_north_flow_history(stock_code, start_date, end_date)

        return custom_jsonify(result)
    except Exception as e:
        app.logger.error(f"获取北向资金历史数据出错: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/search_us_stocks', methods=['GET'])
def search_us_stocks():
    try:
        keyword = request.args.get('keyword', '')
        if not keyword:
            return jsonify({'error': '请输入搜索关键词'}), 400

        results = us_stock_service.search_us_stocks(keyword)
        return jsonify({'results': results})

    except Exception as e:
        app.logger.error(f"搜索美股代码时出错: {str(e)}")
        return jsonify({'error': str(e)}), 500


# 新增可视化分析页面路由
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/stock_detail/<string:stock_code>')
def stock_detail(stock_code):
    market_type = request.args.get('market_type', 'A')
    return render_template('stock_detail.html', stock_code=stock_code, market_type=market_type)


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/market_scan')
def market_scan():
    return render_template('market_scan.html')


# 基本面分析页面
@app.route('/fundamental')
def fundamental():
    return render_template('fundamental.html')


# 资金流向页面
@app.route('/capital_flow')
def capital_flow():
    return render_template('capital_flow.html')


# 情景预测页面
@app.route('/scenario_predict')
def scenario_predict():
    return render_template('scenario_predict.html')


# 风险监控页面
@app.route('/risk_monitor')
def risk_monitor_page():
    return render_template('risk_monitor.html')


# 智能问答页面
@app.route('/qa')
def qa_page():
    return render_template('qa.html')


# 行业分析页面
@app.route('/industry_analysis')
def industry_analysis():
    return render_template('industry_analysis.html')



# 智能体分析页面
@app.route('/agent_analysis')
def agent_analysis_page():
    return render_template('agent_analysis.html')


@app.route('/etf_analysis')
def etf_analysis_page():
    return render_template('etf_analysis.html')


@app.route('/logs')
@admin_required
def logs_page():
    """渲染日志查看页面"""
    return render_template('logs.html')





def make_cache_key_with_stock():
    """创建包含股票代码的自定义缓存键"""
    path = request.path

    # 从请求体中获取股票代码
    stock_code = None
    if request.is_json:
        stock_code = request.json.get('stock_code')

    # 构建包含股票代码的键
    if stock_code:
        return f"{path}_{stock_code}"
    else:
        return path






# ETF 分析路由


# 保留原有API用于向后兼容
@app.route('/api/enhanced_analysis', methods=['POST'])
def enhanced_analysis():
    """原增强分析API的向后兼容版本"""
    try:
        data = request.json
        stock_code = data.get('stock_code')
        market_type = data.get('market_type', 'A')

        if not stock_code:
            return custom_jsonify({'error': '请输入股票代码'}), 400

        # 调用新的任务系统，但模拟同步行为
        # 这会导致和之前一样的超时问题，但保持兼容
        timeout = 300
        start_time = time.time()

        # 获取或创建任务
        task_id, task, is_new = get_or_create_task(
            'stock_analysis',
            stock_code=stock_code,
            market_type=market_type
        )

        # 如果是已完成的任务，直接返回结果
        if task['status'] == TASK_COMPLETED and 'result' in task:
            app.logger.info(f"使用缓存的分析结果: {stock_code}")
            return custom_jsonify({'result': task['result']})

        # 启动分析（如果是新任务）
        if is_new:
            # 同步执行分析
            try:
                result = analyzer.perform_enhanced_analysis(stock_code, market_type)
                update_task_status('stock_analysis', task_id, TASK_COMPLETED, progress=100, result=result)
                app.logger.info(f"分析完成: {stock_code}，耗时 {time.time() - start_time:.2f} 秒")
                return custom_jsonify({'result': result})
            except Exception as e:
                app.logger.error(f"分析过程中出错: {str(e)}")
                update_task_status('stock_analysis', task_id, TASK_FAILED, error=str(e))
                return custom_jsonify({'error': f'分析过程中出错: {str(e)}'}), 500
        else:
            # 已存在正在处理的任务，等待其完成
            max_wait = timeout - (time.time() - start_time)
            wait_interval = 0.5
            waited = 0

            while waited < max_wait:
                with task_lock:
                    current_task = store[task_id]
                    if current_task['status'] == TASK_COMPLETED and 'result' in current_task:
                        return custom_jsonify({'result': current_task['result']})
                    if current_task['status'] == TASK_FAILED:
                        error = current_task.get('error', '任务失败，无详细信息')
                        return custom_jsonify({'error': error}), 500

                time.sleep(wait_interval)
                waited += wait_interval

            # 超时
            return custom_jsonify({'error': '处理超时，请稍后重试'}), 504

    except Exception as e:
        app.logger.error(f"执行增强版分析时出错: {traceback.format_exc()}")
        return custom_jsonify({'error': str(e)}), 500


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


# Update the get_stock_data function in web_server.py to handle date formatting properly











# 基本面分析路由


# 资金流向分析路由
# Add to web_server.py

# 获取概念资金流向的API端点


# 情景预测路由


# 智能问答路由


# 风险分析路由


# 指数分析路由


# 保存股票分析结果到数据库 (MongoDB)
def save_analysis_result(stock_code, market_type, result):
    """保存分析结果到 MongoDB"""
    db = get_mongo_db()
    if not db:
        app.logger.warning("MongoDB not available. Skipping save of analysis result.")
        return

    try:
        analysis_collection = db.analysis_results
        
        # 准备要插入的文档
        analysis_document = {
            'stock_code': stock_code,
            'market_type': market_type,
            'analysis_date': datetime.now(),
            'score': result.get('scores', {}).get('total', 0),
            'recommendation': result.get('recommendation', {}).get('action', ''),
            'technical_data': result.get('technical_analysis', {}),
            'fundamental_data': result.get('fundamental_data', {}),
            'capital_flow_data': result.get('capital_flow_data', {}),
            'ai_analysis': result.get('ai_analysis', '')
        }

        # 插入文档
        analysis_collection.insert_one(analysis_document)
        app.logger.info(f"Successfully saved analysis for {stock_code} to MongoDB.")

    except Exception as e:
        app.logger.error(f"Error saving analysis result to MongoDB: {str(e)}", exc_info=True)


# 从数据库获取历史分析结果

# 添加新闻API端点
# 添加到web_server.py文件中



# --- Start of new FileSessionManager implementation ---
class FileSessionManager:
    """A Flask-compatible file-based session manager for agent tasks."""
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_task_path(self, task_id):
        return self.data_dir / f"{task_id}.json"

    def save_task(self, task_data):
        if 'id' not in task_data:
            app.logger.error("Attempted to save task without an 'id'")
            return
        task_id = task_data['id']
        task_file = self._get_task_path(task_id)
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, ensure_ascii=False, indent=4, cls=NumpyJSONEncoder)

    def load_task(self, task_id):
        task_file = self._get_task_path(task_id)
        if not task_file.exists():
            return None
        with open(task_file, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                app.logger.error(f"Failed to decode JSON for task {task_id}")
                return None

    def get_all_tasks(self):
        tasks = []
        for task_file in self.data_dir.glob("*.json"):
            with open(task_file, 'r', encoding='utf-8') as f:
                try:
                    tasks.append(json.load(f))
                except json.JSONDecodeError:
                    app.logger.warning(f"Skipping corrupted task file: {task_file.name}")
                    continue
        return tasks

    def cleanup_stale_tasks(self, timeout_hours=2):
        """Clean up stale 'running' tasks that have exceeded a timeout."""
        app.logger.info("开始清理过时的任务...")
        cleaned_count = 0
        now = datetime.now()
        
        tasks = self.get_all_tasks()
        for task in tasks:
            if task.get('status') == TASK_RUNNING:
                try:
                    updated_at = datetime.strptime(task.get('updated_at'), '%Y-%m-%d %H:%M:%S')
                    if (now - updated_at).total_seconds() > timeout_hours * 3600:
                        task['status'] = TASK_FAILED
                        task['error'] = '任务因服务器重启或超时而中止'
                        task['updated_at'] = now.strftime('%Y-%m-%d %H:%M:%S')
                        self.save_task(task)
                        cleaned_count += 1
                        app.logger.warning(f"清理了过时的任务 {task.get('id')}，该任务已运行超过 {timeout_hours} 小时。")
                except (ValueError, TypeError) as e:
                    app.logger.error(f"解析任务 {task.get('id')} 的 updated_at 时出错: {e}")
                    continue
        
        if cleaned_count > 0:
            app.logger.info(f"清理完成，共处理了 {cleaned_count} 个过时的任务。")
        else:
            app.logger.info("没有发现需要清理的过时任务。")

    def delete_task(self, task_id):
        """Safely delete a task file."""
        try:
            task_file = self._get_task_path(task_id)
            if task_file.exists():
                task_file.unlink()
                return True
        except Exception as e:
            app.logger.error(f"Failed to delete task {task_id}: {e}")
        return False

# Instantiate the manager
AGENT_SESSIONS_DIR = os.path.join(os.path.dirname(__file__), '../../data/agent_sessions')
agent_session_manager = FileSessionManager(AGENT_SESSIONS_DIR)
# --- End of new FileSessionManager implementation ---


# 智能体分析路由





app.register_blueprint(api_blueprint)


# Start background threads
task_manager.start_cleaner_thread()
start_news_scheduler()

# --- 初始化数据库和默认用户 ---
# 使用应用上下文来确保在正确的时机执行初始化
with app.app_context():
    # 确保所有表已在数据库中创建
    init_db()
    # 检查并创建默认的管理员用户
    create_default_admin_user()
# --- 初始化结束 ---

if __name__ == '__main__':
    # 强制禁用Flask的调试模式，以确保日志配置生效
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", "8888")), debug=False)