import requests
import yaml
import pandas as pd

from utils import read_config


secrets = read_config('secrets.yml')
config = read_config('config.yml')

url = config['url']
headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": secrets['cookie']
}

response = requests.get(url, headers=headers)

# save raw data
pd.DataFrame(response.json()).to_csv(
    config['raw_data'],
    sep='|',
    index=False
)

