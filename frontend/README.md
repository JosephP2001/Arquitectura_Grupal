# 🏥 Medical Appointment Platform - Frontend

Aplicación web moderna y profesional para gestión de citas médicas, construida con **React**, **Vite** y **TailwindCSS** con un diseño médico personalizado.

---

## Tabla de Contenidos

- [Características](#-características)
- [Stack Tecnológico](#-stack-tecnológico)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Scripts Disponibles](#-scripts-disponibles)
- [Diseño y Estilo](#-diseño-y-estilo)
- [Componentes Principales](#-componentes-principales)
- [Rutas y Navegación](#-rutas-y-navegación)
- [Autenticación](#-autenticación)
- [Servicios API](#-servicios-api)
- [Despliegue](#-despliegue)

---

## ✨ Características

- ✅ **Interfaz Moderna**: Diseño médico profesional con TailwindCSS
- ✅ **SPA (Single Page Application)**: Navegación fluida con React Router
- ✅ **Autenticación Basada en Sesiones**: Login/Register seguro
- ✅ **Roles de Usuario**: Dashboards específicos para Admin, Doctor y Paciente
- ✅ **Gestión de Citas**: Agendar, confirmar, completar y cancelar citas
- ✅ **Responsive Design**: Adaptado a móviles, tablets y desktop
- ✅ **Tema Médico Personalizado**: Paleta de colores profesional
- ✅ **Animaciones Suaves**: Transiciones y efectos visuales
- ✅ **Validación de Formularios**: Feedback inmediato al usuario
- ✅ **Dockerizado**: Fácil despliegue con Docker

---

## 🛠 Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **React** | 18.2.0 | Librería UI |
| **Vite** | 5.0.8 | Build tool y dev server |
| **React Router** | 6.20.1 | Enrutamiento SPA |
| **Axios** | 1.6.2 | Cliente HTTP |
| **TailwindCSS** | 3.4.19 | Framework CSS |
| **PostCSS** | 8.5.6 | Procesador CSS |
| **Autoprefixer** | 10.4.23 | Prefijos CSS automáticos |

---

## 📁 Estructura del Proyecto

```
frontend/
├── public/                          # Archivos estáticos
│   └── vite.svg                     # Logo de Vite
│
├── src/
│   ├── assets/                      # Recursos (imágenes, íconos)
│   │
│   ├── components/                  # Componentes reutilizables
│   │   ├── appointments/            # Componentes de citas
│   │   ├── doctors/                 # Componentes de doctores
│   │   └── layout/                  # Componentes de layout
│   │       ├── Navbar.jsx           # Barra de navegación
│   │       └── ProtectedRoute.jsx   # Protección de rutas
│   │
│   ├── context/                     # Context API de React
│   │   └── AuthContext.jsx          # Contexto de autenticación
│   │
│   ├── pages/                       # Páginas de la aplicación
│   │   ├── Login.jsx                # Página de inicio de sesión
│   │   ├── Register.jsx             # Página de registro
│   │   ├── Dashboard.jsx            # Dashboard de admin
│   │   ├── PatientDashboard.jsx     # Dashboard de paciente
│   │   ├── DoctorDashboard.jsx      # Dashboard de doctor
│   │   ├── AppointmentBooking.jsx   # Agendar cita
│   │   └── Reports.jsx              # Reportes del sistema
│   │
│   ├── services/                    # Servicios de API
│   │   ├── api.js                   # Cliente Axios configurado
│   │   ├── authService.js           # Servicios de autenticación
│   │   ├── appointmentService.js    # Servicios de citas
│   │   ├── doctorService.js         # Servicios de doctores
│   │   └── patientService.js        # Servicios de pacientes
│   │
│   ├── styles/                      # Estilos globales
│   │   └── index.css                # CSS personalizado + Tailwind
│   │
│   ├── App.jsx                      # Componente raíz
│   ├── main.jsx                     # Punto de entrada
│   └── index.css                    # Estilos globales
│
├── .gitignore                       # Archivos ignorados por Git
├── Dockerfile                       # Configuración Docker
├── index.html                       # HTML principal
├── package.json                     # Dependencias y scripts
├── postcss.config.js                # Configuración PostCSS
├── tailwind.config.js               # Configuración TailwindCSS
├── vite.config.js                   # Configuración Vite
└── README.md                        # Este archivo
```

---

## Requisitos

### Desarrollo Local
- Node.js 18+
- npm 9+

### Producción (Docker)
- Docker 20.10+
- Docker Compose 2.0+

---

## Instalación

### Opción 1: Docker (Recomendado)

```bash
# Desde la raíz del proyecto
docker-compose up --build

# El frontend estará disponible en http://localhost:5173
```

### Opción 2: Desarrollo Local

```bash
# Navegar a la carpeta frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev

# La aplicación se abrirá en http://localhost:5173
```

---

## ⚙️ Configuración

### Variables de Entorno

Crear archivo `.env` en la raíz de `frontend/`:

```bash
VITE_API_URL=http://localhost:8000
```

**Nota**: En Docker, esta variable se configura en `docker-compose.yml`

### TailwindCSS - Tema Médico Personalizado

El proyecto utiliza una paleta de colores médica profesional:

```javascript
// tailwind.config.js
theme: {
  extend: {
    colors: {
      medical: {
        50: '#f0f9ff',
        100: '#e0f2fe',
        // ... hasta 900
        600: '#0284c7',  // Color principal
      },
      health: {
        500: '#22c55e',  // Verde salud
      },
      clinical: {
        // Grises profesionales
      }
    }
  }
}
```

---

## Uso

### Desarrollo

```bash
# Iniciar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build

# Preview de producción
npm run preview
```

### Usuarios de Prueba

Después de iniciar el backend, puedes crear usuarios:

```
Admin:
- Username: admin
- Password: admin123

Doctor:
- Registrarse como doctor desde /register
- Seleccionar especialidad

Paciente:
- Registrarse como paciente desde /register
```

---

## Scripts Disponibles

| Script | Comando | Descripción |
|--------|---------|-------------|
| **dev** | `npm run dev` | Inicia servidor de desarrollo |
| **build** | `npm run build` | Compila para producción |
| **preview** | `npm run preview` | Preview de build de producción |

---

## Diseño y Estilo

### Paleta de Colores

| Color | Código | Uso |
|-------|--------|-----|
| **Medical Blue** | `#0284c7` | Botones principales, navbar |
| **Health Green** | `#22c55e` | Acciones positivas, confirmaciones |
| **Clinical Gray** | `#78716c` | Textos, fondos neutros |
| **Alert Red** | `#ef4444` | Errores, cancelaciones |
| **Warning Amber** | `#f59e0b` | Advertencias, pendientes |

### Clases CSS Personalizadas

```css
/* Botones */
.btn-medical      /* Botón azul médico */
.btn-success      /* Botón verde salud */
.btn-danger       /* Botón rojo */

/* Cards */
.medical-card     /* Card con sombra médica */
.card-hover       /* Efecto hover elevado */

/* Inputs */
.medical-input    /* Input con focus ring */

/* Badges */
.badge-pending    /* Estado pendiente */
.badge-confirmed  /* Estado confirmado */
.badge-completed  /* Estado completado */
.badge-cancelled  /* Estado cancelado */

/* Alertas */
.alert-success    /* Alerta de éxito */
.alert-error      /* Alerta de error */
.alert-warning    /* Alerta de advertencia */
```

### Animaciones

```css
.fade-in          /* Entrada suave */
.slide-up         /* Deslizar hacia arriba */
.pulse-slow       /* Pulso lento */
.card-hover       /* Elevación en hover */
```

---

## Componentes Principales

### Layout

#### **Navbar**
Barra de navegación sticky con gradiente médico.

```jsx
import Navbar from './components/layout/Navbar'

// Características:
- Logo animado
- Información del usuario
- Badges de rol
- Navegación contextual
- Botón de logout
```

#### **ProtectedRoute**
Protección de rutas basada en autenticación y roles.

```jsx
<ProtectedRoute allowedRoles={['admin']}>
  <AdminPage />
</ProtectedRoute>
```

### Páginas

#### **Login / Register**
- Diseño moderno con gradientes
- Iconos en inputs
- Validación en tiempo real
- Decoración animada de fondo

#### **Dashboards**
- **Admin**: Cards con gradientes únicos, acceso a reportes
- **Doctor**: Perfil, estadísticas, gestión de citas
- **Paciente**: Perfil, historial, agendar citas

#### **AppointmentBooking**
Formulario de agendamiento de citas con:
- Selector de especialidad
- Selector de doctor
- Calendario de fechas
- Selector de hora

---

## 🛣 Rutas y Navegación

| Ruta | Componente | Protegida | Roles |
|------|------------|-----------|-------|
| `/` | Dashboard | Sí | Todos |
| `/login` | Login | No | - |
| `/register` | Register | No | - |
| `/patient/dashboard` | PatientDashboard | Sí | Paciente |
| `/doctor/dashboard` | DoctorDashboard | Sí | Doctor |
| `/appointments/new` | AppointmentBooking | Sí | Paciente |
| `/reports` | Reports | Sí | Admin |

### Redirecciones Automáticas

```javascript
// Basadas en rol del usuario
Admin    → /
Doctor   → /doctor/dashboard
Paciente → /patient/dashboard
```

---

## 🔐 Autenticación

### Context de Autenticación

```jsx
// AuthContext.jsx
const { user, login, logout, isAuthenticated } = useAuth()

// Funciones disponibles:
- login(userData)         // Iniciar sesión
- logout()               // Cerrar sesión
- isAuthenticated        // Boolean de estado
- user                   // Datos del usuario actual
```

### Flujo de Autenticación

```
1. Usuario ingresa credenciales
2. authService.login() → POST /api/auth/login
3. Backend retorna user + crea sesión (cookie)
4. Frontend guarda user en localStorage
5. AuthContext actualiza estado global
6. Redirección según rol
```

---

## 🌐 Servicios API

### Cliente Axios Configurado

```javascript
// services/api.js
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true  // Envía cookies automáticamente
})
```

### Servicios Disponibles

```javascript
// authService.js
- login(username, password)
- register(userData)
- logout()

// appointmentService.js
- getMyAppointments()
- createAppointment(data)
- updateAppointmentStatus(id, status)

// doctorService.js
- getDoctors(specialtyId?)
- getMyProfile()
- getSpecialties()

// patientService.js
- getMyProfile()
- getMedicalRecords()
```

---

## Características Avanzadas

### 1. **Gestión de Estado Global**
- Context API para autenticación
- Estado local con useState/useEffect

### 2. **Manejo de Errores**
- Interceptores de Axios
- Mensajes de error contextuales
- Redirección automática en 401

### 3. **Optimización de Rendimiento**
- Lazy loading de componentes
- Vite con HMR (Hot Module Replacement)
- Build optimizado con tree-shaking

### 4. **Responsive Design**
- Mobile-first approach
- Breakpoints de TailwindCSS
- Componentes adaptables

---

## Despliegue

### Producción con Docker

```bash
# Build de imagen
docker build -t medical-frontend:latest .

# Ejecutar contenedor
docker run -d \
  -p 5173:5173 \
  -e VITE_API_URL=https://api.example.com \
  medical-frontend:latest
```

### Build Manual

```bash
# Generar build de producción
npm run build

# Los archivos estarán en dist/
# Servir con cualquier servidor estático:
# - Nginx
# - Apache
# - Vercel
# - Netlify
```

### Consideraciones de Producción

- ✅ Configurar HTTPS
- ✅ Usar CDN para assets
- ✅ Comprimir archivos (Gzip/Brotli)
- ✅ Implementar service workers
- ✅ Configurar Cache-Control headers
- ✅ Usar variables de entorno para API URL

---

## Testing (Próximamente)

```bash
# Instalar dependencias de testing
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest

# Ejecutar tests
npm run test
```

---

## Personalización del Tema

### Cambiar Colores Principales

Editar `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      medical: {
        600: '#TU_COLOR_AQUI',
      }
    }
  }
}
```

### Agregar Componentes Personalizados

```css
/* src/index.css */
@layer components {
  .mi-boton-custom {
    @apply px-4 py-2 bg-medical-600 text-white rounded-lg;
  }
}
```

---

## Responsive Breakpoints

| Breakpoint | Ancho Mínimo | Uso |
|------------|--------------|-----|
| `sm` | 640px | Teléfonos |
| `md` | 768px | Tablets |
| `lg` | 1024px | Laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Pantallas grandes |

---

## Solución de Problemas

### Error: "Network Error"
```bash
# Verificar que el backend esté ejecutándose
curl http://localhost:8000/health

# Verificar CORS en backend
# Debe permitir http://localhost:5173
```

### Error: "Module not found"
```bash
# Limpiar node_modules y reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Problemas con TailwindCSS
```bash
# Recompilar CSS
npm run dev
```

---

## Contribución

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

## Soporte

Para soporte técnico o preguntas:
- Abrir un issue en GitHub
- Contactar al equipo de desarrollo

---

## 🔗 Enlaces Útiles

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
- [React Router Documentation](https://reactrouter.com/)
- [Axios Documentation](https://axios-http.com/)

---

## 🎉 ¡Gracias por usar Medical Appointment Platform!

Desarrollado con ❤️ para mejorar la gestión de citas médicas.