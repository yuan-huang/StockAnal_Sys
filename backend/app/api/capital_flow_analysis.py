"""
资金流分析

资金流向API接口
包含北向资金历史数据等接口
"""

from flask_api import APIBlueprint, request, status
from app.web.api import api_blueprint
from datetime import datetime, timedelta
import traceback
import logging
from dependency_injector.wiring import inject

logger = logging.getLogger(__name__)

# 创建蓝图
capital_flow_analysis_bp = Blueprint('capital_flow_analysis', __name__, url_prefix='/capital_flow_analysis')

@capital_flow_blueprint.route('/north_flow_history', methods=['POST'])
@inject
def api_north_flow_history():
    """获取北向资金历史数据"""
    try:
        data = request.data
        stock_code = data.get('stock_code')
        days = data.get('days', 10)  # 默认为10天，对应前端的默认选项

        # 计算 end_date 为当前时间
        end_date = datetime.now().strftime('%Y%m%d')

        # 计算 start_date 为 end_date 减去指定的天数
        start_date = (datetime.now() - timedelta(days=int(days))).strftime('%Y%m%d')

        if not stock_code:
            return {'error': '请提供股票代码'}, status.HTTP_400_BAD_REQUEST

        # 调用北向资金历史数据方法

        # 暂时注释掉这个功能，因为方法不存在
        # analyzer = CapitalFlowAnalyzer()
        # result = analyzer.get_north_flow_history(stock_code, start_date, end_date)
        
        # 返回暂时不可用的提示
        return {'error': '北向资金历史数据功能正在重构中，暂时不可用'}, status.HTTP_503_SERVICE_UNAVAILABLE
    except Exception as e:
        logger.error(f"获取北向资金历史数据出错: {traceback.format_exc()}")
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR 
    

# Capital Flow Analysis
@capital_flow_analysis_bp.route('/concept_fund_flow', methods=['GET'])
@inject
def api_concept_fund_flow(capital_flow_analyzer: CapitalFlowAnalyzer = Provide[AnalysisContainer.capital_flow_analyzer]):
    try:
        period = request.args.get('period', '10日排行')
        result = capital_flow_analyzer.get_concept_fund_flow(period)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error getting concept fund flow: {e}", exc_info=True)
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR




@api_blueprint.route('/capital_flow', methods=['POST'])
@inject
def api_capital_flow(capital_flow_analyzer: CapitalFlowAnalyzer = Provide[AnalysisContainer.capital_flow_analyzer]):
    try:
        data = request.json
        stock_code = data.get('stock_code')
        market_type = data.get('market_type', '')
        if not stock_code:
            return {'error': 'Stock code is required'}, status.HTTP_400_BAD_REQUEST
        result = capital_flow_analyzer.calculate_capital_flow_score(stock_code, market_type)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error calculating capital flow score: {e}", exc_info=True)
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR



@api_blueprint.route('/individual_fund_flow_rank', methods=['GET'])
@inject
def api_individual_fund_flow_rank(capital_flow_analyzer: CapitalFlowAnalyzer = Provide[AnalysisContainer.capital_flow_analyzer]):
    try:
        period = request.args.get('period', '10日')
        result = capital_flow_analyzer.get_individual_fund_flow_rank(period)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error getting individual fund flow ranking: {e}", exc_info=True)
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

@api_blueprint.route('/individual_fund_flow', methods=['GET'])
@inject
def api_individual_fund_flow(capital_flow_analyzer: CapitalFlowAnalyzer = Provide[AnalysisContainer.capital_flow_analyzer]):
    try:
        stock_code = request.args.get('stock_code')
        market_type = request.args.get('market_type', '')
        re_date = request.args.get('period-select')
        if not stock_code:
            return {'error': 'Stock code is required'}, status.HTTP_400_BAD_REQUEST
        result = capital_flow_analyzer.get_individual_fund_flow(stock_code, market_type, re_date)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error getting individual fund flow: {e}", exc_info=True)
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


