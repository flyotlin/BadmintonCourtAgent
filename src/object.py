from src.db_mgr import SqliteDatabaseMgr
from src.db_models import UserModel


class User:
    def __init__(self, name, user_id) -> None:
        # TODO: type, value check
        self._name = name
        self._user_id = user_id

        self._php_session = ""
        self._xsrf_token = ""
        self._system_session = ""

    def get_token(self):
        return {
            "PHPSESSID": self._php_session,
            "XSRF-TOKEN": self._xsrf_token,
            "17fit_system_session": self._system_session
        }

    def set_php_session(self, val):
        self._php_session = val

    def set_xsrf_token(self, val):
        self._xsrf_token = val

    def set_system_session(self, val):
        self._system_session = val

    def save(self):
        """Save to Database"""
        db_mgr = SqliteDatabaseMgr()
        row = db_mgr.query_first(UserModel, user_id=self._user_id)

        if row is None:
            db_mgr.insert(UserModel(
                user_id=self._user_id,
                name=self._name,
                php_session=self._php_session,
                xsrf_token=self._xsrf_token,
                system_session=self._system_session
            ))
        else:
            db_mgr.update(
                UserModel,
                filters={"user_id": self._user_id},
                values={
                    "user_id": self._user_id,
                    "name": self._name,
                    "php_session": self._php_session,
                    "xsrf_token": self._xsrf_token,
                    "system_session": self._system_session
                }
            )


class VacantCourt:
    def __init__(self, court_idx: int, date: str, time: str) -> None:
        self._court_idx = court_idx
        self._date = date
        self._time = time

    def string(self) -> str:
        return f"第 {self._court_idx} 場: {self._date} {self._time}"

    def reserve(self, user_id: int):
        """
        I don't know how to resolve circular-import
        between VacantCourt and BadmintonCourtAgent,
        so I came up with putting callback here...
        """
        pass
