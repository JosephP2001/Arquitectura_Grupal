# 📊 DIAGRAMAS DE ARQUITECTURA - SISTEMA DE CITAS MÉDICAS

---

## 1️⃣ DIAGRAMA DE ARQUITECTURA GENERAL

```mermaid
graph TB
    subgraph "Cliente"
        WEB[🌐 Navegador Web]
        MOBILE[📱 Navegador Móvil]
    end

    subgraph "Frontend Container - Puerto 5173"
        REACT[⚛️ React + Vite<br/>Interfaz de Usuario]
    end

    subgraph "Backend Container - Puerto 8000"
        API[🐍 FastAPI<br/>REST API]
        AUTH[🔐 Auth Middleware]
        SERVICES[⚙️ Business Services]
        DAO[📦 Data Access Layer]
    end

    subgraph "Bases de Datos"
        POSTGRES[(🐘 PostgreSQL<br/>Puerto 5432<br/>Datos Relacionales)]
        MONGO[(🍃 MongoDB<br/>Puerto 27017<br/>Historial Médico)]
        REDIS[(🔴 Redis<br/>Puerto 6379<br/>Sesiones & Cache)]
    end

    WEB -->|HTTP/HTTPS| REACT
    MOBILE -->|HTTP/HTTPS| REACT
    REACT -->|REST API<br/>JSON| API
    
    API --> AUTH
    AUTH --> SERVICES
    SERVICES --> DAO
    
    DAO -->|SQL Queries| POSTGRES
    DAO -->|NoSQL Queries| MONGO
    AUTH -->|Session Management| REDIS
    SERVICES -->|Cache Operations| REDIS

    style REACT fill:#3498db,stroke:#2980b9,color:#fff
    style API fill:#3498db,stroke:#2980b9,color:#fff
    style POSTGRES fill:#2ecc71,stroke:#27ae60,color:#fff
    style MONGO fill:#2ecc71,stroke:#27ae60,color:#fff
    style REDIS fill:#e74c3c,stroke:#c0392b,color:#fff
```

**Descripción:**
Este diagrama muestra la arquitectura general del sistema con tres capas principales: Cliente (navegadores), Frontend (React), Backend (FastAPI) y capa de persistencia (PostgreSQL, MongoDB, Redis).

---

## 2️⃣ DIAGRAMA DE ARQUITECTURA DE CAPAS

```mermaid
graph TB
    subgraph "🎨 PRESENTATION LAYER"
        ROUTES[🛣️ API Routes<br/>auth_routes.py<br/>appointment_routes.py<br/>patient_routes.py<br/>doctor_routes.py<br/>report_routes.py]
        MIDDLEWARE[🔒 Middlewares<br/>session_auth_middleware.py<br/>error_logging_middleware.py]
    end

    subgraph "💼 APPLICATION LAYER"
        DTO[📋 DTOs<br/>authentication_dto.py<br/>appointment_dto.py]
        APPSERVICES[⚙️ Application Services<br/>Use Cases & Business Logic]
    end

    subgraph "🏛️ DOMAIN LAYER"
        ENTITIES[📦 Domain Entities<br/>User<br/>Patient<br/>Doctor<br/>Appointment]
        DOMAINSERVICES[🎯 Domain Services<br/>authentication_service.py<br/>appointment_service.py]
    end

    subgraph "🔧 INFRASTRUCTURE LAYER"
        DAOINT[🔌 DAO Interfaces<br/>patient_dao.py<br/>doctor_dao.py<br/>appointment_dao.py]
        DAOIMPL[💾 DAO Implementations<br/>PostgreSQL: patient_dao_impl.py<br/>MongoDB: medical_record_dao_impl.py]
        MODELS[🗄️ Database Models<br/>PostgreSQL: models.py<br/>MongoDB: medical_record.py]
        CACHE[🔴 Cache Layer<br/>redis_client.py<br/>session_repository.py]
        REGISTRY[📡 Service Registry<br/>service_registry.py]
        BREAKER[⚡ Circuit Breaker<br/>circuit_breaker.py]
    end

    ROUTES --> MIDDLEWARE
    MIDDLEWARE --> DTO
    DTO --> APPSERVICES
    APPSERVICES --> DOMAINSERVICES
    DOMAINSERVICES --> ENTITIES
    DOMAINSERVICES --> DAOINT
    DAOINT --> DAOIMPL
    DAOIMPL --> MODELS
    DOMAINSERVICES --> CACHE
    DAOIMPL --> REGISTRY
    DAOIMPL --> BREAKER

    style ROUTES fill:#3498db,stroke:#2980b9,color:#fff
    style DTO fill:#9b59b6,stroke:#8e44ad,color:#fff
    style ENTITIES fill:#e67e22,stroke:#d35400,color:#fff
    style DAOIMPL fill:#2ecc71,stroke:#27ae60,color:#fff
    style CACHE fill:#e74c3c,stroke:#c0392b,color:#fff
```

**Descripción:**
Arquitectura en capas mostrando la separación de responsabilidades: Presentación (HTTP), Aplicación (casos de uso), Dominio (lógica de negocio) e Infraestructura (persistencia).

---

## 3️⃣ DIAGRAMA DE COMUNICACIÓN ENTRE COMPONENTES

```mermaid
sequenceDiagram
    participant Client as 🌐 Cliente
    participant Frontend as ⚛️ Frontend<br/>(React)
    participant API as 🐍 Backend<br/>(FastAPI)
    participant Auth as 🔐 Auth<br/>Middleware
    participant Service as ⚙️ Business<br/>Service
    participant DAO as 📦 DAO Layer
    participant PG as 🐘 PostgreSQL
    participant Mongo as 🍃 MongoDB
    participant Redis as 🔴 Redis

    Client->>Frontend: 1. Solicitud HTTP
    Frontend->>API: 2. REST API Request<br/>(JSON)
    API->>Auth: 3. Validate Session
    Auth->>Redis: 4. Get Session
    Redis-->>Auth: 5. Session Data
    Auth->>Service: 6. Execute Business Logic
    Service->>DAO: 7. Data Access Request
    
    alt Datos Relacionales
        DAO->>PG: 8a. SQL Query
        PG-->>DAO: 9a. Result Set
    else Datos No Estructurados
        DAO->>Mongo: 8b. NoSQL Query
        Mongo-->>DAO: 9b. Documents
    end
    
    DAO-->>Service: 10. Domain Entities
    Service->>Redis: 11. Update Cache
    Service-->>API: 12. Response DTO
    API-->>Frontend: 13. JSON Response
    Frontend-->>Client: 14. UI Update

    Note over API,Redis: Capa de Cache<br/>reduce latencia
    Note over DAO,Mongo: Polyglot Persistence<br/>SQL + NoSQL
```

**Descripción:**
Flujo secuencial de una petición típica mostrando la interacción entre todos los componentes del sistema, desde el cliente hasta las bases de datos.

---

## 4️⃣ DIAGRAMA DE PATRONES DE DISEÑO

```mermaid
graph TB
    subgraph "📐 DAO PATTERN"
        IDAO["<<interface>><br/>PatientDAO"]
        PGDAO["PatientDAOImpl<br/>(PostgreSQL)"]
        
        IDAO -.implements.-> PGDAO
    end

    subgraph "📋 DTO PATTERN"
        REQUEST["LoginRequestDTO<br/>- username<br/>- password"]
        RESPONSE["LoginResponseDTO<br/>- session_id<br/>- user_data"]
        ENTITY["User Entity<br/>(Domain)"]
        
        REQUEST -->|transform| ENTITY
        ENTITY -->|transform| RESPONSE
    end

    subgraph "📡 SERVICE REGISTRY"
        REGISTRY["ServiceRegistry<br/>- register_service()<br/>- discover_service()<br/>- health_check()"]
        PG_SERVICE["PostgreSQL<br/>Service"]
        MONGO_SERVICE["MongoDB<br/>Service"]
        REDIS_SERVICE["Redis<br/>Service"]
        
        PG_SERVICE -->|register| REGISTRY
        MONGO_SERVICE -->|register| REGISTRY
        REDIS_SERVICE -->|register| REGISTRY
    end

    subgraph "⚡ CIRCUIT BREAKER"
        CB["CircuitBreaker<br/>States: CLOSED, OPEN, HALF_OPEN"]
        SERVICE_CALL["Service Call"]
        
        SERVICE_CALL -->|protected by| CB
    end

    subgraph "💉 DEPENDENCY INJECTION"
        FASTAPI["FastAPI Depends()"]
        DB_SESSION["get_db_session()"]
        AUTH_USER["get_current_user()"]
        
        FASTAPI -->|inject| DB_SESSION
        FASTAPI -->|inject| AUTH_USER
    end

    style IDAO fill:#9b59b6,stroke:#8e44ad,color:#fff
    style REQUEST fill:#9b59b6,stroke:#8e44ad,color:#fff
    style REGISTRY fill:#e67e22,stroke:#d35400,color:#fff
    style CB fill:#e74c3c,stroke:#c0392b,color:#fff
    style FASTAPI fill:#3498db,stroke:#2980b9,color:#fff
```

**Descripción:**
Visualización de los 5 patrones de diseño principales implementados: DAO, DTO, Service Registry, Circuit Breaker y Dependency Injection.

---

## 5️⃣ DIAGRAMA DE FLUJO DE AUTENTICACIÓN

```mermaid
flowchart TD
    START([👤 Usuario Ingresa Credenciales]) --> LOGIN[📤 POST /api/auth/login<br/>username + password]
    
    LOGIN --> VALIDATE{🔍 Validar<br/>Credenciales}
    
    VALIDATE -->|❌ Inválidas| ERROR1[❌ Error 401<br/>Unauthorized]
    VALIDATE -->|✅ Válidas| HASH{🔐 Verificar Hash<br/>bcrypt.verify}
    
    HASH -->|❌ No coincide| ERROR1
    HASH -->|✅ Coincide| GETSESSION[🔑 Generar Session ID<br/>uuid4]
    
    GETSESSION --> SAVETOREDIS[💾 Guardar en Redis<br/>Key: session:uuid<br/>TTL: 60 min<br/>Data: user_id, role, username]
    
    SAVETOREDIS --> RESPONSE[📩 Response 200 OK<br/>session_id + user_data]
    
    RESPONSE --> NEXTREQ([🔄 Siguientes Requests])
    
    NEXTREQ --> MIDDLEWARE[🔒 Session Auth<br/>Middleware]
    
    MIDDLEWARE --> CHECKSESSION{🔍 Verificar<br/>Session en Redis}
    
    CHECKSESSION -->|❌ No existe| ERROR2[❌ Error 401<br/>Unauthorized]
    CHECKSESSION -->|⏱️ Expirada| ERROR2
    CHECKSESSION -->|✅ Válida| EXTEND[♻️ Extender TTL<br/>60 min más]
    
    EXTEND --> ALLOW[✅ Permitir Acceso<br/>a Recurso Protegido]
    
    ERROR1 --> END1([🚫 Fin - No Autenticado])
    ERROR2 --> END1
    ALLOW --> END2([✅ Fin - Autenticado])

    style LOGIN fill:#3498db,stroke:#2980b9,color:#fff
    style SAVETOREDIS fill:#e74c3c,stroke:#c0392b,color:#fff
    style ERROR1 fill:#e74c3c,stroke:#c0392b,color:#fff
    style ERROR2 fill:#e74c3c,stroke:#c0392b,color:#fff
    style ALLOW fill:#2ecc71,stroke:#27ae60,color:#fff
```

**Descripción:**
Flujo completo de autenticación mostrando login inicial, creación de sesión en Redis y validación en requests subsecuentes mediante middleware.

---

## 6️⃣ DIAGRAMA DE FLUJO DE CREACIÓN DE CITA

```mermaid
flowchart TD
    START([👤 Paciente: Crear Cita]) --> FORM[📝 Formulario Frontend<br/>Seleccionar Doctor<br/>Fecha y Hora<br/>Motivo]
    
    FORM --> VALIDATE_FRONT{✅ Validación<br/>Frontend}
    
    VALIDATE_FRONT -->|❌ Error| ERROR_FRONT[❌ Mostrar Errores<br/>en Formulario]
    VALIDATE_FRONT -->|✅ OK| POST[📤 POST /api/appointments<br/>+ Session Cookie]
    
    POST --> AUTH_MW[🔐 Auth Middleware<br/>Validar Sesión]
    
    AUTH_MW -->|❌ No autenticado| ERROR_401[❌ Error 401]
    AUTH_MW -->|✅ Sesión válida| CHECK_ROLE{🎭 Verificar Rol}
    
    CHECK_ROLE -->|❌ No es PATIENT| ERROR_403[❌ Error 403<br/>Forbidden]
    CHECK_ROLE -->|✅ Es PATIENT| SERVICE[⚙️ AppointmentService<br/>create_appointment]
    
    SERVICE --> VALIDATE_BUSINESS{🔍 Validaciones<br/>de Negocio}
    
    VALIDATE_BUSINESS -->|❌ Doctor no existe| ERROR_404[❌ Error 404]
    VALIDATE_BUSINESS -->|❌ Horario no disponible| ERROR_CONFLICT[❌ Error 409<br/>Conflict]
    VALIDATE_BUSINESS -->|✅ Todo OK| CHECK_CACHE{🔴 Verificar<br/>Cache Redis}
    
    CHECK_CACHE -->|Datos en cache| USE_CACHE[📥 Usar Datos<br/>desde Cache]
    CHECK_CACHE -->|No en cache| QUERY_DB[🔍 Consultar<br/>PostgreSQL]
    
    USE_CACHE --> SAVE_APPOINTMENT
    QUERY_DB --> CACHE_RESULT[💾 Guardar en Cache]
    CACHE_RESULT --> SAVE_APPOINTMENT
    
    SAVE_APPOINTMENT[💾 Guardar Cita<br/>en PostgreSQL] --> CREATE_RECORD[📝 Crear Registro<br/>en MongoDB<br/>Historial Médico]
    
    CREATE_RECORD --> RESPONSE[📩 Response 201<br/>Created<br/>Appointment Data]
    
    RESPONSE --> UPDATE_UI[🎨 Actualizar UI<br/>Mostrar Confirmación]
    
    ERROR_FRONT --> END1([🚫 Fin - Error Cliente])
    ERROR_401 --> END1
    ERROR_403 --> END1
    ERROR_404 --> END1
    ERROR_CONFLICT --> END1
    UPDATE_UI --> END2([✅ Fin - Cita Creada])

    style POST fill:#3498db,stroke:#2980b9,color:#fff
    style SERVICE fill:#9b59b6,stroke:#8e44ad,color:#fff
    style SAVE_APPOINTMENT fill:#2ecc71,stroke:#27ae60,color:#fff
    style CREATE_RECORD fill:#2ecc71,stroke:#27ae60,color:#fff
    style CHECK_CACHE fill:#e74c3c,stroke:#c0392b,color:#fff
    style ERROR_401 fill:#e74c3c,stroke:#c0392b,color:#fff
    style ERROR_403 fill:#e74c3c,stroke:#c0392b,color:#fff
    style UPDATE_UI fill:#2ecc71,stroke:#27ae60,color:#fff
```

**Descripción:**
Flujo detallado de creación de cita médica incluyendo validaciones frontend/backend, verificación de roles, cache con Redis y persistencia en PostgreSQL + MongoDB.

---

## 7️⃣ DIAGRAMA DE DESPLIEGUE DOCKER

```mermaid
graph TB
    subgraph "🖥️ HOST MACHINE - LAN IP: 192.168.1.X"
        subgraph "🐳 Docker Network: medical_network (bridge)"
            
            subgraph "Frontend Container"
                FE[⚛️ React + Vite<br/>Node.js<br/>Puerto Interno: 5173]
            end
            
            subgraph "Backend Container"
                BE[🐍 FastAPI<br/>Python 3.11<br/>Puerto Interno: 8000]
            end
            
            subgraph "PostgreSQL Container"
                PG[🐘 PostgreSQL 15<br/>Puerto Interno: 5432<br/>Volume: postgres_data]
            end
            
            subgraph "MongoDB Container"
                MG[🍃 MongoDB 7<br/>Puerto Interno: 27017<br/>Volume: mongo_data]
            end
            
            subgraph "Redis Container"
                RD[🔴 Redis 7<br/>Puerto Interno: 6379<br/>Volume: redis_data]
            end
        end
        
        PORTS[📍 Port Mapping:<br/>5173:5173 → Frontend<br/>8000:8000 → Backend<br/>5432:5432 → PostgreSQL<br/>27017:27017 → MongoDB<br/>6379:6379 → Redis]
    end
    
    CLIENT[🌐 Clientes LAN<br/>192.168.1.Y] -->|http://192.168.1.X:5173| PORTS
    PORTS -->|5173| FE
    PORTS -->|8000| BE
    
    FE -->|REST API| BE
    BE -->|SQL| PG
    BE -->|NoSQL| MG
    BE -->|Cache| RD
    
    ENV[⚙️ Environment Variables<br/>DATABASE_URL=postgresql://...<br/>MONGODB_URL=mongodb://...<br/>REDIS_URL=redis://...<br/>VITE_API_URL=http://192.168.1.X:8000]
    
    ENV -.->|Configure| BE
    ENV -.->|Configure| FE

    style FE fill:#3498db,stroke:#2980b9,color:#fff
    style BE fill:#3498db,stroke:#2980b9,color:#fff
    style PG fill:#2ecc71,stroke:#27ae60,color:#fff
    style MG fill:#2ecc71,stroke:#27ae60,color:#fff
    style RD fill:#e74c3c,stroke:#c0392b,color:#fff
    style PORTS fill:#95a5a6,stroke:#7f8c8d,color:#fff
    style ENV fill:#e67e22,stroke:#d35400,color:#fff
```

**Descripción:**
Arquitectura de despliegue mostrando los 5 contenedores Docker, red bridge, mapeo de puertos, volúmenes persistentes y configuración para LAN.

---

## 8️⃣ DIAGRAMA DE SERVICE REGISTRY

```mermaid
stateDiagram-v2
    [*] --> Initializing: Sistema Inicia
    
    Initializing --> Registering: Detectar Servicios
    
    Registering --> Registered: PostgreSQL Registered
    Registering --> Registered: MongoDB Registered
    Registering --> Registered: Redis Registered
    
    Registered --> HealthCheck: Periodic Check (30s)
    
    state HealthCheck {
        [*] --> SendPing: Enviar Health Check
        SendPing --> WaitResponse: Esperar Respuesta
        
        WaitResponse --> Healthy: ✅ Response OK
        WaitResponse --> Degraded: ⚠️ Slow Response
        WaitResponse --> Unavailable: ❌ Timeout/Error
    }
    
    Healthy --> Registered: Update Status
    Degraded --> Registered: Update Status
    Unavailable --> Fallback: Service Down
    
    Fallback --> LocalConfig: Usar Config Local
    LocalConfig --> Retry: Reintentar Conexión
    Retry --> HealthCheck: Después de 60s
    
    Registered --> [*]: Sistema Detiene

    note right of HealthCheck
        Heartbeat cada 30 segundos
        Timeout: 5 segundos
        Retry: 3 intentos
    end note
    
    note right of Fallback
        Si Service Registry falla
        usar variables de entorno
        como fallback
    end note
```

**Descripción:**
Máquina de estados del Service Registry mostrando registro de servicios, health checks periódicos, manejo de degradación y fallback a configuración local.

---

## 9️⃣ DIAGRAMA DE CIRCUIT BREAKER

```mermaid
stateDiagram-v2
    [*] --> CLOSED: Inicialización
    
    state CLOSED {
        [*] --> Monitoring: Permitir Peticiones
        Monitoring --> CountFailures: Contar Fallos
        CountFailures --> CheckThreshold: Evaluar Umbral
    }
    
    CheckThreshold --> OPEN: ❌ Umbral Superado<br/>(5 fallos en 60s)
    CheckThreshold --> CLOSED: ✅ Bajo Umbral
    
    state OPEN {
        [*] --> RejectRequests: Rechazar Peticiones<br/>Inmediatamente
        RejectRequests --> WaitTimeout: Esperar Timeout<br/>(30 segundos)
    }
    
    WaitTimeout --> HALF_OPEN: Timeout Alcanzado
    
    state HALF_OPEN {
        [*] --> TestRequest: Permitir 1 Petición<br/>de Prueba
        TestRequest --> Evaluate: Evaluar Resultado
    }
    
    Evaluate --> CLOSED: ✅ Éxito<br/>Servicio Recuperado
    Evaluate --> OPEN: ❌ Fallo<br/>Aún con Problemas
    
    CLOSED --> [*]: Sistema Detiene
    OPEN --> [*]: Sistema Detiene
    HALF_OPEN --> [*]: Sistema Detiene

    note right of CLOSED
        🟢 CLOSED
        Estado Normal
        Todas las peticiones pasan
        Monitorea tasa de fallos
    end note
    
    note right of OPEN
        🔴 OPEN
        Circuito Abierto
        Fail-fast: responde error
        sin llamar al servicio
    end note
    
    note right of HALF_OPEN
        🟡 HALF_OPEN
        Probando Recuperación
        Permite peticiones limitadas
        para verificar si el servicio
        se ha recuperado
    end note
```

**Descripción:**
Estados del Circuit Breaker (CLOSED, OPEN, HALF_OPEN) con umbrales configurables para proteger contra fallos en cascada.

---

## 🔟 DIAGRAMA DE ESTRUCTURA DE DIRECTORIOS

```mermaid
graph TD
    ROOT[📁 medical-appointment-platform/]
    
    ROOT --> BACKEND[📁 backend/]
    ROOT --> FRONTEND[📁 frontend/]
    ROOT --> DC[📄 docker-compose.yml]
    
    BACKEND --> SRC[📁 src/]
    BACKEND --> TESTS[📁 tests/]
    BACKEND --> DOCKER_BE[📄 Dockerfile]
    BACKEND --> REQ[📄 requirements.txt]
    
    SRC --> MAIN[📄 main.py]
    SRC --> CONFIG[📁 config/]
    SRC --> APP[📁 application/]
    SRC --> DOMAIN[📁 domain/]
    SRC --> INFRA[📁 infrastructure/]
    SRC --> PRES[📁 presentation/]
    
    APP --> DTO_DIR[📁 dto/]
    APP --> SERV_DIR[📁 services/]
    
    DOMAIN --> ENT[📁 entities/]
    DOMAIN --> DOM_SERV[📁 services/]
    
    INFRA --> DAO_DIR[📁 dao/]
    INFRA --> MODELS_DIR[📁 models/]
    INFRA --> CACHE_DIR[📁 cache/]
    INFRA --> REG[📁 registry/]
    INFRA --> RES[📁 resilience/]
    
    DAO_DIR --> INTER[📁 interfaces/]
    DAO_DIR --> PG_IMPL[📁 postgresql/]
    DAO_DIR --> MG_IMPL[📁 mongodb/]
    
    PRES --> ROUTES[📁 routes/]
    PRES --> MW[📁 middlewares/]
    
    FRONTEND --> SRC_FE[📁 src/]
    FRONTEND --> PUBLIC[📁 public/]
    FRONTEND --> DOCKER_FE[📄 Dockerfile]
    FRONTEND --> VITE[📄 vite.config.js]
    FRONTEND --> PACKAGE[📄 package.json]

    style ROOT fill:#95a5a6,stroke:#7f8c8d,color:#fff
    style SRC fill:#3498db,stroke:#2980b9,color:#fff
    style APP fill:#9b59b6,stroke:#8e44ad,color:#fff
    style DOMAIN fill:#e67e22,stroke:#d35400,color:#fff
    style INFRA fill:#2ecc71,stroke:#27ae60,color:#fff
    style PRES fill:#3498db,stroke:#2980b9,color:#fff
```

**Descripción:**
Estructura completa del proyecto mostrando organización de carpetas backend (arquitectura en capas) y frontend, con énfasis en separación de responsabilidades.

---

## 📊 RESUMEN DE DIAGRAMAS

| # | Diagrama | Propósito | Audiencia |
|---|----------|-----------|-----------|
| 1 | Arquitectura General | Vista de alto nivel del sistema completo | Todos |
| 2 | Arquitectura de Capas | Separación lógica del código | Desarrolladores |
| 3 | Comunicación | Flujo de datos entre componentes | Arquitectos |
| 4 | Patrones de Diseño | Patrones implementados | Desarrolladores Senior |
| 5 | Flujo Autenticación | Proceso de login y sesiones | Seguridad/DevOps |
| 6 | Flujo Creación Cita | Caso de uso principal | Product Owners |
| 7 | Despliegue Docker | Infraestructura y networking | DevOps |
| 8 | Service Registry | Descubrimiento de servicios | Arquitectos |
| 9 | Circuit Breaker | Resiliencia del sistema | SRE/DevOps |
| 10 | Estructura Directorios | Organización del código | Desarrolladores |

---

**Fecha de Generación:** Febrero 2026  
**Autores:** Aucancela Andrés, Ponce Joseph, Villareal Jhonatan  
**Versión:** 1.0