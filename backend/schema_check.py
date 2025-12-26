from backend.db import engine

def check_schema():
    with engine.connect() as conn:
        result = conn.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        return [row[0] for row in result]
