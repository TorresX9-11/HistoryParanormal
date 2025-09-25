"""
story_form.py
Formulario para crear/editar historias con diseño moderno.
Permite al usuario publicar nuevas historias o editar existentes.
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivy.app import App
from models.story import StoryManager
from models.user import SessionManager

# Categorías actualizadas con temática de terror
CATEGORIES = [
    'Apariciones', 'Casas Embrujadas', 'Cementerios', 'Posesiones', 
    'Rituales', 'Leyendas Urbanas', 'Hospitales/Sanatorios', 'Carreteras', 
    'Bosques/Montañas', 'Entidades Demoníacas'
]

class StoryFormScreen(MDScreen):
    """
    Formulario moderno para crear o editar historias.
    Incluye validación y diseño mejorado.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.menu = None
        self.edit_mode = False
        self.edit_index = None
        self.setup_ui()
    
    def setup_ui(self):
        """
        Configura la interfaz de usuario del formulario.
        """
        # Layout principal
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Toolbar superior
        toolbar = MDTopAppBar(
            title="Nueva Historia",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["check", lambda x: self.publish_story()]],
            md_bg_color=[0.05, 0.05, 0.05, 1]
        )
        main_layout.add_widget(toolbar)
        
        # ScrollView para el formulario
        scroll_view = MDScrollView(padding=dp(16))
        
        # Layout del contenido
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(0)
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Card del formulario
        form_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(500),
            md_bg_color=[0.1, 0.1, 0.1, 1],
            elevation=3,
            radius=[15, 15, 15, 15],
            padding=dp(20),
            spacing=dp(20)
        )
        
        # Título del formulario
        form_title = MDLabel(
            text='RELATA TU EXPERIENCIA PARANORMAL',
            theme_text_color="Custom",
            text_color=[0.8, 0.1, 0.1, 1],
            font_style="H6",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        form_card.add_widget(form_title)
        
        # Campo de título
        self.title_field = MDTextField(
            hint_text="Título de la historia",
            mode="outlined",
            size_hint_y=None,
            height=dp(60),
            max_text_length=100
        )
        form_card.add_widget(self.title_field)
        
        # Campo de categoría con menú desplegable
        category_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(8)
        )
        
        self.category_field = MDTextField(
            hint_text="Selecciona una categoría",
            mode="outlined",
            readonly=True,
            size_hint_x=0.85
        )
        category_layout.add_widget(self.category_field)
        
        category_button = MDIconButton(
            icon="chevron-down",
            theme_icon_color="Custom",
            icon_color=[0.8, 0.1, 0.1, 1],
            on_release=self.open_category_menu
        )
        category_layout.add_widget(category_button)
        
        form_card.add_widget(category_layout)
        
        # Campo de contenido
        self.content_field = MDTextField(
            hint_text="Relata tu experiencia paranormal en detalle...",
            mode="outlined",
            multiline=True,
            size_hint_y=None,
            height=dp(200),
            max_text_length=2000
        )
        form_card.add_widget(self.content_field)
        
        # Contador de caracteres
        self.char_counter = MDLabel(
            text="0/2000 caracteres",
            theme_text_color="Secondary",
            font_style="Caption",
            halign="right",
            size_hint_y=None,
            height=dp(20)
        )
        form_card.add_widget(self.char_counter)
        
        # Bind para actualizar contador
        self.content_field.bind(text=self.update_char_counter)
        
        content_layout.add_widget(form_card)
        
        # Botones de acción
        buttons_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(12)
        )
        
        # Botón cancelar
        cancel_button = MDRaisedButton(
            text="CANCELAR",
            md_bg_color=[0.3, 0.3, 0.3, 1],
            size_hint_x=0.4,
            on_release=self.go_back
        )
        buttons_layout.add_widget(cancel_button)
        
        # Spacer
        buttons_layout.add_widget(MDLabel())
        
        # Botón publicar
        self.publish_button = MDRaisedButton(
            text="PUBLICAR",
            md_bg_color=[0.8, 0.1, 0.1, 1],
            size_hint_x=0.4,
            on_release=self.publish_story
        )
        buttons_layout.add_widget(self.publish_button)
        
        content_layout.add_widget(buttons_layout)
        
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
    
    def open_category_menu(self, *args):
        """
        Abre el menú desplegable para seleccionar la categoría.
        """
        if not self.menu:
            menu_items = []
            for category in CATEGORIES:
                menu_items.append({
                    'text': category,
                    'on_release': lambda x=category: self.set_category(x)
                })
            
            self.menu = MDDropdownMenu(
                caller=self.category_field,
                items=menu_items,
                width_mult=4,
                background_color=[0.1, 0.1, 0.1, 1],
                radius=[10, 10, 10, 10],
            )
        self.menu.open()
    
    def set_category(self, category):
        """
        Asigna la categoría seleccionada al campo correspondiente.
        """
        self.category_field.text = category
        self.menu.dismiss()
    
    def update_char_counter(self, instance, text):
        """
        Actualiza el contador de caracteres.
        """
        char_count = len(text)
        self.char_counter.text = f"{char_count}/2000 caracteres"
        
        # Cambiar color si se acerca al límite
        if char_count > 1800:
            self.char_counter.text_color = [0.8, 0.1, 0.1, 1]  # Rojo
        elif char_count > 1500:
            self.char_counter.text_color = [0.8, 0.6, 0.1, 1]  # Amarillo
        else:
            self.char_counter.text_color = [0.5, 0.5, 0.5, 1]  # Gris
    
    def publish_story(self, *args):
        """
        Publica una nueva historia o edita una existente.
        Incluye validación mejorada.
        """
        title = self.title_field.text.strip()
        content = self.content_field.text.strip()
        category = self.category_field.text.strip()
        author = SessionManager.get_session()
        
        # Validaciones
        if not title:
            self.show_dialog('Por favor, ingresa un título para tu historia.')
            return
        
        if len(title) < 5:
            self.show_dialog('El título debe tener al menos 5 caracteres.')
            return
        
        if not content:
            self.show_dialog('Por favor, relata tu experiencia paranormal.')
            return
        
        if len(content) < 50:
            self.show_dialog('La historia debe tener al menos 50 caracteres.')
            return
        
        if not category:
            self.show_dialog('Por favor, selecciona una categoría.')
            return
        
        if not author:
            self.show_dialog('Error de sesión. Por favor, inicia sesión nuevamente.')
            return
        
        # Publicar o editar historia
        if self.edit_mode and self.edit_index is not None:
            stories = StoryManager.load_stories()
            stories[self.edit_index] = {
                'title': title,
                'content': content,
                'category': category,
                'author': author
            }
            StoryManager.save_stories(stories)
            self.show_dialog('Historia editada exitosamente.')
            self.edit_mode = False
            self.edit_index = None
        else:
            success, msg = StoryManager.add_story(title, content, category, author)
            self.show_dialog(msg)
        
        if success or self.edit_mode:
            self.clear_form()
            # Regresar a la pantalla principal después de un breve delay
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.go_back(), 2)
    
    def clear_form(self):
        """
        Limpia todos los campos del formulario.
        """
        self.title_field.text = ''
        self.content_field.text = ''
        self.category_field.text = ''
        self.char_counter.text = "0/2000 caracteres"
        self.char_counter.text_color = [0.5, 0.5, 0.5, 1]
    
    def go_back(self, *args):
        """
        Regresa a la pantalla anterior.
        """
        app = App.get_running_app()
        app.screen_manager.current = 'main'
    
    def show_dialog(self, text):
        """
        Muestra un diálogo con el texto proporcionado.
        """
        if not self.dialog:
            self.dialog = MDDialog(text=text)
        else:
            self.dialog.text = text
        self.dialog.open()
    
    def load_story_for_edit(self, story_data, index):
        """
        Carga una historia existente para editar.
        """
        self.title_field.text = story_data.get('title', '')
        self.content_field.text = story_data.get('content', '')
        self.category_field.text = story_data.get('category', '')
        self.edit_mode = True
        self.edit_index = index
        self.publish_button.text = "GUARDAR CAMBIOS"
        
        # Actualizar título de la toolbar
        toolbar = self.children[0].children[1]  # Acceder al toolbar
        toolbar.title = "Editar Historia"