# -*- coding: utf-8 -*-
"""
股票分析API接口
包含股票分析、增强分析等接口
"""

from flask import Blueprint, request, jsonify, current_app
import time
import traceback
import logging
from app.analysis.stock_analyzer import StockAnalyzer

# 创建蓝图
stock_analysis_blueprint = Blueprint('stock_analysis', __name__)

def get_analyzer():
    """获取分析器实例"""
    try:
        # 从Flask应用容器中获取分析器实例
        return current_app.container.stock_analyzer()
    except Exception as e:
        logging.error(f"获取分析器实例失败: {str(e)}")
        return None

@stock_analysis_blueprint.route('/analyze', methods=['POST'])
def analyze():
    """股票分析接口"""
    try:
        data = request.json
        stock_codes = data.get('stock_codes', [])
        market_type = data.get('market_type', 'A')

        if not stock_codes:
            return jsonify({'error': '请输入代码'}), 400

        logging.info(f"分析股票请求: {stock_codes}, 市场类型: {market_type}")

        # 设置最大处理时间，每只股票10秒
        max_time_per_stock = 10  # 秒
        max_total_time = max(30, min(60, len(stock_codes) * max_time_per_stock))  # 至少30秒，最多60秒

        start_time = time.time()
        results = []

        for stock_code in stock_codes:
            try:
                # 检查是否已超时
                if time.time() - start_time > max_total_time:
                    logging.warning(f"分析股票请求已超过{max_total_time}秒，提前返回已处理的{len(results)}只股票")
                    break

                # 使用线程本地缓存的分析器实例
                current_analyzer = get_analyzer()
                if current_analyzer is None:
                    raise Exception("分析器未正确初始化，请检查缓存配置")
                result = current_analyzer.quick_analyze_stock(stock_code.strip(), market_type)

                logging.info(
                    f"分析结果: 股票={stock_code}, 名称={result.get('stock_name', '未知')}, 行业={result.get('industry', '未知')}")
                results.append(result)
            except Exception as e:
                logging.error(f"分析股票 {stock_code} 时出错: {str(e)}")
                results.append({
                    'stock_code': stock_code,
                    'error': str(e),
                    'stock_name': '分析失败',
                    'industry': '未知'
                })

        return jsonify({'results': results})
    except Exception as e:
        logging.error(f"分析股票时出错: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@stock_analysis_blueprint.route('/enhanced_analysis', methods=['POST'])
def enhanced_analysis():
    """原增强分析API的向后兼容版本 - 功能重构中"""
    try:
        data = request.json
        stock_code = data.get('stock_code')
        market_type = data.get('market_type', 'A')

        if not stock_code:
            return jsonify({'error': '请输入股票代码'}), 400

        # 暂时使用基础分析功能
        try:
            current_analyzer = get_analyzer()
            if current_analyzer is None:
                raise Exception("分析器未正确初始化，请检查缓存配置")
            result = current_analyzer.quick_analyze_stock(stock_code, market_type)
            logging.info(f"基础分析完成: {stock_code}")
            return jsonify({'result': result})
        except Exception as e:
            logging.error(f"分析过程中出错: {str(e)}")
            return jsonify({'error': f'分析过程中出错: {str(e)}'}), 500

    except Exception as e:
        logging.error(f"执行分析时出错: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500 