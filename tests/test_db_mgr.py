from genericpath import isfile
import os
import unittest
from sqlalchemy import create_engine

from src.db_mgr import DatabaseMgr
from src.db_models import UserModel


# Not intended for testing, just for demonstrating how to use
class TestDatabaseMgr(unittest.TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        pwd = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(pwd, "../test.sql")

        if os.path.isfile(path):
            os.remove(path)

    def setUp(self) -> None:
        pwd = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(pwd, "../test.sql")

        engine = create_engine(f"sqlite:///{path}")
        self.db_mgr = DatabaseMgr(engine)

    def test_insert(self):
        user = UserModel(user_id="102", name="flyotlin", php_session="fff", xsrf_token="abc", system_session="fee")
        self.db_mgr.insert(user)

    def test_query_user(self):
        result = self.db_mgr.query_first(UserModel)
        print(result.id)
        print(result.user_id)
        print(result.name)

    def test_update_user(self):
        self.db_mgr.update(UserModel, values={
            "name": "Nick"
        })
