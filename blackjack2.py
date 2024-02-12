
from collections import defaultdict
from io import BytesIO
from typing import Union
from matplotlib import pyplot as plt
from termcolor import colored
from PIL import Image, ImageDraw, ImageFont
from blackjack_bot import BlackjackDatabase
from chatbot_db import ChatbotDatabase
from helper_funcs import add_admin, is_user_admin, remove_admin
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeersInfoResponse
from kik_unofficial.datatypes.xmpp.xiphias import UsersByAliasResponse, UsersResponse
import json, logging, os, random, re, threading, time, openai, requests, validators, argparse, psutil
import tempfile
import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.errors import LoginError
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse
api_key = "Get YOUR OWN API KEY " #https://apilayer.com/
username = {}
response = {}
users = {}
super = ""
import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.errors import LoginError
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse

# Specify the path to your SQLite database file (replace 'your_database_file.sqlite3' with your actual path)
db_path = 'blackjack_bot.db'
# Specify a fixed table suffix that remains consistent across bot restarts
table_suffix = 'users'  
DEFAULT_BET_AMOUNT = 0
# Create the Database instance with the provided database file path and table suffix
database = BlackjackDatabase(db_path, table_suffix)
card = {'rank': 'A', 'suit': 'Spades'}
def main():
    # The credentials file where you store the bot's login information
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--creds', default='creds.json', help='Path to credentials file')
    args = parser.parse_args()

    # Changes the current working directory to /examples
    if not os.path.isfile(args.creds):
        print("Can't find credentials file.")
        return

    # load the bot's credentials from creds.json
    with open(args.creds, "r") as f:
        creds = json.load(f)

    bot = EchoBot(creds, database)

def sanitize_filename(filename):
     # Replace or remove invalid characters
    sanitized = re.sub(r'[\\/*?:"<>|]', '', filename)
    return sanitized

def sanitize_filename(filename):
     # Replace or remove invalid characters
    sanitized = re.sub(r'[\\/*?:"<>|]', '', filename)
    return sanitized

HEARTS = '♥'
DIAMONDS = '♦'
CLUBS = '♣'
SPADES = '♠'

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
        board_image = Image.open("YourPATH\kik-bot-api-unofficial-new\\examples\\var\\images\\ttt.png")
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
# Configure the logging as usual
logging.basicConfig(
    level=logging.INFO,  # Set your desired log level
    format="%(asctime)s [%(levelname)s]: %(message)s",
)
class EchoBot(KikClientCallback):
    DEFAULT_BET_AMOUNT = 0  # Define a default bet amount for the blackjack game
    def __init__(self, creds: dict, database):
        self.bot_display_name = None
        self.in_blackjack_game = False
        self.game_starter_jid = None  # JID of the user who started the game
        self.deck = []  # The deck for blackjack
        self.player = []  # The player's hand
        self.dealer = []  # The dealer's hand
        self.database = database
        self.game_state = defaultdict(lambda: {'in_game': False, 'deck': [], 'player_hand': [], 'dealer_hand': [], 'current_phase': 'waiting_for_bets', 'bet_amount': 0})
        self.reset_all_games()
        #HEARTBEAT KEEP ALIVE PRIMAL WAY
        self.start_heartbeat()
        username = creds['username']
        password = creds.get('password') or input("Enter your password:")
        # Optional parameters
        device_id = creds['device_id']
        android_id = creds['android_id']

        node = creds.get('node')
        self.client = KikClient(self, username, str(password), node, device_id=device_id, android_id=android_id)
        # Initialize tic-tac-toe game state
        self.tic_tac_toe_games = {}
        self.custom_commands = {}
        # Initialize scramble dictionaries 
        self.game_initiators = {}  # Dictionary to store game initiators
        self.words = []  # Words loaded from the JSON file
        self.rounds = 5  # Set the number of rounds
        self.current_round = 0
        self.player_score = 0
        self.scrambled_word = ""
        self.game_state = {}
        #YouTube
        self.search_results = {}  # Dictionary to store search results
        self.awaiting_selection = {}  # Dictionary to track if awaiting selection
        #Captcha
        self.pending_math_problems = {}  # Dictionary to store pending math problems
         # Initialize a dictionary to store captcha status for each group
        self.captcha_status = {}
        self.captcha_answers = {}
        self.timeout_duration = 20  # Set the timeout duration in seconds
        self.timers = {}  # Dictionary to store timers for each user
        self.db_lock = threading.Lock()
        self.user_data = {}
        self.db = BlackjackDatabase(db_path, table_suffix)  # Ensure this is the correct class with the transfer_chips method
        # Initialize dictionaries to hold commands  triggers for each group
        self.db = ChatbotDatabase()
        self.database = ChatbotDatabase()
        self.client.wait_for_messages()
    def send_heartbeat(self, group_jid=''): #ADD A group_jid OR user_jid
        while True:
            try:
                if group_jid:
                    self.client.send_chat_message(group_jid, " Status Check: Online Ping")#EDIT YOUR MESSAGE
                time.sleep(300)  
            except Exception as e:
                logging.error(f"Heartbeat error: {e}")
    def start_heartbeat(self):
        heartbeat_thread = threading.Thread(target=self.send_heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()    
    # Logic to load these into your bot's data structure
    def some_database_write_method(self):
        # Use the lock to ensure only one thread can write at a time
        with self.db_lock:
            # Perform database write operations
            pass
    
    # This method is called when the bot is fully logged in and setup
    def on_authenticated(self):
        # Request the roster list
        self.client.request_roster(is_big=True)


    def on_login_ended(self, response: LoginResponse):
        print("Full name: {} {}".format(response.first_name, response.last_name))
    # This method is called when the bot receives a direct message (chat message)
    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        self.client.send_chat_message(chat_message.from_jid, f'You said "{chat_message.body}"!')   
    #YouTube
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
    #trigger/Response
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
    
    
    # simple method to use your nicknames and group name of your choice per groupjid ( clearly a betterway to do this )
    def get_group_name(self, group_jid: str) -> str:
        # Dictionary mapping group JIDs to group names
        group_names = {
            "groupjid here ": "group name here of your choice ",
            "groupjid here ": "group name here of your choice ",
            
            # Add more mappings as needed
        }
        return group_names.get(group_jid, "")  # Return the group name or an empty string if not found

    
    def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        separator = colored("--------------------------------------------------------", "cyan")
        group_message_header = colored("[+ GROUP MESSAGE +]", "cyan")
        print(separator)
        print(group_message_header)
        print(colored(f"From: {database.get_user_nickname_from_db(chat_message.from_jid)}", "yellow"))
       # Get the group name based on the group JID
        group_name = self.get_group_name(chat_message.group_jid)
        group_name_text = colored(f"From group: {group_name}", "yellow") if group_name else colored(f"From group: {chat_message.group_jid}", "yellow")
        print(group_name_text)

        print(colored(f"Says: {chat_message.body}", "red"))

        # Check if the message is related to the Blackjack game
        if chat_message.group_jid in self.game_state:
            print(separator)

        body = chat_message.body.split()
        command = body[0].lower() if body else ""
        group_jid = chat_message.group_jid
        user_jid = chat_message.from_jid
        message_body = chat_message.body
        command_parts = chat_message.body.strip().split()
        command = command_parts[0].lower() if command_parts else ""
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
        if user_jid not in self.user_data:
            self.user_data[user_jid] = {'nickname': None}  # Initialize with default values
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
        if chat_message.from_jid in self.pending_math_problems:
            self.check_math_answer(chat_message)
        
        if chat_message.from_jid in self.pending_math_problems:
            # Check if the user's answer is correct
            user_answer = chat_message.body.strip()
            correct_solution = self.pending_math_problems[chat_message.from_jid]["solution"]

            
            if user_answer.isdigit() and int(user_answer) == correct_solution:
                # Correct answer: You can implement your desired logic here
                self.client.send_chat_message(chat_message.group_jid, "Correct! Welcome to the group.")
            else:
                # Incorrect answer: Remove the user from the group
                self.client.remove_peer_from_group(chat_message.group_jid, chat_message.from_jid)
                self.client.send_chat_message(chat_message.group_jid, "Incorrect answer. User removed from the group.")

            # Remove the pending math problem entry
            del self.pending_math_problems[chat_message.from_jid]
        if chat_message.body.lower() == "/ttt":
            self.start_tic_tac_toe_game(chat_message)
        elif chat_message.body.lower().startswith("/move "):
            self.make_tic_tac_toe_move(chat_message) 
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
        # Assuming you want to display the leaderboard when requested
        if command == "/leaderboard":
            leaderboard_message = self.show_leaderboard(group_jid, user_jid)
            self.client.send_chat_message(group_jid, leaderboard_message)
        if chat_message.body.lower() == "gamehelp":
            with open("help3.txt","r") as f:
                self.client.send_chat_message(chat_message.group_jid, f.read())
            return
        if chat_message.body.lower() == "help":
            with open("help.txt","r") as f:
                self.client.send_chat_message(chat_message.group_jid, f.read())
            return
        if chat_message.body.lower() == "friend":
            self.client.add_friend(chat_message.from_jid)
            self.client.send_chat_message(chat_message.from_jid, "You can now add me to groups! <3")
        
        if chat_message.body.lower() == "intro":
            with open("help2.txt","r") as f:
                self.client.send_chat_message(chat_message.group_jid, f.read())
            return    
        
            
        database.add_user_if_not_exists(user_jid, group_jid)

        if group_jid not in self.game_state:
            self.prepare_blackjack_game(group_jid, user_jid)

        in_game = self.game_state[group_jid]['in_game'] if group_jid in self.game_state else False

        if message_body.startswith("/bet "):
            parts = message_body.split()
            if len(parts) == 2 and parts[1].isdigit():
                bet_amount = int(parts[1])
                self.update_user_bet_in_game_state(user_jid, chat_message.group_jid, bet_amount)
                self.client.send_chat_message(group_jid, f"Bet of {bet_amount} chips placed.")
        
                # Start the game with "/sbj" after placing the bet
                if self.has_user_placed_bet(user_jid, group_jid):
                    self.start_blackjack_game(chat_message)
        
        if "/eg" in message_body:
            self.end_blackjack_game(group_jid)

        elif chat_message.body.strip().lower() == "/chips":
            # Ensure the user exists in the database
            database.add_user_if_not_exists(user_jid, group_jid)

            # Ensure the user has a minimum number of chips
            user_chips = database.get_user_chips(user_jid)
            if user_chips == 0:
                database.update_user_chips(user_jid, 1000)  # Set chips to 1000 if current count is 0
                user_chips = 1000  # Update the local variable to reflect the new chip count

            # Send the updated chip count to the user
            self.client.send_chat_message(group_jid, f"Your chip count: {user_chips} chips")
        elif chat_message.body.lower().startswith("/nickname "):
            # Command to set user's nickname
            try:
                _, nickname = chat_message.body.split(maxsplit=1)
                if len(nickname) > 14:
                    self.client.send_chat_message(group_jid, "Hey there,  keep the nickname under 14 characters.")
                elif not re.match("^[A-Za-z0-9]+$", nickname):
                    self.client.send_chat_message(group_jid, "Hey there, hottie! try again ")
                else:
                    database.set_user_nickname(user_jid, nickname)
                    self.client.send_chat_message(group_jid, f"Mmm, well hello there, {nickname}! ")
            except ValueError:
                self.client.send_chat_message(group_jid, "You can set a  nickname using the command /setnickname followed by your preferred nickname. ")
        
        elif in_game and self.game_state[group_jid]['current_phase'] == 'player_turn':
            if "/hit" in message_body:
                self.hit(chat_message)
            elif "/stand" in message_body:
                self.stand(chat_message)
            elif "/double" in message_body:
                self.double_down(chat_message)
        
        if chat_message.body.strip().lower() == "battery":
            battery = psutil.sensors_battery()
            percent = battery.percent
            power_plugged = battery.power_plugged
            plugged = "Plugged In" if power_plugged else "Not Plugged In"
            fig, ax = plt.subplots()
            ax.bar(['Battery'], [percent])
            ax.set_ylim(0, 100)
            ax.set_ylabel('Battery Level (%)')
            info_text = f'Battery level: {percent}%\n({plugged})'
            ax.text(0.5, 0.5, info_text, ha='center', va='center', fontsize=12, transform=ax.transAxes)
            ax.set_title('Battery Status')
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_data = buffer.getvalue()
            self.client.send_chat_image(chat_message.group_jid, image_data)
            plt.close(fig)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'} 
        if chat_message.body.lower().startswith("temp "):
            city = chat_message.body.lower().split(maxsplit=1)[1]
            url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'current' in data and 'temperature' in data['current']:
                    temperature = data['current']['temperature']
                    description = data['current']['weather_descriptions'][0]
                    celsius = float(temperature)
                    fahrenheit = (celsius * 9/5) + 32
                    if celsius <= 32:
                        image_path = 'C:\\\\Users\\alexf\\Desktop\\kik-bot-api-unofficial-new\\examples\\var\\over80.png'
                    elif celsius <= 50:
                        image_path = 'C:\\\\Users\\alexf\\Desktop\\kik-bot-api-unofficial-new\\examples\\var\\over80.png'
                    elif celsius <= 67:
                        image_path = 'C:\\\\Users\\alexf\\Desktop\\kik-bot-api-unofficial-new\\examples\\var\\over80.png'
                    elif celsius <= 79:
                        image_path = 'C:\\\\Users\\alexf\\Desktop\\kik-bot-api-unofficial-new\\examples\\var\\over80.png'
                    else:
                        image_path = 'C:\\\\Users\\alexf\\Desktop\\kik-bot-api-unofficial-new\\examples\\var\\over80.png'
                    image = Image.open(image_path)
                    draw = ImageDraw.Draw(image)
                    font = ImageFont.truetype("arial.ttf", 70)
                    message = f"{city} is {celsius}°C,"
                    fahrenheit_message = f"{celsius}°C is {fahrenheit}°F"
                    text_width, text_height = font.getsize(message)
                    fahrenheit_width, fahrenheit_height = font.getsize(fahrenheit_message)
                    x = (image.width - text_width) / 2
                    y = (image.height - text_height) / 2
                    fahrenheit_x = (image.width - fahrenheit_width) / 2
                    fahrenheit_y = y + text_height
                    # Draw the weather and Fahrenheit text on the image
                    draw.text((x, y), message, font=font, fill=(255, 0, 0))
                    draw.text((fahrenheit_x, fahrenheit_y), fahrenheit_message, font=font, fill=(255, 0, 0))
                    image.save("weather.png")
                    self.client.send_chat_image(chat_message.group_jid, "weather.png")
                else:
                    self.client.send_chat_message(chat_message.group_jid, "Weather data not found for the specified location.")
            else:
                self.client.send_chat_message(chat_message.group_jid, "An error occurred while fetching weather information.")

        if chat_message.body.lower().startswith("chuck"):
            url = "https://api.chucknorris.io/jokes/random"
            response = requests.get(url)
            response_dict = response.json()
            joke = response_dict["value"]
            image_path = 'C:\\\\Users\\alexf\\Desktop\\kik-bot-api-unofficial-new\\examples\\var\\chuck7.jpeg'
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("arial.ttf", 70)
            message_parts = []
            max_width = 25
            words = joke.split()
            line = ''
            for word in words:
                if len(line) + len(word) + 1 <= max_width:
                    line += word + ' '
                else:
                    message_parts.append(line)
                    line = word + ' '
            message_parts.append(line)
            message = '\n'.join(message_parts)
            text_width, text_height = draw.textsize(message, font=font)
            x = (image.width - text_width) / 2
            y = (image.height - text_height) / 2 + 50
            draw.text((x, y), message, font=font, fill=(255, 255, 255))
            image.save("chuck_norris_joke.jpg")
            self.client.send_chat_image(chat_message.group_jid, "chuck_norris_joke.jpg")
        if chat_message.body.lower().startswith("ping"):
            # Define the path to an image file (e.g., 'lmao.jpeg')
            image_path = 'lmao.jpeg'
            # Send the image to the group chat
            self.client.send_chat_image(chat_message.group_jid, image_path)
        if chat_message.body.lower() == "random monkey":
            monkey_image_url = "https://www.placemonkeys.com/500?random"  # 500 is the width, height is automatically adjusted
            # Download the monkey image and save it temporarily
            image_response = requests.get(monkey_image_url)
            if image_response.status_code == 200:
                temp_image_path = 'temp_monkey_image.jpg'
                with open(temp_image_path, 'wb') as image_file:
                    image_file.write(image_response.content)

                # Send the image in the chat
                self.client.send_chat_image(chat_message.group_jid, temp_image_path)

                # Delete the temporary image file
                os.remove(temp_image_path)
            else:
                self.client.send_chat_message(chat_message.group_jid, "Failed to retrieve monkey image.")

        message = str(chat_message.body.lower())        
        if is_user_admin(chat_message.from_jid, chat_message.group_jid):
            is_admin = True
            is_superadmin = False
        else:
            is_admin = False
            is_superadmin = False
        
        if message.startswith("/listsave"):
            is_admin
            responses = self.database.get_word_responses(chat_message.group_jid)
            response_text = "\n".join([f"{word}/{response}" for word, response in responses])
            self.client.send_chat_message(chat_message.group_jid, response_text or "No saved word responses.")
        if message.startswith("/deletesave"):
            is_admin
            if len(command_parts) > 1:
                word_to_delete = command_parts[1]
                result = self.database.delete_word_response(chat_message.group_jid, word_to_delete)
                self.client.send_chat_message(chat_message.group_jid, result)
            else:
                self.client.send_chat_message(chat_message.group_jid, "Please specify a word to delete. Format: /deletesave [word]")
        #View message settings
        if message.startswith("/getw"):
            is_admin
            welcome_message = self.database.get_welcome(chat_message.group_jid)
            if welcome_message:
                self.client.send_chat_message(chat_message.group_jid, f"Welcome message is: {welcome_message}")
            else:
                self.client.send_chat_message(chat_message.group_jid, "No welcome message set.")
        #delete welcome message 
        if message.startswith("/deletew"):
            is_admin
            self.database.delete_welcome(chat_message.group_jid)
            self.client.send_chat_message(chat_message.group_jid, "Welcome message deleted.")
        #Set welcome message
        if message.startswith("/welcome"):
            is_admin
            welcome_message = ' '.join(command_parts[1:])
            self.database.save_welcome(chat_message.group_jid, welcome_message)
            self.client.send_chat_message(chat_message.group_jid, "Welcome message set.")
        
        if message.startswith("ban"):
            is_admin
            username = str(message.replace("ban ", ""))
            self.client.send_chat_message(chat_message.group_jid, "Attempting to ban \"" + username + "\" from the group...")
            try:
                def get_jid(username):
                    try:
                        grab_jid = self.client.get_jid(username)  # Attempts to get the JID
                        return grab_jid
                    except:
                        return False
                jid = get_jid(username)
                attempts = 1
                while jid == False:  # if there was an problem getting the JID, this continues retrying until it works
                    if attempts > 5: # Limits the number of attempts to fetch the JID to 5 so you don't get stuck in an error loop
                        self.client.send_chat_message(chat_message.group_jid,
                                                      "I was unable to get the JID for \"" + username + "\"! Please try again.\n(Make sure the username is valid!)")
                        jid = ""  # Break the while loop
                    else:
                        jid = get_jid(username)  # Tries again
                        attempts = attempts + 1
                self.client.ban_member_from_group(chat_message.group_jid, jid)
                if jid:  # Checks if there is a JID
                    self.client.send_chat_message(chat_message.group_jid)
            except:
                self.client.send_chat_message(chat_message.group_jid, "Ban attempt failed!")
        if message.startswith("unban"):
            is_admin
            username = str(message.replace("unban ", ""))
            self.client.send_chat_message(chat_message.group_jid, "Attempting to unban \"" + username + "\" from the group...")
            try:
                def get_jid(username):
                    try:
                        grab_jid = self.client.get_jid(username)  # Attempts to get the JID
                        return grab_jid
                    except:
                        return False
                jid = get_jid(username)
                attempts = 1
                while jid == False:  # if there was an problem getting the JID, this continues retrying until it works
                    if attempts > 5: # Limits the number of attempts to fetch the JID to 5 so you don't get stuck in an error loop
                        self.client.send_chat_message(chat_message.group_jid,
                                                      "I was unable to get the JID for \"" + username + "\"! Please try again.\n(Make sure the username is valid!)")
                        jid = ""  # Break the while loop
                    else:
                        jid = get_jid(username)  # Tries again
                        attempts = attempts + 1
                self.client.unban_member_from_group(chat_message.group_jid, jid)
                if jid:  # Checks if there is a JID
                    self.client.send_chat_message(chat_message.group_jid)
            except:
                self.client.send_chat_message(chat_message.group_jid)  
        if message.startswith("promote"):
            is_admin
            username = str(message.replace("promote ", ""))
            self.client.send_chat_message(chat_message.group_jid, "Attempting to promote \"" + username + "\" in the group...")
            try:
                def get_jid(username):
                    try:
                        grab_jid = self.client.get_jid(username)  # Attempts to get the JID
                        return grab_jid
                    except:
                        return False
                jid = get_jid(username)
                attempts = 1
                while jid == False:  # if there was an problem getting the JID, this continues retrying until it works
                    if attempts > 5: # Limits the number of attempts to fetch the JID to 5 so you don't get stuck in an error loop
                        self.client.send_chat_message(chat_message.group_jid,
                                                      "I was unable to get the JID for \"" + username + "\"! Please try again.\n(Make sure the username is valid!)")
                        jid = ""  # Break the while loop
                    else:
                        jid = get_jid(username)  # Tries again
                        attempts = attempts + 1
                self.client.promote_to_admin(chat_message.group_jid, jid)
                if jid:  # Checks if there is a JID
                    self.client.send_chat_message(chat_message.group_jid)
            except:
                self.client.send_chat_message(chat_message.group_jid)      
        if message.startswith("kick"):
            is_admin
            username = str(message.replace("kick ", ""))
            self.client.send_chat_message(chat_message.group_jid, "Attempting to kick \"" + username + "\" from the group...")
            try:
                def get_jid(username):
                    try:
                        grab_jid = self.client.get_jid(username)  # Attempts to get the JID
                        return grab_jid
                    except:
                        return False
                jid = get_jid(username)
                attempts = 1
                while jid == False:  # if there was an problem getting the JID, this continues retrying until it works
                    if attempts > 5: # Limits the number of attempts to fetch the JID to 5 so you don't get stuck in an error loop
                        self.client.send_chat_message(chat_message.group_jid,
                                                      "I was unable to get the JID for \"" + username + "\"! Please try again.\n(Make sure the username is valid!)")
                        jid = ""  # Break the while loop
                    else:
                        jid = get_jid(username)  # Tries again
                        attempts = attempts + 1
                self.client.remove_peer_from_group(chat_message.group_jid, jid)
                if jid:  # Checks if there is a JID
                    self.client.send_chat_message(chat_message.group_jid)
            except:
                self.client.send_chat_message(chat_message.group_jid)  
        if message.startswith("/add"):
            is_admin
            username = str(message.replace("add ", ""))
            self.client.send_chat_message(chat_message.group_jid, "Attempting to add \"" + username + "\" to the group...")
            try:
                def get_jid(username):
                    try:
                        grab_jid = self.client.get_jid(username)  # Attempts to get the JID
                        return grab_jid
                    except:
                        return False
                jid = get_jid(username)
                attempts = 1
                while jid == False:  # if there was an problem getting the JID, this continues retrying until it works
                    if attempts > 5: # Limits the number of attempts to fetch the JID to 5 so you don't get stuck in an error loop
                        self.client.send_chat_message(chat_message.group_jid,
                                                      "I was unable to get the JID for \"" + username + "\"! Please try again.\n(Make sure the username is valid!)")
                        jid = ""  # Break the while loop
                    else:
                        jid = get_jid(username)  # Tries again
                        attempts = attempts + 1
                self.client.add_peer_to_group(chat_message.group_jid, jid)
                if jid:  # Checks if there is a JID
                    self.client.send_chat_message(chat_message.group_jid)
            except:
                self.client.send_chat_message(chat_message.group_jid)
        if message.startswith("demote"):
            is_admin 
            username = str(message.replace("demote ", ""))
            self.client.send_chat_message(chat_message.group_jid, "Attempting to demote \"" + username + "\" from the group... bot must be owner")
            try:
                def get_jid(username):
                    try:
                        grab_jid = self.client.get_jid(username)  # Attempts to get the JID
                        return grab_jid
                    except:
                        return False
                jid = get_jid(username)
                attempts = 1
                while jid == False:  # if there was an problem getting the JID, this continues retrying until it works
                    if attempts > 5: # Limits the number of attempts to fetch the JID to 5 so you don't get stuck in an error loop
                        self.client.send_chat_message(chat_message.group_jid,
                                                      "I was unable to get the JID for \"" + username + "\"! Please try again.\n(Make sure the username is valid!)")
                        jid = ""  # Break the while loop
                    else:
                        jid = get_jid(username)  # Tries again
                        attempts = attempts + 1
                self.client.demote_admin(chat_message.group_jid, jid)
                if jid:  # Checks if there is a JID
                    self.client.send_chat_message(chat_message.group_jid)
            except:
                self.client.send_chat_message(chat_message.group_jid)
                
        

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
        elif chat_message.body.lower().startswith("/search "):
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

    
    #Tic Tac Toe game 
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
    def on_sign_up_ended(self, response: RegisterResponse):
        print("[+] Registered as " + response.kik_node)

   
    def on_login_error(self, login_error: LoginError):
        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)

####BLACKJACK
    def show_leaderboard(self, group_jid, user_jid):
        leaderboard_data = database.get_user_leaderboard(group_jid)

        if not leaderboard_data:
            return "No data available for this group."

        leaderboard_text = "Group Leaderboard:\n"

        # Counter for valid entries
        valid_rank = 0

        for (jid, nickname, chips, hm_score) in leaderboard_data:
            # Check if the nickname is not the default value, not empty, and not None
            if nickname != '1000000' and nickname != "" and nickname is not None:
                valid_rank += 1
                display_name = nickname
                leaderboard_text += f"{valid_rank}. {display_name}: {chips} chips\n"

        # Check if user_jid has a nickname set and include it in the leaderboard text
        user_nickname = database.get_user_nickname(user_jid)

        if user_nickname:
            leaderboard_text += f"\nYour nickname: {user_nickname}"

        return leaderboard_text
    def game_help(self, chat_message):
        game_help = (
            "Blackjack Quick Guide:\n\n"
            "LeaderBoard:\n"
            "/nickname <rank name>\n"
            "/leaderboard\n"
            "Game Commands:\n\n /bet <amount> (start game),\n\n /hit (draw card),\n\n /stand (end turn),\n\n "
            "/double (double bet for one card),\n\n /chips (check count),\n\n"
        
            "Goal:\n\n Beat dealer's hand without exceeding 21. Blackjack = 21 points from deal. Tie = bets returned.\n\n"

            "Card Values:\n\n Numbers = face value, Face cards = 10, Aces = 1 or 11.\n\n"

            "Decisions:\n\n 'Hit' if < 11, 'Stand' if ≥ 17.\n 'Double Down' to increase bet with only one more card."
        )
        self.client.send_chat_message(chat_message.group_jid, game_help)
    def initialize_deck(self):
        # Create a standard 52-card deck
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck
    def update_user_bet_in_game_state(self, user_jid, group_jid, bet_amount):
        # Initialize the players entry if it doesn't exist
        if group_jid not in self.game_state:
            self.prepare_blackjack_game(group_jid)

        # Initialize the player's state if it doesn't exist
        if user_jid not in self.game_state[group_jid]['players']:
            self.game_state[group_jid]['players'][user_jid] = {
                'hands': [[]],
                'bet_amount': [],
                'active_hand': 0
            }

        # Update the bet amount for the current active hand
        active_hand_index = self.game_state[group_jid]['players'][user_jid]['active_hand']
        if len(self.game_state[group_jid]['players'][user_jid]['bet_amount']) > active_hand_index:
            self.game_state[group_jid]['players'][user_jid]['bet_amount'][active_hand_index] = bet_amount
        else:
            self.game_state[group_jid]['players'][user_jid]['bet_amount'].append(bet_amount)
    
    def process_bet(self, chat_message, bet_amount):
        user_jid = chat_message.from_jid
        group_jid = chat_message.group_jid

        # Check if the game is in the right phase for betting
        if self.game_state[group_jid]['current_phase'] != 'waiting_for_bets':
            self.client.send_chat_message(group_jid, "In the sexy world of blackjack, you can only place your bets at the start of a thrilling new game. ")
            return

        # Update the game state with the user's bet
        self.game_state[group_jid]['players'][user_jid]['bet_amount'] = bet_amount
        self.game_state[group_jid]['current_phase'] = 'waiting_to_start'
        self.client.send_chat_message(group_jid, f"Bet of {bet_amount} accepted from {user_jid}. Type '/bet' <amount>.")
    def check_and_execute_dealer_play(self, group_jid):
        if self.are_all_hands_finished(group_jid):
            self.dealer_play(group_jid)
    def has_user_placed_bet(self, user_jid, group_jid):
        # Check if the group is in the game state
        if group_jid not in self.game_state:
            return False

        # Check if the user is in the players list of the group
        if user_jid not in self.game_state[group_jid].get('players', {}):
            return False

        # Retrieve the bet amount, defaulting to an empty list if not set
        bet_amounts = self.game_state[group_jid]['players'][user_jid].get('bet_amount', [])

        # Check if any bet in the list is greater than 0
        return any(bet > 0 for bet in bet_amounts)
    def reset_all_games(self):
        try:
            all_group_ids = database.get_all_group_ids()
            for group_id in all_group_ids:
                self.game_state[group_id]['in_game'] = False
                self.game_state[group_id]['current_phase'] = 'waiting_for_bets'
                self.game_state[group_id]['player_hand'] = []
                self.game_state[group_id]['dealer_hand'] = []
                self.game_state[group_id]['deck'] = self.initialize_deck()
            print("All games have been reset.")
        except Exception as e:
            print(f"Error resetting games: {e}")
            print("All games have been reset.")

#cards Code
    def display_card(self, card):
        # Map the suit to its corresponding symbol
        suit_symbols = {
            'Hearts': HEARTS,
            'Diamonds': DIAMONDS,
            'Clubs': CLUBS,
            'Spades': SPADES
        }

        # Retrieve the symbol using the suit of the card
        suit_symbol = suit_symbols.get(card['suit'], '')  # Default to an empty string if the suit is not found

        # Return the formatted string representation of the card
        return f"{card['rank']} {suit_symbol}"
    def draw_hand(self, deck):
        return [self.draw_card(deck), self.draw_card(deck)]    
    def draw_card(self, deck):
        if not deck:
            deck.extend(self.initialize_deck())
        return deck.pop()
    def display_hand(self, hand):
        # Use display_card to get the string representation of each card in the hand
        hand_representation = ", ".join(self.display_card(card) for card in hand)
        print(f"Displaying hand: {hand_representation}")  # Debug print
        return hand_representation
    def display_dealer_hand(self, group_jid):
        # Fetch the first card of the dealer's hand from the game state
        dealer_first_card = self.game_state[group_jid]['dealer_hand'][0]

        # Use the display_card method to get the string representation of the first card
        first_card_display = self.display_card(dealer_first_card)

        # The rest of the dealer's hand is not visible to the player (X)
        return f"{first_card_display},X"
    def dealer_play(self, group_jid):
        if not self.are_all_hands_finished(group_jid):
            return  # Return early if any player hand is still active

        dealer_hand = self.game_state[group_jid]['dealer_hand']
        deck = self.game_state[group_jid]['deck']

        while self.calculate_score(dealer_hand) < 17:
            if not deck:
                deck.extend(self.initialize_deck())
                random.shuffle(deck)

            new_card = self.draw_card(deck)
            dealer_hand.append(new_card)

        self.game_state[group_jid]['dealer_hand'] = dealer_hand
        # After dealer play, determine winner for all hands
        for user_jid in self.game_state[group_jid]['players']:
            winner_message = self.determine_winner(group_jid, user_jid)
            self.client.send_chat_message(group_jid, winner_message)
        self.end_blackjack_game(group_jid)  # End the game after dealer's turn

        # Update dealer's hand in game state
        self.game_state[group_jid]['dealer_hand'] = dealer_hand
    def are_all_hands_finished(self, group_jid):
        for player in self.game_state[group_jid]['players'].values():
            if player['active_hand'] < len(player['hands']):
                return False
        return True
    def calculate_score(self, hand):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        score = sum(values[card['rank']] for card in hand)
        num_aces = sum(1 for card in hand if card['rank'] == 'A')
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        return score
    def end_blackjack_game(self, group_jid):
        if group_jid in self.game_state:
            # Reset the game state
            self.game_state[group_jid]['in_game'] = False
            self.game_state[group_jid]['current_phase'] = 'waiting_for_bets'
            self.game_state[group_jid]['deck'] = self.initialize_deck()
            self.game_state[group_jid]['dealer_hand'] = []

            # Reset each player's state in this group
            for user_jid in self.game_state[group_jid]['players']:
                self.game_state[group_jid]['players'][user_jid] = {
                    'hands': [[]],
                    'bet_amount': [],
                    'active_hand': 0
                }
        else:
            logging.warning(f"Group ID {group_jid} not found in game state.")
    def prepare_blackjack_game(self, group_jid, user_jid):
        # Initial setup for the game state
        self.game_state[group_jid] = {
            'in_game': False,
            'game_starter_jid': user_jid,
            'deck': self.initialize_deck(),
            'player_hand': [],  # This might be deprecated if using 'hands' in 'players'
            'dealer_hand': [],
            'current_phase': 'waiting_for_bet',
            'players': {}  # Initialize an empty dictionary for players
        }

        # Setup for each player
        self.game_state[group_jid]['players'][user_jid] = {
            'hands': [[]],  # A list of hands, each hand is a list of cards
            'bet_amount': [],  # Initially empty, will be filled when the player places a bet
            'active_hand': 0,  # Index of the currently active hand
            'group_jid': group_jid  # Set the group_jid for the user
        }
    def start_blackjack_game(self, chat_message):
        group_jid = chat_message.group_jid
        user_jid = chat_message.from_jid

        # Ensure the game state for this group is initialized
        if group_jid not in self.game_state:
            self.prepare_blackjack_game(group_jid, user_jid)

        # Check if a game is already in progress
        if self.game_state[group_jid]['in_game']:
            self.client.send_chat_message(group_jid, "A game is already in progress. Finish it before starting a new one.")
            return

        # Check the user's bet for this specific group
        bet_amounts = self.game_state[group_jid]['players'][user_jid].get('bet_amount', [])
        user_chips = database.get_user_chips(user_jid)

        # Check if at least one bet is placed and the user has enough chips
        if bet_amounts and all(bet <= user_chips for bet in bet_amounts):
            print(group_jid,(f"User Chips Before Deduction: {user_chips}"))
            for bet in bet_amounts:
                database.subtract_chips_from_user(user_jid, bet)
                user_chips_after_deduction = database.get_user_chips(user_jid)
                print(group_jid,(f"User Chips After Deduction: {user_chips_after_deduction}"))
            self.start_new_blackjack_round(group_jid, user_jid)
        else:
            self.client.send_chat_message(group_jid, "Please place a bet using '/bet <amount>'")
    
    def start_new_blackjack_round(self, group_jid, user_jid):
        # Set the game as in progress for this group
        self.game_state[group_jid]['in_game'] = True
        self.game_state[group_jid]['deck'] = self.initialize_deck()
        self.game_state[group_jid]['players'][user_jid]['hands'] = [self.draw_hand(self.game_state[group_jid]['deck'])]
        self.game_state[group_jid]['dealer_hand'] = self.draw_hand(self.game_state[group_jid]['deck'])
        self.game_state[group_jid]['current_phase'] = 'player_turn'

        # Send game details to the group chat
        game_message = "BlackJack Game Started\n"
        game_message += f"Dealer's Hand: {self.display_card(self.game_state[group_jid]['dealer_hand'][0])},X\n"
        game_message += f"Your Hand: {self.display_hand(self.game_state[group_jid]['players'][user_jid]['hands'][0])}\n"
        game_message += "Type '/hit' or '/stand' or '/double'."
        self.client.send_chat_message(group_jid, game_message)
    def stand(self, chat_message):
        group_jid = chat_message.group_jid
        if not self.game_state[group_jid]['in_game']:
            self.client.send_chat_message(group_jid, "No active blackjack game. Start one with /bj.")
            return

        self.dealer_play(group_jid)
        winner_message = self.determine_winner(group_jid, chat_message.from_jid)
        self.client.send_chat_message(group_jid, winner_message)
        self.end_blackjack_game(group_jid)  # Reset the game state
    def hit(self, chat_message):
        group_jid = chat_message.group_jid
        user_jid = chat_message.from_jid

        # Check if a blackjack game is active
        if not self.game_state[group_jid]['in_game']:
            self.client.send_chat_message(group_jid, "No active blackjack game. Start one with /bet <amount>.")
            return

        # Access the game deck and the player's current hand
        deck = self.game_state[group_jid]['deck']
        player_hand = self.game_state[group_jid]['players'][user_jid]['hands'][0]

        # Draw a new card and append it to the active hand
        new_card = self.draw_card(deck)
        player_hand.append(new_card)

        # Display the dealer's first card and a placeholder for the second card
        dealer_first_card = self.game_state[group_jid]['dealer_hand'][0]
        dealer_hand_display = f"Dealer's Hand: {self.display_card(dealer_first_card)}, Face Down"

        # Display the updated player hand
        player_hand_display = f"Your Hand: {self.display_hand(player_hand)}"

        # Check if player busts
        if self.calculate_score(player_hand) > 21:
            game_message = f"{dealer_hand_display}\n{player_hand_display}\nBusted!"
            self.client.send_chat_message(group_jid, game_message)

            # Determine the winner (or in this case, the loss)
            winner_message = self.determine_winner(group_jid, user_jid)
            self.client.send_chat_message(group_jid, winner_message)

            # End and reset the game
            self.end_blackjack_game(group_jid)
        else:
            game_message = f"{dealer_hand_display}\n{player_hand_display}\nOptions: /hit, /stand"
            self.client.send_chat_message(group_jid, game_message)
    def double_down(self, chat_message):
        user_jid = chat_message.from_jid
        group_jid = chat_message.group_jid

        if self.game_state[group_jid]['in_game']:
            player = self.game_state[group_jid]['players'][user_jid]
            active_hand = player['hands'][player['active_hand']]

            # Validate if the player can double down (only with two cards in hand)
            if len(active_hand) == 2:
                bet_amount = player['bet_amount'][player['active_hand']]

                if database.get_user_chips(user_jid) >= bet_amount:
                    # Double the bet and update the bet amount in the game state
                    doubled_bet_amount = 2 * bet_amount
                    player['bet_amount'][player['active_hand']] = doubled_bet_amount

                    # Deduct the additional bet amount from the user's chips
                    database.subtract_chips_from_user(user_jid, bet_amount)

                    new_card = self.draw_card(self.game_state[group_jid]['deck'])
                    active_hand.append(new_card)

                    # Check for bust after drawing the new card
                    if self.calculate_score(active_hand) > 21:
                        # Player is busted, end the game
                        self.client.send_chat_message(group_jid, f"Doubled down. Busted with hand: {self.display_hand(active_hand)}")
                        winner_message = self.determine_winner(group_jid, user_jid)
                        self.client.send_chat_message(group_jid, winner_message)
                        self.end_blackjack_game(group_jid)
                    else:
                        # Continue the game
                        self.client.send_chat_message(group_jid, f"Doubled down. Your new hand: {self.display_hand(active_hand)}")
                    
                        # If it's the last hand, proceed to dealer play
                        if player['active_hand'] + 1 >= len(player['hands']):
                            self.dealer_play(group_jid)
                            winner_message = self.determine_winner(group_jid, user_jid)
                            self.client.send_chat_message(group_jid, winner_message)
                            self.end_blackjack_game(group_jid)
                else:
                    self.client.send_chat_message(group_jid, "You do not have enough chips to double down.")
            else:
                self.client.send_chat_message(group_jid, "Can only double down at the start of your turn with two cards.")

    def place_bet(self, chat_message, bet_amount):
        user_jid = chat_message.from_jid
        group_jid = chat_message.group_jid

        # Check if the user has enough chips to place the bet
        user_chips = database.get_user_chips(user_jid)
        if user_chips is None:
            user_chips = self.DEFAULT_BET_AMOUNT  # Assign a default chip count if the user has no record yet

        if bet_amount > 0 and user_chips >= bet_amount:
            # Deduct the bet amount from the user's chips
            database.subtract_chips_from_user(user_jid, bet_amount)

            # Update the game state with the bet amount
            self.update_user_bet_in_game_state(user_jid, group_jid, bet_amount)

            # Inform the user that the bet has been placed
            self.client.send_chat_message(group_jid, f"Bet of {bet_amount} chips placed. Your remaining chips: {user_chips - bet_amount}")
        else:
            # Inform the user they don't have enough chips to place the bet
            self.client.send_chat_message(group_jid, "Invalid bet amount or insufficient chips.")
    
    
    def determine_winner(self, group_jid, user_jid):
        player_hands = self.game_state[group_jid]['players'][user_jid]['hands']
        dealer_hand = self.game_state[group_jid]['dealer_hand']
        dealer_score = self.calculate_score(dealer_hand)
        dealer_hand_display = self.display_hand(dealer_hand)
        overall_outcome = ""

        for i, player_hand in enumerate(player_hands):
            bet_amount = self.game_state[group_jid]['players'][user_jid]['bet_amount'][i]
            player_score = self.calculate_score(player_hand)
            player_hand_display = self.display_hand(player_hand)

            if player_score > 21:
                # Player busted, subtract bet amount
                outcome = f"Busted!\nYour Hand: {player_hand_display}\nDealer's Hand: {dealer_hand_display}\nAmount Lost: {bet_amount}"
            elif dealer_score > 21 or player_score > dealer_score:
                # Player wins, add winnings
                winnings = bet_amount * 2  # Corrected winnings calculation
                database.add_chips_to_user(user_jid, winnings + bet_amount)  # Add both original bet and winnings
                outcome = f"You win!\nYour Hand: {player_hand_display}\nDealer's Hand: {dealer_hand_display}\nWinnings: {winnings}"
            elif dealer_score > player_score:
                # Dealer wins, subtract bet amount
                outcome = f"Dealer wins.\nDealer's Hand: {dealer_hand_display}\nAmount Lost: {bet_amount}"
            else:
                # It's a tie, return the bet amount
                database.add_chips_to_user(user_jid, bet_amount)  # Add the original bet back
                outcome = f"It's a tie!\nYour Hand: {player_hand_display}\nDealer's Hand: {dealer_hand_display}"

            overall_outcome += outcome + "\n"

        # Get and display the new chip count
        new_chip_count = database.get_user_chips(user_jid)
        overall_outcome += f"Your new chip count: {new_chip_count}"

        return overall_outcome

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
                    "3z35fdyojlaevnmvauode3s2gg2jxgou2plb3l4bec3hbqiifbaa_a@talk.kik.com",
                    "lpxs22qlsmljkc3g5c2kppndfl7luczdkoowoq46oynsclseqpkq_a@talk.kik.com",
                    "blrwrc2qiswvmx2wkyhoincphsarb3yktjeqsnsp7nhamuihodha_a@talk.kik.com,"
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

    def on_peer_info_received(self, response: PeersInfoResponse):
        users = '\n'.join([str(member) for member in response.users])
        print(f'Peer info: {users}')

    # Listener for when Peer Info received through Xiphias request.
    def on_xiphias_get_users_response(self, response: Union[UsersResponse, UsersByAliasResponse]):
        users = '\n'.join([str(member) for member in response.users])
        print(f'Peer info: {users}')

if __name__ == '__main__':
    main()
    creds_file = "creds.json"
    if not os.path.isfile(creds_file):
        os.chdir("creditjson path")
    with open(creds_file) as f:
        creds = json.load(f)
    callback = EchoBot(creds, database)
    
    
