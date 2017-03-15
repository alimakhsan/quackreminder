import os
import sys
import json

import requests
from flask import Flask, request
from util import *
import traceback
import random
app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

# word 
greeting = ["hi", "hei", "hai", "hello", "hy", "oi"]

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
  
    try:
        payload = request.get_data()
        sender, message = messaging_events(payload)

        #greetings
        if any(greeting() for greeting in message.lower()):
            send_text_message(sender, "Hi there!")

        #help
        if message == "help":
            send_text_message(sender , "You can choose topic you would like to learn and practice from the menu on left. For more information you can drop us a message and we will reply back to you shortly. ")

        #show examples
        #handle task 1    
        #handle task 2
        #handle task 3
        #handle task 4
        #handle task 5
        #handle task 6
        #handle task 7
        #handle task 8
        #handle task 9
        #handle task 10

        if message == "topics_to_learn":
            send_replies(
                sender, 
                "Select the topic you want to learn? 1.) Rational Numbers <br/> 2.) Linear Equation in One variable /n 3.) Understanding Quadrilaterals",
                [
                    quick_reply(
                        "1",
                        "rat"),
                    quick_reply(
                        "2",
                        "LINEAR"),
                    quick_reply(
                        "3",
                        "QUAD"),
                    quick_reply(
                        "4",
                        "BT"),
                    quick_reply(
                        "5",
                        "ON"),
                    quick_reply(
                        "6",
                        "LINEAR"),
                    quick_reply(
                        "7",
                        "QUAD"),
                    quick_reply(
                        "8",
                        "BT"),
                    quick_reply(
                        "more",
                        "BT")])
            
    except: 
        pass        
    return "ok"

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
