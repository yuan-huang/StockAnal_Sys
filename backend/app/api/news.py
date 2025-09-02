from flask import jsonify, request
from app.analysis.news_fetcher import NewsFetcher
from app.analysis._analysis_container import AnalysisContainer
from app.web.api import api_blueprint
from dependency_injector.wiring import inject, Provide
import logging
logger = logging.getLogger(__name__)        
    


@api_blueprint.route('/latest_news', methods=['GET'])
@inject
def get_latest_news(news_fetcher: NewsFetcher = Provide[AnalysisContainer.news_fetcher]):
    try:
        days = int(request.args.get('days', 1))
        limit = int(request.args.get('limit', 1000))
        source = request.args.get('source', 'cls')
        
        news_data = news_fetcher.get_latest_news(days=days, limit=limit, source=source)
        
        return jsonify({'success': True, 'news': news_data})
    except Exception as e:
        logger.error(f"获取最新新闻数据时出错: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500