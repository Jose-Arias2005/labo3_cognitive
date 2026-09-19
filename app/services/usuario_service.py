from werkzeug.security import generate_password_hash
from app.repositories.usuario_repository import UsuarioRepository

class UsuarioService:

    @staticmethod
    def create_user(nombre: str, email: str, password: str, rol: str) -> bool:
        # Verificar email
        if UsuarioRepository.get_by_email(email):
            return False
        
        password_hash = generate_password_hash(password)
        UsuarioRepository.create(nombre, email, password_hash, rol)
        return True

    @staticmethod
    def update_user(uid: int, nombre: str, email: str, rol: str, password: str = ""):
        # Actualizar datos
        password_hash = generate_password_hash(password) if password else None
        UsuarioRepository.update(uid, nombre, email, rol, password_hash)

    @staticmethod
    def delete_user(uid: int, current_user_id: int) -> bool:
        # Evitar autoeliminación
        if uid == current_user_id:
            return False
        
        UsuarioRepository.delete(uid)
        return True
