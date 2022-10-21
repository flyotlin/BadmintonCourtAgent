from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from src.db_mgr import DatabaseMgr
from src.db_models import SnapCourtJobModel
from src.handler.help import HelpHandler
from src.json_reader import MessageReader
from src.object import VacantCourt
from src.parser import AyeParser
from src.service import VacantCourtService


class SnapCourtHandler(CommandHandler):
    def __init__(self, engine):
        self._engine = engine

        self.handler_command = "snap_court"
        self.reader = MessageReader()

        super().__init__(self.handler_command, self.snap_court_command())

    def snap_court_command(self) -> callable:
        def callback(update: Update, context: CallbackContext):
            parser = AyeParser(context.args)
            ret = parser.parse_snap_court()
            if ret == 0:
                self.help(update)
            elif ret == 1:
                self.check(update, context)
            elif ret == 2:
                self.snap_court(update, context)
            else:
                self.reply("command_error", update, replaced_vars={"command": context.args[0]})
        return callback

    def help(self, update: Update):
        help_handler = HelpHandler()
        help_handler.help_individual_command(self.handler_command, update)

    def check(self, update: Update, context: CallbackContext):
        username = update.message.from_user.username

        job_queue = context.job_queue
        jobs = job_queue.jobs()
        jobs = list(filter(lambda x: x.job.name.startswith(username), jobs))
        if len(jobs) == 0:
            self.reply(f"{self.handler_command}_check_empty", update)
            return

        db_mgr = DatabaseMgr(engine=self._engine)
        reply_msg = ""
        for j in jobs:
            row = db_mgr.query_first(SnapCourtJobModel, name=j.job.name)
            if row is None:
                continue
            reply_msg += f"每{row.interval}秒預約: 第{row.court}場 @ {row.date} {row.time}\n"
        self.reply(f"{self.handler_command}_check", update, replaced_vars={
            "message": reply_msg
        })

    def snap_court(self, update: Update, context: CallbackContext):
        date = context.args[0]
        court = int(context.args[1])
        time = context.args[2]

        service = VacantCourtService(update, context, self._engine)
        service.snap(VacantCourt(court, date, time))

    def reply(self, key, update: Update, replaced_vars: dict = {}, reply_options: dict = {}):
        reply_msg = self.reader.get(key, **replaced_vars)
        update.message.reply_text(reply_msg, **reply_options)
