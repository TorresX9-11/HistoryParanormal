"""
supabase_client.py
Cliente singleton de Supabase para la aplicación.
Configura la conexión a la base de datos.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno
load_dotenv()

class SupabaseClient:
    """
    Cliente singleton de Supabase.
    Gestiona la conexión única a la base de datos.
    """
    _instance = None
    _client: Client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Inicializa el cliente de Supabase con las credenciales del .env
        """
        supabase_url = os.getenv('VITE_SUPABASE_URL')
        supabase_key = os.getenv('VITE_SUPABASE_SUPABASE_ANON_KEY')

        if not supabase_url or not supabase_key:
            raise ValueError("Credenciales de Supabase no encontradas en .env")

        self._client = create_client(supabase_url, supabase_key)

    @property
    def client(self) -> Client:
        """
        Retorna el cliente de Supabase.
        """
        return self._client

def get_supabase_client() -> Client:
    """
    Función helper para obtener el cliente de Supabase.
    """
    return SupabaseClient().client
