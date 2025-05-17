# tests/test_smoke.py
from testcontainers.postgres import PostgresContainer
import psycopg2

def test_pg_connection():
    with PostgresContainer("postgres:16") as pg:
        # pg.get_connection_url() returnează un URL SQLAlchemy,
        # de forma "postgresql+psycopg2://user:pass@host:port/dbname"
        # libpq (și psycopg2) înțelege în schimb URIs de forma "postgresql://…"
        uri = pg.get_connection_url().replace("postgresql+psycopg2://", "postgresql://")
        conn = psycopg2.connect(uri)        # acum e un URI valid libpq
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        assert "PostgreSQL" in version
        conn.close()
