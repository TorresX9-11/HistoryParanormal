# user.py
# Modelo de datos para usuario

# Aquí irá la clase User y funciones relacionadas

import json
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password  # En producción, usar hash
        self.email = email

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email
        }

class UserManager:
    @staticmethod
    def load_users():
        if not os.path.exists(USERS_FILE):
            return []
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_users(users):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    @staticmethod
    def register_user(username, password, email):
        users = UserManager.load_users()
        if any(u['username'] == username for u in users):
            return False, 'El usuario ya existe.'
        new_user = User(username, password, email)
        users.append(new_user.to_dict())
        UserManager.save_users(users)
        return True, 'Usuario registrado exitosamente.'

class SessionManager:
    SESSION_FILE = os.path.join(os.path.dirname(__file__), 'session.json')

    @staticmethod
    def save_session(username):
        with open(SessionManager.SESSION_FILE, 'w', encoding='utf-8') as f:
            json.dump({'username': username}, f)

    @staticmethod
    def get_session():
        if not os.path.exists(SessionManager.SESSION_FILE):
            return None
        with open(SessionManager.SESSION_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('username')

    @staticmethod
    def clear_session():
        if os.path.exists(SessionManager.SESSION_FILE):
            os.remove(SessionManager.SESSION_FILE)
