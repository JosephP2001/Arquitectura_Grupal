# Sistema de Reservas Médicas

Sistema de gestión de citas médicas con arquitectura de microservicios usando **Service Registry** y **Circuit Breaker**.

## 🏗️ Arquitectura

- **Backend**: FastAPI + PostgreSQL + MongoDB + Redis
- **Frontend**: React + Vite + TailwindCSS
- **Patrones**: Service Registry + Circuit Breaker
- **Containerización**: Docker + Docker Compose

## 📋 Requisitos Previos

- Docker Desktop instalado
- Docker Compose instalado
- Puertos disponibles: 5432, 27017, 6379, 8000, 5173

## 🚀 Instalación

### 1. Clonar y preparar el proyecto

```bash
cd Reservas\ medicas
```

### 2. Iniciar los servicios con Docker

```bash
docker-compose up -d
```

Esto iniciará:
- ✅ PostgreSQL (puerto 5432)
- ✅ MongoDB (puerto 27017)
- ✅ Redis (puerto 6379)
- ✅ Backend API (puerto 8000)
- ✅ Frontend (puerto 5173)

### 3. Verificar que los servicios estén corriendo

```bash
docker-compose ps
```

Todos los servicios deben estar en estado "Up".

### 4. Crear datos de prueba

```bash
docker-compose exec backend python scripts/init_data.py
```

## 🌐 Acceso en LAN

### Para el Backend:

El backend está configurado para aceptar conexiones desde cualquier IP en la red local.

### Para el Frontend:

1. **Encuentra la IP de tu máquina**:
   - Windows: `ipconfig` → busca "IPv4 Address"
   - Linux/Mac: `ifconfig` o `ip addr`

2. **Edita `docker-compose.yml`** y cambia `VITE_API_URL`:

```yaml
frontend:
  environment:
    VITE_API_URL: http://TU_IP_LOCAL:8000  # Ejemplo: http://192.168.1.100:8000
```

3. **Reinicia el frontend**:

```bash
docker-compose restart frontend
```

4. **Accede desde cualquier dispositivo en la red**:
   - Frontend: `http://TU_IP_LOCAL:5173`
   - Backend API: `http://TU_IP_LOCAL:8000`
   - Documentación API: `http://TU_IP_LOCAL:8000/docs`

## 📱 Credenciales de Prueba

### Administrador
- Usuario: `admin`
- Contraseña: `admin123`

### Pacientes
- Usuario: `paciente1` / Contraseña: `pass123`
- Usuario: `paciente2` / Contraseña: `pass123`

### Médicos
- Usuario: `doctor1` / Contraseña: `doc123`
- Usuario: `doctor2` / Contraseña: `doc123`

## 🔍 Endpoints Principales

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar nuevo usuario
- `GET /api/auth/me` - Obtener usuario actual
- `POST /api/auth/logout` - Cerrar sesión

### Médicos
- `GET /api/doctors/` - Listar médicos
- `GET /api/doctors/{id}` - Obtener médico
- `GET /api/doctors/{id}/schedule` - Horarios del médico
- `GET /api/doctors/specialties/list` - Listar especialidades

### Citas
- `POST /api/appointments/` - Crear cita
- `GET /api/appointments/my-appointments` - Mis citas
- `PATCH /api/appointments/{id}/status` - Actualizar estado

### Reportes
- `GET /api/reports/patient/{id}` - Reporte completo de paciente
- `GET /api/reports/system` - Reporte del sistema
- `GET /api/reports/doctor/{id}/performance` - Desempeño del médico

## 🔧 Verificación de Servicios

### Health Check
```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "services": {
    "postgres": "UP",
    "mongo": "UP",
    "redis": "UP"
  }
}
```

### Service Registry
El Service Registry monitorea automáticamente el estado de:
- PostgreSQL
- MongoDB
- Redis

### Circuit Breaker
Protege las conexiones a:
- Redis (sesiones)
- PostgreSQL (datos relacionales)
- MongoDB (historiales médicos)

## 📊 Estructura del Proyecto

```
backend/
├── src/
│   ├── application/
│   │   └── dto/                    # Data Transfer Objects
│   ├── config/
│   │   └── database.py            # Configuración de BD
│   ├── domain/
│   │   └── services/              # Lógica de negocio
│   ├── infrastructure/
│   │   ├── cache/                 # Redis
│   │   ├── dao/                   # Data Access Objects
│   │   ├── models/                # Modelos de BD
│   │   ├── observability/         # Logging
│   │   ├── registry/              # Service Registry
│   │   ├── resilience/            # Circuit Breaker
│   │   └── session/               # Gestión de sesiones
│   ├── presentation/
│   │   ├── middlewares/           # Middlewares
│   │   └── routes/                # Endpoints API
│   └── main.py                    # Punto de entrada
├── scripts/
│   └── init_data.py               # Script de datos de prueba
├── Dockerfile
└── requirements.txt

frontend/
├── src/
│   ├── components/                # Componentes React
│   ├── context/                   # Context API
│   ├── pages/                     # Páginas
│   ├── services/                  # Servicios API
│   └── App.jsx
├── Dockerfile
└── package.json
```

## 🛠️ Comandos Útiles

### Ver logs
```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### Reiniciar servicios
```bash
# Todos
docker-compose restart

# Solo backend
docker-compose restart backend
```

### Detener servicios
```bash
docker-compose down
```

### Limpiar volúmenes (⚠️ ELIMINA DATOS)
```bash
docker-compose down -v
```

## 🐛 Troubleshooting

### Error: Puerto 5432 ya en uso
```bash
# Detener PostgreSQL local
sudo systemctl stop postgresql
```

### Error: No se puede conectar a Redis
```bash
# Verificar que Redis está corriendo
docker-compose ps redis

# Ver logs de Redis
docker-compose logs redis
```

### Error: 404 en /api/auth/register
- Verifica que el backend esté corriendo
- Revisa que las rutas estén registradas en `main.py`

### Frontend no conecta con Backend en LAN
1. Verifica la IP local con `ipconfig` o `ifconfig`
2. Actualiza `VITE_API_URL` en `docker-compose.yml`
3. Reinicia el frontend: `docker-compose restart frontend`
4. Verifica el firewall (debe permitir puertos 8000 y 5173)

## 📝 Notas Importantes

- Las sesiones se almacenan en Redis con TTL de 1 hora
- Las contraseñas se hashean con bcrypt
- CORS está configurado para aceptar conexiones de LAN
- El Service Registry hace heartbeat cada 10 segundos
- El Circuit Breaker se abre tras 3 fallos consecutivos

## 🔒 Seguridad en Producción

Para producción, cambiar:
1. Contraseñas de bases de datos
2. `secure=True` en cookies (requiere HTTPS)
3. Configurar CORS con dominios específicos
4. Usar variables de entorno para secretos
5. Activar SSL/TLS

## 📞 Soporte

Para reportar problemas o solicitar ayuda, contactar al equipo de desarrollo.