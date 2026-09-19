import psycopg2
import psycopg2.extras
from flask import g, current_app

def get_db():
    # Pool conexión
    if "db" not in g:
        g.db = psycopg2.connect(current_app.config["DATABASE_URL"])
        g.db.autocommit = True
    return g.db

def close_db(exc=None):
    # Cerrar conexión
    db = g.pop("db", None)
    if db is not None:
        db.close()

def query(sql, params=(), fetchone=False, fetchall=False):
    # Ejecutar query
    cur = get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(sql, params)
    if fetchone:
        return cur.fetchone()
    if fetchall:
        return cur.fetchall()
    return None
