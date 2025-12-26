from sqlalchemy import create_engine

# Use the password that worked in your original app.py
DB_URL = "postgresql+psycopg://postgres:23085522wqd@localhost:5432/callcenter_db"

engine = create_engine(DB_URL)