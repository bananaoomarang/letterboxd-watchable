'''
ADAPTED FROM: https://raw.githubusercontent.com/sjmignot/sceance/master/sceance/update_watchlist.py (thanks)

update your watchlist by signing into your letterboxd account and exporting your content from the site to a local watchlist.txt file.
'''

#IMPORTS

import csv
import re
import os
import sqlite3

import colored
from colored import stylize
import requests
import zipfile

from letterboxd_watchable import db

from config import config

# CONTSTANTS

# letterboxd urls

SIGN_IN_PAGE = "https://letterboxd.com/user/login.do"
EXPORT_PAGE = "https://letterboxd.com/data/export"
REFERER = "https://letterboxd.com/activity/"

# other constants

SIGN_IN_ID_EL = "username"
SIGN_IN_PW_EL = "password"
COOKIE_NAME = "com.xk72.webparts.csrf"
ZIP_FILE = "data/lb_data.zip"
WATCHLIST_CSV = "watchlist.csv"
DATA = "data/"
WATCHLIST_TXT = "data/watchlist.txt"

MY_PATH = os.path.abspath(os.path.dirname(__file__))


def _get_id(row: dict) -> str:
    "Get ID from letterboxd CSV"

    uri: str = row["Letterboxd URI"]
    return uri.split("/")[-1]


def _resolve_tmdb(uri: str):
    res = requests.get(uri)
    tmdb_id = re.search(r'data-tmdb-id="\d+"', res.text)

    if not tmdb_id:
        print(
            stylize(
                f"Could not find TMBD for page {uri}",
                colored.fg("red") + colored.attr("bold")
            )
        )
        return None

    tmdb_id = tmdb_id.group(0).split("=")[-1]
    return "".join(tmdb_id.split('"'))


def _upsert_row(conn: sqlite3.Connection, row: dict):
    with conn:
        conn.execute(
            """
            INSERT INTO cinemas(
                id,
                tmdb_id,
                name,
                year,
                add_date
            )
            VALUES(?, ?, ?, ?, ?)
            ON CONFLICT DO NOTHING
            """,
            (_get_id(row), _resolve_tmdb(row["Letterboxd URI"]), row["Name"], row["Year"], row["Date"])
        )


def process_watchlist():
    watchlist_csv = os.path.join(MY_PATH, f"{DATA}{WATCHLIST_CSV}")
    with open(watchlist_csv, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)


    conn = db.get_conn()

    with conn:
        conn.execute(
            """
CREATE TABLE IF NOT EXISTS cinemas(
    id TEXT PRIMARY KEY,
    tmdb_id INT,
    name TEXT,
    year INT,
    add_date TEXT
)
            """
        )

    for row in rows:
        print(f"processing {row['Name']} ({row['Year']})")
        _upsert_row(conn, row)

    conn.close()


def extract_watchlist():
    zip_file = os.path.join(MY_PATH, ZIP_FILE)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extract(WATCHLIST_CSV, path=os.path.join(MY_PATH, DATA))
    os.remove(zip_file)


def download_letterboxd_content():
    '''signs you into letterboxd and then downloads the content'''

    login_payload = {
        SIGN_IN_ID_EL: config.username,
        SIGN_IN_PW_EL: config.password
    }

    with requests.Session() as session:
        session.get(SIGN_IN_PAGE)
        if COOKIE_NAME in session.cookies:
            login_payload['__csrf'] = session.cookies[COOKIE_NAME]

        # sign in
        session.post(SIGN_IN_PAGE, data=login_payload, headers={'referer': REFERER})
        letterboxd_content = session.get(EXPORT_PAGE)

        with open(ZIP_FILE, 'wb') as f:
            f.write(letterboxd_content.content)


def update_watchlist():
    '''updates your watchlist by downloading letterboxd content and then extracting it'''

    os.makedirs(DATA, exist_ok=True)
    download_letterboxd_content()
    extract_watchlist()
    process_watchlist()

if __name__ == "__main__":
    update_watchlist()
