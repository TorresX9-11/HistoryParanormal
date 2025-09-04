"""
Archivo principal de la aplicación History Paranormal Chile.
Contiene la definición de la app, carga de pantallas y layouts, y el ciclo principal.
"""
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from screens.register import RegisterScreen
from screens.login import LoginScreen
from screens.public import PublicScreen
from screens.user_panel import UserPanelScreen
from screens.story_form import StoryFormScreen

class MenuScreen(MDScreen):
    """
    Pantalla principal del menú de bienvenida.
    Hereda de MDScreen, solo sirve como contenedor visual.
    """
    pass

KV = '''
    # Definición de la interfaz gráfica en lenguaje KV
MDScreenManager:
    MenuScreen:
    RegisterScreen:
    LoginScreen:
    PublicScreen:
    UserPanelScreen:
    StoryFormScreen:

<MenuScreen@MDScreen>:
    MDLabel:
        text: 'Bienvenido a History Paranormal Chile'
        halign: 'center'
        pos_hint: {"center_y": 0.7}
    MDRaisedButton:
        text: 'Ver publicaciones'
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        on_release: app.root.current = 'public'
    MDRaisedButton:
        text: 'Iniciar sesión'
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        on_release: app.root.current = 'login'

<PublicScreen>:
    BoxLayout:
        orientation: 'vertical'
        ScrollView:
            MDList:
                id: stories_list
        MDRaisedButton:
            text: 'Volver'
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = 'MenuScreen'

<RegisterScreen>:
    BoxLayout:
        orientation: 'vertical'
        MDTextField:
            id: username
            hint_text: "Nombre de usuario"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
        MDTextField:
            id: email
            hint_text: "Correo electrónico"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
        MDTextField:
            id: password
            hint_text: "Contraseña"
            password: True
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
        MDRaisedButton:
            text: "Registrarse"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.get_screen('register').register_user()
        MDRaisedButton:
            text: 'Volver'
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = 'MenuScreen'

<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        MDTextField:
            id: username
            hint_text: "Nombre de usuario"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
        MDTextField:
            id: password
            hint_text: "Contraseña"
            password: True
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
        MDRaisedButton:
            text: "Iniciar sesión"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.get_screen('login').login_user()
        MDRaisedButton:
            text: '¿No tienes cuenta? Regístrate'
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = 'register'
        MDRaisedButton:
            text: 'Volver'
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = 'MenuScreen'

<UserPanelScreen>:
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: 'Historias Paranormales de Chile'
            halign: 'center'
        ScrollView:
            MDList:
                id: user_stories_list
        MDRaisedButton:
            text: 'Mis historias'
            pos_hint: {"center_x": 0.5}
            on_release: app.root.get_screen('userpanel').show_my_stories()
        MDRaisedButton:
            text: 'Crear nueva historia'
            pos_hint: {"center_x": 0.5}
            on_release: app.root.get_screen('userpanel').open_story_form()
        MDRaisedButton:
            text: 'Volver'
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = 'MenuScreen'

<StoryFormScreen>:
    BoxLayout:
        orientation: 'vertical'
        MDTextField:
            id: title
            hint_text: "Título de la historia"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
        MDTextField:
            id: content
            hint_text: "Relato"
            multiline: True
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
        MDTextField:
            id: category
            hint_text: "Zona/Categoría"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
            on_focus: if self.focus: app.root.get_screen('storyform').open_category_menu(self)
        MDRaisedButton:
            text: "Publicar"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.get_screen('storyform').publish_story()
        MDRaisedButton:
            text: 'Volver'
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = 'userpanel'
'''

class HistoryParanormalApp(MDApp):
    """
    Clase principal de la aplicación. Hereda de MDApp.
    Se encarga de construir la interfaz y gestionar las pantallas.
    """
    def build(self):
        # Carga el layout KV y crea el gestor de pantallas
        self.screen_manager = Builder.load_string(KV)
        # Agrega cada pantalla al gestor con su nombre único
        self.screen_manager.add_widget(MenuScreen(name='MenuScreen'))
        self.screen_manager.add_widget(RegisterScreen(name='register'))
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(PublicScreen(name='public'))
        self.screen_manager.add_widget(UserPanelScreen(name='userpanel'))
        self.screen_manager.add_widget(StoryFormScreen(name='storyform'))
        # Retorna el gestor de pantallas como raíz de la app
        return self.screen_manager

if __name__ == "__main__":
    # Punto de entrada principal. Inicia la app.
    HistoryParanormalApp().run()
