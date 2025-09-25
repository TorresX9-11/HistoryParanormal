"""
home.py
Pantalla principal de inicio con historias destacadas.
Muestra las historias más recientes y populares en formato de cards.
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivy.metrics import dp
from kivy.app import App
from models.story import StoryManager
from models.user import SessionManager

class StoryCard(MDCard):
    """
    Card personalizada para mostrar historias.
    Incluye título, categoría, autor y preview del contenido.
    """
    def __init__(self, story_data, **kwargs):
        super().__init__(**kwargs)
        self.story_data = story_data
        self.setup_card()
    
    def setup_card(self):
        """
        Configura el diseño y contenido de la card.
        """
        # Configuración de la card
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(200)
        self.md_bg_color = [0.1, 0.1, 0.1, 1]  # Fondo oscuro
        self.elevation = 3
        self.radius = [15, 15, 15, 15]
        self.padding = dp(16)
        self.spacing = dp(8)
        self.ripple_behavior = True
        
        # Bind del evento de toque
        self.bind(on_release=self.open_story_detail)
        
        # Header con categoría
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(8)
        )
        
        # Etiqueta de categoría
        category_label = MDLabel(
            text=self.story_data.get('category', 'Sin categoría'),
            theme_text_color="Custom",
            text_color=[0.8, 0.1, 0.1, 1],  # Rojo
            font_style="Caption",
            size_hint_x=None,
            width=self.texture_size[0] if hasattr(self, 'texture_size') else dp(100)
        )
        header_layout.add_widget(category_label)
        
        # Spacer
        header_layout.add_widget(MDLabel())
        
        # Botón de favoritos (placeholder)
        fav_button = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color=[0.5, 0.5, 0.5, 1],
            size_hint=(None, None),
            size=(dp(30), dp(30))
        )
        header_layout.add_widget(fav_button)
        
        self.add_widget(header_layout)
        
        # Título de la historia
        title_label = MDLabel(
            text=self.story_data.get('title', 'Sin título'),
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(40),
            text_size=(None, None)
        )
        self.add_widget(title_label)
        
        # Preview del contenido
        content_preview = self.story_data.get('content', '')[:100] + "..." if len(self.story_data.get('content', '')) > 100 else self.story_data.get('content', '')
        
        content_label = MDLabel(
            text=content_preview,
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_y=None,
            height=dp(60),
            text_size=(dp(300), None)
        )
        self.add_widget(content_label)
        
        # Footer con autor
        footer_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30)
        )
        
        author_label = MDLabel(
            text=f"Por: {self.story_data.get('author', 'Anónimo')}",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_x=0.7
        )
        footer_layout.add_widget(author_label)
        
        # Botón de compartir (placeholder)
        share_button = MDIconButton(
            icon="share-variant",
            theme_icon_color="Custom",
            icon_color=[0.5, 0.5, 0.5, 1],
            size_hint=(None, None),
            size=(dp(30), dp(30))
        )
        footer_layout.add_widget(share_button)
        
        self.add_widget(footer_layout)
    
    def open_story_detail(self, *args):
        """
        Abre la pantalla de detalle de la historia.
        """
        app = App.get_running_app()
        detail_screen = app.screen_manager.get_screen('story_detail')
        detail_screen.load_story(self.story_data)
        app.screen_manager.current = 'story_detail'

class HomeScreen(MDScreen):
    """
    Pantalla principal de inicio.
    Muestra historias destacadas y recientes en formato de cards.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        """
        Configura la interfaz de usuario de la pantalla de inicio.
        """
        # Layout principal
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(16),
            spacing=dp(16)
        )
        
        # Header con saludo
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(16)
        )
        
        # Saludo personalizado
        username = SessionManager.get_session()
        greeting_text = f"Hola, {username}" if username else "Bienvenido"
        
        greeting_label = MDLabel(
            text=greeting_text,
            theme_text_color="Primary",
            font_style="H5",
            size_hint_x=0.7
        )
        header_layout.add_widget(greeting_label)
        
        # Botón de notificaciones (placeholder)
        notif_button = MDIconButton(
            icon="bell-outline",
            theme_icon_color="Custom",
            icon_color=[0.8, 0.1, 0.1, 1],
            size_hint=(None, None),
            size=(dp(40), dp(40))
        )
        header_layout.add_widget(notif_button)
        
        main_layout.add_widget(header_layout)
        
        # Título de sección
        section_title = MDLabel(
            text="Historias Recientes",
            theme_text_color="Primary",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(section_title)
        
        # ScrollView para las historias
        scroll_view = MDScrollView()
        
        # Grid layout para las cards
        self.stories_grid = MDGridLayout(
            cols=1,
            spacing=dp(16),
            size_hint_y=None,
            height=dp(0)  # Se ajustará dinámicamente
        )
        self.stories_grid.bind(minimum_height=self.stories_grid.setter('height'))
        
        scroll_view.add_widget(self.stories_grid)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
        
        # Cargar historias
        self.load_stories()
    
    def load_stories(self):
        """
        Carga las historias desde el modelo y las muestra en cards.
        """
        stories = StoryManager.load_stories()
        
        # Limpiar grid existente
        self.stories_grid.clear_widgets()
        
        # Agregar cards para cada historia
        for story in reversed(stories[-10:]):  # Mostrar las 10 más recientes
            story_card = StoryCard(story)
            self.stories_grid.add_widget(story_card)
    
    def on_enter(self, *args):
        """
        Se ejecuta al entrar a la pantalla.
        Recarga las historias para mostrar contenido actualizado.
        """
        self.load_stories()