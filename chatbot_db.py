import logging
import sqlite3

class ChatbotDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('bot_data.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.initialize_database()

    def initialize_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS welcomes (
                               group_id TEXT PRIMARY KEY,
                               welcome_message TEXT
                           )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS word_responses (
                           group_id TEXT,
                           word TEXT,
                           response TEXT
                       )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_chips (
                           user_id TEXT PRIMARY KEY,
                           chips INTEGER DEFAULT 0
                       )''')
        self.connection.commit()

    def initialize_jackpot(self, group_jid, initial_amount=0):
        try:
            # Check if the group_jid already exists in the database
            self.cursor.execute("SELECT group_jid FROM jackpot WHERE group_jid = ?", (group_jid,))
            result = self.cursor.fetchone()

            if not result:
                # If the group_jid doesn't exist, insert it
                self.cursor.execute("INSERT INTO jackpot (group_jid, amount) VALUES (?, ?)", (group_jid, initial_amount))
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error initializing jackpot for group {group_jid}: {e}")
    
    def get_custom_command_response(self, group_id, word):
        try:
            self.cursor.execute("SELECT response FROM word_responses WHERE group_id = ? AND word = ?", (group_id, word))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error retrieving word response: {e}")
            return None
    def save_word_response(self, group_id, word, response):
        try:
            print(f"Saving word response: Group ID: {group_id}, Word: {word}, Response: {response}")
            print(f"Types - Group ID: {type(group_id)}, Word: {type(word)}, Response: {type(response)}")
            self.cursor.execute("INSERT INTO word_responses (group_id, word, response) VALUES (?, ?, ?)",
                                (group_id, word, response))
            self.connection.commit()
            return "Word response saved successfully."
        except Exception as e:
            return f"Error saving word response: {e}"

    def get_word_responses(self, group_id):
        try:
            self.cursor.execute("SELECT word, response FROM word_responses WHERE group_id = ?", (group_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving word responses: {e}")
            return []

    def delete_word_response(self, group_id, word):
        try:
            self.cursor.execute("DELETE FROM word_responses WHERE group_id = ? AND word = ?", (group_id, word))
            self.connection.commit()
            if self.cursor.rowcount == 0:
                print(f"No word response found to delete for word '{word}' in group '{group_id}'.")
                return "No such word response found to delete."
            print(f"Deleted word response '{word}' successfully for group '{group_id}'.")
            return "Word response deleted successfully."
        except Exception as e:
            print(f"Error deleting word response: {e}")
            return f"Error deleting word response: {e}"
    def save_welcome(self, group_id, text):
        try:
            text = text.replace('"', "\DQUOTE")
            self.cursor.execute("INSERT INTO welcomes (group_id, welcome_message) VALUES (?, ?)", (group_id, text))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_welcome(self, group_id):
        try:
            self.cursor.execute("SELECT welcome_message FROM welcomes WHERE group_id = ?", (group_id,))
            row = self.cursor.fetchone()
            if row:
                return row[0].replace('\DQUOTE', '"')
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return "An error occurred while retrieving the welcome message."
        # No need for finally block to close connection, as we're using a single persistent connection

    def delete_welcome(self, group_id):
        try:
            self.cursor.execute("DELETE FROM welcomes WHERE group_id = ?", (group_id,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    

    def get_user_chips(self, user_id):
        try:
            self.cursor.execute("SELECT chips FROM user_chips WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"Error retrieving user chips: {e}")
            return 0

    def update_user_chips(self, user_id, chips):
        try:
            self.cursor.execute("INSERT OR REPLACE INTO user_chips (user_id, chips) VALUES (?, ?)", (user_id, chips))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating user chips: {e}")

    def add_chips_to_user(self, user_id, chips_to_add):
        try:
            current_chips = self.get_user_chips(user_id)
            new_chips = current_chips + chips_to_add
            self.update_user_chips(user_id, new_chips)
        except sqlite3.Error as e:
            print(f"Error adding chips to user: {e}")

    def subtract_chips_from_user(self, user_id, chips_to_subtract):
        try:
            current_chips = self.get_user_chips(user_id)
            if current_chips >= chips_to_subtract:
                new_chips = current_chips - chips_to_subtract
                self.update_user_chips(user_id, new_chips)
            else:
                print("Insufficient chips to subtract.")
        except sqlite3.Error as e:
            print(f"Error subtracting chips from user: {e}")

    def get_custom_commands(self, group_id):
        try:
            self.cursor.execute("SELECT trigger, response FROM custom_commands WHERE group_id = ?", (group_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving custom commands: {e}")
            return []
    def get_user_nickname_from_db(self, jid):
        table_name = f"user_chips_{self.table_suffix}"
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT nickname FROM {table_name} WHERE jid = ?", (jid,))
                result = cursor.fetchone()
                return result[0] if result else None
        except sqlite3.Error as e:
            logging.error(f"Error fetching nickname for {jid}: {e}")
            return None
    def get_jackpot_amount(self, group_jid):
        try:
            self.cursor.execute("SELECT amount FROM jackpot WHERE group_jid = ?", (group_jid,))
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"Error retrieving jackpot amount for group {group_jid}: {e}")

    def update_jackpot_amount(self, group_jid, amount):
        try:
            # Check if a row with the given group_jid exists
            self.cursor.execute("SELECT 1 FROM jackpot WHERE group_jid = ?", (group_jid,))
            result = self.cursor.fetchone()

            if result:
                # If the row exists, update the jackpot amount
                self.cursor.execute("UPDATE jackpot SET amount = ? WHERE group_jid = ?", (amount, group_jid))
            else:
                # If the row doesn't exist, insert a new row
                self.cursor.execute("INSERT INTO jackpot (group_jid, amount) VALUES (?, ?)", (group_jid, amount))

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating jackpot amount for group {group_jid}: {e}")

    def reset_jackpot(self, group_jid):
        try:
            # Get the current jackpot for the group
            current_jackpot = self.get_jackpot_amount(group_jid)

            # Store the current jackpot in the database (optional, if needed)
            self.update_jackpot_amount(group_jid, current_jackpot)

            # Reset the jackpot for the group to 0
            self.update_jackpot_amount(group_jid, 0)
        except sqlite3.Error as e:
            print(f"Error resetting jackpot amount for group {group_jid}: {e}")

    def close(self):
        try:
            if self.connection:
                self.connection.close()
        except sqlite3.Error as e:
            print(f"Error closing the database connection: {e}")