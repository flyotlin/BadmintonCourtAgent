import traceback
from telegram import Update
from telegram.ext import CallbackContext
from time import time
from typing import List

from src.agent import BadmintonReserveAgent
from src.db_mgr import DatabaseMgr
from src.db_models import SnapCourtJobModel, UserModel
from src.logger import AyeLogger
from src.object import User, VacantCourt


class VacantCourtService:
    def __init__(self, update: Update, context: CallbackContext, engine) -> None:
        self._update = update
        self._context = context
        self._engine = engine
        self._logger = AyeLogger().get()

    def check(self, user_id: int, court: int, date: str) -> List[VacantCourt]:
        """Find VacantCourts on 17Fit"""
        service = UserService(engine=self._engine)
        user = service.get(user_id=user_id)
        if user is None:
            return None

        agent = BadmintonReserveAgent(user.get_token())
        return agent.check(date=date, courts=tuple([court]))

    def gen_reply_msg(self, courts: List[VacantCourt]) -> str:
        if len(courts) == 0:
            return "目前沒有空場地椰～"

        reply_msg = ""
        for i in courts:
            reply_msg += f"{i.string()}\n"
        return reply_msg

    def snap(self, vacant_court: VacantCourt):
        """Create RepeatingJobs to snap VacantCourt"""
        INTERVAL = 5
        username = self._update.message.from_user.username
        user_id = self._update.message.from_user.id
        job_name = f"{username}_{user_id+int(time())}"

        db_mgr = DatabaseMgr(engine=self._engine)
        row = db_mgr.query_first(SnapCourtJobModel,
            user_id=user_id,
            date=vacant_court._date,
            time=vacant_court._time,
            court=vacant_court._court_idx
        )
        if row is not None:
            job_name = row.name
            job_queue = self._context.job_queue
            jobs = job_queue.get_jobs_by_name(name=job_name)
            if len(jobs) != 0:
                return
            self._logger.warning("job in db, but not in job_queue, may due to inproper AyeServer job initialization.")
            return

        db_mgr.insert(SnapCourtJobModel(
            user_id=user_id,
            interval=INTERVAL,
            date=vacant_court._date,
            time=vacant_court._time,
            court=vacant_court._court_idx,
            name=job_name
        ))
        job_queue = self._context.job_queue
        job_queue.run_repeating(
            callback=self.reserve_callback(vacant_court, user_id),
            interval=INTERVAL,
            name=job_name,
            context=self._update.message.chat_id
        )

    def reserve_callback(self, vacant_court: VacantCourt, user_id: int):
        """
        I don't know how to resolve circular-import
        between VacantCourt and BadmintonCourtAgent,
        so I came up with putting callback here...
        """
        def callback(context: CallbackContext):
            service = UserService(engine=self._engine)
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
                    self._logger.info(f"Not reservable: 第{vacant_court._court_idx}場 @ {vacant_court._date} {vacant_court._time}")
            except Exception as e:
                print("Error occured")
                print(e)
                print(traceback.print_exc())
                context.bot.send_message(
                    chat_id=context.job.context,
                    text=f"錯誤發生，可以嘗試重新設定token: [{e}]"
                )
        return callback


class UserService:
    def __init__(self, engine) -> None:
        self._engine = engine

    def get(self, user_id: int) -> User:
        db_mgr = DatabaseMgr(engine=self._engine)
        row = db_mgr.query_first(UserModel, user_id=user_id)
        if row is None:
            return None

        user = User(name=row.name, user_id=row.user_id, engine=self._engine)
        user.set_php_session(row.php_session)
        user.set_xsrf_token(row.xsrf_token)
        user.set_system_session(row.system_session)
        return user
