from core.database import supabase
from supabase import Client

async def get_db() -> Client:
    return supabase