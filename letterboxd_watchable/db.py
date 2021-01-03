import sqlite3

from config import config


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(config.db_location)
    conn.row_factory = sqlite3.Row
    return conn
