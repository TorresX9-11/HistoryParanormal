"""
Archivo principal de la aplicación Sombras de Chile.
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

# Eliminar la variable KV con la cadena larga

class HistoryParanormalApp(MDApp):
    """
    Clase principal de la aplicación. Hereda de MDApp.
    Se encarga de construir la interfaz y gestionar las pantallas.
    """
    def build(self):
        # Configurar tema oscuro
        self.theme_cls.theme_style = "Dark"  # Tema oscuro
        self.theme_cls.primary_palette = "Red"  # Color primario rojo
        self.theme_cls.primary_hue = "900"  # Tono oscuro del rojo
        
        # Configuración para dispositivos móviles
        from kivy.core.window import Window
        from kivy.utils import platform
        
        # Ajustar la ventana según la plataforma
        if platform in ('android', 'ios'):
            # En dispositivos móviles, usar pantalla completa
            Window.softinput_mode = 'below_target'
        else:
            # En escritorio, establecer un tamaño razonable
            Window.size = (400, 700)  # Simular tamaño de móvil para pruebas
        
        # Título de la aplicación
        self.title = "SOMBRAS DE CHILE"
        
        # Carga el archivo KV principal
        self.screen_manager = Builder.load_file("kv/main.kv")
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
