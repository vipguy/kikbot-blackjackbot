# this bot has captcha say captcha in group to turn it off and on (default on
# add and empty group jid to use as the heartbeat to keep bot alive 
# add bot jids to def on_group_status_received(self, response: chatting.IncomingGroupStatus): (can be done alot better lol )
import argparse
import json
import logging
import os
import threading
import time
import random
import re
from termcolor import colored
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.datatypes.xmpp.errors import LoginError
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse
from helper_funcs import add_admin, is_user_admin, remove_admin
super = ""
logging.basicConfig(
level=logging.ERROR,
format="%(asctime)s [%(levelname)s]: %(message)s")
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
        #Captcha
        self.pending_math_problems = {}  # Dictionary to store pending math problems
        self.captcha_status = {}
        self.timeout_duration = 20  # Set the timeout duration in seconds
        self.timers = {}  # Dictionary to store timers for each user
        self.client.wait_for_messages()
    # This method is called when the bot is fully logged in and setup
    def on_authenticated(self):
        self.client.request_roster()  # request list of chat partners
    #keeps bot alive 
    def send_heartbeat(self, group_jid='1100221456712_g@groups.kik.com'):
        while True:
            try:
                if group_jid:
                    self.client.send_chat_message(group_jid, " Status Check: Online Ping")
                time.sleep(300)
            except Exception as e:
                logging.error(f"Heartbeat error: {e}")

    def start_heartbeat(self):
        heartbeat_thread = threading.Thread(target=self.send_heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()
    # This method is called when the bot receives a direct message (chat message)
    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        self.client.send_chat_message(chat_message.from_jid, f'You said "{chat_message.body}"!')

    # This method is called when the bot receives a chat message in a group
    def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        separator = colored("--------------------------------------------------------", "cyan")
        group_message_header = colored("[+ GROUP MESSAGE +]", "cyan")
        print(separator)
        print(group_message_header)
        print(colored(f"From AJID: {chat_message.from_jid}", "yellow"))
        print(colored(f"From group: {chat_message.group_jid}", "yellow"))
        print(colored(f"Says: {chat_message.body}", "red"))

        # Check if the message is related to the Blackjack game
        if chat_message.group_jid in self.game_state:
            print(separator)
        print(separator)
        if chat_message.from_jid in self.pending_math_problems:
            # Display the math problem to the user
            problem_message = self.pending_math_problems[chat_message.from_jid]["problem"]
            self.client.send_chat_message(chat_message.from_jid, problem_message)

            # Schedule a timer to remove the user if no response within the timeout
            timer = threading.Timer(self.timeout_duration, self.remove_user, args=(chat_message.group_jid, chat_message.from_jid))
            timer.start()

            # Store the timer in the timers dictionary
            self.timers[chat_message.from_jid] = timer

            # Check if the message contains a valid answer
            self.check_math_answer(chat_message)

        # Check if the message contains a valid answer and process it
        if chat_message.from_jid in self.pending_math_problems:
            user_answer = chat_message.body.strip()
            correct_solution = self.pending_math_problems[chat_message.from_jid]["solution"]

            if user_answer.isdigit() and int(user_answer) == correct_solution:
                # Correct answer: You can implement your desired logic here
                self.client.send_chat_message(chat_message.group_jid, "Correct! Welcome to the group.")
            else:
                # Incorrect answer: Remove the user from the group
                self.client.remove_peer_from_group(chat_message.group_jid, chat_message.from_jid)
                self.client.send_chat_message(chat_message.group_jid, "Incorrect answer. User removed from the group.")
        #MUST BE ADMIN OR SUPER 
        if is_user_admin(chat_message.from_jid, chat_message.group_jid):
            is_admin = True
            is_superadmin = False
        else:
            is_admin = False
            is_superadmin = False
       # Convert message to lowercase for case-insensitive comparisons
        message = str(chat_message.body.lower())
        #VIEW IF CAPTCHA IS SET TO ON(default ON) 
        if message == "settings":
            if chat_message.body.lower() and chat_message.from_jid in super or is_admin:
                self.show_settings(chat_message.group_jid)
            else:
                self.client.send_chat_message(chat_message.group_jid, "You don't have permission to view settings.")

        if message == "captcha":
            if chat_message.body.lower() and chat_message.from_jid in super or is_admin:
                current_status = self.get_captcha_status(chat_message.group_jid)
                new_status = not current_status  # Toggle the status
                self.set_captcha_status(chat_message.group_jid, new_status)
                status_message = "Enabled" if new_status else "Disabled"
                self.client.send_chat_message(chat_message.group_jid, f"Captcha is now {status_message}.")
            else:
                self.client.send_chat_message(chat_message.group_jid, "You don't have permission to change captcha settings.")

    def show_settings(self, group_jid):
        captcha_status = "Enabled" if self.get_captcha_status(group_jid) else "Disabled"

        settings_message = (
        f'[Command Settings]\n'
        f'Captcha: {captcha_status}\n'
        # Add other commands and their status here
        )

        self.client.send_chat_message(group_jid, settings_message) 
    def get_captcha_status(self, group_jid):
        # Get captcha status for the group, default to True if not set
        return self.captcha_status.get(group_jid, True) 
    def set_captcha_status(self, group_jid, status):
        # Set captcha status for the group
        self.captcha_status[group_jid] = status        
    def remove_user(self, group_jid, user_jid):
        # Remove the user from the group
        self.client.remove_peer_from_group(group_jid, user_jid)
        self.client.send_chat_message(group_jid, "Timeout or bot: User removed from the group.")
    def check_math_answer(self, chat_message):
        # Check if the user's answer is correct
        user_answer = chat_message.body.strip()
        correct_solution = self.pending_math_problems[chat_message.from_jid]["solution"]

        if user_answer.isdigit() and int(user_answer) == correct_solution:
            # Correct answer: Implement your desired logic here
            # Cancel the timer since the user answered correctly
            if chat_message.from_jid in self.timers:
                self.timers[chat_message.from_jid].cancel()
                del self.timers[chat_message.from_jid]
            else:
                # Incorrect answer: Remove the user
                self.remove_user(chat_message.group_jid, chat_message.from_jid)
    def on_group_status_received(self, response: chatting.IncomingGroupStatus):
        print(self.client.request_info_of_users(response.status_jid))
        if re.search(" has promoted ", str(response.status)):
            add_admin(response.group_jid, response.status_jid)

        elif re.search(" has removed admin status from ", str(response.status)):
            remove_admin(response.group_jid, response.status_jid)

        elif re.search(" from this group$", str(response.status)) or re.search("^You have removed ", str(response.status)) or re.search(" has banned ", str(response.status)):
            try:
                remove_admin(response.group_jid, response.status_jid)
            except:
                pass

        elif re.search(" has left the chat$", str(response.status)):
            try:
                remove_admin(response.group_jid, response.status_jid)
            except:
                pass

        elif re.search(" has joined the chat$", str(response.status)) or re.search(" has joined the chat, invited by ", str(response.status)):
                # Check if the user is a bot that needs to be removed
            if response.status_jid in ["ki7i2vvrjyn2vatxrnwevw23gao26qytetof2l3zkugu4345z5lq_a@talk.kik.com",
                    "fsxuovsiv6idrzrh7bzbp3yvlleu5ryi7zvp7hulld4v7znvw6fq_a@talk.kik.com",
                    "lpxs22qlsmljkc3g5c2kppndfl7luczdkoowoq46oynsclseqpkq_a@talk.kik.com",
                    "virm4x2appzzxfz6m4zx7v6ii3pncau7wfb3zdnbvu2fnzwsye7a_a@talk.kik.com",
                    "ifowda6y73kbqb365tw3zs3jtclpmtjckupcm2gs66cyqcr5cr2q_a@talk.kik.com",
                    "2s3h224lgxowifre5lzqovnausbk2pbc7thr5z3k63phbfkcct6q_a@talk.kik.com",
                    "ke6stdjsskolvrh3ys4oiksoc5kcd5fozam7twqg2gkmo3lml44a_a@talk.kik.com",
                    "vbpzbdyz7dczp5yazqdqbdkfqexhxabpcvbxex34iaou6rlzi4ha_a@talk.kik.com",
                    "g4xgvr7imos3npbtic7tkich6eyvk5dx2on5x2md23wjd2dgna4q_a@talk.kik.com"]:
                    self.client.remove_peer_from_group(response.group_jid, response.status_jid)
                    self.client.send_chat_message(response.group_jid, "Bot removed from the group.")
            else:
                # Send math problem if captcha is enabled
                if self.get_captcha_status(response.group_jid):
                    num1 = random.randint(1, 10)
                    num2 = random.randint(1, 10)
                    solution = num1 + num2

                    # Store the math problem along with the user's JID
                    self.pending_math_problems[response.status_jid] = {
                        "problem": f"Welcome to the group. Solve the math problem to stay. only say the number: {num1} + {num2}",
                        "solution": solution
                    }

                    # Send the math problem to the entire group
                    self.client.send_chat_message(response.group_jid, self.pending_math_problems[response.status_jid]["problem"])
    def on_roster_received(self, response: FetchRosterResponse):
        groups = []
        users = []
        for peer in response.peers:
            if "groups.kik.com" in peer.jid:
                groups.append(peer.jid)
            else:
                users.append(peer.jid)

        user_text = '\n'.join([f"User: {us}" for us in users])
        group_text = '\n'.join([f"Group: {gr}" for gr in groups])
        partner_count = len(response.peers)

        roster_info = (
            f"Roster Received\n"
            f"Total Peers: {partner_count}\n"
            f"Groups ({len(groups)}):\n{group_text}\n"
            f"Users ({len(users)}):\n{user_text}"
        )

        print(roster_info)            
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
