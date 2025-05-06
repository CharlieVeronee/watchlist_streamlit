import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
from sqlalchemy import text

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))

def get_user_password(username: str):
    conn = st.connection("postgresql", type="sql")
    
    row = conn.session.execute(
        text("SELECT app_password FROM Users WHERE app_username = :username"),
        {"username": username}
    ).fetchone()
    return row[0] if row else None
    


