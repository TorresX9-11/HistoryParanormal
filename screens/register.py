# register.py
# Pantalla de registro de usuario

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from models.user import UserManager

class RegisterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

    def show_dialog(self, text):
        if not self.dialog:
            self.dialog = MDDialog(text=text)
        else:
            self.dialog.text = text
        self.dialog.open()

    def register_user(self):
        username = self.ids.username.text
        email = self.ids.email.text
        password = self.ids.password.text
        success, msg = UserManager.register_user(username, password, email)
        self.show_dialog(msg)
