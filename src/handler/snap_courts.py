import re
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from src.db_mgr import SqliteDatabaseMgr
from src.db_models import SnapCourtJobModel
from src.handler.help import HelpHandler
from src.json_reader import MessageReader
from src.object import VacantCourt
from src.service import VacantCourtService


class SnapCourtsHandler(CommandHandler):
    def __init__(self):
        self.handler_command = "snap_courts"
        self.reader = MessageReader()

        super().__init__(self.handler_command, self.snap_courts_command())

    def snap_courts_command(self) -> callable:
        def callback(update: Update, context: CallbackContext):
            if self.is_help(context.args):
                self.help(update)
                return
            if self.is_check(context.args):
                self.check(update, context)
                return
            if self.is_snap_courts(context.args):
                self.snap_courts(update, context)
                return
            self.reply("command_error", update, replaced_vars={"command": context.args[0]})

        return callback

    def is_help(self, args) -> bool:
        if args[0] == "help" and len(args) == 1:
            return True
        return False

    def help(self, update: Update):
        help_handler = HelpHandler()
        help_handler.help_individual_command(self.handler_command, update)

    def is_check(self, args) -> bool:
        if len(args) != 1 or args[0] != "check":
            return False
        return True

    def check(self, update: Update, context: CallbackContext):
        username = update.message.from_user.username

        job_queue = context.job_queue
        jobs = job_queue.jobs()
        jobs = list(filter(lambda x: x.job.name.startswith(username), jobs))
        if len(jobs) == 0:
            self.reply(f"{self.handler_command}_check_empty", update)
            return

        db_mgr = SqliteDatabaseMgr()
        reply_msg = ""
        for j in jobs:
            row = db_mgr.query_first(SnapCourtJobModel, name=j.job.name)
            if row is None:
                continue
            reply_msg += f"每{row.interval}秒預約: 第{row.court}場 @ {row.date} {row.time}\n"
        self.reply(f"{self.handler_command}_check", update, replaced_vars={
            "message": reply_msg
        })

    def is_snap_courts(self, args) -> bool:
        if len(args) != 3:
            print(len(args))
            return False
        date_rule = "^(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$"
        date = args[0]
        if not re.match(date_rule, date):
            print("date not match")
            return False

        court = args[1]
        if not court.isnumeric():
            print("court not match 1")
            return False
        if int(court) < 0 or int(court) > 6:
            print("court not match 2")
            return False

        time_rule = "^(0[6-9]|1[0-9]|2[0-1]):00$"
        time = args[2]
        if not re.match(time_rule, time):
            print("time not match")
            return False
        return True

    def snap_courts(self, update: Update, context: CallbackContext):
        date = context.args[0]
        court = int(context.args[1])
        time = context.args[2]

        service = VacantCourtService(update, context)
        service.snap(VacantCourt(court, date, time))

    def reply(self, key, update: Update, replaced_vars: dict = {}, reply_options: dict = {}):
        reply_msg = self.reader.get(key, **replaced_vars)
        update.message.reply_text(reply_msg, **reply_options)