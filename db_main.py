import sqlite3
import pandas as pd

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


def insert_from_file(filename, config):

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


def main(args):

    config = read_config('config.yml')

    if not args.no_setup:
        create_db(config)

    if args.read_file is not None:
        insert_from_file(args.read_file, config)


if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('--no-setup', action='store_true')
    parser.add_argument('--read-file', required=False, default=None)

    args = parser.parse_args()


    main(args)

