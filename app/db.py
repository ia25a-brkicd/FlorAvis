import psycopg2
from flask import current_app, g

def get_db():
    if 'db' not in g:
        # holt url aus der Config (die sie aus .env hat
        g.db = psycopg2.connect(current_app.config['DB_URL'])
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Erstellt die Tabelle users"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        );
    """)
    conn.commit()
    cur.close()