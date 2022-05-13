import datetime
import sqlite3
import time
import traceback

from telegram import Update
from telegram.ext import CallbackContext, Job
from typing import List, Tuple

from src.util import (
    agent_internal_error,
    agent_success
)


class JobWorker:
    db_file = 'job-queue.db'

    def __init__(self, worker_type: int, update: Update, context: CallbackContext) -> None:
        """_summary_

        Args:
            worker_type (int): remind(0), poll(1), reserve(2)
            update (Update): _description_
            context (CallbackContext): _description_
        """
        self._handler_update = update
        self._handler_context = context

        self._worker_type = worker_type.value
        self._chat_room_id = self._handler_update.message.chat_id

        self._days: Tuple[int] = None
        self._times: Tuple[datetime.time] = None
        self._callback: callable = None
        self._callback_name: str = None

        self._db_last_row_id: int = None

    def create(self, days: Tuple[int], times: Tuple[datetime.time], callback: callable) -> None:
        self._days = days
        self._times = times
        self._callback = callback
        self._callback_name = callback.__name__

        for _time in self._times:
            job_name = f"{self._worker_type}-{self._chat_room_id}-{int(time.time())}"

            if not self._insert_job_to_db(_time, job_name):
                agent_internal_error(self._handler_update, f"建立 job: {job_name} 失敗 (無法寫入資料庫)")
                return

            if not self._set_job_queue(_time, job_name):
                self._delete_job_from_db_by_id()
                agent_internal_error(self._handler_update, f"建立 job: {job_name} 失敗 (無法寫入 job_queue)")
                return

        agent_success(self._handler_update, "成功建立 jobs!")
        return

    def check(self) -> None:
        jobs = self._select_all_jobs_from_db()

        reply_msg = 'id\t小時\t分鐘\n'
        ID_IDX, HOUR_IDX, MINUTE_IDX = 0, 1, 2
        for i in jobs:
            reply_msg += f'{i[ID_IDX]},\t{i[HOUR_IDX]},\t{i[MINUTE_IDX]}\n'

        agent_success(self._handler_update, reply_msg)
        return

    def delete(self, job_db_id: int) -> None:
        JOB_NAME_IDX = 1
        print(job_db_id, type(job_db_id))
        row = self._select_job_from_db_by_id(job_db_id)
        job_name = row[JOB_NAME_IDX]

        if not self._delete_job_from_db_by_id(job_db_id):
            agent_internal_error()
            return

        if not self._delete_job_from_job_queue(job_name):
            agent_internal_error(self._handler_update, f"刪除 job: {job_name} 失敗 (無法於 job_queue 移除)")
            return

        agent_success(self._handler_update, f"成功刪除 job {job_db_id}!")
        return

    def load(self) -> None:
        pass

    def _set_job_queue(self, _time: datetime.time, job_name: str) -> bool:
        TAIPEI_GMT_TIME_DELTA = -8
        try:
            self._handler_context.job_queue.run_daily(
                time=datetime.time(hour=_time.hour + TAIPEI_GMT_TIME_DELTA, minute=_time.minute),
                days=self._days,
                callback=self._callback,
                name=job_name,
                context=self._chat_room_id
            )
            return True
        except Exception:
            traceback.print_exc()
            return False

    def _get_jobs(self) -> Tuple[Job]:
        raw_jobs = self._handler_context.job_queue.jobs()
        return raw_jobs

    def _get_jobs_by_name(self, job_name: str) -> Tuple[Job]:
        jobs = self._handler_context.job_queue.get_jobs_by_name(job_name)
        return jobs

    def _delete_job_from_job_queue(self, job_name: str) -> bool:
        try:
            jobs = self._get_jobs_by_name(job_name)
            for i in jobs:
                i.job.remove()
        except Exception:
            traceback.print_exc()
            return False
        return True

    def _insert_job_to_db(self, _time: datetime.time, job_name: str) -> bool:
        with sqlite3.connect(self.db_file) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Job (name,hour,minute,callback,chat_id,worker_type) VALUES (?,?,?,?,?,?)", (job_name, _time.hour, _time.minute, self._callback_name, self._chat_room_id, self._worker_type))
            self._db_last_row_id = cursor.lastrowid
            days_with_job_id = [(cursor.lastrowid, i) for i in self._days]
            cursor.executemany("INSERT INTO JobDay (job_id,day) VALUES (?,?)", days_with_job_id)
        return True

    def _delete_job_from_db_by_id(self, job_id: id = None) -> bool:
        if not job_id:
            job_id = self._db_last_row_id
        with sqlite3.connect(self.db_file) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Job WHERE id=?", (str(job_id),))
        return True

    def _select_all_jobs_from_db(self) -> List[tuple]:
        """Select all rows (jobs) from table Job.

        Returns:
            List[tuple]: all rows of this `worker_type`.
        """
        with sqlite3.connect(self.db_file) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id,hour,minute FROM Job WHERE worker_type=?", (str(self._worker_type),))
            rows = cursor.fetchall()
            return rows

    def _select_job_from_db_by_id(self, _id: int) -> tuple:
        # TODO: select days from JobDays by JOIN maybe
        with sqlite3.connect(self.db_file) as connection:
            cursor = connection.cursor()
            print(_id, type(_id))
            cursor.execute("SELECT * FROM Job WHERE id=?", (str(_id),))
            row = cursor.fetchone()
            return row
