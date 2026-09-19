from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Usuario:
    id: int
    nombre: str
    email: str
    password_hash: str
    rol: str
    codigo_2fa: Optional[str] = None
    codigo_expira: Optional[datetime] = None
    activo: bool = True
