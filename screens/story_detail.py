"""
story_detail.py
Pantalla de detalle de historia.
Muestra el contenido completo de una historia con opciones de interacción.
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.app import App

class StoryDetailScreen(MDScreen):
    """
    Pantalla de detalle de historia.
    Muestra el contenido completo con opciones de interacción.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_story = None
        self.setup_ui()
    
    def setup_ui(self):
        """
        Configura la interfaz de usuario de la pantalla de detalle.
        """
        # Layout principal
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Toolbar superior
        toolbar = MDTopAppBar(
            title="Detalle de Historia",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[
                ["heart-outline", lambda x: self.toggle_favorite()],
                ["share-variant", lambda x: self.share_story()]
            ],
            md_bg_color=[0.05, 0.05, 0.05, 1]
        )
        main_layout.add_widget(toolbar)
        
        # ScrollView para el contenido
        scroll_view = MDScrollView(padding=dp(16))
        
        # Layout del contenido
        self.content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            size_hint_y=None,
            height=dp(0)
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        scroll_view.add_widget(self.content_layout)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
    
    def load_story(self, story_data):
        """
        Carga los datos de la historia en la pantalla.
        """
        self.current_story = story_data
        self.content_layout.clear_widgets()
        
        # Card principal de la historia
        story_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(0),  # Se ajustará automáticamente
            md_bg_color=[0.1, 0.1, 0.1, 1],
            elevation=3,
            radius=[15, 15, 15, 15],
            padding=dp(20),
            spacing=dp(16)
        )
        
        # Header con categoría y autor
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(12)
        )
        
        # Etiqueta de categoría
        category_label = MDLabel(
            text=story_data.get('category', 'Sin categoría'),
            theme_text_color="Custom",
            text_color=[0.8, 0.1, 0.1, 1],
            font_style="Caption",
            size_hint_x=None,
            width=dp(120)
        )
        header_layout.add_widget(category_label)
        
        # Spacer
        header_layout.add_widget(MDLabel())
        
        # Autor
        author_label = MDLabel(
            text=f"Por: {story_data.get('author', 'Anónimo')}",
            theme_text_color="Secondary",
            font_style="Caption",
            halign="right"
        )
        header_layout.add_widget(author_label)
        
        story_card.add_widget(header_layout)
        
        # Título de la historia
        title_label = MDLabel(
            text=story_data.get('title', 'Sin título'),
            theme_text_color="Primary",
            font_style="H5",
            size_hint_y=None,
            height=dp(60),
            text_size=(None, None)
        )
        story_card.add_widget(title_label)
        
        # Contenido completo de la historia
        content_label = MDLabel(
            text=story_data.get('content', 'Sin contenido'),
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_y=None,
            text_size=(dp(320), None),  # Ancho fijo para wrap
            height=dp(0)  # Se calculará automáticamente
        )
        
        # Calcular altura basada en el contenido
        content_label.bind(texture_size=content_label.setter('size'))
        story_card.add_widget(content_label)
        
        # Ajustar altura de la card
        story_card.height = dp(150) + content_label.texture_size[1]
        
        self.content_layout.add_widget(story_card)
        
        # Card de acciones
        actions_card = MDCard(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            md_bg_color=[0.08, 0.08, 0.08, 1],
            elevation=2,
            radius=[10, 10, 10, 10],
            padding=dp(16),
            spacing=dp(16)
        )
        
        # Botón de me gusta
        like_button = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color=[0.8, 0.1, 0.1, 1],
            size_hint=(None, None),
            size=(dp(48), dp(48)),
            on_release=self.toggle_like
        )
        actions_card.add_widget(like_button)
        
        # Botón de comentarios (placeholder)
        comment_button = MDIconButton(
            icon="comment-outline",
            theme_icon_color="Custom",
            icon_color=[0.5, 0.5, 0.5, 1],
            size_hint=(None, None),
            size=(dp(48), dp(48)),
            on_release=self.open_comments
        )
        actions_card.add_widget(comment_button)
        
        # Spacer
        actions_card.add_widget(MDLabel())
        
        # Botón de compartir
        share_button = MDIconButton(
            icon="share-variant",
            theme_icon_color="Custom",
            icon_color=[0.5, 0.5, 0.5, 1],
            size_hint=(None, None),
            size=(dp(48), dp(48)),
            on_release=self.share_story
        )
        actions_card.add_widget(share_button)
        
        self.content_layout.add_widget(actions_card)
        
        # Botón para volver (alternativo)
        back_button = MDRaisedButton(
            text="VOLVER",
            md_bg_color=[0.3, 0.3, 0.3, 1],
            size_hint_y=None,
            height=dp(45),
            on_release=self.go_back
        )
        self.content_layout.add_widget(back_button)
    
    def go_back(self, *args):
        """
        Regresa a la pantalla anterior.
        """
        app = App.get_running_app()
        app.screen_manager.current = 'main'
    
    def toggle_favorite(self, *args):
        """
        Alterna el estado de favorito (placeholder).
        """
        # Implementar lógica de favoritos
        pass
    
    def toggle_like(self, *args):
        """
        Alterna el me gusta de la historia (placeholder).
        """
        # Implementar lógica de likes
        pass
    
    def open_comments(self, *args):
        """
        Abre la sección de comentarios (placeholder).
        """
        # Implementar sistema de comentarios
        pass
    
    def share_story(self, *args):
        """
        Comparte la historia (placeholder).
        """
        # Implementar funcionalidad de compartir
        pass