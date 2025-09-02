# app/web/api/data.py
from flask import request, jsonify
from . import api_blueprint
from app.web.utils import custom_jsonify
import akshare as ak
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from app.analysis._analysis_container import AnalysisContainer
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide  
from app.analysis.stock_analyzer import StockAnalyzer
from app.core.cache import Cache
from app.analysis.news_fetcher import NewsFetcher

import logging
logger = logging.getLogger(__name__)


@api_blueprint.route('/index_stocks', methods=['GET'])
@inject
def get_index_stocks(cache: Cache = Provide[AnalysisContainer.cache]):
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
        logger.logger.error(f"获取指数成分股时出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/industry_stocks', methods=['GET'])
@inject
def get_industry_stocks(cache: Cache = Provide[AnalysisContainer.cache]):
    try:
        industry = request.args.get('industry')
        if not industry:
            return jsonify({'error': '请提供行业名称'}), 400
        
        stocks = ak.stock_board_industry_cons_em(symbol=industry)
        stock_list = stocks['代码'].tolist() if '代码' in stocks.columns else []

        return jsonify({'stock_list': stock_list})
    except Exception as e:
        logger.error(f"获取行业成分股时出错: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


        
@api_blueprint.route('/market_indices', methods=['GET'])
@inject
def get_market_indices(cache: Cache = Provide[AnalysisContainer.cache]):
    # 获取实时行情数据
    results = {}
    
    # A-share
    try:
        df_a = ak.stock_zh_index_spot_sina()
        if not df_a.empty:
            # 获取上证指数数据（代码通常以'000001'开头）
            sh_index = df_a[df_a['代码'].str.startswith('sh000001')]
            if not sh_index.empty:
                index_info = sh_index.iloc[0]
                results['A-share'] = {
                    'name': '上证指数',
                    'data': {
                        'code': index_info['代码'],
                        'name': index_info['名称'],
                        'latest_price': index_info['最新价'],
                        'change_amount': index_info['涨跌额'],
                        'change_percent': index_info['涨跌幅'],
                        'volume': index_info['成交量'],
                        'amount': index_info['成交额'],
                        'high': index_info['最高'],
                        'low': index_info['最低'],
                        'open': index_info['今开'],
                        'prev_close': index_info['昨收']
                    }
                }
            else:
                results['A-share'] = {'error': '未找到上证指数数据', 'name': '上证指数', 'data': {}}
        else:
            results['A-share'] = {'error': 'A股数据为空', 'name': '上证指数', 'data': {}}
        
    except Exception as e:
        logger.warning(f"获取A股指数数据失败: {e}")
        results['A-share'] = {'error': '获取数据失败', 'name': '上证指数', 'data': {}}

    # HK-share
    try:
        df_hk = ak.stock_hk_index_spot_sina()
        if not df_hk.empty:
            # 获取恒生指数数据
            hk_index = df_hk[df_hk['代码'].str.contains('HSI', na=False)]
            if not hk_index.empty:
                index_info = hk_index.iloc[0]
                results['HK-share'] = {
                    'name': '恒生指数',
                    'data': {
                        'code': index_info['代码'],
                        'name': index_info['名称'],
                        'latest_price': index_info['最新价'],
                        'change_amount': index_info['涨跌额'],
                        'change_percent': index_info['涨跌幅'],
                        'open': index_info['今开'],
                        'high': index_info['最高'],
                        'low': index_info['最低'],
                        'prev_close': index_info['昨收'],
                        'volume': 0,
                        'amount': 0
                    }
                }
            else:
                results['HK-share'] = {'error': '未找到恒生指数数据', 'name': '恒生指数', 'data': {}}
        else:
            results['HK-share'] = {'error': '港股数据为空', 'name': '恒生指数', 'data': {}}
        
    except Exception as e:
        logger.warning(f"获取港股指数数据失败: {e}")
        results['HK-share'] = {'error': '获取数据失败', 'name': '恒生指数', 'data': []}

    # US-share
    try:
        df_us = ak.index_us_stock_sina(symbol=".INX")
        if not df_us.empty:
            # 美股数据通常直接返回标普500指数数据
            if 'close' in df_us.columns:
                latest_row = df_us.iloc[-1]
                results['US-share'] = {
                    'name': '标普500指数',
                    'data': {
                        'close': latest_row['close'],
                        'open': latest_row['open'],
                        'high': latest_row['high'],
                        'low': latest_row['low'],
                        'volume': latest_row['volume']
                    }
                }
            else:
                results['US-share'] = {'error': '美股数据结构异常', 'name': '标普500指数', 'data': {}}
        else:
            results['US-share'] = {'error': '美股数据为空', 'name': '标普500指数', 'data': {}}
        
    except Exception as e:
        logger.warning(f"获取美股指数数据失败: {e}")
        results['US-share'] = {'error': '获取数据失败', 'name': '标普500指数', 'data': []}

    return custom_jsonify(results)
