from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return("<p style=\"color:rgb(88, 101, 242);font-family:\'Segoe UI\'\">Discord Bot is Online</p>")

def run():
    app.run(host='0.0.0.0',port=8080)

def render():
  t = Thread(target=run)
  t.start()
