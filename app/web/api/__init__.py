# app/web/api/__init__.py
from flask import Blueprint

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# Import routes to register them with the blueprint
from . import analysis, tasks, data
