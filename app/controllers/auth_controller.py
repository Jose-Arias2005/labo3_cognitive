from flask import request, redirect, url_for, session, flash, render_template
from app.services.auth_service import AuthService

class AuthController:

    @staticmethod
    def login():
        # Redirigir si logueado
        if "user_id" in session:
            return redirect(url_for("usuario_routes.dashboard"))

        if request.method == "POST":
            identificador = request.form.get("identificador", "").strip()
            password      = request.form.get("password", "")

            usuario = AuthService.authenticate(identificador, password)

            if not usuario:
                flash("Credenciales incorrectas.", "danger")
                return redirect(url_for("auth_routes.login"))
            
            if usuario.get("error") == "inactive":
                flash("Cuenta no verificada. Verifica tu correo.", "warning")
                return redirect(url_for("auth_routes.login"))

            # Guardar pending
            session["pending_user_id"] = usuario["id"]
            session["pending_email"]   = usuario["email"]
            
            AuthService.generate_2fa_code(usuario["id"], usuario["email"])

            flash("Código de verificación enviado a tu correo.", "info")
            return redirect(url_for("auth_routes.verificar_2fa"))

        return render_template("auth/login.html")

    @staticmethod
    def verificar_2fa():
        # Verificar pending
        if "pending_user_id" not in session:
            return redirect(url_for("auth_routes.login"))

        if request.method == "POST":
            codigo = request.form.get("codigo", "").strip()
            user_id = session["pending_user_id"]

            usuario = AuthService.verify_2fa_code(user_id, codigo)

            if not usuario:
                flash("Código inválido o expirado.", "danger")
                return redirect(url_for("auth_routes.verificar_2fa"))

            # Limpiar pending
            session.pop("pending_user_id", None)
            session.pop("pending_email", None)

            # Iniciar sesión
            session["user_id"] = usuario["id"]
            session["nombre"]  = usuario["nombre"]
            session["rol"]     = usuario["rol"]

            flash(f"Bienvenido, {usuario['nombre']}!", "success")
            return redirect(url_for("usuario_routes.dashboard"))

        return render_template("auth/verificar_2fa.html", email=session.get("pending_email"))

    @staticmethod
    def logout():
        # Cerrar sesión
        session.clear()
        flash("Sesión cerrada.", "info")
        return redirect(url_for("auth_routes.login"))

    @staticmethod
    def register():
        # Registrar usuario
        if "user_id" in session:
            return redirect(url_for("usuario_routes.dashboard"))

        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")
            rol = request.form.get("rol", "usuario")

            if not nombre or not email or not password:
                flash("Todos los campos son obligatorios.", "danger")
                return redirect(url_for("auth_routes.register"))

            if password != confirm_password:
                flash("Las contraseñas no coinciden.", "danger")
                return redirect(url_for("auth_routes.register"))

            uid = AuthService.register_user(nombre, email, password, rol)
            if not uid:
                flash("El correo ya está registrado.", "danger")
                return redirect(url_for("auth_routes.register"))

            session["pending_reg_user_id"] = uid
            session["pending_reg_email"] = email
            flash("Código de activación enviado a tu correo.", "info")
            return redirect(url_for("auth_routes.verificar_registro"))

        return render_template("auth/register.html")

    @staticmethod
    def verificar_registro():
        # Verificar registro
        if "pending_reg_user_id" not in session:
            return redirect(url_for("auth_routes.register"))

        if request.method == "POST":
            codigo = request.form.get("codigo", "").strip()
            uid = session["pending_reg_user_id"]

            if AuthService.verify_registration(uid, codigo):
                session.pop("pending_reg_user_id", None)
                session.pop("pending_reg_email", None)
                flash("Cuenta verificada. Ahora puedes iniciar sesión.", "success")
                return redirect(url_for("auth_routes.login"))

            flash("Código inválido o expirado.", "danger")
            return redirect(url_for("auth_routes.verificar_registro"))

        return render_template("auth/verificar_registro.html", email=session.get("pending_reg_email"))
