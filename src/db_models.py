from sqlalchemy import Column, Integer, String, BigInteger, VARCHAR
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
