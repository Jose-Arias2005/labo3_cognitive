from app.repositories.db import query

class UsuarioRepository:
    
    @staticmethod
    def get_by_id(user_id: int) -> dict:
        # Obtener usuario
        return query("SELECT * FROM usuarios WHERE id = %s", (user_id,), fetchone=True)

    @staticmethod
    def get_by_email_or_name(identificador: str) -> dict:
        # Buscar usuario
        return query(
            "SELECT * FROM usuarios WHERE email = %s OR nombre = %s",
            (identificador, identificador),
            fetchone=True
        )

    @staticmethod
    def get_by_email(email: str) -> dict:
        # Buscar email
        return query("SELECT id FROM usuarios WHERE email = %s", (email,), fetchone=True)

    @staticmethod
    def get_all() -> list:
        # Listar usuarios
        return query("SELECT id, nombre, email, rol FROM usuarios ORDER BY id", fetchall=True)

    @staticmethod
    def create(nombre, email, password_hash, rol, activo=True) -> int:
        # Crear usuario
        res = query(
            "INSERT INTO usuarios (nombre, email, password_hash, rol, activo) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (nombre, email, password_hash, rol, activo), fetchone=True
        )
        return res["id"] if res else None

    @staticmethod
    def update(uid, nombre, email, rol, password_hash=None):
        # Actualizar usuario
        if password_hash:
            query(
                "UPDATE usuarios SET nombre=%s, email=%s, rol=%s, password_hash=%s WHERE id=%s",
                (nombre, email, rol, password_hash, uid)
            )
        else:
            query(
                "UPDATE usuarios SET nombre=%s, email=%s, rol=%s WHERE id=%s",
                (nombre, email, rol, uid)
            )

    @staticmethod
    def delete(uid: int):
        # Eliminar usuario
        query("DELETE FROM usuarios WHERE id = %s", (uid,))

    @staticmethod
    def count_all() -> int:
        # Contar usuarios
        res = query("SELECT COUNT(*) AS total FROM usuarios", fetchone=True)
        return res["total"] if res else 0

    @staticmethod
    def count_admins() -> int:
        # Contar admins
        res = query("SELECT COUNT(*) AS total FROM usuarios WHERE rol = 'admin'", fetchone=True)
        return res["total"] if res else 0

    @staticmethod
    def set_2fa_code(uid: int, codigo: str, expira):
        # Guardar 2FA
        query(
            "UPDATE usuarios SET codigo_2fa = %s, codigo_expira = %s WHERE id = %s",
            (codigo, expira, uid)
        )

    @staticmethod
    def activate_user(uid: int):
        # Activar usuario
        query("UPDATE usuarios SET activo = TRUE WHERE id = %s", (uid,))

    @staticmethod
    def clear_2fa_code(uid: int):
        # Limpiar 2FA
        query(
            "UPDATE usuarios SET codigo_2fa = NULL, codigo_expira = NULL WHERE id = %s",
            (uid,)
        )
