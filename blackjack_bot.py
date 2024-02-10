import logging
import sqlite3
import threading

class BlackjackDatabase:
    def __init__(self, db_path, table_suffix):
        self.db_path = db_path
        self.table_suffix = table_suffix
        self.lock = threading.Lock()
        self.setup_database()
        self.user_data = {}  # Dictionary to store user data

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys=ON")
            return conn
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
            return None

    def setup_database(self):
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    user_chips_table_name = f"user_chips_{self.table_suffix}"
                    group_state_table_name = f"group_blackjack_state_{self.table_suffix}"

                    # Create user_chips table with additional columns if they do not exist
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {user_chips_table_name} (
                            jid TEXT PRIMARY KEY,
                            chips INTEGER NOT NULL DEFAULT 1000000,
                            bet_amount INTEGER DEFAULT 0,
                            nickname TEXT,
                            group_jid TEXT,
                            scramble_score INTEGER DEFAULT 0
                        );
                    """)

                    

                    # Create group_blackjack_state table if it doesn't exist
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {group_state_table_name} (
                            group_id TEXT PRIMARY KEY
                        );
                    """)

                    conn.commit()
            except sqlite3.Error as e:
                logging.error(f"Error setting up database: {e}")
   
    # Rest of the methods...
    def set_user_nickname(self, jid, nickname):
        table_name = f"user_chips_{self.table_suffix}"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE {table_name} SET nickname = ? WHERE jid = ?", (nickname, jid))
                    conn.commit()
                    logging.info(f"Nickname set for {jid}: {nickname}")
                
                    # Update user data in the dictionary
                    if jid in self.user_data:
                        self.user_data[jid]['nickname'] = nickname
            except sqlite3.Error as e:
                logging.error(f"Error setting nickname for {jid}: {e}")
    
    def get_nickname_scramble_leaderboard(self, group_jid):
        table_name = f"user_chips_{self.table_suffix}"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    # Fetching the nickname and scramble score along with user details
                    cursor.execute(f"SELECT jid, nickname, scramble_score FROM {table_name} WHERE group_jid=?", (group_jid,))
                    leaderboard_data = cursor.fetchall()
                    # Sorting the leaderboard data based on scramble score
                    leaderboard_data.sort(key=lambda x: x[2], reverse=True)  # Sorting by scramble score
                    return leaderboard_data
            except sqlite3.Error as e:
                logging.error(f"Error in get_nickname_scramble_leaderboard: {e}")
        return []
    def update_scramble_score(self, jid, increment=1):
        table_name = f"user_chips_{self.table_suffix}"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE {table_name} SET scramble_score = scramble_score + ? WHERE jid = ?", (increment, jid))
                    conn.commit()
            except sqlite3.Error as e:
                logging.error(f"Error updating scramble score for {jid}: {e}")
    
    def get_user_leaderboard(self, group_jid):
        table_name = f"user_chips_{self.table_suffix}"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    # Fetching the scramble score along with other user details
                    cursor.execute(f"SELECT jid, nickname, chips, scramble_score FROM {table_name} WHERE group_jid=?", (group_jid,))
                    leaderboard_data = cursor.fetchall()
                    # Filter out entries with default nickname values
                    filtered_leaderboard = [(jid, nickname, chips, scramble_score) for jid, nickname, chips, scramble_score in leaderboard_data if nickname != '1000000']
                    # Sorting the filtered leaderboard data based on your preference
                    filtered_leaderboard.sort(key=lambda x: (x[2], x[3]), reverse=True)  # Example: Sorting by chips and then by scramble score
                    return filtered_leaderboard
            except sqlite3.Error as e:
                logging.error(f"Error in get_user_leaderboard: {e}")
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
    def get_user_nickname(self, jid):
        if jid in self.user_data:
            return self.user_data[jid]['nickname']
        return None

    def get_all_group_ids(self):
        with self.lock:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                group_state_table_name = f"group_blackjack_state_{self.table_suffix}"
                cursor.execute(f"SELECT DISTINCT group_id FROM {group_state_table_name}")
                groups = cursor.fetchall()
                return [group[0] for group in groups]
    def add_user_if_not_exists(self, from_jid, group_jid):
        initial_chips = 1000000
        table_name = f"user_chips_{self.table_suffix}"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"INSERT OR IGNORE INTO {table_name} (jid, chips, group_jid) VALUES (?, ?, ?)", (from_jid, initial_chips, group_jid))
                    conn.commit()
                    logging.info(f"User {from_jid} added or already exists in the database for group {group_jid}.")
            except sqlite3.Error as e:
                logging.error(f"Error in add_user_if_not_exists for {from_jid}: {e}")
    def reset_all_bets(self, group_jid):
        table_name = f"user_chips_{self.table_suffix}"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE {table_name} SET bet_amount = 0 WHERE group_jid = ?", (group_jid,))
                    conn.commit()
                    logging.info(f"All bets reset for group {group_jid}.")
            except sqlite3.Error as e:
                logging.error(f"Error resetting bets for group {group_jid}: {e}")

    def get_user_chips(self, jid):
        table_name = f"user_chips_{self.table_suffix}"
        with self.lock:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT chips FROM {table_name} WHERE jid = ?", (jid,))
                result = cursor.fetchone()
                return result['chips'] if result else 0

    def update_user_chips(self, jid, chips):
        table_name = f"user_chips_{self.table_suffix}"
        with self.lock:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE {table_name} SET chips = ? WHERE jid = ?", (chips, jid))
                conn.commit()

    def update_user_chips_and_bet(self, jid, chips, bet_amount):
        table_name = f"user_chips_{self.table_suffix}"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE {table_name} SET chips = ?, bet_amount = ? WHERE jid = ?", (chips, bet_amount, jid))
                    conn.commit()
            except sqlite3.Error as e:
                logging.error(f"Error updating chips and bet for {jid}: {e}")
    
    def add_chips_to_user(self, jid, chips_to_add):
        if not isinstance(chips_to_add, int):
            try:
                chips_to_add = int(chips_to_add)
            except ValueError:
                raise ValueError("chips_to_add must be an integer")

        table_name = f"user_chips_{self.table_suffix}"
        with self.lock:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE {table_name} SET chips = chips + ? WHERE jid = ?", (chips_to_add, jid))
                conn.commit()

    def subtract_chips_from_user(self, jid, chips_to_subtract):
        table_name = f"user_chips_{self.table_suffix}"
        with self.lock:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT chips FROM {table_name} WHERE jid = ?", (jid,))
                result = cursor.fetchone()
                if result:
                    current_chips = result['chips']
                    new_chips = max(current_chips - chips_to_subtract, 0)
                    cursor.execute(f"UPDATE {table_name} SET chips = ? WHERE jid = ?", (new_chips, jid))
                    conn.commit()

    def set_user_bet(self, jid, bet_amount):
        if bet_amount < 0:
            logging.warning(f"Attempt to set a negative bet amount for {jid}: {bet_amount}")
            return

        table_name = f"user_chips_{self.table_suffix}"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE {table_name} SET bet_amount = ? WHERE jid = ?", (bet_amount, jid))
                    conn.commit()
                    logging.info(f"Bet set for {jid}: {bet_amount}")
            except sqlite3.Error as e:
                logging.error(f"Error setting bet for {jid}: {e}")

    def get_user_bet(self, jid):
        table_name = f"user_chips_{self.table_suffix}"
        try:
            with self.lock:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT bet_amount FROM {table_name} WHERE jid = ?", (jid,))
                    result = cursor.fetchone()
                    if result:
                        bet_amount = result['bet_amount']
                        print(f"Retrieved bet amount for {jid}: {bet_amount}")
                        return bet_amount
                    else:
                        print(f"No bet found for {jid}")
                        return 0
        except Exception as e:
            print(f"Error retrieving bet for {jid}: {e}")
            return 0
    def reset_jackpot(self, group_jid, winner_jid=None, amount_to_add=0):
        try:
            if winner_jid is not None:
                # Someone won the jackpot, reset it to 0
                self.update_jackpot_amount(group_jid, 0)
            else:
                # No winner, just add the specified amount to the current jackpot
                current_jackpot = self.get_jackpot_amount(group_jid)
                new_amount = current_jackpot + amount_to_add
                self.update_jackpot_amount(group_jid, new_amount)
        except sqlite3.Error as e:
            print(f"Error updating jackpot amount for group {group_jid}: {e}")

    def get_jackpot_amount(self, group_jid):
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT amount FROM jackpot WHERE group_jid = ?", (group_jid,))
                result = cursor.fetchone()
                return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"Error retrieving jackpot amount for group {group_jid}: {e}")
            return 0
    def add_lost_chips_to_jackpot(self, group_jid, amount):
        table_name = "jackpot"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE {table_name} SET amount = amount + ? WHERE group_jid = ?", (amount, group_jid))
                    conn.commit()
            except sqlite3.Error as e:
                logging.error(f"Error updating jackpot amount for group {group_jid}: {e}")
    def update_jackpot_amount(self, group_jid, new_amount):
        table_name = "jackpot"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE {table_name} SET amount = ? WHERE group_jid = ?", (new_amount, group_jid))
                    conn.commit()
            except sqlite3.Error as e:
                logging.error(f"Error updating jackpot amount for group {group_jid}: {e}")
   
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
