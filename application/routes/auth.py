from flask import jsonify, request, Blueprint
from application.util.auth_utils import handle_signup, handle_login, handle_logout

bp = Blueprint('auth', __name__)


@bp.route('/api/signup', methods=['POST'])
def signup():
    handle_signup(request)
    return jsonify(status='ok')


@bp.route('/api/login', methods=['POST'])
def login():
    response = handle_login(request)
    return jsonify(response)


@bp.route('/api/logout', methods=['POST'])
def logout():
    handle_logout(request)
    return jsonify(status='ok')
