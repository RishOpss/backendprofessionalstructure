from core.database import supabase


def get_all():
    response = supabase.table("courses").select("*").execute()
    return response.data