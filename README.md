# Badminton Court Agent Bot

## How to Run
1. Prepare `.telegram-bot-conf` under `/BadmintonCourtAgent`.
   Get your Bot Token from **BotFather in Telegram**, and fill it in.
    `$ cp .telegram-bot-conf.Example .telegram-bot-conf`
2. Run the Bot
    Now we only support type `polling`, `webhook` is under development.

    - Run in local, with venv
    `$ python3 -m venv .venv`
    `$ source ./.venv/bin/activate`
    `$ python3 -m pip install -r requirements.txt`
    `$ python3 app.py -t polling`
    - Run in a container
    use `docker-compose` (v1.x) or `docker compose` (v2.x) depends on the version of your docker engine
    `$ docker compose up -d`

## Supported Commands
- `/help`:

    Check all supported commands, `/help [COMMAND]`.
- `/set_token`:

    set 17-fit token, `/set_token ["help"]`
- `/check_courts`:

    check available courts. `/check_courts ("help"|DATE COURT)`
- `/snap_courts`:

    set a repeating job to reserve a court every `INTERVAL` seconds, no matter if the court is available or not.
    `/snap_courts ("help"|"check"|DATE COURT TIME)`

> COMMAND: either "set_token", "check_courts", "snap_courts"

> DATE: "month-date". Like 06-03, remember to pad zero in the front.

> COURT: 1~6

> TIME: hour:00. Like 08:00, remember to pad zero in the front.

## Guide to Source Code
### Directories
- resource/: Some static files like json
- src/: Bot source code
- src/handler: Each handler corresponds to a command supported in our bot.
- tests/: all kinds of tests to ensure our bot works properly
### Files
- app.py:

    bot main entry point, includes `AyeServer` to start the whole bot service.
- server.py:

    sets up **telegram-bot-conf**, **handlers**, **logger**, and decide **service type** (either `polling` or `webhook`).
- logger.py:

    provides a pre-configured logger, a static logger instance shared accross the whole service.
- json_reader.py:

    read messages defined in `resource/messages.json`, so that messages won't be hard-coded in source code.
- db_mgr.py:

    abstract db manager that provides basic db operations, pass in different db engine (defaults to **Sqlite**) in `AyeServer`.
- db_models.py:

    ORM models mapping to db tables, we use `sqlalchemy` as ORM framework.
- agent.py:

    Interact with 17Fit API, provides `check()` and `go()` to check current vacant courts and reserve a specific vacant courts respectively.
- object.py

    Defined some useful object representing the concept we used across the bot service.
    For instance, `User` represents a specific user interacting with our bot, and `VacantCourt` represents court available on 17Fit right now.
- service.py

    Serves the corresponding objects in `objects.py`.

    You can think of this (**XxxService**) as a **service courter**, when you ask **XxxService**, it returns the object(Xxx) or performs some operations related to the object(Xxx).
- parser.py

    Parses the arguments provided, implementing a simple recursive descent parser here.

## Acknowledgement
Special thanks to @cliffxzx.
![](https://avatars.githubusercontent.com/u/44764053?v=4)
