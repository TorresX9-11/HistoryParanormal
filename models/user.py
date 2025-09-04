"""
user.py
Modelo de datos para usuario y gestión de sesión.
Incluye clases y funciones para registrar, guardar y cargar usuarios, y gestionar la sesión activa.
"""

import json  # Para manejo de archivos JSON
import os    # Para rutas de archivos

USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')  # Ruta al archivo de usuarios

class User:
    """
    Representa un usuario de la app.
    """
    def __init__(self, username, password, email):
        self.username = username
        self.password = password  # En producción, usar hash
        self.email = email

    def to_dict(self):
        """
        Convierte el usuario a un diccionario para guardar en JSON.
        """
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email
        }

class UserManager:
    """
    Clase estática para gestionar usuarios: cargar, guardar y registrar.
    """
    @staticmethod
    def load_users():
        """
        Carga la lista de usuarios desde el archivo JSON.
        """
        if not os.path.exists(USERS_FILE):
            return []
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_users(users):
        """
        Guarda la lista de usuarios en el archivo JSON.
        """
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    @staticmethod
    def register_user(username, password, email):
        """
        Registra un nuevo usuario si el nombre no existe.
        """
        users = UserManager.load_users()
        if any(u['username'] == username for u in users):
            return False, 'El usuario ya existe.'
        new_user = User(username, password, email)
        users.append(new_user.to_dict())
        UserManager.save_users(users)
        return True, 'Usuario registrado exitosamente.'

class SessionManager:
    """
    Clase estática para gestionar la sesión activa del usuario.
    """
    SESSION_FILE = os.path.join(os.path.dirname(__file__), 'session.json')

    @staticmethod
    def save_session(username):
        """
        Guarda el usuario actual en el archivo de sesión.
        """
        with open(SessionManager.SESSION_FILE, 'w', encoding='utf-8') as f:
            json.dump({'username': username}, f)

    @staticmethod
    def get_session():
        """
        Obtiene el usuario actual de la sesión guardada.
        """
        if not os.path.exists(SessionManager.SESSION_FILE):
            return None
        with open(SessionManager.SESSION_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('username')

    @staticmethod
    def clear_session():
        if os.path.exists(SessionManager.SESSION_FILE):
            os.remove(SessionManager.SESSION_FILE)
