import pytest
from testcontainers.postgres import PostgresContainer
import yaml
import os
import glob

@pytest.fixture(scope="session")
def test_metadata():
    return load_test_metadata()
def test_metadata_access(test_metadata):
    assert "test_pg_connection" in test_metadata

def load_test_metadata(path="test_metadata.yaml"):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="function")
def pg_container():
    """
    Porneste un container PostgreSQL pe durata testului si-l inchide dupa.
    """
    with PostgresContainer("postgres:16") as container:
        yield container

def test_all_tests_have_metadata(test_metadata):
    test_files = glob.glob("tests/test_*.py")
    defined_tests = set(test_metadata.keys())

    for tf in test_files:
        with open(tf, "r") as f:
            for line in f:
                if line.strip().startswith("def test_"):
                    name = line.strip().split("def ")[1].split("(")[0]
                    assert name in defined_tests, f"Missing metadata for {name}"