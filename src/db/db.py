import os
import sqlite3


class DB:
    def __init__(self, name: str = "db/job-queue.db") -> None:
        self._name = name

    def initialize(self, sql_file_path: str):
        if os.path.isfile(self._name):
            return
        try:
            self._create_db()
            self._create_tables_in_db_by_file(sql_file_path)
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)

    def _create_db(self) -> None:
        connection = None
        try:
            connection = sqlite3.connect(self._name)
        except sqlite3.Error as e:
            raise e
        finally:
            if connection:
                connection.close()

    def _create_tables_in_db_by_file(self, sql_file_path: str) -> None:
        with sqlite3.connect(self._name) as connection:
            cursor = connection.cursor()
            with open(sql_file_path) as f:
                sql_file_script = f.read()
                cursor.executescript(sql_file_script)
