"""
story.py
Modelo de datos para historia y gestión de historias con Supabase.
Incluye clases y funciones para crear, cargar, actualizar y eliminar historias.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_client import get_supabase_client

class Story:
    """
    Representa una historia publicada por un usuario.
    """
    def __init__(self, id, title, content, category, author_id, author_username=None, created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.content = content
        self.category = category
        self.author_id = author_id
        self.author = author_username
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def from_dict(data):
        """
        Crea una historia desde un diccionario de Supabase.
        """
        author_username = None
        if 'users' in data and data['users']:
            author_username = data['users'].get('username')
        elif 'author' in data:
            author_username = data['author']

        return Story(
            id=data.get('id'),
            title=data.get('title'),
            content=data.get('content'),
            category=data.get('category'),
            author_id=data.get('author_id'),
            author_username=author_username,
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self):
        """
        Convierte la historia a un diccionario.
        """
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'author': self.author
        }

class StoryManager:
    """
    Clase estática para gestionar historias con Supabase.
    """
    @staticmethod
    def load_stories():
        """
        Carga todas las historias desde Supabase con información del autor.
        """
        try:
            supabase = get_supabase_client()
            response = supabase.table('stories').select('*, users(username)').order('created_at', desc=True).execute()

            stories = []
            for story_data in response.data:
                story = Story.from_dict(story_data)
                stories.append(story.to_dict())

            return stories

        except Exception as e:
            print(f"Error al cargar historias: {e}")
            return []

    @staticmethod
    def get_story_by_id(story_id):
        """
        Obtiene una historia específica por su ID.
        """
        try:
            supabase = get_supabase_client()
            response = supabase.table('stories').select('*, users(username)').eq('id', story_id).maybeSingle().execute()

            if response.data:
                return Story.from_dict(response.data)
            return None

        except Exception as e:
            print(f"Error al obtener historia: {e}")
            return None

    @staticmethod
    def get_stories_by_author(author_username):
        """
        Obtiene todas las historias de un autor específico.
        """
        try:
            supabase = get_supabase_client()
            response = supabase.table('stories').select('*, users!inner(username)').eq('users.username', author_username).order('created_at', desc=True).execute()

            stories = []
            for story_data in response.data:
                story = Story.from_dict(story_data)
                stories.append(story.to_dict())

            return stories

        except Exception as e:
            print(f"Error al obtener historias del autor: {e}")
            return []

    @staticmethod
    def get_stories_by_category(category):
        """
        Obtiene todas las historias de una categoría específica.
        """
        try:
            supabase = get_supabase_client()
            response = supabase.table('stories').select('*, users(username)').eq('category', category).order('created_at', desc=True).execute()

            stories = []
            for story_data in response.data:
                story = Story.from_dict(story_data)
                stories.append(story.to_dict())

            return stories

        except Exception as e:
            print(f"Error al obtener historias por categoría: {e}")
            return []

    @staticmethod
    def search_stories(query):
        """
        Busca historias por título o contenido.
        """
        try:
            supabase = get_supabase_client()
            response = supabase.table('stories').select('*, users(username)').or_(f'title.ilike.%{query}%,content.ilike.%{query}%').order('created_at', desc=True).execute()

            stories = []
            for story_data in response.data:
                story = Story.from_dict(story_data)
                stories.append(story.to_dict())

            return stories

        except Exception as e:
            print(f"Error al buscar historias: {e}")
            return []

    @staticmethod
    def add_story(title, content, category, author_id):
        """
        Agrega una nueva historia a Supabase.
        """
        try:
            supabase = get_supabase_client()

            new_story = {
                'title': title,
                'content': content,
                'category': category,
                'author_id': author_id
            }

            response = supabase.table('stories').insert(new_story).execute()

            if response.data:
                return True, 'Historia publicada exitosamente.'
            return False, 'Error al publicar historia.'

        except Exception as e:
            print(f"Error al agregar historia: {e}")
            return False, f'Error al publicar historia: {str(e)}'

    @staticmethod
    def update_story(story_id, title, content, category):
        """
        Actualiza una historia existente.
        """
        try:
            supabase = get_supabase_client()

            updated_story = {
                'title': title,
                'content': content,
                'category': category
            }

            response = supabase.table('stories').update(updated_story).eq('id', story_id).execute()

            if response.data:
                return True, 'Historia actualizada exitosamente.'
            return False, 'Error al actualizar historia.'

        except Exception as e:
            print(f"Error al actualizar historia: {e}")
            return False, f'Error al actualizar historia: {str(e)}'

    @staticmethod
    def delete_story(story_id):
        """
        Elimina una historia.
        """
        try:
            supabase = get_supabase_client()
            response = supabase.table('stories').delete().eq('id', story_id).execute()

            if response.data:
                return True, 'Historia eliminada exitosamente.'
            return False, 'Error al eliminar historia.'

        except Exception as e:
            print(f"Error al eliminar historia: {e}")
            return False, f'Error al eliminar historia: {str(e)}'
