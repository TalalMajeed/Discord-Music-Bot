#Create a Hello World Flask app
from flask import Flask
from bot import bot
import os
import threading

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    # Start the bot in a new thread
    bot_thread = threading.Thread(target=bot.run, args=(os.environ.get('TOKEN'),))
    app.run(debug=True, port=80)