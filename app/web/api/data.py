# app/web/api/data.py
from flask import request, jsonify
from . import api_blueprint
from app.web.web_server import analyzer, app, cache # app and cache are still needed here
from app.web.utils import custom_jsonify
import akshare as ak
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

@api_blueprint.route('/stock_data', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_stock_data():
    try:
        stock_code = request.args.get('stock_code')
        market_type = request.args.get('market_type', 'A')
        period = request.args.get('period', '1y')

        if not stock_code:
            return custom_jsonify({'error': '请提供股票代码'}), 400

        end_date = datetime.now().strftime('%Y%m%d')
        days_map = {'1m': 30, '3m': 90, '6m': 180, '1y': 365}
        start_date = (datetime.now() - timedelta(days=days_map.get(period, 365))).strftime('%Y%m%d')

        df = analyzer.get_stock_data(stock_code, market_type, start_date, end_date)

        if df.empty:
            return custom_jsonify({'error': '未找到股票数据'}), 404

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
        app.logger.error(f"获取股票数据时出错: {e}", exc_info=True)
        return custom_jsonify({'error': str(e)}), 500

@api_blueprint.route('/index_stocks', methods=['GET'])
def get_index_stocks():
    try:
        index_code = request.args.get('index_code', '000300')
        
        index_map = {
            '000300': "000300",
            '000905': "000905",
            '000852': "000852",
            '000001': "000001"
        }
        
        symbol = index_map.get(index_code)
        if not symbol:
            return jsonify({'error': '不支持的指数代码'}), 400
            
        stocks = ak.index_stock_cons_weight_csindex(symbol=symbol)
        stock_list = stocks['成分券代码'].tolist() if '成分券代码' in stocks.columns else []
        
        return jsonify({'stock_list': stock_list})
    except Exception as e:
        app.logger.error(f"获取指数成分股时出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/industry_stocks', methods=['GET'])
def get_industry_stocks():
    try:
        industry = request.args.get('industry')
        if not industry:
            return jsonify({'error': '请提供行业名称'}), 400
        
        stocks = ak.stock_board_industry_cons_em(symbol=industry)
        stock_list = stocks['代码'].tolist() if '代码' in stocks.columns else []

        return jsonify({'stock_list': stock_list})
    except Exception as e:
        app.logger.error(f"获取行业成分股时出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/latest_news', methods=['GET'])
def get_latest_news():
    try:
        # This endpoint is kept simple as it delegates to the news_fetcher module
        from app.analysis.news_fetcher import news_fetcher
        days = int(request.args.get('days', 1))
        limit = int(request.args.get('limit', 1000))
        source = request.args.get('source', 'cls')
        
        news_data = news_fetcher.get_latest_news(days=days, limit=limit, source=source)
        
        return jsonify({'success': True, 'news': news_data})
    except Exception as e:
        app.logger.error(f"获取最新新闻数据时出错: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
        
@api_blueprint.route('/market_indices', methods=['GET'])
@cache.cached(timeout=300)
def get_market_indices():
    indices = {
        'A-share': {'symbol': '000001', 'name': '上证指数'},
        'HK-share': {'symbol': 'HSI', 'name': '恒生指数'},
        'US-share': {'symbol': '.INX', 'name': '标普500指数'}
    }
    results = {}

    # A-share
    try:
        df_a = ak.index_zh_a_hist_min_em(symbol=indices['A-share']['symbol'], period="1")
        if not df_a.empty:
            df_a['time'] = pd.to_datetime(df_a['时间']).dt.tz_localize('Asia/Shanghai').astype(np.int64) // 10**6
            results['A-share'] = {
                'name': indices['A-share']['name'],
                'data': df_a[['time', '收盘']].rename(columns={'收盘': 'value'}).to_dict('records')
            }
    except Exception as e:
        app.logger.warning(f"获取A股指数分时数据失败: {e}")
        results['A-share'] = {'name': '上证指数', 'error': '获取数据失败'}

    # HK-share
    try:
        df_hk = ak.index_hk_hist_min_em(symbol=indices['HK-share']['symbol'])
        if not df_hk.empty:
            df_hk['time'] = pd.to_datetime(df_hk['时间']).dt.tz_localize('Asia/Hong_Kong').astype(np.int64) // 10**6
            results['HK-share'] = {
                'name': indices['HK-share']['name'],
                'data': df_hk[['time', '收盘']].rename(columns={'收盘': 'value'}).to_dict('records')
            }
    except Exception as e:
        app.logger.warning(f"获取港股指数分时数据失败: {e}")
        results['HK-share'] = {'name': '恒生指数', 'error': '获取数据失败'}

    # US-share
    try:
        df_us = ak.index_us_hist_min_em(symbol=indices['US-share']['symbol'])
        if not df_us.empty:
            df_us['time'] = pd.to_datetime(df_us['时间']).dt.tz_localize('America/New_York').astype(np.int64) // 10**6
            results['US-share'] = {
                'name': indices['US-share']['name'],
                'data': df_us[['time', '收盘']].rename(columns={'收盘': 'value'}).to_dict('records')
            }
    except Exception as e:
        app.logger.warning(f"获取美股指数分时数据失败: {e}")
        results['US-share'] = {'name': '标普500指数', 'error': '获取数据失败'}

    return custom_jsonify({'success': True, 'indices': results})
