import argparse
import json
import logging
import os
import random
import re
import string
import threading
import time
import tempfile
from typing import Union
from PIL import Image, ImageDraw, ImageFont
import requests
import validators
import youtube_dl

from database import Database
from chatbot_db import ChatbotDatabase

from kik_unofficial.datatypes.xmpp import chatting

from termcolor import colored
from helper_funcs import add_admin, is_user_admin, remove_admin
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.chatting import  IncomingGifMessage
from kik_unofficial.datatypes.xmpp.errors import LoginError
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeersInfoResponse
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse
from kik_unofficial.datatypes.xmpp.xiphias import UsersByAliasResponse, UsersResponse
API_key = "get your own key"
super = "add your jid"
responses = {}
def sanitize_filename(filename):
     # Replace or remove invalid characters
    sanitized = re.sub(r'[\\/*?:"<>|]', '', filename)
    return sanitized
def randomString(length):
    return ''.join(random.choice(string.ascii_uppercase) for i in range(length)) 
try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen, urlencode
# Constants
VIDEO_SIZE_LIMIT = 15728640
VIDEO_COMPRESSION_LIMIT = 5000000
VIDEO_SLEEP_DELAY = 5
from moviepy.editor import VideoFileClip
from pytube import YouTube, Search
import validators

# Tic Tac Toe game class
class TicTacToe:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def make_computer_move(self):
        # Check for any winning moves
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    # Simulate making the move
                    self.board[row][col] = self.current_player
                    if self.check_winner() == self.current_player:
                        # If this move leads to a win, make it and return
                        self.current_player = "O" if self.current_player == "X" else "X"
                        return self.board
                
                    # Undo the move
                    self.board[row][col] = " "
    
        # Check for any blocking moves (preventing opponent from winning)
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    # Simulate making the move for the opponent
                    self.board[row][col] = "X" if self.current_player == "O" else "O"
                    if self.check_winner() == "X" if self.current_player == "O" else "O":
                        # If this move prevents the opponent from winning, block it
                        self.board[row][col] = self.current_player
                        self.current_player = "O" if self.current_player == "X" else "X"
                        return self.board
                
                    # Undo the move
                    self.board[row][col] = " "
    
        # If no winning or blocking moves, make a move that leads to the highest chance of winning
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    # Simulate making the move
                    self.board[row][col] = self.current_player
                    # Check the number of winning moves after this move
                    winning_moves_count = sum(self.board[row][col] == " " and self.check_winner() == self.current_player for row in range(3) for col in range(3))
                    # Undo the move
                    self.board[row][col] = " "
                    if winning_moves_count >= 2:
                        # If this move leads to two or more winning moves, make it and return
                        self.board[row][col] = self.current_player
                        self.current_player = "O" if self.current_player == "X" else "X"
                        return self.board
    
        # If none of the above conditions are met, make a random move
        while True:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if self.board[row][col] == " ":
                self.board[row][col] = self.current_player
                self.current_player = "O" if self.current_player == "X" else "X"
                return self.board

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        else:
            return False

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]
        return None

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == " ":
                    return False
        return True

    def get_board_image(self):
        # Load the Tic Tac Toe board image
        board_image = Image.open("ttt.png")#path to tic tac toe image board provided
        draw = ImageDraw.Draw(board_image)

        # Define coordinates and dimensions for drawing lines and text
        line_color = "black"
        line_width = 5
        font_size = 10  # Adjust the font size for zone labels
        font = ImageFont.truetype("arial.ttf", size=font_size)
        x_o_font_size = 30  # Adjust the font size for "X" and "O"
        x_o_font = ImageFont.truetype("arial.ttf", size=x_o_font_size)
        text_color = "black"
        zone_offset = 27  # Offset for zone label position, increased for moving more to the left

        # Draw vertical lines
        for x in range(1, 3):
            draw.line([(x * (board_image.width // 3), 0), (x * (board_image.width // 3), board_image.height)],
                  fill=line_color, width=line_width)

        # Draw horizontal lines
        for y in range(1, 3):
            draw.line([(0, y * (board_image.height // 3)), (board_image.width, y * (board_image.height // 3))],
                  fill=line_color, width=line_width)

        # Draw X's and O's
        for i in range(3):
            for j in range(3):
                zone_label = f"{j}{i}"  # Swap the positions of row and column indices
                cell_center = ((j + 0.5) * (board_image.width // 3), (i + 0.5) * (board_image.height // 3))
                label_width, label_height = draw.textsize(zone_label, font=font)
                # Calculate the position for the zone label
                label_position = (cell_center[0] - label_width / 2 - zone_offset, cell_center[1] - label_height / 2 - zone_offset)
                draw.text(label_position, zone_label, fill=text_color, font=font)
                # Adjust the position for drawing X and O
                x_o_position = (cell_center[0] - x_o_font_size / 3, cell_center[1] - x_o_font_size / 2)
                if self.board[i][j] == "X":
                    draw.text(x_o_position, "X", fill=text_color, font=x_o_font)  # Larger font for "X"
                elif self.board[i][j] == "O":
                    draw.text(x_o_position, "O", fill=text_color, font=x_o_font)  # Larger font for "O"

        # Return the modified image
        return board_image
        

logging.basicConfig(
level=logging.ERROR,
format="%(asctime)s [%(levelname)s]: %(message)s")
# Define a dictionary to store image URLs and messages
image_commands = {
    "monkey": {
        "url": 'https://source.unsplash.com/1600x900/?monkey',
        "message": "Here's a random monkey image!"
    },
    "cat": {
        "url": 'https://api.thecatapi.com/v1/images/search',
        "message": "Here's a random cat image!"
    },
    "duck": {
        "url": 'https://random-d.uk/api/v2/random',
        "message": "Here's a random duck image!"
    },
    "panda": {
        "url": 'https://some-random-api.ml/img/panda',
        "message": "Here's a random panda image!"
    },
    "doggie": {
        "url": 'https://dog.ceo/api/breeds/image/random',
        "message": "Here's a random dog image!"
    },
    "wolf": {
        "url": 'https://source.unsplash.com/random/800x600/?wolf',
        "message": "Here's a random wolf image!",
        "facts": [
            "Wolves are the largest members of the dog family.",
                "Wolves can run up to 40 miles per hour.",
                "Wolves have excellent hearing and can hear sounds up to 6 miles away.",
                "Wolves are social animals that live in packs.",
                "Wolves can communicate with each other using howls, whines, and barks.",
                "Wolves mate for life and usually have a litter of 4-6 pups.",
                "Wolves have powerful jaws that can exert up to 1,500 pounds of pressure per square inch.",
                "Wolves play an important role in maintaining healthy ecosystems by controlling prey populations.",
                "Wolves are often misunderstood and feared, but they rarely pose a threat to humans.",
                "Wolves have been a part of human mythology and folklore for thousands of years."
            ]
    },
    "random fox": {
        "url": 'https://randomfox.ca/floof/',
        "message": "Here's a random fox image!"
    }
}
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
        
        #YOUTUBE
        self.search_results = {}  # Dictionary to store search results
        self.awaiting_selection = {}  # Dictionary to track if awaiting selection
        # Initialize tic-tac-toe game state
        self.tic_tac_toe_games = {}
        # Trigger > response 
        self.custom_commands = {}
        # Initialize scramble dictionaries 
        self.game_initiators = {}  # Dictionary to store game initiators
        self.words = []  # Words loaded from the JSON file
        self.rounds = 5  # Set the number of rounds
        self.current_round = 0
        self.player_score = 0
        self.scrambled_word = ""
        self.game_state = {}
        # Database
        self.database = Database
        self.db_lock = threading.Lock()
        self.user_data = {}
        self.database = ChatbotDatabase()
        self.client.wait_for_messages()
    #keeps bot alive 
    def send_heartbeat(self, group_jid='add an empty group jid here'):
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

    # This method is called when the bot is fully logged in and setup
    def on_authenticated(self):
        self.client.request_roster()  # Request a list of chat partners
    def some_database_write_method(self):
        # Use the lock to ensure only one thread can write at a time
        with self.db_lock:
            # Perform database write operations
            pass
    def handle_commands(self, command, command_parts, chat_message):
        if command == "/save":
            try:
                _, word, response = chat_message.body.split(' ', 2)
                result = self.database.save_word_response(chat_message.group_jid, word, response)
                self.client.send_chat_message(chat_message.group_jid, result)
            except ValueError:
                self.client.send_chat_message(chat_message.group_jid, "Invalid format. Use /save [word] [response]")

        elif command == "/listsave":
            responses = self.database.get_word_responses(chat_message.group_jid)
            response_text = "\n".join([f"{word}/{response}" for word, response in responses])
            self.client.send_chat_message(chat_message.group_jid, response_text or "No saved word responses.")

        elif command == "/deletesave":
            if len(command_parts) > 1:
                word_to_delete = command_parts[1]
                result = self.database.delete_word_response(chat_message.group_jid, word_to_delete)
                self.client.send_chat_message(chat_message.group_jid, result)
            else:
                self.client.send_chat_message(chat_message.group_jid, "Please specify a word to delete. Format: /deletesave [word]")
    # Chat and Group Messages
    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        print("[+] '{}' says: {}".format(chat_message.from_jid, chat_message.body))

        if chat_message.body.lower() == "friend":
            self.client.add_friend(chat_message.from_jid)
            self.client.send_chat_message(chat_message.from_jid, "You can now add me to groups! <3")
    
        return
    
    # This method is called when the bot receives a chat message in a group
    def download_and_send_youtube_video(self, input_text, group_jid):
        try:
            # Check if input text is a valid URL
            if validators.url(input_text):
                yt = YouTube(input_text)
            else:
                # If not a URL, perform a search and list the top results
                search = Search(input_text)
                if not search.results:
                    return "No search results found for the query."

                # Store the search results in the 'self.search_results' dictionary
                self.search_results[group_jid] = search.results[:5]

                # Create a list of search results as text
                search_results_text = []
                for i, video in enumerate(self.search_results[group_jid]):
                    title = video.title
                    search_results_text.append(f"{i+1}. {title}")

                # Construct the response message with the search results
                response = "Search results:\n" + '\n'.join(search_results_text) + "\nReply with the number to download."
                return response

            video_stream = yt.streams.filter(file_extension="mp4").first()
            if video_stream:
                download_path = r'C:\Users\alexf\Desktop\kik-bot-api-unofficial-new\examples\playlist'
                if not os.path.exists(download_path):
                    os.makedirs(download_path)

                # Sanitize the filename
                safe_filename = sanitize_filename(yt.title)
                video_path = os.path.join(download_path, safe_filename + ".mp4")
                video_stream.download(output_path=download_path, filename=safe_filename + ".mp4")

                # Send the video file
                self.client.send_video_message(group_jid, video_path)

                # Wait 1 second before deleting the file
                time.sleep(1)

                # Delete the video file after sending
                if os.path.exists(video_path):
                    os.remove(video_path)

                # Return information about the video
                video_info = f"{yt.title}\nLength: {int(yt.length / 60)} minutes\nViews: {yt.views}"
                return video_info
            else:
                return "No suitable video stream found."
        except Exception as e:
            # In case of an exception, check if the file exists and delete it
            if os.path.exists(video_path):
                os.remove(video_path)
            return f"An error occurred: {e}"
    def search_youtube_and_list_options(self, query, group_jid):
        try:
            search = Search(query)
            if not search.results:
                return "No search results found for the query."

            # Store top 5 results in the 'self.search_results' dictionary
            self.search_results[group_jid] = search.results[:5]

            # Create a list of search results as text
            search_results_text = []
            for i, video in enumerate(self.search_results[group_jid]):
                title = video.title
                search_results_text.append(f"{i+1}. {title}")

            # Construct the response message with the search results
            response = "Search results:\n" + '\n'.join(search_results_text) + "\nReply with the number to download."
            return response
        except Exception as e:
            return f"An error occurred: {e}"
    def on_video_received(self, response: chatting.IncomingVideoMessage):
        if not response.group_jid:
            print(f"PM Video message was received from {response.video_url}")
        else:
            print(f"Group Video message was received from {response.group_jid}")
    def compress_or_trim_video(self, video_path):
        clip = VideoFileClip(video_path)

        # Option 1: Compress the video
        # Adjust target size (in bytes) as needed
        target_size = 14000000  # For example, 14MB
        compression_ratio = target_size / os.path.getsize(video_path)
        clip_resized = clip.resize(width=int(clip.w * compression_ratio ** 0.5))

        # Option 2: Trim the video
        # Adjust max_duration (in seconds) as needed
        max_duration = 60  # For example, 60 seconds
        if clip.duration > max_duration:
            clip_resized = clip.subclip(0, max_duration)

        # Save the compressed or trimmed video
        new_video_path = os.path.splitext(video_path)[0] + "_compressed.mp4"
        clip_resized.write_videofile(new_video_path)

        clip.close()
        return new_video_path
    def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        separator = colored("--------------------------------------------------------", "cyan")
        group_message_header = colored("[+ GROUP MESSAGE +]", "cyan")
        print(separator)
        print(group_message_header)
        print(colored(f"From AJID: {chat_message.from_jid}", "yellow"))
        print(colored(f"From group: {chat_message.group_jid}", "yellow"))
        print(colored(f"Says: {chat_message.body}", "yellow"))
        print(separator)
        command_parts = chat_message.body.strip().split()
        command = command_parts[0].lower() if command_parts else ""
        group_jid = chat_message.group_jid
        user_jid = chat_message.from_jid
        if group_jid in self.awaiting_selection and self.awaiting_selection[group_jid]:
            if self.awaiting_selection[group_jid]['user_jid'] == user_jid:
                if chat_message.body.isdigit():
                    # Convert the received message to an index
                    choice = int(chat_message.body) - 1
                    if 0 <= choice < len(self.search_results.get(group_jid, [])):
                        selected_video = self.search_results[group_jid][choice]
                        # Download and send the selected YouTube video
                        response = self.download_and_send_youtube_video(selected_video.watch_url, group_jid)
                        # Clear the awaiting selection state for this group
                        self.awaiting_selection[group_jid] = None
                        del self.search_results[group_jid]  # Clear the stored search results
                    else:
                        response = "Invalid choice. Please try again."
                else:
                    # Non-digit message received, ignore and reset the state
                    self.awaiting_selection[group_jid] = None
                    return  # Exit to allow normal chat flow
            else:
                # Message from a different user, allow normal chat flow
                return
        
            text = chat_message.body[5:]  

            if validators.url(text):
                # If it's a valid URL, process it as a direct link
                video_info = self.get_youtube_video_info(text)
                response = f"Video Title: {video_info['title']}\nArtist: {video_info.get('artist', 'Unknown')}\nURL: {text}"
                self.download_and_send_youtube_video(text, group_jid)
            else:
                # If it's not a URL, treat it as a search query
                response = self.search_youtube_and_list_options(text, group_jid)
                # Set the state to awaiting a selection from this user
                self.awaiting_selection[group_jid] = {'user_jid': user_jid, 'awaiting': True}
            self.client.send_chat_message(group_jid, response)

        # Convert message to lowercase for case-insensitive comparisons
        message = str(chat_message.body.lower())

        if chat_message.body.lower() in image_commands:
            command_info = image_commands[chat_message.body.lower()]
            image_url = command_info["url"]
            message = command_info["message"]
            facts = command_info.get("facts")  # Get the facts if available

            # Handle special cases for APIs returning JSON responses
            if "thecatapi.com" in image_url:
                response = requests.get(image_url).json()
                image_url = response[0].get('url')
            elif "random-d.uk" in image_url:
                response = requests.get(image_url).json()
                image_url = response.get('url')
            elif "some-random-api.ml" in image_url:
                response = requests.get(image_url).json()
                image_url = response.get('link')
            elif "randomfox.ca" in image_url:
                response = requests.get(image_url).json()
                image_url = response.get('image')
            elif "dog.ceo" in image_url:
                response = requests.get(image_url).json()
                image_url = response.get('message')

            # Download the image
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                # Save the image temporarily
                temp_image_path = 'temp_image.jpg'
                with open(temp_image_path, 'wb') as image_file:
                    image_file.write(image_response.content)

                # Send the image and message in the chat
                self.client.send_chat_image(chat_message.group_jid, temp_image_path)
                self.client.send_chat_message(chat_message.group_jid, message)

                # Send a random fact if available
                if facts:
                    random_fact = random.choice(facts)
                    self.client.send_chat_message(chat_message.group_jid, random_fact)

                # Delete the temporary image file
                os.remove(temp_image_path)
            else:
                # If failed to retrieve the image, send an error message
                error_message = "Failed to retrieve image for {}.".format(chat_message.body.lower())
                self.client.send_chat_message(chat_message.group_jid, error_message)
                # Check if the message is from a user with a pending math problem
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

        if command in ["/save", "/listsave", "/deletesave"]:
            self.handle_commands(command, command_parts, chat_message)
            return  # Stop further processing after handling a command
        if command == "/save":
            try:
                _, word, response = chat_message.body.split(' ', 2)
                result = self.database.save_word_response(chat_message.group_jid, word, response)
                self.client.send_chat_message(chat_message.group_jid, result)
            except ValueError:
                self.client.send_chat_message(chat_message.group_jid, "Invalid format. Use /save [word] [response]")
       
        # Check for word triggers first
        for word in chat_message.body.strip().lower().split():
            word_response = self.database.get_custom_command_response(chat_message.group_jid, word)
            if word_response:
                self.client.send_chat_message(chat_message.group_jid, word_response)
                return  # Exit the method after responding to a word trigger

        # Check if the message is a command for the Scramble game
        if command == "/scramble":
            # Initialize the game state for this group if it doesn't exist
            if group_jid not in self.game_state:
                self.prepare_word_scramble_game(group_jid)
            # Check if the game is already in progress
            in_game = self.game_state[group_jid]['in_game'] if group_jid in self.game_state else False
            if not in_game:
                self.prepare_word_scramble_game(group_jid)  # Start the game
            else:
                self.client.send_chat_message(group_jid, "A Scramble game is already in progress.")

        elif command == "/sguess" and group_jid in self.game_state and self.game_state[group_jid]['in_game']:
            guess = chat_message.body.split("/sguess", 1)[1].strip()
            self.handle_word_scramble_guess(group_jid, guess)

        elif command == "/scramblehelp":
            self.show_word_scramble_help(group_jid)
        if chat_message.body.lower() == "intro":
            with open("help2.txt","r") as f:
                self.client.send_chat_message(chat_message.group_jid, f.read())
            return 
        if chat_message.body.lower() == "help":
            with open("help.txt","r") as f:
                self.client.send_chat_message(chat_message.group_jid, f.read())
            return
        if chat_message.body.lower().startswith("ping"):
            # Define the path to an image file (e.g., 'lmao.jpeg')
            image_path = 'lmao.jpeg'
            # Send the image to the group chat
            self.client.send_chat_image(chat_message.group_jid, image_path)
        
        #🪨,📃,✂️ game
        if (chat_message.body.lower() == "🪨" or chat_message.body.lower() == "📃" or chat_message.body.lower() == "✂️"):
                possible_actions = ["🪨", "📃", "✂️"]
                computer_action = random.choice(possible_actions)
                self.client.send_chat_message(chat_message.group_jid, f"\nYou chose {chat_message.body.lower()}, computer chose {computer_action}.\n")
                if chat_message.body.lower() == computer_action:
                    self.client.send_chat_message(chat_message.group_jid, f"Both players selected {chat_message.body.lower()}. It's a tie!")
                elif chat_message.body.lower() == "🪨":
                    if computer_action == "✂️":
                        self.client.send_chat_message(chat_message.group_jid, "🪨 smashes ✂️! You win!")
                    else:
                        self.client.send_chat_message(chat_message.group_jid, "📃 covers 🪨! You lose.")
                elif chat_message.body.lower() == "📃":
                    if computer_action == "🪨":
                        self.client.send_chat_message(chat_message.group_jid, "📃 covers 🪨! You win!")
                    else:
                        self.client.send_chat_message(chat_message.group_jid, "✂️ cuts 📃! You lose.")
                elif chat_message.body.lower() == "✂️":
                    if computer_action == "📃":
                        self.client.send_chat_message(chat_message.group_jid, "✂️ cuts 📃! You win!")
                    else:
                        self.client.send_chat_message(chat_message.group_jid, "🪨 smashes ✂️! You lose.")
    
    #TIC TAC TOE
        if chat_message.body.lower() == "/ttt":
            self.start_tic_tac_toe_game(chat_message)
        elif chat_message.body.lower() == "/thelp":
            self.send_tic_tac_toe_help(chat_message.group_jid)
        elif chat_message.body.lower().startswith("/move "):
            self.make_tic_tac_toe_move(chat_message)

        #MUST BE ADMIN OR SUPER 
        if is_user_admin(chat_message.from_jid, chat_message.group_jid):
            is_admin = True
            is_superadmin = False
        else:
            is_admin = False
            is_superadmin = False
        #VIEW IF CAPTCHA IS SET TO ON 
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
        if message.startswith("/getw"):
            is_admin
            welcome_message = self.database.get_welcome(chat_message.group_jid)
            if welcome_message:
                self.client.send_chat_message(chat_message.group_jid, f"Welcome message is: {welcome_message}")
            else:
                self.client.send_chat_message(chat_message.group_jid, "No welcome message set.")
        if message.startswith("/deletew"):
            is_admin
            self.database.delete_welcome(chat_message.group_jid)
            self.client.send_chat_message(chat_message.group_jid, "Welcome message deleted.")
        if message.startswith("/welcome"):
            is_admin
            welcome_message = ' '.join(command_parts[1:])
            self.database.save_welcome(chat_message.group_jid, welcome_message)
            self.client.send_chat_message(chat_message.group_jid, "Welcome message set.")
        if command == "/save" and chat_message.from_jid in super or is_admin:
            try:
                _, word, response = chat_message.body.split(' ', 2)
                result = self.database.save_word_response(chat_message.group_jid, word, response)
                self.client.send_chat_message(chat_message.group_jid, result)
            except ValueError:
                self.client.send_chat_message(chat_message.group_jid, "Invalid format. Use /save [word] [response]")
        elif command == "/listsave" and chat_message.from_jid in super or is_admin:
            responses = self.database.get_word_responses(chat_message.group_jid)
            response_text = "\n".join([f"{word}/{response}" for word, response in responses])
            self.client.send_chat_message(chat_message.group_jid, response_text or "No saved word responses.")
        elif command == "/deletesave" and chat_message.from_jid in super or is_admin:
            if len(command_parts) > 1:
                word_to_delete = command_parts[1]
                result = self.database.delete_word_response(chat_message.group_jid, word_to_delete)
                self.client.send_chat_message(chat_message.group_jid, result)
            else:
                self.client.send_chat_message(chat_message.group_jid, "Please specify a word to delete. Format: /deletesave [word]")
    def send_tic_tac_toe_help(self, user_jid):
        help_message = (
            'Tic Tac Toe Help:'
            '/ttt - Start a new Tic Tac Toe game.'
            '/move [row] [col] - Make a move Example:'
            '/move 1 2 to place your symbol in row 1, column 2.'
            '/thelp - Display this help message'
        )
        self.client.send_chat_message(user_jid, help_message)
    def start_tic_tac_toe_game(self, chat_message):
        group_jid = chat_message.group_jid
        if group_jid not in self.tic_tac_toe_games:
            game = TicTacToe()
            self.tic_tac_toe_games[group_jid] = game
            self.client.send_chat_message(group_jid, "A new Tic Tac Toe game has started! Use /move [row] [col] to make your move. 0 0 is top left box")
        else:
            self.client.send_chat_message(group_jid, "A Tic Tac Toe game is already in progress.")

    def make_tic_tac_toe_move(self, chat_message):
        group_jid = chat_message.group_jid
        if group_jid in self.tic_tac_toe_games:
            game = self.tic_tac_toe_games[group_jid]
            move_args = chat_message.body.lower().split()[1:]
            if len(move_args) == 2 and all(arg.isdigit() for arg in move_args):
                row, col = map(int, move_args)
                if 0 <= row < 3 and 0 <= col < 3:
                    # Invert the row and column indices
                    if game.make_move(col, row):  # Adjust the order of indices
                        winner = game.check_winner()
                        if winner:
                            # Construct a message with the board image and winner
                            board_image = game.get_board_image()
                            message = f"{winner} wins!"
                            # Save the board image to a temporary file
                            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                                board_image.save(tmp_file.name)
                                # Send the message with the temporary image file and winner
                                self.client.send_chat_message(group_jid, message)
                                self.client.send_chat_image(group_jid, tmp_file.name)
                                # Delete the game from the list
                                del self.tic_tac_toe_games[group_jid]
                        elif game.is_full():
                            # Construct a message with the board image for a draw
                            board_image = game.get_board_image()
                            message = "The game is a draw!"
                            # Save the board image to a temporary file
                            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                                board_image.save(tmp_file.name)
                                # Send the message with the temporary image file
                                self.client.send_chat_message(group_jid, message)
                                self.client.send_chat_image(group_jid, tmp_file.name)
                                # Delete the game from the list
                                del self.tic_tac_toe_games[group_jid]
                        else:
                            # After the user's move, let the computer make its move
                            game.make_computer_move()
                            winner = game.check_winner()
                            if winner:
                                # Construct a message with the board image and winner
                                board_image = game.get_board_image()
                                message = f"{winner} wins!"
                                # Save the board image to a temporary file
                                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                                    board_image.save(tmp_file.name)
                                    # Send the message with the temporary image file and winner
                                    self.client.send_chat_message(group_jid, message)
                                    self.client.send_chat_image(group_jid, tmp_file.name)
                                    # Delete the game from the list
                                    del self.tic_tac_toe_games[group_jid]
                            else:
                                # Send the board image after both moves
                                board_image = game.get_board_image()
                                # Save the board image to a temporary file
                                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                                    board_image.save(tmp_file.name)
                                    # Send the message with the temporary image file
                                    self.client.send_chat_image(group_jid, tmp_file.name)
                    else:
                        self.client.send_chat_message(group_jid, "Invalid move. Try again.")
                else:
                    self.client.send_chat_message(group_jid, "Invalid move. Row and column must be between 0 and 2.")
            else:
                self.client.send_chat_message(group_jid, "Invalid move. Please specify row and column numbers.")
        else:
            self.client.send_chat_message(group_jid, "No Tic Tac Toe game is currently in progress.")
    #scrable game
    def show_word_scramble_help(self, group_jid):
        # Display help for Word Scramble game
        help_message = (
            "Word Scramble Help:\n\n"
            "Start a new game: /scramble\n"
            "Guess the word: /sguess [your_guess]\n"
            "Example guess: /s+guess example\n\n"
            "Rules:\n"
            "- Try to unscramble the word.\n"
            "- You have 3 attempts to guess the word.\n"
            "- Use hints wisely if needed."
        )
        self.client.send_chat_message(group_jid, help_message)
    def prepare_word_scramble_game(self, group_jid):
        # Load words from a JSON file
        with open("word_scramble_words.json", "r") as file:
            word_data = json.load(file)
            words = word_data.get("words", [])

        if not words:
            self.client.send_chat_message(group_jid, "No words found in the JSON file.")
            return

        # Select a random word from the list
        secret_word = random.choice(words)

        # Initialize game state for Word Scramble
        self.game_state[group_jid] = {
            'word': secret_word,
            'scrambled_word': self.scramble_word(secret_word),
            'attempts': 0
        }

        # Inform the group about the start of the game
        self.client.send_chat_message(group_jid, f"Word Scramble game started! Unscramble this word: {self.game_state[group_jid]['scrambled_word']}")
        self.game_state[group_jid]['in_game'] = True
    def scramble_word(self, word):
        # Scramble the characters of the word
        scrambled_word = list(word)
        random.shuffle(scrambled_word)
        return ''.join(scrambled_word)
    def handle_word_scramble_guess(self, group_jid, guess):
        game_data = self.game_state.get(group_jid, None)

        if game_data:
            secret_word = game_data['word']
            attempts = game_data['attempts']

            if guess.lower() == secret_word.lower():
                # Correct guess
                self.client.send_chat_message(group_jid, f"Correct! The word is '{secret_word}'.")
                self.game_state.pop(group_jid)  # Remove the game data
            else:
                # Incorrect guess
                attempts += 1
                if attempts >= 3:
                    # Player has exceeded the maximum number of attempts
                    self.client.send_chat_message(group_jid, f"Sorry, the word was '{secret_word}'. You've used up all your attempts.")
                    self.game_state.pop(group_jid)  # Remove the game data
                else:
                    # Provide a hint
                    hint = self.generate_hint(secret_word, attempts)
                    self.client.send_chat_message(group_jid, f"Incorrect guess. Here's a hint: {hint}")
                    self.game_state[group_jid]['attempts'] = attempts
        else:
            self.client.send_chat_message(group_jid, "No active Word Scramble game. Start one with /scramble.")
    def generate_hint(self, word, attempts):
        # Generate a hint based on the word and the number of attempts
        if attempts == 0:
            return f"The word has {len(word)} letters."
        elif attempts == 1:
            return f"The first letter of the word is '{word[0]}'."
        else:
            return f"The word rhymes with '{word[-3:]}'."
    #captcha settings
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
    
                
    # Listener for when Image received from group or PM
    def on_image_received(self, image_message: chatting.IncomingImageMessage):
        if not image_message.group_jid:
            print(f"PM Image message was received from {image_message.from_jid}")
        else:
            print(f"Group Image message was received from {image_message.from_jid}")

    # Listener for when Video received, group or PM
    def on_video_received(self, response: chatting.IncomingVideoMessage):
        if not response.group_jid:
            print(f"PM Video message was received from {response.video_url}")
        else:
            print(f"Group Video message was received from {response.group_jid}")

    # Listener for when GIF received, group or PM
    def on_gif_received(self, response: IncomingGifMessage):
        if not response.group_jid:
            print(f"PM GIF message was received from {response.from_jid}")
        else:
            print(f"Group GIF message was received from {response.group_jid}")

    # Listener for when Card received, group or PM
    def on_card_received(self, response: chatting.IncomingCardMessage):
        if not response.group_jid:
            print(f"PM Card message was received from {response.from_jid}")
        else:
            print(f"Group Card message was received from {response.group_jid}")

    # Listener for when Sticker received, group or PM
    def on_group_sticker(self, response: chatting.IncomingGroupSticker):
        if not response.group_jid:
            print(f"PM Sticker message was received from {response.from_jid}")
        else:
            print(f"Group Sticker message was received from {response.group_jid}")
    def on_image_received(self, image_message: chatting.IncomingImageMessage):
        print(f"[+] Image message was received from {image_message.from_jid}")

    # Events and Statuses
    def on_message_delivered(self, response: chatting.IncomingMessageDeliveredEvent):
        print(f"[+] Chat message with ID {response.message_id} is delivered.")

    def on_message_read(self, response: chatting.IncomingMessageReadEvent):
        print(f"[+] Human has read the message with ID {response.message_id}.")

    def on_is_typing_event_received(self, response: chatting.IncomingIsTypingEvent):
        print(f'[+] {response.from_jid} is now {"" if response.is_typing else "not "}typing.')

    def on_group_is_typing_event_received(self, response: chatting.IncomingGroupIsTypingEvent):
        print(f'[+] {response.from_jid} is now {"" if response.is_typing else "not "}typing in group {response.group_jid}')

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

    def on_peer_info_received(self, response: PeersInfoResponse):
        users = '\n'.join([str(member) for member in response.users])
        print(f'Peer info: {users}')

    # Listener for when Peer Info received through Xiphias request.
    def on_xiphias_get_users_response(self, response: Union[UsersResponse, UsersByAliasResponse]):
        users = '\n'.join([str(member) for member in response.users])
        print(f'Peer info: {users}')   

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
                    

                # Send welcome message if available
                welcome_message = self.database.get_welcome(response.group_jid)
                if welcome_message:
                    self.client.send_chat_message(response.group_jid, welcome_message)
    
    
    
    def on_sign_up_ended(self, response: RegisterResponse):
        print(f"[+] Registered as {response.kik_node}")

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
    os.chdir("Path to your credential")

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
        os.chdir("path to credentials")

    # Load the bot's credentials from creds.json
    with open(creds_file) as f:
        creds = json.load(f)
    callback = EchoBot(creds)
