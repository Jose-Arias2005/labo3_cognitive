# LabAdmin – Laboratorio Flask + PostgreSQL + Docker

Panel de administración web desarrollado en Flask bajo una arquitectura modular por capas. Cuenta con sistema de registro público con selección de rol (Administrador/Usuario), inicio de sesión seguro, doble factor de autenticación (2FA) por correo electrónico y CRUD completo de usuarios sobre PostgreSQL.

---

## Requisitos Previos

- **Docker Desktop** instalado y **en ejecución** (abre la aplicación Docker Desktop antes de ejecutar comandos en la terminal).
- Cuenta de Google/Gmail personal con verificación en dos pasos activa.

---

## 1. Obtener la Contraseña de Aplicación (Gmail 2FA)

Para que el sistema envíe los códigos de 6 dígitos a tu correo real (tanto en el registro como en el login), necesitas generar una clave de 16 caracteres:

1. Abre tu navegador e inicia sesión en tu cuenta de Google.
2. Ingresa directamente al siguiente enlace:  
   👉 **[https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)**
3. En la casilla **Nombre de la app**, escribe: `FlaskLab`.
4. Haz clic en **Crear**.
5. Se mostrará una ventana con una contraseña de **16 caracteres**. Cópiala tal como aparece (sin espacios).

---

## 2. Configuración de Variables de Entorno

1. En la raíz del proyecto, genera tu archivo `.env` copiando la plantilla:

   ```bash
   cp .env.example .env
   ```

2. Abre el archivo `.env` con tu editor de código y reemplaza los valores por tus credenciales reales:
```env
# Configuración de Correo (Gmail SMTP)
MAIL_USERNAME=tu_correo_personal@gmail.com
MAIL_PASSWORD=tu_clave_de_16_caracteres_aqui
MAIL_DEFAULT_SENDER=tu_correo_personal@gmail.com
```

> **Nota:** En `MAIL_PASSWORD` debes pegar la clave de 16 letras generada en el paso anterior (todo seguido, sin espacios). Si decides no configurarlo, el sistema funcionará igualmente imprimiendo los códigos 2FA en la consola de Docker.

---

## 3. Iniciar la Aplicación con Docker

1. Asegúrate de que **Docker Desktop esté abierto y corriendo** en segundo plano.
2. Desde la terminal, ubicado en la raíz del proyecto, ejecuta:
```bash
docker-compose up --build
```

3. Espera a que termine de descargar las imágenes, compilar la aplicación y levantar PostgreSQL.
4. Abre tu navegador e ingresa a:
👉 **http://localhost:5000**

---

## 4. Flujo de Uso

1. **Registro inicial:** Ve a **Registrarse** (`/register`), llena tus datos (usa tu correo real), elige tu rol y envía el formulario.
2. **Activación de cuenta:** Revisa tu correo, copia el código de 6 dígitos e ingrésalo en la pantalla de verificación.
3. **Inicio de sesión:** Inicia sesión con tu correo y contraseña. Te llegará un nuevo código 2FA para acceder.
4. **Panel de Gestión:** Una vez autenticado, accede al CRUD completo para crear, listar, editar y eliminar usuarios.

---

## Comandos Útiles

```bash
# Ver los logs en tiempo real (para ver los códigos 2FA si no usas correo real)
docker-compose logs -f web

# Detener los contenedores
docker-compose down

# Reiniciar la base de datos desde cero (elimina datos y volúmenes)
docker-compose down -v
```