"""
Archivo principal de la aplicación Sombras de Chile.
Aplicación de historias paranormales con diseño moderno basado en Figma.
Contiene la definición de la app, carga de pantallas y layouts, y el ciclo principal.
"""
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from screens.register import RegisterScreen
from screens.login import LoginScreen
from screens.home import HomeScreen
from screens.explore import ExploreScreen
from screens.profile import ProfileScreen
from screens.story_detail import StoryDetailScreen
from screens.story_form import StoryFormScreen

class MenuScreen(MDScreen):
    """
    Pantalla principal del menú de bienvenida.
    Hereda de MDScreen, solo sirve como contenedor visual.
    """
    pass

class MainNavigationScreen(MDScreen):
    """
    Pantalla principal con navegación inferior.
    Contiene las pestañas principales de la aplicación.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_navigation()
    
    def build_navigation(self):
        """
        Construye la navegación inferior con las pestañas principales.
        """
        # Crear el contenedor principal
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Crear la navegación inferior
        bottom_nav = MDBottomNavigation(
            panel_color=[0.05, 0.05, 0.05, 1],  # Fondo oscuro
            text_color_active=[0.8, 0.1, 0.1, 1],  # Rojo activo
            text_color_normal=[0.5, 0.5, 0.5, 1],  # Gris inactivo
        )
        
        # Pestaña Home
        home_item = MDBottomNavigationItem(
            name='home',
            text='Inicio',
            icon='home'
        )
        home_item.add_widget(HomeScreen())
        bottom_nav.add_widget(home_item)
        
        # Pestaña Explorar
        explore_item = MDBottomNavigationItem(
            name='explore',
            text='Explorar',
            icon='compass'
        )
        explore_item.add_widget(ExploreScreen())
        bottom_nav.add_widget(explore_item)
        
        # Pestaña Perfil
        profile_item = MDBottomNavigationItem(
            name='profile',
            text='Perfil',
            icon='account'
        )
        profile_item.add_widget(ProfileScreen())
        bottom_nav.add_widget(profile_item)
        
        main_layout.add_widget(bottom_nav)
        self.add_widget(main_layout)

class HistoryParanormalApp(MDApp):
    """
    Clase principal de la aplicación. Hereda de MDApp.
    Se encarga de construir la interfaz y gestionar las pantallas.
    """
    def build(self):
        """
        Construye la aplicación con tema personalizado y configuración responsiva.
        """
        # Configurar tema personalizado
        self.theme_cls.theme_style = "Dark"  # Tema oscuro
        self.theme_cls.primary_palette = "Red"  # Color primario rojo
        self.theme_cls.primary_hue = "900"  # Tono oscuro del rojo
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.accent_hue = "700"
        
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
        
        # Crear el gestor de pantallas
        self.screen_manager = MDScreenManager()
        
        # Agregar todas las pantallas
        self.screen_manager.add_widget(MenuScreen(name='menu'))
        self.screen_manager.add_widget(RegisterScreen(name='register'))
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(MainNavigationScreen(name='main'))
        self.screen_manager.add_widget(StoryDetailScreen(name='story_detail'))
        self.screen_manager.add_widget(StoryFormScreen(name='story_form'))
        
        # Cargar el archivo KV principal
        Builder.load_file("kv/main.kv")
        
        # Retorna el gestor de pantallas como raíz de la app
        return self.screen_manager

if __name__ == "__main__":
    # Punto de entrada principal. Inicia la app.
    HistoryParanormalApp().run()