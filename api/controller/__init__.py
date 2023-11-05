from flask import Blueprint
from flask_restful import Api
import time

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)

def init_bp(app):  
    from .test_bp import test_bp
    from .translate_bp import translate_bp
 
    bp.register_blueprint(test_bp)
    bp.register_blueprint(translate_bp)

    app.register_blueprint(bp)

    