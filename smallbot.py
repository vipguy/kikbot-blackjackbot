import argparse
import json
import os
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.datatypes.xmpp.errors import LoginError


# This bot class handles all the callbacks from the kik client
class EchoBot(KikClientCallback):
    def __init__(self, creds: dict):
        username = creds['username']
        password = creds.get('password') or input("Enter your password:")
        # Optional parameters
        device_id = creds['device_id']
        android_id = creds['android_id']
        # Node
        node = creds.get('node')
        self.client = KikClient(self, username, str(password), node, device_id=device_id, android_id=android_id)
        self.client.wait_for_messages()
    # This method is called when the bot is fully logged in and setup
    def on_authenticated(self):
        self.client.request_roster()  # request list of chat partners

    # This method is called when the bot receives a direct message (chat message)
    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        self.client.send_chat_message(chat_message.from_jid, f'You said "{chat_message.body}"!')

    # This method is called when the bot receives a chat message in a group
    def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        self.client.send_chat_message(chat_message.group_jid, f'You said "{chat_message.body}"!')

    # This method is called if a captcha is required to login
    def on_login_error(self, login_error: LoginError):
        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)


def main():
    # The credentials file where you store the bot's login information
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--creds', default='creds.json', help='Path to credentials file')
    args = parser.parse_args()

    # Changes the current working directory to /examples
    if not os.path.isfile(args.creds):
        print("Can't find credentials file.")
        return

    # Change the current working directory to /examples
    os.chdir("file path to credit")

    # load the bot's credentials from creds.json
    with open(args.creds, "r") as f:
        creds = json.load(f)

    # Create an instance of EchoBot
    vip = EchoBot(creds)

if __name__ == '__main__':
    main()

    creds_file = "creds.json"

    # Check if the credentials file is in the current working directory, otherwise change directory
    if not os.path.isfile(creds_file):
        os.chdir("credit file path")

    # Load the bot's credentials from creds.json
    with open(creds_file) as f:
        creds = json.load(f)
    callback = EchoBot(creds)
