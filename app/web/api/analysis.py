# app/web/api/analysis.py
from flask import request, jsonify, current_app
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
from app.analysis.task_manager import TaskManager
from app.analysis.task_manager import TaskStatus
from app.analysis.stock_analyzer import StockAnalyzer
import logging
import traceback
import time
from datetime import datetime

logger = logging.getLogger(__name__)

# Fundamental Analysis
@api_blueprint.route('/fundamental_analysis', methods=['POST'])
@inject
def api_fundamental_analysis(fundamental_analyzer: FundamentalAnalyzer = Provide[AnalysisContainer.fundamental_analyzer]):
    try:
        data = request.json
        stock_code = data.get('stock_code')
        if not stock_code:
            return jsonify({'error': '请提供股票代码'}), 400
        result = fundamental_analyzer.calculate_fundamental_score(stock_code)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"基本面分析出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# Capital Flow Analysis
@api_blueprint.route('/concept_fund_flow', methods=['GET'])
@inject
def api_concept_fund_flow(capital_flow_analyzer: CapitalFlowAnalyzer = Provide[AnalysisContainer.capital_flow_analyzer]):
    try:
        period = request.args.get('period', '10日排行')
        result = capital_flow_analyzer.get_concept_fund_flow(period)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error getting concept fund flow: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/individual_fund_flow_rank', methods=['GET'])
@inject
def api_individual_fund_flow_rank(capital_flow_analyzer: CapitalFlowAnalyzer = Provide[AnalysisContainer.capital_flow_analyzer]):
    try:
        period = request.args.get('period', '10日')
        result = capital_flow_analyzer.get_individual_fund_flow_rank(period)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error getting individual fund flow ranking: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/individual_fund_flow', methods=['GET'])
@inject
def api_individual_fund_flow(capital_flow_analyzer: CapitalFlowAnalyzer = Provide[AnalysisContainer.capital_flow_analyzer]):
    try:
        stock_code = request.args.get('stock_code')
        market_type = request.args.get('market_type', '')
        re_date = request.args.get('period-select')
        if not stock_code:
            return jsonify({'error': 'Stock code is required'}), 400
        result = capital_flow_analyzer.get_individual_fund_flow(stock_code, market_type, re_date)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error getting individual fund flow: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/sector_stocks', methods=['GET'])
@inject
def api_sector_stocks(capital_flow_analyzer: CapitalFlowAnalyzer = Provide[AnalysisContainer.capital_flow_analyzer]):
    try:
        sector = request.args.get('sector')
        if not sector:
            return jsonify({'error': 'Sector name is required'}), 400
        result = capital_flow_analyzer.get_sector_stocks(sector)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error getting sector stocks: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/capital_flow', methods=['POST'])
@inject
def api_capital_flow(capital_flow_analyzer: CapitalFlowAnalyzer = Provide[AnalysisContainer.capital_flow_analyzer]):
    try:
        data = request.json
        stock_code = data.get('stock_code')
        market_type = data.get('market_type', '')
        if not stock_code:
            return jsonify({'error': 'Stock code is required'}), 400
        result = capital_flow_analyzer.calculate_capital_flow_score(stock_code, market_type)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error calculating capital flow score: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# Scenario Prediction
@api_blueprint.route('/scenario_predict', methods=['POST'])
@inject
def api_scenario_predict(scenario_predictor: ScenarioPredictor = Provide[AnalysisContainer.scenario_predictor]):
    try:
        data = request.json
        stock_code = data.get('stock_code')
        market_type = data.get('market_type', 'A')
        days = data.get('days', 60)
        if not stock_code:
            return jsonify({'error': '请提供股票代码'}), 400
        result = scenario_predictor.generate_scenarios(stock_code, market_type, days)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"情景预测出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500



# Risk Analysis
@api_blueprint.route('/risk_analysis', methods=['POST'])
@inject
def api_risk_analysis(risk_monitor: RiskMonitor = Provide[AnalysisContainer.risk_monitor]):
    try:
        data = request.json
        stock_code = data.get('stock_code')
        market_type = data.get('market_type', 'A')
        if not stock_code:
            return jsonify({'error': '请提供股票代码'}), 400
        result = risk_monitor.analyze_stock_risk(stock_code, market_type)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"风险分析出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/portfolio_risk', methods=['POST'])
@inject
def api_portfolio_risk(risk_monitor: RiskMonitor = Provide[AnalysisContainer.risk_monitor]):
    try:
        data = request.json
        portfolio = data.get('portfolio', [])
        if not portfolio:
            return jsonify({'error': '请提供投资组合'}), 400
        result = risk_monitor.analyze_portfolio_risk(portfolio)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"投资组合风险分析出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# Index and Industry Analysis
@api_blueprint.route('/index_analysis', methods=['GET'])
@inject
def api_index_analysis(index_industry_analyzer: IndexIndustryAnalyzer = Provide[AnalysisContainer.index_industry_analyzer]):
    try:
        index_code = request.args.get('index_code')
        limit = int(request.args.get('limit', 30))
        if not index_code:
            return jsonify({'error': '请提供指数代码'}), 400
        result = index_industry_analyzer.analyze_index(index_code, limit)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"指数分析出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/industry_analysis', methods=['GET'])
@inject
def api_industry_analysis(index_industry_analyzer: IndexIndustryAnalyzer = Provide[AnalysisContainer.index_industry_analyzer]):
    try:
        industry = request.args.get('industry')
        limit = int(request.args.get('limit', 30))
        if not industry:
            return jsonify({'error': '请提供行业名称'}), 400
        result = index_industry_analyzer.analyze_industry(industry, limit)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"行业分析出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500
        
@api_blueprint.route('/industry_fund_flow', methods=['GET'])
@inject
def api_industry_fund_flow(industry_analyzer: IndustryAnalyzer = Provide[AnalysisContainer.industry_analyzer]):
    try:
        symbol = request.args.get('symbol', '即时')
        result = industry_analyzer.get_industry_fund_flow(symbol)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"获取行业资金流向数据出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/industry_detail', methods=['GET'])
@inject
def api_industry_detail(industry_analyzer: IndustryAnalyzer = Provide[AnalysisContainer.industry_analyzer]):
    try:
        industry = request.args.get('industry')
        if not industry:
            return jsonify({'error': '请提供行业名称'}), 400
        result = industry_analyzer.get_industry_detail(industry)
        if not result:
            return jsonify({'error': f'未找到行业 {industry} 的详细信息'}), 404
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"获取行业详细信息出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/industry_compare', methods=['GET'])
@inject
def api_industry_compare(index_industry_analyzer: IndexIndustryAnalyzer = Provide[AnalysisContainer.index_industry_analyzer]):
    try:
        limit = int(request.args.get('limit', 10))
        result = index_industry_analyzer.compare_industries(limit)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"行业比较出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500




@api_blueprint.route('/agent_analysis_history', methods=['GET'])
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
        return jsonify({'error': str(e)}), 500
    


@api_blueprint.route('/agent_analysis_status/<task_id>', methods=['GET'])
@inject
def get_agent_analysis_status(task_id, task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """获取智能体分析任务的状态"""
    task = task_manager.get_task(task_id)

    if not task:
        return jsonify({'error': '找不到指定的智能体分析任务'}), 404
    
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


@api_blueprint.route('/analysis_status/<task_id>', methods=['GET'])
@inject
def get_analysis_status(task_id, task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """获取个股分析任务状态"""
    task = task_manager.get_task(task_id)
    if not task:
        return jsonify({'error': '找不到指定的分析任务'}), 404

    # 基本状态信息
    status = {
        'id': task['id'],
        'status': task['status'],
        'progress': task.get('progress', 0),
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


@api_blueprint.route('/cancel_analysis/<task_id>', methods=['POST'])
@inject
def cancel_analysis(task_id, task_manager: TaskManager = Provide[AnalysisContainer.task_manager]):
    """取消个股分析任务"""
    task = task_manager.get_task(task_id)
    if not task:
        return jsonify({'error': '找不到指定的分析任务'}), 404

    if task['status'] in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
        return jsonify({'message': '任务已完成或失败，无法取消'})

    # 更新状态为失败
    task['status'] = TaskStatus.FAILED
    task['error'] = '用户取消任务'
    task['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 更新键索引的任务
    if 'key' in task and task['key'] in task_manager.get_all_tasks():
        task_manager.get_all_tasks()[task['key']] = task

    return jsonify({'message': '任务已取消'})