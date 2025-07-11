import json
import os
import sqlite3
from unit3dup import config_settings

# Torrent attributes
create_table_sql = ('\n'
                    'CREATE TABLE IF NOT EXISTS torrents (\n'
                    '    id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
                    '    name TEXT,\n'
                    '    category TEXT,\n'
                    '    category_id INTEGER,\n'
                    '    created_at TEXT,\n'
                    '    description TEXT,\n'
                    '    details_link TEXT,\n'
                    '    download_link TEXT,\n'
                    '    double_upload BOOLEAN,\n'
                    '    featured BOOLEAN,\n'
                    '    freeleech TEXT,\n'
                    '    igdb_id INTEGER,\n'
                    '    imdb_id TEXT,\n'
                    '    info_hash TEXT,\n'
                    '    internal BOOLEAN,\n'
                    '    leechers INTEGER,\n'
                    '    magnet_link TEXT,\n'
                    '    mal_id INTEGER,\n'
                    '    media_info TEXT,\n'
                    '    release_year INTEGER,\n'
                    '    resolution TEXT,\n'
                    '    resolution_id INTEGER,\n'
                    '    seeders INTEGER,\n'
                    '    size INTEGER,\n'
                    '    times_completed INTEGER,\n'
                    '    tmdb_id INTEGER,\n'
                    '    tvdb_id INTEGER,\n'
                    '    type TEXT,\n'
                    '    type_id INTEGER,\n'
                    '    uploader TEXT,\n'
                    '    personal_release BOOLEAN,\n'
                    '    refundable BOOLEAN,\n'
                    '    num_file INTEGER,\n'
                    '    bd_info TEXT,\n'
                    '    genres TEXT,\n'
                    '    poster TEXT,\n'
                    '    meta TEXT,\n'
                    '    files TEXT\n'
                    ')\n')


class Database:
    """
    Create a new database and populate it with torrents attributes
    Search torrents based on attributes
    """

    def __init__(self, db_file):
        self.filename = db_file
        self.CACHE_PATH = config_settings.user_preferences.CACHE_PATH
        self.database = sqlite3.connect(os.path.join(self.CACHE_PATH,f"{db_file}.db"))
        self.cursor = self.database.cursor()
        self.build()

    def build(self):
        self.cursor.execute("DROP TABLE IF EXISTS torrents")
        self.cursor.execute(create_table_sql)
        self.database.commit()


    def write(self, data: dict):
        for key, value in data.items():
            if isinstance(value, (dict,list)):
                data[key] = json.dumps(value)

        keys = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        sql = f'''INSERT INTO torrents ({keys}) VALUES ({placeholders})'''
        self.cursor.execute(sql, values)
        self.database.commit()