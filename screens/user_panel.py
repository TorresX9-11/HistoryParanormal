"""
user_panel.py
Panel de usuario para crear, editar y eliminar historias.
Permite ver todas las historias, filtrar por las propias y gestionar acciones sobre ellas.
"""

from kivymd.uix.screen import MDScreen  # Pantalla base KivyMD
from kivymd.uix.list import OneLineListItem, OneLineAvatarIconListItem, IconRightWidget  # Widgets de lista y acciones
from kivymd.uix.dialog import MDDialog  # Diálogo para mensajes
from models.story import StoryManager   # Gestor de historias
from models.user import SessionManager # Gestor de sesión
from kivy.app import App               # Acceso a la app principal

class UserPanelScreen(MDScreen):
    """
    Panel de usuario.
    Permite ver todas las historias, filtrar por las propias, y editar/eliminar.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None  # Diálogo reutilizable

    def on_enter(self, *args):
        # Se llama automáticamente al entrar en la pantalla
        self.show_all_stories()

    def show_all_stories(self):
        """
        Muestra todas las historias en la lista visual.
        """
        stories = StoryManager.load_stories()
        stories_list = self.ids.user_stories_list
        stories_list.clear_widgets()
        for story in stories:
            item = OneLineListItem(text=f"{story['title']} - {story['category']} ({story['author']})")
            stories_list.add_widget(item)

    def show_my_stories(self):
        """
        Filtra y muestra solo las historias del usuario actual.
        Agrega botones para editar y eliminar cada historia.
        """
        username = SessionManager.get_session()
        stories = StoryManager.load_stories()
        user_stories = [s for s in stories if s['author'] == username]
        stories_list = self.ids.user_stories_list
        stories_list.clear_widgets()
        for idx, story in enumerate(user_stories):
            item = OneLineAvatarIconListItem(text=f"{story['title']} - {story['category']}")
            item.add_widget(IconRightWidget(icon="pencil", on_release=lambda x, i=idx: self.edit_story(i)))
            item.add_widget(IconRightWidget(icon="delete", on_release=lambda x, i=idx: self.delete_story(i)))
            stories_list.add_widget(item)

    def open_story_form(self):
        """
        Navega al formulario para crear una nueva historia.
        """
        App.get_running_app().root.current = 'storyform'

    def edit_story(self, index):
        """
        Carga los datos de la historia seleccionada en el formulario para editar.
        """
        username = SessionManager.get_session()
        stories = StoryManager.load_stories()
        user_stories = [s for s in stories if s['author'] == username]
        story = user_stories[index]
        app = App.get_running_app()
        storyform = app.root.get_screen('storyform')
        storyform.ids.title.text = story['title']
        storyform.ids.content.text = story['content']
        storyform.ids.category.text = story['category']
        storyform.edit_mode = True
        storyform.edit_index = stories.index(story)
        app.root.current = 'storyform'

    def delete_story(self, index):
        """
        Elimina la historia seleccionada del usuario actual.
        """
        username = SessionManager.get_session()
        stories = StoryManager.load_stories()
        user_stories = [s for s in stories if s['author'] == username]
        story_to_delete = user_stories[index]
        stories.remove(story_to_delete)
        StoryManager.save_stories(stories)
        self.show_dialog('Historia eliminada')
        self.populate_user_stories()

    def show_dialog(self, text):
        if not self.dialog:
            self.dialog = MDDialog(text=text)
        else:
            self.dialog.text = text
        self.dialog.open()
