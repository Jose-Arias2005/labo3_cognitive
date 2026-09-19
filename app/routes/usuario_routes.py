from flask import Blueprint, session, redirect, url_for, flash
from functools import wraps
from app.controllers.usuario_controller import UsuarioController

usuario_bp = Blueprint('usuario_routes', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión.", "warning")
            return redirect(url_for("auth_routes.login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("rol") != "admin":
            flash("Acceso restringido a administradores.", "danger")
            return redirect(url_for("usuario_routes.dashboard"))
        return f(*args, **kwargs)
    return decorated

usuario_bp.route('/dashboard', methods=['GET'])(login_required(UsuarioController.dashboard))
usuario_bp.route('/usuarios', methods=['GET'])(login_required(admin_required(UsuarioController.listar_usuarios)))
usuario_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])(login_required(admin_required(UsuarioController.crear_usuario)))
usuario_bp.route('/usuarios/editar/<int:uid>', methods=['GET', 'POST'])(login_required(admin_required(UsuarioController.editar_usuario)))
usuario_bp.route('/usuarios/eliminar/<int:uid>', methods=['POST'])(login_required(admin_required(UsuarioController.eliminar_usuario)))
