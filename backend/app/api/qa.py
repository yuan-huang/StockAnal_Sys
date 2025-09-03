from flask_api import APIBlueprint, request, status
from app.analysis.stock_qa import StockQA
from app.analysis._analysis_container import AnalysisContainer
from . import api_blueprint
from dependency_injector.wiring import inject, Provide
import logging
logger = logging.getLogger(__name__)



# QA
@api_blueprint.route('/qa', methods=['POST'])
@inject
def api_qa(stock_qa: StockQA = Provide[AnalysisContainer.stock_qa]):
    try:
        data = request.data
        stock_code = data.get('stock_code')
        question = data.get('question')
        market_type = data.get('market_type', 'A')
        if not stock_code or not question:
            return {'error': '请提供股票代码和问题'}, status.HTTP_400_BAD_REQUEST
        result = stock_qa.answer_question(stock_code, question, market_type)
        return result
    except Exception as e:
        logger.error(f"智能问答出错: {e}", exc_info=True)
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR