from dependency_injector import containers
from dependency_injector import providers
from app.analysis.etf_analyzer import EtfAnalyzer
from app.analysis.capital_flow_analyzer import CapitalFlowAnalyzer
from app.analysis.industry_analyzer import IndustryAnalyzer
from app.analysis.stock_analyzer import StockAnalyzer
from app.analysis.risk_monitor import RiskMonitor
from app.analysis.scenario_predictor import ScenarioPredictor
from app.analysis.news_fetcher import NewsFetcher
from app.analysis.index_industry_analyzer import IndexIndustryAnalyzer
from app.analysis.fundamental_analyzer import FundamentalAnalyzer
from app.analysis.task_manager import TaskManager
from app.analysis.stock_qa import StockQA
from app.core._core_container import CoreContainer

# 这里引入core容器

class AnalysisContainer(containers.DeclarativeContainer):

    # 引入_core容器
    _core_container = providers.Container(CoreContainer)
    
    cache = providers.Singleton(_core_container.cache)
    redis_client = providers.Singleton(_core_container.redis_cache)

    etf_analyzer = providers.Singleton(EtfAnalyzer)
    capital_flow_analyzer = providers.Singleton(CapitalFlowAnalyzer)
    industry_analyzer = providers.Singleton(IndustryAnalyzer)
    stock_analyzer = providers.Singleton(StockAnalyzer, cache=cache)
    risk_monitor = providers.Singleton(RiskMonitor)
    scenario_predictor = providers.Singleton(ScenarioPredictor)
    news_fetcher = providers.Singleton(NewsFetcher)
    index_industry_analyzer = providers.Singleton(IndexIndustryAnalyzer)
    fundamental_analyzer = providers.Singleton(FundamentalAnalyzer, cache=cache)
    stock_qa = providers.Singleton(StockQA, stock_analyzer=stock_analyzer, cache=cache)

    task_manager = providers.Singleton(TaskManager, redis_client=redis_client)
