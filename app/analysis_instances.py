# app/analysis_instances.py
"""
Centralized module for instantiating all analysis singletons.
This breaks the circular dependency between web_server.py and the api blueprint modules.
"""
from app.analysis.stock_analyzer import StockAnalyzer
from app.analysis.us_stock_service import USStockService
from app.analysis.industry_analyzer import IndustryAnalyzer
from app.analysis.fundamental_analyzer import FundamentalAnalyzer
from app.analysis.capital_flow_analyzer import CapitalFlowAnalyzer
from app.analysis.scenario_predictor import ScenarioPredictor
from app.analysis.stock_qa import StockQA
from app.analysis.risk_monitor import RiskMonitor
from app.analysis.index_industry_analyzer import IndexIndustryAnalyzer
from app.core.config import config_manager

# Main Analyzers
analyzer = StockAnalyzer()
us_stock_service = USStockService()

# Module-specific Analyzers
fundamental_analyzer = FundamentalAnalyzer()
capital_flow_analyzer = CapitalFlowAnalyzer()
scenario_predictor = ScenarioPredictor(analyzer, config_manager.get('OPENAI_API_KEY'), config_manager.get('OPENAI_API_MODEL'))
stock_qa = StockQA(analyzer, config_manager.get('OPENAI_API_KEY'))
risk_monitor = RiskMonitor(analyzer)
index_industry_analyzer = IndexIndustryAnalyzer(analyzer)
industry_analyzer = IndustryAnalyzer()
