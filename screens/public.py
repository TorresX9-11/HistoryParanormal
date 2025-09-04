# public.py
# Pantalla pública para ver historias

from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from models.story import StoryManager

class PublicScreen(MDScreen):
    def on_enter(self, *args):
        self.populate_stories()

    def populate_stories(self):
        stories = StoryManager.load_stories()
        stories_list = self.ids.stories_list
        stories_list.clear_widgets()
        for story in stories:
            item = OneLineListItem(text=f"{story['title']} - {story['category']} ({story['author']})")
            stories_list.add_widget(item)
