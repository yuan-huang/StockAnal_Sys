# -*- coding: utf-8 -*-
"""
页面路由处理模块
包含所有页面相关的路由和视图函数
"""

from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from functools import wraps
from app.core.database import get_session, User
import bcrypt


# 创建蓝图
page_blueprint = Blueprint('pages', __name__)

# --- 认证装饰器 ---
def admin_required(f):
    """一个装饰器，用于验证用户是否已作为管理员登录"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            # 如果未登录，重定向到登录页面，并在URL中包含原始请求页面
            flash('此页面需要管理员权限，请先登录。', 'warning')
            return redirect(url_for('pages.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# --- 页面路由 ---

@page_blueprint.route('/')
def index():
    """主页"""
    return render_template('index.html')

@page_blueprint.route('/dashboard')
def dashboard():
    """仪表板页面"""
    return render_template('dashboard.html')

@page_blueprint.route('/stock_detail/<string:stock_code>')
def stock_detail(stock_code):
    """股票详情页面"""
    market_type = request.args.get('market_type', 'A')
    return render_template('stock_detail.html', stock_code=stock_code, market_type=market_type)

@page_blueprint.route('/portfolio')
def portfolio():
    """投资组合页面"""
    return render_template('portfolio.html')

@page_blueprint.route('/market_scan')
def market_scan():
    """市场扫描页面"""
    return render_template('market_scan.html')

@page_blueprint.route('/fundamental')
def fundamental():
    """基本面分析页面"""
    return render_template('fundamental.html')

@page_blueprint.route('/capital_flow')
def capital_flow():
    """资金流向页面"""
    return render_template('capital_flow.html')

@page_blueprint.route('/scenario_predict')
def scenario_predict():
    """情景预测页面"""
    return render_template('scenario_predict.html')

@page_blueprint.route('/risk_monitor')
def risk_monitor_page():
    """风险监控页面"""
    return render_template('risk_monitor.html')

@page_blueprint.route('/qa')
def qa_page():
    """智能问答页面"""
    return render_template('qa.html')

@page_blueprint.route('/industry_analysis')
def industry_analysis():
    """行业分析页面"""
    return render_template('industry_analysis.html')

@page_blueprint.route('/agent_analysis')
def agent_analysis_page():
    """智能体分析页面"""
    return render_template('agent_analysis.html')

@page_blueprint.route('/etf_analysis')
def etf_analysis_page():
    """ETF分析页面"""
    return render_template('etf_analysis.html')

@page_blueprint.route('/logs')
def logs_page():
    """日志查看页面"""
    return render_template('logs.html')

# --- 认证相关页面路由 ---

@page_blueprint.route('/login', methods=['GET', 'POST'])
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
                    return redirect(url_for('pages.change_password'))

                next_page = request.args.get('next')
                return redirect(next_page or url_for('pages.index'))
            else:
                # 登录失败
                flash('用户名或密码错误。', 'danger')

        except Exception as e:
            import logging
            logging.error(f"登录时发生数据库错误: {e}")
            flash('服务器内部错误，请稍后再试。', 'danger')
        finally:
            db_session.close()

    return render_template('login.html')

@page_blueprint.route('/logout')
def logout():
    """处理用户登出请求"""
    session.pop('is_admin', None)
    session.pop('username', None)
    session.pop('password_change_required', None)
    flash('您已成功登出。', 'info')
    return redirect(url_for('pages.login'))

@page_blueprint.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """处理强制密码修改请求"""
    # 再次检查是否真的需要修改密码，防止用户直接访问URL
    if not session.get('password_change_required', False):
        return redirect(url_for('pages.index'))

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
                return redirect(url_for('pages.index'))
        except Exception as e:
            import logging
            logging.error(f"修改密码时发生数据库错误: {e}")
            flash('服务器内部错误，请稍后再试。', 'danger')
            db_session.rollback()
        finally:
            db_session.close()

    return render_template('change_password.html')

@page_blueprint.route('/settings', methods=['GET', 'POST'])
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

        # 由于我们现在使用环境变量，这里暂时注释掉配置保存功能
        # TODO: 实现基于环境变量的配置管理
        flash('配置管理功能正在重构中，请通过.env文件修改配置。', 'info')
        return redirect(url_for('pages.settings'))

    # 从环境变量读取当前设置
    import os
    current_settings = {
        'OPENAI_API_URL': os.getenv('OPENAI_API_URL', ''),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
        'OPENAI_API_MODEL': os.getenv('OPENAI_API_MODEL', ''),
        'NEWS_MODEL': os.getenv('NEWS_MODEL', ''),
        'EMBEDDING_MODEL': os.getenv('EMBEDDING_MODEL', ''),
        'FUNCTION_CALL_MODEL': os.getenv('FUNCTION_CALL_MODEL', '')
    }
    return render_template('settings.html', settings=current_settings) 




