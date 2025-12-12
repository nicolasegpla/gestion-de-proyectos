
# Gestión de Proyectos – Backend API

Este repositorio contiene el **backend de un sistema de gestión de proyectos** pensado para pequeñas empresas o equipos que necesitan organizar su trabajo mediante:

- Empresas (clientes/organizaciones)
- Usuarios internos de cada empresa
- Proyectos
- Historias de usuario (user stories)
- Tickets asociados a cada historia

Toda la lógica está construida con **FastAPI** y **PostgreSQL**, utilizando **JWT** para la autenticación y **SQLAlchemy + Alembic** para la capa de persistencia y migraciones de base de datos.

---

## 🎯 Objetivo del proyecto

Proveer una **API REST multi-empresa** que permita:

- Registrar empresas y autenticarlas con JWT.
- Gestionar usuarios asociados a cada empresa.
- Crear proyectos y mantenerlos aislados por empresa.
- Definir historias de usuario por proyecto.
- Crear y administrar tickets por historia de usuario, con estados y prioridades.

Este backend está pensado para integrarse con un frontend (por ejemplo, una SPA en React) que consuma estos endpoints y construya un tablero de gestión de proyectos.

---

## 🧱 Stack tecnológico

- **Lenguaje:** Python 3
- **Framework Web:** FastAPI
- **Servidor ASGI:** Uvicorn
- **ORM:** SQLAlchemy 2.x
- **Migraciones:** Alembic
- **Base de datos:** PostgreSQL (SQLite se puede usar para desarrollo rápido)
- **Autenticación:** JWT (`python-jose`, `passlib`, `bcrypt`)
- **Configuración:** `pydantic-settings`, `python-dotenv`
- **Contenedores:** Docker

Revisa el archivo [`requirements.txt`](./requirements.txt) para ver las versiones exactas de las dependencias.

---

## 📁 Estructura principal del proyecto

```bash
.
├── alembic/              # Scripts de migración de base de datos
├── app/
│   ├── core/             # Seguridad, dependencias comunes, configuración
│   ├── db/               # Sesiones, engine y base declarativa
│   ├── models/           # Modelos SQLAlchemy (Empresa, Usuario, Proyecto, etc.)
│   ├── routers/          # Rutas / endpoints organizados por dominio
│   ├── schemas/          # Esquemas Pydantic (requests/responses)
│   ├── services/         # Lógica de dominio / casos de uso
│   └── main.py           # Punto de entrada de la aplicación FastAPI
├── Dockerfile
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## 🔐 Autenticación y multi-tenant

El sistema está diseñado para ser **multi-tenant a nivel de empresa**:

- Cada empresa se registra vía `/auth/registro`.
- El login se realiza en `/auth/login`, devolviendo un **JWT** con:
  - `sub`: email de la entidad autenticada
  - `id`: id de la empresa
  - `type`: tipo de actor (`"empresa"` o `"usuario"`)

Estos datos se utilizan en los endpoints protegidos mediante dependencias como `get_current_empresa`, garantizando que:

- Una empresa solo ve sus propios proyectos.
- Las historias de usuario y tickets están siempre asociados a proyectos de esa empresa.
- No hay “mezcla” de datos entre empresas.

---

## 🔌 Endpoints principales (resumen)

Algunos grupos de rutas más relevantes:

### Autenticación de empresas (`/auth`)

- `POST /auth/registro`  
  Registra una nueva empresa.

- `POST /auth/login`  
  Autentica una empresa y devuelve un **access token JWT**.

- `GET /auth/listado-empresas`  
  Lista de empresas (uso interno / administración).

- `GET /auth/resumen`  
  Listado compacto de empresas (id + nombre).

### Proyectos (`/proyectos`)

- `POST /proyectos/`  
  Crea un nuevo proyecto para la empresa autenticada.

- `GET /proyectos/`  
  Lista todos los proyectos de la empresa.

- `GET /proyectos/{proyecto_id}`  
  Obtiene un proyecto específico.

- `PUT /proyectos/{proyecto_id}`  
  Actualiza nombre y descripción de un proyecto.

- `DELETE /proyectos/{proyecto_id}`  
  Elimina un proyecto de la empresa.

### Historias de usuario (`/historias-usuario`)

- `POST /historias-usuario/`  
  Crea una nueva historia de usuario asociada a un proyecto.

- `GET /historias-usuario/proyecto/{proyecto_id}`  
  Lista todas las historias de un proyecto.

- `GET /historias-usuario/{historia_id}`  
  Obtiene una historia específica.

- `PUT /historias-usuario/{historia_id}`  
  Actualiza título, descripción, estado y prioridad.

- `DELETE /historias-usuario/{historia_id}`  
  Elimina una historia de usuario.

### Tickets (`/tickets`)

- `POST /tickets/`  
  Crea un ticket asociado a una historia de usuario.

- `GET /tickets/historia/{historia_usuario_id}`  
  Lista tickets de una historia de usuario.

- `GET /tickets/{ticket_id}`  
  Obtiene un ticket concreto.

- `PUT /tickets/{ticket_id}`  
  Actualiza asunto, descripción, estado y prioridad.

- `PATCH /tickets/{ticket_id}/estado`  
  Actualiza solo el **estado** de un ticket.

- `DELETE /tickets/{ticket_id}`  
  Elimina un ticket.

> Para ver todos los endpoints disponibles con detalle, puedes abrir la documentación interactiva en `/docs` una vez que la API esté levantada.

---

## ⚙️ Requisitos previos

Para ejecutar este proyecto en otra máquina, asegúrate de contar con:

- **Python 3.10+**
- **PostgreSQL** instalado y con un usuario + base de datos creados.
- Opcional pero recomendado: **Docker** y **Docker Compose**.

---

## 🔧 Configuración local (sin Docker)

1. **Clonar el repositorio**

```bash
git clone https://github.com/nicolasegpla/gestion-de-proyectos.git
cd gestion-de-proyectos
```

2. **Crear y activar un entorno virtual**

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
# .\venv\Scripts\activate  # Windows PowerShell
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

Crea un archivo `.env` en la raíz del proyecto con, al menos:

```env
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:5432/DB_NAME
SECRET_KEY=una_clave_secreta_larga_y_unica
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> Ajusta `USER`, `PASSWORD`, `HOST` y `DB_NAME` según tu configuración de PostgreSQL.

5. **Ejecutar migraciones con Alembic**

```bash
alembic upgrade head
```

Esto creará todas las tablas necesarias en la base de datos apuntada por `DATABASE_URL`.

6. **Levantar la API en local**

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en:

- `http://localhost:8000`
- Documentación interactiva: `http://localhost:8000/docs`

---

## 🐳 Ejecución con Docker

1. **Construir la imagen**

```bash
docker build -t gestion-proyectos-api .
```

2. **Ejecutar el contenedor**

```bash
docker run -d --name gestion-proyectos-api -p 8000:8000 \
  --env-file .env \
  gestion-proyectos-api
```

3. **Verificar que está arriba**

- API: `http://localhost:8000/test`
- Docs: `http://localhost:8000/docs`

> Recuerda que el contenedor también debe poder conectarse a tu instancia de PostgreSQL (local, en otra máquina o en la nube).

---

## 🚀 Uso típico

1. Registrar una empresa (`POST /auth/registro`).
2. Hacer login con la empresa (`POST /auth/login`) y obtener el token JWT.
3. Consumir los endpoints de proyectos, historias de usuario y tickets enviando el header:

```http
Authorization: Bearer <TOKEN_JWT>
```

De esta forma todo el flujo se mantiene aislado por empresa.

---

## 🗺️ Roadmap (ideas futuras)

- Gestión completa de usuarios internos por empresa (roles, permisos).
- Estados personalizados de proyecto e historia de usuario.
- Filtros avanzados y paginación en listados.
- Webhooks/eventos para integraciones con otras herramientas.
- Scripts de despliegue listos para Docker Compose, DigitalOcean, EC2, etc.

---

## 📄 Licencia

Proyecto creado con fines educativos y de práctica.  
Puedes usarlo como base para tus propios experimentos y adaptarlo a tus necesidades.
