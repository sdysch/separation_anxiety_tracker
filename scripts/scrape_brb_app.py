import requests
import yaml
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import read_config

# TODO response checking for API requests

def get_departures(secrets, config):
    url = config['url']
    headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": secrets['cookie']
    }

    response = requests.get(url, headers=headers)

    # save raw data
    df = pd.DataFrame(response.json())
    df.to_csv(
        config['raw_data'],
        sep='|',
        index=False
    )

    return df


def get_warmups(secrets, config, exercise_ids):

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": secrets['cookie']
    }

    def fetch(url, headers, id):
        response = requests.get(url + str(id), headers=headers, timeout=10)
        df = pd.DataFrame(
            response.json()['steps']
        )
        df['exercise_id'] = id
        return df

    # Submit all tasks
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch, config['warmup_url'], headers, id): id for id in exercise_ids}

    # collect results
    results = []
    for future in as_completed(futures):
        url = futures[future]
        data = future.result()
        results.append(data)

    # save raw data
    df = pd.concat(results, ignore_index=True)
    df.to_csv(
        config['raw_warmup_data'],
        sep='|',
        index=False
    )


def main():
    secrets = read_config('secrets.yml')
    config = read_config('config.yml')

    df = get_departures(secrets, config)

    exercise_ids = df['id'].unique().tolist()
    get_warmups(secrets, config, exercise_ids)


if __name__ == '__main__':
    main()

