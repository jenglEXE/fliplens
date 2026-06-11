from supabase import create_client, Client
from backend.config import SUPABASE_URL, SUPABASE_KEY

_client: Client = None


def get_db() -> Client:
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError('Supabase credentials not configured. Check your .env file.')
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client