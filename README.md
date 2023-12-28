# Instagram-Follow-Scraper
Instagram bot that scrapes follower/following data from a target user, then tells you what data has changed since it was ran previously

Once file is opened, insert corresponding data:
login_username --> the username of the account you will login to
login_password --> the password of the account you will login to
target_user --> the username of the account you wish to check status of

Ignore error responses outputting html/css in the console, the program will handle exceptions within 30 seconds
The first time you run it will initialize a database with the current data
Everytime you run it after that it will tell you in the terminal what data has changed
You must be following the target user for this code to work properly unless the users account is public

Fixes/Improvements:
- cookies now clear using relative path
- database initializes using relative path
- improved exception handling
- conventional connection handling
- bot now logs out when program is finished executing

Issues:
InstaBot sometimes grabs duplicate user ids/leaves out user ids in the _get_followers_following(): function, this makes the program suboptimal

The information provided in this program is for instructional purposes only, do not abuse this program.
