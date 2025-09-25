"""
explore.py
Pantalla de exploración con filtros y búsqueda.
Permite buscar historias por categoría, autor o contenido.
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.chip import MDChip
from kivy.metrics import dp
from models.story import StoryManager
from screens.home import StoryCard

class ExploreScreen(MDScreen):
    """
    Pantalla de exploración y búsqueda de historias.
    Incluye filtros por categoría y búsqueda por texto.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_filter = None
        self.setup_ui()
    
    def setup_ui(self):
        """
        Configura la interfaz de usuario de la pantalla de exploración.
        """
        # Layout principal
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(16),
            spacing=dp(16)
        )
        
        # Header con título
        header_label = MDLabel(
            text="Explorar Historias",
            theme_text_color="Primary",
            font_style="H5",
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(header_label)
        
        # Barra de búsqueda
        search_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8)
        )
        
        self.search_field = MDTextField(
            hint_text="Buscar historias...",
            size_hint_x=0.8,
            mode="round"
        )
        search_layout.add_widget(self.search_field)
        
        search_button = MDIconButton(
            icon="magnify",
            theme_icon_color="Custom",
            icon_color=[0.8, 0.1, 0.1, 1],
            on_release=self.search_stories
        )
        search_layout.add_widget(search_button)
        
        main_layout.add_widget(search_layout)
        
        # Filtros por categoría
        filter_label = MDLabel(
            text="Filtrar por categoría:",
            theme_text_color="Secondary",
            font_style="Subtitle2",
            size_hint_y=None,
            height=dp(30)
        )
        main_layout.add_widget(filter_label)
        
        # ScrollView horizontal para chips de categorías
        categories_scroll = MDScrollView(
            size_hint_y=None,
            height=dp(50),
            do_scroll_y=False,
            do_scroll_x=True
        )
        
        self.categories_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_x=None,
            width=dp(0)  # Se ajustará dinámicamente
        )
        
        # Agregar chips de categorías
        categories = [
            'Todas', 'Apariciones', 'Casas Embrujadas', 'Cementerios', 
            'Posesiones', 'Rituales', 'Leyendas Urbanas', 
            'Hospitales/Sanatorios', 'Carreteras', 'Bosques/Montañas', 
            'Entidades Demoníacas'
        ]
        
        for category in categories:
            chip = MDChip(
                text=category,
                check=True if category == 'Todas' else False,
                on_release=lambda x, cat=category: self.filter_by_category(cat)
            )
            self.categories_layout.add_widget(chip)
            self.categories_layout.width += chip.width + dp(8)
        
        categories_scroll.add_widget(self.categories_layout)
        main_layout.add_widget(categories_scroll)
        
        # ScrollView para resultados
        results_scroll = MDScrollView()
        
        self.results_grid = MDGridLayout(
            cols=1,
            spacing=dp(16),
            size_hint_y=None,
            height=dp(0)
        )
        self.results_grid.bind(minimum_height=self.results_grid.setter('height'))
        
        results_scroll.add_widget(self.results_grid)
        main_layout.add_widget(results_scroll)
        
        self.add_widget(main_layout)
        
        # Cargar todas las historias inicialmente
        self.load_all_stories()
    
    def load_all_stories(self):
        """
        Carga todas las historias disponibles.
        """
        stories = StoryManager.load_stories()
        self.display_stories(stories)
    
    def display_stories(self, stories):
        """
        Muestra las historias proporcionadas en el grid de resultados.
        """
        self.results_grid.clear_widgets()
        
        if not stories:
            no_results_label = MDLabel(
                text="No se encontraron historias",
                theme_text_color="Secondary",
                halign="center",
                size_hint_y=None,
                height=dp(100)
            )
            self.results_grid.add_widget(no_results_label)
            return
        
        for story in stories:
            story_card = StoryCard(story)
            self.results_grid.add_widget(story_card)
    
    def search_stories(self, *args):
        """
        Busca historias basándose en el texto ingresado.
        """
        search_text = self.search_field.text.lower().strip()
        
        if not search_text:
            self.load_all_stories()
            return
        
        stories = StoryManager.load_stories()
        filtered_stories = []
        
        for story in stories:
            # Buscar en título, contenido y autor
            if (search_text in story.get('title', '').lower() or
                search_text in story.get('content', '').lower() or
                search_text in story.get('author', '').lower()):
                filtered_stories.append(story)
        
        self.display_stories(filtered_stories)
    
    def filter_by_category(self, category):
        """
        Filtra historias por categoría seleccionada.
        """
        # Actualizar estado de chips
        for chip in self.categories_layout.children:
            if hasattr(chip, 'text'):
                chip.check = (chip.text == category)
        
        self.current_filter = category
        
        stories = StoryManager.load_stories()
        
        if category == 'Todas':
            filtered_stories = stories
        else:
            filtered_stories = [s for s in stories if s.get('category') == category]
        
        self.display_stories(filtered_stories)
    
    def on_enter(self, *args):
        """
        Se ejecuta al entrar a la pantalla.
        """
        if not self.current_filter or self.current_filter == 'Todas':
            self.load_all_stories()