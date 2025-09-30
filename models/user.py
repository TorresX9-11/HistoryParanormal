"""
user.py
Modelo de datos para usuario y gestión de sesión con Supabase.
Incluye clases y funciones para registrar, autenticar usuarios y gestionar sesiones.
"""

import bcrypt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_client import get_supabase_client
from datetime import datetime, timedelta

class User:
    """
    Representa un usuario de la app.
    """
    def __init__(self, id, username, email, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = created_at

    @staticmethod
    def from_dict(data):
        """
        Crea un usuario desde un diccionario de Supabase.
        """
        return User(
            id=data.get('id'),
            username=data.get('username'),
            email=data.get('email'),
            created_at=data.get('created_at')
        )

class UserManager:
    """
    Clase estática para gestionar usuarios con Supabase.
    """
    @staticmethod
    def _hash_password(password):
        """
        Genera un hash seguro de la contraseña usando bcrypt.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def _verify_password(password, password_hash):
        """
        Verifica si una contraseña coincide con su hash.
        """
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    @staticmethod
    def get_user_by_username(username):
        """
        Obtiene un usuario por su nombre de usuario.
        """
        try:
            supabase = get_supabase_client()
            response = supabase.table('users').select('*').eq('username', username).maybeSingle().execute()
            if response.data:
                return User.from_dict(response.data)
            return None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None

    @staticmethod
    def register_user(username, password, email):
        """
        Registra un nuevo usuario en Supabase.
        """
        try:
            supabase = get_supabase_client()

            existing_user = supabase.table('users').select('username').eq('username', username).maybeSingle().execute()
            if existing_user.data:
                return False, 'El usuario ya existe.'

            existing_email = supabase.table('users').select('email').eq('email', email).maybeSingle().execute()
            if existing_email.data:
                return False, 'El email ya está registrado.'

            password_hash = UserManager._hash_password(password)

            new_user = {
                'username': username,
                'password_hash': password_hash,
                'email': email
            }

            response = supabase.table('users').insert(new_user).execute()

            if response.data:
                return True, 'Usuario registrado exitosamente.'
            return False, 'Error al registrar usuario.'

        except Exception as e:
            print(f"Error en registro: {e}")
            return False, f'Error al registrar usuario: {str(e)}'

    @staticmethod
    def authenticate_user(username, password):
        """
        Autentica un usuario verificando su contraseña.
        """
        try:
            supabase = get_supabase_client()
            response = supabase.table('users').select('*').eq('username', username).maybeSingle().execute()

            if not response.data:
                return False, 'Usuario no encontrado.'

            user_data = response.data
            if UserManager._verify_password(password, user_data['password_hash']):
                return True, User.from_dict(user_data)
            else:
                return False, 'Contraseña incorrecta.'

        except Exception as e:
            print(f"Error en autenticación: {e}")
            return False, f'Error al autenticar: {str(e)}'

class SessionManager:
    """
    Clase estática para gestionar sesiones con Supabase.
    """
    _current_session = None

    @staticmethod
    def create_session(user_id):
        """
        Crea una nueva sesión en Supabase.
        """
        try:
            supabase = get_supabase_client()

            SessionManager.clear_expired_sessions(user_id)

            expires_at = datetime.now() + timedelta(days=7)

            session_data = {
                'user_id': user_id,
                'expires_at': expires_at.isoformat()
            }

            response = supabase.table('sessions').insert(session_data).execute()

            if response.data:
                SessionManager._current_session = response.data[0]
                return True
            return False

        except Exception as e:
            print(f"Error al crear sesión: {e}")
            return False

    @staticmethod
    def get_current_user():
        """
        Obtiene el usuario de la sesión actual.
        """
        try:
            if SessionManager._current_session:
                user_id = SessionManager._current_session['user_id']
                supabase = get_supabase_client()
                response = supabase.table('users').select('*').eq('id', user_id).maybeSingle().execute()

                if response.data:
                    return User.from_dict(response.data)
            return None

        except Exception as e:
            print(f"Error al obtener usuario actual: {e}")
            return None

    @staticmethod
    def clear_session():
        """
        Elimina la sesión actual.
        """
        try:
            if SessionManager._current_session:
                supabase = get_supabase_client()
                session_id = SessionManager._current_session['id']
                supabase.table('sessions').delete().eq('id', session_id).execute()
                SessionManager._current_session = None
            return True

        except Exception as e:
            print(f"Error al limpiar sesión: {e}")
            return False

    @staticmethod
    def clear_expired_sessions(user_id):
        """
        Elimina sesiones expiradas del usuario.
        """
        try:
            supabase = get_supabase_client()
            now = datetime.now().isoformat()
            supabase.table('sessions').delete().eq('user_id', user_id).lt('expires_at', now).execute()

        except Exception as e:
            print(f"Error al limpiar sesiones expiradas: {e}")

    @staticmethod
    def get_session():
        """
        Obtiene el username de la sesión actual (compatibilidad).
        """
        user = SessionManager.get_current_user()
        return user.username if user else None
