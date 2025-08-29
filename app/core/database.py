import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 读取配置
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/stock_analyzer.db')
USE_DATABASE = os.getenv('USE_DATABASE', 'False').lower() == 'true'

# 创建引擎
engine = create_engine(DATABASE_URL)
Base = declarative_base()


# 定义模型
class StockInfo(Base):
    __tablename__ = 'stock_info'

    id = Column(Integer, primary_key=True)
    stock_code = Column(String(10), nullable=False, index=True)
    stock_name = Column(String(50))
    market_type = Column(String(5))
    industry = Column(String(50))
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'stock_code': self.stock_code,
            'stock_name': self.stock_name,
            'market_type': self.market_type,
            'industry': self.industry,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }


class AnalysisResult(Base):
    __tablename__ = 'analysis_results'

    id = Column(Integer, primary_key=True)
    stock_code = Column(String(10), nullable=False, index=True)
    market_type = Column(String(5))
    analysis_date = Column(DateTime, default=datetime.now)
    score = Column(Float)
    recommendation = Column(String(100))
    technical_data = Column(JSON)
    fundamental_data = Column(JSON)
    capital_flow_data = Column(JSON)
    ai_analysis = Column(Text)

    def to_dict(self):
        return {
            'stock_code': self.stock_code,
            'market_type': self.market_type,
            'analysis_date': self.analysis_date.strftime('%Y-%m-%d %H:%M:%S') if self.analysis_date else None,
            'score': self.score,
            'recommendation': self.recommendation,
            'technical_data': self.technical_data,
            'fundamental_data': self.fundamental_data,
            'capital_flow_data': self.capital_flow_data,
            'ai_analysis': self.ai_analysis
        }


class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False, index=True)
    name = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    stocks = Column(JSON)  # 存储股票列表的JSON

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'stocks': self.stocks
        }


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    password_change_required = Column(Boolean, default=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password_change_required': self.password_change_required
        }




# 创建会话工厂
Session = sessionmaker(bind=engine)


# 初始化数据库
def init_db():
    Base.metadata.create_all(engine)


# 获取数据库会话
def get_session():
    return Session()

