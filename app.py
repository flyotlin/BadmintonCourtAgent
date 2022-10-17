import argparse

from src.server import AyeServer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str, required=True, help="start bot server using either `polling` or `webhook`")
    args = parser.parse_args()

    server = AyeServer(".telegram-bot-conf")
    if args.type == "polling":
        server.start_polling()
    elif args.type == "webhook":
        server.start_webhook()
