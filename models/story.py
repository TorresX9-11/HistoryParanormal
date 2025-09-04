"""
story.py
Modelo de datos para historia y gestión de historias.
Incluye clases y funciones para crear, guardar y cargar historias.
"""

import json  # Para manejo de archivos JSON
import os    # Para rutas de archivos

STORIES_FILE = os.path.join(os.path.dirname(__file__), 'stories.json')  # Ruta al archivo de historias

class Story:
    """
    Representa una historia publicada por un usuario.
    """
    def __init__(self, title, content, category, author):
        self.title = title
        self.content = content
        self.category = category
        self.author = author

    def to_dict(self):
        """
        Convierte la historia a un diccionario para guardar en JSON.
        """
        return {
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'author': self.author
        }

class StoryManager:
    """
    Clase estática para gestionar historias: cargar, guardar y agregar.
    """
    @staticmethod
    def load_stories():
        """
        Carga la lista de historias desde el archivo JSON.
        """
        if not os.path.exists(STORIES_FILE):
            return []
        with open(STORIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_stories(stories):
        """
        Guarda la lista de historias en el archivo JSON.
        """
        with open(STORIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(stories, f, ensure_ascii=False, indent=2)

    @staticmethod
    def add_story(title, content, category, author):
        """
        Agrega una nueva historia y la guarda en el archivo JSON.
        """
        stories = StoryManager.load_stories()
        new_story = Story(title, content, category, author)
        stories.append(new_story.to_dict())
        StoryManager.save_stories(stories)
        return True, 'Historia publicada exitosamente.'
