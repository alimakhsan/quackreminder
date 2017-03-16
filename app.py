import os
import sys
import json
import string

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

        get_message(data)

        payload = request.get_data()
        sender, message = messaging_events(payload)

        message_length = message.len()

        #greetings
        if any(greeting == message.lower() for greeting in greetings):
            send_text_message(sender, "Hi there!")

        #help
        elif 'help' in message.lower():
            send_replies(
                sender, 
                "What can I help you?",
                [
                    quick_reply(
                        "show me examples",
                        "show me examples"),
                    quick_reply(
                        "my reminders",
                        "my reminders")
                ])

        #show examples

        #handle task 1   
        elif 'meeting' in message.lower():
            send_button_template_message(
                sender,
                "Ok. I will remind you " + message.lower(),
                [
                    generate_button(
                        "reschedule",
                        "reschedule",
                        "text",
                        None),
                    generate_button(
                        "show my reminders",
                        "show my reminders",
                        "text",
                        None)
                ])

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
