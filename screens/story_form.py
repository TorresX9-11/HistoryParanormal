# story_form.py
# Formulario para crear/editar historias

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from models.story import StoryManager
from models.user import SessionManager

CATEGORIES = [
    'Norte', 'Centro', 'Sur', 'Isla de Pascua', 'Patagonia', 'Desconocida'
]


class StoryFormScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.menu = None
        self.edit_mode = False
        self.edit_index = None

    def open_category_menu(self, field):
        if not self.menu:
            self.menu = MDDropdownMenu(
                caller=field,
                items=[{'text': c, 'on_release': lambda x=c: self.set_category(x)} for c in CATEGORIES],
                width_mult=4
            )
        self.menu.open()

    def set_category(self, category):
        self.ids.category.text = category
        self.menu.dismiss()

    def publish_story(self):
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
