# 🔧 GUÍA DE INTEGRACIÓN DE COMPONENTES NUEVOS

Esta guía explica **dónde colocar cada archivo** en tu proyecto existente.

---

## 📂 PASO 1: BACKEND - Archivos Nuevos

### 1.1 Infrastructure - Registry (Service Registry Mejorado)

Copiar estos archivos a `backend/src/infrastructure/registry/`:

```bash
backend/src/infrastructure/registry/
├── service_registry.py          # ✨ REEMPLAZAR archivo existente
├── health_monitor.py            # 🆕 NUEVO
└── notification_service.py      # 🆕 NUEVO
```

**Contenido:**
- `service_registry.py` → Archivo generado (con historial MongoDB y notificaciones)
- `health_monitor.py` → (Opcional, para health checks avanzados)
- `notification_service.py` → Archivo generado (notificaciones email/SMS)

### 1.2 Infrastructure - Resilience (Circuit Breaker Mejorado)

Copiar a `backend/src/infrastructure/resilience/`:

```bash
backend/src/infrastructure/resilience/
└── circuit_breaker.py           # ✨ REEMPLAZAR archivo existente
```

**Contenido:**
- `circuit_breaker.py` → Archivo generado (con métricas y estados)

### 1.3 Infrastructure - External (Servicio Web B)

**CREAR NUEVA CARPETA:** `backend/src/infrastructure/external/`

```bash
backend/src/infrastructure/external/
└── web_service_b.py             # 🆕 NUEVO
```

**Contenido:**
- `web_service_b.py` → Archivo generado (simulador de fallos)

### 1.4 Infrastructure - Models MongoDB

Copiar a `backend/src/infrastructure/models/mongodb/`:

```bash
backend/src/infrastructure/models/mongodb/
└── service_history.py           # 🆕 NUEVO
```

**Contenido:**
- `service_history.py` → Archivo generado (modelos para historial)

### 1.5 Presentation - Routes (APIs de Monitoreo y Demo)

Copiar a `backend/src/presentation/routes/`:

```bash
backend/src/presentation/routes/
├── monitoring_routes.py         # 🆕 NUEVO
└── demo_routes.py               # 🆕 NUEVO
```

**Contenido:**
- `monitoring_routes.py` → Archivo generado (API Service Registry + Circuit Breaker)
- `demo_routes.py` → Archivo generado (API de demostración Circuit Breaker)

### 1.6 Main Application

Copiar a `backend/src/`:

```bash
backend/src/
└── main.py                      # ✨ REEMPLAZAR archivo existente
```

**Contenido:**
- `main.py` → Archivo generado (con imports y configuración nueva)

### 1.7 Configuración

Copiar a `backend/`:

```bash
backend/
├── requirements.txt             # ✨ REEMPLAZAR archivo existente
└── .env.example                 # 🆕 NUEVO
```

**Contenido:**
- `requirements.txt` → Archivo generado (con dependencias nuevas)
- `.env.example` → Archivo generado (template de variables)

---

## 📂 PASO 2: FRONTEND - Dashboards

### 2.1 Pages (Dashboards Nuevos)

**CREAR CARPETA si no existe:** `frontend/src/pages/`

Copiar a `frontend/src/pages/`:

```bash
frontend/src/pages/
├── ServiceRegistryDashboard.jsx  # 🆕 NUEVO
└── CircuitBreakerDashboard.jsx   # 🆕 NUEVO
```

**Contenido:**
- `ServiceRegistryDashboard.jsx` → Archivo generado
- `CircuitBreakerDashboard.jsx` → Archivo generado

### 2.2 Actualizar App.jsx

**MODIFICAR:** `frontend/src/App.jsx`

Agregar las siguientes rutas:

```jsx
import ServiceRegistryDashboard from './pages/ServiceRegistryDashboard';
import CircuitBreakerDashboard from './pages/CircuitBreakerDashboard';

// ... dentro de tus rutas
<Route path="/service-registry" element={<ServiceRegistryDashboard />} />
<Route path="/circuit-breaker" element={<CircuitBreakerDashboard />} />
```

**O si usas un layout/navbar, agregar los enlaces:**

```jsx
<nav>
  {/* ... enlaces existentes */}
  <Link to="/service-registry">Service Registry</Link>
  <Link to="/circuit-breaker">Circuit Breaker</Link>
</nav>
```

---

## 📂 PASO 3: DOCKER

### 3.1 Docker Compose

Copiar a raíz del proyecto:

```bash
./
└── docker-compose.yml           # ✨ REEMPLAZAR archivo existente
```

**Contenido:**
- `docker-compose.yml` → Archivo generado (con healthchecks y variables nuevas)

---

## 🔄 PASO 4: INSTALACIÓN DE DEPENDENCIAS

### 4.1 Backend

```bash
cd backend

# Instalar dependencias nuevas
pip install -r requirements.txt

# O si usas Docker, reconstruir:
cd ..
docker-compose build backend
```

**Dependencias nuevas agregadas:**
- `sendgrid` - Notificaciones por email
- `twilio` - Notificaciones por SMS (opcional)
- `prometheus-client` - Métricas
- `python-json-logger` - Logging mejorado
- `pybreaker` - Circuit breaker pattern
- `tenacity` - Retry logic
- `httpx` - HTTP client
- `websockets` - Para dashboards en tiempo real

### 4.2 Frontend

```bash
cd frontend

# Instalar dependencias (ya deberían estar instaladas)
npm install

# O si usas Docker, reconstruir:
cd ..
docker-compose build frontend
```

---

## ⚙️ PASO 5: CONFIGURACIÓN

### 5.1 Variables de Entorno

```bash
# 1. Copiar template
cp backend/.env.example backend/.env

# 2. Editar con tu configuración
nano backend/.env
```

**Configuración MÍNIMA requerida:**

```bash
# OBLIGATORIO: Cambiar esta IP por la de tu red
LAN_HOST_IP=192.168.1.7  # ← CAMBIAR

# Bases de datos (ya configuradas por docker-compose)
DATABASE_URL=postgresql://medical_user:medical_pass@postgres:5432/medical_appointments
MONGODB_URL=mongodb://mongo_user:mongo_pass@mongodb:27017/
REDIS_URL=redis://redis:6379/0

# Monitoreo
HEALTH_CHECK_INTERVAL=30
HEARTBEAT_INTERVAL=10

# Circuit Breaker
CIRCUIT_BREAKER_FAILURE_THRESHOLD=5
CIRCUIT_BREAKER_TIMEOUT=30
```

**Configuración OPCIONAL (notificaciones):**

```bash
# SendGrid (para emails)
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=notifications@medical-system.com
NOTIFICATION_EMAIL=admin@medical-system.com

# Twilio (para SMS)
TWILIO_ACCOUNT_SID=ACxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1234567890
```

### 5.2 Actualizar docker-compose.yml

**Editar línea 94 en docker-compose.yml:**

```yaml
frontend:
  # ...
  environment:
    VITE_API_URL: http://192.168.1.7:8000  # ← CAMBIAR por tu IP
```

---

## 🚀 PASO 6: LEVANTAR EL SISTEMA

```bash
# En la raíz del proyecto

# 1. Detener servicios actuales (si están corriendo)
docker-compose down

# 2. Reconstruir imágenes
docker-compose build

# 3. Levantar todo
docker-compose up -d

# 4. Ver logs
docker-compose logs -f
```

**Verificar que todo funciona:**

```bash
# Verificar contenedores
docker-compose ps

# Deberías ver:
# ✅ medical_postgres  (healthy)
# ✅ medical_mongodb   (healthy)
# ✅ medical_redis     (healthy)
# ✅ medical_backend   (healthy)
# ✅ medical_frontend  (up)
```

**Verificar endpoints:**

```bash
# Health check
curl http://localhost:8000/health

# Service Registry
curl http://localhost:8000/monitoring/registry/services

# Circuit Breaker
curl http://localhost:8000/monitoring/circuit-breakers
```

---

## 📊 PASO 7: ACCEDER A LOS DASHBOARDS

### Service Registry Dashboard
```
http://localhost:5173/service-registry
# o desde LAN:
http://192.168.X.X:5173/service-registry
```

### Circuit Breaker Dashboard
```
http://localhost:5173/circuit-breaker
# o desde LAN:
http://192.168.X.X:5173/circuit-breaker
```

### API Documentation
```
http://localhost:8000/docs
# o desde LAN:
http://192.168.X.X:8000/docs
```

---

## ✅ CHECKLIST DE INTEGRACIÓN

Verificar que todos estos archivos están en su lugar:

### Backend
- [ ] `backend/src/main.py` (actualizado)
- [ ] `backend/src/infrastructure/registry/service_registry.py` (actualizado)
- [ ] `backend/src/infrastructure/registry/notification_service.py` (nuevo)
- [ ] `backend/src/infrastructure/resilience/circuit_breaker.py` (actualizado)
- [ ] `backend/src/infrastructure/external/web_service_b.py` (nuevo)
- [ ] `backend/src/infrastructure/models/mongodb/service_history.py` (nuevo)
- [ ] `backend/src/presentation/routes/monitoring_routes.py` (nuevo)
- [ ] `backend/src/presentation/routes/demo_routes.py` (nuevo)
- [ ] `backend/requirements.txt` (actualizado)
- [ ] `backend/.env.example` (nuevo)
- [ ] `backend/.env` (creado y configurado)

### Frontend
- [ ] `frontend/src/pages/ServiceRegistryDashboard.jsx` (nuevo)
- [ ] `frontend/src/pages/CircuitBreakerDashboard.jsx` (nuevo)
- [ ] `frontend/src/App.jsx` (actualizado con rutas)

### Docker
- [ ] `docker-compose.yml` (actualizado con IP LAN)

### Variables de Entorno
- [ ] IP LAN configurada en `backend/.env`
- [ ] IP LAN configurada en `docker-compose.yml` (línea 94)

---

## 🔍 TROUBLESHOOTING

### Error: Imports no encontrados

```bash
# Verificar que requirements.txt está actualizado
cd backend
pip install -r requirements.txt --break-system-packages

# O reconstruir contenedor
docker-compose build backend
```

### Error: Rutas no encontradas en frontend

```bash
# Verificar que App.jsx tiene las rutas correctas
cat frontend/src/App.jsx | grep -A2 "service-registry"
cat frontend/src/App.jsx | grep -A2 "circuit-breaker"
```

### Error: Cannot find module

```bash
# Reconstruir frontend
cd frontend
npm install
cd ..
docker-compose build frontend
```

### Error: MongoDB connection failed

```bash
# Verificar que MongoDB está corriendo
docker-compose ps mongodb

# Reiniciar MongoDB
docker-compose restart mongodb
```

---

## 📞 AYUDA ADICIONAL

Si tienes problemas con la integración:

1. **Verificar logs:**
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

2. **Verificar estructura:**
   ```bash
   tree backend/src/infrastructure/
   tree frontend/src/pages/
   ```

3. **Limpiar y reconstruir:**
   ```bash
   docker-compose down -v
   docker-compose build --no-cache
   docker-compose up -d
   ```

---

**Versión:** 2.0.0  
**Autores:** Aucancela, Ponce, Villareal