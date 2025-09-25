"""
login.py
Pantalla de login para la app.
Permite al usuario iniciar sesión con validación mejorada y gestiona la sesión activa.
"""

from kivymd.uix.screen import MDScreen  # Pantalla base KivyMD
from kivymd.uix.dialog import MDDialog  # Diálogo para mostrar mensajes
from models.user import UserManager, SessionManager  # Gestores de usuario y sesión
from kivy.app import App

class LoginScreen(MDScreen):
    """
    Pantalla de inicio de sesión.
    Permite validar credenciales con validación mejorada y guardar la sesión activa.
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
        Obtiene los datos del formulario con validación mejorada.
        Si es correcto, guarda la sesión y navega a la pantalla principal.
        """
        username = self.ids.username.text.strip()
        password = self.ids.password.text
        
        # Validaciones básicas
        if not username:
            self.show_dialog('Por favor, ingresa tu nombre de usuario.')
            return
        
        if not password:
            self.show_dialog('Por favor, ingresa tu contraseña.')
            return
        
        # Validar credenciales
        users = UserManager.load_users()
        user = next((u for u in users if u['username'].strip() == username and u['password'] == password), None)
        
        if user:
            SessionManager.save_session(username)
            self.show_dialog('¡Login exitoso!')
            # Navegar a la pantalla principal con navegación
            App.get_running_app().screen_manager.current = 'main'
        else:
            self.show_dialog('Usuario o contraseña incorrectos.')
    
    def on_enter(self, *args):
        """
        Se ejecuta al entrar a la pantalla.
        Limpia los campos del formulario.
        """
        self.ids.username.text = ''
        self.ids.password.text = ''
