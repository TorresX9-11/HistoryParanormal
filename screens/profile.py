"""
profile.py
Pantalla de perfil de usuario.
Muestra información del usuario, sus historias y opciones de configuración.
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget
from kivy.metrics import dp
from kivy.app import App
from models.user import SessionManager
from models.story import StoryManager
from screens.home import StoryCard

class ProfileCard(MDCard):
    """
    Card de perfil con información del usuario.
    """
    def __init__(self, username, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.setup_card()
    
    def setup_card(self):
        """
        Configura el diseño de la card de perfil.
        """
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(150)
        self.md_bg_color = [0.1, 0.1, 0.1, 1]
        self.elevation = 3
        self.radius = [15, 15, 15, 15]
        self.padding = dp(20)
        self.spacing = dp(12)
        
        # Avatar (placeholder con inicial)
        avatar_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(16)
        )
        
        # Círculo con inicial del usuario
        avatar_card = MDCard(
            size_hint=(None, None),
            size=(dp(60), dp(60)),
            md_bg_color=[0.8, 0.1, 0.1, 1],
            radius=[30, 30, 30, 30],
            elevation=2
        )
        
        avatar_label = MDLabel(
            text=self.username[0].upper() if self.username else "U",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_style="H4",
            halign="center",
            valign="middle"
        )
        avatar_card.add_widget(avatar_label)
        avatar_layout.add_widget(avatar_card)
        
        # Información del usuario
        info_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(4)
        )
        
        username_label = MDLabel(
            text=self.username,
            theme_text_color="Primary",
            font_style="H6"
        )
        info_layout.add_widget(username_label)
        
        # Estadísticas básicas
        stories_count = len([s for s in StoryManager.load_stories() if s.get('author') == self.username])
        stats_label = MDLabel(
            text=f"{stories_count} historias publicadas",
            theme_text_color="Secondary",
            font_style="Caption"
        )
        info_layout.add_widget(stats_label)
        
        avatar_layout.add_widget(info_layout)
        self.add_widget(avatar_layout)

class ProfileScreen(MDScreen):
    """
    Pantalla de perfil del usuario.
    Muestra información personal, historias del usuario y opciones.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.setup_ui()
    
    def setup_ui(self):
        """
        Configura la interfaz de usuario del perfil.
        """
        # Layout principal
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(16),
            spacing=dp(16)
        )
        
        # Header
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50)
        )
        
        title_label = MDLabel(
            text="Mi Perfil",
            theme_text_color="Primary",
            font_style="H5",
            size_hint_x=0.8
        )
        header_layout.add_widget(title_label)
        
        # Botón de configuración
        settings_button = MDIconButton(
            icon="cog",
            theme_icon_color="Custom",
            icon_color=[0.8, 0.1, 0.1, 1],
            on_release=self.open_settings
        )
        header_layout.add_widget(settings_button)
        
        main_layout.add_widget(header_layout)
        
        # ScrollView principal
        scroll_view = MDScrollView()
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_y=None,
            height=dp(0)
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Card de perfil
        username = SessionManager.get_session()
        if username:
            profile_card = ProfileCard(username)
            content_layout.add_widget(profile_card)
        
        # Botones de acción
        actions_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(12),
            size_hint_y=None,
            height=dp(200)
        )
        
        # Botón para crear nueva historia
        create_button = MDRaisedButton(
            text="CREAR NUEVA HISTORIA",
            md_bg_color=[0.8, 0.1, 0.1, 1],
            size_hint_y=None,
            height=dp(45),
            on_release=self.create_new_story
        )
        actions_layout.add_widget(create_button)
        
        # Botón para ver mis historias
        my_stories_button = MDRaisedButton(
            text="MIS HISTORIAS",
            md_bg_color=[0.5, 0.5, 0.5, 1],
            size_hint_y=None,
            height=dp(45),
            on_release=self.show_my_stories
        )
        actions_layout.add_widget(my_stories_button)
        
        # Botón para cerrar sesión
        logout_button = MDRaisedButton(
            text="CERRAR SESIÓN",
            md_bg_color=[0.3, 0.3, 0.3, 1],
            size_hint_y=None,
            height=dp(45),
            on_release=self.logout
        )
        actions_layout.add_widget(logout_button)
        
        content_layout.add_widget(actions_layout)
        
        # Sección de mis historias
        my_stories_label = MDLabel(
            text="Mis Historias Recientes",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        content_layout.add_widget(my_stories_label)
        
        # Grid para historias del usuario
        self.user_stories_grid = MDGridLayout(
            cols=1,
            spacing=dp(12),
            size_hint_y=None,
            height=dp(0)
        )
        self.user_stories_grid.bind(minimum_height=self.user_stories_grid.setter('height'))
        
        content_layout.add_widget(self.user_stories_grid)
        
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
        
        # Cargar historias del usuario
        self.load_user_stories()
    
    def load_user_stories(self):
        """
        Carga las historias del usuario actual.
        """
        username = SessionManager.get_session()
        if not username:
            return
        
        stories = StoryManager.load_stories()
        user_stories = [s for s in stories if s.get('author') == username]
        
        self.user_stories_grid.clear_widgets()
        
        if not user_stories:
            no_stories_label = MDLabel(
                text="Aún no has publicado historias",
                theme_text_color="Secondary",
                halign="center",
                size_hint_y=None,
                height=dp(60)
            )
            self.user_stories_grid.add_widget(no_stories_label)
            return
        
        # Mostrar las 3 más recientes
        for story in user_stories[-3:]:
            story_card = StoryCard(story)
            self.user_stories_grid.add_widget(story_card)
    
    def create_new_story(self, *args):
        """
        Navega a la pantalla de creación de historia.
        """
        app = App.get_running_app()
        app.screen_manager.current = 'story_form'
    
    def show_my_stories(self, *args):
        """
        Muestra todas las historias del usuario.
        """
        # Por ahora, simplemente recarga las historias
        # En una implementación más completa, podría abrir una pantalla dedicada
        self.load_user_stories()
        self.show_dialog("Mostrando tus historias más recientes")
    
    def open_settings(self, *args):
        """
        Abre el diálogo de configuración.
        """
        self.show_dialog("Configuración - Próximamente disponible")
    
    def logout(self, *args):
        """
        Cierra la sesión del usuario y regresa al menú principal.
        """
        SessionManager.clear_session()
        app = App.get_running_app()
        app.screen_manager.current = 'menu'
        self.show_dialog("Sesión cerrada exitosamente")
    
    def show_dialog(self, text):
        """
        Muestra un diálogo con el texto proporcionado.
        """
        if not self.dialog:
            self.dialog = MDDialog(text=text)
        else:
            self.dialog.text = text
        self.dialog.open()
    
    def on_enter(self, *args):
        """
        Se ejecuta al entrar a la pantalla.
        """
        self.load_user_stories()