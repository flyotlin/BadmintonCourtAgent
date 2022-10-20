from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, VARCHAR
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(BigInteger)
    name = Column(VARCHAR)
    php_session = Column(String(50))
    xsrf_token = Column(String(350))
    system_session = Column(String(350))


class SnapCourtJobModel(Base):
    __tablename__ = "snap_court_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"))   # foreign key to table `users`, not telegram user_id
    interval = Column(Integer)
    date = Column(String(10))
    time = Column(String(10))
    court = Column(Integer)
    name = Column(String(50))
