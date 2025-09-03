# -*- coding: utf-8 -*-
"""
美股相关API接口
包含美股搜索等接口
"""

from flask_api import APIBlueprint, request, status
import logging
from app.analysis.us_stock_service import USStockService

# 创建蓝图
us_stocks_blueprint = APIBlueprint('us_stocks', __name__)

# 创建美股服务实例
us_stock_service = USStockService()

@us_stocks_blueprint.route('/search_us_stocks', methods=['GET'])
def search_us_stocks():
    """搜索美股代码"""
    try:
        keyword = request.args.get('keyword', '')
        if not keyword:
            return {'error': '请输入搜索关键词'}, status.HTTP_400_BAD_REQUEST

        results = us_stock_service.search_us_stocks(keyword)
        return {'results': results}

    except Exception as e:
        logging.error(f"搜索美股代码时出错: {str(e)}")
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR 