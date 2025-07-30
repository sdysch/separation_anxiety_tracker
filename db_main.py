import sqlite3
import pandas as pd
import hashlib

from utils import read_config, get_connection


def create_db(config):

    # connect to SQLite database (or create it)
    conn = get_connection(config['db_name'])
    cursor = conn.cursor()

    # create table for departures
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise_id INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        target_duration_seconds INTEGER NOT NULL,
        actual_duration_seconds INTEGER NOT NULL,
        rating TEXT CHECK(rating IN ('aced_it', 'ok', 'struggled')) NOT NULL,
        notes TEXT
    )
    """)

    # create table for warmups
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warmups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT NOT NULL,
        duration_seconds INTEGER NOT NULL,
        dog_response TEXT,
        notes TEXT,
        departure_id INTEGER,
        FOREIGN KEY (departure_id) REFERENCES departures(id) ON DELETE CASCADE
    )
    """)

    # commit and close
    conn.commit()
    conn.close()


def insert_from_brb_file(filename, config):

    df = pd.read_csv(
        filename,
        parse_dates=['exercise_time'],
        usecols=[
            'id',
            'exercise_time',
            'result',
            'target_duration',
            'actual_duration',
            'notes'
        ]
    )

    df = df.rename(
        columns={
            'id': 'exercise_id',
            'exercise_time': 'timestamp',
            'result': 'rating',
            'target_duration': 'target_duration_seconds',
            'actual_duration': 'actual_duration_seconds',
        }
    )

    conn = get_connection(config['db_name'])
    cursor = conn.cursor()

    df.to_sql('departures', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()


def insert_from_google(config):

    id = config['google_sheets_id']
    path = f'https://docs.google.com/spreadsheets/d/{id}/gviz/tq?tqx=out:csv'
    df = pd.read_csv(
       path,
       parse_dates=['date'],
       index_col=False
    )

    df['notes'] = df['notes'].fillna('')

    # generate an exercise ID by hashing the date. Not a great solution because this assumes that we will only ever be doing 1 exercise per day
    def hash_val(x):
        return hashlib.sha256(str(x).encode()).hexdigest()

    df['exercise_id'] = df['date'].apply(hash_val)

    df['timestamp'] = df['date']
    df['target_duration_seconds'] = df['target_min'] * 60.
    df['actual_duration_seconds'] = df['actual_min'] * 60.

    df = df[[
        'exercise_id',
        'timestamp',
        'rating',
        'target_duration_seconds',
        'actual_duration_seconds',
        'notes'
    ]]

    conn = get_connection(config['db_name'])
    cursor = conn.cursor()

    df.to_sql('departures', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()


def main(args):

    config = read_config('config.yml')

    if args.setup:
        create_db(config)

    if args.read_brb_file is not None:
        insert_from_brb_file(args.read_brb_file, config)

    if args.read_google_sheets:
        insert_from_google(config)


if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('--setup', action='store_true')
    parser.add_argument('--read-brb-file', required=False, default=None)
    parser.add_argument('--read-google-sheets', action='store_true')

    args = parser.parse_args()


    main(args)

