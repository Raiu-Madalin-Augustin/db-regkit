from testcontainers.postgres import PostgresContainer

def test_pg_version():
    with PostgresContainer("postgres:16") as pg:
        assert "PostgreSQL" in pg.get_connection_url()