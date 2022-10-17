from telegram import Update
from telegram.ext import CallbackContext
from typing import List

from src.agent import BadmintonReserveAgent
from src.db_mgr import SqliteDatabaseMgr
from src.db_models import UserModel
from src.job import RepeatingJob
from src.job_mgr import JobMgr
from src.object import User, VacantCourt


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

    def snap(self, update: Update, context: CallbackContext, date: str, court: int, time: str):
        job_mgr = JobMgr()
        callback = self.reserve_callback(VacantCourt(court, date, time), update.message.from_user.id)
        job = RepeatingJob(callback, 5, update, context)
        if job_mgr.has(job):
            return
        job_mgr.create(job)

    def reserve_callback(self, vacant_court: VacantCourt, user_id: int):
        """
        I don't know how to resolve circular-import
        between VacantCourt and BadmintonCourtAgent,
        so I came up with putting callback here...
        """
        def callback(context: CallbackContext):
            service = UserService()
            user = service.get(user_id=user_id)
            if user is None:
                raise Exception("token not set")

            try:
                agent = BadmintonReserveAgent(user.get_token())
                ret = agent.go(court=vacant_court._court_idx, date=vacant_court._date, time=vacant_court._time)
                if ret:
                    job = context.job
                    context.bot.send_message(
                        chat_id=job.context,
                        text=f"成功預約: 第{vacant_court._court_idx}場 @ {vacant_court._date} {vacant_court._time}"
                    )
                else:
                    print("Not reservable")
            except Exception:
                print("Error occured")
        return callback


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
