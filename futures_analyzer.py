# -*- coding: utf-8 -*-
import akshare as ak
from datetime import datetime
import pandas as pd
import traceback
import functools

# --- Caching Decorator ---
def cached_property(func):
    """
    Decorator that computes a property once and caches the result.
    """
    return property(functools.lru_cache(maxsize=1)(func))

class FuturesAnalyzer:
    def __init__(self):
        """
        初始化期货分析器
        """
        pass

    @cached_property
    def _get_variety_mapping(self):
        """
        获取期货品种代码与中文名称的映射，并缓存结果。
        """
        try:
            # futures_variety_dict 是一个直接可用的字典
            variety_map = ak.futures_variety_dict()
            # akshare返回的字典是 {中文名: 英文代码}，我们需要反转它
            return {v: k for k, v in variety_map.items()}
        except Exception as e:
            print(f"获取期货品种映射失败: {e}")
            return {}

    def get_futures_rank_summary(self, date=None):
        """
        获取各大期货交易所的每日持仓排名汇总。

        :param date: 日期，格式YYYYMMDD，默认为最新交易日
        :return: 包含排名信息的字典
        """
        if date is None:
            date = (datetime.now() - pd.Timedelta(days=1)).strftime('%Y%m%d')

        variety_mapping = self._get_variety_mapping

        try:
            rank_df = ak.get_rank_sum_daily(start_day=date, end_day=date)
            
            if rank_df.empty:
                return {
                    "date": date,
                    "error": "未获取到指定日期的持仓数据，请检查是否为交易日或尝试更早的日期。"
                }
            
            required_cols = ['variety', 'long_open_interest_top20', 'short_open_interest_top20']
            if not all(col in rank_df.columns for col in required_cols):
                 return {
                    "date": date,
                    "error": f"API返回的数据格式不符合预期。收到的列: {rank_df.columns.tolist()}"
                }

            result_df = rank_df[required_cols].copy()
            
            numeric_cols = ['long_open_interest_top20', 'short_open_interest_top20']
            for col in numeric_cols:
                result_df[col] = pd.to_numeric(result_df[col], errors='coerce').fillna(0)

            result_df['net_position'] = result_df['long_open_interest_top20'] - result_df['short_open_interest_top20']
            
            # 添加中文名称
            result_df['variety_name'] = result_df['variety'].map(variety_mapping).fillna(result_df['variety'])

            result_df.rename(columns={
                'variety': 'variety_code',
                'long_open_interest_top20': 'total_long_position',
                'short_open_interest_top20': 'total_short_position',
            }, inplace=True)
            
            result_df.sort_values(by='net_position', ascending=False, inplace=True)

            result = {
                "date": date,
                "rankings": result_df.to_dict('records')
            }

            return result

        except Exception as e:
            print(traceback.format_exc())
            return {"error": f"处理数据时发生未知错误: {e}"}

if __name__ == '__main__':
    analyzer = FuturesAnalyzer()
    test_date = "20240520" 
    data = analyzer.get_futures_rank_summary(date=test_date)
    import json
    print(json.dumps(data, indent=4, ensure_ascii=False))
