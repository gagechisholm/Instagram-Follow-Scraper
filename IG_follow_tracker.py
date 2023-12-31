import instabot
import sqlite3
import os

# Users and Password
login_username = 'insert_username_here'
login_password = 'insert_password_here'
target_user = 'insert_target_user_here'

# Get the current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize or connect sqlite database with a relative path
db_name = 'insta_followers.db'
db_path = os.path.join(current_dir, db_name)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Deletes old cookies if they exist using a relative path
cookie_file = f"{login_username}_uuid_and_cookie.json"
cookie_path = os.path.join(current_dir, 'config', cookie_file)
if os.path.isfile(cookie_path):
    os.remove(cookie_path)

# Create an instance of the InstaBot and login
bot = instabot.Bot()
bot.login(username=login_username, password=login_password)

# Drops old data if exists
cursor.execute('DROP TABLE IF EXISTS new_followers_id')
cursor.execute('DROP TABLE IF EXISTS new_following_id')

# Create necessary tables if they don't exist
cursor.execute('''
                CREATE TABLE IF NOT EXISTS followers_id (
                    id INTEGER PRIMARY KEY,
                    identity TEXT,
                    followed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
cursor.execute('''
                CREATE TABLE IF NOT EXISTS following_id (
                    id INTEGER PRIMARY KEY,
                    identity TEXT,
                    followed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
cursor.execute('''
                CREATE TABLE IF NOT EXISTS new_followers_id (
                    id INTEGER PRIMARY KEY,
                    identity TEXT,
                    followed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
cursor.execute('''
                CREATE TABLE IF NOT EXISTS new_following_id (
                    id INTEGER PRIMARY KEY,
                    identity TEXT,
                    followed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

# Helper function of store_db to get followers and following from Instagram API


def _get_followers_following():
    followers_by_id = bot.get_user_followers(target_user)
    following_by_id = bot.get_user_following(target_user)
    return followers_by_id, following_by_id

# Function to store followers and following data into the database


def store_db(follower_db_name, following_db_name):
    followers_by_id, following_by_id = _get_followers_following()

    for follower_id in followers_by_id:
        cursor.execute(
            f'INSERT INTO {follower_db_name} (identity) VALUES (?)', (follower_id,))

    for followed_id in following_by_id:
        cursor.execute(
            f'INSERT INTO {following_db_name} (identity) VALUES (?)', (followed_id,))
    conn.commit()

# Function to compare new followers/following with existing data


def get_compare_follow():

    cursor.execute('''
        SELECT identity FROM new_followers_id
        EXCEPT
        SELECT identity FROM followers_id
    ''')
    new_followers = [follower[0] for follower in cursor.fetchall()]

    cursor.execute('''
        SELECT identity FROM new_following_id
        EXCEPT
        SELECT identity FROM following_id
    ''')
    new_following = [followed[0] for followed in cursor.fetchall()]

    cursor.execute('''
        SELECT identity FROM followers_id
        EXCEPT
        SELECT identity FROM new_followers_id
    ''')
    unfollowed = [follower[0] for follower in cursor.fetchall()]

    cursor.execute('''
        SELECT identity FROM following_id
        EXCEPT
        SELECT identity FROM new_following_id
    ''')
    unfollowed_by = [followed[0] for followed in cursor.fetchall()]

    return new_followers, new_following, unfollowed, unfollowed_by

# Function to convert IDs to usernames using Instagram API


def convert_id_to_name(id_list):
    name_list = []
    for id in id_list:
        name_list.append(bot.get_username_from_user_id(id))
    return name_list

# Function to update the database after comparisons


def update_db():
    cursor.execute('DROP TABLE IF EXISTS followers_id')
    cursor.execute('DROP TABLE IF EXISTS following_id')
    cursor.execute('ALTER TABLE new_followers_id RENAME TO followers_id')
    cursor.execute('ALTER TABLE new_following_id RENAME TO following_id')
    conn.commit()

# Function to find and display changes in followers and following


def find_changes():
    try:
        cursor.execute(f"SELECT COUNT(*) FROM followers_id;")
        row_count = cursor.fetchone()[0]

        print(f"Row count in followers_id table: {row_count}")

        if row_count == 0:
            print('First run detected. Initializing Database')
            store_db('followers_id', 'following_id')
            print(f"Database Initialized, run again to see changes.")
        else:
            store_db('new_followers_id', 'new_following_id')
            new_followers, new_following, unfollowed, unfollowed_by = get_compare_follow()
            new_followers_by_name = convert_id_to_name(new_followers)
            new_following_by_name = convert_id_to_name(new_following)
            unfollowed_by_name = convert_id_to_name(unfollowed)
            unfollowed_by_by_name = convert_id_to_name(unfollowed_by)

            print('New Followers: ', new_followers_by_name)
            print('New Following: ', new_following_by_name)
            print('Unfollowed: ', unfollowed_by_name)
            print('Unfollowed By: ', unfollowed_by_by_name)

            update_db()
    except Exception as e:
        print(f'An error has occurred: {e}. Logging out.')
        bot.logout()

# Close the database connection and logs out of the account


def close_connections():
    try:
        conn.commit()
        conn.close()
        bot.logout()
    except Exception as e:
        print(f'Error while closing connections: {e}')


# Call function to find and display changes
try:
    find_changes()
except Exception as e:
    print(f'Error in main process: {e}')
    bot.logout()

close_connections()
