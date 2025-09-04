"""
register.py
Pantalla de registro de usuario.
Contiene la lógica para registrar nuevos usuarios y mostrar mensajes de estado.
"""

from kivymd.uix.screen import MDScreen  # Pantalla base KivyMD
from kivymd.uix.dialog import MDDialog  # Diálogo para mostrar mensajes
from models.user import UserManager     # Gestor de usuarios

class RegisterScreen(MDScreen):
    """
    Pantalla de registro.
    Permite al usuario crear una cuenta nueva y muestra mensajes de éxito o error.
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

    def register_user(self):
        """
        Obtiene los datos del formulario, los normaliza y registra el usuario.
        Muestra el resultado en un diálogo.
        """
        username = self.ids.username.text.strip()
        email = self.ids.email.text.strip()
        password = self.ids.password.text
        success, msg = UserManager.register_user(username, password, email)
        self.show_dialog(msg)
