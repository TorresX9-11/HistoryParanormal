# Sombras de Chile - Aplicación de Historias Paranormales

Una aplicación móvil desarrollada en Python con Kivy/KivyMD para compartir experiencias paranormales y relatos de terror.

## 🎯 Características Principales

- **Diseño Moderno**: Interfaz basada en Material Design con tema oscuro
- **Navegación Intuitiva**: Navegación por pestañas en la parte inferior
- **Gestión de Usuarios**: Sistema completo de registro y autenticación
- **Publicación de Historias**: Formulario avanzado para crear y editar historias
- **Exploración**: Búsqueda y filtrado por categorías
- **Responsive**: Adaptable a diferentes tamaños de pantalla

## 🏗️ Arquitectura del Proyecto

```
sombras-de-chile/
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
├── .env                    # Variables de entorno (Supabase)
├── config/                 # Configuración
│   └── supabase_client.py # Cliente singleton de Supabase
├── models/                 # Modelos de datos
│   ├── user.py            # Gestión de usuarios y sesiones con Supabase
│   ├── story.py           # Gestión de historias con Supabase
│   ├── users.json         # DEPRECATED - migrado a Supabase
│   ├── stories.json       # DEPRECATED - migrado a Supabase
│   └── session.json       # DEPRECATED - migrado a Supabase
├── screens/               # Pantallas de la aplicación
│   ├── home.py           # Pantalla principal con historias
│   ├── explore.py        # Exploración y búsqueda
│   ├── profile.py        # Perfil de usuario
│   ├── story_detail.py   # Detalle de historia
│   ├── story_form.py     # Formulario de historias
│   ├── login.py          # Inicio de sesión
│   └── register.py       # Registro de usuarios
├── kv/                   # Archivos de diseño KV
│   ├── main.kv          # Configuración principal
│   ├── menu.kv          # Pantalla de bienvenida
│   ├── login.kv         # Diseño de login
│   └── register.kv      # Diseño de registro
└── assets/              # Recursos multimedia
    └── LogoApp.png      # Logo de la aplicación
```

## 🚀 Instalación y Configuración

### Requisitos Previos

```bash
# Python 3.8 o superior
python --version

# Instalar dependencias
pip install -r requirements.txt
```

Las dependencias incluyen:
- kivy >= 2.1.0
- kivymd >= 1.1.1
- supabase >= 2.0.0
- bcrypt >= 4.0.0
- python-dotenv >= 1.0.0

### Configuración de Base de Datos

El proyecto utiliza Supabase como base de datos. Las credenciales ya están configuradas en el archivo `.env`:

```
VITE_SUPABASE_URL=https://dgahoefxebndkoxuinpc.supabase.co
VITE_SUPABASE_SUPABASE_ANON_KEY=<tu-clave-anon>
```

La migración inicial de la base de datos ya fue aplicada, creando las siguientes tablas:
- `users`: Usuarios con contraseñas hasheadas
- `stories`: Historias paranormales
- `sessions`: Sesiones de usuarios

### Ejecución

```bash
# Ejecutar la aplicación
python main.py
```

## 📱 Pantallas y Funcionalidades

### 1. Pantalla de Bienvenida (`MenuScreen`)
- Logo y branding de la aplicación
- Botones para explorar historias o iniciar sesión
- Diseño responsivo con adaptación móvil/escritorio

### 2. Sistema de Autenticación
- **Registro**: Validación completa de datos (email, contraseña, usuario único)
- **Login**: Autenticación segura con gestión de sesiones
- **Validaciones**: Formato de email, longitud mínima, campos requeridos

### 3. Navegación Principal (`MainNavigationScreen`)
Navegación por pestañas con tres secciones principales:

#### 🏠 Inicio (`HomeScreen`)
- Saludo personalizado al usuario
- Cards modernas para mostrar historias recientes
- Navegación directa al detalle de cada historia
- Diseño tipo feed de redes sociales

#### 🧭 Explorar (`ExploreScreen`)
- Barra de búsqueda en tiempo real
- Filtros por categoría con chips interactivos
- Grid de resultados con cards
- Categorías: Apariciones, Casas Embrujadas, Cementerios, etc.

#### 👤 Perfil (`ProfileScreen`)
- Card de perfil con avatar personalizado
- Estadísticas del usuario (número de historias)
- Botones de acción: crear historia, ver mis historias, cerrar sesión
- Historial de historias del usuario

### 4. Gestión de Historias

#### 📖 Detalle de Historia (`StoryDetailScreen`)
- Vista completa del contenido
- Información del autor y categoría
- Botones de interacción (me gusta, comentarios, compartir)
- Toolbar con navegación y acciones

#### ✍️ Formulario de Historia (`StoryFormScreen`)
- Editor avanzado con validación en tiempo real
- Selector de categorías con menú desplegable
- Contador de caracteres (límite 2000)
- Validaciones: título mínimo 5 caracteres, contenido mínimo 50 caracteres
- Modo edición para historias existentes

## 🎨 Diseño y UX

### Tema Visual
- **Colores**: Esquema oscuro con acentos rojos (#CC1919)
- **Tipografía**: Material Design con jerarquía clara
- **Cards**: Bordes redondeados, elevación y espaciado consistente
- **Iconografía**: Material Design Icons

### Responsividad
- Detección automática de dispositivos móviles
- Padding y spacing adaptativos
- Tamaños de fuente escalables
- Layout flexible para diferentes resoluciones

### Micro-interacciones
- Efectos ripple en botones y cards
- Transiciones suaves entre pantallas
- Feedback visual en formularios
- Estados hover y focus

## 🔧 Modelos de Datos

### Esquema de Base de Datos (Supabase)

#### Tabla `users`
```sql
{
    "id": uuid (PK),           # Identificador único
    "username": text (UNIQUE), # Nombre único del usuario
    "password_hash": text,     # Hash bcrypt de la contraseña
    "email": text (UNIQUE),    # Email válido
    "created_at": timestamptz  # Fecha de registro
}
```

#### Tabla `stories`
```sql
{
    "id": uuid (PK),           # Identificador único
    "title": text,             # Título de la historia
    "content": text,           # Contenido completo
    "category": text,          # Categoría seleccionada
    "author_id": uuid (FK),    # Referencia al usuario autor
    "created_at": timestamptz, # Fecha de publicación
    "updated_at": timestamptz  # Fecha de última actualización
}
```

#### Tabla `sessions`
```sql
{
    "id": uuid (PK),           # Identificador único
    "user_id": uuid (FK),      # Referencia al usuario
    "created_at": timestamptz, # Fecha de inicio
    "expires_at": timestamptz  # Fecha de expiración (7 días)
}
```

## 🛠️ Componentes Personalizados

### `StoryCard`
Card reutilizable para mostrar historias con:
- Header con categoría y botón de favoritos
- Título y preview del contenido
- Footer con autor y botón de compartir
- Navegación automática al detalle

### `ProfileCard`
Card de perfil con:
- Avatar circular con inicial del usuario
- Información básica y estadísticas
- Diseño consistente con el tema

## 📊 Gestión de Estado

- **Persistencia**: Supabase PostgreSQL para almacenamiento en la nube
- **Sesiones**: Gestión automática con expiración de 7 días
- **Validaciones**: Validación en tiempo real en formularios
- **Navegación**: Stack de pantallas con historial
- **Seguridad**: RLS (Row Level Security) en todas las operaciones

## 🔒 Seguridad

- Validación de entrada en todos los formularios
- Sanitización de datos antes del almacenamiento
- Gestión segura de sesiones con Supabase
- Validación de formato de email con regex
- Contraseñas hasheadas con bcrypt
- Row Level Security (RLS) habilitado en todas las tablas
- Políticas restrictivas por defecto
- Los usuarios solo pueden modificar sus propios datos
- Las historias son públicas para lectura, privadas para edición

## 🚀 Mejoras Futuras

- [ ] Sistema de comentarios y likes
- [ ] Notificaciones push
- [ ] Compartir en redes sociales
- [ ] Modo offline con sincronización
- [ ] Sistema de favoritos
- [ ] Búsqueda avanzada con filtros múltiples
- [ ] Categorías personalizadas
- [ ] Sistema de moderación
- [ ] Estadísticas avanzadas de usuario
- [ ] Temas personalizables

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Equipo de Desarrollo

- **Desarrollador Principal**: [Tu Nombre]
- **Diseño UX/UI**: Basado en Figma Design System
- **Arquitectura**: Patrón MVC con Kivy/KivyMD

---

**Sombras de Chile** - Donde cada historia cobra vida en la oscuridad 🌙