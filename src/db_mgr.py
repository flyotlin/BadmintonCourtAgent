import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from src.db_models import Base


class DatabaseMgr:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self.session_maker = sessionmaker(bind=self.engine)
        self._initialize()

    def _initialize(self) -> None:
        Base.metadata.create_all(self.engine)

    def insert(self, record):
        session = self.session_maker()
        session.add(record)
        session.commit()

    def query_first(self, model, **kwargs):
        return self.query_all(model, **kwargs).first()

    def query_all(self, model, **kwargs):
        """kwargs: filter arguments"""
        session = self.session_maker()
        rows = session.query(model).filter_by(**kwargs)
        session.commit()
        return rows

    def update(self, model, filters: dict = {}, values: dict = {}):
        session = self.session_maker()

        row = session.query(model).filter_by(**filters).first()
        if row is None:
            session.commit()
            return

        for k, v in values.items():
            if k in row.__class__.__dict__.keys():
                setattr(row, k, v)
        session.commit()

    def delete(self, model, **kwargs):
        session = self.session_maker()
        row = session.query(model).filter_by(**kwargs).first()
        session.delete(row)
        session.commit()


class SqliteEngine:
    @staticmethod
    def get(path=None) -> Engine:
        if path is None:
            pwd = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(pwd, "../badminton-court-agent.sql")

        return create_engine(f"sqlite:///{path}")
