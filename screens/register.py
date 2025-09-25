"""
register.py
Pantalla de registro de usuario.
Contiene la lógica para registrar nuevos usuarios con validación mejorada.
"""

from kivymd.uix.screen import MDScreen  # Pantalla base KivyMD
from kivymd.uix.dialog import MDDialog  # Diálogo para mostrar mensajes
from models.user import UserManager     # Gestor de usuarios
import re  # Para validación de email

class RegisterScreen(MDScreen):
    """
    Pantalla de registro.
    Permite al usuario crear una cuenta nueva con validación completa.
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
        Obtiene los datos del formulario con validación completa y registra el usuario.
        Incluye validaciones de formato y longitud.
        """
        username = self.ids.username.text.strip()
        email = self.ids.email.text.strip()
        password = self.ids.password.text
        
        # Validaciones mejoradas
        if not username:
            self.show_dialog('Por favor, ingresa un nombre de usuario.')
            return
        
        if len(username) < 3:
            self.show_dialog('El nombre de usuario debe tener al menos 3 caracteres.')
            return
        
        if not email:
            self.show_dialog('Por favor, ingresa tu correo electrónico.')
            return
        
        # Validar formato de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            self.show_dialog('Por favor, ingresa un correo electrónico válido.')
            return
        
        if not password:
            self.show_dialog('Por favor, ingresa una contraseña.')
            return
        
        if len(password) < 6:
            self.show_dialog('La contraseña debe tener al menos 6 caracteres.')
            return
        
        # Registrar usuario
        success, msg = UserManager.register_user(username, password, email)
        self.show_dialog(msg)
        
        # Si el registro fue exitoso, limpiar formulario
        if success:
            self.clear_form()
    
    def clear_form(self):
        """
        Limpia todos los campos del formulario.
        """
        self.ids.username.text = ''
        self.ids.email.text = ''
        self.ids.password.text = ''
    
    def on_enter(self, *args):
        """
        Se ejecuta al entrar a la pantalla.
        Limpia los campos del formulario.
        """
        self.clear_form()
