/*
  # Crear esquema inicial para Sombras de Chile
  
  ## Tablas Creadas
  
  ### 1. users
  Almacena los usuarios registrados en la aplicación
  - `id` (uuid, primary key): Identificador único del usuario
  - `username` (text, unique): Nombre de usuario único
  - `password_hash` (text): Hash de la contraseña (bcrypt)
  - `email` (text, unique): Email del usuario
  - `created_at` (timestamptz): Fecha de registro
  
  ### 2. stories
  Almacena las historias paranormales publicadas
  - `id` (uuid, primary key): Identificador único de la historia
  - `title` (text): Título de la historia
  - `content` (text): Contenido completo de la historia
  - `category` (text): Categoría (Apariciones, Casas Embrujadas, etc.)
  - `author_id` (uuid, foreign key): Referencia al usuario autor
  - `created_at` (timestamptz): Fecha de publicación
  - `updated_at` (timestamptz): Fecha de última actualización
  
  ### 3. sessions
  Almacena las sesiones activas de usuarios
  - `id` (uuid, primary key): Identificador único de la sesión
  - `user_id` (uuid, foreign key): Referencia al usuario
  - `created_at` (timestamptz): Fecha de inicio de sesión
  - `expires_at` (timestamptz): Fecha de expiración de la sesión
  
  ## Seguridad
  
  - RLS habilitado en todas las tablas
  - Políticas de acceso restrictivas por defecto
  - Los usuarios solo pueden ver y modificar sus propios datos
  - Las historias son públicas para lectura, pero solo el autor puede modificarlas
*/

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  username text UNIQUE NOT NULL,
  password_hash text NOT NULL,
  email text UNIQUE NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Crear tabla de historias
CREATE TABLE IF NOT EXISTS stories (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  content text NOT NULL,
  category text NOT NULL,
  author_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Crear tabla de sesiones
CREATE TABLE IF NOT EXISTS sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at timestamptz DEFAULT now(),
  expires_at timestamptz DEFAULT now() + interval '7 days'
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_stories_author ON stories(author_id);
CREATE INDEX IF NOT EXISTS idx_stories_category ON stories(category);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at);

-- Habilitar RLS en todas las tablas
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE stories ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;

-- Políticas para tabla users
-- Los usuarios pueden ver solo su propio perfil
CREATE POLICY "Users can view own profile"
  ON users FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

-- Los usuarios pueden actualizar solo su propio perfil
CREATE POLICY "Users can update own profile"
  ON users FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Permitir registro de nuevos usuarios (público)
CREATE POLICY "Anyone can create account"
  ON users FOR INSERT
  TO anon
  WITH CHECK (true);

-- Políticas para tabla stories
-- Todos pueden leer historias (público)
CREATE POLICY "Anyone can view stories"
  ON stories FOR SELECT
  TO anon, authenticated
  USING (true);

-- Solo usuarios autenticados pueden crear historias
CREATE POLICY "Authenticated users can create stories"
  ON stories FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = author_id);

-- Solo el autor puede actualizar su historia
CREATE POLICY "Authors can update own stories"
  ON stories FOR UPDATE
  TO authenticated
  USING (auth.uid() = author_id)
  WITH CHECK (auth.uid() = author_id);

-- Solo el autor puede eliminar su historia
CREATE POLICY "Authors can delete own stories"
  ON stories FOR DELETE
  TO authenticated
  USING (auth.uid() = author_id);

-- Políticas para tabla sessions
-- Los usuarios pueden ver solo sus propias sesiones
CREATE POLICY "Users can view own sessions"
  ON sessions FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

-- Los usuarios pueden crear sus propias sesiones
CREATE POLICY "Users can create own sessions"
  ON sessions FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- Los usuarios pueden eliminar sus propias sesiones
CREATE POLICY "Users can delete own sessions"
  ON sessions FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar updated_at en stories
CREATE TRIGGER update_stories_updated_at BEFORE UPDATE ON stories
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();