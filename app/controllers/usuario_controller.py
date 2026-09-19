from flask import render_template, request, redirect, url_for, flash, session
from app.services.usuario_service import UsuarioService
from app.repositories.usuario_repository import UsuarioRepository

class UsuarioController:

    @staticmethod
    def dashboard():
        # Obtener totales
        total = UsuarioRepository.count_all()
        admins = UsuarioRepository.count_admins()
        return render_template(
            "usuarios/dashboard.html",
            total_usuarios=total,
            total_admins=admins
        )

    @staticmethod
    def listar_usuarios():
        # Listar todos
        usuarios = UsuarioRepository.get_all()
        return render_template("usuarios/listar.html", usuarios=usuarios)

    @staticmethod
    def crear_usuario():
        # Manejar creación
        if request.method == "POST":
            nombre   = request.form.get("nombre", "").strip()
            email    = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            rol      = request.form.get("rol", "usuario")

            if not nombre or not email or not password:
                flash("Todos los campos son obligatorios.", "danger")
                return redirect(url_for("usuario_routes.crear_usuario"))

            if not UsuarioService.create_user(nombre, email, password, rol):
                flash("El email ya está registrado.", "danger")
                return redirect(url_for("usuario_routes.crear_usuario"))

            flash("Usuario creado correctamente.", "success")
            return redirect(url_for("usuario_routes.listar_usuarios"))

        return render_template("usuarios/form.html", usuario=None, accion="Crear")

    @staticmethod
    def editar_usuario(uid: int):
        # Manejar edición
        usuario = UsuarioRepository.get_by_id(uid)
        if not usuario:
            flash("Usuario no encontrado.", "danger")
            return redirect(url_for("usuario_routes.listar_usuarios"))

        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()
            email  = request.form.get("email", "").strip()
            rol    = request.form.get("rol", "usuario")
            password = request.form.get("password", "")

            if not nombre or not email:
                flash("Nombre y email son obligatorios.", "danger")
                return redirect(url_for("usuario_routes.editar_usuario", uid=uid))

            UsuarioService.update_user(uid, nombre, email, rol, password)
            flash("Usuario actualizado.", "success")
            return redirect(url_for("usuario_routes.listar_usuarios"))

        return render_template("usuarios/form.html", usuario=usuario, accion="Editar")

    @staticmethod
    def eliminar_usuario(uid: int):
        # Manejar eliminación
        current_user_id = session.get("user_id")
        if not UsuarioService.delete_user(uid, current_user_id):
            flash("No puedes eliminarte a ti mismo.", "danger")
            return redirect(url_for("usuario_routes.listar_usuarios"))

        flash("Usuario eliminado.", "success")
        return redirect(url_for("usuario_routes.listar_usuarios"))
