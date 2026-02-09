# 📊 GUÍA DE LECTURA DE DIAGRAMAS - SISTEMA DE CITAS MÉDICAS

## 🎯 Propósito de esta Guía

Esta guía explica cómo interpretar los diagramas de arquitectura del sistema de gestión de citas médicas. Está diseñada para ser usada como **prompt de regeneración** si necesitas recrear los gráficos más adelante.

---

## 📐 TIPOS DE DIAGRAMAS INCLUIDOS

### 1. **Diagrama de Arquitectura General**
- **Qué muestra:** Vista de alto nivel de todos los componentes del sistema
- **Elementos clave:**
  - Cliente (navegador web)
  - Frontend (React + Vite)
  - Backend (FastAPI)
  - Bases de datos (PostgreSQL, MongoDB, Redis)
  - Red Docker

### 2. **Diagrama de Arquitectura de Capas (Layered Architecture)**
- **Qué muestra:** Separación lógica del código en capas
- **Capas incluidas:**
  - **Presentation Layer:** Rutas HTTP, middlewares
  - **Application Layer:** Servicios, DTOs, lógica de aplicación
  - **Domain Layer:** Entidades de negocio, reglas de dominio
  - **Infrastructure Layer:** DAOs, modelos de BD, cache

### 3. **Diagrama de Comunicación entre Componentes**
- **Qué muestra:** Flujo de datos entre servicios
- **Incluye:**
  - Peticiones HTTP del cliente
  - Respuestas del backend
  - Consultas a bases de datos
  - Operaciones de cache en Redis

### 4. **Diagrama de Patrones de Diseño Implementados**
- **Patrones mostrados:**
  - **DAO Pattern:** Abstracción de acceso a datos
  - **DTO Pattern:** Transferencia de datos entre capas
  - **Service Registry:** Descubrimiento de servicios
  - **Circuit Breaker:** Resiliencia ante fallos
  - **Repository Pattern:** Abstracción de persistencia
  - **Dependency Injection:** Inyección de dependencias con FastAPI

### 5. **Diagrama de Flujo de Autenticación**
- **Qué muestra:** Proceso completo de login y gestión de sesiones
- **Pasos incluidos:**
  - Login del usuario
  - Validación de credenciales
  - Generación de sesión en Redis
  - Middleware de autenticación
  - Validación de sesión en cada request

### 6. **Diagrama de Flujo de Creación de Cita**
- **Qué muestra:** Proceso de creación de una cita médica
- **Componentes involucrados:**
  - Frontend (formulario)
  - Backend (validación)
  - PostgreSQL (datos relacionales)
  - MongoDB (historial médico)

### 7. **Diagrama de Despliegue Docker**
- **Qué muestra:** Cómo se despliegan los contenedores
- **Elementos:**
  - Red bridge de Docker
  - Volúmenes persistentes
  - Mapeo de puertos
  - Variables de entorno

### 8. **Diagrama de Service Registry**
- **Qué muestra:** Mecanismo de descubrimiento de servicios
- **Estados:**
  - Registro de servicios
  - Health checks
  - Heartbeat
  - Fallback a configuración local

### 9. **Diagrama de Circuit Breaker**
- **Qué muestra:** Estados del Circuit Breaker
- **Estados incluidos:**
  - CLOSED (funcionamiento normal)
  - OPEN (fallo detectado)
  - HALF_OPEN (probando recuperación)

---

## 🎨 CONVENCIONES VISUALES

### Colores Utilizados

| Color | Significado | Uso |
|-------|-------------|-----|
| **Azul (#3498db)** | Componentes principales | Frontend, Backend |
| **Verde (#2ecc71)** | Bases de datos | PostgreSQL, MongoDB |
| **Rojo (#e74c3c)** | Cache y sesiones | Redis |
| **Naranja (#e67e22)** | Servicios externos | APIs, integraciones |
| **Gris (#95a5a6)** | Infraestructura | Docker, redes |
| **Morado (#9b59b6)** | Patrones de diseño | DAO, DTO, Service |

### Formas y Símbolos

| Forma | Representación |
|-------|----------------|
| **Rectángulo** | Componente/Servicio |
| **Cilindro** | Base de datos |
| **Rombo** | Decisión/Validación |
| **Flecha sólida →** | Flujo de datos |
| **Flecha punteada ⇢** | Dependencia/Referencia |
| **Línea doble ⇔** | Comunicación bidireccional |

### Notación de Capas

```
┌─────────────────────────────────┐
│  CAPA SUPERIOR (UI/Routes)      │
├─────────────────────────────────┤
│  CAPA INTERMEDIA (Services)     │
├─────────────────────────────────┤
│  CAPA INFERIOR (Data Access)    │
└─────────────────────────────────┘
```

---

## 🔍 CÓMO LEER CADA TIPO DE DIAGRAMA

### 📊 Diagrama de Arquitectura General

**Interpretación:**
1. **Arriba:** Cliente (navegador/móvil)
2. **Centro-izquierda:** Frontend React
3. **Centro-derecha:** Backend FastAPI
4. **Abajo:** Bases de datos y cache

**Flujo de lectura:**
- De arriba hacia abajo (cliente → frontend → backend → BD)
- Las flechas indican dirección del flujo de datos
- Los puertos se muestran junto a cada servicio

---

### 🏗️ Diagrama de Capas (Layered Architecture)

**Interpretación:**
1. **Presentation (arriba):** Todo lo relacionado con HTTP
2. **Application:** Lógica de negocio y casos de uso
3. **Domain:** Modelos de negocio puros
4. **Infrastructure (abajo):** Acceso a datos y servicios externos

**Regla de oro:**
- Las capas superiores pueden llamar a las inferiores
- Las capas inferiores NO deben conocer las superiores
- Las flechas van de arriba hacia abajo

---

### 🔄 Diagrama de Comunicación entre Componentes

**Interpretación:**
1. Los números indican el orden secuencial (1, 2, 3...)
2. Las líneas sólidas son llamadas directas
3. Las líneas punteadas son respuestas
4. Los colores agrupan componentes relacionados

**Ejemplo de lectura:**
```
[Cliente] --1. POST /login--> [Backend]
[Backend] --2. Validate--> [PostgreSQL]
[Backend] --3. Create Session--> [Redis]
[Backend] --4. Response--> [Cliente]
```

---

### 🎯 Diagrama de Patrones de Diseño

**Interpretación:**
1. Cada patrón se muestra con su contexto
2. Las interfaces se representan con líneas punteadas
3. Las implementaciones concretas son líneas sólidas
4. Los colores agrupan componentes del mismo patrón

**Elementos clave:**
- **<<interface>>**: Define el contrato
- **implements**: Clase que implementa la interfaz
- **uses**: Clase que usa otra clase

---

### 🔐 Diagrama de Flujo de Autenticación

**Interpretación:**
1. **Inicio:** Usuario ingresa credenciales
2. **Validación:** Backend verifica en PostgreSQL
3. **Sesión:** Se crea en Redis con TTL
4. **Token/Cookie:** Se envía al cliente
5. **Requests siguientes:** Middleware valida sesión

**Elementos especiales:**
- ❌ Indica punto de fallo/rechazo
- ✅ Indica éxito
- ⏱️ Indica timeout/expiración

---

### 📅 Diagrama de Flujo de Creación de Cita

**Interpretación:**
1. **Validaciones en Frontend:** Fechas, horarios disponibles
2. **Validaciones en Backend:** Roles, disponibilidad
3. **Transacciones:** PostgreSQL para datos relacionales
4. **Registro histórico:** MongoDB para historial médico

**Puntos de decisión:**
- Rombo = validación/decisión
- Camino verde = éxito
- Camino rojo = error

---

### 🐳 Diagrama de Despliegue Docker

**Interpretación:**
1. **Red medical_network:** Conecta todos los contenedores
2. **Volúmenes:** Persistencia de datos
3. **Puertos expuestos:** Acceso desde el host
4. **Variables de entorno:** Configuración dinámica

**Notación:**
```
[Contenedor]
├── Puerto: 8000:8000 (host:container)
├── Volumen: ./app:/app
└── Red: medical_network
```

---

### 🔍 Diagrama de Service Registry

**Interpretación:**
1. **Registro inicial:** Servicios se registran al iniciar
2. **Health check:** Verificación periódica de salud
3. **Heartbeat:** Confirmación de disponibilidad
4. **Fallback:** Uso de configuración local si falla

**Estados de servicio:**
- 🟢 HEALTHY: Funcionando correctamente
- 🟡 DEGRADED: Con problemas
- 🔴 UNAVAILABLE: No disponible

---

### ⚡ Diagrama de Circuit Breaker

**Interpretación de estados:**

1. **CLOSED (🟢):**
   - Todo funciona normal
   - Peticiones pasan al servicio
   - Se monitorea tasa de fallos

2. **OPEN (🔴):**
   - Demasiados fallos detectados
   - Peticiones se rechazan inmediatamente
   - Se espera período de timeout

3. **HALF_OPEN (🟡):**
   - Permitiendo peticiones de prueba
   - Si tienen éxito → CLOSED
   - Si fallan → OPEN

**Umbrales típicos:**
- Threshold: 5 fallos en 60 segundos
- Timeout: 30 segundos
- Test requests: 3 peticiones

---

## 📝 LEYENDAS ESTÁNDAR

### Leyenda de Tecnologías

| Símbolo | Tecnología |
|---------|------------|
| ⚛️ | React (Frontend) |
| ⚡ | Vite (Build tool) |
| 🐍 | Python/FastAPI (Backend) |
| 🐘 | PostgreSQL |
| 🍃 | MongoDB |
| 🔴 | Redis |
| 🐳 | Docker |

### Leyenda de Operaciones

| Símbolo | Operación |
|---------|-----------|
| 📤 | Enviar/POST |
| 📥 | Recibir/GET |
| ✏️ | Actualizar/PUT/PATCH |
| 🗑️ | Eliminar/DELETE |
| 🔍 | Consultar/SELECT |
| 💾 | Guardar/INSERT |

---

## 🎓 PROMPT DE REGENERACIÓN

Si necesitas regenerar estos diagramas, usa el siguiente prompt:

```
Genera diagramas de arquitectura para un sistema de gestión de citas médicas con las siguientes características:

TECNOLOGÍAS:
- Frontend: React + Vite (Puerto 5173)
- Backend: FastAPI + Python 3.11 (Puerto 8000)
- BD Relacional: PostgreSQL 15 (Puerto 5432)
- BD NoSQL: MongoDB 7 (Puerto 27017)
- Cache: Redis 7 (Puerto 6379)
- Despliegue: Docker Compose con red bridge

ARQUITECTURA:
- Arquitectura de 4 capas: Presentation, Application, Domain, Infrastructure
- Comunicación vía REST API (JSON)
- Autenticación basada en sesiones (Redis)
- Manejo de roles: Admin, Doctor, Paciente

PATRONES DE DISEÑO:
1. DAO Pattern (interfaces + implementaciones PostgreSQL/MongoDB)
2. DTO Pattern (transferencia entre capas)
3. Service Registry (descubrimiento de servicios)
4. Circuit Breaker (resiliencia, estados: CLOSED/OPEN/HALF_OPEN)
5. Repository Pattern
6. Dependency Injection (FastAPI Depends)

DIAGRAMAS REQUERIDOS:
1. Arquitectura general del sistema
2. Diagrama de capas (layered architecture)
3. Comunicación entre componentes
4. Patrones de diseño implementados
5. Flujo de autenticación (login + sesiones)
6. Flujo de creación de cita médica
7. Despliegue en Docker (contenedores + redes)
8. Diagrama de Service Registry
9. Diagrama de Circuit Breaker con estados

CONVENCIONES:
- Azul (#3498db): Componentes principales
- Verde (#2ecc71): Bases de datos
- Rojo (#e74c3c): Cache/Redis
- Morado (#9b59b6): Patrones de diseño
- Flechas sólidas: Flujo de datos
- Flechas punteadas: Dependencias
- Numeración secuencial en flujos

FORMATO: Mermaid diagrams profesionales con comentarios explicativos
```

---

## ✅ CHECKLIST DE VALIDACIÓN

Antes de considerar un diagrama como completo, verificar:

- [ ] Todos los componentes principales están representados
- [ ] Las relaciones/flujos son claros y direccionales
- [ ] Los colores siguen la convención definida
- [ ] Las etiquetas son legibles y descriptivas
- [ ] Los puertos están correctamente especificados
- [ ] Las tecnologías están identificadas
- [ ] Los patrones de diseño son evidentes
- [ ] El flujo se lee de manera lógica (top-down o left-right)

---

## 📚 REFERENCIAS

- **Arquitectura de Capas:** Clean Architecture (Robert C. Martin)
- **Patrones DAO/DTO:** Enterprise Application Patterns (Martin Fowler)
- **Circuit Breaker:** Release It! (Michael Nygard)
- **Service Registry:** Microservices Patterns (Chris Richardson)

---

**Versión:** 1.0  
**Fecha:** Febrero 2026  
**Autores:** Aucancela Andrés, Ponce Joseph, Villareal Jhonatan