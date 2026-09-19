-- Tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id             SERIAL PRIMARY KEY,
    nombre         VARCHAR(120)  NOT NULL,
    email          VARCHAR(180)  NOT NULL UNIQUE,
    password_hash  VARCHAR(256)  NOT NULL,
    rol            VARCHAR(20)   NOT NULL DEFAULT 'usuario' CHECK (rol IN ('admin','usuario')),
    codigo_2fa     VARCHAR(6),
    codigo_expira  TIMESTAMP,
    activo         BOOLEAN       DEFAULT TRUE
);

-- Admin por defecto: admin@lab.com / Admin1234!
INSERT INTO usuarios (nombre, email, password_hash, rol)
VALUES (
    'Administrador',
    'admin@lab.com',
    'scrypt:32768:8:1$zMHcToP1Bw8KHGPb$bdc5df5ed58edbc2f597b64f77e25e49e9e53b41c6d0c070c014f2a3df12b0bf3c235e89b6ae3bae461b32be8bd5f20a14b21ccc8d4355513b5a89e49773156e',
    'admin'
)
ON CONFLICT (email) DO NOTHING;

-- Usuario demo: usuario@lab.com / User1234!
INSERT INTO usuarios (nombre, email, password_hash, rol)
VALUES (
    'Usuario Demo',
    'usuario@lab.com',
    'scrypt:32768:8:1$yhgoq1k2n7NzqiWC$7644821f9083a24e29fa7234359e67ab5ce14a10911b8fdd6db2a1722a06d83905b4746b4fbddc3e76d54d94b03eafedd31214bbc974fe0f18b3d4edae7d433e',
    'usuario'
)
ON CONFLICT (email) DO NOTHING;
