
# app/web/api/analysis.py
from flask_api import request, status
from flask import Blueprint

from app.web.api import api_blueprint
from . import api_blueprint
from app.web.utils import custom_jsonify
from dependency_injector.wiring import inject, Provide
from app.analysis.fundamental_analyzer import FundamentalAnalyzer
from app.analysis.capital_flow_analyzer import CapitalFlowAnalyzer
from app.analysis._analysis_container import AnalysisContainer
from app.analysis.scenario_predictor import ScenarioPredictor
from app.analysis.stock_qa import StockQA
from app.analysis.risk_monitor import RiskMonitor
from app.analysis.index_industry_analyzer import IndexIndustryAnalyzer
from app.analysis.industry_analyzer import IndustryAnalyzer
from app.analysis.task_manager import TaskManager,TaskCancelledException
from app.analysis.task_manager import TaskStatus
from app.analysis.stock_analyzer import StockAnalyzer
import threading
import os
import logging
import traceback
import time
from datetime import datetime

logger = logging.getLogger(__name__)

agent_analysis_bp = Blueprint('agent_analysis', __name__, url_prefix='/agent_analysis')

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 智能体分析路由
@agent_analysis_bp.route('/start_agent_analysis', methods=['POST'])
@inject
def start_agent_analysis(task_manager: TaskManager = Provide[AnalysisContainer.task_manager], stock_analyzer: StockAnalyzer = Provide[AnalysisContainer.stock_analyzer]):
    """启动智能体分析任务"""
    try:
        data = request.data
        stock_code = data.get('stock_code')
        research_depth = data.get('research_depth', 3)
        market_type = data.get('market_type', 'A')
        selected_analysts = data.get('selected_analysts', ["market", "social", "news", "fundamentals"])
        analysis_date = data.get('analysis_date')
        enable_memory = data.get('enable_memory', True)
        max_output_length = data.get('max_output_length', 2048)

        if not stock_code:
            return {'error': '请提供股票代码'}, status.HTTP_400_BAD_REQUEST

        # 创建新任务
        task = task_manager.create_task(name=f"Agent Analysis for {stock_code}", params={
            'stock_code': stock_code,
            'research_depth': research_depth,
            'market_type': market_type,
            'selected_analysts': selected_analysts,
            'analysis_date': analysis_date,
            'enable_memory': enable_memory,
            'max_output_length': max_output_length
        })
        task_id = task['id']
        
        
        def run_agent_analysis():
            """在后台线程中运行智能体分析"""
            try:
   
                
                task_manager.update_task(task_id, status=TaskStatus.RUNNING, progress=5, result={'current_step': '正在初始化智能体...'})

                # --- 修复 Start: 强制使用主应用的OpenAI代理配置 ---
                config = DEFAULT_CONFIG.copy()
                config['llm_provider'] = 'openai'
                config['backend_url'] = os.getenv('OPENAI_API_URL')
                main_model = os.getenv('OPENAI_API_MODEL', 'gpt-4o')
                config['deep_think_llm'] = main_model
                config['quick_think_llm'] = main_model
                config['memory_enabled'] = enable_memory
                config['max_tokens'] = max_output_length
                
                if not os.getenv('OPENAI_API_KEY'):
                    raise ValueError("主应用的 OPENAI_API_KEY 未在.env文件中设置")

                logger.info(f"强制使用主应用代理配置进行智能体分析: provider={config['llm_provider']}, url={config['backend_url']}, model={config['deep_think_llm']}")

                ta = TradingAgentsGraph(
                    selected_analysts=selected_analysts,
                    debug=True, 
                    config=config
                )
                # --- 修复 End ---
                
                def progress_callback(progress, step):
                    current_task = task_manager.get_task(task_id)
                    if not current_task or current_task.get('status') == TaskStatus.CANCELLED:
                         raise TaskCancelledException(f"任务 {task_id} 已被用户取消")
                    task_manager.update_task(task_id, status=TaskStatus.RUNNING, progress=progress, result={'current_step': step})

                today = analysis_date or datetime.now().strftime('%Y-%m-%d')
                state, decision = ta.propagate(stock_code, today, market_type=market_type, progress_callback=progress_callback)
                
                # 修复：在任务完成时，获取并添加公司名称到最终结果中
                try:
                    stock_info = stock_analyzer.get_stock_info(stock_code)
                    stock_name = stock_info.get('股票名称', '未知')
                    # 将公司名称添加到 state 字典中，前端将从这里读取
                    if isinstance(state, dict):
                        state['company_name'] = stock_name
                except Exception as e:
                    logger.error(f"为 {stock_code} 获取公司名称时出错: {e}")
                    if isinstance(state, dict):
                        state['company_name'] = '名称获取失败'
                
                task_manager.update_task(task_id, status=TaskStatus.COMPLETED, progress=100, result={'decision': decision, 'final_state': state, 'current_step': '分析完成'})
                logger.info(f"智能体分析任务 {task_id} 完成")

            except TaskCancelledException as e:
                logger.info(str(e))
                task_manager.update_task(task_id, status=TaskStatus.FAILED, error='任务已被用户取消', result={'current_step': '任务已被用户取消'})
            except Exception as e:
                logger.error(f"智能体分析任务 {task_id} 失败: {str(e)}")
                logger.error(traceback.format_exc())
                task_manager.update_task(task_id, status=TaskStatus.FAILED, error=str(e), result={'current_step': f'分析失败: {e}'})

        thread = threading.Thread(target=run_agent_analysis)
        thread.daemon = True
        thread.start()

        return {
            'task_id': task_id,
            'status': 'pending',
            'message': f'已启动对 {stock_code} 的智能体分析'
        }

    except Exception as e:
        logger.error(f"启动智能体分析时出错: {traceback.format_exc()}")
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR




@agent_analysis_bp.route('/agent_analysis_history', methods=['GET'])
@inject
def get_agent_analysis_history(task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """获取已完成的智能体分析任务历史"""
    try:
        all_tasks = task_manager.get_all_tasks()
        history = [
            task for task in all_tasks 
            if task.get('status') in [TaskStatus.COMPLETED, TaskStatus.FAILED]
        ]
        # 按更新时间排序，最新的在前
        history.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        return custom_jsonify({'history': history})
    except Exception as e:
        logger.error(f"获取分析历史时出错: {traceback.format_exc()}")
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@agent_analysis_bp.route('/agent_analysis_status/<task_id>', methods=['GET'])
@inject
def get_agent_analysis_status(task_id, task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """获取智能体分析任务的状态"""
    task = task_manager.get_task(task_id)

    if not task:
        return {'error': '找不到指定的智能体分析任务'}, status.HTTP_404_NOT_FOUND
    
    # 准备要返回的数据
    response_data = {
        'id': task['id'],
        'status': task['status'],
        'progress': task.get('progress', 0),
        'created_at': task['created_at'],
        'updated_at': task['updated_at'],
        'params': task.get('params', {})
    }
    
    if 'result' in task:
         response_data['result'] = task['result']
    if 'error' in task:
         response_data['error'] = task['error']
         
    return custom_jsonify(response_data)    





@agent_analysis_bp.route('/delete_agent_analysis', methods=['POST'])
@inject
def _delete_agent_analysis(task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """Cancel and/or delete one or more agent analysis tasks."""
    try:
        data = request.data
        task_ids = data.get('task_ids', [])
        if not isinstance(task_ids, list):
            return {'error': 'task_ids 必须是一个列表'}, status.HTTP_400_BAD_REQUEST

        if not task_ids:
            return {'error': '请提供要删除的任务ID'}, status.HTTP_400_BAD_REQUEST

        deleted_count = 0
        cancelled_count = 0
        
        for task_id in task_ids:
            task = task_manager.get_task(task_id)
            if not task:
                logger.warning(f"尝试删除一个不存在的任务: {task_id}")
                continue

            # If the task is running, mark it as cancelled
            if task.get('status') == TaskStatus.RUNNING:
                task['status'] = TaskStatus.CANCELLED
                task['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                task['error'] = '任务已被用户取消'
                task_manager.update_task(task_id, status=TaskStatus.CANCELLED, error='任务已被用户取消')
                cancelled_count += 1
                logger.info(f"任务 {task_id} 已被标记为取消。")
            
            # For all other states (or after cancelling), delete the task file
            if task_manager.delete_task(task_id):
                deleted_count += 1
        
        message = f"请求处理 {len(task_ids)} 个任务。已取消 {cancelled_count} 个运行中的任务，并删除了 {deleted_count} 个任务文件。"
        logger.info(message)
        return {'success': True, 'message': message}

    except Exception as e:
        logger.error(f"删除分析历史时出错: {traceback.format_exc()}")
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

