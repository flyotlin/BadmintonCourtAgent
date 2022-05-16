import os
import unittest

from src.db.db import DB


class TestDB(unittest.TestCase):
    def setUp(self) -> None:
        self.db_name = "db/job-queue.db"
        self.db = DB(self.db_name)

    def test_create_db(self):
        self.db._create_db()

        self.assertTrue(os.path.isfile(self.db_name))

    def tearDown(self) -> None:
        if not os.path.isfile(self.db_name):
            return

        os.remove(self.db_name)
