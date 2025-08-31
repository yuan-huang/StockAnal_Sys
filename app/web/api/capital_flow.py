# -*- coding: utf-8 -*-
"""
资金流向API接口
包含北向资金历史数据等接口
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import traceback
import logging

# 创建蓝图
capital_flow_blueprint = Blueprint('capital_flow', __name__)

@capital_flow_blueprint.route('/north_flow_history', methods=['POST'])
def api_north_flow_history():
    """获取北向资金历史数据"""
    try:
        data = request.json
        stock_code = data.get('stock_code')
        days = data.get('days', 10)  # 默认为10天，对应前端的默认选项

        # 计算 end_date 为当前时间
        end_date = datetime.now().strftime('%Y%m%d')

        # 计算 start_date 为 end_date 减去指定的天数
        start_date = (datetime.now() - timedelta(days=int(days))).strftime('%Y%m%d')

        if not stock_code:
            return jsonify({'error': '请提供股票代码'}), 400

        # 调用北向资金历史数据方法

        # 暂时注释掉这个功能，因为方法不存在
        # analyzer = CapitalFlowAnalyzer()
        # result = analyzer.get_north_flow_history(stock_code, start_date, end_date)
        
        # 返回暂时不可用的提示
        return jsonify({'error': '北向资金历史数据功能正在重构中，暂时不可用'}), 503
    except Exception as e:
        logging.error(f"获取北向资金历史数据出错: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500 