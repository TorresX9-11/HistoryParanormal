"""
login.py
Pantalla de login para la app.
Permite al usuario iniciar sesión y gestiona la sesión activa.
"""

from kivymd.uix.screen import MDScreen  # Pantalla base KivyMD
from kivymd.uix.dialog import MDDialog  # Diálogo para mostrar mensajes
from models.user import UserManager, SessionManager  # Gestores de usuario y sesión

class LoginScreen(MDScreen):
    """
    Pantalla de inicio de sesión.
    Permite validar credenciales y guardar la sesión activa.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None  # Diálogo reutilizable

    def show_dialog(self, text):
        """
        Muestra un diálogo con el texto proporcionado.
        """
        if not self.dialog:
            self.dialog = MDDialog(text=text)
        else:
            self.dialog.text = text
        self.dialog.open()

    def login_user(self):
        """
        Obtiene los datos del formulario, los normaliza y valida el usuario.
        Si es correcto, guarda la sesión y navega al panel de usuario.
        """
        username = self.ids.username.text.strip()
        password = self.ids.password.text
        users = UserManager.load_users()
        user = next((u for u in users if u['username'].strip() == username and u['password'] == password), None)
        if user:
            SessionManager.save_session(username)
            self.show_dialog('¡Login exitoso!')
            from kivy.app import App
            App.get_running_app().root.current = 'userpanel'
        else:
            self.show_dialog('Usuario o contraseña incorrectos.')
