import sqlite3
import json

from utils import read_config

config = read_config('config.yml')

# export to json
conn = sqlite3.connect(config['db_name'])
cursor = conn.cursor()
cursor.execute('SELECT * FROM departures')
columns = [desc[0] for desc in cursor.description]
rows = cursor.fetchall()
data = [dict(zip(columns, row)) for row in rows]

with open(config['json_data'], 'w') as f:
    json.dump(data, f, indent=4)
conn.close()

