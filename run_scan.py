from schema_scanner import scan_migration_folder
import yaml

if __name__ == "__main__":
    modified = scan_migration_folder("migrations")
    with open("modified_entities.yaml", "w") as f:
        yaml.dump({k: sorted(v) for k, v in modified.items()}, f, sort_keys=False)
