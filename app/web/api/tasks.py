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

# Stock Analysis Task
@api_blueprint.route('/start_stock_analysis', methods=['POST'])
@inject
def start_stock_analysis(analyzer: StockAnalyzer = Provide[AnalysisContainer.stock_analyzer], task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """Starts an asynchronous stock analysis task."""
    try:
        data = request.json
        stock_code = data.get('stock_code')
        market_type = data.get('market_type', 'A')

        if not stock_code:
            return jsonify({'error': 'Stock code is required'}), 400

        task_params = {'stock_code': stock_code, 'market_type': market_type}
        task = task_manager.create_task(name=f"Analysis for {stock_code}", params=task_params)
        task_id = task['id']

        def run_analysis():
            try:
                task_manager.update_task(task_id, status=TaskStatus.RUNNING, progress=10)
                result = analyzer.perform_enhanced_analysis(stock_code, market_type)
                task_manager.update_task(task_id, status=TaskStatus.COMPLETED, progress=100, result=result)
                current_app.logger.info(f"Analysis task {task_id} completed for {stock_code}")
            except Exception as e:
                current_app.logger.error(f"Analysis task {task_id} failed: {e}", exc_info=True)
                task_manager.update_task(task_id, status=TaskStatus.FAILED, error=str(e))

        thread = threading.Thread(target=run_analysis, daemon=True)
        thread.start()

        return jsonify({'task_id': task_id}), 202
    except Exception as e:
        current_app.logger.error(f"Failed to start stock analysis task: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

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
            current_app.logger.warning(f"Stock list too long ({len(stock_list)}), truncating to 100.")
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
                            current_app.logger.error(f'Error analyzing {stock_code} in market scan: {exc}')
                        
                        completed_count += 1
                        progress = int((completed_count / total) * 100)
                        task_manager.update_task(task_id, progress=progress)

                results.sort(key=lambda x: x['score'], reverse=True)
                task_manager.update_task(task_id, status=TaskStatus.COMPLETED, progress=100, result=results)
                current_app.logger.info(f"Market scan task {task_id} completed, found {len(results)} matching stocks.")

            except Exception as e:
                current_app.logger.error(f"Market scan task {task_id} failed: {e}", exc_info=True)
                task_manager.update_task(task_id, status=TaskStatus.FAILED, error=str(e))

        thread = threading.Thread(target=run_scan, daemon=True)
        thread.start()

        return jsonify({'task_id': task_id}), 202
    except Exception as e:
        current_app.logger.error(f"Failed to start market scan task: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

# ETF Analysis Task
@api_blueprint.route('/start_etf_analysis', methods=['POST'])
@inject
def start_etf_analysis(etf_analyzer: EtfAnalyzer = Provide[AnalysisContainer.etf_analyzer], task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
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
                etf_analyzer_instance = EtfAnalyzer(etf_code, analyzer, market_type, period)
                result = etf_analyzer_instance.run_analysis()
                task_manager.update_task(task_id, status=TaskStatus.COMPLETED, progress=100, result=result)
                current_app.logger.info(f"ETF analysis task {task_id} completed for {etf_code}")
            except Exception as e:
                current_app.logger.error(f"ETF analysis task {task_id} failed: {e}", exc_info=True)
                task_manager.update_task(task_id, status=TaskStatus.FAILED, error=str(e))

        thread = threading.Thread(target=run_etf_analysis, daemon=True)
        thread.start()

        return jsonify({'task_id': task_id}), 202
    except Exception as e:
        current_app.logger.error(f"Failed to start ETF analysis task: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
