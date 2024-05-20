from flask import Blueprint

bp = Blueprint('demo', __name__)

@bp.route('/demo', methods=['GET'])
def hello_world():
    return "Hello world"
