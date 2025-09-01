# app/web/api/__init__.py
from flask import Blueprint





api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# 导入所有API路由模块，确保路由被注册
from . import data
from . import stock_analysis
from . import tasks
from . import analysis
from . import us_stocks
from . import capital_flow
from . import system
from . import news