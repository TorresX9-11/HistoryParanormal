# story.py
# Modelo de datos para historia

# Aquí irá la clase Story y funciones relacionadas

import json
import os

STORIES_FILE = os.path.join(os.path.dirname(__file__), 'stories.json')

class Story:
    def __init__(self, title, content, category, author):
        self.title = title
        self.content = content
        self.category = category
        self.author = author

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'author': self.author
        }

class StoryManager:
    @staticmethod
    def load_stories():
        if not os.path.exists(STORIES_FILE):
            return []
        with open(STORIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_stories(stories):
        with open(STORIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(stories, f, ensure_ascii=False, indent=2)

    @staticmethod
    def add_story(title, content, category, author):
        stories = StoryManager.load_stories()
        new_story = Story(title, content, category, author)
        stories.append(new_story.to_dict())
        StoryManager.save_stories(stories)
        return True, 'Historia publicada exitosamente.'
