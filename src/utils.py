import sqlite3
import yaml
from typing import Any, cast


def get_connection(name: str) -> sqlite3.Connection:
    conn = sqlite3.connect(name)

    return conn


def read_config(file_path: str) -> dict[str, Any]:
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return cast(dict[str, Any], config)
