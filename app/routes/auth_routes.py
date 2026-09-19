from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint('auth_routes', __name__)

auth_bp.route('/', methods=['GET', 'POST'])(AuthController.login)
auth_bp.route('/verificar', methods=['GET', 'POST'])(AuthController.verificar_2fa)
auth_bp.route('/logout', methods=['GET'])(AuthController.logout)
auth_bp.route('/register', methods=['GET', 'POST'])(AuthController.register)
auth_bp.route('/verificar-registro', methods=['GET', 'POST'])(AuthController.verificar_registro)
