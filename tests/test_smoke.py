import psycopg2

def test_pg_connection(pg_container):
    uri = pg_container.get_connection_url().replace(
        "postgresql+psycopg2://", "postgresql://"
    )
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    assert "PostgreSQL" in version
    conn.close()
