
from typing import List
from src.db_mgr import SqliteDatabaseMgr
from src.db_models import UserModel
from src.object import User, VacantCourt
from src.agent import BadmintonReserveAgent


class VacantCourtService:
    def __init__(self) -> None:
        pass

    def check(self, user_id: int, court: int, date: str) -> List[VacantCourt]:
        service = UserService()
        user = service.get(user_id=user_id)
        if user is None:
            return None

        agent = BadmintonReserveAgent(user.get_token())
        return agent.check(date=date, courts=tuple([court]))

    def gen_reply_msg(self, courts: List[VacantCourt]) -> str:
        if len(courts) == 0:
            return f"目前沒有空場地椰～"

        reply_msg = ""
        for i in courts:
            reply_msg += f"{i.string()}\n"
        return reply_msg


class UserService:
    def __init__(self) -> None:
        pass

    def get(self, user_id: int) -> User:
        db_mgr = SqliteDatabaseMgr()
        row = db_mgr.query_first(UserModel, user_id=user_id)
        if row is None:
            return None

        user = User(name=row.name, user_id=row.user_id)
        user.set_php_session(row.php_session)
        user.set_xsrf_token(row.xsrf_token)
        user.set_system_session(row.system_session)
        return user

