import traceback

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from src.job_worker.parser import JobWorkerParser
from src.job_worker.job_worker import JobWorker
from src.enums import SubCommand
from src.util import agent_internal_error


class BaseToggle:
    def __init__(self) -> None:
        pass

    def get_toggle_handler(self, _name: str, _callback: callable, _worker_type: int) -> CommandHandler:
        def base_toggle_command(update: Update, context: CallbackContext) -> None:
            parser = JobWorkerParser()
            job_worker = JobWorker(_worker_type, update, context)
            try:
                subcommand = parser.parse(context.args)
                if subcommand == SubCommand.CREATE:
                    job_worker.create(
                        days=parser.get_days(),
                        times=parser.get_times(),
                        callback=_callback
                    )
                elif subcommand == SubCommand.CHECK:
                    job_worker.check()
                elif subcommand == SubCommand.DELETE:
                    job_worker.delete(job_db_id=parser.get_delete_id())
            except Exception:
                traceback.print_exc()
                agent_internal_error(update, "內部發生一些錯誤椰～")

        return CommandHandler(_name, base_toggle_command)
