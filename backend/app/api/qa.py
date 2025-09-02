from flask import jsonify, request
from app.analysis.stock_qa import StockQA
from app.analysis._analysis_container import AnalysisContainer
from app.web.api import api_blueprint
from dependency_injector.wiring import inject, Provide
import logging
logger = logging.getLogger(__name__)



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
        return result
    except Exception as e:
        logger.error(f"智能问答出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500