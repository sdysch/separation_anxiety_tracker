#!/bin/sh
python scripts/scrape_brb_app.py
python scripts/format_raw_data.py
python db_main.py --read-brb-file data/formatted_data.csv
