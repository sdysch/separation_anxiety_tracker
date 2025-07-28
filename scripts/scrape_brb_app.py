import requests
import yaml
import pandas as pd

def read_secrets(file_path):
    with open(file_path, 'r') as file:
        secrets = yaml.safe_load(file)
    return secrets

secrets = read_secrets('secrets.yml')

url = "https://berightbackapp.io/owner/v3/exercises?type=DepartureExercise"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": secrets['cookie']
}

response = requests.get(url, headers=headers)

# save raw data
pd.DataFrame(response.json()).to_csv(
    'data/raw_brb_data.csv',
    sep='|',
    index=False
)

