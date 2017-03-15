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

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    #words
    greetings = ['hi', 'hei', 'hai', 'hello', 'hy', 'oi']
  
    try:
        payload = request.get_data()
        sender, message = messaging_events(payload)

        #greetings
        #if any(greeting() == message.lower() for greeting in greetings):
        #    send_text_message(sender, "Hi there!")
        if message == 'hi':
            send_text_message(sender, "hi tooooooooo")
        #help
        elif message.lower() == 'help':
            send_button_template_message(sender, "What can I help you?",
                [
                    generate_button(
                        "show me examples"
                        ),
                    generate_button(
                        "show my reminders"
                        )
                ])
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
        else:
            send_text_message(sender, "Sorry I'm just a little ducky")
            
    except: 
        pass        
    return "ok"

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True)
