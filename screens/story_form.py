"""
story_form.py
Formulario para crear/editar historias.
Permite al usuario publicar nuevas historias o editar existentes.
"""

from kivymd.uix.screen import MDScreen  # Pantalla base KivyMD
from kivymd.uix.dialog import MDDialog  # Diálogo para mensajes
from kivymd.uix.menu import MDDropdownMenu  # Menú desplegable para categorías
from models.story import StoryManager   # Gestor de historias
from models.user import SessionManager # Gestor de sesión

CATEGORIES = [
    'Norte', 'Centro', 'Sur', 'Isla de Pascua', 'Patagonia', 'Desconocida'
]

class StoryFormScreen(MDScreen):
    """
    Formulario para crear o editar historias.
    Permite seleccionar categoría, publicar o editar historias.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None  # Diálogo reutilizable
        self.menu = None    # Menú de categorías
        self.edit_mode = False  # Modo edición
        self.edit_index = None  # Índice de historia a editar

    def open_category_menu(self, field):
        """
        Abre el menú desplegable para seleccionar la categoría.
        """
        if not self.menu:
            self.menu = MDDropdownMenu(
                caller=field,
                items=[{'text': c, 'on_release': lambda x=c: self.set_category(x)} for c in CATEGORIES],
                width_mult=4
            )
        self.menu.open()

    def set_category(self, category):
        """
        Asigna la categoría seleccionada al campo correspondiente.
        """
        self.ids.category.text = category
        self.menu.dismiss()

    def publish_story(self):
        """
        Publica una nueva historia o edita una existente según el modo.
        Valida los campos y muestra el resultado en un diálogo.
        """
        title = self.ids.title.text
        content = self.ids.content.text
        category = self.ids.category.text
        author = SessionManager.get_session()
        if not (title and content and category and author):
            self.show_dialog('Completa todos los campos.')
            return
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
        self.clear_form()

    def clear_form(self):
        self.ids.title.text = ''
        self.ids.content.text = ''
        self.ids.category.text = ''

    def show_dialog(self, text):
        if not self.dialog:
            self.dialog = MDDialog(text=text)
        else:
            self.dialog.text = text
        self.dialog.open()
