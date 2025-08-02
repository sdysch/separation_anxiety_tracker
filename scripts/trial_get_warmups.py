import requests
import yaml
import pandas as pd

from utils import read_config


secrets = read_config('secrets.yml')
config = read_config('config.yml')

exercise_id = '403602'
url = config['warmup_url'] + exercise_id
headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": secrets['cookie']
}

response = requests.get(url, headers=headers)

df = pd.DataFrame(response.json()['steps'])
df['exercise_id'] = exercise_id
print(df)

