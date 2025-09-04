# user_panel.py
# Panel de usuario para crear, editar y eliminar historias

from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem, IconRightWidget
from kivymd.uix.dialog import MDDialog
from models.story import StoryManager
from models.user import SessionManager
from kivy.app import App

class UserPanelScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

    def on_enter(self, *args):
        self.populate_user_stories()

    def populate_user_stories(self):
        username = SessionManager.get_session()
        stories = StoryManager.load_stories()
        user_stories = [s for s in stories if s['author'] == username]
        stories_list = self.ids.user_stories_list
        stories_list.clear_widgets()
        for idx, story in enumerate(user_stories):
            item = OneLineListItem(text=f"{story['title']} - {story['category']}")
            item.add_widget(IconRightWidget(icon="pencil", on_release=lambda x, i=idx: self.edit_story(i)))
            item.add_widget(IconRightWidget(icon="delete", on_release=lambda x, i=idx: self.delete_story(i)))
            stories_list.add_widget(item)

    def open_story_form(self):
        App.get_running_app().root.current = 'storyform'

    def edit_story(self, index):
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
