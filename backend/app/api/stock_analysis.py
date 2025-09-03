# -*- coding: utf-8 -*-
"""
股票分析API接口
包含股票分析、增强分析等接口
"""

from flask_api import request, status
import time
import logging
import traceback
from app.analysis.stock_analyzer import StockAnalyzer
from app.analysis.task_manager import TaskStatus, TaskManager
from app.analysis._analysis_container import AnalysisContainer
from dependency_injector.wiring import inject, Provide
from app.web.utils import custom_jsonify
from app.core.cache import Cache
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from . import api_blueprint

logger = logging.getLogger(__name__)

# Stock Analysis Task
@api_blueprint.route('/start_stock_analysis', methods=['POST'])
@inject
def start_stock_analysis(analyzer: StockAnalyzer = Provide[AnalysisContainer.stock_analyzer], task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """Starts an asynchronous stock analysis task."""
    try:
        data = request.data
        stock_code = data.get('stock_code')
        market_type = data.get('market_type', 'A')

        if not stock_code:
            return {'error': 'Stock code is required'}, status.HTTP_400_BAD_REQUEST

        task_params = {'stock_code': stock_code, 'market_type': market_type}
        task = task_manager.create_task(name=f"Analysis for {stock_code}", params=task_params)
        task_id = task['id']

        try:
            task_manager.update_task(task_id, status=TaskStatus.RUNNING, progress=10)
            result = analyzer.perform_enhanced_analysis(stock_code, market_type)
            task_manager.update_task(task_id, status=TaskStatus.COMPLETED, progress=100, result=result)
            logger.info(f"Analysis task {task_id} completed for {stock_code}")
        except Exception as e:
            logger.error(f"Analysis task {task_id} failed: {e}", exc_info=True)
            task_manager.update_task(task_id, status=TaskStatus.FAILED, error=str(e))


        return {'task_id': task_id}, status.HTTP_202_ACCEPTED
    except Exception as e:
        logger.error(f"Failed to start stock analysis task: {e}", exc_info=True)
        return {'error': 'Internal server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR



@api_blueprint.route('/stock_data', methods=['GET'])
@inject
def get_stock_analysis_data(analyzer: StockAnalyzer = Provide[AnalysisContainer.stock_analyzer], cache: Cache = Provide[AnalysisContainer.cache]):
    try:
        stock_code = request.args.get('stock_code')
        market_type = request.args.get('market_type', 'A')
        period = request.args.get('period', '1y')

        if not stock_code:
            return custom_jsonify({'error': '请提供股票代码'}), status.HTTP_400_BAD_REQUEST

        end_date = datetime.now().strftime('%Y%m%d')
        days_map = {'1m': 30, '3m': 90, '6m': 180, '1y': 365}
        start_date = (datetime.now() - timedelta(days=days_map.get(period, 365))).strftime('%Y%m%d')

        df = analyzer.get_stock_data(stock_code, market_type, start_date, end_date)

        if df.empty:
            return custom_jsonify({'error': '未找到股票数据'}), status.HTTP_404_NOT_FOUND

        df = analyzer.calculate_indicators(df)
        
        if 'date' in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df['date']):
                df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            else:
                df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

        df = df.replace({np.nan: None, np.inf: None, -np.inf: None})
        records = df.to_dict('records')
        
        return custom_jsonify({'data': records})
    except Exception as e:
        logger.error(f"获取股票数据时出错: {e}", exc_info=True)
        return custom_jsonify({'error': str(e)}), status.HTTP_500_INTERNAL_SERVER_ERROR





# # 创建蓝图
@api_blueprint.route('/analyze', methods=['POST'])
@inject
def stock_analyze(stock_analyzer: StockAnalyzer = Provide[AnalysisContainer.stock_analyzer]):
    try:
        data = request.data
        stock_codes = data.get('stock_codes', [])
        market_type = data.get('market_type', 'A')

        if not stock_codes:
            return {'error': '请输入代码'}, status.HTTP_400_BAD_REQUEST

        logger.info(f"分析股票请求: {stock_codes}, 市场类型: {market_type}")

        # 设置最大处理时间，每只股票10秒
        max_time_per_stock = 10  # 秒
        max_total_time = max(30, min(60, len(stock_codes) * max_time_per_stock))  # 至少30秒，最多60秒

        start_time = time.time()
        results = []

        for stock_code in stock_codes:
            try:
                # 检查是否已超时
                if time.time() - start_time > max_total_time:
                    logger.warning(f"分析股票请求已超过{max_total_time}秒，提前返回已处理的{len(results)}只股票")
                    break

                # 使用线程本地缓存的分析器实例
                result = stock_analyzer.quick_analyze_stock(stock_code.strip(), market_type)

                logger.info(
                    f"分析结果: 股票={stock_code}, 名称={result.get('stock_name', '未知')}, 行业={result.get('industry', '未知')}")
                results.append(result)
            except Exception as e:
                logger.error(f"分析股票 {stock_code} 时出错: {str(e)}")
                results.append({
                    'stock_code': stock_code,
                    'error': str(e),
                    'stock_name': '分析失败',
                    'industry': '未知'
                })

        return {'results': results}
    except Exception as e:
        logger.error(f"分析股票时出错: {traceback.format_exc()}")
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
    




@api_blueprint.route('/enhanced_analysis', methods=['POST'])
@inject
def enhanced_analysis(analyzer: StockAnalyzer = Provide[AnalysisContainer.stock_analyzer]):
    """原增强分析API的向后兼容版本 - 功能重构中"""
    try:
        data = request.data
        stock_code = data.get('stock_code')
        market_type = data.get('market_type', 'A')

        if not stock_code:
            return {'error': '请输入股票代码'}, status.HTTP_400_BAD_REQUEST

        # 暂时使用基础分析功能
        try:
            result = analyzer.quick_analyze_stock(stock_code, market_type)
            logging.info(f"基础分析完成: {stock_code}")
            return {'result': result}
        except Exception as e:
            logging.error(f"分析过程中出错: {str(e)}")
            return {'error': f'分析过程中出错: {str(e)}'}, status.HTTP_500_INTERNAL_SERVER_ERROR

    except Exception as e:
        logging.error(f"执行分析时出错: {traceback.format_exc()}")
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR 
    





# Scenario Prediction
@api_blueprint.route('/scenario_predict', methods=['POST'])
@inject
def api_scenario_predict(scenario_predictor: ScenarioPredictor = Provide[AnalysisContainer.scenario_predictor]):
    """股票预测"""
    try:
        data = request.data
        stock_code = data.get('stock_code')
        market_type = data.get('market_type', 'A')
        days = data.get('days', 60)
        if not stock_code:
            return {'error': '请提供股票代码'}, status.HTTP_400_BAD_REQUEST
        result = scenario_predictor.generate_scenarios(stock_code, market_type, days)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"情景预测出错: {e}", exc_info=True)
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

