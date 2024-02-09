import logging
import sqlite3
import time
import random
import string

def randomString(length):
    return ''.join(random.choice(string.ascii_uppercase) for i in range(length))

def check_captchas(client, bot):
    print(f"({bot}) Captcha checks started.")
    while True:
        conn = sqlite3.connect('db.sqlite3')
        curr = conn.cursor()
        curr.execute('SELECT * FROM captchas WHERE (bot=?)', (bot,))
        query = curr.fetchall()

        for captcha in query:
            if (int(time.time()) - int(captcha[3])) > 120:
                curr.execute('DELETE FROM captchas WHERE (jid=?)', (captcha[0],))
                conn.commit()
                client.remove_peer_from_group(captcha[4], captcha[0])

        time.sleep(30)

def clear_captchas():
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute('DELETE FROM captchas')
    conn.commit()
    conn.close()

def ping_captcha(jid, message):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM captchas WHERE (jid=?)', (jid,))
    query = curr.fetchall()

    try:
        if str(query[0][1]) in message and len(message) < 5:
            curr.execute(f'DELETE FROM captchas WHERE (jid=?)', (jid,))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False
    except IndexError:
        pass

def enable_captcha(group_jid):
    try:
        conn = sqlite3.connect('db.sqlite3')
        curr = conn.cursor()
        curr.execute(f'UPDATE groups SET captcha = "True" WHERE (group_id = ?)', (group_jid,))
        conn.commit()
        conn.close()
        print(f"Captcha enabled for group: {group_jid}")
    except Exception as e:
        print(f"Error enabling captcha: {e}")

def disable_captcha(group_jid):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'UPDATE groups SET captcha = "False" WHERE (group_id = ?)', (group_jid,))
    conn.commit()
    conn.close()

def make_captcha(jid, group, bot):
    vars = []
    vars.append(random.randint(0, 10))
    vars.append(random.randint(0, 10))
    sol = vars[0] + vars[1]
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'INSERT INTO captchas VALUES (?,?,?,?,?)', (jid, sol, bot, int(time.time()), group))
    conn.commit()
    conn.close()
    return vars


def save_user(alias, jid):
    if get_user(alias) == False:
        conn = sqlite3.connect('db.sqlite3')
        curr = conn.cursor()
        curr.execute(f'INSERT INTO namebase VALUES (?,?)', (alias, jid))
        conn.commit()
        conn.close()

def get_user(alias):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM namebase WHERE (alias=?)', (alias,))
    query = curr.fetchall()
    conn.close()

    if query != []:
        return query[0][1]
    else:
        return False



def get_censored(group_jid):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM censored WHERE (group_jid = ?)', (group_jid,))
    query = curr.fetchall()
    conn.close()

    censored = []
    for q in query:
        censored.append(q[1])
    return censored

def censor(group_jid, word):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'INSERT INTO censored VALUES (?,?)', (group_jid, word.lower()))
    conn.commit()
    conn.close()

def uncensor(group_jid, word):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'DELETE FROM censored WHERE (group_jid = ? AND word = ?)', (group_jid, word.lower()))
    conn.commit()
    conn.close()

def is_censored(group_jid, message):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM censored WHERE (group_jid = ?)', (group_jid,))
    query = curr.fetchall()
    conn.close()

    for q in query:
        if q[1] in message.lower():
            return True
    return False

def add_trigger(group_jid, trigger, response):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    trigger = trigger.replace('"',"\DQUOTE")
    response = response.replace('"',"\DQUOTE")
    curr.execute(f'INSERT INTO triggers VALUES (?,?,?)', (group_jid, trigger.lower(), response))
    conn.commit()
    conn.close()

def remove_trigger(group_jid, trigger):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    trigger = trigger.replace('"',"\DQUOTE")
    curr.execute(f'DELETE FROM triggers WHERE (group_jid = ? AND trigger = ?)', (group_jid, trigger.lower()))
    conn.commit()
    conn.close()

def is_trigger(group_jid, message):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    message = message.replace('"',"\DQUOTE")
    curr.execute(f'SELECT * FROM triggers WHERE (trigger=? AND group_jid=?)', (message.lower(), group_jid))
    query = curr.fetchall()
    conn.close()

    if query != []:
        return query[0][2].replace('\DQUOTE','"')
    else:
        return False

def ensure_bot(username):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()

    curr.execute(f'SELECT 1 FROM groupcounts WHERE username=?', (username,))
    query = curr.fetchone()

    if query == None:
        curr.execute('INSERT INTO groupcounts VALUES (?, 0)', (username,))
        conn.commit()
    conn.close()
    return

def get_bot_groupcount(username):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM groupcounts where username=?', (username,))
    query = curr.fetchall()
    conn.close()

    return query[0][1]

def compare_groupcounts(username):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM groupcounts')
    bots = curr.fetchall()
    conn.close()

    smallest_bot = username
    smallest_count = get_bot_groupcount(username)
    for bot in bots:
        if bot[1]+10 < smallest_count:
            smallest_bot = bot[0]
    return smallest_bot

def add_to_groupcount(username):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM groupcounts where username=?', (username,))
    bot = curr.fetchall()

    count = bot[0][1]
    curr.execute(f'UPDATE groupcounts SET count = ? WHERE (username = ?)', (int(count)+1, username))
    conn.commit()
    conn.close()

def remove_from_groupcount(username):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM groupcounts where username=?', (username,))
    bot = curr.fetchall()

    count = bot[0][1]
    curr.execute(f'UPDATE groupcounts SET count = ? WHERE (username = ?)', (int(count)-1, username))
    conn.commit()
    conn.close()

def group_data_exists(group_id):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT 1 FROM groups WHERE group_id=?', (group_id,))
    query = curr.fetchone()
    conn.close()

    if query == None:
        return False
    else:
        return True

def get_cooldown(group_id):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM groups WHERE group_id=?', (group_id,))
    rows = curr.fetchall()
    conn.close()
    return rows[0][4]

def update_cooldown(group_id):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'UPDATE groups SET cooldown = ? WHERE (group_id = ?)', (int(time.time()), group_id))
    conn.commit()
    conn.close()

def get_group_settings(group_id):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM groups WHERE group_id=?', (group_id,))
    rows = curr.fetchall()
    conn.close()
    
    if rows:
        return rows[0]
    else:
        # Handle the case where no rows were found in the database
        return None  # Or any other appropriate value or action

# Rest of your code

def add_admin(group_id, user_id):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'INSERT INTO admins VALUES (?, ?)', (group_id, user_id))
    conn.commit()
    conn.close()

def remove_admin(group_id, user_id):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'DELETE FROM admins WHERE (group_id = ? AND user_id = ?)', (group_id, user_id))
    conn.commit()
    conn.close()

logging.basicConfig(level=logging.DEBUG)

def is_user_admin(user_id, group_id):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM admins WHERE (user_id=? AND group_id = ?)', (user_id, group_id))
    rows = curr.fetchall()

    conn.close()

    if rows == []:
        return False
    else:
        return True
# Call the function to create the table when your script/module initializes
create_admins_table()
def get_admins(group_id):
    with sqlite3.connect('db.sqlite3') as conn:
        curr = conn.cursor()
        curr.execute('SELECT * FROM admins WHERE group_id=?', (group_id,))
        rows = curr.fetchall()

    if not rows:
        return "No admins found in this group."

    admin_list = "List of Admins:\n"
    for row in rows:
        admin_list += f"- {row[1]}\n"  # Assuming row[1] contains the admin's name or identifier

    return admin_list
def save_welcome(group_id, text, toggle=True):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    text = text.replace('"', "\DQUOTE")
    curr.execute(f'INSERT INTO welcomes VALUES (?, ?, ?)', (group_id, text, toggle))
    conn.commit()
    conn.close()

def get_welcome(group_id):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM welcomes WHERE (group_id=?)', (group_id,))
    rows = curr.fetchall()
    conn.close()

    try:
        return rows[0][1].replace('\DQUOTE', '"'), rows[0][2]
    except IndexError:
        return None, False  # Default toggle status is False when no welcome message is set

def delete_welcome(group_id):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'DELETE FROM welcomes WHERE (group_id = ?)', (group_id,))
    conn.commit()
    conn.close()
def retrieve_group_lock_status(group_jid):
    try:
        with sqlite3.connect('db.sqlite3') as conn:
            curr = conn.cursor()
            curr.execute('SELECT lock FROM groups WHERE group_id = ?', (group_jid,))
            result = curr.fetchone()

        if result:
            return result[0] == "True"
        else:
            return False
    except sqlite3.Error as e:
        print(f"Error retrieving group lock status: {e}")
        return False

def toggle_group_lock(group_jid, toggle):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'UPDATE groups SET lock = ? WHERE group_id = ?', (str(toggle), group_jid))
    conn.commit()
    conn.close()

def is_locked(group_id):
    try:
        with sqlite3.connect('db.sqlite3') as conn:
            curr = conn.cursor()
            curr.execute('SELECT lock FROM groups WHERE group_id=?', (group_id,))
            existing_group = curr.fetchone()

        if existing_group:
            return existing_group[0] == "True"
        else:
            return False
    except sqlite3.Error as e:
        print(f"Error checking if group is locked: {e}")
        return False

def reset_group(group_id):
    conn = sqlite3.connect('db.sqlite3')
    curr = conn.cursor()
    curr.execute(f'DELETE FROM groups WHERE (group_id = ?)', (group_id,))
    curr.execute(f'DELETE FROM admins WHERE (group_id = ?)', (group_id,))
    curr.execute(f'DELETE FROM triggers WHERE (group_jid = ?)', (group_id,))
    curr.execute(f'DELETE FROM censored WHERE (group_jid = ?)', (group_id,))
    conn.commit()
    conn.close()

