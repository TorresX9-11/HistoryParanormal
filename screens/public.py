"""
public.py
Pantalla pública para ver historias.
Muestra todas las historias disponibles en la app.
"""

from kivymd.uix.screen import MDScreen  # Pantalla base KivyMD
from kivymd.uix.list import OneLineListItem  # Item de lista para mostrar historias
from models.story import StoryManager       # Gestor de historias

class PublicScreen(MDScreen):
    """
    Pantalla pública.
    Al entrar, muestra todas las historias disponibles.
    """
    def on_enter(self, *args):
        # Se llama automáticamente al entrar en la pantalla
        self.populate_stories()

    def populate_stories(self):
        """
        Carga todas las historias y las muestra en la lista visual.
        """
        stories = StoryManager.load_stories()
        stories_list = self.ids.stories_list
        stories_list.clear_widgets()
        for story in stories:
            item = OneLineListItem(text=f"{story['title']} - {story['category']} ({story['author']})")
            stories_list.add_widget(item)
