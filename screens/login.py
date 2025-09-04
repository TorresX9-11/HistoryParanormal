# login.py
# Pantalla de login para la app

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from models.user import UserManager, SessionManager

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

    def show_dialog(self, text):
        if not self.dialog:
            self.dialog = MDDialog(text=text)
        else:
            self.dialog.text = text
        self.dialog.open()

    def login_user(self):
        username = self.ids.username.text
        password = self.ids.password.text
        users = UserManager.load_users()
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            SessionManager.save_session(username)
            self.show_dialog('¡Login exitoso!')
            # Aquí puedes navegar al panel de usuario
        else:
            self.show_dialog('Usuario o contraseña incorrectos.')
