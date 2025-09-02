# app/web/api/tasks.py
from flask import request, jsonify, current_app
from . import api_blueprint
from app.analysis.task_manager import TaskStatus, TaskManager
from app.analysis.etf_analyzer import EtfAnalyzer   
from app.web.utils import custom_jsonify
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dependency_injector.wiring import inject
from app.analysis._analysis_container import AnalysisContainer
from dependency_injector.wiring import Provide
from app.analysis.stock_analyzer import StockAnalyzer
import logging
import traceback
logger = logging.getLogger(__name__)

from datetime import datetime

# Generic Task Endpoints
@api_blueprint.route('/tasks', methods=['GET'])
@inject
def get_tasks(task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """Lists all tasks."""
    return custom_jsonify(task_manager.get_all_tasks())

@api_blueprint.route('/tasks/<task_id>', methods=['GET'])
@inject
def get_task(task_id, task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """Gets a single task by its ID."""
    task = task_manager.get_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return custom_jsonify(task)

@api_blueprint.route('/tasks/<task_id>', methods=['DELETE'])
@inject
def delete_task(task_id, task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """Deletes a task."""
    if task_manager.delete_task(task_id):
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404



@api_blueprint.route('/active_tasks', methods=['GET'])
@inject
def get_active_tasks(task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """获取所有正在进行的智能体分析任务"""
    try:
        all_tasks = task_manager.get_all_tasks()
        active_tasks_list = []
        for task in all_tasks:
            if task.get('status') == TaskStatus.RUNNING:
                task_info = {
                    'task_id': task['id'],
                    'stock_code': task.get('params', {}).get('stock_code', ''),
                    'progress': task.get('progress', 0),
                    'current_step': (task.get('result') or {}).get('current_step', '加载中...'),
                }
                active_tasks_list.append(task_info)
        # 按创建时间排序，最新的在前
        active_tasks_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return custom_jsonify({'active_tasks': active_tasks_list})
    except Exception as e:
        logger.error(f"获取活动任务时出错: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500
    


# Market Scan Task
@api_blueprint.route('/start_market_scan', methods=['POST'])
@inject
def start_market_scan(analyzer: StockAnalyzer = Provide[AnalysisContainer.stock_analyzer], task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """Starts an asynchronous market scan task."""
    try:
        data = request.json
        stock_list = data.get('stock_list', [])
        min_score = data.get('min_score', 60)
        market_type = data.get('market_type', 'A')

        if not stock_list:
            return jsonify({'error': 'Stock list is required'}), 400

        if len(stock_list) > 100:
            logger.warning(f"Stock list too long ({len(stock_list)}), truncating to 100.")
            stock_list = stock_list[:100]

        task_params = {'stock_list_count': len(stock_list), 'min_score': min_score, 'market_type': market_type}
        task = task_manager.create_task(name="Market Scan", params=task_params)
        task_id = task['id']

        def run_scan():
            try:
                task_manager.update_task(task_id, status=TaskStatus.RUNNING, progress=0)
                
                results = []
                total = len(stock_list)
                completed_count = 0
                
                with ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_stock = {executor.submit(analyzer.quick_analyze_stock, code, market_type): code for code in stock_list}
                    
                    for future in as_completed(future_to_stock):
                        stock_code = future_to_stock[future]
                        try:
                            report = future.result()
                            if report and report.get('score', 0) >= min_score:
                                results.append(report)
                        except Exception as exc:
                            logger.error(f'Error analyzing {stock_code} in market scan: {exc}')
                        
                        completed_count += 1
                        progress = int((completed_count / total) * 100)
                        task_manager.update_task(task_id, progress=progress)

                results.sort(key=lambda x: x['score'], reverse=True)
                task_manager.update_task(task_id, status=TaskStatus.COMPLETED, progress=100, result=results)
                logger.info(f"Market scan task {task_id} completed, found {len(results)} matching stocks.")

            except Exception as e:
                logger.error(f"Market scan task {task_id} failed: {e}", exc_info=True)
                task_manager.update_task(task_id, status=TaskStatus.FAILED, error=str(e))

        thread = threading.Thread(target=run_scan, daemon=True)
        thread.start()

        return jsonify({'task_id': task_id}), 202
    except Exception as e:
        logger.error(f"Failed to start market scan task: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500




# ETF Analysis Task
@api_blueprint.route('/start_etf_analysis', methods=['POST'])
@inject
def start_etf_analysis(stock_analyzer = Provide[AnalysisContainer.stock_analyzer], task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """Starts an asynchronous ETF analysis task."""
    try:
        data = request.json
        etf_code = data.get('etf_code')
        market_type = data.get('market_type', 'A')
        period = data.get('period', '1y')

        if not etf_code:
            return jsonify({'error': 'ETF code is required'}), 400

        task_params = {'etf_code': etf_code, 'market_type': market_type, 'period': period}
        task = task_manager.create_task(name=f"ETF Analysis for {etf_code}", params=task_params)
        task_id = task['id']

        def run_etf_analysis():
            try:
                task_manager.update_task(task_id, status=TaskStatus.RUNNING, progress=10)
                # 使用工厂创建EtfAnalyzer实例
                etf_analyzer_instance = EtfAnalyzer(etf_code, stock_analyzer, market_type, period)
                result = etf_analyzer_instance.run_analysis()
                task_manager.update_task(task_id, status=TaskStatus.COMPLETED, progress=100, result=result)
                logger.info(f"ETF analysis task {task_id} completed for {etf_code}")
            except Exception as e:
                logger.error(f"ETF analysis task {task_id} failed: {e}", exc_info=True)
                task_manager.update_task(task_id, status=TaskStatus.FAILED, error=str(e))

        thread = threading.Thread(target=run_etf_analysis, daemon=True)
        thread.start()

        return jsonify({'task_id': task_id}), 202
    except Exception as e:
        logger.error(f"Failed to start ETF analysis task: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500




@api_blueprint.route('/etf_analysis_status/<task_id>', methods=['GET'])
@inject
def get_etf_analysis_status(task_id, task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """获取ETF分析任务状态"""
    task = task_manager.get_task(task_id)
    if not task:
        return jsonify({'error': '找不到指定的ETF分析任务'}), 404

    status = {
        'id': task['id'],
        'status': task['status'],
        'progress': task.get('progress', 0),
        'created_at': task['created_at'],
        'updated_at': task['updated_at']
    }

    if task['status'] == TaskStatus.COMPLETED and 'result' in task:
        status['result'] = task['result']
    
    if task['status'] == TaskStatus.FAILED and 'error' in task:
        status['error'] = task['error']

    return custom_jsonify(status)



@api_blueprint.route('/scan_status/<task_id>', methods=['GET'])
@inject
def get_scan_status(task_id, task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """获取扫描任务状态"""
    task = task_manager.get_task(task_id)

    # 基本状态信息
    status = {
        'id': task['id'],
        'status': task['status'],
        'progress': task.get('progress', 0),
        'total': task.get('total', 0),
        'created_at': task['created_at'],
        'updated_at': task['updated_at']
    }

    # 如果任务完成，包含结果
    if task['status'] == TaskStatus.COMPLETED and 'result' in task:
        status['result'] = task['result']

    # 如果任务失败，包含错误信息
    if task['status'] == TaskStatus.FAILED and 'error' in task:
        status['error'] = task['error']

    return custom_jsonify(status)


@api_blueprint.route('/cancel_scan/<task_id>', methods=['POST'])
@inject
def cancel_scan(task_id, task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """取消扫描任务"""
    if task_id not in task_manager.get_all_tasks():
        return jsonify({'error': '找不到指定的扫描任务'}), 404

    task = task_manager.get_task(task_id)

    if task['status'] in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
        return jsonify({'message': '任务已完成或失败，无法取消'})

    # 更新状态为失败
    task['status'] = TaskStatus.FAILED
    task['error'] = '用户取消任务'
    task['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return jsonify({'message': '任务已取消'})







