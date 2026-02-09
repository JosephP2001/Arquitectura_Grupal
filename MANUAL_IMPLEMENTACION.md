# 📘 MANUAL DE IMPLEMENTACIÓN - MEDICAL APPOINTMENT PLATFORM V2.0

## 🎯 PATRONES IMPLEMENTADOS

### ✅ Patrón 1: Service Registry con Monitoreo
- **Descripción:** Sistema completo de registro y monitoreo de servicios (PostgreSQL, MongoDB, Redis)
- **Características:**
  - Health checks automáticos cada 30 segundos
  - Historial de estados almacenado en MongoDB
  - Notificaciones por email cuando servicios caen/recuperan
  - Dashboard web interactivo en tiempo real
  - Métricas de uptime, latencia y disponibilidad

### ✅ Patrón 2: Circuit Breaker con Demostración
- **Descripción:** Implementación completa del patrón Circuit Breaker con escenarios de demostración
- **Características:**
  - Estados: CLOSED, OPEN, HALF_OPEN
  - Servicio Web B simulado con modos de fallo configurables
  - Servicio Web A que consume Web B protegido por Circuit Breaker
  - Dashboard interactivo con métricas en tiempo real
  - Cola de peticiones y fallback automático
  - Métricas de performance y tasa de fallos

---

## 🖥️ REQUISITOS DEL SISTEMA

### Hardware Mínimo
- CPU: 4 cores
- RAM: 8 GB
- Disco: 10 GB libres

### Software Requerido
```
✅ Docker 20.10+ (instalar desde https://docker.com)
✅ Docker Compose 2.0+
✅ Navegador web moderno (Chrome, Firefox, Edge)
```

### Puertos Necesarios
Los siguientes puertos deben estar disponibles:
- `5432` - PostgreSQL
- `27017` - MongoDB
- `6379` - Redis
- `8000` - Backend FastAPI
- `5173` - Frontend React

---

## 📦 ESTRUCTURA DEL PROYECTO

```
medical-appointment-platform/
├── backend/
│   ├── src/
│   │   ├── main.py                              # ✨ ACTUALIZADO
│   │   ├── config/
│   │   │   └── database.py
│   │   ├── infrastructure/
│   │   │   ├── registry/
│   │   │   │   ├── service_registry.py          # ✨ MEJORADO
│   │   │   │   ├── health_monitor.py            # 🆕 NUEVO
│   │   │   │   └── notification_service.py      # 🆕 NUEVO
│   │   │   ├── resilience/
│   │   │   │   └── circuit_breaker.py           # ✨ MEJORADO
│   │   │   ├── external/
│   │   │   │   └── web_service_b.py             # 🆕 NUEVO
│   │   │   └── models/
│   │   │       └── mongodb/
│   │   │           └── service_history.py       # 🆕 NUEVO
│   │   └── presentation/
│   │       └── routes/
│   │           ├── monitoring_routes.py         # 🆕 NUEVO
│   │           └── demo_routes.py               # 🆕 NUEVO
│   ├── requirements.txt                         # ✨ ACTUALIZADO
│   ├── Dockerfile
│   └── .env.example                             # 🆕 NUEVO
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── ServiceRegistryDashboard.jsx     # 🆕 NUEVO
│   │   │   └── CircuitBreakerDashboard.jsx      # 🆕 NUEVO
│   │   └── App.jsx                              # (agregar rutas)
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml                           # ✨ ACTUALIZADO
```

---

## 🚀 INSTALACIÓN Y DESPLIEGUE

### Paso 1: Preparar el Entorno

```bash
# 1. Clonar o descomprimir el proyecto
cd /ruta/al/proyecto

# 2. Verificar estructura de carpetas
ls -la
# Deberías ver: backend/, frontend/, docker-compose.yml

# 3. Dar permisos de ejecución (Linux/Mac)
chmod -R 755 backend/ frontend/
```

### Paso 2: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp backend/.env.example backend/.env

# Editar con tu IP de LAN
nano backend/.env
```

**⚠️ IMPORTANTE: Configurar la IP LAN**

Editar la siguiente línea en `backend/.env` y en `docker-compose.yml`:

```bash
# Encuentra tu IP local:
# Windows: ipconfig
# Linux/Mac: ifconfig o ip addr

# Luego edita:
LAN_HOST_IP=192.168.X.X  # ← Cambiar por tu IP real
```

**Ejemplo:**
Si tu IP es `192.168.1.105`, entonces:
```bash
LAN_HOST_IP=192.168.1.105
```

Y en `docker-compose.yml`, línea del frontend:
```yaml
VITE_API_URL: http://192.168.1.105:8000
```

### Paso 3: Levantar el Sistema

```bash
# En la raíz del proyecto

# Construir imágenes (primera vez o tras cambios)
docker-compose build

# Levantar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

**✅ Verificar que todo está corriendo:**
```bash
docker-compose ps
```

Deberías ver 5 contenedores en estado "Up":
- `medical_postgres`
- `medical_mongodb`
- `medical_redis`
- `medical_backend`
- `medical_frontend`

### Paso 4: Verificar Acceso

**Desde la máquina local:**
```
Frontend:     http://localhost:5173
Backend API:  http://localhost:8000/docs
Health Check: http://localhost:8000/health
```

**Desde cualquier dispositivo en la LAN:**
```
Frontend:     http://192.168.X.X:5173
Backend API:  http://192.168.X.X:8000/docs
Health Check: http://192.168.X.X:8000/health
```

---

## 📊 ACCESO A LOS DASHBOARDS

### 1️⃣ Service Registry Dashboard

**URL:** `http://192.168.X.X:5173/service-registry`

**Funcionalidades:**
- ✅ Estado actual de todos los servicios (PostgreSQL, MongoDB, Redis)
- ✅ Métricas de uptime y disponibilidad
- ✅ Historial de health checks
- ✅ Health check manual
- ✅ Auto-refresh cada 5 segundos

**Cómo usar:**
1. Abrir dashboard
2. Ver tarjetas de servicios con indicadores de estado (verde/rojo/amarillo)
3. Hacer clic en "Ver Historial" para ver eventos pasados
4. Usar "Health Check Manual" para forzar verificación inmediata

### 2️⃣ Circuit Breaker Dashboard

**URL:** `http://192.168.X.X:5173/circuit-breaker`

**Funcionalidades:**
- ✅ Estado del Circuit Breaker en tiempo real (CLOSED/OPEN/HALF_OPEN)
- ✅ Métricas de llamadas (exitosas/fallidas/rechazadas)
- ✅ Control de Service B (simulador de fallos)
- ✅ Tests automatizados
- ✅ Historial de llamadas recientes

**Cómo usar:**
1. Ver estado actual del Circuit Breaker (indicador grande con emoji)
2. Configurar Service B en diferentes modos (ver sección de escenarios)
3. Ejecutar tests con botones "Run X Requests"
4. Observar cambios de estado en tiempo real

### 3️⃣ API Documentation (Swagger)

**URL:** `http://192.168.X.X:8000/docs`

**Secciones nuevas:**
- **Monitoring:** Endpoints de Service Registry
- **Demo:** Endpoints de Circuit Breaker

---

## 🎬 ESCENARIOS DE DEMOSTRACIÓN

### 📍 ESCENARIO 1: Service Registry - Servicio Caído

**Objetivo:** Demostrar detección de fallos y notificaciones

**Pasos:**
```bash
# 1. Tener dashboard abierto: http://192.168.X.X:5173/service-registry

# 2. Detener PostgreSQL intencionalmente
docker stop medical_postgres

# 3. Esperar 30 segundos (siguiente health check)
# ✅ El dashboard mostrará PostgreSQL en rojo (DOWN)
# ✅ Se enviará notificación por email (si SendGrid configurado)
# ✅ El historial mostrará el cambio de estado

# 4. Recuperar servicio
docker start medical_postgres

# 5. Esperar 30 segundos
# ✅ El dashboard mostrará PostgreSQL en verde (UP)
# ✅ Se enviará notificación de recuperación
```

**Qué observar:**
- Cambio de color en tarjeta de servicio
- Entrada en historial con timestamp
- Métricas de uptime actualizadas
- (Opcional) Email de notificación recibido

---

### 📍 ESCENARIO 2: Circuit Breaker - Funcionamiento Normal

**Objetivo:** Demostrar Circuit Breaker en estado CLOSED

**Pasos:**
```bash
# 1. Abrir dashboard: http://192.168.X.X:5173/circuit-breaker

# 2. Configurar Service B en modo STABLE
#    - Hacer clic en botón "🟢 STABLE"

# 3. Ejecutar test
#    - Hacer clic en "Run 10 Requests"

# 4. Observar resultados:
```

**Qué observar:**
- Circuit Breaker permanece en estado CLOSED (🟢)
- Todas las peticiones exitosas (verde)
- Success rate cercano al 100%
- Response time bajo

---

### 📍 ESCENARIO 3: Circuit Breaker - Fallos Intermitentes

**Objetivo:** Demostrar transición a estado OPEN

**Pasos:**
```bash
# 1. Configurar Service B en modo INTERMITTENT
#    - Hacer clic en "🟡 INTERMITTENT"
#    - Ajustar failure rate a 50% (slider)

# 2. Ejecutar test
#    - Hacer clic en "Run 10 Requests"

# 3. Ejecutar otro test si no se abrió el circuito
#    - Hacer clic en "Run 10 Requests" nuevamente
```

**Qué observar:**
- Mezcla de peticiones exitosas (verde) y fallidas (rojo)
- Failure count incrementando
- Al llegar a 5 fallos → Circuit Breaker pasa a OPEN (🔴)
- Nuevas peticiones se rechazan inmediatamente (amarillo)
- NO llegan a Service B (protección activa)

**Resultado esperado:**
```
Estado inicial:  CLOSED 🟢
Tras 5 fallos:   OPEN 🔴
Peticiones:      RECHAZADAS (no llegan a Service B)
```

---

### 📍 ESCENARIO 4: Circuit Breaker - Service Completamente Caído

**Objetivo:** Demostrar apertura rápida del circuito

**Pasos:**
```bash
# 1. Resetear Circuit Breaker
#    - Hacer clic en "♻️ Reset Circuit Breaker"

# 2. Configurar Service B en modo FAILING
#    - Hacer clic en "🔴 FAILING"

# 3. Ejecutar test
#    - Hacer clic en "Run 10 Requests"
```

**Qué observar:**
- Primeras 5 peticiones fallan (rojo)
- Circuit Breaker pasa a OPEN inmediatamente
- Peticiones 6-10 son RECHAZADAS (amarillo)
- Service B muestra 5 fallos, NO 10 (protección funcionó)

---

### 📍 ESCENARIO 5: Circuit Breaker - Recuperación Automática

**Objetivo:** Demostrar estados HALF_OPEN y CLOSED

**Pasos:**
```bash
# 1. Tener Circuit Breaker en estado OPEN (desde escenario anterior)

# 2. Configurar Service B en modo STABLE
#    - Hacer clic en "🟢 STABLE"

# 3. ESPERAR 30 segundos (timeout configurado)
#    - Usar cronómetro o reloj

# 4. Hacer una petición (backend):
curl http://192.168.X.X:8000/demo/patient/1

# 5. El Circuit Breaker pasa a HALF_OPEN 🟡
#    - Permite 3 peticiones de prueba

# 6. Si las 3 peticiones son exitosas → CLOSED 🟢
```

**Qué observar:**
- Transición: OPEN → HALF_OPEN → CLOSED
- Solo 3 peticiones de prueba permitidas
- Si todas exitosas → circuito se cierra
- Si falla alguna → vuelve a OPEN

---

### 📍 ESCENARIO 6: Circuit Breaker - Servicio Lento (Timeout)

**Objetivo:** Demostrar detección de servicios lentos

**Pasos:**
```bash
# 1. Resetear Circuit Breaker

# 2. Configurar Service B en modo SLOW
#    - Hacer clic en "🔵 SLOW"
#    - Ajustar delay a 3 segundos

# 3. Ejecutar test
#    - Hacer clic en "Run 5 Requests"
```

**Qué observar:**
- Peticiones tardan ~3 segundos cada una
- Average response time incrementa significativamente
- Service sigue funcionando (no falla, solo es lento)

---

## 📧 CONFIGURACIÓN DE NOTIFICACIONES

### SendGrid (Email)

**Para habilitar notificaciones por email:**

1. Crear cuenta gratuita en SendGrid: https://signup.sendgrid.com/

2. Obtener API Key:
   - Settings → API Keys → Create API Key
   - Copiar la key (solo se muestra una vez)

3. Configurar en `backend/.env`:
```bash
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=notifications@tu-dominio.com
NOTIFICATION_EMAIL=tu-email@gmail.com
```

4. Reiniciar backend:
```bash
docker-compose restart backend
```

**⚠️ Nota:** Sin SendGrid configurado, el sistema funcionará pero las notificaciones se simularán (solo en logs).

### Twilio (SMS) - Opcional

Si deseas notificaciones por SMS:

1. Crear cuenta en Twilio: https://www.twilio.com/

2. Configurar en `backend/.env`:
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1234567890
```

3. Descomentar código en `notification_service.py` líneas 35-43 y 88-100

---

## 🔧 COMANDOS ÚTILES

### Docker

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend

# Reiniciar un servicio
docker-compose restart backend

# Detener todo
docker-compose down

# Detener y eliminar volúmenes (reset completo)
docker-compose down -v

# Reconstruir tras cambios
docker-compose up -d --build

# Ver estado de servicios
docker-compose ps

# Acceder a shell de un contenedor
docker exec -it medical_backend bash
```

### Base de Datos

```bash
# Acceder a PostgreSQL
docker exec -it medical_postgres psql -U medical_user -d medical_appointments

# Acceder a MongoDB
docker exec -it medical_mongodb mongosh -u mongo_user -p mongo_pass

# Acceder a Redis
docker exec -it medical_redis redis-cli
```

### Backend

```bash
# Ver logs del backend en tiempo real
docker-compose logs -f backend

# Reiniciar backend tras cambios en código
docker-compose restart backend

# Acceder a shell del backend
docker exec -it medical_backend bash

# Ver procesos de Python
docker exec medical_backend ps aux | grep python
```

---

## 🧪 TESTING DE API (Postman/curl)

### Service Registry

```bash
# Obtener todos los servicios
curl http://192.168.X.X:8000/monitoring/registry/services

# Obtener métricas
curl http://192.168.X.X:8000/monitoring/registry/metrics

# Health check manual
curl -X POST http://192.168.X.X:8000/monitoring/registry/health-check

# Historial de un servicio
curl http://192.168.X.X:8000/monitoring/registry/services/postgres/history
```

### Circuit Breaker

```bash
# Estado de circuit breakers
curl http://192.168.X.X:8000/monitoring/circuit-breakers

# Obtener datos de paciente (protegido por CB)
curl http://192.168.X.X:8000/demo/patient/1

# Configurar Service B en modo FAILING
curl -X POST "http://192.168.X.X:8000/demo/service-b/mode?mode=FAILING"

# Ejecutar test de 10 peticiones
curl -X POST "http://192.168.X.X:8000/demo/test-circuit-breaker?num_requests=10"

# Resetear circuit breaker
curl -X POST http://192.168.X.X:8000/monitoring/circuit-breakers/web_service_b/reset

# Estadísticas de Service B
curl http://192.168.X.X:8000/demo/service-b/statistics
```

---

## ❌ TROUBLESHOOTING

### Problema: Puerto ya en uso

```bash
# Ver qué proceso usa el puerto
# Linux/Mac:
lsof -i :8000
netstat -tuln | grep 8000

# Windows:
netstat -ano | findstr :8000

# Detener el servicio conflictivo o cambiar puerto en docker-compose.yml
```

### Problema: Contenedores no inician

```bash
# Ver logs completos
docker-compose logs

# Verificar recursos de Docker
docker system df

# Limpiar recursos no usados
docker system prune -a
```

### Problema: No se puede acceder desde LAN

```bash
# 1. Verificar IP correcta
ipconfig  # Windows
ifconfig  # Linux/Mac

# 2. Verificar firewall
# Permitir puertos 8000 y 5173 en firewall

# Windows:
netsh advfirewall firewall add rule name="Medical App" dir=in action=allow protocol=TCP localport=8000,5173

# 3. Verificar que docker-compose.yml tiene la IP correcta
```

### Problema: MongoDB no conecta

```bash
# Verificar que MongoDB está corriendo
docker-compose ps

# Reiniciar MongoDB
docker-compose restart mongodb

# Ver logs
docker-compose logs mongodb
```

### Problema: Frontend no carga

```bash
# Reconstruir frontend
docker-compose up -d --build frontend

# Verificar variables de entorno
docker exec medical_frontend env | grep VITE_API_URL

# Debería mostrar: VITE_API_URL=http://192.168.X.X:8000
```

---

## 📸 EVIDENCIAS PARA ENTREGA

### Capturas de Pantalla Recomendadas

1. **Service Registry Dashboard**
   - Todos los servicios en verde (UP)
   - Tabla de métricas con uptime
   - Historial de un servicio

2. **Circuit Breaker Dashboard**
   - Estado CLOSED funcionando normal
   - Estado OPEN tras fallos
   - Gráficas de success/failure rate
   - Tabla de recent calls

3. **Swagger Documentation**
   - Endpoints de `/monitoring`
   - Endpoints de `/demo`

4. **Logs del Sistema**
   - Output de `docker-compose logs` mostrando health checks
   - Notificaciones en consola

5. **Terminal**
   - `docker-compose ps` mostrando todos los servicios UP
   - Respuesta de health check endpoint

---

## 📝 CHECKLIST DE VALIDACIÓN

Antes de la defensa, verificar:

- [ ] Todos los contenedores están corriendo (`docker-compose ps`)
- [ ] Health check endpoint responde: `http://192.168.X.X:8000/health`
- [ ] Service Registry Dashboard accesible y mostrando servicios
- [ ] Circuit Breaker Dashboard accesible y funcional
- [ ] Se puede cambiar modo de Service B (STABLE/INTERMITTENT/FAILING)
- [ ] Circuit Breaker cambia de estado correctamente
- [ ] Se puede resetear Circuit Breaker
- [ ] Los tests de 5/10/20 peticiones funcionan
- [ ] El sistema es accesible desde otro dispositivo en la LAN
- [ ] Los logs muestran health checks automáticos cada 30s

---

## 📚 DOCUMENTACIÓN ADICIONAL

### Endpoints Importantes

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Health check del sistema |
| `/monitoring/registry/services` | GET | Listar servicios registrados |
| `/monitoring/registry/metrics` | GET | Métricas de servicios |
| `/monitoring/circuit-breakers` | GET | Estado de circuit breakers |
| `/demo/service-b/mode` | POST | Configurar modo de Service B |
| `/demo/test-circuit-breaker` | POST | Ejecutar test de CB |

### Variables de Entorno Críticas

```bash
# Backend
DATABASE_URL=postgresql://medical_user:medical_pass@postgres:5432/medical_appointments
MONGODB_URL=mongodb://mongo_user:mongo_pass@mongodb:27017/
REDIS_URL=redis://redis:6379/0
HEALTH_CHECK_INTERVAL=30
CIRCUIT_BREAKER_FAILURE_THRESHOLD=5
CIRCUIT_BREAKER_TIMEOUT=30

# Frontend
VITE_API_URL=http://192.168.X.X:8000
```

---

## 👥 AUTORES

- Aucancela Andrés
- Ponce Joseph
- Villareal Jhonatan

---

## 📞 SOPORTE

En caso de problemas durante la instalación o demostración, verificar:

1. Docker y Docker Compose están instalados y corriendo
2. Puertos 5432, 27017, 6379, 8000, 5173 están disponibles
3. IP LAN está correctamente configurada en `.env` y `docker-compose.yml`
4. Firewall permite conexiones en puertos 8000 y 5173

**Logs completos:**
```bash
docker-compose logs > logs_completos.txt
```

---

## 🎓 CRITERIOS DE EVALUACIÓN CUBIERTOS

### ✅ Service Registry
- [x] Múltiples servicios monitoreados (PostgreSQL, MongoDB, Redis)
- [x] Health checks automáticos periódicos
- [x] Dashboard/reporte con estado actual
- [x] Historial de estados y estadísticas
- [x] Sistema de notificaciones (email)
- [x] Detección de caídas y recuperaciones

### ✅ Circuit Breaker
- [x] Servicio Web B con fallos configurables
- [x] Servicio Web A consume Web B con Circuit Breaker
- [x] Estados CLOSED/OPEN/HALF_OPEN
- [x] Dashboard/reporte en tiempo real
- [x] Métricas de llamadas y rendimiento
- [x] Cola de peticiones pendientes (simulada en fallback)
- [x] Mensajes amigables al usuario

---

**Versión:** 2.0.0  
**Fecha:** Febrero 2026  
**Última actualización:** Pre-defensa