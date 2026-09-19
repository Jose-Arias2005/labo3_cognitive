import os

class Config:
    # Clave secreta
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave_super_secreta_dev")

    # Conexión BD
    DB_HOST     = os.environ.get("DB_HOST", "db")
    DB_PORT     = os.environ.get("DB_PORT", "5432")
    DB_NAME     = os.environ.get("DB_NAME", "labdb")
    DB_USER     = os.environ.get("DB_USER", "labuser")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "labpass")

    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Flask-Mail
    MAIL_SERVER   = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT     = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS  = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@lab.com")

    # Simular email si no hay credenciales
    MAIL_SUPPRESS_SEND = MAIL_USERNAME == ""
