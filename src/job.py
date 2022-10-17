from telegram import Update
from telegram.ext import CallbackContext
from time import time


class AyeJob:
    def __init__(self, update: Update, context: CallbackContext) -> None:
        self._update = update
        self._context = context
        self._job_name = self._gen_job_name()

    def _gen_job_name(self) -> str:
        username = self._update.message.from_user.username
        user_id = self._update.message.from_user.id
        epoch = int(time())

        return f"{username}_{user_id+epoch}"

    def _is_in_database(self) -> bool:
        """Abstract method, should be implemented by subclass"""
        pass

    def _is_in_jobqueue(self) -> bool:
        """Abstract method, should be implemented by subclass"""
        pass

    def _create_in_database(self):
        """Abstract method, should be implemented by subclass"""
        pass

    def _create_in_jobqueue(self):
        """Abstract method, should be implemented by subclass"""
        pass


class RepeatingJob(AyeJob):
    def __init__(self, callback: callable, interval: int, update: Update, context: CallbackContext) -> None:
        self._callback = callback
        self._interval = interval
        super().__init__(update, context)

    def _is_in_database(self) -> bool:
        return True

    def _is_in_jobqueue(self) -> bool:
        job_queue = self._context.job_queue
        jobs = job_queue.get_jobs_by_name(self._job_name)
        if len(jobs) == 0:
            return False
        return True

    def _create_in_database(self):
        pass

    def _create_in_jobqueue(self):
        job_queue = self._context.job_queue
        job_queue.run_repeating(
            callback=self._callback,
            interval=self._interval,
            name=self._job_name,
            context=self._update.message.chat_id
        )
