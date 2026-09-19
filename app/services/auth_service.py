import random
import logging
from datetime import datetime, timedelta
from flask import current_app
from flask_mail import Message
from werkzeug.security import check_password_hash
from app.repositories.usuario_repository import UsuarioRepository
from app.extensions import mail

log = logging.getLogger(__name__)

class AuthService:

    @staticmethod
    def authenticate(identificador: str, password: str) -> dict:
        # Validar credenciales
        usuario = UsuarioRepository.get_by_email_or_name(identificador)
        if usuario and check_password_hash(usuario["password_hash"], password):
            if not usuario.get("activo", True):
                return {"error": "inactive"}
            return usuario
        return None

    @staticmethod
    def generate_2fa_code(uid: int, email: str):
        # Generar 2FA
        codigo = str(random.randint(100000, 999999))
        expira = datetime.utcnow() + timedelta(minutes=5)
        UsuarioRepository.set_2fa_code(uid, codigo, expira)
        AuthService.send_2fa_email(email, codigo)

    @staticmethod
    def send_2fa_email(email: str, codigo: str):
        # Enviar email
        if current_app.config["MAIL_SUPPRESS_SEND"]:
            log.info("──────────────────────────────────────")
            log.info(f"  CÓDIGO 2FA para {email}: {codigo}")
            log.info("──────────────────────────────────────")
            return
        
        msg = Message(
            subject="Tu código de verificación",
            recipients=[email],
            body=f"Tu código de verificación es: {codigo}\nVálido por 5 minutos."
        )
        mail.send(msg)

    @staticmethod
    def verify_2fa_code(uid: int, codigo_ingresado: str) -> dict:
        # Verificar 2FA
        usuario = UsuarioRepository.get_by_id(uid)
        ahora = datetime.utcnow()

        if (
            not usuario
            or usuario["codigo_2fa"] != codigo_ingresado
            or usuario["codigo_expira"] is None
            or ahora > usuario["codigo_expira"].replace(tzinfo=None)
        ):
            return None

        UsuarioRepository.clear_2fa_code(uid)
        return usuario

    @staticmethod
    def register_user(nombre: str, email: str, password: str, rol: str = "usuario") -> int:
        # Crear inactivo
        from werkzeug.security import generate_password_hash
        
        if UsuarioRepository.get_by_email(email):
            return None
        
        password_hash = generate_password_hash(password)
        uid = UsuarioRepository.create(nombre, email, password_hash, rol, activo=False)
        AuthService.generate_2fa_code(uid, email)
        return uid

    @staticmethod
    def verify_registration(uid: int, codigo: str) -> bool:
        # Activar cuenta
        usuario = AuthService.verify_2fa_code(uid, codigo)
        if usuario:
            UsuarioRepository.activate_user(uid)
            return True
        return False
