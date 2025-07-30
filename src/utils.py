import sqlite3
import yaml

def get_connection(name):
    conn = sqlite3.connect(name)

    return conn


def read_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

