from core.database import supabase
from supabase import Client

def get_db() -> Client:
    return supabase