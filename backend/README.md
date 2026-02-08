# Medical Appointment Platform - Backend

API REST profesional para gestión de citas médicas construida con **FastAPI** y arquitectura multicapa, implementando patrones de diseño empresariales.

---

## Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Stack Tecnológico](#-stack-tecnológico)
- [Arquitectura](#-arquitectura)
- [Patrones de Diseño](#-patrones-de-diseño)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Bases de Datos](#-bases-de-datos)
- [Testing](#-testing)
- [Despliegue](#-despliegue)

---

## ✨ Características Principales

- ✅ **Autenticación y Autorización** basada en sesiones con Redis
- ✅ **Multi-base de datos**: PostgreSQL (relacional) + MongoDB (NoSQL)
- ✅ **Gestión de Citas Médicas** completa
- ✅ **Roles de Usuario**: Admin, Doctor, Paciente
- ✅ **Service Registry** para descubrimiento de servicios
- ✅ **Circuit Breaker** para resiliencia
- ✅ **Observabilidad** con logging estructurado
- ✅ **Cache** con Redis para optimización de rendimiento
- ✅ **Validación** con Pydantic
- ✅ **CORS** configurado para desarrollo y producción

---

## 🛠 Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.11 | Lenguaje de programación |
| **FastAPI** | Latest | Framework web asíncrono |
| **Uvicorn** | Latest | Servidor ASGI |
| **SQLAlchemy** | Latest | ORM para PostgreSQL |
| **PostgreSQL** | 15 | Base de datos relacional |
| **MongoDB** | 7 | Base de datos NoSQL |
| **Redis** | 7 | Cache y sesiones |
| **PyMongo** | Latest | Driver para MongoDB |
| **Pydantic** | Latest | Validación de datos |
| **Bcrypt** | 4.0.1 | Hashing de contraseñas |
| **Python-JOSE** | Latest | JWT y criptografía |

---

## 🏗 Arquitectura

### Arquitectura Multicapa

```
┌─────────────────────────────────────────────┐
│         Presentation Layer (Routes)          │
│  - REST API Endpoints                        │
│  - Request/Response DTOs                     │
│  - Middlewares (Auth, CORS, Logging)         │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Application Layer (Services)         │
│  - Business Logic                            │
│  - DTO Transformations                       │
│  - Use Cases                                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│            Domain Layer (Entities)           │
│  - Business Entities                         │
│  - Domain Services                           │
│  - Business Rules                            │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│       Infrastructure Layer (Data Access)     │
│  - DAO Implementations (PostgreSQL/MongoDB)  │
│  - Database Models                           │
│  - External Services Integration             │
└─────────────────────────────────────────────┘
```

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Auth       │  │  Appointment │  │   Reports    │      │
│  │   Routes     │  │   Routes     │  │   Routes     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │               │
│  ┌──────▼──────────────────▼──────────────────▼───────┐      │
│  │            Service Layer / Business Logic          │      │
│  └──────┬──────────────────┬──────────────────┬───────┘      │
│         │                  │                  │               │
│  ┌──────▼───────┐   ┌──────▼───────┐  ┌──────▼───────┐      │
│  │ PostgreSQL   │   │   MongoDB    │  │    Redis     │      │
│  │     DAO      │   │     DAO      │  │    Cache     │      │
│  └──────────────┘   └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
         │                    │                   │
         ▼                    ▼                   ▼
   ┌──────────┐        ┌──────────┐       ┌──────────┐
   │PostgreSQL│        │ MongoDB  │       │  Redis   │
   └──────────┘        └──────────┘       └──────────┘
```

---

## Patrones de Diseño

### 1. **DAO (Data Access Object)**
Abstracción de la capa de persistencia con interfaces comunes.

```python
# Interfaces
src/infrastructure/dao/interfaces/
    - patient_dao.py
    - doctor_dao.py
    - appointment_dao.py

# Implementaciones PostgreSQL
src/infrastructure/dao/postgresql/
    - patient_dao_impl.py
    - doctor_dao_impl.py

# Implementaciones MongoDB
src/infrastructure/dao/mongodb/
    - medical_record_dao_impl.py
```

### 2. **DTO (Data Transfer Object)**
Objetos para transferencia de datos entre capas.

```python
src/application/dto/
    - authentication_dto.py
    - appointment_dto.py
```

### 3. **Service Registry**
Descubrimiento dinámico de servicios (PostgreSQL, MongoDB, Redis).

```python
src/infrastructure/registry/
    - service_registry.py
```

**Características:**
- ✅ Registro dinámico de servicios
- ✅ Health checks automáticos
- ✅ Heartbeat para verificar disponibilidad
- ✅ Fallback a configuración local

### 4. **Circuit Breaker**
Protección contra fallos en cascada.

```python
src/infrastructure/resilience/
    - circuit_breaker.py
```

**Estados:**
- 🟢 **CLOSED**: Operación normal
- 🟡 **OPEN**: Fallo detectado, rechaza peticiones
- 🔵 **HALF_OPEN**: Probando recuperación

### 5. **Repository Pattern**
Implementado a través de DAOs para abstraer la persistencia.

### 6. **Dependency Injection**
Uso de FastAPI Depends para inyección de dependencias.

---

## Estructura del Proyecto

```
backend/
├── src/
│   ├── main.py                      # Punto de entrada de la aplicación
│   │
│   ├── application/                 # Capa de aplicación
│   │   ├── dto/                     # Data Transfer Objects
│   │   │   ├── authentication_dto.py
│   │   │   └── appointment_dto.py
│   │   └── services/                # Servicios de aplicación
│   │
│   ├── domain/                      # Capa de dominio
│   │   ├── entities/                # Entidades de negocio
│   │   └── services/                # Servicios de dominio
│   │       ├── authentication_service.py
│   │       └── appointment_service.py
│   │
│   ├── infrastructure/              # Capa de infraestructura
│   │   ├── cache/                   # Implementación de cache
│   │   │   ├── redis_client.py
│   │   │   └── session_repository.py
│   │   │
│   │   ├── dao/                     # Data Access Objects
│   │   │   ├── interfaces/          # Interfaces abstractas
│   │   │   ├── postgresql/          # Implementaciones PostgreSQL
│   │   │   └── mongodb/             # Implementaciones MongoDB
│   │   │
│   │   ├── models/                  # Modelos de datos
│   │   │   ├── postgresql/          # Modelos SQLAlchemy
│   │   │   │   └── models.py
│   │   │   └── mongodb/             # Esquemas MongoDB
│   │   │       └── medical_record.py
│   │   │
│   │   ├── observability/           # Logging y monitoreo
│   │   │   └── logger.py
│   │   │
│   │   ├── registry/                # Service Registry
│   │   │   └── service_registry.py
│   │   │
│   │   ├── resilience/              # Patrones de resiliencia
│   │   │   └── circuit_breaker.py
│   │   │
│   │   └── session/                 # Gestión de sesiones
│   │       └── session_manager.py
│   │
│   ├── presentation/                # Capa de presentación
│   │   ├── routes/                  # Endpoints de la API
│   │   │   ├── auth_routes.py
│   │   │   ├── appointment_routes.py
│   │   │   ├── patient_routes.py
│   │   │   ├── doctor_routes.py
│   │   │   └── report_routes.py
│   │   │
│   │   └── middlewares/             # Middlewares
│   │       ├── session_auth_middleware.py
│   │       └── error_logging_middleware.py
│   │
│   ├── config/                      # Configuración
│   │   └── database.py              # Conexiones a bases de datos
│   │
│   └── utils/                       # Utilidades
│       └── security.py              # Funciones de seguridad
│
├── tests/                           # Tests unitarios e integración
├── scripts/                         # Scripts de utilidad
├── requirements.txt                 # Dependencias Python
├── Dockerfile                       # Configuración Docker
└── README.md                        # Este archivo
```

---

## Requisitos

### Desarrollo Local
- Python 3.11+
- PostgreSQL 15+
- MongoDB 7+
- Redis 7+

### Producción (Docker)
- Docker 20.10+
- Docker Compose 2.0+

---

## Instalación

### Opción 1: Docker (Recomendado)

```bash
# Clonar el repositorio
git clone <repository-url>
cd backend

# Construir y levantar servicios
docker-compose up --build

# La API estará disponible en http://localhost:8000
```

### Opción 2: Desarrollo Local

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar bases de datos (ver sección Configuración)

# Ejecutar aplicación
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ⚙️ Configuración

### Variables de Entorno

El sistema utiliza Service Registry con fallback a variables de entorno:

```bash
# PostgreSQL
DATABASE_URL=postgresql://medical_user:medical_pass@localhost:5432/medical_appointments

# MongoDB
MONGODB_URL=mongodb://mongo_user:mongo_pass@localhost:27017/

# Redis
REDIS_URL=redis://localhost:6379/0

# Sesiones
SESSION_EXPIRE_MINUTES=60
```

### Configuración de Docker Compose

El archivo `docker-compose.yml` configura automáticamente:
- PostgreSQL en puerto 5432
- MongoDB en puerto 27017
- Redis en puerto 6379
- Backend en puerto 8000

**Credenciales por defecto:**
```yaml
PostgreSQL:
  user: medical_user
  password: medical_pass
  database: medical_appointments

MongoDB:
  user: mongo_user
  password: mongo_pass
  database: medical_records

Redis:
  No requiere autenticación por defecto
```

### Inicialización de Base de Datos

Las tablas de PostgreSQL se crean automáticamente al iniciar la aplicación.

**Datos de prueba (opcional):**
```bash
# Crear usuario admin manualmente
python scripts/create_admin.py
```

---

## Uso

### Ejecutar en Desarrollo

```bash
# Con Docker
docker-compose up

# Sin Docker
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Acceder a la Documentación

FastAPI genera documentación automática:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Verificar Estado de Servicios

```bash
# Health check
curl http://localhost:8000/health

# Service Registry status
curl http://localhost:8000/
```

---

## API Endpoints

### Autenticación (`/api/auth`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/register` | Registrar nuevo usuario | No |
| POST | `/login` | Iniciar sesión | No |
| POST | `/logout` | Cerrar sesión | Sí |
| GET | `/me` | Obtener usuario actual | Sí |

### Citas (`/api/appointments`)

| Método | Endpoint | Descripción | Auth | Rol |
|--------|----------|-------------|------|-----|
| GET | `/my-appointments` | Listar mis citas | Sí | Todos |
| POST | `/` | Crear cita | Sí | Paciente |
| GET | `/{id}` | Obtener cita | Sí | Todos |
| PATCH | `/{id}/status` | Actualizar estado | Sí | Doctor |

### Pacientes (`/api/patients`)

| Método | Endpoint | Descripción | Auth | Rol |
|--------|----------|-------------|------|-----|
| GET | `/me` | Mi perfil y estadísticas | Sí | Paciente |
| GET | `/medical-records` | Historial médico | Sí | Paciente |

### Doctores (`/api/doctors`)

| Método | Endpoint | Descripción | Auth | Rol |
|--------|----------|-------------|------|-----|
| GET | `/me` | Mi perfil y estadísticas | Sí | Doctor |
| GET | `/` | Listar doctores | No | - |
| GET | `/{id}` | Obtener doctor | No | - |
| GET | `/{id}/schedule` | Horarios del doctor | No | - |
| GET | `/specialties/list` | Listar especialidades | No | - |

### Reportes (`/api/reports`)

| Método | Endpoint | Descripción | Auth | Rol |
|--------|----------|-------------|------|-----|
| GET | `/system` | Reporte general del sistema | Sí | Admin |

---

## 🗄️ Bases de Datos

### PostgreSQL (Datos Relacionales)

**Tablas principales:**
- `users` - Usuarios del sistema
- `patients` - Información de pacientes
- `doctors` - Información de médicos
- `specialties` - Especialidades médicas
- `schedules` - Horarios de doctores
- `appointments` - Citas médicas

**Relaciones:**
```
users 1---* patients
users 1---* doctors
doctors *---1 specialties
doctors 1---* schedules
doctors 1---* appointments
patients 1---* appointments
```

### MongoDB (Datos No Estructurados)

**Colecciones:**
- `medical_records` - Registros médicos de pacientes
  - Campos dinámicos
  - Historial clínico
  - Notas del doctor

### Redis (Cache y Sesiones)

**Estructura:**
- `session:{session_id}` - Datos de sesión
  - TTL: 60 minutos
  - Almacena: user_id, role, username

---

## Testing

```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=src tests/

# Tests específicos
pytest tests/test_authentication.py
```

---

## Despliegue

### Producción con Docker

```bash
# Construir imagen
docker build -t medical-backend:latest .

# Ejecutar contenedor
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=<production-db-url> \
  -e MONGODB_URL=<production-mongo-url> \
  -e REDIS_URL=<production-redis-url> \
  medical-backend:latest
```

### Consideraciones de Producción

- ✅ Usar variables de entorno para credenciales
- ✅ Configurar HTTPS/SSL
- ✅ Implementar rate limiting
- ✅ Configurar backups automáticos
- ✅ Monitoreo con logs estructurados
- ✅ Usar secrets management (AWS Secrets Manager, etc.)

---

## Logs

Sistema de logging estructurado en JSON:

```json
{
  "timestamp": "2026-02-08T19:13:35.767210",
  "level": "INFO",
  "message": "Session retrieved",
  "module": "session_repository",
  "function": "get_session",
  "session_id": "74d179f7-e458-4087-96a9-0d314431676a",
  "user_id": "14"
}
```

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---


## 👥 Autores

 - Aucancela Andrés
 - Ponce Joseph
 - Villareal Jhonatan
---
---

## Soporte

Para soporte técnico o preguntas:
- Abrir un issue en GitHub
- Contactar al equipo de desarrollo

---

## Enlaces Útiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [Redis Python Client](https://redis-py.readthedocs.io/)