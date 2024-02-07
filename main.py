#Create a Hello World Flask app
from flask import Flask
from bot import bot
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    bot.run(os.environ.get('TOKEN'))
    app.run(debug=True, port=80)