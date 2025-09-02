# app/web/api/__init__.py
from flask import Blueprint

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
