# news_fetcher.py
# -*- coding: utf-8 -*-
"""
智能分析系统（股票） - 新闻数据获取模块
功能: 获取财联社电报新闻数据并缓存到本地，避免重复内容
"""

import os
import json
import itertools
import logging
import time
import hashlib
from datetime import datetime, timedelta, date
import akshare as ak
import pandas as pd

# A dictionary mapping news source keys to their akshare function and parameters
NEWS_SOURCES = {
    "cls": {"func": ak.stock_info_global_cls, "params": {"symbol": "全部"}, "name": "财联社"},
    "cjzc": {"func": ak.stock_info_cjzc_em, "params": {}, "name": "财经早餐"},
    "global_em": {"func": ak.stock_info_global_em, "params": {}, "name": "东方财富"},
    "global_sina": {"func": ak.stock_info_global_sina, "params": {}, "name": "新浪财经"},
    "global_futu": {"func": ak.stock_info_global_futu, "params": {}, "name": "富途牛牛"},
    "global_ths": {"func": ak.stock_info_global_ths, "params": {}, "name": "同花顺"},
}


# 设置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('news_fetcher')

# 自定义JSON编码器，处理日期类型
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if pd.isna(obj):  # 处理pandas中的NaN
            return None
        return super(DateEncoder, self).default(obj)

class NewsFetcher:
    def __init__(self, save_dir="data/news"):
        """初始化新闻获取器"""
        self.save_dir = save_dir
        # 确保保存目录存在
        os.makedirs(self.save_dir, exist_ok=True)
        self.last_fetch_time = None

        # 哈希集合用于快速判断新闻是否已存在
        self.news_hashes = set()
        # 加载已有的新闻哈希
        self._load_existing_hashes()

    def _load_existing_hashes(self):
        """加载已有文件中的新闻哈希值"""
        try:
            # 获取最近3天的文件来加载哈希值
            today = datetime.now()
            for i in range(3):  # 检查今天和前两天的数据
                date = today - timedelta(days=i)
                filename = self.get_news_filename(date)

                if os.path.exists(filename):
                    with open(filename, 'r', encoding='utf-8') as f:
                        try:
                            news_data = json.load(f)
                            for item in news_data:
                                # 如果有哈希字段就直接使用，否则计算新的哈希
                                if 'hash' in item:
                                    self.news_hashes.add(item['hash'])
                                else:
                                    content_hash = self._calculate_hash(item['content'])
                                    self.news_hashes.add(content_hash)
                        except json.JSONDecodeError:
                            logger.warning(f"文件 {filename} 格式错误，跳过加载哈希值")

            logger.info(f"已加载 {len(self.news_hashes)} 条新闻哈希值")
        except Exception as e:
            logger.error(f"加载现有新闻哈希值时出错: {str(e)}")
            # 出错时清空哈希集合，保证程序可以继续运行
            self.news_hashes = set()

    def _calculate_hash(self, content):
        """计算新闻内容的哈希值"""
        # 使用MD5哈希算法计算内容的哈希值
        # 对于财经新闻，内容通常是唯一的标识，所以只对内容计算哈希
        return hashlib.md5(str(content).encode('utf-8')).hexdigest()

    def get_news_filename(self, date=None):
        """获取指定日期的新闻文件名"""
        if date is None:
            date = datetime.now().strftime('%Y%m%d')
        else:
            date = date.strftime('%Y%m%d')
        return os.path.join(self.save_dir, f"news_{date}.json")

    def _fetch_from_source(self, source_key):
        """Fetch and normalize news from a single source."""
        source_info = NEWS_SOURCES.get(source_key)
        if not source_info:
            logger.warning(f"未知的新闻源: {source_key}")
            return []

        logger.info(f"开始获取 {source_info['name']} 的新闻数据")
        try:
            df = source_info["func"](**source_info["params"])
            if df.empty:
                logger.warning(f"获取的 {source_info['name']} 数据为空")
                return []

            logger.info(f"Source {source_key} columns: {df.columns.tolist()}")
            logger.info(f"Source {source_key} head:\\n{df.head().to_string()}")

            # Normalize columns
            # This requires knowing the column names for each source
            normalized_data = []
            for _, row in df.iterrows():
                item = {}
                pub_time_str = ''  # Initialize pub_time_str

                if source_key == 'cls':
                    item['title'] = row.get('标题')
                    item['content'] = row.get('内容')
                    item['date'] = row.get('发布日期')
                    item['time'] = row.get('发布时间')

                elif source_key == 'cjzc':
                    item['title'] = row.get('标题')
                    item['content'] = row.get('摘要')
                    pub_time_str = str(row.get('发布时间', ''))

                elif source_key == 'global_em':
                    item['title'] = row.get('标题')
                    item['content'] = row.get('摘要')
                    pub_time_str = str(row.get('发布时间', ''))

                elif source_key == 'global_sina':
                    content = row.get('内容', '')
                    item['title'] = content[:40] + '...' if len(content) > 40 else content
                    item['content'] = content
                    pub_time_str = str(row.get('时间', ''))

                elif source_key == 'global_futu':
                    item['title'] = row.get('标题')
                    item['content'] = row.get('内容')
                    pub_time_str = str(row.get('发布时间', ''))
                
                elif source_key == 'global_ths':
                    item['title'] = row.get('标题')
                    item['content'] = row.get('内容')
                    pub_time_str = str(row.get('发布时间', ''))

                # Common time parsing for sources that provide a single datetime string
                if pub_time_str:
                    try:
                        dt_object = pd.to_datetime(pub_time_str)
                        item['date'] = dt_object.strftime('%Y-%m-%d')
                        item['time'] = dt_object.strftime('%H:%M:%S')
                    except (ValueError, TypeError):
                        item['date'] = datetime.now().strftime('%Y-%m-%d')
                        item['time'] = ''
                
                # Ensure date and time are not missing if not parsed
                if 'date' not in item:
                    item['date'] = datetime.now().strftime('%Y-%m-%d')
                if 'time' not in item:
                    item['time'] = ''

                item['source'] = source_key
                normalized_data.append(item)

            return normalized_data
        except Exception as e:
            logger.error(f"获取 {source_info['name']} 数据时出错: {e}")
            return []

    def fetch_and_save(self, sources=None):
        """获取指定来源的新闻并保存到JSON文件，避免重复内容"""
        if sources is None:
            sources = list(NEWS_SOURCES.keys())
        
        now = datetime.now()
        all_new_items = []
        
        for source in sources:
            news_items = self._fetch_from_source(source)
            if not news_items:
                continue

            for item in news_items:
                content = str(item.get("content", ""))
                content_hash = self._calculate_hash(content)

                if content_hash in self.news_hashes:
                    continue

                self.news_hashes.add(content_hash)

                pub_date = item.get("date", "")
                pub_time = item.get("time", "")

                all_new_items.append({
                    "title": str(item.get("title", "")),
                    "content": content,
                    "date": str(pub_date),
                    "time": str(pub_time),
                    "datetime": f"{str(pub_date)} {str(pub_time)}".strip(),
                    "fetch_time": now.strftime('%Y-%m-%d %H:%M:%S'),
                    "hash": content_hash,
                    "source": item.get("source", source)
                })
        
        if not all_new_items:
            logger.info("没有新的新闻数据需要保存")
            return True

        # Group by date and save to respective files
        all_new_items.sort(key=lambda x: x['datetime'], reverse=True)
        
        # Get unique dates from new items
        dates_to_update = {item['date'] for item in all_new_items if item.get('date')}

        for news_date_str in dates_to_update:
            try:
                news_date = pd.to_datetime(news_date_str).to_pydatetime()
                filename = self.get_news_filename(news_date)
                
                daily_news = [item for item in all_new_items if item.get('date') == news_date_str]

                if os.path.exists(filename):
                    with open(filename, 'r', encoding='utf-8') as f:
                        try:
                            existing_data = json.load(f)
                            merged_news = existing_data + daily_news
                        except json.JSONDecodeError:
                            merged_news = daily_news
                else:
                    merged_news = daily_news
                
                merged_news.sort(key=lambda x: x['datetime'], reverse=True)

                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(merged_news, f, ensure_ascii=False, indent=2, cls=DateEncoder)
            except Exception as e:
                logger.error(f"保存日期 {news_date_str} 的新闻时出错: {e}")

        logger.info(f"成功处理 {len(all_new_items)} 条新新闻")
        self.last_fetch_time = now
        return True


    def get_latest_news(self, days=1, limit=50, source='all'):
        """获取最近几天的新闻数据，并按来源筛选"""
        news_data = []
        today = datetime.now()
        processed_dates = []

        for i in range(days):
            d = today - timedelta(days=i)
            filename = self.get_news_filename(d)
            if os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if source != 'all':
                            data = [item for item in data if item.get('source') == source]
                        news_data.extend(data)
                        processed_dates.append(d.strftime('%Y%m%d'))
                except Exception as e:
                    logger.error(f"读取文件 {filename} 时出错: {str(e)}")
        
        unique_news = {item['hash']: item for item in news_data if 'hash' in item}
        deduplicated_news = list(unique_news.values())
        deduplicated_news.sort(key=lambda x: x.get('datetime', ''), reverse=True)

        result = deduplicated_news[:limit]
        
        logger.info(f"获取来源 '{source}' 的最近 {days} 天新闻, "
                    f"共找到 {len(deduplicated_news)} 条, 返回最新 {len(result)} 条")

        return result

# 单例模式的新闻获取器
news_fetcher = NewsFetcher()

def fetch_news_task():
    """执行新闻获取任务"""
    logger.info("开始执行新闻获取任务")
    # Fetch all sources by default
    news_fetcher.fetch_and_save(sources=list(NEWS_SOURCES.keys()))
    logger.info("新闻获取任务完成")

def start_news_scheduler():
    """启动新闻获取定时任务"""
    import threading
    import time

    def _run_scheduler():
        while True:
            try:
                fetch_news_task()
                # 等待10分钟
                time.sleep(600)
            except Exception as e:
                logger.error(f"定时任务执行出错: {str(e)}")
                time.sleep(60)  # 出错后等待1分钟再试

    # 创建并启动定时任务线程
    scheduler_thread = threading.Thread(target=_run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    logger.info("新闻获取定时任务已启动")

# 初始获取一次数据
if __name__ == "__main__":
    fetch_news_task()
