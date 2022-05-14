import datetime
import sqlite3
import traceback
from typing import List

from telegram.ext import JobQueue
from src.job_worker.callbacks import poll_callback, remind_callback, reserve_callback


class Loader:
    db_file = 'db/job-queue.db'

    def __init__(self, job_queue: JobQueue) -> None:
        self._job_queue = job_queue

    def load_jobs(self) -> None:
        raw_jobs = self._select_all_jobs_from_db()
        jobs = self._squash_jobs(raw_jobs)
        for job in jobs:
            self._set_job_queue(job)

    def _set_job_queue(self, job: dict) -> bool:
        TAIPEI_GMT_TIME_DELTA = -8
        if job['callback_name'] == 'poll_callback':
            _callback = poll_callback
        elif job['callback_name'] == 'remind_callback':
            _callback = remind_callback
        elif job['callback_name'] == 'reserve_callback':
            _callback = reserve_callback
        try:
            self._job_queue.run_daily(
                time=datetime.time(hour=job['hour'] + TAIPEI_GMT_TIME_DELTA, minute=job['minute']),
                days=job['days'],
                callback=_callback,
                name=job['job_name'],
                context=job['chat_room_id']
            )
            return True
        except Exception:
            traceback.print_exc()
            return False

    def _squash_jobs(self, jobs: List[tuple]):
        days_dicts = {}
        job_dicts = {}
        for i in jobs:
            if i[0] in days_dicts.keys():
                days_dicts[i[0]].append(i[9])
            else:
                days_dicts[i[0]] = [i[9]]
                job_dicts[i[0]] = {
                    'job_name': i[1],
                    'hour': int(i[2]),
                    'minute': int(i[3]),
                    'days': [],
                    'callback_name': i[4],
                    'chat_room_id': i[5],
                    'worker_type': i[6],
                }
        processed_jobs = []
        for i in job_dicts.keys():
            job_dicts[i]['days'] = days_dicts[i]
            processed_jobs.append(job_dicts[i])
        return processed_jobs

    def _select_all_jobs_from_db(self) -> List[tuple]:
        with sqlite3.connect(self.db_file) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Job JOIN JobDay on Job.id=JobDay.job_id")
            rows = cursor.fetchall()
            return rows
