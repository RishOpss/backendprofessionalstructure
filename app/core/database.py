from functools import lru_cache

from supabase import create_client, Client
from core.config import SUPABASE_URL, SUPABASE_KEY


@lru_cache
def get_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    return create_client(SUPABASE_URL, SUPABASE_KEY)
