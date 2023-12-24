# Instagram-Follow-Scraper
Instagram bot that scrapes follower/following data from a target user, then tells you what data has changed since it was ran previously

Once file is opened, insert corresponding data
login_username --> the username of the account you will login to
login_password --> the password of the account you will login to
target_user --> the username of the account you wish to check status of
if os.path.isfile --> insert path to where your file is stored, only change what is marked to change
os.remove --> insert path to where your file is stored, only change what is marked to change

The first time you run it will initialize a database with the current data
Everytime you run it after that it will tell you in the terminal what data has changed
You must be following the user for this code to work properly, it does not work on private accounts

The information provided in this program is for instructional purposes only, do not abuse this program.
