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

# QA
@api_blueprint.route('/qa', methods=['POST'])
@inject
def api_qa(stock_qa: StockQA = Provide[AnalysisContainer.stock_qa]):
    try:
        data = request.json
        stock_code = data.get('stock_code')
        question = data.get('question')
        market_type = data.get('market_type', 'A')
        if not stock_code or not question:
            return jsonify({'error': '请提供股票代码和问题'}), 400
        result = stock_qa.answer_question(stock_code, question, market_type)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"智能问答出错: {e}", exc_info=True)
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
