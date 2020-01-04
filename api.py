import os

from dotenv import load_dotenv

from push_random.services import PushoverNotificationSender


def main() -> None:
    load_dotenv()
    PUSHOVER_USER = os.environ["PUSHOVER_USER"]
    PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]

    sender = PushoverNotificationSender(PUSHOVER_USER, PUSHOVER_TOKEN)
    message = 'test'
    sender.send(message)



if __name__ == '__main__':
    main()
