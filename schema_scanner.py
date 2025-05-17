# schema_scanner.py

import re
import os
from collections import defaultdict

DDL_PATTERNS = {
    "table": re.compile(r"\bCREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+(\w+)|\bCREATE\s+TABLE\s+(\w+)", re.IGNORECASE),
    "alter": re.compile(r"\bALTER\s+TABLE\s+(\w+)", re.IGNORECASE),
    "add_column": re.compile(r"\bADD\s+COLUMN\s+(\w+)", re.IGNORECASE),
    "proc": re.compile(r"\bCREATE\s+(OR\s+REPLACE\s+)?FUNCTION\s+(\w+)", re.IGNORECASE),
}

def parse_sql_file(path):
    entities = defaultdict(set)
    with open(path, "r") as f:
        content = f.read()

        for match in DDL_PATTERNS["table"].findall(content):
            table = match[0] or match[1]
            if table:
                entities["tables"].add(table)

        for match in DDL_PATTERNS["alter"].findall(content):
            entities["tables"].add(match)

        for match in DDL_PATTERNS["proc"].findall(content):
            entities["procs"].add(match[1])

        for table in entities["tables"]:
            for col in DDL_PATTERNS["add_column"].findall(content):
                entities["columns"].add(f"{table}.{col}")

    return entities

def scan_migration_folder(migrations_path="migrations"):
    all_entities = defaultdict(set)
    for file in os.listdir(migrations_path):
        if file.endswith(".sql"):
            full_path = os.path.join(migrations_path, file)
            file_entities = parse_sql_file(full_path)
            for key, vals in file_entities.items():
                all_entities[key].update(vals)
    return all_entities

import subprocess

def extract_sql_from_git(commit_hash, output_dir):
    subprocess.run(["git", "checkout", commit_hash], check=True)
    subprocess.run(["cp", "-r", "migrations", output_dir], check=True)
